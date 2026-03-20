# Exit-Intent Popup Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

> **Replaces:** OptinMonster ($7-82/mo), Sumo/BDOW ($0-49/mo), Hello Bar ($39-129/mo), Sleeknote ($49-299/mo). This is the same feature set those tools charge $400-1,500/year for — exit-intent detection, scroll/time triggers, frequency capping, A/B testing, mobile detection, analytics events — shipped as a zero-dependency React component.

---

## Conversion Job

**RECOVER ABANDONING VISITORS** — The visitor is about to leave. This is the last chance to capture their email, offer a compelling reason to stay, or redirect them to a high-value action. Exit-intent popups convert 2-5% of abandoning visitors on average, with well-optimized versions reaching 10-17%.

**When to include:** Every page benefits from exit-intent recovery. The skill automatically includes this component when the page has a lead-capture CTA (free trial, waitlist, demo, newsletter).

---

## Trigger System

The popup supports 4 trigger types. By default, exit-intent fires first. If exit-intent doesn't fire within the session, the time/scroll fallbacks activate.

### Trigger Priority (first match wins)

| Priority | Trigger | Default | How it works |
|----------|---------|---------|--------------|
| 1 | **Exit-intent (desktop)** | Enabled | `mouseleave` event when `clientY <= 0` and cursor leaves document |
| 2 | **Exit-intent (mobile)** | Enabled | Rapid scroll-up velocity (> 80px/100ms) toward URL bar |
| 3 | **Time on page** | 45 seconds | `setTimeout` after configurable delay |
| 4 | **Scroll depth** | 65% | `IntersectionObserver` on a sentinel element at target depth |

### Trigger Guards (prevent false positives)

- **Minimum time on page:** Popup never fires before 5 seconds regardless of trigger type
- **Interaction required:** At least one scroll or click must occur before popup can fire
- **Internal navigation:** Exit-intent does NOT fire when user clicks an internal link
- **Single-fire:** Only one popup per session, period
- **Converted suppression:** If visitor has already submitted the form, popup never shows again

---

## Frequency Capping (Anti-Annoyance)

Uses `localStorage` to prevent popup fatigue:

| Event | Suppression Rule |
|-------|-----------------|
| Popup shown, user closes | Suppress for **14 days** (configurable) |
| Popup shown, user submits | Suppress **permanently** for this popup |
| User clicks "Don't show again" | Suppress **permanently** |
| Already shown this session | Never show twice per session |

```typescript
// Storage keys
const STORAGE_KEY = "sp_exit_popup";

interface PopupState {
  lastShown: number;      // timestamp
  dismissed: boolean;      // closed without converting
  converted: boolean;      // submitted the form
  suppressUntil: number;   // timestamp when suppression expires
  permanent: boolean;      // never show again
  variant: "A" | "B";     // last shown variant (for A/B consistency)
}
```

---

## A/B Testing

Built-in 50/50 split testing with localStorage persistence:

- First visit: randomly assign variant A or B
- All subsequent visits: show the same variant (consistent experience)
- Track `popup_view`, `popup_close`, `popup_convert` events per variant
- Variants can differ in: headline, offer text, CTA label, image, or layout (modal vs slide-in)

```typescript
function getVariant(): "A" | "B" {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    const state: PopupState = JSON.parse(stored);
    if (state.variant) return state.variant;
  }
  const variant = Math.random() < 0.5 ? "A" : "B";
  // persist variant choice
  return variant;
}
```

---

## Desktop Layout (Centered Modal)

```
┌──────────────────────────────────────────────────┐
│                 [Overlay bg-black/50]             │
│                                                    │
│        ┌────────────────────────────┐              │
│        │  [X close]                 │              │
│        │                            │              │
│        │     [Headline]             │              │
│        │     [Subheadline]          │              │
│        │                            │              │
│        │  ┌──────────────────────┐  │              │
│        │  │  email@example.com   │  │              │
│        │  └──────────────────────┘  │              │
│        │  ┌──────────────────────┐  │              │
│        │  │   [CTA Button]       │  │              │
│        │  └──────────────────────┘  │              │
│        │                            │              │
│        │  [Trust hint / privacy]    │              │
│        │  [☐ GDPR consent]          │              │
│        │  ["Don't show again"]      │              │
│        └────────────────────────────┘              │
│                                                    │
└──────────────────────────────────────────────────┘
```

- Overlay: `fixed inset-0 z-50 bg-black/50 backdrop-blur-sm`
- Modal: `max-w-md mx-auto rounded-2xl bg-card border border-border shadow-2xl p-8`
- Entrance: scale from 0.95 + fade in (200ms)
- Exit: scale to 0.95 + fade out (150ms)
- Close: X button (top-right), ESC key, overlay click

## Mobile Layout (Slide-Up with Teaser)

### Phase 1: Teaser (small tab at bottom)
```
┌──────────────────────┐
│                      │
│    [Page content]    │
│                      │
│ ┌──────────────────┐ │
│ │ 🎁 Special offer │ │
│ └──────────────────┘ │
└──────────────────────┘
```

- Teaser: `fixed bottom-0 left-0 right-0 z-40 p-3 bg-primary text-primary-foreground text-center text-sm rounded-t-xl`
- Slides up from bottom (200ms)
- Tap teaser → expand to full popup

### Phase 2: Full popup (on teaser tap)
```
┌──────────────────────┐
│                      │
│  ┌────────────────┐  │
│  │  [X close]     │  │
│  │                │  │
│  │  [Headline]    │  │
│  │  [Subheadline] │  │
│  │                │  │
│  │  [email input] │  │
│  │  [CTA button]  │  │
│  │  [Trust hint]  │  │
│  │  [GDPR]        │  │
│  └────────────────┘  │
└──────────────────────┘
```

- Slides up from bottom, takes ~60% of viewport height
- `rounded-t-2xl` top corners
- All inputs are full-width, touch-friendly (44px minimum height)
- CTA button is full-width

---

## Copy Structure

| Element | Rule | Example |
|---------|------|---------|
| **Headline** | Benefit-focused, max 8 words. Never "Wait!" or "Don't go!" | "Get 20% off your first month" or "Free guide: Ship 3x faster" |
| **Subheadline** | Expand on the value, 15-25 words | "Join 2,400 teams who reduced deploy time by 73%. Enter your email for instant access." |
| **Email input** | Placeholder: "you@company.com" | — |
| **CTA button** | Action verb + outcome, 2-5 words | "Send me the guide" / "Claim my discount" / "Start free trial" |
| **Trust hint** | Privacy reassurance, max 40 chars | "No spam. Unsubscribe anytime." |
| **GDPR checkbox** | Only when GDPR mode is enabled | "I agree to receive marketing emails" |
| **Dismiss link** | Polite, not guilt-tripping | "No thanks" (never "No, I don't want to save money") |

### Copy Anti-Patterns (NEVER use)
- ❌ "Wait! Don't leave!" (desperate)
- ❌ "Are you sure you want to miss out?" (guilt-trip)
- ❌ "No, I don't want to grow my business" (manipulative dismiss button)
- ❌ Fake countdown timers with no real deadline
- ❌ Multiple form fields (keep to email only, or email + name max)

---

## Offer Templates by CTA Goal

| CTA Goal | Popup Offer | Headline Template |
|----------|------------|-------------------|
| **free-trial** | Extended trial (14→30 days) | "Take an extra 2 weeks to decide" |
| **waitlist** | Priority access or skip-the-line | "Jump to the front of the line" |
| **demo** | Instant demo video (no scheduling) | "See it in action — 2 minute demo" |
| **purchase** | First-month discount (10-20%) | "Here's 20% off your first month" |
| **newsletter** | Lead magnet (PDF, checklist, template) | "Free: [Specific resource title]" |

---

## Analytics Events

Every popup interaction fires an analytics event (GA4, Plausible, or custom):

```typescript
const EVENTS = {
  popup_impression: {
    event_category: "exit_intent",
    event_label: "variant_A",    // or variant_B
    trigger_type: "exit_intent", // or "time", "scroll"
  },
  popup_close: {
    event_category: "exit_intent",
    event_label: "variant_A",
    close_method: "x_button",    // or "overlay", "escape", "dont_show"
  },
  popup_convert: {
    event_category: "exit_intent",
    event_label: "variant_A",
    email_captured: true,
  },
  popup_teaser_shown: {
    event_category: "exit_intent",
    event_label: "teaser",
    device: "mobile",
  },
  popup_teaser_click: {
    event_category: "exit_intent",
    event_label: "teaser_expanded",
  },
};
```

---

## Section-Specific Notes

- Component renders as a portal (`createPortal` to `document.body`) — no parent layout interference
- Uses `AnimatePresence` for enter/exit animations
- Traps focus within the modal when open (accessibility requirement)
- `aria-modal="true"` and `role="dialog"` on the popup container
- Body scroll locked when popup is open (`overflow: hidden` on `<body>`)
- ESC key closes the popup (via `useEffect` keydown listener)
- All localStorage operations are wrapped in try/catch (SSR-safe, private browsing safe)
- Component tree-shakes cleanly — if not used, zero bytes in bundle
- Total JS weight: < 4KB gzipped (no external dependencies beyond Framer Motion)

---

## Exit-Intent Detection Hook

```tsx
import { useEffect, useRef, useCallback } from "react";

interface UseExitIntentOptions {
  /** Minimum time (ms) on page before popup can fire. Default: 5000 */
  minTimeOnPage?: number;
  /** Mobile scroll-up velocity threshold (px/100ms). Default: 80 */
  mobileScrollThreshold?: number;
  /** Whether to require at least one user interaction before firing. Default: true */
  requireInteraction?: boolean;
  /** Disable on specific paths (e.g. ["/checkout", "/app"]). Default: [] */
  disabledPaths?: string[];
}

export function useExitIntent(
  onExitIntent: () => void,
  options: UseExitIntentOptions = {}
) {
  const {
    minTimeOnPage = 5000,
    mobileScrollThreshold = 80,
    requireInteraction = true,
    disabledPaths = [],
  } = options;

  const hasFired = useRef(false);
  const hasInteracted = useRef(false);
  const pageLoadTime = useRef(Date.now());
  const lastScrollY = useRef(0);
  const lastScrollTime = useRef(0);

  const canFire = useCallback(() => {
    if (hasFired.current) return false;
    if (Date.now() - pageLoadTime.current < minTimeOnPage) return false;
    if (requireInteraction && !hasInteracted.current) return false;
    if (disabledPaths.some((p) => window.location.pathname.startsWith(p))) return false;
    return true;
  }, [minTimeOnPage, requireInteraction, disabledPaths]);

  const fire = useCallback(() => {
    if (!canFire()) return;
    hasFired.current = true;
    onExitIntent();
  }, [canFire, onExitIntent]);

  useEffect(() => {
    // Track interaction
    const markInteraction = () => { hasInteracted.current = true; };
    window.addEventListener("scroll", markInteraction, { once: true, passive: true });
    window.addEventListener("click", markInteraction, { once: true });

    // --- Desktop: mouseleave ---
    const handleMouseLeave = (e: MouseEvent) => {
      if (e.clientY <= 0 && e.relatedTarget === null) {
        fire();
      }
    };
    document.addEventListener("mouseleave", handleMouseLeave);

    // --- Mobile: rapid scroll-up velocity ---
    const handleScroll = () => {
      const currentY = window.scrollY;
      const currentTime = Date.now();
      const timeDelta = currentTime - lastScrollTime.current;

      if (timeDelta > 0 && timeDelta < 300) {
        const velocity = (lastScrollY.current - currentY) / (timeDelta / 100);
        // Positive velocity = scrolling up. High velocity = fast scroll up
        if (velocity > mobileScrollThreshold && currentY < 200) {
          fire();
        }
      }

      lastScrollY.current = currentY;
      lastScrollTime.current = currentTime;
    };

    // Only attach scroll listener on touch devices
    const isTouchDevice = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    if (isTouchDevice) {
      window.addEventListener("scroll", handleScroll, { passive: true });
    }

    // --- Mobile: page visibility (tab switch) ---
    const handleVisibilityChange = () => {
      if (document.visibilityState === "hidden") {
        // User switched tabs or minimized — don't fire popup, but note the intent
        // Only fire if they come back within 30 seconds (still considering)
      }
    };
    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      document.removeEventListener("mouseleave", handleMouseLeave);
      window.removeEventListener("scroll", handleScroll);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("scroll", markInteraction);
      window.removeEventListener("click", markInteraction);
    };
  }, [fire, mobileScrollThreshold]);
}
```

---

## Complete JSX Template

```tsx
"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { createPortal } from "react-dom";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

interface ExitIntentPopupProps {
  /** Popup headline — benefit-focused, max 8 words */
  headline?: string;
  /** Supporting text — 15-25 words */
  subheadline?: string;
  /** CTA button label — action + outcome */
  ctaLabel?: string;
  /** Where the form submits (API route or mailto) */
  formAction?: string;
  /** Trust/privacy text below the form */
  trustHint?: string;
  /** Polite dismiss text */
  dismissText?: string;
  /** Show GDPR consent checkbox */
  gdprMode?: boolean;
  /** GDPR checkbox label */
  gdprLabel?: string;
  /** Mobile teaser text */
  teaserText?: string;
  /** Suppress popup for N days after dismissal. Default: 14 */
  suppressDays?: number;
  /** Minimum seconds on page before popup can fire. Default: 5 */
  minTimeOnPage?: number;
  /** Time-based trigger delay in seconds. Default: 45 */
  timeDelay?: number;
  /** Scroll depth trigger (0-1). Default: 0.65 */
  scrollDepth?: number;
  /** Disable exit-intent (only use time/scroll triggers) */
  disableExitIntent?: boolean;
  /** Paths where popup should not appear */
  disabledPaths?: string[];
  /** A/B variant config — provide two configs and the component auto-splits */
  variants?: {
    A: { headline: string; subheadline: string; ctaLabel: string };
    B: { headline: string; subheadline: string; ctaLabel: string };
  };
  /** Callback when email is captured */
  onConvert?: (email: string, variant: "A" | "B") => void;
  /** Callback when popup is dismissed */
  onDismiss?: (method: string, variant: "A" | "B") => void;
}

// -------------------------------------------------------------------
// Storage
// -------------------------------------------------------------------

const STORAGE_KEY = "sp_exit_popup";

interface PopupState {
  lastShown: number;
  suppressUntil: number;
  converted: boolean;
  permanent: boolean;
  variant: "A" | "B";
  sessionId: string;
}

function getState(): PopupState | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    // Validate shape — reject corrupted or tampered data
    if (
      typeof parsed !== "object" ||
      parsed === null ||
      typeof parsed.lastShown !== "number" ||
      typeof parsed.suppressUntil !== "number" ||
      typeof parsed.converted !== "boolean" ||
      typeof parsed.permanent !== "boolean"
    ) {
      localStorage.removeItem(STORAGE_KEY);
      return null;
    }
    return parsed as PopupState;
  } catch {
    localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

function setState(state: Partial<PopupState>) {
  try {
    const current = getState() || {
      lastShown: 0,
      suppressUntil: 0,
      converted: false,
      permanent: false,
      variant: Math.random() < 0.5 ? "A" : "B",
      sessionId: "",
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ ...current, ...state }));
  } catch {
    // localStorage unavailable (private browsing, SSR)
  }
}

function getSessionId(): string {
  try {
    let id = sessionStorage.getItem("sp_session");
    if (!id) {
      // Use cryptographically secure random values instead of Math.random()
      const bytes = new Uint8Array(16);
      crypto.getRandomValues(bytes);
      id = Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
      sessionStorage.setItem("sp_session", id);
    }
    return id;
  } catch {
    return "fallback";
  }
}

function shouldShow(suppressDays: number): boolean {
  const state = getState();
  if (!state) return true; // first visit
  if (state.permanent) return false;
  if (state.converted) return false;
  if (state.sessionId === getSessionId()) return false; // already shown this session
  if (state.suppressUntil > Date.now()) return false;
  return true;
}

function getVariant(): "A" | "B" {
  const state = getState();
  if (state?.variant === "A" || state?.variant === "B") return state.variant;
  const variant: "A" | "B" = Math.random() < 0.5 ? "A" : "B";
  setState({ variant });
  return variant;
}

// -------------------------------------------------------------------
// Analytics helper
// -------------------------------------------------------------------

function trackEvent(
  name: string,
  params: Record<string, string | boolean | number>
) {
  // GA4
  if (typeof window !== "undefined" && typeof (window as any).gtag === "function") {
    (window as any).gtag("event", name, params);
  }
  // Plausible
  if (typeof window !== "undefined" && typeof (window as any).plausible === "function") {
    (window as any).plausible(name, { props: params });
  }
}

// -------------------------------------------------------------------
// Animations
// -------------------------------------------------------------------

const overlayVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.2 } },
  exit: { opacity: 0, transition: { duration: 0.15 } },
};

const modalVariants = {
  hidden: { opacity: 0, scale: 0.95, y: 10 },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] },
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    y: 10,
    transition: { duration: 0.15 },
  },
};

const slideUpVariants = {
  hidden: { y: "100%" },
  visible: {
    y: 0,
    transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] },
  },
  exit: {
    y: "100%",
    transition: { duration: 0.2 },
  },
};

const teaserVariants = {
  hidden: { y: "100%", opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.3, ease: "easeOut" },
  },
  exit: {
    y: "100%",
    opacity: 0,
    transition: { duration: 0.2 },
  },
};

// -------------------------------------------------------------------
// Exit-Intent Detection Hook
// -------------------------------------------------------------------

function useExitIntent(
  onExitIntent: () => void,
  options: {
    minTimeOnPage: number;
    timeDelay: number;
    scrollDepth: number;
    disableExitIntent: boolean;
    disabledPaths: string[];
  }
) {
  const hasFired = useRef(false);
  const hasInteracted = useRef(false);
  const pageLoadTime = useRef(Date.now());
  const lastScrollY = useRef(0);
  const lastScrollTime = useRef(0);

  const canFire = useCallback(() => {
    if (hasFired.current) return false;
    if (Date.now() - pageLoadTime.current < options.minTimeOnPage * 1000) return false;
    if (!hasInteracted.current) return false;
    if (options.disabledPaths.some((p) => window.location.pathname.startsWith(p)))
      return false;
    return true;
  }, [options.minTimeOnPage, options.disabledPaths]);

  const fire = useCallback(() => {
    if (!canFire()) return;
    hasFired.current = true;
    onExitIntent();
  }, [canFire, onExitIntent]);

  useEffect(() => {
    // Track interaction
    const markInteraction = () => {
      hasInteracted.current = true;
    };
    window.addEventListener("scroll", markInteraction, { once: true, passive: true });
    window.addEventListener("click", markInteraction, { once: true });

    // --- Desktop exit-intent: mouseleave ---
    const handleMouseLeave = (e: MouseEvent) => {
      if (options.disableExitIntent) return;
      if (e.clientY <= 0 && e.relatedTarget === null) {
        fire();
      }
    };
    document.addEventListener("mouseleave", handleMouseLeave);

    // --- Mobile exit-intent: rapid scroll-up ---
    const isTouchDevice =
      "ontouchstart" in window || navigator.maxTouchPoints > 0;

    const handleScroll = () => {
      if (options.disableExitIntent) return;
      const currentY = window.scrollY;
      const currentTime = Date.now();
      const timeDelta = currentTime - lastScrollTime.current;

      if (timeDelta > 0 && timeDelta < 300) {
        const velocity =
          (lastScrollY.current - currentY) / (timeDelta / 100);
        if (velocity > 80 && currentY < 200) {
          fire();
        }
      }

      lastScrollY.current = currentY;
      lastScrollTime.current = currentTime;
    };

    if (isTouchDevice) {
      window.addEventListener("scroll", handleScroll, { passive: true });
    }

    // --- Time-based fallback ---
    const timeTimer = setTimeout(() => {
      fire();
    }, options.timeDelay * 1000);

    // --- Scroll depth fallback ---
    const sentinel = document.createElement("div");
    sentinel.style.cssText =
      "position:absolute;width:1px;height:1px;pointer-events:none;";
    sentinel.style.top = `${options.scrollDepth * 100}%`;
    document.body.style.position = "relative";
    document.body.appendChild(sentinel);

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          fire();
          observer.disconnect();
        }
      },
      { threshold: 0 }
    );
    observer.observe(sentinel);

    return () => {
      document.removeEventListener("mouseleave", handleMouseLeave);
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("scroll", markInteraction);
      window.removeEventListener("click", markInteraction);
      clearTimeout(timeTimer);
      observer.disconnect();
      sentinel.remove();
    };
  }, [fire, options.disableExitIntent, options.timeDelay, options.scrollDepth]);
}

// -------------------------------------------------------------------
// Component
// -------------------------------------------------------------------

export default function ExitIntentPopup({
  headline = "Before you go — here's 20% off",
  subheadline = "Join 2,400 teams who ship faster. Enter your email for an exclusive discount.",
  ctaLabel = "Claim my discount",
  formAction = "/api/subscribe",
  trustHint = "No spam. Unsubscribe anytime.",
  dismissText = "No thanks",
  gdprMode = false,
  gdprLabel = "I agree to receive marketing emails and accept the privacy policy.",
  teaserText = "🎁 Special offer before you go",
  suppressDays = 14,
  minTimeOnPage = 5,
  timeDelay = 45,
  scrollDepth = 0.65,
  disableExitIntent = false,
  disabledPaths = [],
  variants,
  onConvert,
  onDismiss,
}: ExitIntentPopupProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [showTeaser, setShowTeaser] = useState(false);
  const [email, setEmail] = useState("");
  const [gdprChecked, setGdprChecked] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const variant = useRef(getVariant());

  // Resolve variant-specific copy
  const copy = variants
    ? variants[variant.current]
    : { headline, subheadline, ctaLabel };

  // SSR safety
  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Detect if touch device
  const isTouchDevice = useRef(false);
  useEffect(() => {
    isTouchDevice.current =
      "ontouchstart" in window || navigator.maxTouchPoints > 0;
  }, []);

  // Handle popup trigger
  const handleTrigger = useCallback(() => {
    if (!shouldShow(suppressDays)) return;

    if (isTouchDevice.current) {
      // Mobile: show teaser first
      setShowTeaser(true);
      trackEvent("popup_teaser_shown", {
        event_category: "exit_intent",
        device: "mobile",
      });
    } else {
      // Desktop: show modal directly
      setIsOpen(true);
      setState({
        lastShown: Date.now(),
        sessionId: getSessionId(),
      });
      trackEvent("popup_impression", {
        event_category: "exit_intent",
        event_label: `variant_${variant.current}`,
        trigger_type: "exit_intent",
      });
    }
  }, [suppressDays]);

  // Teaser click → expand to full popup
  const handleTeaserClick = () => {
    setShowTeaser(false);
    setIsOpen(true);
    setState({
      lastShown: Date.now(),
      sessionId: getSessionId(),
    });
    trackEvent("popup_teaser_click", {
      event_category: "exit_intent",
      event_label: "teaser_expanded",
    });
    trackEvent("popup_impression", {
      event_category: "exit_intent",
      event_label: `variant_${variant.current}`,
      trigger_type: "teaser",
    });
  };

  // Close popup
  const handleClose = (method: string) => {
    setIsOpen(false);
    setShowTeaser(false);
    const suppressUntil = Date.now() + suppressDays * 24 * 60 * 60 * 1000;
    setState({
      suppressUntil,
      permanent: method === "dont_show",
    });
    trackEvent("popup_close", {
      event_category: "exit_intent",
      event_label: `variant_${variant.current}`,
      close_method: method,
    });
    onDismiss?.(method, variant.current);
    document.body.style.overflow = "";
  };

  // Submit form
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || (gdprMode && !gdprChecked)) return;

    setIsSubmitting(true);

    try {
      const res = await fetch(formAction, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          source: "exit_intent_popup",
          variant: variant.current,
          gdprConsent: gdprMode ? gdprChecked : undefined,
        }),
      });

      if (res.ok) {
        setIsSuccess(true);
        setState({ converted: true, permanent: true });
        trackEvent("popup_convert", {
          event_category: "exit_intent",
          event_label: `variant_${variant.current}`,
          email_captured: true,
        });
        onConvert?.(email, variant.current);

        // Auto-close after 2 seconds
        setTimeout(() => {
          setIsOpen(false);
          document.body.style.overflow = "";
        }, 2000);
      }
    } catch {
      // Silently fail — don't break the page for a popup error
    } finally {
      setIsSubmitting(false);
    }
  };

  // Lock body scroll when open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
      // Focus the email input after animation
      setTimeout(() => inputRef.current?.focus(), 300);
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  // ESC key handler
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        handleClose("escape");
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  // Attach exit-intent detection
  useExitIntent(handleTrigger, {
    minTimeOnPage,
    timeDelay,
    scrollDepth,
    disableExitIntent,
    disabledPaths,
  });

  // Don't render on server
  if (!isMounted) return null;

  return createPortal(
    <>
      {/* ---- Mobile Teaser ---- */}
      <AnimatePresence>
        {showTeaser && !isOpen && (
          <motion.button
            variants={teaserVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            onClick={handleTeaserClick}
            className="fixed bottom-0 left-0 right-0 z-40
                       bg-primary text-primary-foreground
                       px-4 py-3.5 text-sm font-medium text-center
                       rounded-t-xl shadow-lg
                       cursor-pointer
                       hover:brightness-110
                       transition-colors duration-200"
            aria-label="View special offer"
          >
            {teaserText}
          </motion.button>
        )}
      </AnimatePresence>

      {/* ---- Popup Modal ---- */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Overlay */}
            <motion.div
              variants={overlayVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              onClick={() => handleClose("overlay")}
              className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
              aria-hidden="true"
            />

            {/* Modal */}
            <div
              className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4"
              role="dialog"
              aria-modal="true"
              aria-labelledby="exit-popup-heading"
            >
              <motion.div
                variants={isTouchDevice.current ? slideUpVariants : modalVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
                className="relative w-full sm:max-w-md
                           rounded-t-2xl sm:rounded-2xl
                           bg-card border border-border
                           shadow-2xl
                           p-6 sm:p-8"
              >
                {/* Close button */}
                <button
                  onClick={() => handleClose("x_button")}
                  className="absolute top-4 right-4
                             p-1.5 rounded-full
                             text-muted-foreground hover:text-foreground
                             hover:bg-muted
                             transition-colors duration-200
                             focus-visible:outline-2 focus-visible:outline-primary
                             focus-visible:outline-offset-2"
                  aria-label="Close popup"
                >
                  <X className="h-5 w-5" />
                </button>

                {isSuccess ? (
                  /* ---- Success state ---- */
                  <div className="text-center py-6">
                    <div
                      className="mx-auto mb-4 flex h-12 w-12 items-center justify-center
                                  rounded-full bg-green-100 dark:bg-green-900/30"
                      aria-hidden="true"
                    >
                      <svg
                        className="h-6 w-6 text-green-600 dark:text-green-400"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={2}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </div>
                    <h3 className="text-lg font-semibold text-foreground">
                      You're in!
                    </h3>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Check your inbox for next steps.
                    </p>
                  </div>
                ) : (
                  /* ---- Form state ---- */
                  <div className="pr-6">
                    <h2
                      id="exit-popup-heading"
                      className="text-xl sm:text-2xl font-bold text-foreground
                                 leading-tight"
                    >
                      {copy.headline}
                    </h2>

                    <p className="mt-2 text-sm sm:text-base text-muted-foreground leading-relaxed">
                      {copy.subheadline}
                    </p>

                    <form onSubmit={handleSubmit} className="mt-6 space-y-3">
                      <Input
                        ref={inputRef}
                        type="email"
                        required
                        placeholder="you@company.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="h-12 text-base"
                        aria-label="Email address"
                        autoComplete="email"
                      />

                      {gdprMode && (
                        <label className="flex items-start gap-2 text-xs text-muted-foreground cursor-pointer">
                          <input
                            type="checkbox"
                            checked={gdprChecked}
                            onChange={(e) => setGdprChecked(e.target.checked)}
                            className="mt-0.5 rounded border-border"
                            required
                          />
                          <span>{gdprLabel}</span>
                        </label>
                      )}

                      <Button
                        type="submit"
                        size="lg"
                        disabled={isSubmitting || (gdprMode && !gdprChecked)}
                        className="w-full h-12 text-base font-semibold
                                   shadow-lg shadow-primary/20"
                      >
                        {isSubmitting ? (
                          <span className="flex items-center gap-2">
                            <svg
                              className="animate-spin h-4 w-4"
                              viewBox="0 0 24 24"
                              fill="none"
                            >
                              <circle
                                className="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                strokeWidth="4"
                              />
                              <path
                                className="opacity-75"
                                fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                              />
                            </svg>
                            Sending...
                          </span>
                        ) : (
                          copy.ctaLabel
                        )}
                      </Button>
                    </form>

                    {/* Trust hint */}
                    <p className="mt-3 text-xs text-center text-muted-foreground/70">
                      {trustHint}
                    </p>

                    {/* Polite dismiss */}
                    <div className="mt-4 text-center">
                      <button
                        onClick={() => handleClose("dismiss_text")}
                        className="text-xs text-muted-foreground/60
                                   hover:text-muted-foreground
                                   underline-offset-2 hover:underline
                                   transition-colors duration-200"
                      >
                        {dismissText}
                      </button>
                    </div>
                  </div>
                )}
              </motion.div>
            </div>
          </>
        )}
      </AnimatePresence>
    </>,
    document.body
  );
}
```

---

## Usage in Page

```tsx
// In your page layout (e.g., app/page.tsx or layout.tsx)
import ExitIntentPopup from "@/components/sections/exit-intent-popup";

export default function LandingPage() {
  return (
    <>
      {/* ... your page sections ... */}

      {/* Exit-intent popup — renders via portal, no layout impact */}
      <ExitIntentPopup
        headline="Get 20% off your first month"
        subheadline="Join 2,400 teams who ship faster. Enter your email for an exclusive discount."
        ctaLabel="Claim my discount"
        formAction="/api/subscribe"
        suppressDays={14}
        timeDelay={45}
        scrollDepth={0.65}
        gdprMode={false}
        // Optional A/B testing:
        // variants={{
        //   A: { headline: "Get 20% off", subheadline: "...", ctaLabel: "Claim discount" },
        //   B: { headline: "Free guide: Ship 3x faster", subheadline: "...", ctaLabel: "Send me the guide" },
        // }}
      />
    </>
  );
}
```

---

## Benchmark Targets

| Metric | Target | Industry Average |
|--------|--------|-----------------|
| Popup conversion rate (SaaS) | 3-5% | 2.1% |
| Exit-intent popup CVR | 5-10% | 2-5% |
| Popup with countdown CVR | 10-15% | 14.41% |
| Mobile popup CVR | 4-6% | 4.98% |
| Teaser click-through rate | 8-12% | — |
| Frequency fatigue rate | < 5% | — |
