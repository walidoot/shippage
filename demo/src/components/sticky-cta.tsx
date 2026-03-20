"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, X } from "lucide-react";

export function StickyCTA() {
  const [visible, setVisible] = useState(false);
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    if (dismissed) return;
    const wasDismissed = sessionStorage.getItem("sp_sticky_dismissed");
    if (wasDismissed) {
      setDismissed(true);
      return;
    }

    const handleScroll = () => {
      const heroBottom = document.querySelector("[data-hero-cta]");
      if (!heroBottom) {
        setVisible(window.scrollY > 600);
        return;
      }
      const rect = heroBottom.getBoundingClientRect();
      setVisible(rect.bottom < 0);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [dismissed]);

  const handleDismiss = () => {
    setDismissed(true);
    sessionStorage.setItem("sp_sticky_dismissed", "1");
  };

  if (dismissed) return null;

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 100, opacity: 0 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          className="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-card/95 backdrop-blur-sm"
        >
          <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
            <p className="hidden text-sm text-muted-foreground sm:block">
              Ship a landing page from your terminal. Free forever.
            </p>
            <div className="flex flex-1 items-center justify-end gap-3">
              <a
                href="https://github.com/imjahanzaib/shippage"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2 text-sm font-medium text-primary-foreground transition-colors hover:brightness-110"
              >
                Install Free
                <ArrowRight className="h-4 w-4" />
              </a>
              <button
                onClick={handleDismiss}
                className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                aria-label="Dismiss sticky bar"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
