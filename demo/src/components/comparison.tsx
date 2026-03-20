"use client";

import { motion, type Variants } from "framer-motion";

interface ComparisonRow {
  feature: string;
  shippage: string;
  v0: string;
  shipfast: string;
}

const rows: ComparisonRow[] = [
  {
    feature: "Writes conversion copy",
    shippage: "\u2713 (629-line system)",
    v0: "\u2717",
    shipfast: "\u2717",
  },
  {
    feature: "Pre-launch mode",
    shippage: "\u2713",
    v0: "\u2717",
    shipfast: "\u2717",
  },
  {
    feature: "Design tokens",
    shippage: "200+ real sites",
    v0: "Same every time",
    shipfast: "1 template",
  },
  {
    feature: "Exit-intent popups",
    shippage: "\u2713 Built-in",
    v0: "\u2717",
    shipfast: "\u2717",
  },
  {
    feature: "Legal pages",
    shippage: "\u2713 GDPR/CCPA",
    v0: "\u2717",
    shipfast: "\u2717",
  },
  {
    feature: "Cookie consent",
    shippage: "\u2713 Full CMP",
    v0: "\u2717",
    shipfast: "\u2717",
  },
  {
    feature: "SEO automation",
    shippage: "JSON-LD + OG + sitemap",
    v0: "Basic meta",
    shipfast: "Basic meta",
  },
  {
    feature: "Frameworks",
    shippage: "6",
    v0: "Next.js only",
    shipfast: "Next.js only",
  },
  {
    feature: "Contact forms",
    shippage: "\u2713 Built-in",
    v0: "\u2717",
    shipfast: "\u2717",
  },
  {
    feature: "Price",
    shippage: "Free",
    v0: "$20/mo",
    shipfast: "$199 one-time",
  },
  {
    feature: "You own the code",
    shippage: "\u2713",
    v0: "\u2713",
    shipfast: "\u2713",
  },
];

const sectionVariants: Variants = {
  hidden: { opacity: 0, y: 32 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.25, 0.4, 0.25, 1] },
  },
};

function isCheck(value: string): boolean {
  return value.startsWith("\u2713");
}

function isX(value: string): boolean {
  return value === "\u2717";
}

function CellValue({ value, isShippage }: { value: string; isShippage?: boolean }) {
  if (isX(value)) {
    return <span className="text-red-400" aria-label="Not available">{value}</span>;
  }
  if (isCheck(value)) {
    return (
      <span className={isShippage ? "text-green-500 font-medium" : "text-green-500"} aria-label="Available">
        {value}
      </span>
    );
  }
  return (
    <span className={isShippage ? "font-medium text-foreground" : "text-muted-foreground"}>
      {value}
    </span>
  );
}

export function Comparison() {
  return (
    <section
      id="comparison"
      className="bg-background py-16 lg:py-24"
      aria-labelledby="comparison-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="mx-auto mb-12 max-w-2xl text-center lg:mb-16">
          <h2
            id="comparison-heading"
            className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl"
          >
            How Shippage stacks up.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground sm:text-lg">
            Feature-by-feature against the tools you&rsquo;re considering.
          </p>
        </div>

        {/* Desktop table */}
        <motion.div
          className="hidden md:block"
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.15 }}
        >
          <div className="overflow-hidden rounded-xl border border-border bg-card" role="table" aria-label="Feature comparison between Shippage, v0.dev, and ShipFast">
            {/* Table header */}
            <div className="grid grid-cols-4 border-b border-border" role="row">
              <div className="px-6 py-4 text-sm font-semibold text-muted-foreground" role="columnheader">
                Feature
              </div>
              <div
                className="border-x border-primary/30 bg-primary/5 px-6 py-4 text-sm font-semibold text-primary"
                role="columnheader"
              >
                Shippage
              </div>
              <div className="px-6 py-4 text-sm font-semibold text-muted-foreground" role="columnheader">
                v0.dev
              </div>
              <div className="px-6 py-4 text-sm font-semibold text-muted-foreground" role="columnheader">
                ShipFast
              </div>
            </div>

            {/* Table rows */}
            {rows.map((row, i) => (
              <div
                key={row.feature}
                className={`grid grid-cols-4 ${i < rows.length - 1 ? "border-b border-border" : ""}`}
                role="row"
              >
                <div className="px-6 py-4 text-sm font-medium text-foreground" role="rowheader">
                  {row.feature}
                </div>
                <div
                  className="border-x border-primary/30 bg-primary/5 px-6 py-4 text-sm"
                  role="cell"
                >
                  <CellValue value={row.shippage} isShippage />
                </div>
                <div className="px-6 py-4 text-sm" role="cell">
                  <CellValue value={row.v0} />
                </div>
                <div className="px-6 py-4 text-sm" role="cell">
                  <CellValue value={row.shipfast} />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Mobile cards */}
        <motion.div
          className="flex flex-col gap-4 md:hidden"
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
          role="list"
          aria-label="Feature comparison cards"
        >
          {rows.map((row) => (
            <div
              key={row.feature}
              className="rounded-xl border border-border bg-card p-4"
              role="listitem"
            >
              <h3 className="mb-3 text-sm font-semibold text-foreground">
                {row.feature}
              </h3>
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between rounded-lg border border-primary/30 bg-primary/5 px-3 py-2">
                  <span className="text-xs font-medium text-primary">Shippage</span>
                  <span className="text-sm">
                    <CellValue value={row.shippage} isShippage />
                  </span>
                </div>
                <div className="flex items-center justify-between rounded-lg bg-muted/50 px-3 py-2">
                  <span className="text-xs font-medium text-muted-foreground">v0.dev</span>
                  <span className="text-sm">
                    <CellValue value={row.v0} />
                  </span>
                </div>
                <div className="flex items-center justify-between rounded-lg bg-muted/50 px-3 py-2">
                  <span className="text-xs font-medium text-muted-foreground">ShipFast</span>
                  <span className="text-sm">
                    <CellValue value={row.shipfast} />
                  </span>
                </div>
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
