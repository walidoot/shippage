#!/usr/bin/env python3
"""
select-sections.py - Choose and order landing page sections for conversion
==========================================================================

Given an awareness level, CTA goal, available social proof, and desired
section count, outputs an ordered list of page sections that follows
proven SaaS conversion sequences.

The algorithm prioritises sections based on visitor psychology:
  - Problem-aware visitors need pain agitation before the solution.
  - Solution-aware visitors need differentiation and proof.
  - Product-aware visitors need features and pricing up front.

Section types available:
  navbar, hero-split, hero-centered, social-proof-logos, pain-points,
  how-it-works, features-bento, features-alternating, testimonials,
  comparison-table, pricing, faq, cta-footer

Usage:
  python3 scripts/select-sections.py \\
      --awareness problem-aware --cta free-trial \\
      --proof logos,testimonials --sections 9

  python3 scripts/select-sections.py \\
      --awareness product-aware --cta purchase \\
      --proof metrics,badges

  python3 scripts/select-sections.py \\
      --awareness solution-aware --cta demo \\
      --proof none --sections 7
"""

import argparse
import sys


# =============================================================================
# Constants
# =============================================================================

AWARENESS_LEVELS = ("problem-aware", "solution-aware", "product-aware")
CTA_GOALS = ("free-trial", "demo", "waitlist", "purchase")
PROOF_OPTIONS = ("logos", "testimonials", "metrics", "badges", "none")
HERO_VARIANTS = ("auto", "split", "centered")

# Priority offsets for optional sections (higher = more likely to be dropped)
LOW_PRIORITY_OFFSET = 5

DEFAULT_SECTION_COUNT = 8
MIN_SECTION_COUNT = 5
MAX_SECTION_COUNT = 15

# CTA label mapping
CTA_LABELS = {
    "free-trial": "Start Free Trial",
    "demo": "Book a Demo",
    "waitlist": "Join the Waitlist",
    "purchase": "Get Started",
}

# Section notes keyed by section type
SECTION_NOTES = {
    "navbar": "Sticky nav with primary CTA",
    "hero-split": "Primary CTA: {cta_label}",
    "hero-centered": "Primary CTA: {cta_label}",
    "social-proof-logos": "Logo strip + metrics bar",
    "pain-points": "Problem-aware: agitate before solution",
    "how-it-works": "3-step process for clarity",
    "features-bento": "3-5 key features in bento grid",
    "features-alternating": "Feature/benefit alternating rows",
    "testimonials": "Social proof before pricing",
    "metrics-bar": "Key numbers to build credibility",
    "trust-badges": "Security/compliance badges",
    "comparison-table": "Why us vs alternatives",
    "pricing": "3-tier with annual toggle",
    "faq": "Address top objections",
    "cta-footer": "Final CTA + footer",
}


# =============================================================================
# Section selection logic
# =============================================================================

def select_hero_variant(
    hero: str,
    awareness: str,
    cta: str,
) -> str:
    """
    Choose hero-split or hero-centered based on heuristics.

    - hero-split: Best when you have a product screenshot or side-by-side visual.
      Works for most SaaS pages.  Default safe choice.
    - hero-centered: Best for bold statement pages, waitlist/pre-launch,
      dark-premium vibes, or when there's no product visual to show.

    Returns "hero-split" or "hero-centered".
    """
    if hero == "split":
        return "hero-split"
    if hero == "centered":
        return "hero-centered"

    # Auto-select heuristic
    # Waitlist pages rarely have a product screenshot → centered
    if cta == "waitlist":
        return "hero-centered"

    # Product-aware visitors already know the product → centered headline works
    if awareness == "product-aware" and cta in ("purchase", "demo"):
        return "hero-centered"

    # Default: split layout (product visual assumed)
    return "hero-split"


def select_sections(
    awareness: str,
    cta: str,
    proof: list,
    count: int,
    hero: str = "auto",
) -> list:
    """
    Build an ordered list of (section_type, note) tuples following the
    conversion sequence appropriate for the given parameters.

    The ordering follows a psychological flow:
      1. navbar          - Always first
      2. hero            - Value proposition
      3. social proof    - Immediate credibility
      4. pain points     - Agitate the problem (problem-aware only)
      5. how-it-works    - Bridge to solution (problem-aware/complex)
      6. features        - Show the product
      7. testimonials    - Deeper social proof
      8. metrics/badges  - Additional credibility
      9. pricing         - Commit (free-trial/purchase)
      10. faq            - Handle objections (demo/purchase)
      11. cta-footer     - Always last
    """
    cta_label = CTA_LABELS.get(cta, "Get Started")
    has_logos = "logos" in proof
    has_testimonials = "testimonials" in proof
    has_metrics = "metrics" in proof
    has_badges = "badges" in proof
    has_any_proof = has_logos or has_testimonials or has_metrics or has_badges

    # --- Build the candidate pool in priority order --------------------------
    # Each entry: (section_type, note, priority)
    # Priority: lower = must include, higher = can be dropped to hit count
    candidates = []
    priority = 0

    # 1. Navbar - always included
    candidates.append(("navbar", SECTION_NOTES["navbar"], priority))
    priority += 1

    # 2. Hero - always included; variant chosen by heuristic or explicit flag
    hero_type = select_hero_variant(hero, awareness, cta)
    hero_note = SECTION_NOTES[hero_type].format(cta_label=cta_label)
    candidates.append((hero_type, hero_note, priority))
    priority += 1

    # 3. Social proof logos - early if available
    if has_logos or has_testimonials:
        note = "Logo strip"
        if has_metrics:
            note += " + metrics bar"
        candidates.append(("social-proof-logos", note, priority))
        priority += 1

    # 4. Pain points - problem-aware only
    if awareness == "problem-aware":
        candidates.append(("pain-points", SECTION_NOTES["pain-points"], priority))
        priority += 1

    # 5. How-it-works - for complex products (problem-aware)
    if awareness == "problem-aware":
        candidates.append(("how-it-works", SECTION_NOTES["how-it-works"], priority))
        priority += 1

    # 6. Features - always at least one
    # Default to bento for richer layouts; alternating for simpler ones
    candidates.append(("features-bento", SECTION_NOTES["features-bento"], priority))
    priority += 1

    # 7. Additional features section if we have room (solution-aware benefits)
    if awareness in ("solution-aware", "product-aware"):
        candidates.append((
            "features-alternating",
            "Detailed feature/benefit breakdown",
            priority + LOW_PRIORITY_OFFSET,  # lower priority, can be dropped
        ))

    # 8. Testimonials - if available
    if has_testimonials:
        candidates.append(("testimonials", SECTION_NOTES["testimonials"], priority))
        priority += 1

    # 9. Metrics bar - standalone if we have metrics but no logos section
    if has_metrics and not has_logos and not has_testimonials:
        candidates.append(("metrics-bar", SECTION_NOTES["metrics-bar"], priority))
        priority += 1

    # 10. Trust badges - if available
    if has_badges:
        candidates.append(("trust-badges", SECTION_NOTES["trust-badges"], priority))
        priority += 1

    # 10b. Comparison table - solution-aware visitors actively comparing alternatives
    if awareness == "solution-aware":
        candidates.append((
            "comparison-table",
            SECTION_NOTES["comparison-table"],
            priority + LOW_PRIORITY_OFFSET,  # optional, included if room
        ))

    # 11. Pricing - for free-trial or purchase CTAs
    if cta in ("free-trial", "purchase"):
        candidates.append(("pricing", SECTION_NOTES["pricing"], priority))
        priority += 1

    # 12. FAQ - always valuable, priority varies by CTA type
    if cta in ("demo", "purchase"):
        # High-ticket: FAQ addresses pricing/contract objections
        candidates.append(("faq", SECTION_NOTES["faq"], priority))
        priority += 1
    elif cta == "waitlist":
        # Pre-launch: FAQ addresses "when does this launch?" + roadmap
        candidates.append(("faq", "Address launch timeline and access questions", priority))
        priority += 1
    elif cta == "free-trial":
        # Free trial: FAQ addresses trial limits, card requirements
        candidates.append(("faq", "Address trial terms and onboarding questions", priority + LOW_PRIORITY_OFFSET - 2))
    elif awareness == "problem-aware":
        # Problem-aware: FAQ educates about the problem space
        candidates.append(("faq", "Address common questions", priority + LOW_PRIORITY_OFFSET - 2))

    # 13. CTA footer - always last
    candidates.append(("cta-footer", SECTION_NOTES["cta-footer"], priority))
    priority += 1

    # --- Select sections up to the requested count ---------------------------
    # navbar and cta-footer are mandatory; count the rest by priority
    mandatory = [c for c in candidates if c[0] in ("navbar", "cta-footer")]
    optional = [c for c in candidates if c[0] not in ("navbar", "cta-footer")]

    # Sort optional by priority (lower = more important)
    optional.sort(key=lambda x: x[2])

    # Determine how many optional sections we can include
    available_slots = count - len(mandatory)
    if available_slots < 0:
        available_slots = 0

    selected_optional = optional[:available_slots]

    # --- Rebuild in conversion-sequence order --------------------------------
    # Define the canonical ordering
    ORDER = [
        "navbar",
        "hero-split",
        "hero-centered",
        "social-proof-logos",
        "pain-points",
        "how-it-works",
        "features-bento",
        "features-alternating",
        "testimonials",
        "metrics-bar",
        "trust-badges",
        "comparison-table",
        "pricing",
        "faq",
        "cta-footer",
    ]

    selected_set = {c[0]: c[1] for c in mandatory + selected_optional}
    ordered = []
    for section in ORDER:
        if section in selected_set:
            ordered.append((section, selected_set[section]))

    return ordered


# =============================================================================
# Output formatting
# =============================================================================

def format_section_list(sections: list) -> str:
    """Format sections as a numbered list with inline notes."""
    lines = []
    # Compute alignment width from longest section name
    max_name_len = max(len(s[0]) for s in sections) if sections else 0

    for i, (section, note) in enumerate(sections, 1):
        padded = section.ljust(max_name_len)
        lines.append(f"{i:>2}. {padded}  # {note}")

    return "\n".join(lines)


# =============================================================================
# Validation helpers
# =============================================================================

def validate_proof(value: str) -> list:
    """Parse and validate the --proof argument."""
    if not value:
        return ["none"]

    items = [p.strip().lower() for p in value.split(",")]
    invalid = [p for p in items if p not in PROOF_OPTIONS]
    if invalid:
        raise argparse.ArgumentTypeError(
            f"Invalid proof type(s): {', '.join(invalid)}. "
            f"Valid options: {', '.join(PROOF_OPTIONS)}"
        )

    # If "none" is combined with others, it makes no sense
    if "none" in items and len(items) > 1:
        raise argparse.ArgumentTypeError(
            '"none" cannot be combined with other proof types.'
        )

    return items


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Select and order landing page sections for optimal conversion.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Section selection follows proven SaaS conversion sequences:
  - Problem-aware:  Hero -> Social Proof -> Pain Points -> Features -> CTA
  - Solution-aware: Hero -> Social Proof -> Features -> Testimonials -> CTA
  - Product-aware:  Hero -> Features -> Pricing -> CTA

Examples:
  %(prog)s --awareness problem-aware --cta free-trial --proof logos,testimonials
  %(prog)s --awareness product-aware --cta purchase --proof metrics,badges --sections 7
  %(prog)s --awareness solution-aware --cta demo --proof none
        """,
    )
    parser.add_argument(
        "--awareness",
        type=str,
        required=True,
        choices=AWARENESS_LEVELS,
        help="Visitor awareness level: problem-aware, solution-aware, or product-aware",
    )
    parser.add_argument(
        "--cta",
        type=str,
        required=True,
        choices=CTA_GOALS,
        help="Primary CTA goal: free-trial, demo, waitlist, or purchase",
    )
    parser.add_argument(
        "--proof",
        type=str,
        required=True,
        help=(
            "Comma-separated list of available social proof types: "
            "logos, testimonials, metrics, badges, none"
        ),
    )
    parser.add_argument(
        "--hero",
        type=str,
        default="auto",
        choices=HERO_VARIANTS,
        help=(
            "Hero variant: auto (heuristic), split (side-by-side), "
            "or centered (full-width headline). Default: auto"
        ),
    )
    parser.add_argument(
        "--sections",
        type=int,
        default=DEFAULT_SECTION_COUNT,
        help=f"Target number of sections to include (default: {DEFAULT_SECTION_COUNT})",
    )

    args = parser.parse_args()

    # Validate proof
    try:
        proof_list = validate_proof(args.proof)
    except argparse.ArgumentTypeError as e:
        parser.error(str(e))

    # Validate section count
    if args.sections < MIN_SECTION_COUNT:
        parser.error(
            f"--sections must be at least {MIN_SECTION_COUNT} "
            f"(navbar + hero + cta-footer + 2 content sections)."
        )
    if args.sections > MAX_SECTION_COUNT:
        parser.error(
            f"--sections must be at most {MAX_SECTION_COUNT}. "
            f"More sections hurt conversion rates."
        )

    # Select sections
    sections = select_sections(
        awareness=args.awareness,
        cta=args.cta,
        proof=proof_list,
        count=args.sections,
        hero=args.hero,
    )

    # Output
    print(format_section_list(sections))


if __name__ == "__main__":
    main()
