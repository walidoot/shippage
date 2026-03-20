# Framework Adapters

> Default output is **React + Tailwind CSS + Framer Motion + shadcn/ui**.
> Adapt for the user's framework using this guide.

---

## Next.js (App Router) — Default

```
Structure:   app/layout.tsx, app/page.tsx, app/globals.css
Images:      next/image (priority, quality={90}, sizes)
Fonts:       next/font/google — zero CLS, auto font-display: swap
Dynamic:     next/dynamic({ ssr: false }) for background effects
Dark mode:   next-themes (ThemeProvider in layout.tsx)
Metadata:    export const metadata: Metadata = { ... }
Deploy:      npx vercel --prod
```

### Key patterns
- Add `"use client"` at top of any file using useState, useEffect, or Framer Motion
- Use `<Image>` instead of `<img>` for automatic optimization
- Use `<Link>` from `next/link` for client-side navigation

---

## Vite + React

```
Structure:   src/main.tsx, src/App.tsx, src/index.css
Images:      <img> with loading="lazy", explicit width/height
Fonts:       @fontsource/inter or Google Fonts @import in CSS
Dynamic:     React.lazy() + <Suspense fallback={...}>
Dark mode:   Manual class toggle on <html> or use a context
Deploy:      npm run build → deploy dist/
```

### Key changes from Next.js default
- Remove all `"use client"` directives (everything is client-side)
- Replace `next/image` → `<img loading="lazy" width={W} height={H} />`
- Replace `next/link` → `<a href="...">` or react-router `<Link>`
- Replace `next/font` → CSS `@import` or fontsource package
- Replace `next/dynamic` → `React.lazy()`

---

## Remix

```
Structure:   app/routes/_index.tsx, app/root.tsx
Images:      <img> (or remix-image for optimization)
Fonts:       links() export in root.tsx
Dark mode:   Cookie-based or session-based theme
Deploy:      Varies by adapter (Vercel, Cloudflare, Node)
```

### Key changes
- Remove `"use client"` — Remix handles server/client boundary differently
- Use `links()` function export for font preloading
- Use `<img>` with standard attributes

---

## Astro

```
Structure:   src/pages/index.astro, src/layouts/Layout.astro
Images:      <Image> from astro:assets (built-in optimization)
Fonts:       @fontsource packages or <link> in Layout.astro
Tailwind:    @astrojs/tailwind integration
Deploy:      astro build → deploy dist/
```

### Key changes
- React components become "islands": `<HeroSplit client:visible />`
- Remove `"use client"` directives
- Only interactive sections need `client:visible` (static sections can be Astro)
- Replace `next/image` → Astro `<Image>` component

---

## Vue 3 / Nuxt

```
Structure:   src/App.vue (Vue) or pages/index.vue (Nuxt)
Animation:   @vueuse/motion or CSS transitions (replaces Framer Motion)
Components:  shadcn-vue (same API, Vue SFC format)
```

### Key changes
- Convert JSX → `<template>` + `<script setup>` SFC syntax
- Replace `motion.div` → `<Motion>` from @vueuse/motion or CSS transitions
- Replace `useState` → `ref()` / `reactive()`
- Tailwind classes transfer unchanged

---

## Svelte / SvelteKit

```
Structure:   src/routes/+page.svelte (SvelteKit)
Animation:   svelte/transition (fly, fade, slide)
Components:  shadcn-svelte (same API, Svelte syntax)
```

### Key changes
- Convert JSX → Svelte template syntax (`{#if}`, `{#each}`)
- Replace Framer Motion → `transition:fly={{ y: 24, duration: 500 }}`
- Replace `useState` → Svelte `$state` rune (Svelte 5) or `let` (Svelte 4)
- Tailwind classes transfer unchanged

---

## Deployment Checklist (All Frameworks)

```
Pre-deploy:
  [ ] Favicon (favicon.ico + apple-touch-icon.png)
  [ ] OG image (1200x630, og-image.png)
  [ ] robots.txt (allow all, link to sitemap)
  [ ] sitemap.xml (list all pages)
  [ ] Meta tags (title, description, og:*, twitter:*)
  [ ] JSON-LD structured data (Organization + WebSite + FAQPage)
  [ ] Security headers (X-Frame-Options, CSP, HSTS)
  [ ] Performance: Lighthouse score > 90

Deploy options:
  Vercel:   npx vercel --prod
  Netlify:  npm run build && netlify deploy --prod --dir=dist
  Docker:   Multi-stage build (node:20-alpine → nginx:alpine)
```

---

## JSON-LD Structured Data (All Frameworks)

Structured data gives Google rich results — star ratings, FAQ dropdowns, breadcrumbs,
organization info. Every landing page should include these three schemas in `<head>`.

### XSS Prevention

**IMPORTANT:** Never pass unsanitized user input into `JSON.stringify()` inside
`dangerouslySetInnerHTML`. A malicious string containing `</script>` breaks out of
the JSON-LD block and injects arbitrary HTML/JS. Always use this helper:

```tsx
function safeJsonLd(obj: unknown): string {
  return JSON.stringify(obj)
    .replace(/<\/script/gi, "<\\/script")
    .replace(/<!--/g, "<\\!--");
}

// Usage: dangerouslySetInnerHTML={{ __html: safeJsonLd(data) }}
```

All examples below use `safeJsonLd()` instead of raw `JSON.stringify()`.

### 1. Organization Schema (every page)

```tsx
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: safeJsonLd({
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ProductName",
  "url": "https://productname.com",
  "logo": "https://productname.com/logo.png",
  "description": "One-line product description from intake",
  "sameAs": [
    "https://twitter.com/productname",
    "https://github.com/productname"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "support@productname.com",
    "contactType": "customer support"
  }
}) }} />
```

### 2. WebSite Schema with SearchAction (homepage only)

```tsx
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: safeJsonLd({
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "ProductName",
  "url": "https://productname.com",
  "description": "Meta description from intake",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://productname.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}) }} />
```

Skip `potentialAction` if the product has no search feature.

### 3. SoftwareApplication Schema (SaaS products)

```tsx
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: safeJsonLd({
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "ProductName",
  "applicationCategory": "BusinessApplication",  // or DeveloperApplication, DesignApplication
  "operatingSystem": "Web",
  "url": "https://productname.com",
  "description": "One-line product description",
  "offers": {
    "@type": "AggregateOffer",
    "priceCurrency": "USD",
    "lowPrice": "0",         // free tier price
    "highPrice": "99",       // highest tier price
    "offerCount": "3"        // number of pricing tiers
  }
}) }} />
```

### 4. FAQPage Schema (when FAQ section exists)

```tsx
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: safeJsonLd({
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": faqItems.map(item => ({
    "@type": "Question",
    "name": item.question,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": item.answer
    }
  }))
}) }} />
```

This is the highest-value schema — Google renders FAQ answers directly in search results,
increasing SERP real estate by 2-3x. Always include when the page has an FAQ section.

### Framework-Specific Rendering

| Framework | How to render JSON-LD |
|-----------|----------------------|
| Next.js (App Router) | `<script>` in `layout.tsx` or page metadata `export const metadata` |
| Next.js (Pages) | `<Head><script type="application/ld+json">` |
| Vite / Remix | `<script type="application/ld+json">` in HTML head |
| Astro | `<script type="application/ld+json" set:html={safeJsonLd(data)}>` in `<head>` |
| Vue / Nuxt | `useHead({ script: [{ type: 'application/ld+json', innerHTML: safeJsonLd(data) }] })` |
| Svelte / SvelteKit | `<svelte:head><script type="application/ld+json">{@html safeJsonLd(data)}</script></svelte:head>` |

> **IMPORTANT:** Every framework must use `safeJsonLd()` (defined above) instead of raw `JSON.stringify()`.
> The Svelte example uses `{@html ...}` because the string is already escaped by `safeJsonLd()`.
> Never pass unescaped user input into JSON-LD script blocks in any framework.

---

## OG Image (All Frameworks)

Every social share needs an Open Graph image. Without one, links to the page look
bare on Twitter, LinkedIn, Slack, and iMessage. This is the single highest-ROI
asset for organic traffic.

### Spec

```
Size:     1200 × 630px (2:1 ratio)
Format:   PNG or JPG (< 300KB)
Content:  Product name + one-line value prop + logo + brand colors
Text:     Large, readable at thumbnail size (minimum 40px equivalent)
```

### Meta Tags (add to `<head>`)

```html
<meta property="og:image" content="https://productname.com/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="ProductName — one-line value prop" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://productname.com/og-image.png" />
```

### CSS-Generated OG Image Template

When the user has no OG image, generate one as a React component they can screenshot
or render to PNG via a serverless function:

```tsx
// components/og-image.tsx — render at 1200x630 for screenshot/export
export function OGImage({ title, subtitle, logo }: {
  title: string; subtitle: string; logo?: string;
}) {
  return (
    <div className="flex h-[630px] w-[1200px] flex-col items-center justify-center bg-background p-16">
      <div className="flex flex-col items-center gap-6 text-center">
        {logo && <img src={logo} alt="" className="h-16 w-auto" />}
        <h1 className="text-6xl font-bold tracking-tight text-foreground">
          {title}
        </h1>
        <p className="max-w-[800px] text-2xl text-muted-foreground">
          {subtitle}
        </p>
      </div>
      <div className="absolute bottom-8 right-8 text-lg text-muted-foreground">
        productname.com
      </div>
    </div>
  );
}
```

### Next.js Dynamic OG (recommended for Next.js projects)

```tsx
// app/opengraph-image.tsx — Next.js auto-generates OG image at build time
import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "ProductName — one-line value prop";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    <div style={{
      display: "flex", flexDirection: "column", alignItems: "center",
      justifyContent: "center", width: "100%", height: "100%",
      backgroundColor: "#0a0a0a", color: "#fafafa", padding: "60px",
    }}>
      <h1 style={{ fontSize: "64px", fontWeight: "bold", textAlign: "center" }}>
        ProductName
      </h1>
      <p style={{ fontSize: "28px", color: "#a1a1aa", marginTop: "16px", textAlign: "center" }}>
        One-line value prop from intake
      </p>
    </div>,
    { ...size }
  );
}
```

---

## Sitemap & robots.txt (All Frameworks)

### robots.txt

```txt
User-agent: *
Allow: /

Sitemap: https://productname.com/sitemap.xml
```

Block legal page crawling only if you want (optional — most SaaS sites don't):
```txt
User-agent: *
Allow: /
Disallow: /api/

Sitemap: https://productname.com/sitemap.xml
```

### sitemap.xml

Generate from the page routes. For a typical landing page with legal pages:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://productname.com/</loc>
    <lastmod>2026-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://productname.com/privacy</loc>
    <lastmod>2026-01-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://productname.com/terms</loc>
    <lastmod>2026-01-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://productname.com/cookies</loc>
    <lastmod>2026-01-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>
```

### Framework-Specific Generation

| Framework | How |
|-----------|-----|
| **Next.js (App Router)** | `app/sitemap.ts` + `app/robots.ts` — export functions, auto-generated at build |
| **Next.js (Pages)** | `next-sitemap` package in `next-sitemap.config.js` |
| **Vite** | Static `public/robots.txt` + `public/sitemap.xml` |
| **Remix** | `app/routes/[sitemap.xml].tsx` + `app/routes/[robots.txt].tsx` resource routes |
| **Astro** | `@astrojs/sitemap` integration (auto) + `public/robots.txt` |
| **Nuxt** | `nuxt-simple-sitemap` module (auto) + `public/robots.txt` |
| **SvelteKit** | `src/routes/sitemap.xml/+server.ts` + `static/robots.txt` |

### Next.js App Router Example

```tsx
// app/sitemap.ts
import type { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://productname.com";
  return [
    { url: baseUrl, lastModified: new Date(), changeFrequency: "weekly", priority: 1 },
    { url: `${baseUrl}/privacy`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.3 },
    { url: `${baseUrl}/terms`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.3 },
    { url: `${baseUrl}/cookies`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.3 },
  ];
}

// app/robots.ts
import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/", disallow: "/api/" },
    sitemap: "https://productname.com/sitemap.xml",
  };
}
```

---

## Analytics Setup (All Frameworks)

Every generated page should include basic conversion tracking. Without measurement,
the page is a guess — not a sales machine.

### Step 1: Ask the User

Before adding tracking, always ask:

> "Do you have a Google Analytics ID (G-XXXXXXXXXX), Plausible URL, or Umami instance?
> I'll wire it into the page. If not, I'll add placeholder comments you can fill in later."

### Step 2: Add Analytics Script

**Google Analytics 4 (default)**:
```tsx
// In layout head or _app.tsx — replace G-XXXXXXXXXX with user's ID
<Script src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX" strategy="afterInteractive" />
<Script id="gtag" strategy="afterInteractive">
  {`window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}
    gtag('js',new Date());gtag('config','G-XXXXXXXXXX');`}
</Script>
```

**Plausible (privacy-friendly alternative)**:
```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

**Umami (self-hosted)**:
```html
<script defer src="https://your-umami.com/script.js" data-website-id="your-id"></script>
```

For Vite/Remix/Astro: use `<script>` tags directly in HTML head instead of Next.js `<Script>`.

### Step 3: Add CTA Click Events

Add to every CTA button — tracks which CTAs drive conversions:
```tsx
onClick={() => {
  // Google Analytics 4
  if (typeof gtag !== 'undefined') {
    gtag('event', 'cta_click', {
      event_category: 'conversion',
      event_label: 'hero_primary_cta',  // unique per CTA location
    });
  }
  // Plausible
  if (typeof plausible !== 'undefined') {
    plausible('CTA Click', { props: { location: 'hero_primary_cta' } });
  }
}}
```

Use these labels for each CTA location:
- `hero_primary_cta` — main hero button
- `hero_secondary_cta` — secondary hero button (if present)
- `pricing_cta` — pricing section button
- `footer_cta` — final CTA section button
- `navbar_cta` — sticky nav button

### Step 4: Scroll Depth Tracking

Auto-fire events at 25%, 50%, 75%, 100% scroll depth:
```tsx
useEffect(() => {
  const thresholds = [25, 50, 75, 100];
  const fired = new Set<number>();

  const handleScroll = () => {
    const scrollPercent = Math.round(
      (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
    );
    for (const t of thresholds) {
      if (scrollPercent >= t && !fired.has(t)) {
        fired.add(t);
        if (typeof gtag !== 'undefined') {
          gtag('event', 'scroll_depth', { event_label: `${t}%` });
        }
      }
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

---

## Content Security Policy (All Frameworks)

A Content Security Policy (CSP) header prevents XSS and data injection attacks.
Every production landing page should ship with at least a baseline CSP.

### Baseline CSP Header

> **Security note:** The baseline uses `'unsafe-inline'` for `style-src` because Tailwind CSS
> injects inline styles. For `script-src`, use **nonce-based** CSP when possible (see below).
> If your framework doesn't support nonces, `'unsafe-inline'` is acceptable as a starting point
> but should be upgraded before production.

**Tier 1 — Nonce-based (recommended for production):**
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-{SERVER_GENERATED_NONCE}' https://www.googletagmanager.com https://www.google-analytics.com https://plausible.io;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  img-src 'self' data: https: blob:;
  font-src 'self' https://fonts.gstatic.com;
  connect-src 'self' https://www.google-analytics.com https://plausible.io https://region1.google-analytics.com;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
```

Generate a unique nonce per request server-side (`crypto.randomBytes(16).toString('base64')`)
and inject it into every `<script>` tag as `nonce="{value}"`. This eliminates the need for
`'unsafe-inline'` in `script-src`.

**Tier 2 — Fallback (when nonces aren't feasible):**
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com https://plausible.io;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  img-src 'self' data: https: blob:;
  font-src 'self' https://fonts.gstatic.com;
  connect-src 'self' https://www.google-analytics.com https://plausible.io https://region1.google-analytics.com;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
```

### Framework-Specific Setup

| Framework | How |
|-----------|-----|
| **Next.js** | `next.config.js` → `headers()` function returning CSP |
| **Vite** | Nginx/Caddy config or `vite-plugin-csp` |
| **Remix** | Return headers from root loader |
| **Astro** | `astro.config.mjs` security headers or hosting config |
| **Nuxt** | `nuxt.config.ts` → `routeRules` or `nitro.routeRules` |
| **SvelteKit** | `hooks.server.ts` → `handle()` function |

### Next.js Example (Nonce-Based CSP)

```tsx
// middleware.ts — generate nonce per request (Next.js 13+)
import { NextRequest, NextResponse } from "next/server";
import { randomBytes } from "crypto";

export function middleware(req: NextRequest) {
  const nonce = randomBytes(16).toString("base64");
  const csp = [
    "default-src 'self'",
    `script-src 'self' 'nonce-${nonce}' https://www.googletagmanager.com https://www.google-analytics.com https://plausible.io`,
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "img-src 'self' data: https: blob:",
    "font-src 'self' https://fonts.gstatic.com",
    "connect-src 'self' https://www.google-analytics.com https://plausible.io https://region1.google-analytics.com",
    "frame-src 'none'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
  ].join("; ");

  const headers = new Headers(req.headers);
  headers.set("x-nonce", nonce);

  const res = NextResponse.next({ request: { headers } });
  res.headers.set("Content-Security-Policy", csp);
  res.headers.set("X-Frame-Options", "DENY");
  res.headers.set("X-Content-Type-Options", "nosniff");
  res.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  res.headers.set("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
  return res;
}

// In layout.tsx — pass nonce to <Script> components:
// const nonce = headers().get("x-nonce") ?? "";
// <Script nonce={nonce} src="..." />
```

**Fallback (static headers via next.config.js):**
```js
// next.config.js — use when middleware nonces aren't needed
const securityHeaders = [
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com https://plausible.io",
      "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
      "img-src 'self' data: https: blob:",
      "font-src 'self' https://fonts.gstatic.com",
      "connect-src 'self' https://www.google-analytics.com https://plausible.io https://region1.google-analytics.com",
      "frame-src 'none'",
      "object-src 'none'",
      "base-uri 'self'",
      "form-action 'self'",
    ].join("; "),
  },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
];

module.exports = {
  async headers() {
    return [{ source: "/(.*)", headers: securityHeaders }];
  },
};
```

**Important**: If the page uses Google Fonts via `@import` or `<link>`, add
`https://fonts.googleapis.com` to `style-src` and `https://fonts.gstatic.com`
to `font-src`. Adjust `script-src` for whichever analytics provider is in use.

---

### Key Metrics to Track

| Metric | What It Tells You | Action If Bad |
|--------|------------------|---------------|
| Bounce rate (hero) | Is the headline working? | Rewrite headline + subheadline |
| Scroll depth to CTA | Are visitors reaching the conversion point? | Move CTA higher or add mid-page CTA |
| CTA click rate | Is the offer compelling? | Change CTA text, add trust hint |
| Time on page | Are visitors engaged or just scrolling? | Add more engaging content sections |
| Scroll to pricing | Are visitors interested in buying? | Test pricing placement and tiers |
