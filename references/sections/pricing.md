# Pricing -- Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**REMOVE DOUBT** -- Present clear, transparent pricing that eliminates confusion.
Highlight the recommended tier, show annual savings, and surround the section with
trust signals. The visitor should never feel uncertain about what they get or what it costs.

---

## Desktop Layout

```
                    [ Monthly  |o|  Annual (Save 20%) ]

+---------------------+  +---------------------------+  +---------------------+
|  Starter            |  |  ★ MOST POPULAR ★          |  |  Enterprise         |
|  $19/mo             |  |  Pro                       |  |  Custom             |
|  "For individuals"  |  |  $49/mo                    |  |  "For large teams"  |
|                     |  |  "For growing teams"       |  |                     |
|  ✓ Feature 1        |  |  ✓ Feature 1               |  |  ✓ Everything in Pro|
|  ✓ Feature 2        |  |  ✓ Feature 2               |  |  ✓ Feature 1        |
|  ✗ Feature 3        |  |  ✓ Feature 3               |  |  ✓ Feature 2        |
|  ✗ Feature 4        |  |  ✓ Feature 4               |  |  ✓ Feature 3        |
|                     |  |                            |  |                     |
|  [Get Started]      |  |  [Start Free Trial]        |  |  [Contact Sales]    |
|   (outline btn)     |  |   (primary/accent btn)     |  |   (outline btn)     |
+---------------------+  +---------------------------+  +---------------------+

              [SOC 2]  [GDPR]  [99.9% Uptime]  [Cancel Anytime]
```

- 3-column grid: `grid grid-cols-3 gap-8`
- Popular tier: ring border (`ring-2 ring-primary`), "Most Popular" badge, slight scale or shadow
- Feature lists aligned vertically across all cards for easy comparison
- Trust badges centered below pricing cards

---

## Mobile Layout (mobile-first)

```
[ Monthly  |o|  Annual (Save 20%) ]   <-- sticky on scroll

+---------------------------+
|  ★ MOST POPULAR ★         |  <-- Popular tier shows FIRST
|  Pro -- $49/mo            |
|  ✓ Feature list...        |
|  [Start Free Trial]       |
+---------------------------+
+---------------------------+
|  Starter -- $19/mo        |
|  ✓ Feature list...        |
|  [Get Started]            |
+---------------------------+
+---------------------------+
|  Enterprise -- Custom     |
|  ✓ Feature list...        |
|  [Contact Sales]          |
+---------------------------+

[Trust badges row]
```

- Cards stack vertically in single column
- Popular tier renders FIRST (reorder via `order-first` or array sort)
- Monthly/annual toggle: `sticky top-[header-height] z-10` while scrolling through cards
- Each card full-width with comfortable padding

---

## Copy Structure

| Element             | Guidelines                                                     |
|---------------------|----------------------------------------------------------------|
| Section eyebrow     | "Pricing" or "Simple, Transparent Pricing"                     |
| Section heading     | "Choose the plan that fits your needs"                         |
| Section subheading  | "Start free. Upgrade when you're ready. Cancel anytime."       |
| Tier name           | 1 word: "Starter", "Pro", "Enterprise"                         |
| Tier price          | "$19/mo" or "$190/yr" -- toggle between the two                |
| Tier description    | One sentence positioning ("For individuals and small teams")   |
| Feature list        | 5-8 features per tier, Check for included, X or dash for not   |
| CTA text            | Action-oriented: "Get Started", "Start Free Trial", "Contact Sales" |
| Popular badge       | "Most Popular" or "Recommended"                                |
| Annual savings      | "Save 20%" badge near toggle or on annual prices               |

---

## Section-Specific Notes

- Popular tier highlighted with `ring-2 ring-primary` and a "Most Popular" badge
- Monthly/annual toggle uses shadcn Switch with `aria-live="polite"` on the price display
- Popular card renders first on mobile via `order-first` class
- Toggle becomes sticky on mobile: `sticky top-20 z-10`
- Trust badges row below pricing cards (SOC 2, GDPR, uptime)
- No background effects recommended -- pricing must be instantly scannable

---

## Complete JSX Template

```tsx
"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Check, X, Shield, Sparkles } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

// --- Types -------------------------------------------------------------------

interface PricingFeature {
  text: string;
  included: boolean;
}

interface PricingTier {
  name: string;
  monthlyPrice: number | null; // null = "Contact Sales"
  annualPrice: number | null;
  description: string;
  features: PricingFeature[];
  cta: string;
  popular?: boolean;
}

// --- Data --------------------------------------------------------------------

const tiers: PricingTier[] = [
  {
    name: "Starter",
    monthlyPrice: 19,
    annualPrice: 190,
    description: "For individuals and small projects getting started.",
    features: [
      { text: "Up to 3 projects", included: true },
      { text: "Basic analytics", included: true },
      { text: "Email support", included: true },
      { text: "API access", included: false },
      { text: "Custom integrations", included: false },
      { text: "Priority support", included: false },
    ],
    cta: "Get Started",
  },
  {
    name: "Pro",
    monthlyPrice: 49,
    annualPrice: 490,
    description: "For growing teams that need more power and flexibility.",
    features: [
      { text: "Unlimited projects", included: true },
      { text: "Advanced analytics", included: true },
      { text: "Priority email support", included: true },
      { text: "Full API access", included: true },
      { text: "Custom integrations", included: true },
      { text: "Dedicated account manager", included: false },
    ],
    cta: "Start Free Trial",
    popular: true,
  },
  {
    name: "Enterprise",
    monthlyPrice: null,
    annualPrice: null,
    description: "For large organizations with advanced security needs.",
    features: [
      { text: "Everything in Pro", included: true },
      { text: "SSO & SAML", included: true },
      { text: "Audit logs", included: true },
      { text: "Custom SLA", included: true },
      { text: "Dedicated account manager", included: true },
      { text: "On-premise deployment", included: true },
    ],
    cta: "Contact Sales",
  },
];

const trustBadges = [
  { label: "SOC 2 Type II", icon: Shield },
  { label: "GDPR Compliant", icon: Shield },
  { label: "99.9% Uptime SLA", icon: Sparkles },
];

// --- Animation Variants ------------------------------------------------------

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.12 },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 24 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

const badgeVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { duration: 0.4, delay: 0.4 },
  },
};

// --- Pricing Card ------------------------------------------------------------

function PricingCard({
  tier,
  isAnnual,
}: {
  tier: PricingTier;
  isAnnual: boolean;
}) {
  const price = isAnnual ? tier.annualPrice : tier.monthlyPrice;
  const period = isAnnual ? "/yr" : "/mo";

  return (
    <motion.div
      variants={cardVariants}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className={cn(
        "relative flex flex-col rounded-2xl border bg-[hsl(var(--card))] p-8 shadow-sm transition-shadow duration-200 hover:shadow-lg",
        tier.popular
          ? "border-[hsl(var(--primary))] ring-2 ring-[hsl(var(--primary))] shadow-md md:scale-105 order-first md:order-none"
          : "border-[hsl(var(--border))]"
      )}
    >
      {/* Popular Badge */}
      {tier.popular && (
        <Badge className="absolute -top-3 left-1/2 -translate-x-1/2 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] px-4 py-1 text-xs font-semibold">
          Most Popular
        </Badge>
      )}

      {/* Tier Header */}
      <div>
        <h3 className="text-lg font-semibold text-[hsl(var(--foreground))]">
          {tier.name}
        </h3>
        <p className="mt-1 text-sm text-[hsl(var(--muted-foreground))]">
          {tier.description}
        </p>
      </div>

      {/* Price */}
      <div className="mt-6" aria-live="polite">
        {price !== null ? (
          <div className="flex items-baseline gap-1">
            <span className="text-4xl font-bold tracking-tight text-[hsl(var(--foreground))]">
              ${price}
            </span>
            <span className="text-sm text-[hsl(var(--muted-foreground))]">
              {period}
            </span>
          </div>
        ) : (
          <div className="flex items-baseline">
            <span className="text-4xl font-bold tracking-tight text-[hsl(var(--foreground))]">
              Custom
            </span>
          </div>
        )}
        {isAnnual && price !== null && (
          <p className="mt-1 text-xs text-[hsl(var(--primary))]">
            Save ${(tier.monthlyPrice! * 12) - tier.annualPrice!} per year
          </p>
        )}
      </div>

      {/* Feature List */}
      <ul className="mt-8 flex-1 space-y-3" role="list">
        {tier.features.map((feature) => (
          <li key={feature.text} className="flex items-start gap-3 text-sm">
            {feature.included ? (
              <>
                <Check
                  className="mt-0.5 h-4 w-4 flex-shrink-0 text-[hsl(var(--primary))]"
                  aria-hidden="true"
                />
                <span className="text-[hsl(var(--foreground))]">
                  {feature.text}
                </span>
                <span className="sr-only">(Included)</span>
              </>
            ) : (
              <>
                <X
                  className="mt-0.5 h-4 w-4 flex-shrink-0 text-[hsl(var(--muted-foreground)/0.4)]"
                  aria-hidden="true"
                />
                <span className="text-[hsl(var(--muted-foreground))]">
                  {feature.text}
                </span>
                <span className="sr-only">(Not included)</span>
              </>
            )}
          </li>
        ))}
      </ul>

      {/* CTA */}
      <div className="mt-8">
        <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
          <Button
            className={cn(
              "w-full",
              tier.popular
                ? "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] hover:brightness-110"
                : "bg-transparent border border-[hsl(var(--border))] text-[hsl(var(--foreground))] hover:bg-[hsl(var(--accent))]"
            )}
            size="lg"
            aria-label={`${tier.cta} for ${tier.name} plan`}
          >
            {tier.cta}
          </Button>
        </motion.div>
      </div>
    </motion.div>
  );
}

// --- Trust Badges ------------------------------------------------------------

function TrustBadges() {
  return (
    <motion.div
      variants={badgeVariants}
      className="mt-12 flex flex-wrap items-center justify-center gap-4"
    >
      {trustBadges.map((badge) => {
        const Icon = badge.icon;
        return (
          <div
            key={badge.label}
            className="flex items-center gap-2 rounded-full border border-[hsl(var(--border))] bg-[hsl(var(--card))] px-4 py-2 text-xs font-medium text-[hsl(var(--muted-foreground))]"
          >
            <Icon className="h-4 w-4" aria-hidden="true" />
            {badge.label}
          </div>
        );
      })}
      <p className="w-full text-center text-xs text-[hsl(var(--muted-foreground))] mt-2">
        No credit card required. Cancel anytime.
      </p>
    </motion.div>
  );
}

// --- Main Section ------------------------------------------------------------

export default function Pricing() {
  const [isAnnual, setIsAnnual] = useState(false);

  return (
    <section
      className="relative py-20 md:py-28"
      aria-labelledby="pricing-heading"
    >
      <div className="mx-auto max-w-6xl px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mx-auto max-w-2xl text-center"
        >
          <p className="text-sm font-medium uppercase tracking-wider text-[hsl(var(--primary))]">
            Pricing
          </p>
          <h2
            id="pricing-heading"
            className="mt-3 text-3xl font-bold tracking-tight text-[hsl(var(--foreground))] md:text-4xl"
          >
            Simple, transparent pricing
          </h2>
          <p className="mt-4 text-base text-[hsl(var(--muted-foreground))]">
            Start free. Upgrade when you are ready. Cancel anytime.
          </p>
        </motion.div>

        {/* Billing Toggle */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="mt-10 flex items-center justify-center gap-3 sticky top-20 z-10 bg-[hsl(var(--background)/0.9)] backdrop-blur-sm py-3 md:static md:bg-transparent md:backdrop-blur-none"
        >
          <span
            className={cn(
              "text-sm font-medium transition-colors",
              !isAnnual
                ? "text-[hsl(var(--foreground))]"
                : "text-[hsl(var(--muted-foreground))]"
            )}
          >
            Monthly
          </span>
          <Switch
            checked={isAnnual}
            onCheckedChange={setIsAnnual}
            aria-label="Toggle annual billing"
          />
          <span
            className={cn(
              "text-sm font-medium transition-colors",
              isAnnual
                ? "text-[hsl(var(--foreground))]"
                : "text-[hsl(var(--muted-foreground))]"
            )}
          >
            Annual
          </span>
          {isAnnual && (
            <Badge
              variant="secondary"
              className="ml-1 bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 text-xs"
            >
              Save 20%
            </Badge>
          )}
        </motion.div>

        {/* Pricing Cards */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-80px" }}
          className="mt-10 grid grid-cols-1 gap-8 md:grid-cols-3 md:items-start"
        >
          {tiers.map((tier) => (
            <PricingCard key={tier.name} tier={tier} isAnnual={isAnnual} />
          ))}
        </motion.div>

        {/* Trust Badges */}
        <TrustBadges />
      </div>
    </section>
  );
}
```

### Usage Notes

- Replace the `tiers` array with real plan names, prices, and features.
- Annual prices should reflect the actual discount (typically 15-20% off monthly * 12).
- Enterprise tier uses `null` prices to display "Custom" with a "Contact Sales" CTA.
- On mobile, the popular card renders first via `order-first` class (resets to normal order on `md:`).
- The billing toggle becomes sticky on mobile (`sticky top-20`) so users always see it while scrolling cards.
- Add real trust badge images (SOC 2 seal, GDPR badge) by replacing the Shield icons with `<img>` elements.
- To add a "per seat" pricing model, extend the `PricingTier` type with a `perSeat: boolean` field and adjust the price display.
- For a freemium model, add a 4th tier with `monthlyPrice: 0` and fewer features at the beginning of the array.
