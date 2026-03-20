# How It Works -- Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**SHOW THE SOLUTION** -- Simplify understanding of the product by breaking the user journey
into 3-4 concrete, numbered steps. Reduce perceived complexity so the visitor thinks
"that's it?" rather than "that sounds complicated."

---

## Desktop Layout

```
[Step 1: Icon + Number] -----> [Step 2: Icon + Number] -----> [Step 3: Icon + Number]
   Title                           Title                           Title
   Description                     Description                     Description
```

- Horizontal `flex-row` with `justify-between` or `justify-center gap-16`
- Connecting line between steps: CSS `border-top` on a pseudo-element or thin SVG arrow
- Each step card is `max-w-xs text-center`
- Circled number: `w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center`
- Optional Lucide icon above the number or replacing it

---

## Mobile Layout (mobile-first)

```
[Step 1]
   |
   | (vertical line)
   |
[Step 2]
   |
   | (vertical line)
   |
[Step 3]
```

- Vertical `flex-col` with left-aligned steps
- Vertical connecting line: `border-left` on a wrapper or absolute-positioned `div`
- Each step uses `flex-row` internally: number/icon on left, text on right
- Number circle shrinks to `w-10 h-10`
- Full-width text block beside the number

---

## Copy Structure

| Element          | Guidelines                                          |
|------------------|-----------------------------------------------------|
| Section eyebrow  | "How It Works" (uppercase, tracking-wider, small)   |
| Section heading   | "Get started in minutes" or similar benefit-driven  |
| Step number       | "1", "2", "3" (or "01", "02", "03" for premium)    |
| Step title        | 2-4 words, action-oriented ("Connect Your Data")    |
| Step description  | 1-2 sentences, plain language, no jargon            |

---

## Section-Specific Notes

- Steps use ordered list (`<ol>`) for semantic step ordering
- Connecting line between steps: CSS border (horizontal on desktop, vertical on mobile)
- Connecting line optionally animates with `scaleX`/`scaleY`
- Step stagger delay is 200ms (slightly longer than standard 120ms)
- Number circles: `w-12 h-12 rounded-full bg-primary text-primary-foreground`

---

## Complete JSX Template

```tsx
"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Zap, Settings, BarChart3, Rocket } from "lucide-react";

// --- Data -------------------------------------------------------------------

const steps = [
  {
    number: "01",
    title: "Connect Your Data",
    description:
      "Link your existing tools in two clicks. We support 50+ integrations out of the box.",
    icon: Zap,
  },
  {
    number: "02",
    title: "Configure Your Workflow",
    description:
      "Set up automations with our visual builder. No code required, no learning curve.",
    icon: Settings,
  },
  {
    number: "03",
    title: "Monitor & Optimize",
    description:
      "Track performance in real-time dashboards and let AI surface actionable insights.",
    icon: BarChart3,
  },
];

// --- Animation Variants -----------------------------------------------------

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.2 },
  },
};

const stepVariants = {
  hidden: { opacity: 0, y: 30 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

const lineVariants = {
  hidden: { scaleX: 0 },
  show: {
    scaleX: 1,
    transition: { duration: 0.6, ease: "easeOut", delay: 0.3 },
  },
};

const lineVariantsMobile = {
  hidden: { scaleY: 0 },
  show: {
    scaleY: 1,
    transition: { duration: 0.6, ease: "easeOut", delay: 0.3 },
  },
};

// --- Step Card ---------------------------------------------------------------

function StepCard({
  step,
}: {
  step: (typeof steps)[number];
}) {
  const Icon = step.icon;

  return (
    <motion.li
      variants={stepVariants}
      className="relative flex flex-col items-center text-center md:max-w-xs"
    >
      {/* Number Circle */}
      <motion.div
        whileHover={{ scale: 1.1 }}
        transition={{ duration: 0.2 }}
        className="flex h-12 w-12 items-center justify-center rounded-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] text-sm font-bold shadow-md"
      >
        <span aria-hidden="true">{step.number}</span>
      </motion.div>

      {/* Icon */}
      <div className="mt-4 flex h-10 w-10 items-center justify-center rounded-lg bg-[hsl(var(--primary)/0.1)]">
        <Icon className="h-5 w-5 text-[hsl(var(--primary))]" aria-hidden="true" />
      </div>

      {/* Text */}
      <h3 className="mt-4 text-lg font-semibold text-[hsl(var(--foreground))]">
        {step.title}
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-[hsl(var(--muted-foreground))]">
        {step.description}
      </p>
    </motion.li>
  );
}

// --- Connector Line ----------------------------------------------------------

function ConnectorDesktop() {
  return (
    <motion.div
      variants={lineVariants}
      className="hidden md:block h-px w-full max-w-[80px] origin-left bg-[hsl(var(--border))]"
      aria-hidden="true"
    />
  );
}

function ConnectorMobile() {
  return (
    <motion.div
      variants={lineVariantsMobile}
      className="block md:hidden h-10 w-px origin-top bg-[hsl(var(--border))]"
      aria-hidden="true"
    />
  );
}

// --- Main Section ------------------------------------------------------------

export default function HowItWorks() {
  return (
    <section
      className="relative py-20 md:py-28 bg-[hsl(var(--muted)/0.3)]"
      aria-labelledby="how-it-works-heading"
    >
      <div className="mx-auto max-w-5xl px-6">
        {/* Header */}
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-medium uppercase tracking-wider text-[hsl(var(--primary))]">
            How It Works
          </p>
          <h2
            id="how-it-works-heading"
            className="mt-3 text-3xl font-bold tracking-tight text-[hsl(var(--foreground))] md:text-4xl"
          >
            Get started in three simple steps
          </h2>
          <p className="mt-4 text-base text-[hsl(var(--muted-foreground))]">
            No complex setup. No lengthy onboarding. Connect, configure, and go
            live in under five minutes.
          </p>
        </div>

        {/* Steps -- Desktop: horizontal row, Mobile: vertical stack */}
        <motion.ol
          variants={containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-80px" }}
          className="
            mt-16
            flex flex-col items-center gap-2
            md:flex-row md:items-start md:justify-center md:gap-6
          "
          role="list"
        >
          {steps.map((step, index) => (
            <div
              key={step.number}
              className="flex flex-col items-center md:flex-row md:items-start md:gap-6"
            >
              <StepCard step={step} />

              {/* Connector between steps (not after the last one) */}
              {index < steps.length - 1 && (
                <>
                  <ConnectorDesktop />
                  <ConnectorMobile />
                </>
              )}
            </div>
          ))}
        </motion.ol>
      </div>
    </section>
  );
}
```

### Usage Notes

- Swap the `steps` array data to match the product being built.
- Add a 4th step by pushing another object to the array -- the layout adapts automatically.
- To use SVG arrows instead of plain lines, replace the `Connector*` components with inline SVG.
- For a premium variant, animate the connector line color from `--border` to `--primary` as each step reveals.
- Icons are optional -- remove the icon block and the `icon` field from data if not needed.
