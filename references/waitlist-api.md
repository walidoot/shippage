# Waitlist API — Serverless Backend

> The backend that powers the viral waitlist system. Self-hosted, zero vendor lock-in.
> Generates unique referral codes, tracks referrals, calculates positions, manages rewards.

---

## Architecture

```
Client (waitlist.tsx)
  ├── POST /api/waitlist/signup     → Create signup, generate referral code
  ├── GET  /api/waitlist/status     → Get position, referrals, leaderboard
  ├── GET  /api/waitlist/count      → Get total waitlist count (public)
  └── POST /api/waitlist/export     → Export CSV (admin, protected)

Storage (pick one):
  ├── Vercel KV / Upstash Redis    → Recommended for production
  ├── Supabase (PostgreSQL)        → Full-featured, free tier available
  └── JSON file (fs)               → Local dev / prototype only
```

---

## Storage Adapters

### Option A: Vercel KV / Upstash Redis (Recommended)

```bash
npm install @vercel/kv
# or
npm install @upstash/redis
```

Data model (Redis keys):
```
waitlist:emails              → SET of all emails (dedup check)
waitlist:user:{email}        → HASH { email, referralCode, referredBy, referralCount, signupTime, source, ipHash }
waitlist:ref:{code}          → STRING email (reverse lookup: code → user)
waitlist:referrals:{email}   → SET of emails this user referred
waitlist:count               → STRING total count
waitlist:ratelimit:{ipHash}  → managed by @upstash/ratelimit (sliding window)
```

### Option B: Supabase (PostgreSQL)

```sql
CREATE TABLE waitlist (
  id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email         TEXT UNIQUE NOT NULL,
  referral_code TEXT UNIQUE NOT NULL,
  referred_by   TEXT,                          -- referral code of referrer
  referral_count INTEGER DEFAULT 0,
  signup_time   TIMESTAMPTZ DEFAULT now(),
  source        TEXT,                          -- URL they signed up from
  ip_hash       TEXT,                          -- SHA-256 hash, not raw IP (GDPR Article 6)
  metadata      JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_waitlist_referral_code ON waitlist(referral_code);
CREATE INDEX idx_waitlist_referred_by ON waitlist(referred_by);
CREATE INDEX idx_waitlist_signup_time ON waitlist(signup_time);

-- Function to increment referral count
CREATE OR REPLACE FUNCTION increment_referral_count(referrer_code TEXT)
RETURNS void AS $$
  UPDATE waitlist SET referral_count = referral_count + 1
  WHERE referral_code = referrer_code;
$$ LANGUAGE sql;
```

### Option C: JSON File (Prototype Only)

```typescript
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join } from "path";

const DB_PATH = join(process.cwd(), "data", "waitlist.json");

interface WaitlistDB {
  users: Record<string, WaitlistUser>;
  emailToCode: Record<string, string>;
  codeToEmail: Record<string, string>;
}

function readDB(): WaitlistDB {
  if (!existsSync(DB_PATH)) {
    return { users: {}, emailToCode: {}, codeToEmail: {} };
  }
  return JSON.parse(readFileSync(DB_PATH, "utf-8"));
}

function writeDB(db: WaitlistDB): void {
  writeFileSync(DB_PATH, JSON.stringify(db, null, 2));
}
```

---

## API Routes (Next.js App Router)

### POST /api/waitlist/signup

```typescript
// app/api/waitlist/signup/route.ts
import { NextRequest, NextResponse } from "next/server";
import { nanoid } from "nanoid";
import { createHash } from "crypto";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

interface SignupRequest {
  email: string;
  referredBy?: string;    // referral code of the person who referred them
  source?: string;        // page pathname (not full URL — avoid leaking query params)
}

interface SignupResponse {
  position: number;
  totalWaiters: number;
  referralCode: string;
  referralCount: number;
  referralLink: string;
  leaderboard: LeaderboardEntry[];
}

// -------------------------------------------------------------------
// Configuration
// -------------------------------------------------------------------

const RANKING_ALGORITHM = "skip-n";   // "fifo" | "referral-count" | "skip-n" | "points"
const SKIP_VALUE = 5;                  // positions to skip per referral (skip-n mode)
const RATE_LIMIT_MAX = 5;             // max signups per IP per hour
const REFERRAL_CODE_LENGTH = 8;       // nanoid length
const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL || "https://yourproduct.com";

// -------------------------------------------------------------------
// Helpers
// -------------------------------------------------------------------

function generateReferralCode(): string {
  // URL-safe, 8 chars, ~1 trillion combinations
  return nanoid(REFERRAL_CODE_LENGTH);
}

function anonymizeEmail(email: string): string {
  const [local, domain] = email.split("@");
  if (local.length <= 2) return `${local[0]}***@${domain}`;
  return `${local[0]}${local[1]}***@${domain}`;
}

function hashIp(ip: string): string {
  // One-way hash — GDPR compliant, cannot be reversed to raw IP
  return createHash("sha256").update(ip).digest("hex").slice(0, 16);
}

function isValidEmail(email: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!regex.test(email)) return false;
  // Block disposable email domains (top 20)
  const disposable = [
    "mailinator.com", "guerrillamail.com", "tempmail.com", "throwaway.email",
    "yopmail.com", "sharklasers.com", "guerrillamailblock.com", "grr.la",
    "dispostable.com", "mailnesia.com", "maildrop.cc", "10minutemail.com",
    "trashmail.com", "fakeinbox.com", "emailondeck.com", "getnada.com",
    "temp-mail.org", "mohmal.com", "burner.kiwi", "harakirimail.com",
  ];
  const domain = email.split("@")[1].toLowerCase();
  return !disposable.includes(domain);
}

// -------------------------------------------------------------------
// Position Calculation
// -------------------------------------------------------------------

function calculatePosition(
  user: { signupTime: number; referralCount: number },
  allUsers: { email: string; signupTime: number; referralCount: number }[],
): number {
  // Sort all users by the chosen algorithm
  const sorted = [...allUsers].sort((a, b) => {
    switch (RANKING_ALGORITHM) {
      case "fifo":
        return a.signupTime - b.signupTime;

      case "referral-count":
        if (b.referralCount !== a.referralCount) {
          return b.referralCount - a.referralCount;
        }
        return a.signupTime - b.signupTime;  // tie-break: earlier signup wins

      case "skip-n": {
        const aScore = a.signupTime - (a.referralCount * SKIP_VALUE * 1000);
        const bScore = b.signupTime - (b.referralCount * SKIP_VALUE * 1000);
        return aScore - bScore;
      }

      case "points": {
        // Points: signup=1, each referral=5
        const aPoints = 1 + a.referralCount * 5;
        const bPoints = 1 + b.referralCount * 5;
        if (bPoints !== aPoints) return bPoints - aPoints;
        return a.signupTime - b.signupTime;
      }

      default:
        return a.signupTime - b.signupTime;
    }
  });

  return sorted.findIndex((u) => u.email === user.email) + 1;  // 1-indexed
}

// -------------------------------------------------------------------
// Rate Limiting (Redis-backed — survives cold starts)
// -------------------------------------------------------------------
//
// Uses @upstash/ratelimit for serverless-safe rate limiting.
// Falls back to a per-request check if Redis is unavailable.
//
// Install: npm install @upstash/ratelimit @upstash/redis
//
// Env vars: UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN

import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(RATE_LIMIT_MAX, "1 h"),
  analytics: true,
  prefix: "waitlist:ratelimit",
});

async function checkRateLimit(ip: string): Promise<boolean> {
  try {
    const { success } = await ratelimit.limit(ip);
    return success;
  } catch {
    // Redis unavailable — DENY request (fail-closed) to prevent abuse during outage.
    // A fail-open policy would allow unlimited signups when Redis is down.
    console.error("Rate limiter unavailable — Redis connection failed. Blocking request.");
    return false;
  }
}

// -------------------------------------------------------------------
// Route Handler
// -------------------------------------------------------------------

export async function POST(req: NextRequest) {
  try {
    const body: SignupRequest = await req.json();
    const { email: rawEmail, referredBy, source } = body;

    // 1. Validate email
    const email = rawEmail?.toLowerCase().trim();
    if (!email || !isValidEmail(email)) {
      return NextResponse.json(
        { error: "Please enter a valid email address." },
        { status: 400 }
      );
    }

    // 2. Rate limit
    const ip = req.headers.get("x-forwarded-for")?.split(",")[0] || "unknown";
    if (!(await checkRateLimit(ip))) {
      return NextResponse.json(
        { error: "Too many signups. Please try again later." },
        { status: 429 }
      );
    }

    // 3. Validate referral code format (if provided) before any storage operations.
    //    Frontend validates via /^[a-zA-Z0-9_-]{6,16}$/ — backend must re-validate
    //    because attackers bypass frontends. Reject oversized/malformed values.
    const safeReferredBy =
      referredBy && /^[a-zA-Z0-9_-]{6,16}$/.test(referredBy) ? referredBy : null;

    // 4. Generate referral code
    const referralCode = generateReferralCode();

    // 5. Atomic dedup + create (prevents TOCTOU race on concurrent signups)
    //
    //    IMPORTANT: Do NOT use a check-then-create pattern (SISMEMBER → SADD).
    //    Two concurrent requests can both pass the check and create duplicates.
    //    Use the storage layer's atomic uniqueness enforcement instead.
    const user = {
      email,
      referralCode,
      referredBy: safeReferredBy,
      referralCount: 0,
      signupTime: Date.now(),
      source: source || null,
      ipHash: hashIp(ip),
    };

    // >>> REPLACE WITH YOUR STORAGE ADAPTER (pick one) <<<
    //
    // --- Redis: SADD returns 0 if the member already exists (atomic) ---
    // const added = await redis.sadd("waitlist:emails", email);
    // if (!added) {
    //   return NextResponse.json(
    //     { error: "This email is already on the waitlist." },
    //     { status: 409 }
    //   );
    // }
    // await redis.hset(`waitlist:user:${email}`, user);
    // await redis.set(`waitlist:ref:${referralCode}`, email);
    // await redis.incr("waitlist:count");
    //
    // --- Supabase/Postgres: INSERT with ON CONFLICT (atomic) ---
    // const { data, error } = await supabase
    //   .from("waitlist")
    //   .insert({
    //     email,
    //     referral_code: referralCode,
    //     referred_by: safeReferredBy,
    //     source: source || null,
    //     ip_hash: hashIp(ip),
    //   })
    //   .select("id")
    //   .single();
    // if (error?.code === "23505") {  // unique_violation
    //   return NextResponse.json(
    //     { error: "This email is already on the waitlist." },
    //     { status: 409 }
    //   );
    // }

    // 6. Credit referrer (if valid referral code)
    if (safeReferredBy) {
      // >>> REPLACE WITH YOUR STORAGE ADAPTER <<<
      // const referrerEmail = await redis.get(`waitlist:ref:${safeReferredBy}`);
      // if (referrerEmail) {
      //   await redis.hincrby(`waitlist:user:${referrerEmail}`, "referralCount", 1);
      //   await redis.sadd(`waitlist:referrals:${referrerEmail}`, email);
      // }
    }

    // 7. Calculate position and build response
    // >>> REPLACE: fetch all users from storage, run calculatePosition() <<<
    const totalWaiters = 1;  // placeholder
    const position = 1;      // placeholder

    // 8. Build leaderboard (top 10 by referral count)
    // >>> REPLACE: fetch top referrers from storage <<<
    const leaderboard: LeaderboardEntry[] = [];

    // 9. Send welcome email (async, don't block response)
    // >>> See Email Templates section below <<<
    // sendWelcomeEmail(email, referralCode, position, totalWaiters);

    const response: SignupResponse = {
      position,
      totalWaiters,
      referralCode,
      referralCount: 0,
      referralLink: `${BASE_URL}?ref=${referralCode}`,
      leaderboard,
    };

    return NextResponse.json(response, { status: 201 });
  } catch (err) {
    console.error("Waitlist signup error:", err);
    return NextResponse.json(
      { error: "Something went wrong. Please try again." },
      { status: 500 }
    );
  }
}
```

### GET /api/waitlist/status

> **Security note:** This endpoint requires both email AND referral code to prevent email
> enumeration attacks. An attacker cannot probe whether an email is on the waitlist without
> knowing the corresponding referral code (which is only sent to the user's inbox).

```typescript
// app/api/waitlist/status/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const email = req.nextUrl.searchParams.get("email")?.toLowerCase().trim();
  const code = req.nextUrl.searchParams.get("code")?.trim();

  if (!email || !code) {
    return NextResponse.json(
      { error: "Email and referral code required." },
      { status: 400 }
    );
  }

  // Rate limit status checks to prevent brute-force code guessing
  const ip = req.headers.get("x-forwarded-for")?.split(",")[0] || "unknown";
  if (!(await checkRateLimit(ip))) {
    return NextResponse.json(
      { error: "Too many requests. Please try again later." },
      { status: 429 }
    );
  }

  // >>> REPLACE WITH YOUR STORAGE ADAPTER <<<
  // const userData = await redis.hgetall(`waitlist:user:${email}`);
  // Verify the referral code matches the email — prevents enumeration
  // if (!userData || userData.referralCode !== code) {
  //   return NextResponse.json({ error: "Not found." }, { status: 404 });
  // }

  // >>> Calculate position, build leaderboard, return response <<<

  return NextResponse.json({
    position: 1,        // calculated
    totalWaiters: 1,    // from storage
    referralCode: "",   // from storage
    referralCount: 0,   // from storage
    referralLink: "",   // constructed
    leaderboard: [],    // top 10
  });
}
```

### GET /api/waitlist/count

```typescript
// app/api/waitlist/count/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  // >>> REPLACE WITH YOUR STORAGE ADAPTER <<<
  // const total = await redis.get("waitlist:count") || 0;

  return NextResponse.json({ total: 0 });
}
```

### POST /api/waitlist/export (Admin Only)

```typescript
// app/api/waitlist/export/route.ts
import { NextRequest, NextResponse } from "next/server";
import { timingSafeEqual } from "crypto";

const ADMIN_SECRET = process.env.WAITLIST_ADMIN_SECRET;

function verifyAdminAuth(req: NextRequest): boolean {
  const authHeader = req.headers.get("authorization");
  if (!authHeader?.startsWith("Bearer ") || !ADMIN_SECRET) return false;
  const token = authHeader.slice(7);
  // Timing-safe comparison prevents timing attacks on the secret
  try {
    return timingSafeEqual(
      Buffer.from(token, "utf-8"),
      Buffer.from(ADMIN_SECRET, "utf-8"),
    );
  } catch {
    return false; // length mismatch throws, treat as unauthorized
  }
}

export async function POST(req: NextRequest) {
  // Auth via Authorization header with timing-safe comparison
  if (!verifyAdminAuth(req)) {
    return NextResponse.json({ error: "Unauthorized." }, { status: 401 });
  }

  // >>> REPLACE WITH YOUR STORAGE ADAPTER <<<
  // Fetch all users, format as CSV

  const csv = "email,referral_code,referral_count,signup_time,referred_by,source,ip_hash\n";
  // ... append rows

  return new NextResponse(csv, {
    headers: {
      "Content-Type": "text/csv",
      "Content-Disposition": "attachment; filename=waitlist-export.csv",
    },
  });
}
```

---

## Vite / Remix / Astro Adaptation

### CORS Configuration

When the frontend and API are on different origins (common with Vite + separate backend),
configure CORS explicitly. **Never use `Access-Control-Allow-Origin: *` in production.**

```typescript
// Example: Hono CORS middleware
import { cors } from "hono/cors";

app.use("/api/*", cors({
  origin: process.env.ALLOWED_ORIGIN || "https://yourproduct.com",
  allowMethods: ["GET", "POST"],
  allowHeaders: ["Content-Type", "Authorization"],
  maxAge: 86400,
}));
```

| Framework | CORS Setup |
|-----------|-----------|
| **Vite + Hono** | `hono/cors` middleware (shown above) |
| **Vite + Express** | `cors` npm package with explicit origin |
| **Remix** | Headers in loader/action: `"Access-Control-Allow-Origin": ALLOWED_ORIGIN` |
| **Astro** | `src/middleware.ts` response headers or hosting config |
| **Next.js** | Same-origin by default — CORS only needed for cross-origin API consumers |

For non-Next.js frameworks, adapt the API routes:

**Vite (Express/Hono backend):**
```typescript
// server/routes/waitlist.ts
import { Hono } from "hono";
const app = new Hono();
app.post("/api/waitlist/signup", async (c) => { /* same logic */ });
app.get("/api/waitlist/status", async (c) => { /* same logic */ });
app.get("/api/waitlist/count", async (c) => { /* same logic */ });
export default app;
```

**Remix (action/loader):**
```typescript
// app/routes/api.waitlist.signup.tsx
export async function action({ request }: ActionFunctionArgs) {
  const body = await request.json();
  // same logic as Next.js route handler
}
```

**Astro (API endpoints):**
```typescript
// src/pages/api/waitlist/signup.ts
export async function POST({ request }: APIContext) {
  const body = await request.json();
  // same logic as Next.js route handler
}
```

---

## Email Templates

### Welcome Email (send immediately after signup)

```typescript
// lib/waitlist-emails.ts

interface WelcomeEmailData {
  email: string;
  position: number;
  totalWaiters: number;
  referralLink: string;
  productName: string;
}

// HTML-escape user-controlled strings before interpolation into email templates.
// Prevents HTML injection via productName or other user-supplied fields.
function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function buildWelcomeEmail(data: WelcomeEmailData): { subject: string; html: string } {
  const safeProductName = escapeHtml(data.productName);
  const safePosition = Number.isFinite(data.position) ? data.position : 0;
  const safeTotalWaiters = Number.isFinite(data.totalWaiters) ? data.totalWaiters : 0;

  return {
    subject: `You're #${safePosition} on the ${escapeHtml(data.productName)} waitlist`,
    html: `
      <div style="max-width:600px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1a1a2e;">
        <div style="padding:32px 24px;text-align:center;">
          <h1 style="font-size:28px;font-weight:700;margin:0 0 8px;">
            You're #${safePosition} in line
          </h1>
          <p style="font-size:16px;color:#64748b;margin:0 0 32px;">
            out of ${safeTotalWaiters.toLocaleString()} people waiting for ${safeProductName}
          </p>

          <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px;margin:0 0 24px;">
            <p style="font-size:14px;color:#64748b;margin:0 0 8px;">
              Want to skip the line? Share your personal link:
            </p>
            <a href="${encodeURI(data.referralLink)}"
               style="display:inline-block;background:#6366f1;color:white;font-size:14px;font-weight:600;
                      padding:12px 24px;border-radius:8px;text-decoration:none;margin:12px 0;">
              Share &amp; Move Up →
            </a>
            <p style="font-size:13px;color:#94a3b8;margin:12px 0 0;word-break:break-all;">
              ${escapeHtml(data.referralLink)}
            </p>
          </div>

          <div style="text-align:left;margin:24px 0;">
            <p style="font-size:14px;font-weight:600;margin:0 0 12px;">Unlock rewards:</p>
            <table style="width:100%;border-collapse:collapse;">
              <tr>
                <td style="padding:8px 0;font-size:14px;">⚡ 3 referrals</td>
                <td style="padding:8px 0;font-size:14px;color:#64748b;">Early access</td>
              </tr>
              <tr>
                <td style="padding:8px 0;font-size:14px;">✨ 5 referrals</td>
                <td style="padding:8px 0;font-size:14px;color:#64748b;">Beta features</td>
              </tr>
              <tr>
                <td style="padding:8px 0;font-size:14px;">👑 10 referrals</td>
                <td style="padding:8px 0;font-size:14px;color:#64748b;">Lifetime deal</td>
              </tr>
            </table>
          </div>

          <p style="font-size:13px;color:#94a3b8;margin:32px 0 0;">
            You're receiving this because you joined the ${safeProductName} waitlist.
          </p>
        </div>
      </div>
    `,
  };
}
```

### Email Service Integration

```typescript
// Send via Resend (recommended — free tier: 3,000 emails/mo)
import { Resend } from "resend";
const resend = new Resend(process.env.RESEND_API_KEY);

async function sendWelcomeEmail(data: WelcomeEmailData) {
  const { subject, html } = buildWelcomeEmail(data);
  await resend.emails.send({
    from: `${data.productName} <waitlist@yourdomain.com>`,
    to: data.email,
    subject,
    html,
  });
}

// Alternative: Nodemailer (any SMTP provider)
// Alternative: SendGrid, Mailgun, Postmark — same pattern
```

---

## Analytics & Metrics

The API should track and expose these metrics (via admin endpoint or dashboard):

| Metric | What It Measures | Formula |
|--------|-----------------|---------|
| **Total signups** | Overall demand | Count of all users |
| **Daily signups** | Growth velocity | Signups per day |
| **Referral rate** | % of signups from referrals | Referred signups / total signups |
| **Viral coefficient (k)** | Self-sustaining growth indicator | Avg referrals per user × conversion rate |
| **Top referrer** | Most influential advocate | User with highest referral count |
| **Source breakdown** | Where traffic comes from | Group by UTM source or referrer URL |
| **Reward tier distribution** | How many hit each milestone | Count users by referral count bracket |
| **Conversion funnel** | Page view → signup rate | Signups / unique page visits |

**Viral coefficient formula:**
```
k = (average invites sent per user) × (conversion rate of invited visitors)

k > 1.0 = viral growth (self-sustaining)
k = 0.5 - 1.0 = healthy referral program
k < 0.5 = referral program needs improvement
```

---

## Fraud Prevention

| Threat | Prevention |
|--------|-----------|
| **Duplicate emails** | Unique constraint on email in storage; case-insensitive comparison |
| **Bot signups** | Honeypot field (hidden input), rate limiting (5 per IP per hour) |
| **Self-referral** | Block signup if referral cookie matches signup email |
| **Disposable emails** | Block top 20 disposable email domains (mailinator, guerrillamail, etc.) |
| **Referral fraud** | Track IP of referrer and referred — flag if same IP refers > 3 signups |
| **Email harvesting** | Leaderboard shows anonymized emails only (s***h@gmail.com) |

---

## Environment Variables

```env
# Required
NEXT_PUBLIC_BASE_URL=https://yourproduct.com

# Storage (pick one)
KV_REST_API_URL=           # Vercel KV
KV_REST_API_TOKEN=         # Vercel KV
UPSTASH_REDIS_REST_URL=    # Upstash Redis
UPSTASH_REDIS_REST_TOKEN=  # Upstash Redis
SUPABASE_URL=              # Supabase
SUPABASE_ANON_KEY=         # Supabase

# Email (pick one)
RESEND_API_KEY=            # Resend (recommended)
SENDGRID_API_KEY=          # SendGrid
SMTP_HOST=                 # Generic SMTP
SMTP_PORT=
SMTP_USER=
SMTP_PASS=

# Admin
WAITLIST_ADMIN_SECRET=     # For export endpoint
```

---

## Quick Setup Checklist

```
1. [ ] Choose storage: Vercel KV, Upstash, Supabase, or JSON file
2. [ ] Set environment variables
3. [ ] Create API routes (copy from templates above)
4. [ ] Add Waitlist component to your page
5. [ ] Configure reward tiers for your product
6. [ ] Set up email sending (Resend recommended — free tier)
7. [ ] Test: signup → referral link → friend signup → position update
8. [ ] Verify: honeypot blocks bots, rate limiting works, duplicates rejected
```
