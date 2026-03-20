"use client";

import { motion, type Variants } from "framer-motion";
import { Palette, PenLine, ArrowLeftRight, CreditCard } from "lucide-react";
import type { ComponentType, SVGProps } from "react";

interface PainPointCard {
  icon: ComponentType<SVGProps<SVGSVGElement> & { className?: string }>;
  title: string;
  description: string;
}

const painPoints: PainPointCard[] = [
  {
    icon: Palette,
    title: "Same design, every time",
    description:
      "Inter font. Purple gradient. Cards in a grid. Your visitors have seen this page a hundred times. It screams \u2018I let AI do this\u2019 and kills trust on contact.",
  },
  {
    icon: PenLine,
    title: "Copy that says nothing",
    description:
      "Leverage seamless solutions to unlock your potential. That\u2019s not copy. That\u2019s AI word salad. Your headline needs to speak to a real problem in your customer\u2019s language.",
  },
  {
    icon: ArrowLeftRight,
    title: "Context switching kills flow",
    description:
      "You\u2019re building in your terminal. Then you switch to Framer. Or v0. Or Webflow. Every tab switch costs you 20 minutes of focus. The page still doesn\u2019t convert.",
  },
  {
    icon: CreditCard,
    title: "Death by subscription",
    description:
      "v0 is $20/mo. OptinMonster is $82/mo. Termly is $20/mo. Cookie consent, legal pages, popups, analytics \u2014 it adds up to $600/year for a single landing page.",
  },
];

const containerVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.12,
    },
  },
};

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" as const },
  },
};

export function PainPoints() {
  return (
    <section
      id="pain-points"
      className="bg-background py-16 lg:py-24"
      aria-labelledby="pain-points-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="mx-auto mb-12 max-w-2xl text-center lg:mb-16">
          <h2
            id="pain-points-heading"
            className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl"
          >
            You&rsquo;ve seen this page before.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground sm:text-lg">
            Every AI-generated landing page looks the same. Here&rsquo;s why
            yours doesn&rsquo;t convert.
          </p>
        </div>

        {/* Pain point cards */}
        <motion.div
          className="grid grid-cols-1 gap-6 lg:grid-cols-2"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
          role="list"
          aria-label="Common landing page pain points"
        >
          {painPoints.map((point) => {
            const Icon = point.icon;

            return (
              <motion.div
                key={point.title}
                className="rounded-xl border border-border bg-card p-6"
                variants={cardVariants}
                role="listitem"
              >
                <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                  <Icon
                    className="h-5 w-5 text-primary"
                    aria-hidden="true"
                  />
                </div>
                <h3 className="text-lg font-semibold text-foreground">
                  {point.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {point.description}
                </p>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
