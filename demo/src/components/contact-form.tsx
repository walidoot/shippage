"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Send,
  CheckCircle,
  AlertCircle,
  Mail,
  Github,
} from "lucide-react";

const containerVariants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } },
};
const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" as const } },
};

export function ContactForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [honeypot, setHoneypot] = useState("");
  const [status, setStatus] = useState<
    "idle" | "sending" | "success" | "error"
  >("idle");
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const errs: Record<string, string> = {};
    if (!name.trim()) errs.name = "Name is required";
    if (!email.trim()) errs.email = "Email is required";
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      errs.email = "Enter a valid email";
    if (!message.trim()) errs.message = "Message is required";
    else if (message.trim().length < 10)
      errs.message = "Message must be at least 10 characters";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (honeypot) {
      setStatus("success");
      return;
    }
    if (!validate()) return;
    setStatus("sending");
    try {
      // Replace with your Formspree endpoint or API route
      const res = await fetch("https://formspree.io/f/xwpkbjgv", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, message }),
      });
      if (res.ok) {
        setStatus("success");
        setName("");
        setEmail("");
        setMessage("");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  };

  if (status === "success") {
    return (
      <section id="contact" className="bg-muted/30 py-16 lg:py-24">
        <div className="mx-auto max-w-2xl px-4 text-center sm:px-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <CheckCircle className="mx-auto h-12 w-12 text-green-500" />
            <h3 className="mt-4 text-2xl font-bold text-foreground">
              Message received
            </h3>
            <p className="mt-2 text-muted-foreground">
              Thanks for reaching out. We&apos;ll get back to you within 24
              hours.
            </p>
          </motion.div>
        </div>
      </section>
    );
  }

  return (
    <section id="contact" className="bg-muted/30 py-16 lg:py-24">
      <motion.div
        className="mx-auto grid max-w-4xl gap-12 px-4 sm:px-6 lg:grid-cols-2 lg:gap-16"
        variants={containerVariants}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: "-100px" }}
      >
        <motion.div
          variants={itemVariants}
          className="flex flex-col justify-center"
        >
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Get in touch
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Have a question, feature request, or want to contribute? Drop us a
            message and we&apos;ll respond within 24 hours.
          </p>
          <div className="mt-8 space-y-4">
            <a
              href="mailto:jahan@agenticmode.ai"
              className="flex items-center gap-3 text-muted-foreground transition-colors hover:text-foreground"
            >
              <Mail className="h-5 w-5 text-primary" />
              <span>jahan@agenticmode.ai</span>
            </a>
            <a
              href="https://github.com/imjahanzaib/shippage"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 text-muted-foreground transition-colors hover:text-foreground"
            >
              <Github className="h-5 w-5 text-primary" />
              <span>github.com/imjahanzaib/shippage</span>
            </a>
          </div>
        </motion.div>

        <motion.form
          variants={itemVariants}
          onSubmit={handleSubmit}
          className="space-y-4 rounded-xl border border-border bg-card p-6 shadow-sm sm:p-8"
          noValidate
        >
          {/* Honeypot */}
          <input
            type="text"
            name="website"
            value={honeypot}
            onChange={(e) => setHoneypot(e.target.value)}
            className="absolute h-0 w-0 opacity-0 pointer-events-none"
            tabIndex={-1}
            autoComplete="off"
            aria-hidden="true"
          />

          <div>
            <label
              htmlFor="contact-name"
              className="block text-sm font-medium text-foreground"
            >
              Name
            </label>
            <input
              id="contact-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              aria-required="true"
              aria-describedby={errors.name ? "name-error" : undefined}
              className="mt-1 block w-full rounded-lg border border-border bg-background px-4 py-2.5 text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
              placeholder="Your name"
            />
            {errors.name && (
              <p id="name-error" className="mt-1 text-sm text-destructive">
                {errors.name}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="contact-email"
              className="block text-sm font-medium text-foreground"
            >
              Email
            </label>
            <input
              id="contact-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              aria-required="true"
              aria-describedby={errors.email ? "email-error" : undefined}
              className="mt-1 block w-full rounded-lg border border-border bg-background px-4 py-2.5 text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
              placeholder="you@company.com"
            />
            {errors.email && (
              <p id="email-error" className="mt-1 text-sm text-destructive">
                {errors.email}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="contact-message"
              className="block text-sm font-medium text-foreground"
            >
              Message
            </label>
            <textarea
              id="contact-message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={5}
              aria-required="true"
              aria-describedby={errors.message ? "message-error" : undefined}
              className="mt-1 block w-full resize-none rounded-lg border border-border bg-background px-4 py-2.5 text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
              placeholder="Tell us what you're building..."
            />
            {errors.message && (
              <p id="message-error" className="mt-1 text-sm text-destructive">
                {errors.message}
              </p>
            )}
          </div>

          {status === "error" && (
            <div className="flex items-center gap-2 rounded-lg bg-destructive/10 p-3 text-sm text-destructive">
              <AlertCircle className="h-4 w-4 flex-shrink-0" />
              Something went wrong. Please try again or email us directly.
            </div>
          )}

          <button
            type="submit"
            disabled={status === "sending"}
            className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-medium text-primary-foreground transition-colors hover:brightness-110 disabled:opacity-60"
          >
            {status === "sending" ? (
              <>
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
                Sending...
              </>
            ) : (
              <>
                <Send className="h-4 w-4" />
                Send Message
              </>
            )}
          </button>

          <p className="text-center text-xs text-muted-foreground">
            We respond within 24 hours. No spam, ever.
          </p>
        </motion.form>
      </motion.div>
    </section>
  );
}
