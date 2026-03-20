"use client";

import { motion, type Variants } from "framer-motion";
import { Terminal } from "lucide-react";

const containerVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" as const },
  },
};

interface FooterLinkGroup {
  heading: string;
  links: Array<{
    label: string;
    href: string;
    external?: boolean;
  }>;
}

const footerLinkGroups: FooterLinkGroup[] = [
  {
    heading: "Product",
    links: [
      { label: "Features", href: "#features" },
      { label: "How It Works", href: "#how-it-works" },
      { label: "FAQ", href: "#faq" },
    ],
  },
  {
    heading: "Resources",
    links: [
      {
        label: "GitHub",
        href: "https://github.com/imjahanzaib/shippage",
        external: true,
      },
      { label: "Documentation", href: "#" },
    ],
  },
  {
    heading: "Legal",
    links: [
      { label: "Privacy Policy", href: "/privacy" },
      { label: "Terms of Service", href: "/terms" },
      { label: "Cookie Policy", href: "/cookies" },
    ],
  },
];

export function CTAFooter() {
  return (
    <>
      {/* CTA Section */}
      <section
        data-cta-footer
        className="bg-gradient-to-b from-primary/10 to-background py-20 lg:py-28"
        aria-labelledby="cta-heading"
      >
        <motion.div
          className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.3 }}
        >
          <motion.h2
            id="cta-heading"
            className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl"
            variants={fadeUp}
          >
            Your next landing page is one sentence away.
          </motion.h2>

          <motion.p
            className="mt-4 text-base leading-relaxed text-muted-foreground sm:text-lg"
            variants={fadeUp}
          >
            Install Shippage. Describe your product. Ship a page that converts.
          </motion.p>

          <motion.div className="mt-10" variants={fadeUp}>
            <a
              href="https://github.com/imjahanzaib/shippage"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex h-12 items-center justify-center rounded-lg bg-primary px-8 py-3 text-sm font-semibold text-primary-foreground transition-all hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              Install Free on GitHub
            </a>
          </motion.div>

          <motion.p
            className="mt-5 text-sm text-muted-foreground"
            variants={fadeUp}
          >
            Free forever &middot; MIT Licensed &middot; 18 sections &middot;
            200+ design tokens
          </motion.p>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-card py-12" role="contentinfo">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          {/* Footer grid */}
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {/* Brand column */}
            <div className="col-span-2 md:col-span-1">
              <a
                href="#"
                className="inline-flex items-center gap-2 text-foreground transition-opacity hover:opacity-80"
                aria-label="Shippage home"
              >
                <Terminal
                  className="h-5 w-5 text-primary"
                  aria-hidden="true"
                />
                <span className="text-lg font-bold tracking-tight">
                  Shippage
                </span>
              </a>
              <p className="mt-3 max-w-xs text-sm leading-relaxed text-muted-foreground">
                Ship landing pages from your terminal. One prompt. Production-ready
                code you own.
              </p>
            </div>

            {/* Link columns */}
            {footerLinkGroups.map((group) => (
              <div key={group.heading}>
                <h3 className="text-sm font-semibold text-foreground">
                  {group.heading}
                </h3>
                <ul className="mt-3 flex flex-col gap-2.5" role="list">
                  {group.links.map((link) => (
                    <li key={link.label}>
                      <a
                        href={link.href}
                        {...(link.external
                          ? {
                              target: "_blank",
                              rel: "noopener noreferrer",
                            }
                          : {})}
                        className="text-sm text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background rounded-sm"
                      >
                        {link.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Bottom bar */}
          <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-border pt-8 sm:flex-row">
            <p className="text-sm text-muted-foreground">
              &copy; 2026 Shippage. MIT Licensed.
            </p>
            <button
              type="button"
              data-cookie-settings
              className="text-sm text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background rounded-sm"
            >
              Cookie Settings
            </button>
          </div>
        </div>
      </footer>
    </>
  );
}
