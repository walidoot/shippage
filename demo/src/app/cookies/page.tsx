import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Cookie Policy — Shippage",
  description: "How Shippage uses cookies on shippage.dev.",
};

export default function CookiesPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:py-24">
      <Link
        href="/"
        className="text-sm text-muted-foreground transition-colors hover:text-foreground"
      >
        &larr; Back to home
      </Link>

      <h1 className="mt-8 text-3xl font-bold text-foreground">
        Cookie Policy
      </h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Last updated: March 21, 2026
      </p>

      <div className="mt-8 space-y-8 text-muted-foreground [&_h2]:mt-8 [&_h2]:text-xl [&_h2]:font-semibold [&_h2]:text-foreground [&_p]:mt-3">
        <section>
          <h2>What Are Cookies</h2>
          <p>
            Cookies are small text files stored on your device when you visit a
            website. They help the site remember your preferences and understand
            how you use it.
          </p>
        </section>

        <section>
          <h2>Cookies We Use</h2>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border text-left text-foreground">
                  <th className="py-3 pr-4 font-medium">Cookie</th>
                  <th className="py-3 pr-4 font-medium">Purpose</th>
                  <th className="py-3 pr-4 font-medium">Duration</th>
                  <th className="py-3 font-medium">Type</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-border/50">
                  <td className="py-3 pr-4 font-mono text-xs">
                    sp_cookie_consent
                  </td>
                  <td className="py-3 pr-4">
                    Remembers your cookie preference
                  </td>
                  <td className="py-3 pr-4">Persistent</td>
                  <td className="py-3">Essential</td>
                </tr>
                <tr className="border-b border-border/50">
                  <td className="py-3 pr-4 font-mono text-xs">
                    sp_sticky_dismissed
                  </td>
                  <td className="py-3 pr-4">
                    Remembers if you closed the sticky bar
                  </td>
                  <td className="py-3 pr-4">Session</td>
                  <td className="py-3">Functional</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h2>Managing Cookies</h2>
          <p>
            You can control cookies through your browser settings. Most browsers
            allow you to block or delete cookies. Note that blocking essential
            cookies may affect site functionality.
          </p>
          <p>
            You can also update your preferences using the &ldquo;Cookie
            Settings&rdquo; link in our footer.
          </p>
        </section>

        <section>
          <h2>Contact</h2>
          <p>
            Questions about our cookie practices? Email{" "}
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
