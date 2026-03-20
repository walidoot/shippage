# Testimonials -- Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

---

## Conversion Job

**PROVE IT WORKS** -- Social proof from real customers reduces purchase anxiety.
A featured testimonial anchors credibility while supporting cards add volume.
Place after features and before pricing for maximum conversion impact.

---

## Desktop Layout

```
+-----------------------------------------------------------------------+
|                    Featured Testimonial (full-width)                    |
|  [Large Photo]  "Long 3-4 sentence quote..."                          |
|                  -- Full Name, Job Title, Company  [Company Logo]      |
|                  ★★★★★                                                 |
+-----------------------------------------------------------------------+

+---------------------+  +---------------------+  +---------------------+
|  Smaller Card 1     |  |  Smaller Card 2     |  |  Smaller Card 3     |
|  [Photo] Name       |  |  [Photo] Name       |  |  [Photo] Name       |
|  Title, Company     |  |  Title, Company     |  |  Title, Company     |
|  "Short quote..."   |  |  "Short quote..."   |  |  "Short quote..."   |
+---------------------+  +---------------------+  +---------------------+
```

- Featured card: full-width, larger padding, larger photo (`w-16 h-16`), prominent quote
- Smaller cards: `grid grid-cols-3 gap-6` below the featured card
- Each smaller card: consistent height with `flex flex-col` and `mt-auto` footer

---

## Mobile Layout (mobile-first)

```
+---------------------------+
| Featured Testimonial      |
| (full-width, stacked)     |
+---------------------------+
+---------------------------+
| Smaller Card 1            |
+---------------------------+
+---------------------------+
| Smaller Card 2            |
+---------------------------+
+---------------------------+
| Smaller Card 3            |
+---------------------------+
```

- All cards stack vertically in a single column
- Featured card remains visually distinct (larger quote text, bigger photo)
- Alternative: swipeable horizontal carousel using `overflow-x-auto snap-x` for smaller cards
- Carousel variant uses Aceternity `InfiniteMovingCards` for hands-free scrolling

---

## Copy Structure

| Element              | Guidelines                                                   |
|----------------------|--------------------------------------------------------------|
| Section eyebrow     | "What Our Customers Say" (uppercase, tracking-wider)         |
| Section heading      | "Loved by teams worldwide" or benefit-driven variant         |
| Section subheading   | "See how companies like yours achieved results." (optional)  |
| Featured quote       | 3-4 sentences, specific results or emotions                  |
| Smaller quotes       | 1-2 sentences, punchy and specific                           |
| Attribution          | Full name, job title, company name (all required)            |
| Star rating          | 5 stars on featured, optional on smaller cards               |

---

## Section-Specific Notes

- **Layout variants:** `"grid"` (featured + small cards) and `"carousel"` (infinite scroll).
- **Featured card semantics:** use `<blockquote>` + `<figure>` + `<figcaption>` pattern.
- **Star ratings:** amber-400 fill, `aria-label="Rated X out of 5 stars"`.
- **Carousel motion:** respects `prefers-reduced-motion` (pauses animation).
- **Avatar images:** `loading="lazy"`, explicit `width`/`height` to prevent CLS.
- **Testimonial counts:** minimum 4 for carousel, 3-6 for grid.

---

## Complete JSX Template

```tsx
"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Star, Quote } from "lucide-react";
import { cn } from "@/lib/utils";

// --- Types -------------------------------------------------------------------

interface Testimonial {
  name: string;
  title: string;
  company: string;
  avatar: string;
  companyLogo?: string;
  quote: string;
  rating?: number;
  featured?: boolean;
}

// --- Data --------------------------------------------------------------------

const testimonials: Testimonial[] = [
  {
    name: "Sarah Chen",
    title: "CTO",
    company: "Acme Inc",
    avatar: "/avatars/sarah.jpg",
    companyLogo: "/logos/acme.svg",
    quote:
      "This platform transformed how our engineering team ships features. We cut our deployment cycle from two weeks to two days. The onboarding was seamless and the support team is world-class.",
    rating: 5,
    featured: true,
  },
  {
    name: "Marcus Rivera",
    title: "VP Engineering",
    company: "TechCorp",
    avatar: "/avatars/marcus.jpg",
    companyLogo: "/logos/techcorp.svg",
    quote:
      "We evaluated 12 solutions before choosing this one. Best developer experience we have ever seen.",
    rating: 5,
  },
  {
    name: "Priya Patel",
    title: "Head of Product",
    company: "ScaleUp",
    avatar: "/avatars/priya.jpg",
    companyLogo: "/logos/scaleup.svg",
    quote:
      "Our team adopted it in a single sprint. The ROI was visible within the first month.",
    rating: 5,
  },
  {
    name: "James O'Connor",
    title: "Lead Developer",
    company: "DevHouse",
    avatar: "/avatars/james.jpg",
    companyLogo: "/logos/devhouse.svg",
    quote:
      "Finally, a tool that understands how developers actually work. Clean API, great docs, zero friction.",
    rating: 5,
  },
];

// --- Animation Variants ------------------------------------------------------

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.15 },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

const featuredVariants = {
  hidden: { opacity: 0, scale: 0.98 },
  show: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.6, ease: "easeOut" },
  },
};

// --- Star Rating -------------------------------------------------------------

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="flex gap-0.5" aria-label={`Rated ${rating} out of 5 stars`}>
      {Array.from({ length: 5 }).map((_, i) => (
        <Star
          key={i}
          className={cn(
            "h-4 w-4",
            i < rating
              ? "fill-amber-400 text-amber-400"
              : "fill-[hsl(var(--muted))] text-[hsl(var(--muted))]"
          )}
          aria-hidden="true"
        />
      ))}
    </div>
  );
}

// --- Featured Testimonial Card -----------------------------------------------

function FeaturedCard({ testimonial }: { testimonial: Testimonial }) {
  return (
    <motion.figure
      variants={featuredVariants}
      className="relative overflow-hidden rounded-2xl border border-[hsl(var(--border))] bg-[hsl(var(--card))] p-8 md:p-10 shadow-sm"
    >
      {/* Decorative quote icon */}
      <Quote
        className="absolute top-6 right-6 h-12 w-12 text-[hsl(var(--primary)/0.1)]"
        aria-hidden="true"
      />

      {testimonial.rating && <StarRating rating={testimonial.rating} />}

      <blockquote className="mt-4 text-lg md:text-xl leading-relaxed text-[hsl(var(--foreground))]">
        &ldquo;{testimonial.quote}&rdquo;
      </blockquote>

      <figcaption className="mt-6 flex items-center gap-4 border-t border-[hsl(var(--border))] pt-6">
        <img
          src={testimonial.avatar}
          alt={`Photo of ${testimonial.name}`}
          className="h-14 w-14 rounded-full object-cover ring-2 ring-[hsl(var(--primary)/0.2)]"
          loading="eager"
          width={56}
          height={56}
        />
        <div className="flex-1 min-w-0">
          <p className="text-base font-semibold text-[hsl(var(--foreground))]">
            {testimonial.name}
          </p>
          <p className="text-sm text-[hsl(var(--muted-foreground))]">
            {testimonial.title}, {testimonial.company}
          </p>
        </div>
        {testimonial.companyLogo && (
          <img
            src={testimonial.companyLogo}
            alt={testimonial.company}
            className="h-6 w-auto opacity-60 hover:opacity-100 transition-opacity duration-200"
            loading="lazy"
          />
        )}
      </figcaption>
    </motion.figure>
  );
}

// --- Small Testimonial Card --------------------------------------------------

function SmallCard({ testimonial }: { testimonial: Testimonial }) {
  return (
    <motion.figure
      variants={cardVariants}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className="flex flex-col rounded-xl border border-[hsl(var(--border))] bg-[hsl(var(--card))] p-6 shadow-sm hover:shadow-lg transition-shadow duration-200"
    >
      {testimonial.rating && <StarRating rating={testimonial.rating} />}

      <blockquote className="mt-3 flex-1 text-sm leading-relaxed text-[hsl(var(--foreground)/0.8)]">
        &ldquo;{testimonial.quote}&rdquo;
      </blockquote>

      <figcaption className="mt-4 flex items-center gap-3 border-t border-[hsl(var(--border))] pt-4">
        <img
          src={testimonial.avatar}
          alt={`Photo of ${testimonial.name}`}
          className="h-10 w-10 rounded-full object-cover"
          loading="lazy"
          width={40}
          height={40}
        />
        <div className="min-w-0">
          <p className="text-sm font-semibold text-[hsl(var(--foreground))] truncate">
            {testimonial.name}
          </p>
          <p className="text-xs text-[hsl(var(--muted-foreground))] truncate">
            {testimonial.title}, {testimonial.company}
          </p>
        </div>
      </figcaption>
    </motion.figure>
  );
}

// --- Layout Variant: Grid ----------------------------------------------------

function TestimonialsGrid() {
  const featured = testimonials.find((t) => t.featured);
  const others = testimonials.filter((t) => !t.featured);

  return (
    <div className="space-y-8">
      {/* Featured Card */}
      {featured && <FeaturedCard testimonial={featured} />}

      {/* Smaller Cards Grid */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: "-60px" }}
        className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
      >
        {others.map((testimonial) => (
          <SmallCard key={testimonial.name} testimonial={testimonial} />
        ))}
      </motion.div>
    </div>
  );
}

// --- Layout Variant: Carousel ------------------------------------------------

function TestimonialsCarousel() {
  return (
    <div className="relative overflow-hidden py-4">
      <div
        className="flex animate-scroll gap-6"
        aria-roledescription="carousel"
        aria-label="Customer testimonials"
      >
        {/* Duplicate items for infinite scroll effect */}
        {[...testimonials, ...testimonials].map((testimonial, index) => (
          <figure
            key={`${testimonial.name}-${index}`}
            role="group"
            aria-roledescription="slide"
            className="w-[320px] flex-shrink-0 rounded-xl border border-[hsl(var(--border))] bg-[hsl(var(--card))] p-6 shadow-sm"
          >
            {testimonial.rating && <StarRating rating={testimonial.rating} />}
            <blockquote className="mt-3 text-sm leading-relaxed text-[hsl(var(--foreground)/0.8)]">
              &ldquo;{testimonial.quote}&rdquo;
            </blockquote>
            <figcaption className="mt-4 flex items-center gap-3 border-t border-[hsl(var(--border))] pt-4">
              <img
                src={testimonial.avatar}
                alt={`Photo of ${testimonial.name}`}
                className="h-10 w-10 rounded-full object-cover"
                loading="lazy"
                width={40}
                height={40}
              />
              <div className="min-w-0">
                <p className="text-sm font-semibold text-[hsl(var(--foreground))] truncate">
                  {testimonial.name}
                </p>
                <p className="text-xs text-[hsl(var(--muted-foreground))] truncate">
                  {testimonial.title}, {testimonial.company}
                </p>
              </div>
            </figcaption>
          </figure>
        ))}
      </div>

      {/* Gradient fade edges */}
      <div className="pointer-events-none absolute inset-y-0 left-0 w-20 bg-gradient-to-r from-[hsl(var(--background))] to-transparent" />
      <div className="pointer-events-none absolute inset-y-0 right-0 w-20 bg-gradient-to-l from-[hsl(var(--background))] to-transparent" />

      {/* CSS for infinite scroll animation */}
      <style>{`
        @keyframes scroll {
          from { transform: translateX(0); }
          to { transform: translateX(-50%); }
        }
        .animate-scroll {
          animation: scroll 30s linear infinite;
        }
        @media (prefers-reduced-motion: reduce) {
          .animate-scroll { animation: none; }
        }
      `}</style>
    </div>
  );
}

// --- Main Section ------------------------------------------------------------

export default function Testimonials({
  variant = "grid",
}: {
  variant?: "grid" | "carousel";
}) {
  return (
    <section
      className="relative py-20 md:py-28"
      aria-labelledby="testimonials-heading"
    >
      <div className="mx-auto max-w-6xl px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mx-auto max-w-2xl text-center"
        >
          <p className="text-sm font-medium uppercase tracking-wider text-[hsl(var(--primary))]">
            What Our Customers Say
          </p>
          <h2
            id="testimonials-heading"
            className="mt-3 text-3xl font-bold tracking-tight text-[hsl(var(--foreground))] md:text-4xl"
          >
            Loved by teams worldwide
          </h2>
          <p className="mt-4 text-base text-[hsl(var(--muted-foreground))]">
            See how companies like yours ship faster and build better products.
          </p>
        </motion.div>

        {/* Content */}
        <div className="mt-14">
          {variant === "grid" ? (
            <TestimonialsGrid />
          ) : (
            <TestimonialsCarousel />
          )}
        </div>
      </div>
    </section>
  );
}
```

### Usage Notes

- Pass `variant="carousel"` for the infinite-scroll layout, or omit / pass `"grid"` for the default.
- Replace the `testimonials` array with real customer data.
- For Aceternity `InfiniteMovingCards`, dynamically import the component and pass the testimonials array to it instead of the CSS-based carousel above.
- Featured testimonial should always have the most compelling, specific quote with measurable results.
- Minimum 4 testimonials for carousel variant to feel full. Grid works well with 3-6.
- Avatar images should be 128x128px minimum for retina displays (rendered at 40-56px).
