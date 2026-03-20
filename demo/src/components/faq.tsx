"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence, type Variants } from "framer-motion";
import { ChevronDown } from "lucide-react";

interface FAQItem {
  question: string;
  answer: string;
}

const faqItems: FAQItem[] = [
  {
    question: "Is Shippage really free?",
    answer:
      "Yes. MIT licensed. No credits, no usage limits, no subscription. The skill generates code you own completely.",
  },
  {
    question: "What frameworks does it support?",
    answer:
      "React (Next.js, Vite, Remix), Astro, Vue/Nuxt, and Svelte/SvelteKit. The default output is React + Tailwind CSS + Framer Motion + shadcn/ui.",
  },
  {
    question: "Do I need social proof to use it?",
    answer:
      "No. Pre-launch mode handles the cold start problem with waitlist counters, founder story sections, architecture diagrams, and gradient placeholders instead of screenshots and testimonials.",
  },
  {
    question: "How is this different from v0?",
    answer:
      "v0 generates components. Shippage generates complete, conversion-optimized landing pages with professional copy, design tokens from 200+ real SaaS sites, legal pages, cookie consent, exit-intent popups, and analytics wiring. v0 has none of that.",
  },
  {
    question: "What if I already have a landing page?",
    answer:
      "Use audit mode. Shippage scores your page against conversion, design, performance, accessibility, and SEO checklists, then rewrites your weakest sections.",
  },
  {
    question: "Does it work with my existing project?",
    answer:
      "Yes. The output is standard React/Tailwind components. Drop them into any existing project or use the generated project as a standalone site.",
  },
];

const containerVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.08,
    },
  },
};

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 16 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: "easeOut" as const },
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

const answerVariants: Variants = {
  collapsed: {
    height: 0,
    opacity: 0,
    transition: { duration: 0.25, ease: "easeInOut" as const },
  },
  expanded: {
    height: "auto",
    opacity: 1,
    transition: { duration: 0.3, ease: "easeOut" as const },
  },
};

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggle = useCallback((index: number) => {
    setOpenIndex((prev) => (prev === index ? null : index));
  }, []);

  return (
    <section
      id="faq"
      className="bg-muted/30 py-16 lg:py-24"
      aria-labelledby="faq-heading"
    >
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          className="mb-12 text-center lg:mb-16"
          variants={headingVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.3 }}
        >
          <h2
            id="faq-heading"
            className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl"
          >
            Questions? Answered.
          </h2>
        </motion.div>

        {/* Accordion */}
        <motion.div
          className="flex flex-col gap-3"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
          role="list"
          aria-label="Frequently asked questions"
        >
          {faqItems.map((item, index) => {
            const isOpen = openIndex === index;

            return (
              <motion.div
                key={index}
                className="rounded-xl border border-border bg-card"
                variants={cardVariants}
                role="listitem"
              >
                <button
                  type="button"
                  className="flex w-full items-center justify-between px-6 py-5 text-left transition-colors hover:bg-muted/30 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background rounded-xl"
                  onClick={() => toggle(index)}
                  aria-expanded={isOpen}
                  aria-controls={`faq-answer-${index}`}
                  id={`faq-question-${index}`}
                >
                  <span className="pr-4 text-sm font-semibold text-foreground sm:text-base">
                    {item.question}
                  </span>
                  <motion.span
                    className="flex-shrink-0"
                    animate={{ rotate: isOpen ? 180 : 0 }}
                    transition={{ duration: 0.25, ease: "easeInOut" as const }}
                    aria-hidden="true"
                  >
                    <ChevronDown className="h-5 w-5 text-muted-foreground" />
                  </motion.span>
                </button>

                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      id={`faq-answer-${index}`}
                      role="region"
                      aria-labelledby={`faq-question-${index}`}
                      variants={answerVariants}
                      initial="collapsed"
                      animate="expanded"
                      exit="collapsed"
                      className="overflow-hidden"
                    >
                      <p className="px-6 pb-5 text-sm leading-relaxed text-muted-foreground">
                        {item.answer}
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
