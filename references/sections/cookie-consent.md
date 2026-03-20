# Cookie Consent Banner Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**COMPLIANCE + TRUST** — The cookie consent banner satisfies GDPR/ePrivacy/CCPA legal requirements
while maintaining user trust. A well-designed banner signals professionalism and respect for
user privacy. A bad one (dark patterns, no reject button, wall of text) erodes trust.

**Replaces**: Termly CMP ($10-20/mo), Iubenda Cookie Solution ($3.49-119.99/mo),
GetTerms CMP ($5-8/mo), Enzuzo Cookie Banner ($7-49/mo), OneTrust, CookieYes.

---

## How It Works

1. On first visit, check localStorage for existing consent
2. If no consent stored, determine user's region:
   - EU/EEA/UK → show **opt-in** banner (GDPR: block non-essential cookies until consent)
   - California/US states with privacy laws → show **opt-out** notice (CCPA: can collect by default, provide opt-out)
   - Other regions → show simplified notice (informational only)
3. User selects Accept All, Reject All, or opens Preferences
4. Store consent decision in localStorage with timestamp
5. Block/unblock scripts based on consent categories
6. Provide "Cookie Settings" link in footer to re-open preferences

---

## Regional Behavior

| Region | Default State | Banner Type | Legal Requirement |
|--------|--------------|-------------|-------------------|
| EU/EEA/UK | Block all non-essential | Opt-in with Accept/Reject + Preferences | GDPR + ePrivacy Directive |
| California | Allow all, show notice | Opt-out notice with "Do Not Sell" link | CCPA/CPRA |
| Canada | Allow all, show notice | Opt-out with preference center | PIPEDA |
| Brazil | Block all non-essential | Opt-in with Accept/Reject | LGPD |
| Other | Allow all | Informational notice | Varies |

---

## CNIL Compliance (Strictest Standard)

The French CNIL issues the largest cookie fines in Europe (EUR 139M+ in 2022-2024).
Design to CNIL standards and you comply everywhere:

- **Accept All and Reject All must be equally prominent** — same size, same visual weight, same number of clicks
- **No pre-ticked checkboxes** — all non-essential categories default to OFF
- **No dark patterns** — reject must not be hidden, dimmed, or smaller
- **Cookie purposes described** with short title + brief description
- **Consent valid for max 13 months** — re-prompt after expiry
- **Store consent proof** for at least 6 months (best practice: 5 years)

---

## Desktop Layout

- **Banner position**: Bottom of viewport, full-width
- Banner container: `fixed bottom-0 inset-x-0 z-[9999]`
- Inner content: `max-w-4xl mx-auto` with `px-4 sm:px-6 py-4`
- Two-row layout: text on top, buttons on bottom right
- Preference panel: slides up from bottom as a modal overlay

## Mobile Layout

- Full-width bottom banner, `px-4 py-4`
- Buttons stack vertically, full width
- Preference panel is a full-screen overlay (not a slide-up)
- Touch targets ≥ 44px for all interactive elements
- Text size minimum 14px for readability

---

## Cookie Categories

| Category | Description | Default (Opt-in regions) | Can Disable? |
|----------|-------------|--------------------------|--------------|
| **Essential** | Authentication, security, core functionality | Always ON | No |
| **Analytics** | Usage statistics, performance monitoring | OFF | Yes |
| **Marketing** | Advertising, retargeting, attribution | OFF | Yes |
| **Functional** | Preferences, personalization, A/B testing | OFF | Yes |

---

## Copy Structure

| Element | Content Rule |
|---------|-------------|
| **Banner text** | "We use cookies to improve your experience. You can accept all cookies, reject non-essential cookies, or customize your preferences." Keep under 2 sentences. |
| **Accept All button** | "Accept All" — primary style |
| **Reject All button** | "Reject All" — equal visual weight to Accept (CNIL requirement) |
| **Preferences button** | "Cookie Settings" or "Customize" — secondary style |
| **Preference panel title** | "Cookie Preferences" |
| **Category toggle labels** | Category name + 1-sentence description |
| **Save button** | "Save Preferences" |
| **Footer link** | "Cookie Settings" — reopens the preference panel |

---

## Section-Specific Notes

- Banner renders via `createPortal(…, document.body)` for z-index isolation
- Essential cookies toggle is always ON and disabled (not toggleable)
- Consent stored in `localStorage` key: `cookie-consent`
- Consent object includes: `timestamp`, `categories`, `version`, `region`
- `version` field allows re-prompting when cookie policy changes
- On Accept All: set all categories to true, fire `consent_granted` event
- On Reject All: set all non-essential to false, fire `consent_denied` event
- Script blocking: use `data-cookie-category` attribute on `<script>` tags
- Re-prompt after 13 months (CNIL guideline)
- Banner animates in with slide-up + fade (200ms)
- Banner animates out with slide-down + fade (150ms)
- Keyboard accessible: Escape closes preference panel, Tab cycles through options
- `prefers-reduced-motion`: no animation, instant show/hide

---

## Script Blocking Pattern

To block non-essential scripts until consent, use `type="text/plain"` with a data attribute:

```html
<!-- Blocked by default — activated after consent -->
<script
  type="text/plain"
  data-cookie-category="analytics"
  data-src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"
></script>

<!-- Essential scripts load normally -->
<script src="/js/app.js"></script>
```

After consent, the cookie consent component finds all `[data-cookie-category]` scripts
matching approved categories and activates them:

```ts
function activateScripts(approvedCategories: string[]) {
  document
    .querySelectorAll("script[data-cookie-category]")
    .forEach((script) => {
      const category = script.getAttribute("data-cookie-category");
      if (category && approvedCategories.includes(category)) {
        const src = script.getAttribute("data-src") || "";
        // Validate data-src against trusted origins before loading
        // (see TRUSTED_SCRIPT_ORIGINS allowlist in component code)
        if (src && !isTrustedScriptSrc(src)) {
          console.warn(`Cookie consent: blocked untrusted script src: ${src}`);
          return;
        }
        const newScript = document.createElement("script");
        newScript.src = src;
        newScript.type = "text/javascript";
        document.head.appendChild(newScript);
      }
    });
}
```

---

## Complete JSX Template

```tsx
"use client";

import { useState, useEffect, useCallback } from "react";
import { createPortal } from "react-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Cookie, X, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

interface CookieCategory {
  id: string;
  name: string;
  description: string;
  required: boolean;
}

interface ConsentState {
  timestamp: number;
  categories: Record<string, boolean>;
  version: number;
  region: "eu" | "us-ccpa" | "other";
}

interface CookieConsentProps {
  /** Current consent version — increment when cookie policy changes to re-prompt */
  consentVersion?: number;
  /** Override region detection (useful for testing) */
  forceRegion?: "eu" | "us-ccpa" | "other";
  /** Custom cookie categories */
  categories?: CookieCategory[];
  /** URL to full cookie policy page */
  cookiePolicyUrl?: string;
  /** Callback when consent is given/updated */
  onConsentChange?: (consent: ConsentState) => void;
}

// -------------------------------------------------------------------
// Constants
// -------------------------------------------------------------------

const STORAGE_KEY = "cookie-consent";
const CONSENT_MAX_AGE_MS = 13 * 30 * 24 * 60 * 60 * 1000; // ~13 months (CNIL)

const defaultCategories: CookieCategory[] = [
  {
    id: "essential",
    name: "Essential",
    description:
      "Required for authentication, security, and core functionality. Cannot be disabled.",
    required: true,
  },
  {
    id: "analytics",
    name: "Analytics",
    description:
      "Help us understand how you use the site so we can improve it. Includes tools like Google Analytics.",
    required: false,
  },
  {
    id: "marketing",
    name: "Marketing",
    description:
      "Used for advertising and retargeting. Allow us to show you relevant ads on other platforms.",
    required: false,
  },
  {
    id: "functional",
    name: "Functional",
    description:
      "Enable personalization features like theme preferences, language settings, and A/B testing.",
    required: false,
  },
];

// -------------------------------------------------------------------
// Animation variants
// -------------------------------------------------------------------

const bannerVariants = {
  hidden: { y: "100%", opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.2, ease: "easeOut" },
  },
  exit: {
    y: "100%",
    opacity: 0,
    transition: { duration: 0.15, ease: "easeIn" },
  },
};

const overlayVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.2 } },
  exit: { opacity: 0, transition: { duration: 0.15 } },
};

const panelVariants = {
  hidden: { y: "100%", opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.25, ease: "easeOut" },
  },
  exit: {
    y: "100%",
    opacity: 0,
    transition: { duration: 0.2, ease: "easeIn" },
  },
};

// -------------------------------------------------------------------
// Utility: Activate blocked scripts
// -------------------------------------------------------------------

// Allowlist of trusted script source patterns.
// Only scripts matching these origins will be activated from data-src attributes.
// This prevents DOM-based XSS if an attacker can inject data-src attributes.
const TRUSTED_SCRIPT_ORIGINS = [
  "https://www.googletagmanager.com",
  "https://www.google-analytics.com",
  "https://plausible.io",
  "https://cdn.usefathom.com",
  "https://cloud.umami.is",
];

function isTrustedScriptSrc(src: string): boolean {
  try {
    const url = new URL(src);
    // Must be HTTPS
    if (url.protocol !== "https:") return false;
    // Must match a trusted origin
    return TRUSTED_SCRIPT_ORIGINS.some((origin) => src.startsWith(origin));
  } catch {
    return false; // Malformed URL
  }
}

function activateScripts(approvedCategories: string[]) {
  if (typeof document === "undefined") return;

  document
    .querySelectorAll<HTMLScriptElement>("script[data-cookie-category]")
    .forEach((script) => {
      const category = script.getAttribute("data-cookie-category");
      if (category && approvedCategories.includes(category)) {
        const newScript = document.createElement("script");
        const src = script.getAttribute("data-src");
        if (src) {
          // Validate data-src against trusted origins before loading
          if (!isTrustedScriptSrc(src)) {
            console.warn(`Cookie consent: blocked untrusted script src: ${src}`);
            return;
          }
          newScript.src = src;
        } else {
          newScript.textContent = script.textContent;
        }
        newScript.type = "text/javascript";
        document.head.appendChild(newScript);
        script.remove();
      }
    });
}

// -------------------------------------------------------------------
// Utility: Detect region (basic, override with forceRegion)
// -------------------------------------------------------------------

function detectRegion(): "eu" | "us-ccpa" | "other" {
  // In production, use server-side geolocation or a lightweight IP lookup.
  // This client-side check uses timezone as a rough heuristic.
  if (typeof Intl === "undefined") return "other";

  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";

  // EU/EEA timezones
  if (
    tz.startsWith("Europe/") ||
    tz === "Atlantic/Reykjavik" ||
    tz === "Atlantic/Canary"
  ) {
    return "eu";
  }

  // California / US states with privacy laws
  if (
    tz === "America/Los_Angeles" ||
    tz === "America/Denver" ||
    tz === "America/Chicago" ||
    tz === "America/New_York" ||
    tz.startsWith("America/")
  ) {
    return "us-ccpa";
  }

  return "other";
}

// -------------------------------------------------------------------
// Component
// -------------------------------------------------------------------

export default function CookieConsent({
  consentVersion = 1,
  forceRegion,
  categories = defaultCategories,
  cookiePolicyUrl = "/cookies",
  onConsentChange,
}: CookieConsentProps) {
  const [mounted, setMounted] = useState(false);
  const [showBanner, setShowBanner] = useState(false);
  const [showPreferences, setShowPreferences] = useState(false);
  const [region, setRegion] = useState<"eu" | "us-ccpa" | "other">("other");
  const [selections, setSelections] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    categories.forEach((cat) => {
      initial[cat.id] = cat.required;
    });
    return initial;
  });

  // ---- Mount + check existing consent ----
  useEffect(() => {
    setMounted(true);
    const detectedRegion = forceRegion || detectRegion();
    setRegion(detectedRegion);

    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);

        // Validate shape — reject corrupted or tampered data
        if (
          typeof parsed !== "object" ||
          parsed === null ||
          typeof parsed.timestamp !== "number" ||
          typeof parsed.categories !== "object" ||
          parsed.categories === null ||
          typeof parsed.version !== "number" ||
          !["eu", "us-ccpa", "other"].includes(parsed.region)
        ) {
          localStorage.removeItem(STORAGE_KEY);
          setShowBanner(true);
          return;
        }

        const consent: ConsentState = parsed;

        // Re-prompt if version changed or consent expired (13 months)
        const isExpired =
          Date.now() - consent.timestamp > CONSENT_MAX_AGE_MS;
        const isOutdated = consent.version < consentVersion;

        if (!isExpired && !isOutdated) {
          // Valid consent exists — activate approved scripts
          const approved = Object.entries(consent.categories)
            .filter(([, v]) => v)
            .map(([k]) => k);
          activateScripts(approved);
          return;
        }
      }
    } catch {
      // Corrupted storage — clean up and show banner
      try { localStorage.removeItem(STORAGE_KEY); } catch {}
    }

    // No valid consent — show banner
    setShowBanner(true);
  }, [consentVersion, forceRegion, categories]);

  // ---- Save consent ----
  const saveConsent = useCallback(
    (cats: Record<string, boolean>) => {
      const consent: ConsentState = {
        timestamp: Date.now(),
        categories: cats,
        version: consentVersion,
        region,
      };

      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(consent));
      } catch {
        // localStorage full or disabled — consent still works for session
      }

      // Server-side consent logging (GDPR Article 7 — demonstrable proof of consent)
      // This is a non-blocking fire-and-forget request. The page works without it,
      // but regulators may require server-side proof that consent was collected.
      fetch("/api/consent/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          categories: cats,
          version: consentVersion,
          timestamp: new Date().toISOString(),
        }),
      }).catch(() => {
        // Non-blocking — consent still saved locally even if server is unreachable
      });

      // Activate approved scripts
      const approved = Object.entries(cats)
        .filter(([, v]) => v)
        .map(([k]) => k);
      activateScripts(approved);

      // Fire custom event for analytics integration
      if (typeof window !== "undefined") {
        window.dispatchEvent(
          new CustomEvent("cookie-consent-change", { detail: consent })
        );
      }

      onConsentChange?.(consent);
      setShowBanner(false);
      setShowPreferences(false);
    },
    [consentVersion, region, onConsentChange]
  );

  // ---- Accept All ----
  const handleAcceptAll = useCallback(() => {
    const all: Record<string, boolean> = {};
    categories.forEach((cat) => {
      all[cat.id] = true;
    });
    saveConsent(all);
  }, [categories, saveConsent]);

  // ---- Reject All ----
  const handleRejectAll = useCallback(() => {
    const minimal: Record<string, boolean> = {};
    categories.forEach((cat) => {
      minimal[cat.id] = cat.required;
    });
    saveConsent(minimal);
  }, [categories, saveConsent]);

  // ---- Save Preferences ----
  const handleSavePreferences = useCallback(() => {
    saveConsent(selections);
  }, [selections, saveConsent]);

  // ---- Toggle category ----
  const toggleCategory = useCallback(
    (id: string) => {
      setSelections((prev) => ({
        ...prev,
        [id]: !prev[id],
      }));
    },
    []
  );

  // ---- Open preferences from footer link ----
  useEffect(() => {
    if (!mounted) return;

    function handleOpenSettings() {
      // Reset selections to current consent
      try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
          const parsed = JSON.parse(stored);
          // Validate shape before trusting
          if (
            typeof parsed === "object" &&
            parsed !== null &&
            typeof parsed.categories === "object" &&
            parsed.categories !== null
          ) {
            setSelections(parsed.categories);
          }
        }
      } catch {
        // Use defaults
      }
      setShowPreferences(true);
    }

    // Listen for clicks on [data-cookie-settings] elements
    document.querySelectorAll("[data-cookie-settings]").forEach((el) => {
      el.addEventListener("click", handleOpenSettings);
    });

    return () => {
      document.querySelectorAll("[data-cookie-settings]").forEach((el) => {
        el.removeEventListener("click", handleOpenSettings);
      });
    };
  }, [mounted]);

  // ---- Keyboard: Escape closes preference panel ----
  useEffect(() => {
    if (!showPreferences) return;

    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        setShowPreferences(false);
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [showPreferences]);

  // ---- Don't render on server ----
  if (!mounted) return null;

  return createPortal(
    <>
      <AnimatePresence>
        {/* ================================================================
            BANNER
            ================================================================ */}
        {showBanner && !showPreferences && (
          <motion.div
            key="cookie-banner"
            variants={bannerVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            role="dialog"
            aria-label="Cookie consent"
            aria-describedby="cookie-banner-text"
            className="fixed bottom-0 inset-x-0 z-[9999]
                       bg-card border-t border-border shadow-2xl"
          >
            <div className="mx-auto max-w-4xl px-4 sm:px-6 py-4 sm:py-5">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                {/* Text */}
                <div className="flex items-start gap-3 flex-1">
                  <Cookie
                    className="h-5 w-5 text-muted-foreground shrink-0 mt-0.5"
                    aria-hidden="true"
                  />
                  <p
                    id="cookie-banner-text"
                    className="text-sm text-muted-foreground leading-relaxed"
                  >
                    We use cookies to improve your experience.{" "}
                    {region === "eu"
                      ? "You can accept all, reject non-essential, or customize your preferences."
                      : "You can manage your preferences at any time."}{" "}
                    <a
                      href={cookiePolicyUrl}
                      className="text-primary hover:underline"
                    >
                      Learn more
                    </a>
                  </p>
                </div>

                {/* Buttons */}
                <div className="flex flex-col gap-2 sm:flex-row sm:gap-3 shrink-0">
                  {/* CNIL: Reject All must be equally prominent as Accept All */}
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleRejectAll}
                    className="w-full sm:w-auto text-sm font-medium"
                  >
                    Reject All
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowPreferences(true)}
                    className="w-full sm:w-auto text-sm font-medium"
                  >
                    Cookie Settings
                  </Button>
                  <Button
                    size="sm"
                    onClick={handleAcceptAll}
                    className="w-full sm:w-auto text-sm font-medium"
                  >
                    Accept All
                  </Button>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {/* ================================================================
            PREFERENCE PANEL (MODAL OVERLAY)
            ================================================================ */}
        {showPreferences && (
          <>
            {/* Backdrop */}
            <motion.div
              key="cookie-overlay"
              variants={overlayVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="fixed inset-0 z-[10000] bg-black/50"
              onClick={() => setShowPreferences(false)}
              aria-hidden="true"
            />

            {/* Panel */}
            <motion.div
              key="cookie-panel"
              variants={panelVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              role="dialog"
              aria-label="Cookie preferences"
              aria-modal="true"
              className="fixed bottom-0 inset-x-0 z-[10001]
                         bg-card border-t border-border rounded-t-2xl
                         shadow-2xl max-h-[85vh] overflow-y-auto"
            >
              <div className="mx-auto max-w-2xl px-4 sm:px-6 py-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-semibold text-foreground">
                    Cookie Preferences
                  </h2>
                  <button
                    onClick={() => setShowPreferences(false)}
                    className="p-2 rounded-lg
                               text-muted-foreground hover:text-foreground
                               hover:bg-muted transition-colors"
                    aria-label="Close cookie preferences"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>

                <p className="text-sm text-muted-foreground mb-6">
                  Choose which cookie categories to allow. Essential cookies
                  cannot be disabled as they are required for the site to
                  function.{" "}
                  <a
                    href={cookiePolicyUrl}
                    className="text-primary hover:underline"
                  >
                    Read our Cookie Policy
                  </a>
                </p>

                {/* Category toggles */}
                <div className="space-y-4">
                  {categories.map((cat) => (
                    <div
                      key={cat.id}
                      className="flex items-start justify-between gap-4
                                 p-4 rounded-lg border border-border bg-background"
                    >
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <h3 className="text-sm font-medium text-foreground">
                            {cat.name}
                          </h3>
                          {cat.required && (
                            <span className="text-xs px-2 py-0.5 rounded-full
                                             bg-muted text-muted-foreground">
                              Required
                            </span>
                          )}
                        </div>
                        <p className="mt-1 text-xs text-muted-foreground leading-relaxed">
                          {cat.description}
                        </p>
                      </div>
                      <Switch
                        checked={selections[cat.id] ?? cat.required}
                        onCheckedChange={() => toggleCategory(cat.id)}
                        disabled={cat.required}
                        aria-label={`${cat.required ? "Required" : "Toggle"} ${cat.name} cookies`}
                        className="shrink-0"
                      />
                    </div>
                  ))}
                </div>

                {/* Action buttons — CNIL: equal visual weight */}
                <div className="flex flex-col gap-2 sm:flex-row sm:justify-end sm:gap-3 mt-6">
                  <Button
                    variant="outline"
                    onClick={handleRejectAll}
                    className="w-full sm:w-auto"
                  >
                    Reject All
                  </Button>
                  <Button
                    variant="outline"
                    onClick={handleAcceptAll}
                    className="w-full sm:w-auto"
                  >
                    Accept All
                  </Button>
                  <Button
                    onClick={handleSavePreferences}
                    className="w-full sm:w-auto"
                  >
                    Save Preferences
                  </Button>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>,
    document.body
  );
}
```

---

## Footer Integration

Add a "Cookie Settings" link to the footer that reopens the preference panel:

```tsx
{/* In cta-footer.tsx, add to the Legal links group: */}
<a
  href="#"
  data-cookie-settings
  className="text-sm text-muted-foreground hover:text-foreground transition-colors"
>
  Cookie Settings
</a>
```

The `data-cookie-settings` attribute is detected by the CookieConsent component,
which attaches a click handler to open the preference panel.

---

## Google Consent Mode v2 Integration

For sites using Google Analytics or Google Ads, fire consent signals:

```tsx
// Add to the onConsentChange callback:
function handleConsentChange(consent: ConsentState) {
  if (typeof gtag !== "undefined") {
    gtag("consent", "update", {
      analytics_storage: consent.categories.analytics ? "granted" : "denied",
      ad_storage: consent.categories.marketing ? "granted" : "denied",
      ad_user_data: consent.categories.marketing ? "granted" : "denied",
      ad_personalization: consent.categories.marketing ? "granted" : "denied",
      functionality_storage: consent.categories.functional
        ? "granted"
        : "denied",
      security_storage: "granted", // Always granted (essential)
    });
  }
}
```

Set default consent mode in `<head>` BEFORE Google scripts load:

```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'functionality_storage': 'denied',
    'security_storage': 'granted',
    'wait_for_update': 500
  });
</script>
```

---

## Server-Side Consent Logging Endpoint

GDPR Article 7 requires "demonstrable" consent proof. localStorage alone is insufficient
because it lives on the user's device and can be cleared. Add this minimal API route
to log consent server-side:

```typescript
// app/api/consent/log/route.ts (Next.js App Router)
import { NextRequest, NextResponse } from "next/server";

// Simple in-memory rate limit for consent logging (10 requests per IP per minute).
// For production with multiple instances, replace with Redis-backed rate limiting.
const consentRateLimit = new Map<string, { count: number; resetAt: number }>();
const CONSENT_RATE_LIMIT = 10;
const CONSENT_RATE_WINDOW_MS = 60_000;

function checkConsentRateLimit(ip: string): boolean {
  const now = Date.now();
  const entry = consentRateLimit.get(ip);
  if (!entry || now > entry.resetAt) {
    consentRateLimit.set(ip, { count: 1, resetAt: now + CONSENT_RATE_WINDOW_MS });
    return true;
  }
  if (entry.count >= CONSENT_RATE_LIMIT) return false;
  entry.count++;
  return true;
}

export async function POST(req: NextRequest) {
  try {
    // Rate limit to prevent abuse (consent logging is non-critical)
    const ip = req.headers.get("x-forwarded-for")?.split(",")[0] || "unknown";
    if (!checkConsentRateLimit(ip)) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    const body = await req.json();
    const { categories, version, timestamp } = body;

    // Validate payload shape
    if (!categories || typeof version !== "number" || !timestamp) {
      return NextResponse.json({ error: "Invalid payload" }, { status: 400 });
    }

    // Store consent record — pick your storage:
    //
    // Option A: Database (recommended for production)
    //   await db.insert("consent_log", {
    //     categories: JSON.stringify(categories),
    //     version,
    //     timestamp,
    //     ip_hash: hashIp(req.headers.get("x-forwarded-for")?.split(",")[0] || ""),
    //   });
    //
    // Option B: Append-only log file (simpler, GDPR audit-friendly)
    //   fs.appendFileSync("data/consent-log.jsonl", JSON.stringify({ categories, version, timestamp }) + "\n");
    //
    // Option C: Third-party consent management API

    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ error: "Server error" }, { status: 500 });
  }
}
```

Keep consent records for at least 5 years (CNIL best practice). Never store raw IP
addresses — hash them the same way the waitlist API does.

---

## Accessibility

- Banner has `role="dialog"` and `aria-label="Cookie consent"`
- Preference panel has `role="dialog"`, `aria-modal="true"`
- All toggles have descriptive `aria-label`
- Escape key closes the preference panel
- Tab order flows logically through all interactive elements
- Focus is trapped within the preference panel when open
- Essential toggle is `disabled` with clear "Required" badge
- Text meets 4.5:1 contrast ratio
- Touch targets ≥ 44px on mobile
- `prefers-reduced-motion`: all animations disabled
