"use client";

import { useRef } from "react";
import {
  motion,
  useInView,
  type Variants,
} from "framer-motion";
import {
  FileText,
  Palette,
  LayoutGrid,
  Rocket,
  Shield,
  Check,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

/* -------------------------------------------------------------------------- */
/*  Visual sub-components for each feature block                              */
/* -------------------------------------------------------------------------- */

function BeforeAfterVisual() {
  return (
    <div className="rounded-xl border border-border bg-card p-5 sm:p-6 shadow-lg">
      <p className="mb-1 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
        Before
      </p>
      <p className="text-sm text-destructive line-through decoration-destructive/60 sm:text-base">
        &ldquo;Unlock Your Potential with Our Seamless Solution&rdquo;
      </p>
      <div className="my-4 h-px bg-border" />
      <p className="mb-1 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
        After
      </p>
      <p className="text-sm font-bold text-emerald-400 sm:text-base">
        &ldquo;Deploy in 30&nbsp;seconds. Not 30&nbsp;minutes.&rdquo;
      </p>
    </div>
  );
}

const swatches = [
  { color: "#0a0a0a", label: "Background" },
  { color: "#6366f1", label: "Primary" },
  { color: "#818cf8", label: "Accent" },
  { color: "#1a1a1a", label: "Muted" },
  { color: "#fafafa", label: "Foreground" },
] as const;

function SwatchVisual() {
  return (
    <div className="rounded-xl border border-border bg-card p-5 sm:p-6 shadow-lg">
      <p className="mb-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        dark-premium palette
      </p>
      <div className="flex items-center gap-2 sm:gap-3">
        {swatches.map((s) => (
          <div key={s.color} className="flex flex-col items-center gap-1.5">
            <div
              className="h-10 w-10 rounded-lg border border-border shadow-sm sm:h-12 sm:w-12"
              style={{ backgroundColor: s.color }}
              role="img"
              aria-label={`${s.label}: ${s.color}`}
            />
            <span className="font-mono text-[10px] text-muted-foreground">
              {s.color}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

const sectionItems = [
  "Hero with social proof",
  "Pain agitation",
  "Solution reveal",
  "Feature grid",
  "Testimonials",
  "Final CTA",
] as const;

function SectionListVisual() {
  return (
    <div className="rounded-xl border border-border bg-card p-5 sm:p-6 shadow-lg">
      <p className="mb-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Narrative arc sections
      </p>
      <ul className="space-y-2.5" role="list">
        {sectionItems.map((item, i) => (
          <li key={i} className="flex items-center gap-2.5 text-sm text-foreground/80">
            <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/20 text-primary">
              <Check className="h-3 w-3" aria-hidden="true" />
            </span>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function BetaBadgeVisual() {
  return (
    <div className="flex items-center justify-center rounded-xl border border-border bg-card p-8 shadow-lg sm:p-10">
      <div className="inline-flex flex-col items-center gap-2 rounded-xl border border-primary/30 bg-gradient-to-br from-primary/10 to-accent/10 px-6 py-5 text-center shadow-md">
        <span className="text-xs font-semibold uppercase tracking-widest text-accent">
          Private Beta
        </span>
        <span className="text-2xl font-extrabold tabular-nums text-foreground">
          47 spots left
        </span>
      </div>
    </div>
  );
}

function ComplianceBadgesVisual() {
  return (
    <div className="rounded-xl border border-border bg-card p-5 sm:p-6 shadow-lg">
      <p className="mb-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Compliance frameworks
      </p>
      <div className="flex flex-wrap items-center gap-3">
        {["GDPR", "CCPA", "PIPEDA"].map((badge) => (
          <span
            key={badge}
            className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-muted px-3 py-1.5 text-xs font-semibold text-foreground/80"
          >
            <Shield className="h-3.5 w-3.5 text-primary" aria-hidden="true" />
            {badge}
          </span>
        ))}
      </div>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*  Feature data                                                               */
/* -------------------------------------------------------------------------- */

interface FeatureData {
  icon: LucideIcon;
  title: string;
  description: string;
  visual: React.ReactNode;
}

const features: FeatureData[] = [
  {
    icon: FileText,
    title: "629 lines of conversion copy rules",
    description:
      "Not a prompt template. A structured copy system with headline formulas by awareness level, anti-AI word filtering, outcome-driven CTAs, and voice calibration. Every word earns its place.",
    visual: <BeforeAfterVisual />,
  },
  {
    icon: Palette,
    title: "200+ real design tokens",
    description:
      "Extracted from Stripe, Linear, Vercel, Notion, and 196 other production SaaS sites. Say \u2018dark premium\u2019 and get a curated palette that actually works \u2014 not a random AI guess.",
    visual: <SwatchVisual />,
  },
  {
    icon: LayoutGrid,
    title: "18 conversion-optimized sections",
    description:
      "Each section has exactly one job in a 7-step narrative arc: stop the scroll, build trust, agitate pain, show solution, prove it works, remove doubt, make the ask.",
    visual: <SectionListVisual />,
  },
  {
    icon: Rocket,
    title: "Pre-launch mode",
    description:
      "No screenshots? No testimonials? No problem. Waitlist counters, founder credibility sections, architecture diagrams, and gradient placeholders. Built for the 60% of users who ship before they have social proof.",
    visual: <BetaBadgeVisual />,
  },
  {
    icon: Shield,
    title: "Legal + compliance built in",
    description:
      "Privacy policy, terms of service, cookie policy, cookie consent banner \u2014 generated from your product details. GDPR, CCPA, PIPEDA compliant. Replaces $600/year in SaaS subscriptions.",
    visual: <ComplianceBadgesVisual />,
  },
];

/* -------------------------------------------------------------------------- */
/*  Animation variants                                                         */
/* -------------------------------------------------------------------------- */

const containerVariants: Variants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.15 },
  },
};

function slideVariants(direction: "left" | "right"): Variants {
  return {
    hidden: {
      opacity: 0,
      x: direction === "left" ? -48 : 48,
    },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.55, ease: [0.25, 0.46, 0.45, 0.94] },
    },
  };
}

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] },
  },
};

/* -------------------------------------------------------------------------- */
/*  Feature block component                                                    */
/* -------------------------------------------------------------------------- */

function FeatureBlock({
  feature,
  index,
}: {
  feature: FeatureData;
  index: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });
  const isEven = index % 2 === 1;
  const Icon = feature.icon;

  // Odd rows (0, 2, 4): text left, visual right => text slides from left, visual slides from right
  // Even rows (1, 3): visual left, text right => visual slides from left, text slides from right
  const textDirection = isEven ? "right" : "left";
  const visualDirection = isEven ? "left" : "right";

  return (
    <motion.div
      ref={ref}
      variants={containerVariants}
      initial="hidden"
      animate={isInView ? "visible" : "hidden"}
      className="grid items-center gap-8 lg:grid-cols-2 lg:gap-12"
    >
      {/* Text column */}
      <motion.div
        variants={slideVariants(textDirection)}
        className={isEven ? "order-1 lg:order-2" : "order-1"}
      >
        <div className="flex items-center gap-3 mb-4">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/15 text-primary">
            <Icon className="h-5 w-5" aria-hidden="true" />
          </span>
          <h3 className="text-xl font-bold text-foreground sm:text-2xl">
            {feature.title}
          </h3>
        </div>
        <p className="text-base leading-relaxed text-muted-foreground sm:text-lg">
          {feature.description}
        </p>
      </motion.div>

      {/* Visual column */}
      <motion.div
        variants={slideVariants(visualDirection)}
        className={isEven ? "order-2 lg:order-1" : "order-2"}
      >
        {feature.visual}
      </motion.div>
    </motion.div>
  );
}

/* -------------------------------------------------------------------------- */
/*  Main Features section                                                      */
/* -------------------------------------------------------------------------- */

export function Features() {
  const headingRef = useRef<HTMLDivElement>(null);
  const headingInView = useInView(headingRef, { once: true, margin: "-60px" });

  return (
    <section
      id="features"
      className="bg-muted/30 py-16 lg:py-24"
      aria-labelledby="features-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          ref={headingRef}
          variants={containerVariants}
          initial="hidden"
          animate={headingInView ? "visible" : "hidden"}
          className="mx-auto mb-14 max-w-2xl text-center lg:mb-20"
        >
          <motion.h2
            id="features-heading"
            variants={fadeUp}
            className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl"
          >
            Not another template. A conversion machine.
          </motion.h2>
          <motion.p
            variants={fadeUp}
            className="mt-4 text-base leading-relaxed text-muted-foreground sm:text-lg"
          >
            Every section, every headline, every CTA is built to do one job:
            make your visitor act.
          </motion.p>
        </motion.div>

        {/* Feature blocks */}
        <div className="space-y-16 lg:space-y-24">
          {features.map((feature, i) => (
            <FeatureBlock key={i} feature={feature} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
