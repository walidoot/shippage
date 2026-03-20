# CTA Footer Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**Part 1 -- Final CTA:** MAKE THE ASK. This is the last conversion opportunity. The visitor has scrolled through every argument. Now give them one clean, confident prompt to act.

**Part 2 -- Footer:** NAVIGATION + LEGAL. Provide secondary navigation, legal links, and social presence without competing with the CTA above.

---

## Desktop Layout

### CTA Section
- Full-width container with dark or accent background
- Inner content: `max-w-2xl mx-auto text-center`
- Headline, subheadline, and CTA button stacked vertically
- Trust hints centered below the button
- Generous padding: `py-20 lg:py-28`

### Footer
- Full-width, darker background than CTA
- Inner content: `max-w-6xl mx-auto`
- Multi-column flex layout: logo column + 3-4 link columns
- Copyright line spans full width at the bottom
- Padding: `py-12 lg:py-16`

## Mobile Layout (mobile-first)

### CTA Section
- Full width with `px-4 sm:px-6` padding
- Same centered stacking as desktop, responsive text sizes
- CTA button full width on mobile (`w-full sm:w-auto`)
- Reduced padding: `py-12 sm:py-16`

### Footer
- Columns stack vertically, centered text
- Logo and tagline centered at top
- Link groups stack with spacing between them
- Social icons centered
- Padding: `py-8 sm:py-12`

---

## Copy Structure

| Element | Content Rule |
|---|---|
| **CTA Heading** | Action-oriented: "Ready to [primary benefit]?" or "Start [doing thing] today." |
| **CTA Subheadline** | One sentence reiterating the core value prop. No new information. |
| **CTA Button** | Same label as hero CTA for consistency. "Start Free Trial", "Get Started Free", etc. |
| **Trust Hints** | Below button: "Free trial . No credit card . Cancel anytime" |
| **Footer Logo** | Product name or logo mark |
| **Footer Tagline** (optional) | One-liner brand statement |
| **Footer Links: Product** | Features, Pricing, Integrations, Changelog |
| **Footer Links: Company** | About, Blog, Careers, Contact |
| **Footer Links: Resources** | Documentation, Help Center, API Reference, Status |
| **Footer Links: Legal** | Privacy Policy, Terms of Service, Cookie Policy |
| **Social Icons** | Twitter/X, GitHub, LinkedIn (use Lucide icons) |
| **Copyright** | "(c) {year} {Company}. All rights reserved." |

---

## Section-Specific Notes

- CTA section uses inverted colors: `bg-primary` with `text-primary-foreground`
- CTA button is inverted: `bg-background text-primary` (stands out against primary bg)
- Optional radial glow behind CTA for focus
- Footer uses semantic `<footer role="contentinfo">`
- Social links include `aria-label` with platform name
- Footer content fades in as a single block (no stagger)
- CTA button is `w-full` on mobile, `w-auto` on sm+

---

## Complete JSX Template

```tsx
"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import { Twitter, Github, Linkedin } from "lucide-react";
import { Button } from "@/components/ui/button";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

interface FooterLinkGroup {
  title: string;
  links: { label: string; href: string }[];
}

interface CTAFooterProps {
  /* CTA Section */
  ctaHeading?: string;
  ctaSubheading?: string;
  ctaButtonLabel?: string;
  ctaButtonHref?: string;
  trustHints?: string[];
  /* Footer */
  companyName?: string;
  companyTagline?: string;
  footerLinks?: FooterLinkGroup[];
  socialLinks?: { platform: string; href: string; icon: React.ElementType }[];
}

// -------------------------------------------------------------------
// Defaults
// -------------------------------------------------------------------

const defaultFooterLinks: FooterLinkGroup[] = [
  {
    title: "Product",
    links: [
      { label: "Features", href: "#features" },
      { label: "Pricing", href: "#pricing" },
      { label: "Integrations", href: "#integrations" },
      { label: "Changelog", href: "/changelog" },
    ],
  },
  {
    title: "Company",
    links: [
      { label: "About", href: "/about" },
      { label: "Blog", href: "/blog" },
      { label: "Careers", href: "/careers" },
      { label: "Contact", href: "/contact" },
    ],
  },
  {
    title: "Resources",
    links: [
      { label: "Documentation", href: "/docs" },
      { label: "Help Center", href: "/help" },
      { label: "API Reference", href: "/api" },
      { label: "Status", href: "/status" },
    ],
  },
  {
    title: "Legal",
    links: [
      { label: "Privacy Policy", href: "/privacy" },
      { label: "Terms of Service", href: "/terms" },
      { label: "Cookie Policy", href: "/cookies" },
    ],
  },
];

const defaultSocialLinks = [
  { platform: "Twitter", href: "https://twitter.com", icon: Twitter },
  { platform: "GitHub", href: "https://github.com", icon: Github },
  { platform: "LinkedIn", href: "https://linkedin.com", icon: Linkedin },
];

const defaultTrustHints = ["Free trial", "No credit card", "Cancel anytime"];

// -------------------------------------------------------------------
// Animation variants
// -------------------------------------------------------------------

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: (delay: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut", delay },
  }),
};

const fadeIn = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

// -------------------------------------------------------------------
// Component
// -------------------------------------------------------------------

export default function CTAFooter({
  ctaHeading = "Ready to transform your workflow?",
  ctaSubheading = "Join thousands of teams already shipping faster. Start your free trial today.",
  ctaButtonLabel = "Get Started Free",
  ctaButtonHref = "#signup",
  trustHints = defaultTrustHints,
  companyName = "YourProduct",
  companyTagline = "Ship better software, faster.",
  footerLinks = defaultFooterLinks,
  socialLinks = defaultSocialLinks,
}: CTAFooterProps) {
  const ctaRef = useRef<HTMLElement>(null);
  const footerRef = useRef<HTMLElement>(null);
  const ctaInView = useInView(ctaRef, { once: true, margin: "-80px" });
  const footerInView = useInView(footerRef, { once: true, margin: "-40px" });

  const currentYear = new Date().getFullYear();

  return (
    <>
      {/* ================================================================
          PART 1: Final CTA Section
          ================================================================ */}
      <section
        ref={ctaRef}
        id="cta"
        aria-labelledby="cta-heading"
        className="relative overflow-hidden py-12 sm:py-16 lg:py-28 bg-primary"
      >
        {/* Optional radial glow background */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0
                     bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.12)_0%,transparent_70%)]"
        />

        <div className="relative mx-auto max-w-2xl px-4 sm:px-6 text-center">
          {/* Heading */}
          <motion.h2
            id="cta-heading"
            custom={0}
            variants={fadeUp}
            initial="hidden"
            animate={ctaInView ? "visible" : "hidden"}
            className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight
                       text-primary-foreground"
          >
            {ctaHeading}
          </motion.h2>

          {/* Subheadline */}
          <motion.p
            custom={0.1}
            variants={fadeUp}
            initial="hidden"
            animate={ctaInView ? "visible" : "hidden"}
            className="mt-4 sm:mt-6 text-base sm:text-lg
                       text-primary-foreground/80
                       max-w-xl mx-auto"
          >
            {ctaSubheading}
          </motion.p>

          {/* CTA Button */}
          <motion.div
            custom={0.2}
            variants={fadeUp}
            initial="hidden"
            animate={ctaInView ? "visible" : "hidden"}
            className="mt-8 sm:mt-10"
          >
            <Button
              asChild
              size="lg"
              className="w-full sm:w-auto px-8 py-3 text-base font-semibold
                         bg-background text-primary
                         hover:scale-105 hover:shadow-lg
                         transition-all duration-200 ease-out"
            >
              <a href={ctaButtonHref}>{ctaButtonLabel}</a>
            </Button>
          </motion.div>

          {/* Trust Hints */}
          {trustHints.length > 0 && (
            <motion.p
              custom={0.35}
              variants={fadeUp}
              initial="hidden"
              animate={ctaInView ? "visible" : "hidden"}
              className="mt-4 text-sm text-primary-foreground/60"
            >
              {trustHints.join(" \u00b7 ")}
            </motion.p>
          )}
        </div>
      </section>

      {/* ================================================================
          PART 2: Footer
          ================================================================ */}
      <footer
        ref={footerRef}
        role="contentinfo"
        className="bg-card border-t border-border"
      >
        <motion.div
          variants={fadeIn}
          initial="hidden"
          animate={footerInView ? "visible" : "hidden"}
          className="mx-auto max-w-6xl px-4 sm:px-6 py-8 sm:py-12 lg:py-16"
        >
          {/* Top: Logo + Link Columns */}
          <div className="flex flex-col items-center gap-10
                          lg:flex-row lg:items-start lg:justify-between">
            {/* Logo & Tagline */}
            <div className="text-center lg:text-left lg:max-w-xs shrink-0">
              <span className="text-xl font-bold text-foreground">
                {companyName}
              </span>
              {companyTagline && (
                <p className="mt-2 text-sm text-muted-foreground">
                  {companyTagline}
                </p>
              )}

              {/* Social Icons */}
              <div className="mt-5 flex items-center justify-center lg:justify-start gap-4">
                {socialLinks.map(({ platform, href, icon: Icon }) => (
                  <a
                    key={platform}
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`Follow us on ${platform}`}
                    className="text-muted-foreground
                               hover:text-foreground
                               hover:scale-110
                               transition-all duration-200"
                  >
                    <Icon className="h-5 w-5" />
                  </a>
                ))}
              </div>
            </div>

            {/* Link Columns */}
            <div className="grid grid-cols-2 gap-8 text-center
                            sm:grid-cols-4 sm:text-left">
              {footerLinks.map((group) => (
                <div key={group.title}>
                  <h3 className="text-sm font-semibold tracking-wide uppercase
                                 text-foreground">
                    {group.title}
                  </h3>
                  <ul className="mt-3 space-y-2" role="list">
                    {group.links.map((link) => (
                      <li key={link.label}>
                        <a
                          href={link.href}
                          className="text-sm
                                     text-muted-foreground
                                     hover:text-foreground
                                     transition-colors duration-200"
                        >
                          {link.label}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          {/* Bottom: Copyright */}
          <div className="mt-10 pt-6
                          border-t border-border
                          text-center">
            <p className="text-xs text-muted-foreground">
              &copy; {currentYear} {companyName}. All rights reserved.
            </p>
          </div>
        </motion.div>
      </footer>
    </>
  );
}
```
