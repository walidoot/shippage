# Comparison Table Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**DIFFERENTIATE** -- The visitor is comparing options. This section intercepts the comparison impulse and frames it on YOUR terms. Instead of letting them open 5 tabs, give them the comparison right here -- with your product winning on the dimensions that matter most to your audience.

---

## Desktop Layout

- Section: `max-w-5xl mx-auto`, centered within a full-width container
- Section heading + subheading centered above the table
- Comparison table: sticky left column (your product), scrollable competitor columns
- Checkmark grid with clear visual hierarchy (your column highlighted)
- Generous vertical padding: `py-20 lg:py-28`

```
[Heading: "Why teams choose [Product] over [alternatives]"]
[Subheading: one sentence]

| Feature          | YourProduct  | Competitor A | Competitor B |
|------------------|:----:|:----:|:----:|
| Feature 1        |  check  |  check  |  x  |
| Feature 2        |  check  |  x  |  x  |
| Feature 3        |  check  |  check  |  check  |
| Pricing          | $X/mo | $Y/mo | $Z/mo |
| Free tier        |  check  |  x  |  check  |

[CTA button below table]
```

## Mobile Layout (mobile-first)

- Full width with `px-4 sm:px-6` horizontal padding
- Table scrolls horizontally with `overflow-x-auto`
- Your product column stays sticky on the left (`sticky left-0 z-10`)
- Feature names truncate with `truncate` class on narrow screens
- Reduced vertical padding: `py-12 sm:py-16`
- Alternative: stack as feature cards with checkmarks on mobile (no table)

---

## Copy Structure

| Element | Content Rule |
|---|---|
| **Section Heading** | "Why [audience] choose [Product]" or "See how [Product] compares" |
| **Subheading** | One sentence positioning the comparison as helpful, not aggressive |
| **Your Product Column Header** | Product name with a subtle highlight badge or "Recommended" pill |
| **Competitor Columns** | Use real competitor names if possible, or category labels ("Traditional tools", "DIY approach") |
| **Feature Rows** | 5-8 rows max. Lead with YOUR strongest differentiators. End with pricing. |
| **Check/X Icons** | Green checkmark for included, muted X or dash for missing |
| **Bottom CTA** | "Start Free Trial" or "See Why Teams Switch" |
| **Trust Hint** | Below CTA: "No credit card required" or "Switch in under 10 minutes" |

**Copy Rules:**
- Never trash competitors directly -- let the checkmarks speak
- Frame missing competitor features as gaps, not insults
- Include 1-2 rows where competitors DO have checkmarks (credibility, honesty)
- End with a row that is YOUR unique advantage (competitors can't match)

---

## Section-Specific Notes

- Uses semantic `<table>`, `<thead>`, `<tbody>`, `<th scope="col">`, `<td>`
- Your product column highlighted: `bg-primary/5 border-x border-primary/20`
- Check icons: `aria-label="Included"`, X icons: `aria-label="Not included"`
- Table scrolls horizontally on mobile with `overflow-x-auto`
- Table appears as a unit (no row stagger) -- fades up with heading
- No background effects -- the comparison data does the selling

---

## Complete JSX Template

```tsx
"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import { Check, Minus } from "lucide-react";
import { Button } from "@/components/ui/button";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

interface ComparisonFeature {
  feature: string;
  values: Record<string, boolean | string>;
}

interface ComparisonTableProps {
  heading?: string;
  subheading?: string;
  productName?: string;
  competitors?: string[];
  features?: ComparisonFeature[];
  ctaText?: string;
  ctaHref?: string;
  trustHint?: string;
}

// -------------------------------------------------------------------
// Default data
// -------------------------------------------------------------------

const defaultCompetitors = ["Competitor A", "Competitor B"];

const defaultFeatures: ComparisonFeature[] = [
  {
    feature: "Automated workflows",
    values: { self: true, "Competitor A": true, "Competitor B": false },
  },
  {
    feature: "Real-time collaboration",
    values: { self: true, "Competitor A": false, "Competitor B": false },
  },
  {
    feature: "Custom integrations",
    values: { self: true, "Competitor A": true, "Competitor B": true },
  },
  {
    feature: "Priority support",
    values: { self: true, "Competitor A": false, "Competitor B": true },
  },
  {
    feature: "SOC 2 compliance",
    values: { self: true, "Competitor A": true, "Competitor B": false },
  },
  {
    feature: "Free tier",
    values: { self: "Unlimited", "Competitor A": "14 days", "Competitor B": false },
  },
  {
    feature: "Starting price",
    values: { self: "$29/mo", "Competitor A": "$49/mo", "Competitor B": "$79/mo" },
  },
];

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

// -------------------------------------------------------------------
// Helper: render cell value
// -------------------------------------------------------------------

function CellValue({ value }: { value: boolean | string }) {
  if (value === true) {
    return (
      <span className="inline-flex items-center justify-center">
        <Check className="h-5 w-5 text-primary" aria-label="Included" />
      </span>
    );
  }
  if (value === false) {
    return (
      <span className="inline-flex items-center justify-center">
        <Minus
          className="h-5 w-5 text-muted-foreground/40"
          aria-label="Not included"
        />
      </span>
    );
  }
  return (
    <span className="text-sm font-medium text-foreground">{value}</span>
  );
}

// -------------------------------------------------------------------
// Component
// -------------------------------------------------------------------

export default function ComparisonTable({
  heading = "See how we compare",
  subheading = "An honest look at what you get with each option.",
  productName = "YourProduct",
  competitors = defaultCompetitors,
  features = defaultFeatures,
  ctaText = "Start Free Trial",
  ctaHref = "#cta",
  trustHint = "No credit card required",
}: ComparisonTableProps) {
  const sectionRef = useRef<HTMLElement>(null);
  const isInView = useInView(sectionRef, { once: true, margin: "-80px" });

  const allColumns = [productName, ...competitors];

  return (
    <section
      ref={sectionRef}
      id="comparison"
      aria-labelledby="comparison-heading"
      className="relative py-12 sm:py-16 lg:py-28 bg-background"
    >
      <div className="mx-auto max-w-5xl px-4 sm:px-6">
        {/* ---- Heading ---- */}
        <motion.div
          className="text-center mb-10 lg:mb-14"
          custom={0}
          variants={fadeUp}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
        >
          <h2
            id="comparison-heading"
            className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-foreground"
          >
            {heading}
          </h2>
          {subheading && (
            <p className="mt-4 text-base sm:text-lg text-muted-foreground max-w-2xl mx-auto">
              {subheading}
            </p>
          )}
        </motion.div>

        {/* ---- Table ---- */}
        <motion.div
          custom={0.2}
          variants={fadeUp}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
          className="overflow-x-auto rounded-xl border border-border"
        >
          <table className="w-full text-left">
            <thead>
              <tr className="bg-muted">
                <th
                  scope="col"
                  className="px-4 py-3 text-sm font-semibold text-muted-foreground uppercase tracking-wide"
                >
                  Feature
                </th>
                {allColumns.map((col, i) => (
                  <th
                    key={col}
                    scope="col"
                    className={`px-4 py-3 text-center text-sm font-semibold uppercase tracking-wide ${
                      i === 0
                        ? "text-primary bg-primary/5 border-x border-primary/20"
                        : "text-muted-foreground"
                    }`}
                    {...(i === 0 ? { "aria-current": "true" as const } : {})}
                  >
                    {col}
                    {i === 0 && (
                      <span className="ml-2 inline-block rounded-full bg-primary/10 px-2 py-0.5 text-[10px] font-bold text-primary uppercase">
                        You
                      </span>
                    )}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {features.map((row, rowIndex) => (
                <tr
                  key={row.feature}
                  className={`border-b border-border hover:bg-muted/50 transition-colors duration-150 ${
                    rowIndex % 2 === 1 ? "bg-muted/20" : ""
                  }`}
                >
                  <td
                    scope="row"
                    className="px-4 py-3.5 text-sm font-medium text-foreground"
                  >
                    {row.feature}
                  </td>
                  {allColumns.map((col, colIndex) => {
                    const key = colIndex === 0 ? "self" : col;
                    const value = row.values[key] ?? false;
                    return (
                      <td
                        key={col}
                        className={`px-4 py-3.5 text-center ${
                          colIndex === 0
                            ? "bg-primary/5 border-x border-primary/20"
                            : ""
                        }`}
                      >
                        <CellValue value={value} />
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>

        {/* ---- CTA ---- */}
        <motion.div
          custom={0.4}
          variants={fadeUp}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
          className="mt-10 text-center"
        >
          <Button asChild size="lg" className="px-8">
            <motion.a
              href={ctaHref}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              transition={{ duration: 0.15, ease: "easeInOut" }}
            >
              {ctaText}
            </motion.a>
          </Button>
          {trustHint && (
            <p className="mt-3 text-sm text-muted-foreground">{trustHint}</p>
          )}
        </motion.div>
      </div>
    </section>
  );
}
```
