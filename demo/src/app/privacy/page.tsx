import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Privacy Policy — Shippage",
  description: "How Shippage handles your data.",
};

export default function PrivacyPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:py-24">
      <Link
        href="/"
        className="text-sm text-muted-foreground transition-colors hover:text-foreground"
      >
        &larr; Back to home
      </Link>

      <h1 className="mt-8 text-3xl font-bold text-foreground">
        Privacy Policy
      </h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Last updated: March 21, 2026
      </p>

      <div className="mt-8 space-y-8 text-muted-foreground [&_h2]:mt-8 [&_h2]:text-xl [&_h2]:font-semibold [&_h2]:text-foreground [&_p]:mt-3 [&_ul]:mt-3 [&_ul]:list-disc [&_ul]:pl-6 [&_li]:mt-1">
        <section>
          <h2>Overview</h2>
          <p>
            Shippage is an open-source Claude Code skill. The skill itself runs
            entirely on your local machine and does not transmit any data to
            Shippage servers. This policy covers the shippage.dev website only.
          </p>
        </section>

        <section>
          <h2>Data We Collect</h2>
          <p>
            When you visit shippage.dev, we may collect basic analytics data
            through privacy-respecting tools:
          </p>
          <ul>
            <li>Pages visited and time spent</li>
            <li>Referral source</li>
            <li>Browser type and screen size</li>
            <li>Country (derived from IP, which is not stored)</li>
          </ul>
        </section>

        <section>
          <h2>Contact Form</h2>
          <p>
            If you submit the contact form, we collect your name, email address,
            and message. This data is used solely to respond to your inquiry and
            is not shared with third parties.
          </p>
        </section>

        <section>
          <h2>Cookies</h2>
          <p>
            We use minimal cookies for analytics and to remember your cookie
            consent preference. See our{" "}
            <Link href="/cookies" className="text-primary hover:underline">
              Cookie Policy
            </Link>{" "}
            for details.
          </p>
        </section>

        <section>
          <h2>Third-Party Services</h2>
          <p>
            This website may use Vercel Analytics for privacy-friendly usage
            statistics. No personal data is sold or shared with advertisers.
          </p>
        </section>

        <section>
          <h2>Your Rights</h2>
          <p>
            Under GDPR, CCPA, and similar regulations, you have the right to
            access, correct, or delete your personal data. Contact us at{" "}
            <a
              href="mailto:jahan@agenticmode.ai"
              className="text-primary hover:underline"
            >
              jahan@agenticmode.ai
            </a>{" "}
            to exercise these rights.
          </p>
        </section>

        <section>
          <h2>Contact</h2>
          <p>
            For privacy-related questions, email{" "}
            <a
              href="mailto:jahan@agenticmode.ai"
              className="text-primary hover:underline"
            >
              jahan@agenticmode.ai
            </a>
            .
          </p>
        </section>
      </div>
    </main>
  );
}
