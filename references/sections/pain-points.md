# Pain Points -- "Is This You?" Section

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**AGITATE THE PAIN** -- Make the visitor feel seen by naming their exact frustrations.
When prospects think "yes, that's exactly my problem," they become primed for the
solution you present in the next section. This is the emotional bridge between the
hero promise and the feature showcase.

---

## Desktop Layout

```
┌──────────────────────────────────────────────────────┐
│                   "Sound familiar?"                  │
│        "You're not alone. These are the              │
│         problems we hear every single day."          │
│                                                      │
│  ┌─────────────────┐  ┌─────────────────┐           │
│  │ 🔴 Icon         │  │ 🔴 Icon         │           │
│  │ Pain headline   │  │ Pain headline   │           │
│  │ 1-2 sentence    │  │ 1-2 sentence    │           │
│  │ description     │  │ description     │           │
│  └─────────────────┘  └─────────────────┘           │
│  ┌─────────────────┐  ┌─────────────────┐           │
│  │ 🔴 Icon         │  │ 🔴 Icon         │           │
│  │ Pain headline   │  │ Pain headline   │           │
│  │ 1-2 sentence    │  │ 1-2 sentence    │           │
│  │ description     │  │ description     │           │
│  └─────────────────┘  └─────────────────┘           │
│                                                      │
│              [ optional 5th card centered ]           │
└──────────────────────────────────────────────────────┘
```

- 2-column grid (`md:grid-cols-2`) or 3-column (`lg:grid-cols-3`)
- If odd number of cards, last card centered with `col-span` logic
- Cards have generous padding (`p-6 sm:p-8`)
- Max-width: `max-w-5xl mx-auto`

---

## Mobile Layout (mobile-first)

```
┌──────────────────────┐
│  "Sound familiar?"   │
│  Intro paragraph     │
│                      │
│  ┌──────────────────┐│
│  │ Icon             ││
│  │ Pain headline    ││
│  │ Description text ││
│  └──────────────────┘│
│  ┌──────────────────┐│
│  │ Icon             ││
│  │ Pain headline    ││
│  │ Description text ││
│  └──────────────────┘│
│  ┌──────────────────┐│
│  │ ...              ││
│  └──────────────────┘│
└──────────────────────┘
```

- Single column stack (`grid-cols-1`)
- Cards have full width with `p-5` padding
- Spacing between cards: `gap-4`
- Section padding: `py-12` mobile, `py-20` desktop

---

## Copy Structure

| Element            | Content Pattern                                          | Character Limit |
|--------------------|----------------------------------------------------------|-----------------|
| Section tag        | "Sound familiar?" or "Is this you?"                      | 25 chars        |
| Section intro      | Empathetic 1-2 sentence hook                             | 120 chars       |
| Pain headline      | Specific frustration in the prospect's own words         | 50 chars        |
| Pain description   | Expand on the consequence of the problem                 | 140 chars       |

---

## Section-Specific Notes

- Uses destructive color tokens for pain icons: `bg-destructive/10`, `text-destructive`
- Card hover border shifts to `border-destructive/30` (unique to this section)
- Tone: second person ("you"), conversational, empathetic. Never condescending.
- Supports 2-column or 3-column grid via `columns` prop

---

## Complete JSX Template

```tsx
"use client";

import React from "react";
import { motion } from "framer-motion";
import {
  Clock,
  AlertTriangle,
  DollarSign,
  Frown,
  RefreshCw,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

// ------------------------------------------------------------------
// Types
// ------------------------------------------------------------------
interface PainPoint {
  icon: React.ElementType;
  headline: string;
  description: string;
}

// ------------------------------------------------------------------
// Default data (replace per-project)
// ------------------------------------------------------------------
const defaultPainPoints: PainPoint[] = [
  {
    icon: Clock,
    headline: "Wasting hours on manual busywork",
    description:
      "You spend more time copy-pasting between tools than doing the strategic work you were hired for.",
  },
  {
    icon: AlertTriangle,
    headline: "Scattered data, zero visibility",
    description:
      "Critical information lives in 5 different spreadsheets. By the time you find it, it's already outdated.",
  },
  {
    icon: DollarSign,
    headline: "Tools that cost more than they save",
    description:
      "Your current stack charges per seat and per feature. The bill keeps climbing but productivity doesn't.",
  },
  {
    icon: Frown,
    headline: "Your team dreads using the software",
    description:
      "Adoption is low because the UX is painful. People revert to email and sticky notes instead.",
  },
  {
    icon: RefreshCw,
    headline: "Onboarding takes weeks, not minutes",
    description:
      "Every new hire means another round of training sessions, screen recordings, and support tickets.",
  },
];

// ------------------------------------------------------------------
// Animation variants
// ------------------------------------------------------------------
const staggerContainer = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.12 },
  },
};

const staggerItem = {
  hidden: { opacity: 0, y: 20 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

// ------------------------------------------------------------------
// Sub-components
// ------------------------------------------------------------------
function PainCard({ point }: { point: PainPoint }) {
  const Icon = point.icon;

  return (
    <motion.div variants={staggerItem}>
      <Card
        className="group h-full border border-[hsl(var(--border))]
                   bg-[hsl(var(--card))] rounded-xl
                   hover:border-[hsl(var(--destructive)/0.3)]
                   hover:shadow-md hover:-translate-y-1
                   transition-all duration-300 ease-out"
      >
        <CardContent className="flex flex-col gap-3 p-5 sm:p-6 lg:p-8">
          {/* Icon */}
          <div
            className="flex h-10 w-10 items-center justify-center rounded-lg
                       bg-[hsl(var(--destructive)/0.1)]
                       group-hover:bg-[hsl(var(--destructive)/0.15)]
                       group-hover:scale-110
                       transition-all duration-300"
            aria-hidden="true"
          >
            <Icon className="h-5 w-5 text-[hsl(var(--destructive))]" />
          </div>

          {/* Headline */}
          <h3 className="text-lg font-semibold text-[hsl(var(--foreground))]">
            {point.headline}
          </h3>

          {/* Description */}
          <p className="text-sm leading-relaxed text-[hsl(var(--muted-foreground))]">
            {point.description}
          </p>
        </CardContent>
      </Card>
    </motion.div>
  );
}

// ------------------------------------------------------------------
// Main Component
// ------------------------------------------------------------------
interface PainPointsProps {
  tag?: string;
  intro?: string;
  painPoints?: PainPoint[];
  /** Grid columns on large screens: 2 or 3 */
  columns?: 2 | 3;
}

export default function PainPoints({
  tag = "Sound familiar?",
  intro = "You're not alone. These are the problems we hear every single day from teams just like yours.",
  painPoints = defaultPainPoints,
  columns = 2,
}: PainPointsProps) {
  const gridCols =
    columns === 3
      ? "md:grid-cols-2 lg:grid-cols-3"
      : "md:grid-cols-2";

  return (
    <section
      aria-labelledby="pain-points-heading"
      className="relative w-full overflow-hidden
                 py-12 sm:py-16 lg:py-20
                 bg-[hsl(var(--background))]"
    >
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        {/* ---- Header ---- */}
        <div className="mx-auto mb-10 max-w-2xl text-center sm:mb-14">
          <motion.span
            id="pain-points-heading"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.4 }}
            className="mb-3 inline-block text-sm font-semibold uppercase tracking-widest
                       text-[hsl(var(--primary))]"
          >
            {tag}
          </motion.span>

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

        {/* ---- Pain Point Cards ---- */}
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-60px" }}
          className={`grid grid-cols-1 gap-4 sm:gap-6 ${gridCols}`}
        >
          {painPoints.map((point) => (
            <PainCard key={point.headline} point={point} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}
```
