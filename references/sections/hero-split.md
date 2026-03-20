## Hero Split

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

### Conversion Job
STOP THE SCROLL -- The split hero must arrest attention within 3 seconds. Left side
delivers the value proposition through copy; right side provides visual proof via a
product screenshot in a browser mockup frame.

### Desktop Layout
```
[Badge pill                                    ]
[H1 Headline (60%)       ] [Product Screenshot (40%)]
[Subheadline             ] [  in browser mockup     ]
[CTA Primary] [CTA Ghost ] [                        ]
[Trust hint              ] [                        ]

--- Background effect slot (absolute, behind all content) ---
```
- Outer: `relative min-h-screen flex items-center overflow-hidden`
- Inner: `max-w-7xl mx-auto px-6 py-24 md:py-32`
- Grid: `flex flex-col md:flex-row md:items-center gap-12 md:gap-16`
- Left column: `flex-1 md:max-w-[60%]`
- Right column: `flex-1 md:max-w-[40%]`

### Mobile Layout (mobile-first)
- Single column, stacked vertically
- Order: badge -> headline -> subheadline -> CTA group -> trust hint -> screenshot
- Screenshot scales to full width with slight horizontal negative margin for edge bleed
- CTA buttons stack: primary full-width, secondary full-width below
- `flex flex-col gap-6 text-center md:text-left`

### Copy Structure
| Element       | Limit             | Framework                    |
|---------------|-------------------|------------------------------|
| Badge pill    | 3-6 words         | Novelty / recency signal     |
| H1 headline   | Max 10 words      | Value prop (PAS / AIDA)      |
| Subheadline   | 15-25 words       | Expand on the "how" or "who" |
| CTA primary   | 2-4 words         | Action verb + outcome        |
| CTA secondary | 2-4 words         | Lower commitment alternative |
| Trust hint    | Max 60 chars      | Social proof micro-copy      |

### Section-Specific Notes
- Screenshot uses custom slide-in from right: `hidden: { x: 40 }` → `show: { x: 0, delay: 0.4 }`
- Hero image should use priority loading (above the fold)
- Browser mockup frame is pure CSS (no image dependency)
- Background effect: dynamic import with fallback

### Complete JSX Template
```tsx
"use client";

import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

// ------------------------------------------------------------------ Types
interface HeroSplitProps {
  badge?: string;
  headline: string;
  subheadline: string;
  ctaPrimaryText?: string;
  ctaPrimaryHref?: string;
  ctaSecondaryText?: string;
  ctaSecondaryHref?: string;
  trustHint?: string;
  screenshotSrc: string;
  screenshotAlt: string;
  backgroundEffect?: React.ReactNode;
}

// ------------------------------------------------------------------ Variants
const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.12, delayChildren: 0.1 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 24 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

const screenshotVariants = {
  hidden: { opacity: 0, x: 40 },
  show: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.6, ease: "easeOut", delay: 0.4 },
  },
};

// ------------------------------------------------------------------ Component
export default function HeroSplit({
  badge,
  headline,
  subheadline,
  ctaPrimaryText = "Get Started",
  ctaPrimaryHref = "#cta",
  ctaSecondaryText = "Learn More",
  ctaSecondaryHref = "#features",
  trustHint = "Join 500+ teams already shipping faster",
  screenshotSrc,
  screenshotAlt,
  backgroundEffect,
}: HeroSplitProps) {
  return (
    <section
      aria-labelledby="hero-heading"
      className="relative min-h-screen flex items-center overflow-hidden"
    >
      {/* ---- Background effect slot ---- */}
      {backgroundEffect && (
        <div className="absolute inset-0 z-0" aria-hidden="true">
          {backgroundEffect}
        </div>
      )}

      {/* ---- Content ---- */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-24 md:py-32 w-full">
        <div className="flex flex-col md:flex-row md:items-center gap-12 md:gap-16">
          {/* ---- Left column: copy ---- */}
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, margin: "-100px" }}
            className="flex-1 md:max-w-[60%] flex flex-col items-center md:items-start text-center md:text-left gap-6"
          >
            {/* Badge */}
            {badge && (
              <motion.span
                variants={itemVariants}
                className="inline-flex items-center gap-2 rounded-full border border-border bg-muted/50 px-4 py-1.5 text-sm font-medium text-foreground hover:bg-muted transition-colors duration-200"
              >
                <Sparkles className="h-3.5 w-3.5 text-primary" aria-hidden="true" />
                {badge}
              </motion.span>
            )}

            {/* Headline */}
            <motion.h1
              id="hero-heading"
              variants={itemVariants}
              className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-foreground leading-[1.1]"
            >
              {headline}
            </motion.h1>

            {/* Subheadline */}
            <motion.p
              variants={itemVariants}
              className="text-lg sm:text-xl text-muted-foreground max-w-xl leading-relaxed"
            >
              {subheadline}
            </motion.p>

            {/* CTA Group */}
            <motion.div
              variants={itemVariants}
              className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto"
            >
              <Button
                asChild
                size="lg"
                className="w-full sm:w-auto rounded-lg px-6 shadow-lg shadow-primary/20"
              >
                <motion.a
                  href={ctaPrimaryHref}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  transition={{ duration: 0.15, ease: "easeInOut" }}
                >
                  {ctaPrimaryText}
                  <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" />
                </motion.a>
              </Button>

              <Button
                asChild
                variant="outline"
                size="lg"
                className="w-full sm:w-auto rounded-lg px-6"
              >
                <a href={ctaSecondaryHref}>{ctaSecondaryText}</a>
              </Button>
            </motion.div>

            {/* Trust hint */}
            {trustHint && (
              <motion.p
                variants={itemVariants}
                className="text-sm text-muted-foreground"
                aria-label={trustHint}
              >
                {trustHint}
              </motion.p>
            )}
          </motion.div>

          {/* ---- Right column: screenshot in browser mockup ---- */}
          <motion.div
            variants={screenshotVariants}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, margin: "-100px" }}
            className="flex-1 md:max-w-[40%] w-full"
          >
            <div className="rounded-xl border border-border bg-muted overflow-hidden shadow-2xl hover:shadow-3xl transition-shadow duration-300">
              {/* Browser top bar */}
              <div
                className="h-10 bg-muted border-b border-border flex items-center px-4 gap-2"
                aria-hidden="true"
              >
                <span className="w-3 h-3 rounded-full bg-red-400" />
                <span className="w-3 h-3 rounded-full bg-yellow-400" />
                <span className="w-3 h-3 rounded-full bg-green-400" />
                <span className="ml-4 text-xs text-muted-foreground truncate">
                  yourproduct.com
                </span>
              </div>
              {/* Screenshot */}
              {/* Next.js: replace <img> with <Image> from "next/image" and add priority, quality={90}, sizes */}
              <img
                src={screenshotSrc}
                alt={screenshotAlt}
                width={800}
                height={500}
                loading="eager"
                className="w-full h-auto object-cover"
              />
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
```
