import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { safeJsonLd } from "@/lib/utils";

const geist = Geist({ subsets: ["latin"], variable: "--font-sans" });
const geistMono = Geist_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: "Shippage — Ship a landing page from your terminal",
  description:
    "One sentence. Production-ready landing page. No AI slop. Free forever. A Claude Code skill that generates conversion-optimized SaaS pages with real copy, real design tokens, and zero templates.",
  metadataBase: new URL("https://shippage.dev"),
  openGraph: {
    title: "Shippage — Ship a landing page from your terminal",
    description:
      "One sentence. Production-ready landing page. No AI slop. Free forever.",
    url: "https://shippage.dev",
    siteName: "Shippage",
    type: "website",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Shippage — Ship a landing page from your terminal",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Shippage — Ship a landing page from your terminal",
    description:
      "One sentence. Production-ready landing page. No AI slop. Free forever.",
    images: ["/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const orgSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Shippage",
    url: "https://shippage.dev",
    description:
      "A Claude Code skill that generates conversion-optimized SaaS landing pages from a single prompt.",
    sameAs: ["https://github.com/imjahanzaib/shippage"],
  };

  const softwareSchema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "Shippage",
    applicationCategory: "DeveloperApplication",
    operatingSystem: "Web",
    url: "https://shippage.dev",
    description:
      "Ship a landing page from your terminal. One sentence in, production-ready page out.",
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "USD",
    },
  };

  return (
    <html lang="en" className={`${geist.variable} ${geistMono.variable} dark`}>
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: safeJsonLd(orgSchema) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: safeJsonLd(softwareSchema) }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
