# Viral Waitlist Section Template

> Defaults: See `section-defaults.md` for shared tokens, hover states, scroll animation, accessibility, and performance rules.

> **Replaces**: GetWaitlist ($15/mo), Waitlister ($15-39/mo), Viral Loops ($35-279/mo),
> Prefinery ($69-249/mo), LaunchList ($19 one-time). Self-hosted, free, zero vendor lock-in.

---

## Conversion Job

**CAPTURE AND MULTIPLY.** This is not just an email form — it's a growth engine. Every signup
generates a unique referral link. Every referral moves the user up the queue. Tiered rewards
create "just one more share" psychology. The result: 30-77% of signups come from referrals
(Harry's achieved 77%, Robinhood hit 50%+ conversion with zero ad spend).

---

## System Architecture

The waitlist has two states and three components:

### Two States
1. **Pre-signup**: Email capture form with value prop, social proof counter, and reward tiers preview
2. **Post-signup**: Referral dashboard showing queue position, unique referral link, sharing buttons, reward progress, and leaderboard

### Three Components
1. **Frontend** (this template) — React component with both states
2. **API route** (see `references/waitlist-api.md`) — Serverless function for signup, referral tracking, and data
3. **Storage** — Vercel KV, Upstash Redis, Supabase, or JSON file (all supported)

---

## Desktop Layout

### Pre-Signup State
```
                    [Badge: "Join the waitlist"]
                 [H1: Bold value proposition headline]
                  [Subheadline with specific benefit]

           ┌──────────────────────────────────────────┐
           │  [Email input]         [Join Waitlist →]  │
           └──────────────────────────────────────────┘
                   [Trust: "Join 1,247 others waiting"]

           ┌──── Reward Tier Preview (horizontal) ────┐
           │  3 referrals    5 referrals   10 referrals│
           │  Early Access   Beta Feature   Lifetime   │
           └──────────────────────────────────────────┘
```
- Outer: `relative min-h-screen flex flex-col items-center justify-center overflow-hidden`
- Inner: `text-center max-w-2xl mx-auto px-6 py-24`
- Form: `flex flex-col sm:flex-row gap-3 w-full max-w-md mx-auto`
- Reward tiers: `grid grid-cols-3 gap-4 max-w-lg mx-auto mt-12`

### Post-Signup State (Referral Dashboard)
```
           ┌──────────────────────────────────────────┐
           │          You're #47 in line               │
           │   ████████████░░░░░░░░  47 of 1,247      │
           └──────────────────────────────────────────┘

           ┌──────────────────────────────────────────┐
           │  Your referral link:                      │
           │  [https://product.com/?ref=abc123]  [📋]  │
           └──────────────────────────────────────────┘

           ┌──── Share ────────────────────────────────┐
           │  [Twitter]  [LinkedIn]  [WhatsApp]  [Email]│
           └──────────────────────────────────────────┘

           ┌──── Reward Progress ─────────────────────┐
           │  ✅ 1/3 Early Access                      │
           │  ○ 0/5 Beta Features                      │
           │  ○ 0/10 Lifetime Deal                     │
           └──────────────────────────────────────────┘

           ┌──── Leaderboard (top 10) ────────────────┐
           │  1. sarah@...   12 referrals              │
           │  2. mike@...     9 referrals              │
           │  3. you          1 referral   ← highlight │
           └──────────────────────────────────────────┘
```

## Mobile Layout (mobile-first)

### Pre-Signup
- Full-width form, email + button stacked vertically
- Reward tiers: `grid-cols-1 sm:grid-cols-3` — stack on mobile
- Generous touch targets: button `h-12`, input `h-12`
- `px-4 py-12` padding

### Post-Signup
- Position card full-width with `px-4`
- Referral link truncated with copy button (full-width tap target)
- Share buttons: 2x2 grid on mobile, 4-column on desktop
- Reward progress: vertical list, full-width cards
- Leaderboard: simplified, show top 5 on mobile

---

## Copy Structure

| Element | Content Rule |
|---|---|
| **Badge** | "Join the waitlist" or "Early access" — 3-5 words |
| **Headline** | Benefit-focused: "Be first to [outcome]" or "Get early access to [product]" |
| **Subheadline** | Specific: "Join [N] founders already waiting. Refer friends to skip the line." |
| **Email placeholder** | "Enter your email" (not "Subscribe" or "Sign up") |
| **Submit button** | "Join the Waitlist" or "Get Early Access" — action verb |
| **Social proof counter** | "Join [real number] others" — updates in real-time |
| **Position display** | "You're #[N] in line" — large, prominent number |
| **Referral CTA** | "Share your link to move up" — clear cause and effect |
| **Reward tier labels** | Specific rewards, not vague ("Lifetime deal" not "Special reward") |
| **Share pre-fills** | Platform-specific: Twitter gets hashtags, LinkedIn gets professional tone |

### Share Message Templates
```
Twitter:    "I just joined the waitlist for [Product] — [one-liner]. Join me → [link] #[product]"
LinkedIn:   "Excited to get early access to [Product]. [One-liner that sounds professional]. [link]"
WhatsApp:   "Hey! Check out [Product] — [one-liner]. Get early access: [link]"
Email:
  Subject:  "You need to see this — [Product]"
  Body:     "Hey,\n\nI just signed up for [Product] — [one-liner].\n\nYou can skip the line using my link: [link]\n\nCheck it out!"
```

---

## Section-Specific Notes

- **Honeypot field**: Hidden input `<input type="text" name="website" className="hidden" tabIndex={-1} />` — bots fill it, humans don't
- **Email validation**: Client-side regex + server-side MX record check (in API)
- **Rate limiting**: API enforces max 5 signups per IP per hour
- **Referral attribution**: Cookie stored for 30 days + URL `?ref=` parameter
- **Position calculation**: Dynamic — recalculated on every request based on referral count
- **Leaderboard**: Anonymized emails (s***h@gmail.com) for privacy
- **Animations**: Confetti burst on successful signup (CSS-only, no library needed)
- **Analytics events**: Fire `waitlist_signup`, `referral_share`, `referral_link_copy` events

---

## Ranking Algorithms (configurable)

The API supports 4 ranking modes (matches Prefinery's enterprise feature set):

| Algorithm | How It Works | Best For |
|-----------|-------------|----------|
| **FIFO** | First in, first out. Position = signup order. | Simple launches, no referral pressure |
| **referral-count** | More referrals = higher position. Ties broken by signup time. | Viral growth, maximum sharing incentive |
| **skip-n** | Each referral moves user up N positions (configurable, default 5). | Balanced — rewards sharing without making early users feel cheated |
| **points** | Configurable points per activity: signup (1), share (1), referral (5), milestone (10). | Gamified campaigns with multiple engagement signals |

Default: `skip-n` with skip value of 5 (best balance of fairness and viral incentive).

---

## Reward Tiers Configuration

```tsx
const defaultRewardTiers = [
  {
    referrals: 3,
    title: "Early Access",
    description: "Skip the line — get access before public launch",
    icon: Zap,       // Lucide icon
    emoji: "⚡",
  },
  {
    referrals: 5,
    title: "Beta Features",
    description: "Unlock features still in development",
    icon: Sparkles,
    emoji: "✨",
  },
  {
    referrals: 10,
    title: "Lifetime Deal",
    description: "Free forever — never pay a subscription",
    icon: Crown,
    emoji: "👑",
  },
];
```

Design guidelines for reward tiers:
- **3 tiers maximum** — more creates decision fatigue
- **First tier achievable** (3 referrals) — users need a quick win
- **Middle tier aspirational** (5-10) — keeps them sharing after first win
- **Top tier exceptional** (10-25) — the "just one more" stretch goal
- **Rewards must be real products/access** — not vague "prizes"
- **Display progress bars** — visual progress drives completion

---

## Complete JSX Template

```tsx
"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight,
  Check,
  Copy,
  Crown,
  Gift,
  Sparkles,
  Twitter,
  Linkedin,
  Mail,
  MessageCircle,
  Users,
  Zap,
  Loader2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

interface RewardTier {
  referrals: number;
  title: string;
  description: string;
  icon: React.ElementType;
  emoji: string;
}

interface LeaderboardEntry {
  position: number;
  email: string;       // anonymized: s***h@gmail.com
  referralCount: number;
  isCurrentUser: boolean;
}

interface WaitlistData {
  position: number;
  totalWaiters: number;
  referralCode: string;
  referralCount: number;
  referralLink: string;
  leaderboard: LeaderboardEntry[];
}

interface WaitlistProps {
  /* Content */
  productName?: string;
  headline?: string;
  subheadline?: string;
  badge?: string;
  /* Config */
  apiEndpoint?: string;
  rewardTiers?: RewardTier[];
  /* Styling */
  backgroundEffect?: React.ReactNode;
}

// -------------------------------------------------------------------
// Defaults
// -------------------------------------------------------------------

const defaultRewardTiers: RewardTier[] = [
  {
    referrals: 3,
    title: "Early Access",
    description: "Skip the line — get access before public launch",
    icon: Zap,
    emoji: "⚡",
  },
  {
    referrals: 5,
    title: "Beta Features",
    description: "Unlock features still in development",
    icon: Sparkles,
    emoji: "✨",
  },
  {
    referrals: 10,
    title: "Lifetime Deal",
    description: "Free forever — never pay a subscription",
    icon: Crown,
    emoji: "👑",
  },
];

// -------------------------------------------------------------------
// Animation variants
// -------------------------------------------------------------------

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.1 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

const dashboardVariants = {
  hidden: { opacity: 0, scale: 0.95 },
  show: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] },
  },
};

// -------------------------------------------------------------------
// Confetti burst (CSS-only, no library)
// -------------------------------------------------------------------

function ConfettiBurst() {
  return (
    <div className="pointer-events-none fixed inset-0 z-50" aria-hidden="true">
      {Array.from({ length: 50 }).map((_, i) => {
        const x = Math.random() * 100;
        const delay = Math.random() * 0.5;
        const duration = 1 + Math.random() * 1.5;
        const color = ["#6366f1", "#f97316", "#22c55e", "#eab308", "#ec4899"][
          Math.floor(Math.random() * 5)
        ];
        return (
          <span
            key={i}
            className="absolute w-2 h-2 rounded-full animate-confetti"
            style={{
              left: `${x}%`,
              top: "-10px",
              backgroundColor: color,
              animationDelay: `${delay}s`,
              animationDuration: `${duration}s`,
            }}
          />
        );
      })}
    </div>
  );
}

// -------------------------------------------------------------------
// Sub-components
// -------------------------------------------------------------------

function ShareButtons({
  referralLink,
  productName,
  onShare,
}: {
  referralLink: string;
  productName: string;
  onShare: () => void;
}) {
  const shareText = `I just joined the waitlist for ${productName}. Check it out →`;
  const encodedLink = encodeURIComponent(referralLink);
  const encodedText = encodeURIComponent(shareText);

  const channels = [
    {
      name: "Twitter",
      icon: Twitter,
      href: `https://twitter.com/intent/tweet?text=${encodedText}&url=${encodedLink}`,
      className: "bg-[#1DA1F2]/10 text-[#1DA1F2] hover:bg-[#1DA1F2]/20",
    },
    {
      name: "LinkedIn",
      icon: Linkedin,
      href: `https://www.linkedin.com/sharing/share-offsite/?url=${encodedLink}`,
      className: "bg-[#0A66C2]/10 text-[#0A66C2] hover:bg-[#0A66C2]/20",
    },
    {
      name: "WhatsApp",
      icon: MessageCircle,
      href: `https://wa.me/?text=${encodedText}%20${encodedLink}`,
      className: "bg-[#25D366]/10 text-[#25D366] hover:bg-[#25D366]/20",
    },
    {
      name: "Email",
      icon: Mail,
      href: `mailto:?subject=${encodeURIComponent(`Check out ${productName}`)}&body=${encodedText}%20${encodedLink}`,
      className: "bg-muted text-muted-foreground hover:bg-muted/80",
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
      {channels.map((channel) => (
        <a
          key={channel.name}
          href={channel.href}
          target="_blank"
          rel="noopener noreferrer"
          onClick={onShare}
          className={`flex items-center justify-center gap-2 rounded-lg px-4 py-3
                      text-sm font-medium transition-all duration-200
                      ${channel.className}`}
        >
          <channel.icon className="h-4 w-4" />
          {channel.name}
        </a>
      ))}
    </div>
  );
}

function RewardProgress({
  tiers,
  currentReferrals,
}: {
  tiers: RewardTier[];
  currentReferrals: number;
}) {
  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-foreground">Your Rewards</h3>
      {tiers.map((tier) => {
        const achieved = currentReferrals >= tier.referrals;
        const progress = Math.min(currentReferrals / tier.referrals, 1);
        return (
          <div
            key={tier.referrals}
            className={`flex items-center gap-4 rounded-lg border p-4 transition-colors
                        ${achieved
                          ? "border-primary/50 bg-primary/5"
                          : "border-border bg-card"
                        }`}
          >
            <div
              className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full
                          ${achieved
                            ? "bg-primary text-primary-foreground"
                            : "bg-muted text-muted-foreground"
                          }`}
            >
              {achieved ? (
                <Check className="h-5 w-5" />
              ) : (
                <tier.icon className="h-5 w-5" />
              )}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <span
                  className={`text-sm font-medium ${
                    achieved ? "text-primary" : "text-foreground"
                  }`}
                >
                  {tier.title}
                </span>
                <span className="text-xs text-muted-foreground">
                  {Math.min(currentReferrals, tier.referrals)}/{tier.referrals}
                </span>
              </div>
              <p className="text-xs text-muted-foreground mt-0.5 truncate">
                {tier.description}
              </p>
              {/* Progress bar */}
              <div className="mt-2 h-1.5 w-full rounded-full bg-muted overflow-hidden">
                <motion.div
                  className={`h-full rounded-full ${
                    achieved ? "bg-primary" : "bg-primary/60"
                  }`}
                  initial={{ width: 0 }}
                  animate={{ width: `${progress * 100}%` }}
                  transition={{ duration: 0.8, ease: "easeOut", delay: 0.3 }}
                />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function Leaderboard({ entries }: { entries: LeaderboardEntry[] }) {
  if (!entries.length) return null;

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-foreground flex items-center gap-2">
        <Users className="h-4 w-4 text-muted-foreground" />
        Top Referrers
      </h3>
      <div className="rounded-lg border border-border overflow-hidden">
        {entries.map((entry, i) => (
          <div
            key={entry.position}
            className={`flex items-center justify-between px-4 py-3 text-sm
                        ${i !== entries.length - 1 ? "border-b border-border" : ""}
                        ${entry.isCurrentUser
                          ? "bg-primary/5 font-medium"
                          : "bg-card"
                        }`}
          >
            <div className="flex items-center gap-3">
              <span
                className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold
                            ${i === 0 ? "bg-yellow-500/20 text-yellow-600" : ""}
                            ${i === 1 ? "bg-gray-300/20 text-gray-500" : ""}
                            ${i === 2 ? "bg-orange-400/20 text-orange-500" : ""}
                            ${i > 2 ? "bg-muted text-muted-foreground" : ""}`}
              >
                {entry.position}
              </span>
              <span className={entry.isCurrentUser ? "text-primary" : "text-foreground"}>
                {entry.isCurrentUser ? "You" : entry.email}
              </span>
            </div>
            <span className="text-muted-foreground">
              {entry.referralCount} referral{entry.referralCount !== 1 ? "s" : ""}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// -------------------------------------------------------------------
// Main Component
// -------------------------------------------------------------------

export default function Waitlist({
  productName = "YourProduct",
  headline = "Be the first to experience something new",
  subheadline = "Join the waitlist for early access. Refer friends to skip the line and unlock exclusive rewards.",
  badge = "Join the waitlist",
  apiEndpoint = "/api/waitlist",
  rewardTiers = defaultRewardTiers,
  backgroundEffect,
}: WaitlistProps) {
  // ---- State ----
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [waitlistData, setWaitlistData] = useState<WaitlistData | null>(null);
  const [copied, setCopied] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [totalWaiters, setTotalWaiters] = useState<number | null>(null);
  const honeypotRef = useRef<HTMLInputElement>(null);

  // ---- Check for referral code in URL ----
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const ref = params.get("ref");
    if (ref && /^[a-zA-Z0-9_-]{6,16}$/.test(ref)) {
      // Store validated referral code in cookie (30-day expiry)
      document.cookie = `waitlist_ref=${encodeURIComponent(ref)};max-age=${30 * 24 * 60 * 60};path=/;SameSite=Lax;Secure`;
    }
  }, []);

  // ---- Check for existing signup (localStorage) ----
  useEffect(() => {
    const stored = localStorage.getItem(`waitlist_${productName}`);
    if (stored) {
      try {
        const data = JSON.parse(stored);
        // Refresh data from API
        refreshWaitlistData(data.email);
      } catch {
        // Invalid stored data, ignore
      }
    }
    // Fetch total count for pre-signup display
    fetchTotalCount();
  }, []);

  async function fetchTotalCount() {
    try {
      const res = await fetch(`${apiEndpoint}/count`);
      if (res.ok) {
        const data = await res.json();
        setTotalWaiters(data.total);
      }
    } catch {
      // Silently fail — counter is optional
    }
  }

  async function refreshWaitlistData(userEmail: string) {
    try {
      const res = await fetch(`${apiEndpoint}/status?email=${encodeURIComponent(userEmail)}`);
      if (res.ok) {
        const data = await res.json();
        setWaitlistData(data);
      }
    } catch {
      // Silently fail — will show signup form
    }
  }

  // ---- Submit handler ----
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    // Honeypot check
    if (honeypotRef.current?.value) return;

    // Client-side email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Please enter a valid email address.");
      return;
    }

    setIsSubmitting(true);

    try {
      // Get referral code from cookie
      const refCookie = document.cookie
        .split("; ")
        .find((c) => c.startsWith("waitlist_ref="));
      const referredBy = refCookie ? refCookie.split("=")[1] : undefined;

      const res = await fetch(`${apiEndpoint}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email.toLowerCase().trim(),
          referredBy,
          source: window.location.pathname,
        }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => null);
        throw new Error(errData?.error || "Something went wrong. Please try again.");
      }

      const data: WaitlistData = await res.json();
      setWaitlistData(data);

      // Persist signup locally
      localStorage.setItem(
        `waitlist_${productName}`,
        JSON.stringify({ email: email.toLowerCase().trim() })
      );

      // Show confetti
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 3000);

      // Fire analytics event
      if (typeof gtag !== "undefined") {
        gtag("event", "waitlist_signup", {
          event_category: "conversion",
          event_label: referredBy ? "referred" : "organic",
        });
      }
      if (typeof plausible !== "undefined") {
        plausible("Waitlist Signup", {
          props: { type: referredBy ? "referred" : "organic" },
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsSubmitting(false);
    }
  }

  // ---- Copy referral link ----
  function copyReferralLink() {
    if (!waitlistData) return;
    navigator.clipboard.writeText(waitlistData.referralLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);

    // Fire analytics event
    if (typeof gtag !== "undefined") {
      gtag("event", "referral_link_copy", { event_category: "engagement" });
    }
  }

  // ---- Share tracking ----
  function handleShare() {
    if (typeof gtag !== "undefined") {
      gtag("event", "referral_share", { event_category: "engagement" });
    }
  }

  // ================================================================
  // RENDER
  // ================================================================

  return (
    <section
      aria-labelledby="waitlist-heading"
      className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden"
    >
      {/* Background effect slot */}
      {backgroundEffect && (
        <div className="absolute inset-0 z-0" aria-hidden="true">
          {backgroundEffect}
        </div>
      )}

      {/* Confetti */}
      <AnimatePresence>{showConfetti && <ConfettiBurst />}</AnimatePresence>

      <div className="relative z-10 w-full max-w-2xl mx-auto px-4 sm:px-6 py-16 sm:py-24 md:py-32">
        <AnimatePresence mode="wait">
          {!waitlistData ? (
            /* ==============================================================
               PRE-SIGNUP STATE: Email capture form
               ============================================================== */
            <motion.div
              key="signup"
              variants={containerVariants}
              initial="hidden"
              animate="show"
              exit={{ opacity: 0, y: -20, transition: { duration: 0.3 } }}
              className="text-center flex flex-col items-center gap-5 md:gap-6"
            >
              {/* Badge */}
              <motion.span
                variants={itemVariants}
                className="inline-flex items-center gap-2 rounded-full border border-border
                           bg-muted/50 px-4 py-1.5 text-sm font-medium text-foreground"
              >
                <Gift className="h-3.5 w-3.5 text-primary" aria-hidden="true" />
                {badge}
              </motion.span>

              {/* Headline */}
              <motion.h1
                id="waitlist-heading"
                variants={itemVariants}
                className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold
                           tracking-tight text-foreground leading-[1.08] max-w-4xl"
              >
                {headline}
              </motion.h1>

              {/* Subheadline */}
              <motion.p
                variants={itemVariants}
                className="text-lg sm:text-xl text-muted-foreground max-w-xl leading-relaxed"
              >
                {subheadline}
              </motion.p>

              {/* Email form */}
              <motion.form
                variants={itemVariants}
                onSubmit={handleSubmit}
                className="w-full max-w-md mx-auto mt-2"
              >
                {/* Honeypot — hidden from humans, bots fill it */}
                <input
                  ref={honeypotRef}
                  type="text"
                  name="website"
                  className="hidden"
                  tabIndex={-1}
                  autoComplete="off"
                  aria-hidden="true"
                />

                <div className="flex flex-col sm:flex-row gap-3">
                  <Input
                    type="email"
                    value={email}
                    onChange={(e) => {
                      setEmail(e.target.value);
                      setError(null);
                    }}
                    placeholder="Enter your email"
                    required
                    autoComplete="email"
                    className="h-12 text-base flex-1"
                    aria-label="Email address"
                    disabled={isSubmitting}
                  />
                  <Button
                    type="submit"
                    size="lg"
                    disabled={isSubmitting}
                    className="h-12 px-6 text-base font-semibold w-full sm:w-auto
                               shadow-lg shadow-primary/20"
                  >
                    {isSubmitting ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <>
                        Join the Waitlist
                        <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" />
                      </>
                    )}
                  </Button>
                </div>

                {/* Error message */}
                {error && (
                  <p className="mt-2 text-sm text-destructive" role="alert">
                    {error}
                  </p>
                )}
              </motion.form>

              {/* Social proof counter */}
              {totalWaiters !== null && totalWaiters > 0 && (
                <motion.p
                  variants={itemVariants}
                  className="text-sm text-muted-foreground flex items-center gap-2"
                >
                  <Users className="h-4 w-4" aria-hidden="true" />
                  Join {totalWaiters.toLocaleString()} others already waiting
                </motion.p>
              )}

              {/* Reward tier preview */}
              <motion.div
                variants={itemVariants}
                className="mt-8 w-full"
              >
                <p className="text-xs uppercase tracking-wider text-muted-foreground mb-4">
                  Refer friends to unlock
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-lg mx-auto">
                  {rewardTiers.map((tier) => (
                    <div
                      key={tier.referrals}
                      className="flex flex-col items-center gap-2 rounded-lg border border-border
                                 bg-card/50 p-4 text-center"
                    >
                      <span className="text-2xl" aria-hidden="true">{tier.emoji}</span>
                      <span className="text-sm font-medium text-foreground">
                        {tier.title}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {tier.referrals} referral{tier.referrals !== 1 ? "s" : ""}
                      </span>
                    </div>
                  ))}
                </div>
              </motion.div>
            </motion.div>
          ) : (
            /* ==============================================================
               POST-SIGNUP STATE: Referral dashboard
               ============================================================== */
            <motion.div
              key="dashboard"
              variants={dashboardVariants}
              initial="hidden"
              animate="show"
              className="space-y-6"
            >
              {/* Success header */}
              <div className="text-center space-y-2">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 200, damping: 15 }}
                  className="mx-auto flex h-16 w-16 items-center justify-center rounded-full
                             bg-primary/10 text-primary"
                >
                  <Check className="h-8 w-8" />
                </motion.div>
                <h2 className="text-2xl sm:text-3xl font-bold text-foreground">
                  You&apos;re on the list!
                </h2>
              </div>

              {/* Position card */}
              <div className="rounded-xl border border-border bg-card p-6 text-center space-y-3">
                <p className="text-sm text-muted-foreground">Your position</p>
                <p className="text-5xl sm:text-6xl font-bold text-foreground tabular-nums">
                  #{waitlistData.position.toLocaleString()}
                </p>
                <div className="mx-auto w-full max-w-xs">
                  <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                    <motion.div
                      className="h-full rounded-full bg-primary"
                      initial={{ width: 0 }}
                      animate={{
                        width: `${Math.max(
                          5,
                          100 - (waitlistData.position / waitlistData.totalWaiters) * 100
                        )}%`,
                      }}
                      transition={{ duration: 1, ease: "easeOut", delay: 0.5 }}
                    />
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {waitlistData.position} of {waitlistData.totalWaiters.toLocaleString()}
                  </p>
                </div>
              </div>

              {/* Referral link */}
              <div className="rounded-xl border border-border bg-card p-4 space-y-2">
                <p className="text-sm font-medium text-foreground">
                  Share your link to move up
                </p>
                <div className="flex gap-2">
                  <Input
                    readOnly
                    value={waitlistData.referralLink}
                    className="h-10 text-sm bg-muted font-mono"
                    onClick={(e) => (e.target as HTMLInputElement).select()}
                  />
                  <Button
                    variant="outline"
                    size="sm"
                    className="h-10 px-3 shrink-0"
                    onClick={copyReferralLink}
                  >
                    {copied ? (
                      <Check className="h-4 w-4 text-primary" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground">
                  {waitlistData.referralCount} referral{waitlistData.referralCount !== 1 ? "s" : ""} so far
                </p>
              </div>

              {/* Share buttons */}
              <ShareButtons
                referralLink={waitlistData.referralLink}
                productName={productName}
                onShare={handleShare}
              />

              {/* Reward progress */}
              <RewardProgress
                tiers={rewardTiers}
                currentReferrals={waitlistData.referralCount}
              />

              {/* Leaderboard */}
              <Leaderboard entries={waitlistData.leaderboard} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Confetti keyframe — add to globals.css */}
      <style jsx global>{`
        @keyframes confetti {
          0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
          }
          100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
          }
        }
        .animate-confetti {
          animation: confetti linear forwards;
        }
      `}</style>
    </section>
  );
}
```
