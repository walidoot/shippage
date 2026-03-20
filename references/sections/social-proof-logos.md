# Social Proof -- Logo Strip & Metrics Bar

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**BUILD TRUST** -- Establish credibility by showing recognizable brand logos and impressive
metrics. Visitors who see trusted logos are 2-3x more likely to convert. This section
answers the subconscious question: "Do serious companies use this?"

---

## Desktop Layout

```
┌──────────────────────────────────────────────────────┐
│          "Trusted by 2,000+ companies"               │
│                                                      │
│  [logo] [logo] [logo] [logo] [logo] [logo] ────►    │
│  ◄──── [logo] [logo] [logo] [logo] [logo] [logo]    │
│                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐  │
│  │  10,000+  │ │  99.9%   │ │   50M+   │ │  4.9★  │  │
│  │  Customers│ │  Uptime  │ │ Requests │ │ Rating │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘  │
└──────────────────────────────────────────────────────┘
```

- Logos scroll in a Marquee (two rows, opposite directions) or sit in a static centered row
- Metrics bar spans full width in a 4-column grid beneath the logos
- Section max-width: `max-w-6xl mx-auto`

---

## Mobile Layout (mobile-first)

```
┌──────────────────────┐
│ "Trusted by 2,000+"  │
│                      │
│  ◄── marquee ──►     │
│  ◄── marquee ──►     │
│                      │
│  ┌────────┐┌────────┐│
│  │ 10,000+││ 99.9%  ││
│  │ Custmrs││ Uptime ││
│  └────────┘└────────┘│
│  ┌────────┐┌────────┐│
│  │  50M+  ││  4.9★  ││
│  │Requests││ Rating ││
│  └────────┘└────────┘│
└──────────────────────┘
```

- Marquee works at all breakpoints (touch-scroll friendly)
- Metrics collapse to a 2x2 grid on mobile (`grid-cols-2`)
- Padding reduced: `py-12` mobile vs `py-20` desktop

---

## Copy Structure

| Element            | Content Pattern                        | Character Limit |
|--------------------|----------------------------------------|-----------------|
| Section label      | "Trusted by X+ companies"              | 40 chars        |
| Logo alt text      | Company name for accessibility          | --              |
| Metric value       | Big round number with suffix (+, %, M) | 8 chars         |
| Metric label       | Short descriptor                       | 20 chars        |

---

## Section-Specific Notes

- Logos default to `grayscale opacity-50`, hover to `grayscale-0 opacity-100`
- Marquee auto-scrolling pauses on hover (`pauseOnHover`)
- Marquee respects `prefers-reduced-motion: reduce` (pauses)
- NumberTicker counts up from 0 for metric values (Magic UI component)
- Supports 1 or 2 marquee rows (prop: `rows`)
- Logo images should be SVG for crisp scaling, < 5KB each

---

## Complete JSX Template

```tsx
"use client";

import React from "react";
import { motion } from "framer-motion";
import { Marquee } from "@/components/ui/marquee";
import { NumberTicker } from "@/components/ui/number-ticker";
import { Users, TrendingUp, Shield, Star } from "lucide-react";

// ------------------------------------------------------------------
// Types
// ------------------------------------------------------------------
interface Logo {
  name: string;
  src: string;
}

interface Metric {
  value: number;
  suffix?: string;
  label: string;
  icon: React.ElementType;
  decimals?: number;
}

// ------------------------------------------------------------------
// Default data (replace per-project)
// ------------------------------------------------------------------
const defaultLogos: Logo[] = [
  { name: "Acme Corp", src: "/logos/acme.svg" },
  { name: "Globex", src: "/logos/globex.svg" },
  { name: "Initech", src: "/logos/initech.svg" },
  { name: "Umbrella", src: "/logos/umbrella.svg" },
  { name: "Hooli", src: "/logos/hooli.svg" },
  { name: "Pied Piper", src: "/logos/pied-piper.svg" },
  { name: "Massive Dynamic", src: "/logos/massive.svg" },
  { name: "Wayne Enterprises", src: "/logos/wayne.svg" },
];

const defaultMetrics: Metric[] = [
  { value: 10000, suffix: "+", label: "Customers", icon: Users },
  { value: 99.9, suffix: "%", label: "Uptime", icon: Shield, decimals: 1 },
  { value: 50, suffix: "M+", label: "API Requests", icon: TrendingUp },
  { value: 4.9, suffix: "★", label: "Average Rating", icon: Star, decimals: 1 },
];

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
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } },
};

// ------------------------------------------------------------------
// Sub-components
// ------------------------------------------------------------------
function LogoImage({ logo }: { logo: Logo }) {
  return (
    <img
      src={logo.src}
      alt={logo.name}
      loading="lazy"
      className="h-8 w-auto object-contain grayscale opacity-50
                 hover:grayscale-0 hover:opacity-100 hover:scale-105
                 transition-all duration-300 ease-out mx-8 sm:mx-10"
    />
  );
}

function MetricCard({ metric }: { metric: Metric }) {
  return (
    <motion.div
      variants={staggerItem}
      className="flex flex-col items-center gap-1 rounded-xl p-4
                 hover:bg-[hsl(var(--muted))] hover:shadow-sm
                 transition-all duration-300"
    >
      <metric.icon
        className="h-5 w-5 text-[hsl(var(--muted-foreground))] mb-1"
        aria-hidden="true"
      />
      <span
        className="text-3xl sm:text-4xl font-bold tracking-tight
                   text-[hsl(var(--foreground))]"
        aria-label={`${metric.value}${metric.suffix ?? ""} ${metric.label}`}
      >
        <NumberTicker
          value={metric.value}
          decimalPlaces={metric.decimals ?? 0}
        />
        {metric.suffix && (
          <span className="text-[hsl(var(--muted-foreground))]">
            {metric.suffix}
          </span>
        )}
      </span>
      <span className="text-sm text-[hsl(var(--muted-foreground))]">
        {metric.label}
      </span>
    </motion.div>
  );
}

// ------------------------------------------------------------------
// Main Component
// ------------------------------------------------------------------
interface SocialProofLogosProps {
  heading?: string;
  logos?: Logo[];
  metrics?: Metric[];
  showMetrics?: boolean;
  /** Number of Marquee rows. 1 = single strip, 2 = dual opposing. */
  rows?: 1 | 2;
}

export default function SocialProofLogos({
  heading = "Trusted by 2,000+ innovative companies",
  logos = defaultLogos,
  metrics = defaultMetrics,
  showMetrics = true,
  rows = 2,
}: SocialProofLogosProps) {
  return (
    <section
      aria-labelledby="social-proof-heading"
      className="relative w-full overflow-hidden
                 py-12 sm:py-16 lg:py-20
                 bg-[hsl(var(--background))]"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        {/* ---- Heading ---- */}
        <motion.p
          id="social-proof-heading"
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.5 }}
          className="mb-8 text-center text-sm font-medium uppercase tracking-widest
                     text-[hsl(var(--muted-foreground))]"
        >
          {heading}
        </motion.p>

        {/* ---- Logo Marquee ---- */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6, delay: 0.1 }}
          aria-label="Logo carousel of trusted companies"
          className="space-y-4"
        >
          <Marquee pauseOnHover className="[--duration:30s]">
            {logos.map((logo) => (
              <LogoImage key={logo.name} logo={logo} />
            ))}
          </Marquee>

          {rows === 2 && (
            <Marquee pauseOnHover reverse className="[--duration:30s]">
              {logos.map((logo) => (
                <LogoImage key={`rev-${logo.name}`} logo={logo} />
              ))}
            </Marquee>
          )}
        </motion.div>

        {/* ---- Metrics Bar ---- */}
        {showMetrics && (
          <>
            <div
              className="my-10 border-t border-[hsl(var(--border))]"
              aria-hidden="true"
            />

            <motion.div
              variants={staggerContainer}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, margin: "-60px" }}
              className="grid grid-cols-2 gap-4 sm:gap-6 lg:grid-cols-4"
            >
              {metrics.map((metric) => (
                <MetricCard key={metric.label} metric={metric} />
              ))}
            </motion.div>
          </>
        )}
      </div>
    </section>
  );
}
```
