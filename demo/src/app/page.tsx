import { Navbar } from "@/components/navbar";
import { Hero } from "@/components/hero";
import { SocialProof } from "@/components/social-proof";
import { PainPoints } from "@/components/pain-points";
import { Features } from "@/components/features";
import { HowItWorks } from "@/components/how-it-works";
import { Comparison } from "@/components/comparison";
import { FAQ } from "@/components/faq";
import { ContactForm } from "@/components/contact-form";
import { CTAFooter } from "@/components/cta-footer";
import { StickyCTA } from "@/components/sticky-cta";
import { CookieConsent } from "@/components/cookie-consent";
import { safeJsonLd } from "@/lib/utils";

const faqItems = [
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

export default function HomePage() {
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqItems.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: item.answer,
      },
    })),
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: safeJsonLd(faqSchema) }}
      />
      <Navbar />
      <main>
        <Hero />
        <SocialProof />
        <PainPoints />
        <Features />
        <HowItWorks />
        <Comparison />
        <FAQ />
        <ContactForm />
      </main>
      <CTAFooter />
      <StickyCTA />
      <CookieConsent />
    </>
  );
}
