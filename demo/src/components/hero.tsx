"use client";

import { motion } from "framer-motion";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.12, delayChildren: 0.1 },
  },
};

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.25, 0.4, 0.25, 1] as const },
  },
};

const terminalLines = [
  { type: "command" as const, text: "$ claude" },
  {
    type: "prompt" as const,
    text: "> Build a landing page for Deploybot — one-click deploys for small teams",
  },
  { type: "blank" as const, text: "" },
  {
    type: "check" as const,
    text: "Design system: dark-premium (matched to dev tools)",
  },
  {
    type: "check" as const,
    text: "Sections: hero, social proof, pain points, features, FAQ, CTA",
  },
  {
    type: "check" as const,
    text: "Copy: 12 headlines, 6 CTAs, 4 FAQ answers written",
  },
  {
    type: "check" as const,
    text: "Effects: Aurora background + Gradient text (2/3 budget)",
  },
  {
    type: "check" as const,
    text: "Legal: Privacy policy, terms, cookie policy generated",
  },
  { type: "blank" as const, text: "" },
  {
    type: "done" as const,
    text: "Done. Run npm install && npm run dev to preview.",
  },
];

export function Hero() {
  return (
    <section
      className="relative min-h-[calc(100vh-4rem)] bg-background"
      aria-label="Hero"
    >
      {/* Dot pattern overlay */}
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle,rgba(99,102,241,0.06)_1px,transparent_1px)] bg-[size:24px_24px]"
        aria-hidden="true"
      />

      <motion.div
        className="relative mx-auto flex max-w-4xl flex-col items-center px-4 pt-24 pb-16 text-center sm:px-6 sm:pt-32 lg:px-8 lg:pt-40"
        variants={container}
        initial="hidden"
        animate="show"
      >
        {/* Badge */}
        <motion.div variants={fadeUp}>
          <span className="inline-flex items-center rounded-full border border-border bg-muted/50 px-3.5 py-1 text-xs font-medium text-muted-foreground">
            Free &amp; Open Source
          </span>
        </motion.div>

        {/* Headline */}
        <motion.h1
          className="mt-6 text-5xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl"
          variants={fadeUp}
        >
          Ship a landing page
          <br className="hidden sm:block" />
          {" from your "}
          <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            terminal
          </span>
          .
        </motion.h1>

        {/* Subheadline */}
        <motion.p
          className="mt-6 max-w-2xl text-lg text-muted-foreground sm:text-xl"
          variants={fadeUp}
        >
          One prompt. Real conversion copy. 200+ design tokens. 18 sections. No
          AI slop. Production-ready code you own.
        </motion.p>

        {/* CTA buttons */}
        <motion.div
          className="mt-10 flex w-full flex-col items-center gap-3 sm:w-auto sm:flex-row sm:gap-4"
          variants={fadeUp}
        >
          <a
            href="https://github.com/imjahanzaib/shippage"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex h-12 w-full items-center justify-center rounded-lg bg-primary px-8 py-3 text-sm font-semibold text-primary-foreground transition-all hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background sm:w-auto"
          >
            Install Free
          </a>
          <a
            href="#how-it-works"
            className="inline-flex h-12 w-full items-center justify-center rounded-lg border border-border px-8 py-3 text-sm font-semibold text-foreground transition-colors hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background sm:w-auto"
          >
            See How It Works
          </a>
        </motion.div>

        {/* Trust hint */}
        <motion.p
          className="mt-5 text-sm text-muted-foreground"
          variants={fadeUp}
        >
          MIT Licensed &middot; Works with 6 frameworks &middot; Zero config
        </motion.p>

        {/* Terminal mockup */}
        <motion.div
          className="mt-14 w-full max-w-2xl overflow-x-auto"
          variants={fadeUp}
        >
          <div className="rounded-xl border border-border bg-card p-4">
            {/* Terminal chrome */}
            <div className="mb-3 flex items-center gap-1.5">
              <span
                className="h-3 w-3 rounded-full bg-[#ff5f57]"
                aria-hidden="true"
              />
              <span
                className="h-3 w-3 rounded-full bg-[#febc2e]"
                aria-hidden="true"
              />
              <span
                className="h-3 w-3 rounded-full bg-[#28c840]"
                aria-hidden="true"
              />
            </div>

            {/* Terminal content */}
            <pre
              className="whitespace-pre-wrap text-left font-mono text-sm leading-relaxed text-muted-foreground"
              aria-label="Terminal output showing Shippage generating a landing page"
            >
              {terminalLines.map((line, i) => {
                if (line.type === "blank") {
                  return <br key={i} />;
                }
                if (line.type === "command") {
                  return (
                    <div key={i}>
                      <span className="text-foreground">{line.text}</span>
                    </div>
                  );
                }
                if (line.type === "prompt") {
                  return (
                    <div key={i}>
                      <span className="text-muted-foreground">{line.text}</span>
                    </div>
                  );
                }
                if (line.type === "check") {
                  return (
                    <div key={i}>
                      <span className="text-emerald-400">{"✓ "}</span>
                      <span>{line.text}</span>
                    </div>
                  );
                }
                /* done */
                return (
                  <div key={i}>
                    <span className="text-foreground">{line.text}</span>
                  </div>
                );
              })}
            </pre>
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
}
