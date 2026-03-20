## Hero Centered

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

### Conversion Job
STOP THE SCROLL -- Centered hero is ideal when the product visual is the star.
All copy elements lead the eye downward to a full-width screenshot that provides
immediate visual proof. The symmetrical layout conveys confidence and polish.

### Desktop Layout
```
         [Background effect slot -- absolute, behind all content]

                        [Badge pill]
                     [H1 Headline]
                    [Subheadline text]
              [CTA Primary]  [CTA Secondary]
                      [Trust hint]

     [-------- Full-width product screenshot in browser mockup --------]
```
- Outer: `relative min-h-screen flex flex-col items-center justify-center overflow-hidden`
- Inner: `text-center max-w-4xl mx-auto px-6 py-24 md:py-32`
- Copy stack: `flex flex-col items-center gap-6`
- Screenshot container: `w-full max-w-5xl mx-auto mt-16 px-6`

### Mobile Layout (mobile-first)
- Same centered layout -- text sizes scale down, spacing tightens
- CTA buttons stack vertically, full-width
- Screenshot takes full viewport width with `mx-[-24px]` negative margin for edge bleed
- `text-center` on all breakpoints (no alignment change)
- `gap-5` on mobile, `gap-6` on desktop
- Badge, headline, subheadline, CTAs, trust hint all centered and stacked

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
- Screenshot uses rise-up animation: `hidden: { y: 60, scale: 0.95 }` -> `show: { y: 0, scale: 1, delay: 0.5 }`
- Headline scales up to `lg:text-7xl` (larger than split hero)
- Hero image should use priority loading (above the fold)

### Complete JSX Template
```tsx
"use client";

import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

// ------------------------------------------------------------------ Types
interface HeroCenteredProps {
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
    transition: { staggerChildren: 0.1, delayChildren: 0.1 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

const screenshotVariants = {
  hidden: { opacity: 0, y: 60, scale: 0.95 },
  show: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1], delay: 0.5 },
  },
};

// ------------------------------------------------------------------ Component
export default function HeroCentered({
  badge,
  headline,
  subheadline,
  ctaPrimaryText = "Get Started Free",
  ctaPrimaryHref = "#cta",
  ctaSecondaryText = "See How It Works",
  ctaSecondaryHref = "#features",
  trustHint = "Free trial -- No credit card required",
  screenshotSrc,
  screenshotAlt,
  backgroundEffect,
}: HeroCenteredProps) {
  return (
    <section
      aria-labelledby="hero-heading"
      className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden"
    >
      {/* ---- Background effect slot ---- */}
      {backgroundEffect && (
        <div className="absolute inset-0 z-0" aria-hidden="true">
          {backgroundEffect}
        </div>
      )}

      {/* ---- Copy content ---- */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: "-100px" }}
        className="relative z-10 text-center max-w-4xl mx-auto px-6 py-24 md:py-32 flex flex-col items-center gap-5 md:gap-6"
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
          className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight text-foreground leading-[1.08] max-w-4xl"
        >
          {headline}
        </motion.h1>

        {/* Subheadline */}
        <motion.p
          variants={itemVariants}
          className="text-lg sm:text-xl text-muted-foreground max-w-2xl leading-relaxed"
        >
          {subheadline}
        </motion.p>

        {/* CTA Group */}
        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto mt-2"
        >
          <Button
            asChild
            size="lg"
            className="w-full sm:w-auto rounded-lg px-8 shadow-lg shadow-primary/20"
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
            className="w-full sm:w-auto rounded-lg px-8"
          >
            <a href={ctaSecondaryHref}>{ctaSecondaryText}</a>
          </Button>
        </motion.div>

        {/* Trust hint */}
        {trustHint && (
          <motion.p
            variants={itemVariants}
            className="text-sm text-muted-foreground"
          >
            {trustHint}
          </motion.p>
        )}
      </motion.div>

      {/* ---- Product screenshot in browser mockup ---- */}
      <motion.div
        variants={screenshotVariants}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: "-100px" }}
        className="relative z-10 w-full max-w-5xl mx-auto px-6 pb-24"
      >
        <div className="rounded-xl border border-border bg-muted overflow-hidden shadow-2xl shadow-black/10 hover:shadow-3xl transition-shadow duration-300">
          {/* Browser top bar */}
          <div
            className="h-10 bg-muted border-b border-border flex items-center px-4 gap-2"
            aria-hidden="true"
          >
            <span className="w-3 h-3 rounded-full bg-red-400" />
            <span className="w-3 h-3 rounded-full bg-yellow-400" />
            <span className="w-3 h-3 rounded-full bg-green-400" />
            <span className="ml-4 flex-1">
              <span className="inline-block rounded-md bg-background/50 px-3 py-1 text-xs text-muted-foreground">
                yourproduct.com
              </span>
            </span>
          </div>
          {/* Screenshot */}
          {/* Next.js: replace <img> with <Image> from "next/image" and add priority, quality={90}, sizes */}
          <img
            src={screenshotSrc}
            alt={screenshotAlt}
            width={1200}
            height={750}
            loading="eager"
            className="w-full h-auto object-cover"
          />
        </div>
      </motion.div>
    </section>
  );
}
```
