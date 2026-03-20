#!/usr/bin/env python3
"""
select-design-system.py - Find matching design systems by industry and vibe
===========================================================================

Queries the design-tokens-db.json database and returns the 5-8 closest
matching design systems based on industry and vibe scoring.

Scoring:
  - Exact industry match:    3 points
  - Adjacent industry match: 1 point
  - Exact vibe match:        2 points
  - Similar vibe match:      1 point

Prerequisites:
  - Run parse-tokens.py first to generate references/design-tokens-db.json

Usage:
  python3 scripts/select-design-system.py --industry "Developer Tools" --vibe dark
  python3 scripts/select-design-system.py --industry "Fintech / Payments" --vibe minimal
  python3 scripts/select-design-system.py --industry "AI / ML" --vibe bold --top 8
  python3 scripts/select-design-system.py --list-industries
  python3 scripts/select-design-system.py --list-vibes
  python3 scripts/select-design-system.py --industry "Marketing / Email / CRM" --vibe playful --json
"""

import argparse
import json
import sys
from pathlib import Path


# =============================================================================
# Constants
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_DB_PATH = PROJECT_DIR / "references" / "design-tokens-db.json"

MIN_RESULTS = 5
MAX_RESULTS = 8
DEFAULT_RESULTS = 6

# Industry adjacency: industries that share design sensibilities
INDUSTRY_ADJACENCY = {
    "Developer Tools": [
        "AI / ML",
        "Analytics / Data",
        "Auth / Security / Infra",
    ],
    "Fintech / Payments": [
        "Marketing / Email / CRM",
        "Analytics / Data",
        "Auth / Security / Infra",
    ],
    "AI / ML": [
        "Developer Tools",
        "Analytics / Data",
        "Design / Creative",
    ],
    "Marketing / Email / CRM": [
        "Productivity / Collaboration",
        "Analytics / Data",
        "Fintech / Payments",
        "Design / Creative",
    ],
    "Productivity / Collaboration": [
        "Marketing / Email / CRM",
        "Design / Creative",
        "Developer Tools",
    ],
    "Design / Creative": [
        "Productivity / Collaboration",
        "AI / ML",
        "Marketing / Email / CRM",
    ],
    "Analytics / Data": [
        "Developer Tools",
        "AI / ML",
        "Fintech / Payments",
        "Auth / Security / Infra",
    ],
    "Auth / Security / Infra": [
        "Developer Tools",
        "Analytics / Data",
        "Fintech / Payments",
    ],
}

# Vibe similarity: vibes that share aesthetic sensibilities
VIBE_SIMILARITY = {
    "dark": ["bold", "enterprise"],
    "bold": ["dark", "playful"],
    "minimal": ["enterprise"],
    "playful": ["bold"],
    "enterprise": ["minimal", "dark"],
}

ALL_VIBES = sorted(VIBE_SIMILARITY.keys())

# Also accept long-form vibe names used in curated tokens
LONG_VIBES = ["dark-premium", "bold-modern", "minimal-clean", "playful-creative", "enterprise-trust"]
ACCEPTED_VIBES = sorted(set(ALL_VIBES + LONG_VIBES))


# =============================================================================
# Scoring
# =============================================================================

def score_entry(entry: dict, target_industry: str, target_vibe: str) -> int:
    """
    Score a design system entry against target industry and vibe.

    Scoring:
      Exact industry match:    3 points
      Adjacent industry match: 1 point
      Exact vibe match:        2 points
      Similar vibe match:      1 point
    """
    score = 0
    entry_industry = entry.get("industry", "Unknown")
    entry_vibe = entry.get("vibe", "minimal")

    # Industry scoring
    if entry_industry.lower() == target_industry.lower():
        score += 3
    elif entry_industry in INDUSTRY_ADJACENCY.get(target_industry, []):
        score += 1

    # Vibe scoring — handle both short ("dark") and long ("dark-premium") vibe names
    entry_vibe_short = entry_vibe.split("-")[0].lower() if "-" in entry_vibe else entry_vibe.lower()
    target_vibe_short = target_vibe.split("-")[0].lower() if "-" in target_vibe else target_vibe.lower()

    if entry_vibe.lower() == target_vibe.lower() or entry_vibe_short == target_vibe_short:
        score += 2
    elif entry_vibe_short in VIBE_SIMILARITY.get(target_vibe_short, []):
        score += 1

    return score


def select_matches(
    entries: list,
    industry: str,
    vibe: str,
    top_n: int = DEFAULT_RESULTS,
) -> list:
    """
    Select the top matching design systems. Returns between MIN_RESULTS and
    MAX_RESULTS entries, sorted by score descending then alphabetically.
    """
    # Clamp top_n to valid range
    top_n = max(MIN_RESULTS, min(MAX_RESULTS, top_n))

    scored = []
    for entry in entries:
        s = score_entry(entry, industry, vibe)
        scored.append((s, entry))

    # Sort by score descending, then alphabetically by site name
    scored.sort(key=lambda x: (-x[0], x[1].get("domain", x[1].get("site", ""))))

    # Take top_n, but ensure we have at least MIN_RESULTS if available
    results = scored[:top_n]

    # If we have fewer than MIN_RESULTS with score > 0, pad with top-scored
    high_score_results = [r for r in results if r[0] > 0]
    if len(high_score_results) < MIN_RESULTS and len(scored) >= MIN_RESULTS:
        results = scored[:MIN_RESULTS]

    return results


# =============================================================================
# Output formatting
# =============================================================================

def format_result_text(scored_results: list, industry: str, vibe: str) -> str:
    """Format results as human-readable text."""
    lines = []
    lines.append(f"Design System Matches: industry={industry}, vibe={vibe}")
    lines.append(f"{'=' * 60}")
    lines.append("")

    if not scored_results:
        lines.append("No matches found. Try broadening your criteria.")
        return "\n".join(lines)

    for i, (score, entry) in enumerate(scored_results, 1):
        site = entry.get("domain", entry.get("site", "unknown"))
        entry_industry = entry.get("industry", "Unknown")
        entry_vibe = entry.get("vibe", "unknown")

        # Score breakdown
        ind_match = ""
        if entry_industry.lower() == industry.lower():
            ind_match = "exact"
        elif entry_industry in INDUSTRY_ADJACENCY.get(industry, []):
            ind_match = "adjacent"
        else:
            ind_match = "none"

        entry_vibe_short = entry_vibe.split("-")[0].lower() if "-" in entry_vibe else entry_vibe.lower()
        target_vibe_short = vibe.split("-")[0].lower() if "-" in vibe else vibe.lower()
        vibe_match = ""
        if entry_vibe.lower() == vibe.lower() or entry_vibe_short == target_vibe_short:
            vibe_match = "exact"
        elif entry_vibe_short in VIBE_SIMILARITY.get(target_vibe_short, []):
            vibe_match = "similar"
        else:
            vibe_match = "none"

        lines.append(f"  {i}. {site}")
        lines.append(f"     Score: {score}/5  |  Industry: {entry_industry} ({ind_match})  |  Vibe: {entry_vibe} ({vibe_match})")

        # Show key design tokens — support both nested (tokens.typography) and flat (typography) formats
        tokens = entry.get("tokens", {})
        typo = tokens.get("typography", entry.get("typography", {}))
        colors_light = tokens.get("colors", entry.get("colors", {})).get("light", {})

        lines.append(f"     Fonts: {typo.get('heading_font', 'N/A')} / {typo.get('body_font', 'N/A')}")
        lines.append(f"     Accent: {colors_light.get('accent', 'N/A')}  |  BG: {colors_light.get('bg_primary', 'N/A')}")

        gradients = tokens.get("gradients", entry.get("gradients", []))
        if gradients:
            lines.append(f"     Gradient: {gradients[0]}")

        lines.append("")

    lines.append(f"Showing {len(scored_results)} of {len(scored_results)} matches.")
    lines.append(f"Use --json for machine-readable output.")
    return "\n".join(lines)


def format_result_json(scored_results: list, industry: str, vibe: str) -> str:
    """Format results as JSON."""
    output = {
        "query": {
            "industry": industry,
            "vibe": vibe,
        },
        "results": [],
    }

    for score, entry in scored_results:
        result = {
            "score": score,
            "domain": entry.get("domain", entry.get("site")),
            "industry": entry.get("industry"),
            "vibe": entry.get("vibe"),
        }
        # Include full token data — support both nested and flat formats
        if "tokens" in entry:
            result["tokens"] = entry["tokens"]
        else:
            # Flat format: collect token fields directly
            for key in ("typography", "colors", "spacing", "border_radius",
                        "shadows", "motion", "notable_effects", "dark_mode",
                        "tech_stack_observed"):
                if key in entry:
                    result[key] = entry[key]
        output["results"].append(result)

    return json.dumps(output, indent=2, ensure_ascii=False)


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Find matching design systems by industry and vibe.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --industry "Developer Tools" --vibe dark
  %(prog)s --industry "Fintech / Payments" --vibe minimal --top 8
  %(prog)s --industry "AI / ML" --vibe bold --json
  %(prog)s --list-industries
  %(prog)s --list-vibes
        """,
    )
    parser.add_argument(
        "--industry",
        type=str,
        help="Target industry vertical (e.g., 'Developer Tools', 'Fintech / Payments')",
    )
    parser.add_argument(
        "--vibe",
        type=str,
        choices=ACCEPTED_VIBES,
        help=f"Target design vibe ({', '.join(ACCEPTED_VIBES)})",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"Path to design-tokens-db.json (default: {DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=DEFAULT_RESULTS,
        help=f"Number of results to return ({MIN_RESULTS}-{MAX_RESULTS}, default: {DEFAULT_RESULTS})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON instead of human-readable text",
    )
    parser.add_argument(
        "--list-industries",
        action="store_true",
        help="List all known industry verticals and exit",
    )
    parser.add_argument(
        "--list-vibes",
        action="store_true",
        help="List all known vibes with descriptions and exit",
    )

    args = parser.parse_args()

    # Handle --list-industries
    if args.list_industries:
        print("Known Industry Verticals:")
        print("-" * 40)
        for ind in sorted(INDUSTRY_ADJACENCY.keys()):
            adjacent = ", ".join(INDUSTRY_ADJACENCY[ind])
            print(f"  {ind}")
            print(f"    Adjacent to: {adjacent}")
        sys.exit(0)

    # Handle --list-vibes
    if args.list_vibes:
        vibe_descriptions = {
            "dark": "Dark backgrounds, high contrast, moody aesthetic (e.g., Linear, Vercel)",
            "bold": "Bright saturated accents, strong visual presence (e.g., Stripe, Lemon Squeezy)",
            "minimal": "Clean, muted palette, restrained color use (e.g., Notion, Cal.com)",
            "playful": "Multiple bright colors, energetic, approachable (e.g., Monday, ClickUp)",
            "enterprise": "Navy/gray palette, professional, corporate trust (e.g., Datadog, Auth0)",
        }
        print("Design Vibes:")
        print("-" * 60)
        for v in ALL_VIBES:
            similar = ", ".join(VIBE_SIMILARITY.get(v, []))
            print(f"  {v}")
            print(f"    {vibe_descriptions.get(v, 'No description')}")
            print(f"    Similar to: {similar}")
            print()
        sys.exit(0)

    # Validate required arguments
    if not args.industry or not args.vibe:
        parser.error("Both --industry and --vibe are required (or use --list-industries / --list-vibes)")

    # Load database
    if not args.db.exists():
        print(f"ERROR: Database not found at {args.db}", file=sys.stderr)
        print("Run parse-tokens.py first to generate the database.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.db, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"ERROR: Failed to load database: {e}", file=sys.stderr)
        sys.exit(1)

    # Support both wrapped format {"sites": [...]} and flat array [...]
    if isinstance(raw, dict) and "sites" in raw:
        entries = raw["sites"]
    elif isinstance(raw, list):
        entries = raw
    else:
        print("ERROR: Database should be a JSON array or {\"sites\": [...]}.", file=sys.stderr)
        sys.exit(1)

    if not entries:
        print("ERROR: Database is empty. Run parse-tokens.py first.", file=sys.stderr)
        sys.exit(1)

    # Validate industry exists in database (warn but don't fail)
    known_industries = set(e.get("industry", "") for e in entries)
    if args.industry not in known_industries:
        matching = [ind for ind in known_industries if args.industry.lower() in ind.lower()]
        if matching:
            print(f"WARNING: '{args.industry}' not found exactly. Did you mean: {', '.join(matching)}?",
                  file=sys.stderr)
        else:
            print(f"WARNING: '{args.industry}' not found in database. Available: {', '.join(sorted(known_industries))}",
                  file=sys.stderr)

    # Select matches
    results = select_matches(entries, args.industry, args.vibe, args.top)

    # Output
    if args.json_output:
        print(format_result_json(results, args.industry, args.vibe))
    else:
        print(format_result_text(results, args.industry, args.vibe))


if __name__ == "__main__":
    main()
