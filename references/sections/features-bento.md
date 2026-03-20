# Features -- Bento Grid Layout

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**SHOW THE SOLUTION** -- After agitating the pain, present your features as the
antidote. The bento grid format creates visual hierarchy: the most important feature
gets the largest card, supporting features fill the remaining cells. This layout
signals sophistication and a well-rounded product.

---

## Desktop Layout

```
┌──────────────────────────────────────────────────────┐
│            "Everything you need to..."               │
│            Section intro text                        │
│                                                      │
│  ┌────────────────────────┐  ┌──────────────┐       │
│  │                        │  │  Medium Card │       │
│  │     Large Feature      │  │  icon+title  │       │
│  │     (2 col x 2 row)    │  │  desc+visual │       │
│  │     icon + title       │  ├──────────────┤       │
│  │     desc + visual      │  │  Medium Card │       │
│  │                        │  │  icon+title  │       │
│  │                        │  │  desc+visual │       │
│  └────────────────────────┘  └──────────────┘       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐       │
│  │  Small   │  │  Small   │  │  Small Card  │       │
│  │  Card    │  │  Card    │  │  (optional)  │       │
│  └──────────┘  └──────────┘  └──────────────┘       │
└──────────────────────────────────────────────────────┘
```

- CSS Grid: `grid-cols-3`, `grid-rows-[auto]`
- Large card: `col-span-2 row-span-2`
- Medium cards: `col-span-1 row-span-1`
- Small cards: `col-span-1 row-span-1`
- Gap: `gap-4 sm:gap-6`
- Max-width: `max-w-6xl mx-auto`

---

## Mobile Layout (mobile-first)

```
┌──────────────────────┐
│  Section heading     │
│  Section intro       │
│                      │
│  ┌──────────────────┐│
│  │ Feature 1 (lg)   ││
│  │ Full width card  ││
│  └──────────────────┘│
│  ┌──────────────────┐│
│  │ Feature 2 (md)   ││
│  └──────────────────┘│
│  ┌──────────────────┐│
│  │ Feature 3 (md)   ││
│  └──────────────────┘│
│  ┌──────────────────┐│
│  │ Feature 4 (sm)   ││
│  └──────────────────┘│
│  ┌──────────────────┐│
│  │ Feature 5 (sm)   ││
│  └──────────────────┘│
└──────────────────────┘
```

- Stacks to `grid-cols-1` on mobile
- All cards become the same width but keep relative content differences
- Large cards still show more content than small cards
- Section padding: `py-12` mobile, `py-20` desktop

---

## Copy Structure

| Element             | Content Pattern                                     | Character Limit |
|---------------------|-----------------------------------------------------|-----------------|
| Section tag         | "Features" or "What's included"                     | 25 chars        |
| Section heading     | Benefit-oriented heading                            | 60 chars        |
| Section intro       | Supporting sentence                                 | 140 chars       |
| Feature title       | Short, action-oriented                              | 40 chars        |
| Feature description | "Do X so that Y" benefit clause                     | 120 chars       |
| Feature badge       | Optional label: "New", "Popular", "Beta"            | 10 chars        |

Every feature description should include a **"so that"** benefit clause:
"Automate your reports **so that** you reclaim 5 hours every week."

---

## Section-Specific Notes

- Large card spans `col-span-2 row-span-2`; medium and small cards are `col-span-1`.
- Cards use group hover: `group-hover:scale-110` on the icon container.
- Optional badge per feature ("New", "Popular", "Beta").
- Large card supports an optional visual slot (chart mockup, illustration).

---

## Complete JSX Template

```tsx
"use client";

import React from "react";
import { motion } from "framer-motion";
import {
  BarChart3,
  Zap,
  Shield,
  Users,
  Globe,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// ------------------------------------------------------------------
// Types
// ------------------------------------------------------------------
type CardSize = "large" | "medium" | "small";

interface Feature {
  icon: React.ElementType;
  title: string;
  description: string;
  size: CardSize;
  badge?: string;
  visual?: React.ReactNode;
}

// ------------------------------------------------------------------
// Default data (replace per-project)
// ------------------------------------------------------------------
const defaultFeatures: Feature[] = [
  {
    icon: BarChart3,
    title: "Real-time analytics dashboard",
    description:
      "Monitor every metric in one place so that you can make data-driven decisions in seconds, not days.",
    size: "large",
    badge: "Popular",
    visual: (
      <div
        className="mt-4 h-32 w-full rounded-lg bg-gradient-to-br
                   from-[hsl(var(--primary)/0.1)] to-[hsl(var(--primary)/0.05)]
                   flex items-center justify-center"
        aria-hidden="true"
      >
        <BarChart3 className="h-16 w-16 text-[hsl(var(--primary)/0.3)]" />
      </div>
    ),
  },
  {
    icon: Zap,
    title: "Instant automations",
    description:
      "Set up workflows in minutes so that your team can focus on high-value work instead of repetitive tasks.",
    size: "medium",
    badge: "New",
  },
  {
    icon: Shield,
    title: "Enterprise-grade security",
    description:
      "SOC 2 compliant with end-to-end encryption so that your data stays protected at every layer.",
    size: "medium",
  },
  {
    icon: Users,
    title: "Team collaboration",
    description:
      "Built-in comments and mentions so that everyone stays aligned without switching tools.",
    size: "small",
  },
  {
    icon: Globe,
    title: "Global CDN",
    description:
      "Sub-100ms response times worldwide so that your users get a fast experience everywhere.",
    size: "small",
  },
];

// ------------------------------------------------------------------
// Grid span mapping
// ------------------------------------------------------------------
const sizeClasses: Record<CardSize, string> = {
  large: "md:col-span-2 md:row-span-2",
  medium: "md:col-span-1 md:row-span-1",
  small: "md:col-span-1 md:row-span-1",
};

// ------------------------------------------------------------------
// Animation variants
// ------------------------------------------------------------------
const staggerContainer = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const staggerItem = {
  hidden: { opacity: 0, y: 20, scale: 0.95 },
  show: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

// ------------------------------------------------------------------
// Sub-components
// ------------------------------------------------------------------
function FeatureCard({ feature }: { feature: Feature }) {
  const Icon = feature.icon;
  const isLarge = feature.size === "large";

  return (
    <motion.div variants={staggerItem} className={sizeClasses[feature.size]}>
      <Card
        className="group relative h-full overflow-hidden rounded-2xl
                   border border-[hsl(var(--border))]
                   bg-[hsl(var(--card))] shadow-sm
                   hover:shadow-xl hover:-translate-y-1 hover:scale-[1.01]
                   hover:border-[hsl(var(--primary)/0.2)]
                   transition-all duration-300 ease-out"
      >
        <CardContent
          className={`flex flex-col gap-3 ${
            isLarge ? "p-6 sm:p-8 lg:p-10" : "p-5 sm:p-6"
          }`}
        >
          {/* Badge */}
          {feature.badge && (
            <Badge
              className="w-fit bg-[hsl(var(--primary))]
                         text-[hsl(var(--primary-foreground))]
                         text-xs font-medium"
            >
              {feature.badge}
            </Badge>
          )}

          {/* Icon */}
          <div
            className="flex h-10 w-10 items-center justify-center rounded-lg
                       bg-[hsl(var(--primary)/0.1)]
                       group-hover:bg-[hsl(var(--primary)/0.15)]
                       group-hover:scale-110
                       transition-all duration-300"
            aria-hidden="true"
          >
            <Icon className="h-5 w-5 text-[hsl(var(--primary))]" />
          </div>

          {/* Title */}
          <h3
            className={`font-semibold text-[hsl(var(--foreground))] ${
              isLarge ? "text-xl sm:text-2xl" : "text-lg"
            }`}
          >
            {feature.title}
          </h3>

          {/* Description */}
          <p
            className={`leading-relaxed text-[hsl(var(--muted-foreground))] ${
              isLarge ? "text-base" : "text-sm"
            }`}
          >
            {feature.description}
          </p>

          {/* Optional visual (large card only) */}
          {feature.visual && feature.visual}
        </CardContent>
      </Card>
    </motion.div>
  );
}

// ------------------------------------------------------------------
// Main Component
// ------------------------------------------------------------------
interface FeaturesBentoProps {
  tag?: string;
  heading?: string;
  intro?: string;
  features?: Feature[];
}

export default function FeaturesBento({
  tag = "Features",
  heading = "Everything you need to move faster",
  intro = "A complete toolkit designed to eliminate busywork and help your team ship what matters.",
  features = defaultFeatures,
}: FeaturesBentoProps) {
  return (
    <section
      aria-labelledby="features-bento-heading"
      className="relative w-full overflow-hidden
                 py-12 sm:py-16 lg:py-20
                 bg-[hsl(var(--background))]"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        {/* ---- Header ---- */}
        <div className="mx-auto mb-10 max-w-2xl text-center sm:mb-14">
          <motion.span
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.4 }}
            className="mb-3 inline-block text-sm font-semibold uppercase tracking-widest
                       text-[hsl(var(--primary))]"
          >
            {tag}
          </motion.span>

          <motion.h2
            id="features-bento-heading"
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5, delay: 0.05 }}
            className="mb-4 text-3xl font-bold tracking-tight
                       text-[hsl(var(--foreground))]
                       sm:text-4xl lg:text-5xl"
          >
            {heading}
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-base sm:text-lg leading-relaxed
                       text-[hsl(var(--muted-foreground))]"
          >
            {intro}
          </motion.p>
        </div>

        {/* ---- Bento Grid ---- */}
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-60px" }}
          className="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-3"
        >
          {features.map((feature) => (
            <FeatureCard key={feature.title} feature={feature} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}
```
