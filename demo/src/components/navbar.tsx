"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, useMotionValueEvent, useScroll } from "framer-motion";
import { Terminal, Menu, X } from "lucide-react";

const navLinks = [
  { label: "Features", href: "#features" },
  { label: "How It Works", href: "#how-it-works" },
  { label: "FAQ", href: "#faq" },
] as const;

export function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { scrollY } = useScroll();

  useMotionValueEvent(scrollY, "change", (latest) => {
    setScrolled(latest > 20);
  });

  const handleLinkClick = useCallback(() => {
    setMobileOpen(false);
  }, []);

  // Lock body scroll when mobile menu is open
  useEffect(() => {
    if (mobileOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileOpen]);

  // Close mobile menu on escape key
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape" && mobileOpen) {
        setMobileOpen(false);
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [mobileOpen]);

  return (
    <motion.header
      className="fixed top-0 left-0 right-0 z-50 border-b backdrop-blur-md"
      animate={{
        backgroundColor: scrolled
          ? "rgba(10, 10, 10, 0.95)"
          : "rgba(10, 10, 10, 0)",
        borderColor: scrolled
          ? "rgba(255, 255, 255, 0.08)"
          : "rgba(255, 255, 255, 0)",
      }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <nav
        className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8"
        aria-label="Main navigation"
      >
        {/* Logo */}
        <a
          href="#"
          className="flex items-center gap-2 text-foreground transition-opacity hover:opacity-80"
          aria-label="Shippage home"
        >
          <Terminal className="h-5 w-5 text-primary" aria-hidden="true" />
          <span className="text-lg font-bold tracking-tight">Shippage</span>
        </a>

        {/* Desktop nav links */}
        <ul className="hidden items-center gap-1 md:flex" role="list">
          {navLinks.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="inline-flex h-11 items-center rounded-md px-4 text-sm font-medium text-foreground/70 transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Desktop CTA + Mobile hamburger */}
        <div className="flex items-center gap-3">
          <a
            href="https://github.com/imjahanzaib/shippage"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden h-11 items-center rounded-lg bg-primary px-5 text-sm font-semibold text-primary-foreground transition-all hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background md:inline-flex"
          >
            Install Free
          </a>

          <button
            type="button"
            className="inline-flex h-11 w-11 items-center justify-center rounded-md text-foreground/70 transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background md:hidden"
            onClick={() => setMobileOpen((prev) => !prev)}
            aria-expanded={mobileOpen}
            aria-controls="mobile-menu"
            aria-label={mobileOpen ? "Close menu" : "Open menu"}
          >
            {mobileOpen ? (
              <X className="h-6 w-6" aria-hidden="true" />
            ) : (
              <Menu className="h-6 w-6" aria-hidden="true" />
            )}
          </button>
        </div>
      </nav>

      {/* Mobile menu */}
      <motion.div
        id="mobile-menu"
        role="dialog"
        aria-label="Mobile navigation"
        className="overflow-hidden border-t border-border/50 md:hidden"
        initial={false}
        animate={{
          height: mobileOpen ? "auto" : 0,
          opacity: mobileOpen ? 1 : 0,
        }}
        transition={{ duration: 0.25, ease: "easeInOut" }}
      >
        <div className="flex flex-col gap-1 bg-[#0a0a0a] px-4 pb-6 pt-3">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              onClick={handleLinkClick}
              className="flex h-11 items-center rounded-md px-3 text-base font-medium text-foreground/70 transition-colors hover:bg-white/5 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
            >
              {link.label}
            </a>
          ))}
          <a
            href="https://github.com/imjahanzaib/shippage"
            target="_blank"
            rel="noopener noreferrer"
            onClick={handleLinkClick}
            className="mt-2 flex h-11 items-center justify-center rounded-lg bg-primary px-5 text-sm font-semibold text-primary-foreground transition-all hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background"
          >
            Install Free
          </a>
        </div>
      </motion.div>
    </motion.header>
  );
}
