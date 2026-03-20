# Features -- Alternating Left-Right Blocks

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**SHOW THE SOLUTION** -- Walk the visitor through your key features one at a time
with dedicated visual space for each. The alternating layout creates rhythm and keeps
the eye moving down the page. Each block pairs a specific feature with a screenshot
or visual proof, building cumulative confidence.

---

## Desktop Layout

```
┌──────────────────────────────────────────────────────┐
│            "How it works" / "Features"               │
│            Section intro text                        │
│                                                      │
│  ┌───────────────────┐  ┌───────────────────┐       │
│  │  TAG              │  │                   │       │
│  │  Headline         │  │   Screenshot in   │       │
│  │                   │  │   browser mockup  │       │
│  │  Description      │  │                   │       │
│  │  • Bullet point   │  │                   │       │
│  │  • Bullet point   │  │                   │       │
│  └───────────────────┘  └───────────────────┘       │
│                                                      │
│  ┌───────────────────┐  ┌───────────────────┐       │
│  │                   │  │  TAG              │       │
│  │   Screenshot in   │  │  Headline         │       │
│  │   phone mockup    │  │                   │       │
│  │                   │  │  Description      │       │
│  │                   │  │  • Bullet point   │       │
│  │                   │  │  • Bullet point   │       │
│  └───────────────────┘  └───────────────────┘       │
│                                                      │
│  ┌───────────────────┐  ┌───────────────────┐       │
│  │  TAG              │  │                   │       │
│  │  Headline         │  │   Screenshot in   │       │
│  │  ...              │  │   browser mockup  │       │
│  └───────────────────┘  └───────────────────┘       │
└──────────────────────────────────────────────────────┘
```

- Each block: `flex flex-col md:flex-row` (even index) or `md:flex-row-reverse` (odd index)
- Text column: 45% width, image column: 55% width on desktop
- Vertical spacing between blocks: `gap-16 sm:gap-20 lg:gap-28`
- Content vertically centered: `items-center`
- Max-width: `max-w-6xl mx-auto`

---

## Mobile Layout (mobile-first)

```
┌──────────────────────┐
│  Section heading     │
│  Section intro       │
│                      │
│  ┌──────────────────┐│
│  │ TAG              ││
│  │ Headline         ││
│  │ Description      ││
│  │ • Bullet         ││
│  │ • Bullet         ││
│  └──────────────────┘│
│  ┌──────────────────┐│
│  │  Screenshot in   ││
│  │  mockup frame    ││
│  └──────────────────┘│
│                      │
│  ┌──────────────────┐│
│  │ TAG              ││
│  │ Headline         ││
│  │ Description      ││
│  │ • Bullet         ││
│  └──────────────────┘│
│  ┌──────────────────┐│
│  │  Screenshot      ││
│  └──────────────────┘│
└──────────────────────┘
```

- Stacks to `flex-col` -- text ALWAYS above image (regardless of alternation)
- Image takes full width with `aspect-video` or `aspect-[4/3]`
- Section padding: `py-12` mobile, `py-20` desktop
- Block spacing: `gap-12` mobile

---

## Copy Structure

| Element             | Content Pattern                                        | Character Limit |
|---------------------|--------------------------------------------------------|-----------------|
| Section tag         | "How it works" or "Features"                           | 25 chars        |
| Section heading     | Benefit-driven heading                                 | 60 chars        |
| Section intro       | Supporting sentence                                    | 140 chars       |
| Feature tag         | Category label (e.g., "Analytics", "Collaboration")    | 20 chars        |
| Feature headline    | Action-benefit headline                                | 50 chars        |
| Feature description | Expanded explanation with "so that" benefit clause     | 200 chars       |
| Bullet points       | 2-3 supporting details, each starting with a verb      | 60 chars each   |

---

## Section-Specific Notes

- **Alternation direction**: Even-index blocks use `md:flex-row` (text left, image right); odd-index blocks use `md:flex-row-reverse` (image left, text right).
- **Mobile override**: On mobile, text ALWAYS appears above the image regardless of the alternation index.
- **Mockup frames**: Each block supports either a `"browser"` (desktop chrome) or `"phone"` (mobile device) mockup frame, set per block via `mockupType`.
- **Slide-in animation**: The text column slides in from the left (`x: -20`) on even blocks and from the right (`x: 20`) on odd blocks; the image column uses the opposite offset.

---

## Complete JSX Template

```tsx
"use client";

import React from "react";
import { motion } from "framer-motion";
import {
  BarChart3,
  Zap,
  Users,
  Check,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";

// ------------------------------------------------------------------
// Types
// ------------------------------------------------------------------
interface FeatureBlock {
  tag: string;
  headline: string;
  description: string;
  bullets?: string[];
  image: string;
  imageAlt: string;
  icon: React.ElementType;
  /** "browser" renders a desktop chrome frame, "phone" renders a mobile frame */
  mockupType?: "browser" | "phone";
}

// ------------------------------------------------------------------
// Default data (replace per-project)
// ------------------------------------------------------------------
const defaultFeatures: FeatureBlock[] = [
  {
    tag: "Analytics",
    headline: "See what matters at a glance",
    description:
      "A real-time dashboard that surfaces the metrics your team cares about so that you never miss a trend or anomaly.",
    bullets: [
      "Custom KPI widgets you can drag and drop",
      "Automated daily and weekly email digests",
      "Export to CSV, PDF, or direct to Slack",
    ],
    image: "/screenshots/dashboard.webp",
    imageAlt: "Analytics dashboard showing revenue charts and user growth metrics",
    icon: BarChart3,
    mockupType: "browser",
  },
  {
    tag: "Automation",
    headline: "Eliminate the busywork",
    description:
      "Build powerful workflows with a visual editor so that repetitive tasks run on autopilot while you focus on strategy.",
    bullets: [
      "50+ pre-built automation templates",
      "Conditional logic and branching paths",
      "Connects to your existing tools via API",
    ],
    image: "/screenshots/automation.webp",
    imageAlt: "Visual workflow builder showing a multi-step automation with branching logic",
    icon: Zap,
    mockupType: "browser",
  },
  {
    tag: "Collaboration",
    headline: "Keep your team in sync",
    description:
      "Built-in comments, mentions, and shared views so that context lives where the work happens -- not buried in chat threads.",
    bullets: [
      "Real-time multiplayer editing",
      "Thread-based discussions on any record",
      "Role-based permissions and audit trail",
    ],
    image: "/screenshots/collaboration.webp",
    imageAlt: "Team collaboration view with inline comments and shared task board",
    icon: Users,
    mockupType: "phone",
  },
];

// ------------------------------------------------------------------
// Sub-components
// ------------------------------------------------------------------

/** Browser-style mockup frame */
function BrowserMockup({
  image,
  imageAlt,
}: {
  image: string;
  imageAlt: string;
}) {
  return (
    <div
      className="overflow-hidden rounded-xl border border-[hsl(var(--border))]
                 bg-[hsl(var(--muted))] shadow-lg
                 group-hover:shadow-2xl group-hover:scale-[1.02]
                 transition-all duration-300 ease-out"
    >
      {/* Top bar */}
      <div
        className="flex items-center gap-1.5 border-b border-[hsl(var(--border))] px-4 py-2.5"
        aria-hidden="true"
      >
        <span className="h-2.5 w-2.5 rounded-full bg-red-400" />
        <span className="h-2.5 w-2.5 rounded-full bg-yellow-400" />
        <span className="h-2.5 w-2.5 rounded-full bg-green-400" />
        <span className="ml-3 h-5 flex-1 rounded-md bg-[hsl(var(--background))]" />
      </div>
      {/* Screenshot */}
      <img
        src={image}
        alt={imageAlt}
        loading="lazy"
        className="w-full object-cover"
      />
    </div>
  );
}

/** Phone-style mockup frame */
function PhoneMockup({
  image,
  imageAlt,
}: {
  image: string;
  imageAlt: string;
}) {
  return (
    <div
      className="mx-auto w-[260px] sm:w-[280px] overflow-hidden rounded-[2rem]
                 border-[6px] border-[hsl(var(--foreground)/0.15)]
                 bg-[hsl(var(--muted))] shadow-lg
                 group-hover:shadow-2xl group-hover:scale-[1.02]
                 transition-all duration-300 ease-out"
    >
      {/* Notch */}
      <div className="flex justify-center py-2" aria-hidden="true">
        <span className="h-5 w-20 rounded-full bg-[hsl(var(--foreground)/0.1)]" />
      </div>
      {/* Screenshot */}
      <img
        src={image}
        alt={imageAlt}
        loading="lazy"
        className="w-full object-cover"
      />
    </div>
  );
}

function FeatureBlockItem({
  feature,
  index,
}: {
  feature: FeatureBlock;
  index: number;
}) {
  const isReversed = index % 2 !== 0;
  const Icon = feature.icon;
  const Mockup =
    feature.mockupType === "phone" ? PhoneMockup : BrowserMockup;

  return (
    <motion.article
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className={`group flex flex-col items-center gap-8 sm:gap-12
                  md:flex-row md:gap-16
                  ${isReversed ? "md:flex-row-reverse" : ""}`}
    >
      {/* ---- Text Column ---- */}
      <motion.div
        initial={{ opacity: 0, x: isReversed ? 20 : -20 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.5, delay: 0.15, ease: "easeOut" }}
        className="flex flex-col gap-4 md:w-[45%]"
      >
        {/* Tag */}
        <Badge
          variant="secondary"
          className="w-fit bg-[hsl(var(--primary)/0.1)]
                     text-[hsl(var(--primary))] text-xs font-semibold
                     uppercase tracking-wider"
        >
          <Icon className="mr-1.5 h-3.5 w-3.5" aria-hidden="true" />
          {feature.tag}
        </Badge>

        {/* Headline */}
        <h3 className="text-2xl font-bold tracking-tight text-[hsl(var(--foreground))] sm:text-3xl">
          {feature.headline}
        </h3>

        {/* Description */}
        <p className="text-base leading-relaxed text-[hsl(var(--muted-foreground))]">
          {feature.description}
        </p>

        {/* Bullet points */}
        {feature.bullets && feature.bullets.length > 0 && (
          <ul className="mt-1 flex flex-col gap-2.5" role="list">
            {feature.bullets.map((bullet) => (
              <li
                key={bullet}
                className="flex items-start gap-2.5 text-sm
                           text-[hsl(var(--muted-foreground))]"
              >
                <Check
                  className="mt-0.5 h-4 w-4 shrink-0 text-[hsl(var(--primary))]"
                  aria-hidden="true"
                />
                <span>{bullet}</span>
              </li>
            ))}
          </ul>
        )}
      </motion.div>

      {/* ---- Image Column ---- */}
      <motion.div
        initial={{ opacity: 0, x: isReversed ? -20 : 20 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.5, delay: 0.2, ease: "easeOut" }}
        className="w-full md:w-[55%]"
      >
        <Mockup image={feature.image} imageAlt={feature.imageAlt} />
      </motion.div>
    </motion.article>
  );
}

// ------------------------------------------------------------------
// Main Component
// ------------------------------------------------------------------
interface FeaturesAlternatingProps {
  tag?: string;
  heading?: string;
  intro?: string;
  features?: FeatureBlock[];
}

export default function FeaturesAlternating({
  tag = "Features",
  heading = "Built for the way you actually work",
  intro = "Every feature is designed to save you time and remove friction from your daily workflow.",
  features = defaultFeatures,
}: FeaturesAlternatingProps) {
  return (
    <section
      aria-labelledby="features-alt-heading"
      className="relative w-full overflow-hidden
                 py-12 sm:py-16 lg:py-20
                 bg-[hsl(var(--background))]"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        {/* ---- Section Header ---- */}
        <div className="mx-auto mb-12 max-w-2xl text-center sm:mb-16 lg:mb-20">
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
            id="features-alt-heading"
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

        {/* ---- Feature Blocks ---- */}
        <div className="flex flex-col gap-16 sm:gap-20 lg:gap-28">
          {features.map((feature, index) => (
            <FeatureBlockItem
              key={feature.tag}
              feature={feature}
              index={index}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
```
