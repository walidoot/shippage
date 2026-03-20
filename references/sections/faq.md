# FAQ Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**REMOVE DOUBT** -- The visitor's remaining objections are answered before they reach the CTA. Every unanswered question is a reason to leave. The FAQ exists to intercept hesitation and convert it into confidence.

---

## Desktop Layout

- Section: `max-w-3xl mx-auto`, centered within a full-width container
- Section heading centered above the accordion
- Optional subheading below the heading
- Accordion items stack vertically with consistent spacing
- Generous vertical padding: `py-20 lg:py-28`

## Mobile Layout (mobile-first)

- Full width with `px-4 sm:px-6` horizontal padding
- Heading and subheading left-aligned or centered
- Accordion items span full width
- Tap targets meet 44px minimum for trigger areas
- Reduced vertical padding: `py-12 sm:py-16`

---

## Copy Structure

| Element | Content Rule |
|---|---|
| **Section Heading** | "Frequently Asked Questions" or a benefit-framed variant like "Got questions? We have answers." |
| **Subheading** (optional) | One sentence: "Everything you need to know about [Product]." |
| **Q1: Value** | "Is [Product] worth the money?" -- Answer with ROI framing and specific savings. |
| **Q2: Setup** | "How long does it take to set up?" -- Answer with exact timeframe and simplicity proof. |
| **Q3: Risk** | "What if I don't like it?" -- Answer with refund/cancellation policy, zero-risk framing. |
| **Q4: Security** | "Is my data safe?" -- Answer with certifications, encryption, and compliance details. |
| **Q5: Integration** | "Does it integrate with my existing tools?" -- Answer with integration count and key names. |
| **Q6: Product-specific** | Placeholder for the most common product-specific question. |
| **Q7: Product-specific** | Placeholder for the second most common product-specific question. |

---

## Section-Specific Notes

- shadcn Accordion handles `aria-expanded` and `aria-controls` automatically
- Accordion trigger: text shifts to `text-primary` on hover, chevron rotates
- Accordion items stagger with 50ms delay (faster than standard 120ms)
- No background effects -- section should be visually quiet

---

## Complete JSX Template

```tsx
"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

interface FAQItem {
  question: string;
  answer: string;
}

interface FAQSectionProps {
  heading?: string;
  subheading?: string;
  items?: FAQItem[];
}

// -------------------------------------------------------------------
// Default FAQ data -- addresses the 5 universal SaaS objections
// plus 2 product-specific placeholders
// -------------------------------------------------------------------

const defaultFAQItems: FAQItem[] = [
  {
    question: "Is it worth the money?",
    answer:
      "Teams using our platform save an average of 12 hours per week on manual tasks. Most customers see a positive ROI within the first 30 days. We also offer flexible plans so you only pay for what you need.",
  },
  {
    question: "How long does it take to set up?",
    answer:
      "Most teams are up and running in under 10 minutes. Our onboarding wizard walks you through every step, and our support team is available to help if you get stuck. No technical expertise required.",
  },
  {
    question: "What if I don't like it?",
    answer:
      "We offer a 14-day free trial with no credit card required. If you decide it's not for you, simply stop using it -- there's nothing to cancel. Paid plans include a 30-day money-back guarantee, no questions asked.",
  },
  {
    question: "Is my data safe?",
    answer:
      "Absolutely. We use AES-256 encryption at rest and TLS 1.3 in transit. Our infrastructure is SOC 2 Type II certified, and we conduct regular third-party security audits. Your data is never shared or sold.",
  },
  {
    question: "Does it integrate with my existing tools?",
    answer:
      "Yes. We integrate natively with over 50 tools including Slack, Jira, GitHub, Notion, and Google Workspace. We also offer a REST API and webhooks for custom integrations.",
  },
  {
    question: "Can I invite my whole team?",
    answer:
      "Yes. All plans support unlimited team members. You can manage roles and permissions from the admin dashboard to control who has access to what.",
  },
  {
    question: "Do you offer discounts for startups or nonprofits?",
    answer:
      "We do. Eligible startups and nonprofits receive up to 50% off any plan for the first year. Reach out to our sales team with your details and we'll get you set up.",
  },
];

// -------------------------------------------------------------------
// Animation variants
// -------------------------------------------------------------------

const sectionVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 16 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: "easeOut",
      delay: i * 0.05,
    },
  }),
};

// -------------------------------------------------------------------
// Component
// -------------------------------------------------------------------

export default function FAQSection({
  heading = "Frequently Asked Questions",
  subheading = "Everything you need to know about our product.",
  items = defaultFAQItems,
}: FAQSectionProps) {
  const sectionRef = useRef<HTMLElement>(null);
  const isInView = useInView(sectionRef, { once: true, margin: "-80px" });

  return (
    <section
      ref={sectionRef}
      id="faq"
      aria-labelledby="faq-heading"
      className="relative py-12 sm:py-16 lg:py-28 bg-background"
    >
      <div className="mx-auto max-w-3xl px-4 sm:px-6">
        {/* ---- Heading ---- */}
        <motion.div
          className="text-center mb-10 lg:mb-14"
          variants={sectionVariants}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
        >
          <h2
            id="faq-heading"
            className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-foreground"
          >
            {heading}
          </h2>
          {subheading && (
            <p className="mt-4 text-base sm:text-lg text-muted-foreground max-w-xl mx-auto">
              {subheading}
            </p>
          )}
        </motion.div>

        {/* ---- Accordion ---- */}
        <Accordion type="single" collapsible className="w-full">
          {items.map((item, index) => (
            <motion.div
              key={index}
              custom={index}
              variants={itemVariants}
              initial="hidden"
              animate={isInView ? "visible" : "hidden"}
            >
              <AccordionItem
                value={`item-${index}`}
                className="border-b border-border"
              >
                <AccordionTrigger
                  className="py-5 text-left text-base sm:text-lg font-medium
                             text-foreground
                             hover:text-primary
                             transition-colors duration-200"
                >
                  {item.question}
                </AccordionTrigger>
                <AccordionContent
                  className="pb-5 text-sm sm:text-base leading-relaxed
                             text-muted-foreground"
                >
                  {item.answer}
                </AccordionContent>
              </AccordionItem>
            </motion.div>
          ))}
        </Accordion>
      </div>
    </section>
  );
}
```
