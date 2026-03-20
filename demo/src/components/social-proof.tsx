"use client";

import { motion } from "framer-motion";
import { Github, Star, Blocks, FileCode2, Palette } from "lucide-react";

const stats = [
  { icon: Blocks, value: "18", label: "Section templates" },
  { icon: FileCode2, value: "629", label: "Lines of copy rules" },
  { icon: Palette, value: "200+", label: "Design tokens" },
  { icon: Star, value: "6", label: "Frameworks supported" },
];

const containerVariants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } },
};

const itemVariants = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" as const } },
};

export function SocialProof() {
  return (
    <section className="border-y border-border bg-card/50 py-12 lg:py-16">
      <motion.div
        className="mx-auto flex max-w-5xl flex-col items-center gap-8 px-4 sm:px-6"
        variants={containerVariants}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: "-50px" }}
      >
        <motion.div
          variants={itemVariants}
          className="flex items-center gap-2 text-sm text-muted-foreground"
        >
          <Github className="h-4 w-4" />
          <span>Free &amp; open source on GitHub</span>
          <span className="mx-2 text-border">·</span>
          <span>MIT Licensed</span>
        </motion.div>

        <div className="grid w-full grid-cols-2 gap-6 sm:gap-8 lg:grid-cols-4">
          {stats.map((stat) => (
            <motion.div
              key={stat.label}
              variants={itemVariants}
              className="flex flex-col items-center gap-2 text-center"
            >
              <stat.icon className="h-5 w-5 text-primary" />
              <span className="text-2xl font-bold text-foreground sm:text-3xl">
                {stat.value}
              </span>
              <span className="text-sm text-muted-foreground">
                {stat.label}
              </span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </section>
  );
}
