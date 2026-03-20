# Sticky CTA Bar Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

> **Replaces:** Hello Bar ($39-129/mo), OptinMonster floating bars ($7-82/mo), Sleeknote Sleekbars ($49-299/mo). A sticky notification bar that appears when the hero CTA scrolls out of view, keeping the primary conversion action always accessible. Zero external dependencies.

---

## Conversion Job

**PERSISTENT CONVERSION ACCESS** — The visitor has scrolled past the hero and is now deep in your content. The primary CTA button is no longer visible. The sticky bar ensures the conversion action remains one tap away at all times, without interrupting reading flow.

**Impact data:**
- Sites with sticky CTA bars see 8-15% conversion improvement (multiple studies)
- One brand reported +37% increase in checkout starts within 2 weeks of adding a bottom sticky bar
- Sticky bars generate massive impression volume with ~0.5-3.7% CVR per impression

**When to include:** Every page with a primary CTA benefits from a sticky bar. The skill includes this automatically whenever the page has a hero CTA above the fold.

---

## Trigger Behavior

The sticky bar is NOT always visible. It uses scroll-aware intelligence:

### Show Rules

| Trigger | Behavior |
|---------|----------|
| **Hero CTA scroll-out** (default) | Bar appears when the hero's primary CTA button scrolls out of the viewport |
| **Scroll percentage fallback** | If hero CTA element not found, trigger at 20% scroll depth |
| **Scroll direction** | Bar hides on scroll-down (user is reading), reveals on scroll-up (user is navigating) |

### Hide Rules

| Condition | Behavior |
|-----------|----------|
| User scrolls back to hero | Bar hides (hero CTA is visible again) |
| User dismisses bar | Bar stays hidden for this session |
| User clicks CTA | Bar hides (mission accomplished) |
| Footer is in view | Bar hides (final CTA section is visible) |

```typescript
// Scroll-aware visibility logic
const [isVisible, setIsVisible] = useState(false);
const [isDismissed, setIsDismissed] = useState(false);
const lastScrollY = useRef(0);
const scrollDirection = useRef<"up" | "down">("down");

useEffect(() => {
  const heroCTA = document.querySelector("[data-hero-cta]");
  const footer = document.querySelector("[data-cta-footer]");

  const handleScroll = () => {
    if (isDismissed) return;

    const currentY = window.scrollY;
    scrollDirection.current = currentY > lastScrollY.current ? "down" : "up";
    lastScrollY.current = currentY;

    // Check if hero CTA is out of view
    const heroRect = heroCTA?.getBoundingClientRect();
    const heroOutOfView = heroRect ? heroRect.bottom < 0 : currentY > window.innerHeight * 0.2;

    // Check if footer CTA is in view
    const footerRect = footer?.getBoundingClientRect();
    const footerInView = footerRect ? footerRect.top < window.innerHeight : false;

    // Show bar when: hero CTA out of view AND footer not in view
    // On desktop: also consider scroll direction (hide on scroll-down for cleaner reading)
    const isMobile = window.innerWidth < 640;
    const shouldShow = heroOutOfView && !footerInView;

    if (isMobile) {
      // Mobile: always show when conditions met (no direction-based hiding)
      setIsVisible(shouldShow);
    } else {
      // Desktop: hide on scroll-down, show on scroll-up
      setIsVisible(shouldShow && scrollDirection.current === "up");
    }
  };

  window.addEventListener("scroll", handleScroll, { passive: true });
  return () => window.removeEventListener("scroll", handleScroll);
}, [isDismissed]);
```

---

## Desktop Layout

### Bottom bar (default)
```
┌────────────────────────────────────────────────────────────┐
│                      [Page content]                         │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │  [Product tagline]              [CTA Button]    [✕]     │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

- Position: `fixed bottom-0 left-0 right-0 z-40`
- Inner: `max-w-6xl mx-auto px-4 sm:px-6 py-3`
- Layout: `flex items-center justify-between gap-4`
- Background: `bg-card/95 backdrop-blur-md border-t border-border shadow-lg`
- CTA button: compact, matches hero CTA styling
- Close: small X button on the right
- Entrance: slide up from bottom (200ms)

### Top bar (alternative)
```
┌─────────────────────────────────────────────────────────┐
│ [Product tagline]              [CTA Button]       [✕]   │
├─────────────────────────────────────────────────────────┤
│                      [Page content]                      │
└─────────────────────────────────────────────────────────┘
```

- Position: `fixed top-0 left-0 right-0 z-40`
- Uses `border-b` instead of `border-t`
- Entrance: slide down from top (200ms)
- Note: top bar can conflict with sticky navbar — use bottom by default

---

## Mobile Layout

### Bottom bar (strongly recommended for mobile)
```
┌──────────────────────┐
│                      │
│    [Page content]    │
│                      │
│ ┌──────────────────┐ │
│ │  [CTA Button]  ✕ │ │
│ └──────────────────┘ │
└──────────────────────┘
```

- Full-width button: `w-full` CTA button for easy thumb reach
- Tagline text hidden on mobile (button only) to save height
- Minimal height: `py-3 px-4`
- Close button: inline with CTA, small
- Safe area padding: `pb-[env(safe-area-inset-bottom)]` for iPhones with home indicator
- Background: `bg-card/95 backdrop-blur-md` (semi-transparent for content peek-through)

---

## Copy Structure

| Element | Rule | Example |
|---------|------|---------|
| **Tagline** (desktop only) | Echo the core benefit in ≤ 8 words | "Ship 3x faster with zero config" |
| **CTA button** | Same label as hero CTA for consistency | "Start Free Trial" / "Get Started Free" |
| **Secondary text** (optional) | Trust micro-copy next to button | "No credit card required" |

### CTA Button should match hero CTA exactly
The sticky bar CTA must use the **same label and destination** as the hero's primary CTA. This reduces cognitive load — the visitor already understood the offer, they just need the button back.

---

## Variants

### 1. Simple Bar (default)
Tagline + CTA button. Clean, minimal, professional.

### 2. Email Capture Bar
Inline email input + submit button. For lead-gen pages.
```
[📧 email@example.com  ] [Subscribe →]  [✕]
```

### 3. Announcement Bar
Non-conversion messaging: product launch, event, new feature.
```
[🚀 We just launched v2.0 — see what's new]  [Learn more →]  [✕]
```

### 4. Countdown Bar
Urgency-driven with countdown timer. Use sparingly and only for real deadlines.
```
[⏰ Early bird pricing ends in 2d 14h 23m]  [Lock in price →]  [✕]
```

---

## Section-Specific Notes

- The bar renders via `createPortal` to `document.body` (no parent layout interference)
- Uses `data-hero-cta` attribute on the hero's CTA button to detect scroll-out
- Uses `data-cta-footer` attribute on the footer CTA section to detect scroll-in
- Dismissal is session-only (`sessionStorage`) — bar comes back on next visit
- `prefers-reduced-motion`: bar appears/disappears instantly (no slide animation)
- Total JS weight: < 2KB gzipped
- The bar should not overlap with:
  - Cookie consent banners (check for `[data-cookie-banner]` and offset)
  - Chat widgets (check for common chat widget selectors)
  - Mobile browser bottom toolbars (use `env(safe-area-inset-bottom)`)
- Tab order: bar's CTA should be reachable but not interrupt page flow
  - `tabindex="0"` on the CTA button
  - Skip-link pattern if needed

---

## Complete JSX Template

```tsx
"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { createPortal } from "react-dom";
import { motion, AnimatePresence } from "framer-motion";
import { X, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

type BarVariant = "simple" | "email-capture" | "announcement" | "countdown";
type BarPosition = "top" | "bottom";

interface StickyCTABarProps {
  /** Bar variant. Default: "simple" */
  variant?: BarVariant;
  /** Position: top or bottom. Default: "bottom" */
  position?: BarPosition;
  /** Tagline text (hidden on mobile for simple/email variants) */
  tagline?: string;
  /** CTA button label — should match hero CTA */
  ctaLabel?: string;
  /** CTA destination */
  ctaHref?: string;
  /** Trust micro-copy next to button (desktop only) */
  trustText?: string;
  /** For email-capture variant: placeholder text */
  emailPlaceholder?: string;
  /** For email-capture variant: form action */
  formAction?: string;
  /** For announcement variant: link text */
  announcementLink?: string;
  /** For countdown variant: deadline date (ISO string) */
  countdownDeadline?: string;
  /** CSS selector for the hero CTA element. Default: "[data-hero-cta]" */
  heroCTASelector?: string;
  /** CSS selector for the footer CTA section. Default: "[data-cta-footer]" */
  footerSelector?: string;
  /** Callback when CTA is clicked */
  onCTAClick?: () => void;
  /** Callback when email is captured (email-capture variant) */
  onEmailCapture?: (email: string) => void;
}

// -------------------------------------------------------------------
// Countdown hook
// -------------------------------------------------------------------

function useCountdown(deadline: string) {
  const [timeLeft, setTimeLeft] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0 });

  useEffect(() => {
    const target = new Date(deadline).getTime();

    const update = () => {
      const now = Date.now();
      const diff = Math.max(0, target - now);
      setTimeLeft({
        days: Math.floor(diff / (1000 * 60 * 60 * 24)),
        hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((diff / (1000 * 60)) % 60),
        seconds: Math.floor((diff / 1000) % 60),
      });
    };

    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, [deadline]);

  return timeLeft;
}

// -------------------------------------------------------------------
// Analytics helper
// -------------------------------------------------------------------

function trackEvent(
  name: string,
  params: Record<string, string | boolean | number>
) {
  if (typeof window !== "undefined" && typeof (window as any).gtag === "function") {
    (window as any).gtag("event", name, params);
  }
  if (typeof window !== "undefined" && typeof (window as any).plausible === "function") {
    (window as any).plausible(name, { props: params });
  }
}

// -------------------------------------------------------------------
// Animations
// -------------------------------------------------------------------

const slideFromBottom = {
  hidden: { y: "100%", opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] },
  },
  exit: {
    y: "100%",
    opacity: 0,
    transition: { duration: 0.2 },
  },
};

const slideFromTop = {
  hidden: { y: "-100%", opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] },
  },
  exit: {
    y: "-100%",
    opacity: 0,
    transition: { duration: 0.2 },
  },
};

// -------------------------------------------------------------------
// Component
// -------------------------------------------------------------------

export default function StickyCTABar({
  variant = "simple",
  position = "bottom",
  tagline = "Ship 3x faster with zero config",
  ctaLabel = "Start Free Trial",
  ctaHref = "#cta",
  trustText = "No credit card required",
  emailPlaceholder = "you@company.com",
  formAction = "/api/subscribe",
  announcementLink = "Learn more",
  countdownDeadline = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
  heroCTASelector = "[data-hero-cta]",
  footerSelector = "[data-cta-footer]",
  onCTAClick,
  onEmailCapture,
}: StickyCTABarProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isDismissed, setIsDismissed] = useState(false);
  const [email, setEmail] = useState("");
  const [emailSubmitted, setEmailSubmitted] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  const lastScrollY = useRef(0);
  const scrollDirection = useRef<"up" | "down">("down");
  const hasTrackedImpression = useRef(false);

  const countdown = useCountdown(countdownDeadline);

  // SSR safety
  useEffect(() => {
    setIsMounted(true);

    // Check if previously dismissed this session
    try {
      if (sessionStorage.getItem("sp_sticky_dismissed") === "true") {
        setIsDismissed(true);
      }
    } catch {
      // sessionStorage unavailable
    }
  }, []);

  // Scroll-aware visibility
  useEffect(() => {
    if (!isMounted || isDismissed) return;

    const handleScroll = () => {
      const currentY = window.scrollY;
      scrollDirection.current = currentY > lastScrollY.current ? "down" : "up";
      lastScrollY.current = currentY;

      // Check if hero CTA is out of view
      const heroCTA = document.querySelector(heroCTASelector);
      const heroRect = heroCTA?.getBoundingClientRect();
      const heroOutOfView = heroRect
        ? heroRect.bottom < 0
        : currentY > window.innerHeight * 0.2;

      // Check if footer CTA is in view
      const footer = document.querySelector(footerSelector);
      const footerRect = footer?.getBoundingClientRect();
      const footerInView = footerRect
        ? footerRect.top < window.innerHeight
        : false;

      const shouldShow = heroOutOfView && !footerInView;

      // Mobile: always show when conditions met
      // Desktop: also factor in scroll direction (hide on scroll-down)
      const isMobile = window.innerWidth < 640;
      if (isMobile) {
        setIsVisible(shouldShow);
      } else {
        setIsVisible(shouldShow && scrollDirection.current === "up");
      }
    };

    window.addEventListener("scroll", handleScroll, { passive: true });

    // Initial check (in case page loads scrolled)
    handleScroll();

    return () => window.removeEventListener("scroll", handleScroll);
  }, [isMounted, isDismissed, heroCTASelector, footerSelector]);

  // Track impression once
  useEffect(() => {
    if (isVisible && !hasTrackedImpression.current) {
      hasTrackedImpression.current = true;
      trackEvent("sticky_bar_impression", {
        event_category: "sticky_cta",
        variant,
        position,
      });
    }
  }, [isVisible, variant, position]);

  // Dismiss handler
  const handleDismiss = useCallback(() => {
    setIsDismissed(true);
    setIsVisible(false);
    try {
      sessionStorage.setItem("sp_sticky_dismissed", "true");
    } catch {
      // sessionStorage unavailable
    }
    trackEvent("sticky_bar_dismiss", {
      event_category: "sticky_cta",
      variant,
    });
  }, [variant]);

  // CTA click handler
  const handleCTAClick = () => {
    trackEvent("sticky_bar_cta_click", {
      event_category: "sticky_cta",
      variant,
      cta_label: ctaLabel,
    });
    onCTAClick?.();
  };

  // Email submit handler
  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    try {
      await fetch(formAction, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, source: "sticky_bar" }),
      });
      setEmailSubmitted(true);
      trackEvent("sticky_bar_email_capture", {
        event_category: "sticky_cta",
        email_captured: true,
      });
      onEmailCapture?.(email);

      // Auto-dismiss after 2 seconds
      setTimeout(() => handleDismiss(), 2000);
    } catch {
      // Silently fail
    }
  };

  if (!isMounted) return null;

  const variants = position === "bottom" ? slideFromBottom : slideFromTop;
  const positionClasses =
    position === "bottom"
      ? "bottom-0 border-t pb-[env(safe-area-inset-bottom)]"
      : "top-0 border-b";

  return createPortal(
    <AnimatePresence>
      {isVisible && (
        <motion.div
          variants={variants}
          initial="hidden"
          animate="visible"
          exit="exit"
          className={`fixed left-0 right-0 z-40
                      bg-card/95 backdrop-blur-md border-border shadow-lg
                      ${positionClasses}`}
          role="complementary"
          aria-label="Call to action"
        >
          <div className="mx-auto max-w-6xl px-4 sm:px-6 py-3">
            {/* ---- Simple Variant ---- */}
            {variant === "simple" && (
              <div className="flex items-center justify-between gap-3 sm:gap-4">
                {/* Tagline (hidden on mobile) */}
                <p className="hidden sm:block text-sm font-medium text-foreground truncate">
                  {tagline}
                </p>

                <div className="flex items-center gap-3 w-full sm:w-auto">
                  {/* Trust text (hidden on mobile) */}
                  {trustText && (
                    <span className="hidden lg:block text-xs text-muted-foreground whitespace-nowrap">
                      {trustText}
                    </span>
                  )}

                  {/* CTA Button */}
                  <Button
                    asChild
                    size="sm"
                    onClick={handleCTAClick}
                    className="w-full sm:w-auto whitespace-nowrap shadow-sm"
                  >
                    <a href={ctaHref}>
                      {ctaLabel}
                      <ArrowRight className="ml-1.5 h-3.5 w-3.5" aria-hidden="true" />
                    </a>
                  </Button>

                  {/* Close button */}
                  <button
                    onClick={handleDismiss}
                    className="shrink-0 p-1.5 rounded-md
                               text-muted-foreground hover:text-foreground
                               hover:bg-muted
                               transition-colors duration-200"
                    aria-label="Dismiss notification bar"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              </div>
            )}

            {/* ---- Email Capture Variant ---- */}
            {variant === "email-capture" && (
              <div className="flex items-center justify-between gap-3 sm:gap-4">
                {/* Tagline (hidden on mobile) */}
                <p className="hidden sm:block text-sm font-medium text-foreground truncate">
                  {tagline}
                </p>

                {emailSubmitted ? (
                  <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400 font-medium">
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                    You're in! Check your inbox.
                  </div>
                ) : (
                  <form
                    onSubmit={handleEmailSubmit}
                    className="flex items-center gap-2 w-full sm:w-auto"
                  >
                    <Input
                      type="email"
                      required
                      placeholder={emailPlaceholder}
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="h-9 text-sm w-full sm:w-56"
                      aria-label="Email address"
                      autoComplete="email"
                    />
                    <Button
                      type="submit"
                      size="sm"
                      className="shrink-0 whitespace-nowrap"
                    >
                      {ctaLabel}
                    </Button>

                    {/* Close button */}
                    <button
                      onClick={handleDismiss}
                      className="shrink-0 p-1.5 rounded-md
                                 text-muted-foreground hover:text-foreground
                                 hover:bg-muted
                                 transition-colors duration-200"
                      aria-label="Dismiss notification bar"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </form>
                )}
              </div>
            )}

            {/* ---- Announcement Variant ---- */}
            {variant === "announcement" && (
              <div className="flex items-center justify-center gap-3 text-center">
                <p className="text-sm font-medium text-foreground">
                  {tagline}
                </p>
                <a
                  href={ctaHref}
                  onClick={handleCTAClick}
                  className="text-sm font-semibold text-primary
                             hover:underline underline-offset-2
                             whitespace-nowrap flex items-center gap-1"
                >
                  {announcementLink}
                  <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
                </a>
                <button
                  onClick={handleDismiss}
                  className="shrink-0 p-1.5 rounded-md
                             text-muted-foreground hover:text-foreground
                             hover:bg-muted
                             transition-colors duration-200"
                  aria-label="Dismiss notification bar"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            )}

            {/* ---- Countdown Variant ---- */}
            {variant === "countdown" && (
              <div className="flex items-center justify-between gap-3 sm:gap-4">
                {/* Countdown display */}
                <div className="flex items-center gap-2 text-sm text-foreground">
                  <span className="hidden sm:inline font-medium">{tagline}</span>
                  <div className="flex items-center gap-1 font-mono text-xs sm:text-sm font-semibold">
                    {countdown.days > 0 && (
                      <span className="bg-muted px-1.5 py-0.5 rounded">{countdown.days}d</span>
                    )}
                    <span className="bg-muted px-1.5 py-0.5 rounded">{String(countdown.hours).padStart(2, "0")}h</span>
                    <span className="bg-muted px-1.5 py-0.5 rounded">{String(countdown.minutes).padStart(2, "0")}m</span>
                    <span className="bg-muted px-1.5 py-0.5 rounded">{String(countdown.seconds).padStart(2, "0")}s</span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Button
                    asChild
                    size="sm"
                    onClick={handleCTAClick}
                    className="whitespace-nowrap shadow-sm"
                  >
                    <a href={ctaHref}>
                      {ctaLabel}
                      <ArrowRight className="ml-1.5 h-3.5 w-3.5" aria-hidden="true" />
                    </a>
                  </Button>
                  <button
                    onClick={handleDismiss}
                    className="shrink-0 p-1.5 rounded-md
                               text-muted-foreground hover:text-foreground
                               hover:bg-muted
                               transition-colors duration-200"
                    aria-label="Dismiss notification bar"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body
  );
}
```

---

## Usage in Page

```tsx
// In your page layout
import StickyCTABar from "@/components/sections/sticky-cta-bar";

export default function LandingPage() {
  return (
    <>
      {/* Hero section — add data-hero-cta to the primary CTA button */}
      <section>
        <Button data-hero-cta asChild>
          <a href="#cta">Start Free Trial</a>
        </Button>
      </section>

      {/* ... other sections ... */}

      {/* Footer CTA — add data-cta-footer to the section */}
      <section data-cta-footer>
        {/* ... final CTA content ... */}
      </section>

      {/* Sticky CTA bar — renders via portal */}
      <StickyCTABar
        variant="simple"
        position="bottom"
        tagline="Ship 3x faster with zero config"
        ctaLabel="Start Free Trial"
        ctaHref="#cta"
        trustText="No credit card required"
      />

      {/* OR email capture variant */}
      {/* <StickyCTABar
        variant="email-capture"
        tagline="Get early access"
        ctaLabel="Subscribe"
        formAction="/api/subscribe"
      /> */}

      {/* OR countdown variant */}
      {/* <StickyCTABar
        variant="countdown"
        tagline="Early bird pricing ends in"
        ctaLabel="Lock in price"
        ctaHref="#pricing"
        countdownDeadline="2026-04-01T00:00:00Z"
      /> */}
    </>
  );
}
```

---

## Integration with Hero Templates

For the sticky bar to work, the hero section's CTA button needs a `data-hero-cta` attribute:

```tsx
// In hero-centered.md or hero-split.md template
<Button data-hero-cta asChild size="lg">
  <a href={ctaPrimaryHref}>{ctaPrimaryText}</a>
</Button>
```

And the footer CTA section needs a `data-cta-footer` attribute:

```tsx
// In cta-footer.md template
<section data-cta-footer ref={ctaRef} id="cta" ...>
```

The skill should automatically add these data attributes when generating pages that include the sticky bar.

---

## Benchmark Targets

| Metric | Target | Industry Average |
|--------|--------|-----------------|
| Sticky bar impression volume | High (100% of scrolling visitors) | — |
| Sticky bar CVR | 2-4% | 0.5-3.7% |
| Conversion improvement | 8-15% | 8-15% (well-documented) |
| Checkout start increase | 15-30% | 37% (best case study) |
| Dismiss rate | 10-20% (healthy) | — |
| Bar height (mobile) | ≤ 56px | — |
| Animation duration | 200-250ms | — |
| JS weight | < 2KB gzipped | — |
