"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Cookie, X } from "lucide-react";

export function CookieConsent() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem("sp_cookie_consent");
    if (!consent) {
      const timer = setTimeout(() => setVisible(true), 1500);
      return () => clearTimeout(timer);
    }
  }, []);

  const accept = () => {
    localStorage.setItem("sp_cookie_consent", "accepted");
    setVisible(false);
  };

  const decline = () => {
    localStorage.setItem("sp_cookie_consent", "declined");
    setVisible(false);
  };

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 100, opacity: 0 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          className="fixed bottom-4 left-4 right-4 z-[60] mx-auto max-w-lg rounded-xl border border-border bg-card p-4 shadow-2xl sm:bottom-6 sm:left-6 sm:right-auto sm:p-6"
        >
          <div className="flex items-start gap-3">
            <Cookie className="mt-0.5 h-5 w-5 flex-shrink-0 text-primary" />
            <div className="flex-1">
              <p className="text-sm font-medium text-foreground">
                Cookie notice
              </p>
              <p className="mt-1 text-sm text-muted-foreground">
                We use analytics cookies to understand how you use our site and
                improve your experience. No personal data is sold.
              </p>
              <div className="mt-4 flex gap-3">
                <button
                  onClick={accept}
                  className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:brightness-110"
                >
                  Accept
                </button>
                <button
                  onClick={decline}
                  className="rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-muted"
                >
                  Decline
                </button>
              </div>
            </div>
            <button
              onClick={decline}
              className="rounded-lg p-1 text-muted-foreground transition-colors hover:text-foreground"
              aria-label="Close cookie notice"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
