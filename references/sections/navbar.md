## Navbar

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

### Conversion Job
NAVIGATION + CONVERSION -- The navbar serves dual purpose: wayfinding across the page
and persistent CTA visibility. The primary CTA button must never scroll out of view
on any device.

### Desktop Layout
```
[AnnouncementBar] ................................................ full width, optional
[Logo]   [NavLink NavLink NavLink NavLink NavLink]   [CTAButton]
 ^left          ^center (gap-8)                        ^right
```
- Outer container: `fixed top-0 inset-x-0 z-50`
- Inner: `max-w-7xl mx-auto flex items-center justify-between px-6 h-16`
- Nav links group: `hidden md:flex items-center gap-8`
- CTA: `hidden md:inline-flex`

### Mobile Layout (mobile-first)
- Logo left, hamburger icon right
- Tap hamburger opens a slide-in drawer from the right (shadcn Sheet)
- Drawer contains nav links stacked vertically + CTA button at bottom
- Sticky bottom CTA bar appears after user scrolls past the hero section
  - `fixed bottom-0 inset-x-0 z-40 md:hidden`
  - Renders the same CTA button full-width with safe-area padding

### Copy Structure
| Element           | Limit           | Framework        |
|-------------------|-----------------|------------------|
| Logo text/image   | --              | Brand identity   |
| Nav links         | Max 5 items     | Short labels (1-2 words) |
| CTA button        | 2-4 words       | Action-oriented  |
| Announcement text | Max 80 chars    | Urgency / news   |

### Section-Specific Notes
- Navbar is visible immediately (no entrance animation).
- Scroll state transition: `bg-transparent` -> `bg-background/80 backdrop-blur-lg` via `useEffect`.
- Sticky mobile CTA slides up with `AnimatePresence` after scrolling past hero.
- No dynamic imports needed -- navbar is critical and above the fold.
- Skip-to-content link: `sr-only focus:not-sr-only` as first focusable element.

### Complete JSX Template
```tsx
"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

// ------------------------------------------------------------------ Types
interface NavLink {
  label: string;
  href: string;
}

interface NavbarProps {
  logo?: React.ReactNode;
  links?: NavLink[];
  ctaText?: string;
  ctaHref?: string;
  announcement?: string;
  announcementHref?: string;
}

// ------------------------------------------------------------------ Data defaults
const defaultLinks: NavLink[] = [
  { label: "Features", href: "#features" },
  { label: "Pricing", href: "#pricing" },
  { label: "Testimonials", href: "#testimonials" },
  { label: "FAQ", href: "#faq" },
];

// ------------------------------------------------------------------ Component
export default function Navbar({
  logo = <span className="text-xl font-bold tracking-tight">Brand</span>,
  links = defaultLinks,
  ctaText = "Get Started",
  ctaHref = "#cta",
  announcement,
  announcementHref,
}: NavbarProps) {
  const [scrolled, setScrolled] = useState(false);
  const [pastHero, setPastHero] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);

  // ---- Scroll listener
  const handleScroll = useCallback(() => {
    const y = window.scrollY;
    setScrolled(y > 20);
    setPastHero(y > window.innerHeight * 0.8);
  }, []);

  useEffect(() => {
    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll(); // initialize
    return () => window.removeEventListener("scroll", handleScroll);
  }, [handleScroll]);

  // ---- Smooth scroll helper
  const scrollTo = (href: string) => {
    setDrawerOpen(false);
    const el = document.querySelector(href);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <>
      {/* ---- Skip to content ---- */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[60] focus:rounded-lg focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground focus:outline-none"
      >
        Skip to content
      </a>

      {/* ---- Announcement bar ---- */}
      {announcement && (
        <div className="bg-primary text-primary-foreground text-sm text-center py-2 px-4">
          {announcementHref ? (
            <a
              href={announcementHref}
              className="inline-flex items-center gap-1 hover:underline"
            >
              {announcement}
              <ArrowRight className="h-3 w-3" aria-hidden="true" />
            </a>
          ) : (
            <p>{announcement}</p>
          )}
        </div>
      )}

      {/* ---- Main navbar ---- */}
      <header
        role="banner"
        className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
          announcement ? "top-[36px]" : "top-0"
        } ${
          scrolled
            ? "bg-background/80 backdrop-blur-lg border-b border-border/50 shadow-sm"
            : "bg-transparent"
        }`}
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between px-6 h-16">
          {/* Logo */}
          <a
            href="/"
            className="relative z-10 hover:opacity-80 transition-opacity duration-150"
            aria-label="Home"
          >
            {logo}
          </a>

          {/* Desktop nav links */}
          <nav aria-label="Main navigation" className="hidden md:block">
            <ul className="flex items-center gap-8">
              {links.map((link) => (
                <li key={link.href}>
                  <button
                    onClick={() => scrollTo(link.href)}
                    className="relative text-sm font-medium text-muted-foreground hover:text-foreground transition-colors duration-150 after:absolute after:bottom-[-2px] after:left-0 after:h-[2px] after:w-0 after:bg-current after:transition-[width] after:duration-150 hover:after:w-full focus-visible:outline-2 focus-visible:outline-primary focus-visible:outline-offset-2 focus-visible:rounded-sm"
                  >
                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </nav>

          {/* Desktop CTA */}
          <motion.div
            className="hidden md:block"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            transition={{ duration: 0.15, ease: "easeInOut" }}
          >
            <Button
              asChild
              size="sm"
              className="rounded-lg px-4"
            >
              <a href={ctaHref}>{ctaText}</a>
            </Button>
          </motion.div>

          {/* Mobile hamburger */}
          <Sheet open={drawerOpen} onOpenChange={setDrawerOpen}>
            <SheetTrigger asChild>
              <button
                className="md:hidden p-2 rounded-md hover:bg-muted transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-primary focus-visible:outline-offset-2"
                aria-label="Open menu"
              >
                <Menu className="h-5 w-5" aria-hidden="true" />
              </button>
            </SheetTrigger>
            <SheetContent
              side="right"
              className="w-[300px] bg-background p-6"
            >
              <SheetHeader>
                <SheetTitle className="text-left">{logo}</SheetTitle>
              </SheetHeader>
              <nav aria-label="Mobile navigation" className="mt-8">
                <ul className="flex flex-col gap-4">
                  {links.map((link) => (
                    <li key={link.href}>
                      <button
                        onClick={() => scrollTo(link.href)}
                        className="w-full text-left text-base font-medium text-muted-foreground hover:text-foreground transition-colors duration-150 py-2 focus-visible:outline-2 focus-visible:outline-primary focus-visible:outline-offset-2 focus-visible:rounded-sm"
                      >
                        {link.label}
                      </button>
                    </li>
                  ))}
                </ul>
              </nav>
              <div className="mt-8">
                <Button
                  asChild
                  className="w-full rounded-lg"
                >
                  <a href={ctaHref} onClick={() => setDrawerOpen(false)}>
                    {ctaText}
                  </a>
                </Button>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </header>

      {/* ---- Sticky mobile CTA (appears after scrolling past hero) ---- */}
      <AnimatePresence>
        {pastHero && (
          <motion.div
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="fixed bottom-0 inset-x-0 z-40 md:hidden bg-background/95 backdrop-blur-md border-t border-border px-4 py-3 pb-[env(safe-area-inset-bottom)]"
          >
            <Button asChild className="w-full rounded-lg">
              <a href={ctaHref}>{ctaText}</a>
            </Button>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
```
