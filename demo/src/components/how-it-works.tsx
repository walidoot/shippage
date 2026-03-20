"use client";

import { motion, type Variants } from "framer-motion";
import { Terminal, MessageSquare, Rocket } from "lucide-react";
import type { ComponentType, SVGProps } from "react";

interface Step {
  number: number;
  icon: ComponentType<SVGProps<SVGSVGElement> & { className?: string }>;
  title: string;
  description: string;
  code: string;
}

const steps: Step[] = [
  {
    number: 1,
    icon: Terminal,
    title: "Install the skill",
    description:
      "Copy one line into your Claude Code skills directory. That\u2019s it.",
    code: "cp -r shippage ~/.claude/skills/",
  },
  {
    number: 2,
    icon: MessageSquare,
    title: "Describe your product",
    description:
      "Give it a name and a one-liner. Shippage infers design, copy, sections, and effects.",
    code: '"Build a landing page for Deploybot \u2014 one-click deploys for small teams"',
  },
  {
    number: 3,
    icon: Rocket,
    title: "Ship it",
    description:
      "Get a complete Next.js project. Run it. Deploy it. Start converting.",
    code: "npm install && npm run dev",
  },
];

const containerVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.15,
    },
  },
};

const stepVariants: Variants = {
  hidden: { opacity: 0, y: 32 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" as const },
  },
};

const headingVariants: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" as const },
  },
};

export function HowItWorks() {
  return (
    <section
      id="how-it-works"
      className="bg-background py-16 lg:py-24"
      aria-labelledby="how-it-works-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          className="mx-auto mb-12 max-w-2xl text-center lg:mb-16"
          variants={headingVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.3 }}
        >
          <h2
            id="how-it-works-heading"
            className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl"
          >
            Three steps. One deployed page.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground sm:text-lg">
            No config. No boilerplate. No context switching.
          </p>
        </motion.div>

        {/* Steps */}
        <motion.div
          className="grid grid-cols-1 gap-8 lg:grid-cols-3"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
          role="list"
          aria-label="Three steps to ship a landing page"
        >
          {steps.map((step, index) => {
            const Icon = step.icon;

            return (
              <motion.div
                key={step.number}
                className="relative flex flex-col items-center text-center"
                variants={stepVariants}
                role="listitem"
              >
                {/* Connecting dashed line between step circles (desktop only) */}
                {index < steps.length - 1 && (
                  <div
                    className="pointer-events-none absolute top-5 left-[calc(50%+28px)] hidden h-0 w-[calc(100%-56px)] border-t-2 border-dashed border-border lg:block"
                    aria-hidden="true"
                  />
                )}

                {/* Step number circle */}
                <div className="relative z-10 flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-bold text-primary-foreground">
                  {step.number}
                </div>

                {/* Icon */}
                <div className="mt-5 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                  <Icon
                    className="h-6 w-6 text-primary"
                    aria-hidden="true"
                  />
                </div>

                {/* Title */}
                <h3 className="mt-4 text-lg font-semibold text-foreground">
                  {step.title}
                </h3>

                {/* Description */}
                <p className="mt-2 max-w-xs text-sm leading-relaxed text-muted-foreground">
                  {step.description}
                </p>

                {/* Code block */}
                <div className="mt-4 w-full max-w-xs overflow-x-auto rounded-lg border border-border bg-card px-4 py-3">
                  <code className="whitespace-nowrap font-mono text-xs text-muted-foreground">
                    {step.code}
                  </code>
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
