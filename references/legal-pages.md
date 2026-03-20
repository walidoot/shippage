# Legal Pages Generator

> Generates production-ready, jurisdiction-compliant legal page components for SaaS products.
> Replaces Termly ($10-35/mo), GetTerms ($5-8/mo), Iubenda ($3.49-119.99/mo),
> TermsFeed ($24-119 one-time), Enzuzo ($7-49/mo), PrivacyPolicies.com ($49-170 one-time).

---

## Why This Exists

Every SaaS footer links to `/privacy`, `/terms`, `/cookies` — but the pages are either:
- **Missing entirely** (most indie hackers skip them)
- **Copy-pasted from another site** (non-compliant, wrong business details)
- **Hosted on a third-party** (Termly/Iubenda embed = external dependency, branding, monthly cost)

This generator creates **actual React page components** with your business details filled in.
You own the code. Zero ongoing costs. No external dependencies. No branding to remove.

---

## Competitive Advantage Over Existing Tools

| Pain Point (from user reviews) | Competitors | Our Approach |
|-------------------------------|-------------|-------------|
| Deceptive "free" pricing | All 6 tools | Actually free — you own the generated code |
| Can't customize generated text | Termly, GetTerms, Enzuzo | It's your code — edit anything |
| External script/iframe dependency | Termly, Iubenda, GetTerms | Zero dependencies — static React components |
| Branding watermark on free tier | Termly, Iubenda, GetTerms | No branding ever |
| Manual re-embed after edits | Termly, TermsFeed | Edit source directly, redeploy |
| No DPA generator | ALL competitors (zero offer this) | Full DPA template included |
| No AUP generator | Only GetTerms has one | Full AUP template included |
| Auto-blocker breaks site | Termly, Iubenda | Cookie consent banner with easy whitelist |

---

## Intake Questions for Legal Pages

During page generation (Step 1), add these questions when legal pages are needed:

### Required Fields

| Field | Example | Used In |
|-------|---------|---------|
| `companyLegalName` | "Acme Inc." | All pages |
| `companyName` | "Acme" (brand name) | All pages |
| `companyEmail` | "privacy@acme.com" | Privacy, Terms |
| `companyAddress` | "123 Main St, San Francisco, CA 94102" | Privacy, Terms |
| `companyWebsite` | "https://acme.com" | All pages |
| `productName` | "Acme Analytics" | Terms, AUP |
| `productDescription` | "Real-time analytics for SaaS" | Terms |
| `lastUpdated` | "March 20, 2026" | All pages |

### Data Collection Fields (for Privacy Policy)

| Field | Type | Options |
|-------|------|---------|
| `dataCollected` | checklist | name, email, billing info, usage data, cookies, IP address, device info, location, user content |
| `dataCollectionMethods` | checklist | account registration, contact forms, payment processing, automatic collection (cookies/analytics), user-generated content |
| `thirdPartyServices` | checklist | Google Analytics, Stripe, PostHog, Sentry, Intercom, Mailchimp, AWS, Vercel, custom |
| `cookieTypes` | checklist | essential (session, auth), analytics (GA, PostHog), marketing (ads, retargeting), functional (preferences) |
| `internationalTransfers` | boolean | Does data leave the user's country? |
| `targetRegions` | checklist | US, EU/EEA, UK, Canada, Brazil, Australia, worldwide |
| `childrenUnder13` | boolean | Is the service directed at children? |
| `aiDataUsage` | boolean | Is user data shared with AI/ML services? |

### Business Model Fields (for Terms of Service)

| Field | Type | Options |
|-------|------|---------|
| `pricingModel` | select | free, freemium, subscription, usage-based, one-time |
| `hasFreeTrial` | boolean | Offers free trial? |
| `freeTrialDays` | number | 7, 14, 30 |
| `refundPolicy` | select | 30-day money-back, 14-day, pro-rata, no refunds |
| `autoRenewal` | boolean | Subscriptions auto-renew? |
| `userContentOwnership` | select | user-owns, license-to-provider, shared |
| `uptimeTarget` | select | none, 99.5%, 99.9%, 99.95%, 99.99% |

### Inference Rules (Quick Mode)

When user doesn't answer legal questions, infer from existing intake:

```
pricingModel → from CTA type (free-trial → freemium, purchase → subscription, waitlist → free)
targetRegions → worldwide (safe default)
dataCollected → [name, email, usage data, cookies, IP address, device info]
thirdPartyServices → [Google Analytics, Stripe] (most common SaaS stack)
cookieTypes → [essential, analytics]
childrenUnder13 → false
aiDataUsage → false
refundPolicy → 30-day money-back
autoRenewal → true
userContentOwnership → user-owns
```

---

## Generated Pages

The generator creates these page components:

| Page | Route | Legally Required? |
|------|-------|-------------------|
| Privacy Policy | `/privacy` | **YES** — GDPR, CCPA, PIPEDA, LGPD, CalOPPA |
| Terms of Service | `/terms` | No, but essential for SaaS |
| Cookie Policy | `/cookies` | **YES** (EU/UK) — ePrivacy Directive |
| Acceptable Use Policy | `/acceptable-use` | No, but recommended for SaaS |

All pages share the same layout component and design tokens as the landing page.

---

## Shared Layout Component

Every legal page uses this wrapper for consistent styling:

```tsx
"use client";

import { ArrowLeft } from "lucide-react";

interface LegalPageLayoutProps {
  title: string;
  lastUpdated: string;
  children: React.ReactNode;
  backHref?: string;
}

export default function LegalPageLayout({
  title,
  lastUpdated,
  children,
  backHref = "/",
}: LegalPageLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 py-6">
          <a
            href={backHref}
            className="inline-flex items-center gap-2 text-sm text-muted-foreground
                       hover:text-foreground transition-colors duration-200 mb-4"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to home
          </a>
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-foreground">
            {title}
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Last updated: {lastUpdated}
          </p>
        </div>
      </header>

      {/* Content */}
      <main className="mx-auto max-w-3xl px-4 sm:px-6 py-8 sm:py-12">
        <article
          className="prose prose-neutral dark:prose-invert max-w-none
                     prose-headings:scroll-mt-20
                     prose-h2:text-2xl prose-h2:font-semibold prose-h2:mt-10 prose-h2:mb-4
                     prose-h3:text-lg prose-h3:font-medium prose-h3:mt-8 prose-h3:mb-3
                     prose-p:text-base prose-p:leading-relaxed prose-p:text-muted-foreground
                     prose-li:text-muted-foreground
                     prose-a:text-primary prose-a:no-underline hover:prose-a:underline
                     prose-strong:text-foreground
                     prose-table:text-sm
                     prose-th:text-left prose-th:font-medium prose-th:text-foreground
                     prose-td:text-muted-foreground"
        >
          {children}
        </article>
      </main>

      {/* Footer */}
      <footer className="border-t border-border">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 py-6 text-center">
          <p className="text-xs text-muted-foreground">
            &copy; {new Date().getFullYear()}{" "}
            <a href={backHref} className="hover:text-foreground transition-colors">
              {/* companyName inserted here */}
            </a>
            . All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
```

---

## Page 1: Privacy Policy

### Compliance Coverage

This template covers mandatory requirements for:

| Law | Jurisdiction | Key Requirement |
|-----|-------------|-----------------|
| GDPR (Articles 13-14) | EU/EEA | 12 mandatory disclosures, lawful basis, DPO contact |
| UK GDPR | United Kingdom | Same as GDPR with UK-specific supervisory authority |
| CCPA/CPRA | California, USA | 12-month retrospective lists, "Do Not Sell" link, SPI categories |
| CalOPPA | California, USA | Conspicuous posting, Do Not Track disclosure |
| COPPA | USA (children) | Parental consent, children under 13 |
| PIPEDA | Canada | 10 fair information principles, privacy officer |
| LGPD | Brazil | 10 legal bases, right to anonymization, 15-day response |
| Australia Privacy Act | Australia | 13 Australian Privacy Principles |
| US State Laws | VA, CO, CT, DE, 11+ states | Opt-out rights, data minimization |

### Section Structure

Generate these sections in order:

1. **Introduction** — who we are, what this policy covers
2. **Information We Collect** — categorized table (personal, usage, device, payment)
3. **How We Collect Information** — direct, automatic, third-party sources
4. **How We Use Your Information** — purposes with lawful basis (GDPR requirement)
5. **How We Share Your Information** — third-party services table with purpose
6. **Cookies and Tracking** — types, link to cookie policy
7. **Data Retention** — how long, criteria for determining
8. **Your Privacy Rights** — by jurisdiction (GDPR, CCPA, PIPEDA, LGPD)
9. **International Data Transfers** — safeguards, SCCs
10. **Children's Privacy** — COPPA compliance
11. **AI and Automated Processing** — if applicable
12. **Security Measures** — encryption, access controls
13. **Changes to This Policy** — notification process
14. **Contact Us** — privacy contact, DPO if applicable

### Complete JSX Template

```tsx
import LegalPageLayout from "@/components/legal-page-layout";

// -------------------------------------------------------------------
// Types — fill these from intake questionnaire
// -------------------------------------------------------------------

interface PrivacyPolicyConfig {
  companyLegalName: string;
  companyName: string;
  companyEmail: string;
  companyAddress: string;
  companyWebsite: string;
  productName: string;
  lastUpdated: string;
  dpoEmail?: string;
  dataCollected: {
    category: string;
    items: string[];
    purpose: string;
    lawfulBasis: string; // GDPR requirement
  }[];
  thirdPartyServices: {
    name: string;
    purpose: string;
    dataShared: string;
    privacyPolicyUrl: string;
  }[];
  cookieTypes: {
    category: string;
    purpose: string;
    duration: string;
    examples: string;
  }[];
  retentionPeriod: string;
  targetRegions: string[];
  childrenUnder13: boolean;
  aiDataUsage: boolean;
  hasFreeTrial: boolean;
}

// -------------------------------------------------------------------
// Default configuration (replace with user's actual data)
// -------------------------------------------------------------------

const defaultConfig: PrivacyPolicyConfig = {
  companyLegalName: "YourCompany Inc.",
  companyName: "YourProduct",
  companyEmail: "privacy@yourproduct.com",
  companyAddress: "123 Main Street, City, State, Country",
  companyWebsite: "https://yourproduct.com",
  productName: "YourProduct",
  lastUpdated: "March 20, 2026",
  dataCollected: [
    {
      category: "Account Information",
      items: ["Name", "Email address", "Password (hashed)"],
      purpose: "Account creation and authentication",
      lawfulBasis: "Performance of contract",
    },
    {
      category: "Billing Information",
      items: ["Payment method", "Billing address", "Transaction history"],
      purpose: "Payment processing and invoicing",
      lawfulBasis: "Performance of contract",
    },
    {
      category: "Usage Data",
      items: [
        "Pages visited",
        "Features used",
        "Time spent",
        "Click patterns",
      ],
      purpose: "Product improvement and analytics",
      lawfulBasis: "Legitimate interest",
    },
    {
      category: "Device Information",
      items: [
        "IP address",
        "Browser type",
        "Operating system",
        "Device identifier",
      ],
      purpose: "Security, fraud prevention, and troubleshooting",
      lawfulBasis: "Legitimate interest",
    },
  ],
  thirdPartyServices: [
    {
      name: "Stripe",
      purpose: "Payment processing",
      dataShared: "Billing information, transaction details",
      privacyPolicyUrl: "https://stripe.com/privacy",
    },
    {
      name: "Google Analytics",
      purpose: "Website analytics",
      dataShared: "Usage data, device information, IP address",
      privacyPolicyUrl: "https://policies.google.com/privacy",
    },
  ],
  cookieTypes: [
    {
      category: "Essential",
      purpose: "Authentication, security, core functionality",
      duration: "Session to 1 year",
      examples: "Session cookies, CSRF tokens",
    },
    {
      category: "Analytics",
      purpose: "Understanding how visitors use the site",
      duration: "Up to 2 years",
      examples: "Google Analytics (_ga, _gid)",
    },
  ],
  retentionPeriod:
    "We retain your personal data for as long as your account is active or as needed to provide you with our services. After account deletion, we retain data for up to 90 days for backup and fraud prevention purposes, unless a longer retention period is required by law.",
  targetRegions: ["US", "EU", "UK", "Canada"],
  childrenUnder13: false,
  aiDataUsage: false,
  hasFreeTrial: true,
};

// -------------------------------------------------------------------
// Component
// -------------------------------------------------------------------

export default function PrivacyPolicy({
  config = defaultConfig,
}: {
  config?: PrivacyPolicyConfig;
}) {
  return (
    <LegalPageLayout title="Privacy Policy" lastUpdated={config.lastUpdated}>
      {/* ---- 1. Introduction ---- */}
      <section>
        <h2 id="introduction">Introduction</h2>
        <p>
          {config.companyLegalName} (&quot;{config.companyName},&quot;
          &quot;we,&quot; &quot;us,&quot; or &quot;our&quot;) operates{" "}
          {config.productName} (the &quot;Service&quot;). This Privacy Policy
          explains how we collect, use, disclose, and safeguard your personal
          information when you visit our website at{" "}
          <a href={config.companyWebsite}>{config.companyWebsite}</a> or use our
          Service.
        </p>
        <p>
          By using the Service, you agree to the collection and use of
          information in accordance with this policy. If you do not agree with
          any part of this policy, please do not use our Service.
        </p>
      </section>

      {/* ---- 2. Information We Collect ---- */}
      <section>
        <h2 id="information-we-collect">Information We Collect</h2>
        <p>
          We collect information that you provide directly, information collected
          automatically, and information from third-party sources.
        </p>

        <table>
          <thead>
            <tr>
              <th>Category</th>
              <th>Data Collected</th>
              <th>Purpose</th>
              <th>Legal Basis (GDPR)</th>
            </tr>
          </thead>
          <tbody>
            {config.dataCollected.map((category) => (
              <tr key={category.category}>
                <td>
                  <strong>{category.category}</strong>
                </td>
                <td>{category.items.join(", ")}</td>
                <td>{category.purpose}</td>
                <td>{category.lawfulBasis}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* ---- 3. How We Collect Information ---- */}
      <section>
        <h2 id="how-we-collect">How We Collect Information</h2>
        <h3>Information You Provide</h3>
        <p>
          We collect information you voluntarily provide when you create an
          account, make a purchase, contact our support team, or otherwise
          interact with the Service.
        </p>

        <h3>Information Collected Automatically</h3>
        <p>
          When you access the Service, we automatically collect certain
          technical data including your IP address, browser type, operating
          system, referring URLs, pages viewed, and the dates and times of your
          visits. We use cookies and similar tracking technologies to collect
          this information. See our{" "}
          <a href="/cookies">Cookie Policy</a> for details.
        </p>

        <h3>Information from Third Parties</h3>
        <p>
          We may receive information about you from third-party services you
          connect to your account (such as single sign-on providers) and from
          our analytics and payment processing partners.
        </p>
      </section>

      {/* ---- 4. How We Use Your Information ---- */}
      <section>
        <h2 id="how-we-use">How We Use Your Information</h2>
        <p>We use the information we collect to:</p>
        <ul>
          <li>
            <strong>Provide and maintain the Service</strong> — including
            account management, payment processing, and customer support
          </li>
          <li>
            <strong>Improve the Service</strong> — analyzing usage patterns to
            fix bugs, develop new features, and improve user experience
          </li>
          <li>
            <strong>Communicate with you</strong> — sending transactional
            emails, product updates, and responding to inquiries
          </li>
          <li>
            <strong>Ensure security</strong> — detecting and preventing fraud,
            abuse, and unauthorized access
          </li>
          <li>
            <strong>Comply with legal obligations</strong> — meeting regulatory
            requirements and responding to legal requests
          </li>
          {config.aiDataUsage && (
            <li>
              <strong>AI and machine learning</strong> — improving our
              AI-powered features using aggregated, anonymized usage data. We do
              not use your personal data or private content to train AI models
              without your explicit consent.
            </li>
          )}
        </ul>
      </section>

      {/* ---- 5. How We Share Your Information ---- */}
      <section>
        <h2 id="sharing">How We Share Your Information</h2>
        <p>
          We do not sell your personal information. We share your data only with
          the following categories of service providers, and only to the extent
          necessary to operate the Service:
        </p>

        <table>
          <thead>
            <tr>
              <th>Service Provider</th>
              <th>Purpose</th>
              <th>Data Shared</th>
              <th>Privacy Policy</th>
            </tr>
          </thead>
          <tbody>
            {config.thirdPartyServices.map((service) => (
              <tr key={service.name}>
                <td>
                  <strong>{service.name}</strong>
                </td>
                <td>{service.purpose}</td>
                <td>{service.dataShared}</td>
                <td>
                  <a
                    href={service.privacyPolicyUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View Policy
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <p>We may also share your information:</p>
        <ul>
          <li>When required by law, regulation, or legal process</li>
          <li>To protect the rights, property, or safety of our users or others</li>
          <li>
            In connection with a merger, acquisition, or sale of assets (you
            will be notified)
          </li>
          <li>With your consent or at your direction</li>
        </ul>
      </section>

      {/* ---- 6. Cookies ---- */}
      <section>
        <h2 id="cookies">Cookies and Tracking Technologies</h2>
        <p>
          We use cookies and similar tracking technologies to collect and store
          information. Cookies are small data files stored on your device.
        </p>

        <table>
          <thead>
            <tr>
              <th>Category</th>
              <th>Purpose</th>
              <th>Duration</th>
              <th>Examples</th>
            </tr>
          </thead>
          <tbody>
            {config.cookieTypes.map((cookie) => (
              <tr key={cookie.category}>
                <td>
                  <strong>{cookie.category}</strong>
                </td>
                <td>{cookie.purpose}</td>
                <td>{cookie.duration}</td>
                <td>{cookie.examples}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <p>
          You can control cookies through your browser settings. Disabling
          certain cookies may affect the functionality of the Service. For
          detailed information, see our <a href="/cookies">Cookie Policy</a>.
        </p>
      </section>

      {/* ---- 7. Data Retention ---- */}
      <section>
        <h2 id="retention">Data Retention</h2>
        <p>{config.retentionPeriod}</p>
      </section>

      {/* ---- 8. Your Privacy Rights ---- */}
      <section>
        <h2 id="your-rights">Your Privacy Rights</h2>

        {/* GDPR Rights */}
        {(config.targetRegions.includes("EU") ||
          config.targetRegions.includes("UK")) && (
          <>
            <h3>European Economic Area and United Kingdom (GDPR / UK GDPR)</h3>
            <p>
              If you are in the EEA or UK, you have the following rights under
              the General Data Protection Regulation:
            </p>
            <ul>
              <li>
                <strong>Right of access</strong> — request a copy of your
                personal data
              </li>
              <li>
                <strong>Right to rectification</strong> — request correction of
                inaccurate data
              </li>
              <li>
                <strong>Right to erasure</strong> — request deletion of your
                data (&quot;right to be forgotten&quot;)
              </li>
              <li>
                <strong>Right to restrict processing</strong> — request
                limitation of how we use your data
              </li>
              <li>
                <strong>Right to data portability</strong> — receive your data
                in a structured, machine-readable format
              </li>
              <li>
                <strong>Right to object</strong> — object to processing based on
                legitimate interest
              </li>
              <li>
                <strong>Right to withdraw consent</strong> — withdraw consent at
                any time where consent is the legal basis
              </li>
              <li>
                <strong>Right to lodge a complaint</strong> — file a complaint
                with your local data protection authority
              </li>
            </ul>
            <p>
              We will respond to your request within 30 days. To exercise these
              rights, contact us at{" "}
              <a href={`mailto:${config.companyEmail}`}>
                {config.companyEmail}
              </a>
              .
            </p>
          </>
        )}

        {/* CCPA/CPRA Rights */}
        {config.targetRegions.includes("US") && (
          <>
            <h3>California (CCPA / CPRA)</h3>
            <p>
              If you are a California resident, you have the following rights
              under the California Consumer Privacy Act and the California
              Privacy Rights Act:
            </p>
            <ul>
              <li>
                <strong>Right to know</strong> — request disclosure of the
                categories and specific pieces of personal information collected
                about you in the prior 12 months
              </li>
              <li>
                <strong>Right to delete</strong> — request deletion of your
                personal information
              </li>
              <li>
                <strong>Right to correct</strong> — request correction of
                inaccurate personal information
              </li>
              <li>
                <strong>Right to opt out</strong> — opt out of the sale or
                sharing of your personal information
              </li>
              <li>
                <strong>Right to limit use of sensitive personal information</strong>{" "}
                — restrict processing of sensitive categories
              </li>
              <li>
                <strong>Right to non-discrimination</strong> — we will not
                discriminate against you for exercising your rights
              </li>
            </ul>
            <p>
              <strong>We do not sell your personal information.</strong> We do
              not use or disclose sensitive personal information for purposes
              other than those authorized by the CCPA/CPRA.
            </p>
            <p>
              <strong>Categories collected in the prior 12 months:</strong>{" "}
              Identifiers (name, email), commercial information (transaction
              records), internet activity (usage data, browsing history),
              geolocation data (IP-derived).
            </p>
          </>
        )}

        {/* PIPEDA Rights */}
        {config.targetRegions.includes("Canada") && (
          <>
            <h3>Canada (PIPEDA)</h3>
            <p>
              If you are a Canadian resident, the Personal Information
              Protection and Electronic Documents Act gives you the right to:
            </p>
            <ul>
              <li>Access your personal information held by us</li>
              <li>Challenge the accuracy and completeness of your data</li>
              <li>Withdraw consent for certain data processing</li>
              <li>File a complaint with the Office of the Privacy Commissioner of Canada</li>
            </ul>
          </>
        )}

        {/* LGPD Rights */}
        {config.targetRegions.includes("Brazil") && (
          <>
            <h3>Brazil (LGPD)</h3>
            <p>
              If you are a Brazilian resident, the Lei Geral de Proteção de
              Dados gives you the following rights:
            </p>
            <ul>
              <li>Confirmation of data processing and access to your data</li>
              <li>Correction of incomplete, inaccurate, or outdated data</li>
              <li>Anonymization, blocking, or deletion of unnecessary data</li>
              <li>Data portability to another service provider</li>
              <li>Deletion of data processed with consent</li>
              <li>Information about public and private entities with which data is shared</li>
              <li>Information about the possibility of denying consent and its consequences</li>
              <li>Revocation of consent</li>
            </ul>
            <p>We will respond to your request within 15 days.</p>
          </>
        )}

        <h3>Exercising Your Rights</h3>
        <p>
          To exercise any of these rights, contact us at{" "}
          <a href={`mailto:${config.companyEmail}`}>{config.companyEmail}</a>.
          We may need to verify your identity before processing your request. We
          will respond within the timeframe required by applicable law.
        </p>
      </section>

      {/* ---- 9. International Transfers ---- */}
      {config.targetRegions.length > 1 && (
        <section>
          <h2 id="international-transfers">International Data Transfers</h2>
          <p>
            Your information may be transferred to and processed in countries
            other than your country of residence. These countries may have
            different data protection laws.
          </p>
          <p>
            When we transfer personal data outside the EEA or UK, we ensure
            appropriate safeguards are in place, including:
          </p>
          <ul>
            <li>
              Standard Contractual Clauses (SCCs) approved by the European
              Commission
            </li>
            <li>
              Transfers to countries with an adequacy decision from the European
              Commission
            </li>
            <li>
              Other legally approved transfer mechanisms
            </li>
          </ul>
        </section>
      )}

      {/* ---- 10. Children's Privacy ---- */}
      <section>
        <h2 id="children">Children&apos;s Privacy</h2>
        {config.childrenUnder13 ? (
          <p>
            Portions of our Service may be directed at children under 13. We
            comply with the Children&apos;s Online Privacy Protection Act
            (COPPA). We obtain verifiable parental consent before collecting
            personal information from children under 13. Parents can review,
            delete, or refuse further collection of their child&apos;s
            information by contacting us at{" "}
            <a href={`mailto:${config.companyEmail}`}>
              {config.companyEmail}
            </a>
            .
          </p>
        ) : (
          <p>
            Our Service is not directed at children under 13. We do not
            knowingly collect personal information from children under 13. If
            you believe we have collected data from a child under 13, please
            contact us at{" "}
            <a href={`mailto:${config.companyEmail}`}>
              {config.companyEmail}
            </a>{" "}
            and we will promptly delete the information.
          </p>
        )}
      </section>

      {/* ---- 11. AI Processing ---- */}
      {config.aiDataUsage && (
        <section>
          <h2 id="ai-processing">AI and Automated Processing</h2>
          <p>
            Our Service uses artificial intelligence and machine learning to
            provide certain features. We want you to know:
          </p>
          <ul>
            <li>
              We use aggregated, anonymized data to improve our AI models. Your
              personal data is not used for AI training without your explicit
              consent.
            </li>
            <li>
              Automated decisions that significantly affect you will include an
              option for human review.
            </li>
            <li>
              You have the right to opt out of automated decision-making under
              GDPR Article 22.
            </li>
          </ul>
        </section>
      )}

      {/* ---- 12. Security ---- */}
      <section>
        <h2 id="security">Security Measures</h2>
        <p>
          We implement appropriate technical and organizational measures to
          protect your personal data, including:
        </p>
        <ul>
          <li>Encryption in transit (TLS 1.2+) and at rest (AES-256)</li>
          <li>Access controls and authentication requirements</li>
          <li>Regular security assessments and monitoring</li>
          <li>Employee training on data protection</li>
          <li>Incident response procedures</li>
        </ul>
        <p>
          No method of transmission or storage is 100% secure. While we strive
          to use commercially acceptable means to protect your data, we cannot
          guarantee absolute security.
        </p>
      </section>

      {/* ---- 13. Changes ---- */}
      <section>
        <h2 id="changes">Changes to This Privacy Policy</h2>
        <p>
          We may update this Privacy Policy from time to time. We will notify
          you of any material changes by posting the new policy on this page and
          updating the &quot;Last updated&quot; date. For significant changes, we
          will provide additional notice via email or an in-app notification.
        </p>
        <p>
          We encourage you to review this Privacy Policy periodically for any
          changes. Your continued use of the Service after changes are posted
          constitutes your acceptance of the updated policy.
        </p>
      </section>

      {/* ---- 14. Contact ---- */}
      <section>
        <h2 id="contact">Contact Us</h2>
        <p>
          If you have any questions about this Privacy Policy or our data
          practices, please contact us:
        </p>
        <ul>
          <li>
            <strong>Email:</strong>{" "}
            <a href={`mailto:${config.companyEmail}`}>
              {config.companyEmail}
            </a>
          </li>
          <li>
            <strong>Address:</strong> {config.companyAddress}
          </li>
          {config.dpoEmail && (
            <li>
              <strong>Data Protection Officer:</strong>{" "}
              <a href={`mailto:${config.dpoEmail}`}>{config.dpoEmail}</a>
            </li>
          )}
        </ul>
        {(config.targetRegions.includes("EU") ||
          config.targetRegions.includes("UK")) && (
          <p>
            If you are in the EU/EEA, you have the right to lodge a complaint
            with your local data protection authority. A list of EU data
            protection authorities is available at{" "}
            <a
              href="https://edpb.europa.eu/about-edpb/about-edpb/members_en"
              target="_blank"
              rel="noopener noreferrer"
            >
              edpb.europa.eu
            </a>
            .
          </p>
        )}
      </section>
    </LegalPageLayout>
  );
}
```

---

## Page 2: Terms of Service

### Section Structure

1. **Agreement to Terms** — binding terms, effective date
2. **Description of Service** — what the product does
3. **Account Registration** — requirements, responsibilities
4. **Subscription and Billing** — pricing model, payment terms, auto-renewal
5. **Free Trial** — if applicable, terms
6. **Cancellation and Refunds** — refund policy, data after cancellation
7. **Acceptable Use** — brief version (or link to full AUP)
8. **Intellectual Property** — who owns what
9. **User Content** — user-generated content ownership and license
10. **Service Availability and SLA** — uptime target, maintenance windows
11. **Limitation of Liability** — caps, exclusions
12. **Indemnification** — user indemnifies provider
13. **Termination** — when we can terminate, data export
14. **Dispute Resolution** — governing law, jurisdiction, arbitration
15. **Changes to Terms** — notification process
16. **Contact** — how to reach us

### Complete JSX Template

```tsx
import LegalPageLayout from "@/components/legal-page-layout";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

interface TermsConfig {
  companyLegalName: string;
  companyName: string;
  companyEmail: string;
  companyAddress: string;
  companyWebsite: string;
  productName: string;
  productDescription: string;
  lastUpdated: string;
  governingLaw: string; // e.g., "State of Delaware, United States"
  pricingModel: "free" | "freemium" | "subscription" | "usage-based" | "one-time";
  hasFreeTrial: boolean;
  freeTrialDays: number;
  refundPolicy: "30-day" | "14-day" | "pro-rata" | "no-refunds";
  autoRenewal: boolean;
  userContentOwnership: "user-owns" | "license-to-provider" | "shared";
  uptimeTarget: string; // e.g., "99.9%"
  liabilityCap: string; // e.g., "12 months of fees paid"
}

// -------------------------------------------------------------------
// Defaults
// -------------------------------------------------------------------

const defaultConfig: TermsConfig = {
  companyLegalName: "YourCompany Inc.",
  companyName: "YourProduct",
  companyEmail: "legal@yourproduct.com",
  companyAddress: "123 Main Street, City, State, Country",
  companyWebsite: "https://yourproduct.com",
  productName: "YourProduct",
  productDescription: "a software-as-a-service platform",
  lastUpdated: "March 20, 2026",
  governingLaw: "State of Delaware, United States",
  pricingModel: "subscription",
  hasFreeTrial: true,
  freeTrialDays: 14,
  refundPolicy: "30-day",
  autoRenewal: true,
  userContentOwnership: "user-owns",
  uptimeTarget: "99.9%",
  liabilityCap: "the total fees paid by you in the 12 months preceding the claim",
};

// -------------------------------------------------------------------
// Component
// -------------------------------------------------------------------

export default function TermsOfService({
  config = defaultConfig,
}: {
  config?: TermsConfig;
}) {
  const refundText = {
    "30-day":
      "If you are not satisfied with the Service, you may request a full refund within 30 days of your initial purchase. No questions asked.",
    "14-day":
      "You may request a full refund within 14 days of your initial purchase.",
    "pro-rata":
      "If you cancel mid-cycle, you will receive a pro-rated refund for the unused portion of your current billing period.",
    "no-refunds":
      "All fees are non-refundable except as required by applicable law.",
  };

  return (
    <LegalPageLayout title="Terms of Service" lastUpdated={config.lastUpdated}>
      {/* 1. Agreement */}
      <section>
        <h2 id="agreement">Agreement to Terms</h2>
        <p>
          These Terms of Service (&quot;Terms&quot;) constitute a legally
          binding agreement between you (&quot;you&quot; or &quot;your&quot;) and{" "}
          {config.companyLegalName} (&quot;{config.companyName},&quot;
          &quot;we,&quot; &quot;us,&quot; or &quot;our&quot;) governing your
          access to and use of {config.productName} (the &quot;Service&quot;).
        </p>
        <p>
          By creating an account or using the Service, you agree to be bound by
          these Terms. If you do not agree to these Terms, do not use the
          Service.
        </p>
      </section>

      {/* 2. Description */}
      <section>
        <h2 id="service">Description of Service</h2>
        <p>
          {config.productName} is {config.productDescription}. We reserve the
          right to modify, suspend, or discontinue any part of the Service at
          any time with reasonable notice.
        </p>
      </section>

      {/* 3. Accounts */}
      <section>
        <h2 id="accounts">Account Registration</h2>
        <p>To use the Service, you must:</p>
        <ul>
          <li>Be at least 18 years old (or the age of majority in your jurisdiction)</li>
          <li>Provide accurate and complete registration information</li>
          <li>Maintain the security of your account credentials</li>
          <li>Notify us immediately of any unauthorized access to your account</li>
        </ul>
        <p>
          You are responsible for all activity that occurs under your account.
          We are not liable for any loss or damage arising from unauthorized
          use of your account.
        </p>
      </section>

      {/* 4. Billing */}
      {config.pricingModel !== "free" && (
        <section>
          <h2 id="billing">Subscription and Billing</h2>
          {config.pricingModel === "subscription" && (
            <>
              <p>
                The Service is billed on a recurring{" "}
                {config.autoRenewal ? "auto-renewing" : ""} subscription basis.
                You agree to pay all fees associated with your selected plan.
              </p>
              {config.autoRenewal && (
                <p>
                  <strong>Auto-renewal:</strong> Your subscription will
                  automatically renew at the end of each billing period unless
                  you cancel before the renewal date. We will charge the
                  payment method on file. You can cancel auto-renewal at any
                  time from your account settings.
                </p>
              )}
              <p>
                <strong>Price changes:</strong> We may change our prices with
                at least 30 days&apos; notice before the start of your next
                billing period. Continued use after the price change constitutes
                acceptance of the new price.
              </p>
            </>
          )}
          {config.pricingModel === "usage-based" && (
            <p>
              Fees are calculated based on your usage of the Service during each
              billing period. Usage details and pricing are available on your
              account dashboard and at{" "}
              <a href={`${config.companyWebsite}/pricing`}>our pricing page</a>.
            </p>
          )}
          <p>
            <strong>Late payments:</strong> Overdue amounts may accrue interest
            at 1.5% per month (or the maximum rate permitted by law). We may
            suspend your access to the Service for accounts with overdue
            balances exceeding 15 days.
          </p>
        </section>
      )}

      {/* 5. Free Trial */}
      {config.hasFreeTrial && (
        <section>
          <h2 id="free-trial">Free Trial</h2>
          <p>
            We offer a {config.freeTrialDays}-day free trial. During the trial,
            you have access to the full features of the Service at no cost. No
            credit card is required to start a trial.
          </p>
          <p>
            At the end of your trial period, you may choose a paid plan to
            continue using the Service. If you do not select a plan, your
            access to paid features will be restricted.
          </p>
        </section>
      )}

      {/* 6. Cancellation and Refunds */}
      <section>
        <h2 id="cancellation">Cancellation and Refunds</h2>
        <p>
          You may cancel your subscription at any time from your account
          settings. Upon cancellation:
        </p>
        <ul>
          <li>
            Your access continues until the end of your current billing period
          </li>
          <li>
            You can export your data for 30 days after the end of your billing
            period
          </li>
          <li>
            After the export window, your data will be permanently deleted
          </li>
        </ul>
        <p>
          <strong>Refunds:</strong> {refundText[config.refundPolicy]}
        </p>
      </section>

      {/* 7. Acceptable Use */}
      <section>
        <h2 id="acceptable-use">Acceptable Use</h2>
        <p>You agree not to:</p>
        <ul>
          <li>
            Use the Service for any illegal purpose or in violation of any applicable law
          </li>
          <li>
            Reverse engineer, decompile, or disassemble any part of the Service
          </li>
          <li>
            Attempt to gain unauthorized access to the Service or its related systems
          </li>
          <li>
            Interfere with or disrupt the integrity or performance of the
            Service
          </li>
          <li>
            Use the Service to send spam, malware, or unsolicited
            communications
          </li>
          <li>
            Use the Service to collect data about other users without their
            consent
          </li>
          <li>
            Use the Service for competitive benchmarking or to build a
            competing product
          </li>
          <li>
            Share your account credentials with unauthorized third parties
          </li>
        </ul>
        <p>
          Violation of these terms may result in immediate suspension or
          termination of your account.
        </p>
      </section>

      {/* 8. Intellectual Property */}
      <section>
        <h2 id="intellectual-property">Intellectual Property</h2>
        <p>
          The Service, including its original content, features, and
          functionality, is owned by {config.companyLegalName} and is protected
          by copyright, trademark, and other intellectual property laws.
        </p>
        <p>
          We grant you a limited, non-exclusive, non-transferable,
          non-sublicensable license to access and use the Service for your
          internal business purposes during your subscription term.
        </p>
      </section>

      {/* 9. User Content */}
      <section>
        <h2 id="user-content">User Content</h2>
        {config.userContentOwnership === "user-owns" && (
          <>
            <p>
              <strong>You retain full ownership of all data and content you
              upload to the Service</strong> (&quot;User Content&quot;). We do
              not claim any ownership rights to your User Content.
            </p>
            <p>
              By uploading User Content, you grant us a limited license to
              host, store, process, and display your content solely to
              provide the Service to you. This license terminates when you
              delete your content or close your account.
            </p>
          </>
        )}
        <p>
          You represent that you own or have the necessary rights to all User
          Content you upload, and that your content does not violate any
          third-party rights.
        </p>
      </section>

      {/* 10. SLA */}
      {config.uptimeTarget !== "none" && (
        <section>
          <h2 id="availability">Service Availability</h2>
          <p>
            We target {config.uptimeTarget}% uptime for the Service, measured on
            a monthly basis. This excludes scheduled maintenance, which we
            will announce with at least 24 hours&apos; notice when possible.
          </p>
          <p>
            If we fail to meet this target, you may be eligible for service
            credits. Contact us at{" "}
            <a href={`mailto:${config.companyEmail}`}>{config.companyEmail}</a>{" "}
            to request credits.
          </p>
        </section>
      )}

      {/* 11. Liability */}
      <section>
        <h2 id="liability">Limitation of Liability</h2>
        <p>
          TO THE MAXIMUM EXTENT PERMITTED BY LAW, {config.companyName.toUpperCase()}{" "}
          SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL,
          CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO LOSS
          OF PROFITS, DATA, OR BUSINESS OPPORTUNITIES.
        </p>
        <p>
          OUR TOTAL LIABILITY FOR ALL CLAIMS ARISING FROM OR RELATING TO THESE
          TERMS OR THE SERVICE SHALL NOT EXCEED {config.liabilityCap.toUpperCase()}.
        </p>
        <p>
          Some jurisdictions do not allow the exclusion or limitation of
          certain damages. In such jurisdictions, our liability is limited to
          the maximum extent permitted by law.
        </p>
      </section>

      {/* 12. Indemnification */}
      <section>
        <h2 id="indemnification">Indemnification</h2>
        <p>
          You agree to indemnify and hold harmless {config.companyLegalName},
          its officers, directors, employees, and agents from any claims,
          damages, losses, or expenses (including reasonable attorneys&apos;
          fees) arising from your use of the Service, your violation of these
          Terms, or your violation of any rights of a third party.
        </p>
      </section>

      {/* 13. Termination */}
      <section>
        <h2 id="termination">Termination</h2>
        <p>
          We may suspend or terminate your access to the Service immediately,
          without prior notice, if you:
        </p>
        <ul>
          <li>Violate these Terms or our Acceptable Use Policy</li>
          <li>Engage in any activity that threatens the security of the Service</li>
          <li>Fail to pay fees when due (after a 15-day grace period)</li>
        </ul>
        <p>
          Upon termination, your right to use the Service ceases immediately.
          You may request export of your data within 30 days of termination.
        </p>
      </section>

      {/* 14. Dispute Resolution */}
      <section>
        <h2 id="dispute-resolution">Dispute Resolution</h2>
        <p>
          These Terms are governed by the laws of the {config.governingLaw},
          without regard to conflict of law principles.
        </p>
        <p>
          Any dispute arising from these Terms will first be resolved through
          good-faith negotiation. If negotiation fails within 30 days, either
          party may pursue binding arbitration or file a claim in the courts
          of the {config.governingLaw}.
        </p>
      </section>

      {/* 15. Changes */}
      <section>
        <h2 id="changes">Changes to These Terms</h2>
        <p>
          We may update these Terms from time to time. We will provide at least
          30 days&apos; notice of material changes via email or an in-app
          notification. Continued use of the Service after the effective date of
          changes constitutes your acceptance of the updated Terms.
        </p>
      </section>

      {/* 16. Contact */}
      <section>
        <h2 id="contact">Contact Us</h2>
        <p>
          If you have questions about these Terms, contact us at{" "}
          <a href={`mailto:${config.companyEmail}`}>{config.companyEmail}</a>.
        </p>
        <ul>
          <li>
            <strong>Email:</strong>{" "}
            <a href={`mailto:${config.companyEmail}`}>{config.companyEmail}</a>
          </li>
          <li>
            <strong>Address:</strong> {config.companyAddress}
          </li>
        </ul>
      </section>
    </LegalPageLayout>
  );
}
```

---

## Page 3: Cookie Policy

### Complete JSX Template

```tsx
import LegalPageLayout from "@/components/legal-page-layout";

// -------------------------------------------------------------------
// Types
// -------------------------------------------------------------------

interface CookiePolicyConfig {
  companyLegalName: string;
  companyName: string;
  companyEmail: string;
  companyWebsite: string;
  lastUpdated: string;
  cookieTypes: {
    category: string;
    name: string;
    provider: string;
    purpose: string;
    duration: string;
    type: "essential" | "analytics" | "marketing" | "functional";
  }[];
}

// -------------------------------------------------------------------
// Defaults
// -------------------------------------------------------------------

const defaultConfig: CookiePolicyConfig = {
  companyLegalName: "YourCompany Inc.",
  companyName: "YourProduct",
  companyEmail: "privacy@yourproduct.com",
  companyWebsite: "https://yourproduct.com",
  lastUpdated: "March 20, 2026",
  cookieTypes: [
    {
      category: "Essential",
      name: "session_id",
      provider: "YourProduct",
      purpose: "Maintains your login session",
      duration: "Session",
      type: "essential",
    },
    {
      category: "Essential",
      name: "__csrf",
      provider: "YourProduct",
      purpose: "Prevents cross-site request forgery attacks",
      duration: "Session",
      type: "essential",
    },
    {
      category: "Analytics",
      name: "_ga",
      provider: "Google Analytics",
      purpose: "Distinguishes unique users to track site usage",
      duration: "2 years",
      type: "analytics",
    },
    {
      category: "Analytics",
      name: "_gid",
      provider: "Google Analytics",
      purpose: "Distinguishes unique users for 24-hour metrics",
      duration: "24 hours",
      type: "analytics",
    },
    {
      category: "Functional",
      name: "theme_preference",
      provider: "YourProduct",
      purpose: "Remembers your dark/light mode preference",
      duration: "1 year",
      type: "functional",
    },
    {
      category: "Functional",
      name: "cookie_consent",
      provider: "YourProduct",
      purpose: "Stores your cookie consent preferences",
      duration: "1 year",
      type: "functional",
    },
  ],
};

// -------------------------------------------------------------------
// Component
// -------------------------------------------------------------------

export default function CookiePolicy({
  config = defaultConfig,
}: {
  config?: CookiePolicyConfig;
}) {
  const categories = [
    {
      type: "essential" as const,
      title: "Essential Cookies",
      description:
        "These cookies are necessary for the website to function and cannot be switched off. They are usually set in response to actions you take, such as logging in, setting privacy preferences, or filling in forms.",
      canDisable: false,
    },
    {
      type: "analytics" as const,
      title: "Analytics Cookies",
      description:
        "These cookies help us understand how visitors interact with our website by collecting and reporting information anonymously. They help us improve the Service.",
      canDisable: true,
    },
    {
      type: "marketing" as const,
      title: "Marketing Cookies",
      description:
        "These cookies are used to track visitors across websites to display relevant advertisements. They are set by third-party advertising partners.",
      canDisable: true,
    },
    {
      type: "functional" as const,
      title: "Functional Cookies",
      description:
        "These cookies enable enhanced functionality and personalization, such as remembering your preferences. They may be set by us or by third-party providers whose services we use.",
      canDisable: true,
    },
  ];

  return (
    <LegalPageLayout title="Cookie Policy" lastUpdated={config.lastUpdated}>
      {/* Introduction */}
      <section>
        <h2 id="what-are-cookies">What Are Cookies?</h2>
        <p>
          Cookies are small text files stored on your device (computer, tablet,
          or mobile) when you visit a website. They are widely used to make
          websites work more efficiently and to provide information to website
          owners.
        </p>
        <p>
          This Cookie Policy explains what cookies {config.productName} uses,
          why we use them, and how you can control them.
        </p>
      </section>

      {/* Cookie Categories */}
      {categories
        .filter((cat) =>
          config.cookieTypes.some((cookie) => cookie.type === cat.type)
        )
        .map((category) => (
          <section key={category.type}>
            <h2 id={category.type}>{category.title}</h2>
            <p>{category.description}</p>
            {!category.canDisable && (
              <p>
                <strong>These cookies cannot be disabled</strong> as they are
                required for the Service to function.
              </p>
            )}

            <table>
              <thead>
                <tr>
                  <th>Cookie Name</th>
                  <th>Provider</th>
                  <th>Purpose</th>
                  <th>Duration</th>
                </tr>
              </thead>
              <tbody>
                {config.cookieTypes
                  .filter((cookie) => cookie.type === category.type)
                  .map((cookie) => (
                    <tr key={cookie.name}>
                      <td>
                        <code>{cookie.name}</code>
                      </td>
                      <td>{cookie.provider}</td>
                      <td>{cookie.purpose}</td>
                      <td>{cookie.duration}</td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </section>
        ))}

      {/* Managing Cookies */}
      <section>
        <h2 id="managing-cookies">Managing Your Cookie Preferences</h2>
        <p>You can control cookies in several ways:</p>

        <h3>Cookie Consent Banner</h3>
        <p>
          When you first visit our website, a cookie consent banner allows you
          to accept or reject non-essential cookies. You can change your
          preferences at any time by clicking the cookie settings link in our
          footer.
        </p>

        <h3>Browser Settings</h3>
        <p>
          Most web browsers allow you to control cookies through their settings.
          You can typically find these in the &quot;Options&quot; or
          &quot;Preferences&quot; menu:
        </p>
        <ul>
          <li>
            <strong>Chrome:</strong> Settings &gt; Privacy and security &gt; Cookies
          </li>
          <li>
            <strong>Firefox:</strong> Settings &gt; Privacy &amp; Security &gt; Cookies
          </li>
          <li>
            <strong>Safari:</strong> Preferences &gt; Privacy &gt; Manage Website Data
          </li>
          <li>
            <strong>Edge:</strong> Settings &gt; Cookies and site permissions
          </li>
        </ul>
        <p>
          Blocking certain cookies may impact the functionality of the Service.
          Essential cookies cannot be disabled without affecting core features
          like authentication.
        </p>

        <h3>Do Not Track</h3>
        <p>
          Some browsers send a &quot;Do Not Track&quot; signal. We currently
          respond to Do Not Track signals by disabling non-essential cookies
          for those users.
        </p>

        <h3>Global Privacy Control (GPC)</h3>
        <p>
          We honor the Global Privacy Control signal as a valid opt-out
          mechanism for the sale or sharing of personal information under
          applicable US state privacy laws.
        </p>
      </section>

      {/* Third-Party Cookies */}
      <section>
        <h2 id="third-party">Third-Party Cookies</h2>
        <p>
          Some cookies are placed by third-party services that appear on our
          pages. We do not control the use of these cookies and recommend
          reviewing the privacy policies of these third parties:
        </p>
        <ul>
          {[
            ...new Set(
              config.cookieTypes
                .filter((c) => c.provider !== config.companyName)
                .map((c) => c.provider)
            ),
          ].map((provider) => (
            <li key={provider}>{provider}</li>
          ))}
        </ul>
      </section>

      {/* Updates */}
      <section>
        <h2 id="updates">Changes to This Cookie Policy</h2>
        <p>
          We may update this Cookie Policy to reflect changes in the cookies we
          use or for operational, legal, or regulatory reasons. Please revisit
          this page periodically to stay informed.
        </p>
      </section>

      {/* Contact */}
      <section>
        <h2 id="contact">Contact Us</h2>
        <p>
          If you have questions about our use of cookies, contact us at{" "}
          <a href={`mailto:${config.companyEmail}`}>{config.companyEmail}</a>.
        </p>
      </section>
    </LegalPageLayout>
  );
}
```

---

## Page 4: Acceptable Use Policy

> **Gap exploited**: Only GetTerms offers an AUP generator among all competitors.

### Complete JSX Template

```tsx
import LegalPageLayout from "@/components/legal-page-layout";

interface AUPConfig {
  companyLegalName: string;
  companyName: string;
  companyEmail: string;
  productName: string;
  lastUpdated: string;
}

const defaultConfig: AUPConfig = {
  companyLegalName: "YourCompany Inc.",
  companyName: "YourProduct",
  companyEmail: "legal@yourproduct.com",
  productName: "YourProduct",
  lastUpdated: "March 20, 2026",
};

export default function AcceptableUsePolicy({
  config = defaultConfig,
}: {
  config?: AUPConfig;
}) {
  return (
    <LegalPageLayout
      title="Acceptable Use Policy"
      lastUpdated={config.lastUpdated}
    >
      <section>
        <h2 id="overview">Overview</h2>
        <p>
          This Acceptable Use Policy (&quot;AUP&quot;) sets out the rules for
          using {config.productName} (the &quot;Service&quot;) provided by{" "}
          {config.companyLegalName}. By using the Service, you agree to comply
          with this policy. This AUP is incorporated by reference into our{" "}
          <a href="/terms">Terms of Service</a>.
        </p>
      </section>

      <section>
        <h2 id="prohibited">Prohibited Activities</h2>
        <p>
          You must not use the Service to engage in any of the following
          activities:
        </p>

        <h3>Illegal Activities</h3>
        <ul>
          <li>
            Violate any local, state, national, or international law or
            regulation
          </li>
          <li>
            Engage in fraud, phishing, or any deceptive practices
          </li>
          <li>
            Facilitate money laundering, terrorist financing, or other financial
            crimes
          </li>
        </ul>

        <h3>Security Violations</h3>
        <ul>
          <li>
            Attempt to gain unauthorized access to the Service, other accounts,
            or connected systems
          </li>
          <li>
            Probe, scan, or test vulnerabilities without written authorization
          </li>
          <li>
            Distribute malware, viruses, trojans, spyware, or other harmful code
          </li>
          <li>
            Interfere with or disrupt the Service infrastructure (including DDoS
            attacks)
          </li>
          <li>
            Circumvent any security measures, authentication mechanisms, or
            access controls
          </li>
        </ul>

        <h3>Content Restrictions</h3>
        <ul>
          <li>
            Upload or distribute unlawful, defamatory, harassing, abusive,
            threatening, or obscene material
          </li>
          <li>
            Transmit content that infringes any patent, trademark, copyright, or
            other intellectual property rights
          </li>
          <li>
            Send spam, unsolicited communications, or bulk messages
          </li>
          <li>
            Post content that promotes violence, discrimination, or hatred
          </li>
        </ul>

        <h3>Service Abuse</h3>
        <ul>
          <li>
            Reverse engineer, decompile, disassemble, or attempt to discover the
            source code of the Service
          </li>
          <li>
            Use the Service for competitive benchmarking or to build a competing
            product
          </li>
          <li>
            Resell, sublicense, or provide access to the Service to unauthorized
            third parties
          </li>
          <li>
            Share account credentials with unauthorized users
          </li>
          <li>
            Use automated tools (bots, scrapers, crawlers) to access the Service
            beyond permitted API usage
          </li>
          <li>
            Intentionally overload the Service infrastructure
          </li>
        </ul>

        <h3>Export and Compliance</h3>
        <ul>
          <li>
            Use the Service in any manner that would violate US export control
            laws or regulations
          </li>
          <li>
            Access or use the Service from any embargoed or sanctioned country or
            territory
          </li>
        </ul>
      </section>

      <section>
        <h2 id="your-responsibilities">Your Responsibilities</h2>
        <ul>
          <li>
            Maintain the security and confidentiality of your account
            credentials
          </li>
          <li>
            Promptly notify us of any unauthorized use of your account
          </li>
          <li>
            Ensure that all users accessing the Service through your account
            comply with this AUP
          </li>
          <li>
            Use the Service only for its intended purpose as described in our
            documentation
          </li>
        </ul>
      </section>

      <section>
        <h2 id="enforcement">Enforcement</h2>
        <p>
          We reserve the right to investigate suspected violations of this AUP.
          If we determine that a violation has occurred, we may take action
          including:
        </p>
        <ul>
          <li>Issuing a warning</li>
          <li>Temporarily suspending your access to the Service</li>
          <li>Permanently terminating your account</li>
          <li>Reporting violations to law enforcement authorities</li>
          <li>Pursuing legal remedies</li>
        </ul>
        <p>
          In urgent cases (security threats, illegal activity, harm to other
          users), we may suspend access immediately without prior notice.
        </p>
      </section>

      <section>
        <h2 id="reporting">Reporting Violations</h2>
        <p>
          If you become aware of any violation of this AUP, please report it to{" "}
          <a href={`mailto:${config.companyEmail}`}>{config.companyEmail}</a>.
          We take all reports seriously and will investigate promptly.
        </p>
      </section>

      <section>
        <h2 id="changes">Changes to This Policy</h2>
        <p>
          We may update this AUP from time to time. Material changes will be
          communicated through the Service or via email. Continued use of the
          Service after changes take effect constitutes acceptance of the
          updated policy.
        </p>
      </section>

      <section>
        <h2 id="contact">Contact Us</h2>
        <p>
          Questions about this policy? Contact us at{" "}
          <a href={`mailto:${config.companyEmail}`}>{config.companyEmail}</a>.
        </p>
      </section>
    </LegalPageLayout>
  );
}
```

---

## Integration with Landing Page Generator

### When to Generate Legal Pages

```
IF footer links to /privacy, /terms, /cookies (default):
  → Generate all 3 legal page components
  → Ask legal intake questions OR infer from existing intake

IF user mentions "legal pages", "privacy policy", "terms of service":
  → Generate requested pages
  → Ask relevant intake questions

IF CTA type is waitlist or free-trial:
  → Privacy Policy is REQUIRED (collecting email addresses)
  → Generate at minimum the Privacy Policy
```

### File Output Structure

```
src/
├── app/ (or pages/)
│   ├── page.tsx              # Landing page
│   ├── privacy/page.tsx      # Privacy Policy
│   ├── terms/page.tsx        # Terms of Service
│   ├── cookies/page.tsx      # Cookie Policy
│   └── acceptable-use/page.tsx  # Acceptable Use Policy (optional)
├── components/
│   ├── legal-page-layout.tsx  # Shared layout
│   └── ui/                    # shadcn components
└── ...
```

### Framework Adapters

| Framework | Privacy Route | Layout File |
|-----------|--------------|-------------|
| Next.js (App Router) | `app/privacy/page.tsx` | `app/layout.tsx` wraps all |
| Next.js (Pages Router) | `pages/privacy.tsx` | `pages/_app.tsx` |
| Vite + React Router | `src/pages/Privacy.tsx` + route in `main.tsx` | `src/layouts/LegalLayout.tsx` |
| Remix | `app/routes/privacy.tsx` | `app/root.tsx` |
| Astro | `src/pages/privacy.astro` | `src/layouts/LegalLayout.astro` |

---

## Disclaimer

The legal page templates generated by this skill are **informational templates**,
not legal advice. They cover common requirements for GDPR, CCPA/CPRA, PIPEDA,
LGPD, and other privacy laws, but they may not address every situation.

**We recommend consulting with a qualified attorney** to review your legal pages
before going live, especially if you:

- Process sensitive personal information (health, financial, biometric data)
- Target users under 13 years old
- Operate in highly regulated industries (healthcare, finance, education)
- Transfer data internationally across multiple jurisdictions
- Use AI/ML to make automated decisions about individuals

The templates provide a strong starting point that covers 90%+ of standard
SaaS use cases — far better than copying another company's policy or using
a non-compliant free generator.
