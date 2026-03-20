#!/usr/bin/env python3
"""
parse-tokens.py - Distill Dembrandt JSON extractions into design token references
=================================================================================

Reads all JSON files from output/*/ directories (Dembrandt extraction output),
extracts and normalizes design tokens for each site, classifies industry and vibe,
and produces two reference files:

  references/design-systems.md     - Top 50 sites in YAML-like markdown format
  references/design-tokens-db.json - All sites as a JSON array

Prerequisites:
  - Run extract-tokens.sh first to populate the output/ directory
  - Python 3.7+ (stdlib only, no dependencies)

Usage:
  python3 scripts/parse-tokens.py
  python3 scripts/parse-tokens.py --output-dir output --sites-file sites/sites.txt
  python3 scripts/parse-tokens.py --top 50 --verbose
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# =============================================================================
# Defaults
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "output"
DEFAULT_SITES_FILE = PROJECT_DIR / "sites" / "sites.txt"
DEFAULT_REFERENCES_DIR = PROJECT_DIR / "references"
DEFAULT_TOP_N = 50


# =============================================================================
# Industry mapping from sites.txt
# =============================================================================

def parse_sites_file(sites_file: Path) -> dict:
    """
    Parse sites.txt to build a mapping of site domain -> industry vertical.
    Lines starting with # are vertical headers; subsequent lines are sites.
    """
    site_to_industry = {}
    current_industry = "Unknown"

    if not sites_file.exists():
        print(f"WARNING: Sites file not found at {sites_file}", file=sys.stderr)
        return site_to_industry

    with open(sites_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                # Extract industry name: "# Developer Tools" -> "Developer Tools"
                current_industry = line.lstrip("#").strip()
            else:
                # Normalize: strip protocol + trailing slashes, preserve paths
                domain = line.lower().strip().rstrip("/")
                if domain.startswith("http://"):
                    domain = domain[7:]
                elif domain.startswith("https://"):
                    domain = domain[8:]
                site_to_industry[domain] = current_industry
                # Also map just the domain part for fallback matching
                domain_only = domain.split("/")[0]
                if domain_only != domain and domain_only not in site_to_industry:
                    site_to_industry[domain_only] = current_industry
    return site_to_industry


# =============================================================================
# Vibe classification
# =============================================================================


def classify_vibe(tokens: dict) -> str:
    """
    Auto-classify a site's vibe based on its extracted design tokens.
    Rules:
      - Dark background color (#000-#333 or very low lightness) -> "dark"
      - Bright saturated accent color -> "bold"
      - Navy/dark gray bg + muted palette -> "enterprise"
      - Muted, desaturated palette with light bg -> "minimal"
      - Multiple saturated colors -> "playful"
    Falls back to "minimal" if no strong signal.
    """
    colors = tokens.get("colors", {})
    light = colors.get("light", {})
    dark_mode = colors.get("dark", {})

    bg_primary = light.get("bg_primary", "#ffffff").lower()
    accent = light.get("accent", "#000000").lower()
    text_primary = light.get("text_primary", "#000000").lower()
    text_muted = light.get("text_muted", "#666666").lower()

    # Check if the site primarily uses dark mode as default
    has_dark_bg = _is_dark_color(bg_primary)

    # Check accent saturation and brightness
    accent_saturated = _is_saturated(accent)
    accent_bright = _is_bright(accent)

    # Check if palette is muted overall
    palette_muted = not accent_saturated

    # Check for navy/corporate tones
    is_navy = _is_navy(bg_primary) or _is_navy(text_primary)

    # Multi-color detection (secondary accent differs significantly from primary)
    secondary_accent = light.get("secondary", light.get("accent_secondary", ""))
    multi_color = (
        secondary_accent
        and secondary_accent != accent
        and _is_saturated(secondary_accent)
    )

    # Scoring
    scores = {
        "dark": 0,
        "bold": 0,
        "minimal": 0,
        "playful": 0,
        "enterprise": 0,
    }

    if has_dark_bg:
        scores["dark"] += 3
    if accent_bright and accent_saturated:
        scores["bold"] += 2
    if is_navy:
        scores["enterprise"] += 2
    if palette_muted and not has_dark_bg:
        scores["minimal"] += 2
    if multi_color:
        scores["playful"] += 2
    if not accent_saturated and not has_dark_bg:
        scores["minimal"] += 1
    if has_dark_bg and accent_saturated:
        scores["bold"] += 1

    # Gradient presence often signals bold or playful
    gradients = tokens.get("gradients", [])
    if gradients:
        scores["bold"] += 1
        scores["playful"] += 1

    # Pick the highest scoring vibe
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "minimal"
    return best


def _hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to (r, g, b) tuple. Returns (128,128,128) on failure."""
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    if len(hex_color) != 6:
        return (128, 128, 128)
    try:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return (128, 128, 128)


def _rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    """Convert RGB (0-255) to HSL (h: 0-360, s: 0-100, l: 0-100)."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2.0

    if mx == mn:
        h = s = 0.0
    else:
        d = mx - mn
        s = d / (2.0 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6.0

    return (h * 360, s * 100, l * 100)


def _is_dark_color(hex_color: str) -> bool:
    """Check if a color is dark (lightness < 20)."""
    if not hex_color or hex_color in ("#", ""):
        return False
    r, g, b = _hex_to_rgb(hex_color)
    _, _, l = _rgb_to_hsl(r, g, b)
    return l < 20


def _is_navy(hex_color: str) -> bool:
    """Check if a color is a navy/dark blue."""
    if not hex_color or hex_color in ("#", ""):
        return False
    r, g, b = _hex_to_rgb(hex_color)
    h, s, l = _rgb_to_hsl(r, g, b)
    return 200 <= h <= 260 and s > 30 and l < 40


def _is_saturated(hex_color: str) -> bool:
    """Check if a color has high saturation."""
    if not hex_color or hex_color in ("#", ""):
        return False
    r, g, b = _hex_to_rgb(hex_color)
    _, s, _ = _rgb_to_hsl(r, g, b)
    return s > 50


def _is_bright(hex_color: str) -> bool:
    """Check if a color is bright (high lightness or high value)."""
    if not hex_color or hex_color in ("#", ""):
        return False
    r, g, b = _hex_to_rgb(hex_color)
    _, _, l = _rgb_to_hsl(r, g, b)
    return l > 40


# =============================================================================
# Token extraction from Dembrandt JSON
# =============================================================================

def extract_tokens_from_json(data: dict, is_dark_mode: bool = False) -> dict:
    """
    Extract and normalize design tokens from a single Dembrandt JSON report.
    Handles various Dembrandt output schemas gracefully with sensible defaults.
    """

    tokens = {}

    # --- Typography -----------------------------------------------------------
    typography = data.get("typography", data.get("fonts", {}))
    if isinstance(typography, list):
        # Some versions output a list of font usages
        typography = _list_to_typography(typography)

    heading_font = _deep_get(typography, "heading.family", "headingFont", "heading_font",
                              "h1.fontFamily", "h1.family", default="Inter")
    heading_weight = _deep_get(typography, "heading.weight", "headingWeight", "heading_weight",
                                "h1.fontWeight", "h1.weight", default="700")
    body_font = _deep_get(typography, "body.family", "bodyFont", "body_font",
                           "body.fontFamily", "paragraph.family", default="Inter")
    body_weight = _deep_get(typography, "body.weight", "bodyWeight", "body_weight",
                             "body.fontWeight", "paragraph.weight", default="400")
    h1_size = _deep_get(typography, "h1.size", "h1.fontSize", "heading.size",
                         "sizes.h1", default="48px")
    body_size = _deep_get(typography, "body.size", "body.fontSize", "paragraph.size",
                           "sizes.body", "sizes.p", default="16px")
    line_height_heading = _deep_get(typography, "heading.lineHeight", "h1.lineHeight",
                                     default="1.1")
    line_height_body = _deep_get(typography, "body.lineHeight", "paragraph.lineHeight",
                                  default="1.6")
    letter_spacing = _deep_get(typography, "heading.letterSpacing", "h1.letterSpacing",
                                "letterSpacing", default="-0.02em")

    tokens["typography"] = {
        "heading_font": _clean_font(heading_font),
        "heading_weight": str(heading_weight),
        "body_font": _clean_font(body_font),
        "body_weight": str(body_weight),
        "h1_size": _normalize_size(h1_size),
        "body_size": _normalize_size(body_size),
        "line_height_heading": str(line_height_heading),
        "line_height_body": str(line_height_body),
        "letter_spacing": str(letter_spacing),
    }

    # --- Colors ---------------------------------------------------------------
    colors_raw = data.get("colors", data.get("palette", data.get("colorPalette", {})))
    if isinstance(colors_raw, list):
        colors_raw = _list_to_colors(colors_raw)

    # Extract light and dark mode color sets
    light_colors = _extract_color_set(colors_raw, "light", data)
    dark_colors = _extract_color_set(colors_raw, "dark", data)

    tokens["colors"] = {
        "light": light_colors,
        "dark": dark_colors,
    }

    # --- Gradients ------------------------------------------------------------
    gradients_raw = data.get("gradients", data.get("gradient", []))
    if isinstance(gradients_raw, str):
        gradients_raw = [gradients_raw]
    elif isinstance(gradients_raw, dict):
        gradients_raw = list(gradients_raw.values())

    tokens["gradients"] = [str(g) for g in gradients_raw[:5]] if gradients_raw else []

    # --- Spacing --------------------------------------------------------------
    spacing_raw = data.get("spacing", data.get("layout", {}))
    tokens["spacing"] = {
        "section_padding": _deep_get(spacing_raw, "sectionPadding", "section_padding",
                                      "section.padding", "verticalRhythm", default="80px 0"),
        "container_max_width": _deep_get(spacing_raw, "containerMaxWidth", "container_max_width",
                                          "container.maxWidth", "maxWidth", default="1200px"),
        "card_padding": _deep_get(spacing_raw, "cardPadding", "card_padding",
                                   "card.padding", default="24px"),
        "card_gap": _deep_get(spacing_raw, "cardGap", "card_gap", "gap",
                               "card.gap", default="24px"),
    }

    # --- Border radius --------------------------------------------------------
    radius_raw = data.get("borderRadius", data.get("border_radius",
                  data.get("radius", data.get("borders", {}))))
    if isinstance(radius_raw, dict):
        tokens["border_radius"] = _deep_get(radius_raw, "default", "base", "card",
                                              "md", default="12px")
    elif isinstance(radius_raw, (str, int, float)):
        tokens["border_radius"] = _normalize_size(str(radius_raw))
    else:
        tokens["border_radius"] = "12px"

    # --- Shadows --------------------------------------------------------------
    shadows_raw = data.get("shadows", data.get("boxShadow", data.get("box_shadows", [])))
    if isinstance(shadows_raw, str):
        tokens["shadows"] = [shadows_raw]
    elif isinstance(shadows_raw, list):
        tokens["shadows"] = [str(s) for s in shadows_raw[:3]]
    elif isinstance(shadows_raw, dict):
        tokens["shadows"] = [str(v) for v in list(shadows_raw.values())[:3]]
    else:
        tokens["shadows"] = ["0 1px 3px rgba(0,0,0,0.1)", "0 4px 20px rgba(0,0,0,0.08)"]

    # --- Motion style ---------------------------------------------------------
    motion_raw = data.get("motion", data.get("animations", data.get("transitions", {})))
    if isinstance(motion_raw, dict):
        tokens["motion"] = _deep_get(motion_raw, "style", "type", "easing",
                                      "default", default="ease-out")
    elif isinstance(motion_raw, str):
        tokens["motion"] = motion_raw
    else:
        tokens["motion"] = "ease-out"

    return tokens


def _extract_color_set(colors_raw: dict, mode: str, full_data: dict) -> dict:
    """Extract a color set (light or dark) from various Dembrandt output formats."""

    defaults_light = {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f8f9fa",
        "text_primary": "#111111",
        "text_secondary": "#333333",
        "text_muted": "#666666",
        "accent": "#6366f1",
        "border": "#e5e7eb",
    }

    defaults_dark = {
        "bg_primary": "#0a0a0a",
        "bg_secondary": "#141414",
        "text_primary": "#f5f5f5",
        "text_secondary": "#d4d4d4",
        "text_muted": "#737373",
        "accent": "#818cf8",
        "border": "#262626",
    }

    defaults = defaults_dark if mode == "dark" else defaults_light

    # Try mode-specific sub-object first
    mode_colors = colors_raw.get(mode, colors_raw.get(f"{mode}Mode",
                   colors_raw.get(f"{mode}_mode", {})))

    # If no mode-specific colors, use the flat colors object for light mode
    if not mode_colors and mode == "light":
        mode_colors = colors_raw

    if not isinstance(mode_colors, dict):
        mode_colors = {}

    # Also check full_data for dark mode specific extraction
    if mode == "dark":
        dark_data = full_data.get("darkMode", full_data.get("dark_mode", {}))
        if isinstance(dark_data, dict):
            dark_colors = dark_data.get("colors", dark_data.get("palette", {}))
            if isinstance(dark_colors, dict):
                mode_colors = {**mode_colors, **dark_colors}

    return {
        "bg_primary": _find_color(mode_colors, "bg_primary", "background", "bgPrimary",
                                   "bg", "backgroundColor", default=defaults["bg_primary"]),
        "bg_secondary": _find_color(mode_colors, "bg_secondary", "backgroundSecondary",
                                     "bgSecondary", "bg2", "surfaceColor",
                                     default=defaults["bg_secondary"]),
        "text_primary": _find_color(mode_colors, "text_primary", "text", "textPrimary",
                                     "foreground", "color", default=defaults["text_primary"]),
        "text_secondary": _find_color(mode_colors, "text_secondary", "textSecondary",
                                       "text2", default=defaults["text_secondary"]),
        "text_muted": _find_color(mode_colors, "text_muted", "textMuted", "muted",
                                   "textTertiary", "text3", default=defaults["text_muted"]),
        "accent": _find_color(mode_colors, "accent", "primary", "accentColor",
                               "brandColor", "brand", "primaryColor", "cta",
                               default=defaults["accent"]),
        "border": _find_color(mode_colors, "border", "borderColor", "divider",
                               "separator", default=defaults["border"]),
    }


def _find_color(data: dict, *keys, default: str = "#000000") -> str:
    """Find a color value trying multiple possible key names."""
    for key in keys:
        val = data.get(key)
        if val and isinstance(val, str) and (val.startswith("#") or val.startswith("rgb")):
            return _normalize_color(val)
        # Try nested: "bg.primary"
        if "." in key:
            parts = key.split(".")
            nested = data
            for part in parts:
                if isinstance(nested, dict):
                    nested = nested.get(part)
                else:
                    nested = None
                    break
            if nested and isinstance(nested, str):
                return _normalize_color(nested)
    return default


def _normalize_color(color: str) -> str:
    """Normalize a color string to hex format where possible."""
    color = color.strip()
    if color.startswith("#"):
        hex_val = color.lstrip("#")
        if len(hex_val) == 3:
            hex_val = "".join(c * 2 for c in hex_val)
        elif len(hex_val) == 4:
            # 4-digit RGBA shorthand -> 6-digit RGB (drop alpha)
            hex_val = "".join(c * 2 for c in hex_val[:3])
        elif len(hex_val) == 8:
            # 8-digit RGBA -> 6-digit RGB (drop alpha bytes)
            hex_val = hex_val[:6]
        return f"#{hex_val[:6].lower()}"
    if color.startswith("rgb"):
        # Try to convert rgb(r,g,b) to hex
        nums = re.findall(r"\d+", color)
        if len(nums) >= 3:
            try:
                r, g, b = int(nums[0]), int(nums[1]), int(nums[2])
                return f"#{r:02x}{g:02x}{b:02x}"
            except (ValueError, IndexError):
                pass
    return color


def _list_to_typography(font_list: list) -> dict:
    """Convert a list-style typography output to a dict."""
    result = {}
    for item in font_list:
        if isinstance(item, dict):
            role = item.get("role", item.get("type", "")).lower()
            if "heading" in role or "h1" in role:
                result["heading"] = {
                    "family": item.get("family", item.get("fontFamily", "")),
                    "weight": item.get("weight", item.get("fontWeight", "")),
                    "size": item.get("size", item.get("fontSize", "")),
                    "lineHeight": item.get("lineHeight", ""),
                    "letterSpacing": item.get("letterSpacing", ""),
                }
            elif "body" in role or "paragraph" in role or "text" in role:
                result["body"] = {
                    "family": item.get("family", item.get("fontFamily", "")),
                    "weight": item.get("weight", item.get("fontWeight", "")),
                    "size": item.get("size", item.get("fontSize", "")),
                    "lineHeight": item.get("lineHeight", ""),
                }
    return result


def _list_to_colors(color_list: list) -> dict:
    """Convert a list-style color output to a dict."""
    result = {}
    for item in color_list:
        if isinstance(item, dict):
            name = item.get("name", item.get("role", item.get("type", ""))).lower()
            value = item.get("value", item.get("hex", item.get("color", "")))
            if name and value:
                result[name] = value
    return result


def _deep_get(data, *keys, default=None):
    """
    Try multiple possible key paths in a dict, returning the first match.
    Supports dot-notation for nested keys: "heading.family"
    """
    if not isinstance(data, dict):
        return default

    for key in keys:
        if "." in key:
            parts = key.split(".")
            val = data
            for part in parts:
                if isinstance(val, dict):
                    val = val.get(part)
                else:
                    val = None
                    break
            if val is not None and val != "":
                return val
        else:
            val = data.get(key)
            if val is not None and val != "":
                return val
    return default


def _clean_font(font: str) -> str:
    """Clean and normalize a font family name."""
    if not font or not isinstance(font, str):
        return "Inter"
    # Remove quotes
    font = font.strip().strip("'\"")
    # Take the first font from a font stack
    if "," in font:
        font = font.split(",")[0].strip().strip("'\"")
    return font or "Inter"


def _normalize_size(size) -> str:
    """Normalize a size value to include units."""
    size = str(size).strip()
    if not size:
        return "16px"
    # If it's just a number, add px
    try:
        num = float(size)
        return f"{int(num)}px" if num == int(num) else f"{num}px"
    except ValueError:
        return size


# =============================================================================
# File discovery and processing
# =============================================================================

def discover_sites(output_dir: Path) -> dict:
    """
    Discover all extracted sites and their JSON files.
    Returns {site_name: {"light": path, "dark": path}}
    """
    sites = {}

    if not output_dir.exists():
        print(f"ERROR: Output directory not found: {output_dir}", file=sys.stderr)
        return sites

    for site_dir in sorted(output_dir.iterdir()):
        if not site_dir.is_dir():
            continue

        dir_name = site_dir.name
        # Determine if this is a dark mode extraction
        is_dark = dir_name.endswith("_dark") or "_dark_" in dir_name
        base_name = re.sub(r"_dark$", "", dir_name)

        if base_name not in sites:
            sites[base_name] = {"light": None, "dark": None}

        # Find JSON files in this directory
        json_files = sorted(site_dir.glob("*.json"))
        if json_files:
            mode = "dark" if is_dark else "light"
            # Prefer report.json, then any other JSON
            report = site_dir / "report.json"
            sites[base_name][mode] = report if report.exists() else json_files[0]

    return sites


def dir_name_to_domain(dir_name: str) -> str:
    """Convert a sanitized directory name back to a domain-like string."""
    # Replace underscores back to dots/slashes where sensible
    # "stripe_com" -> "stripe.com", "vercel_com" -> "vercel.com"
    # Handle common TLDs
    for tld in [".com", ".app", ".dev", ".io", ".so", ".co", ".ai", ".sh",
                ".tech", ".design", ".rest"]:
        sanitized_tld = tld.replace(".", "_")
        if dir_name.endswith(sanitized_tld):
            prefix = dir_name[: -len(sanitized_tld)]
            return prefix.replace("_", ".") + tld

    # Fallback: replace the last underscore with a dot
    parts = dir_name.rsplit("_", 1)
    if len(parts) == 2:
        return f"{parts[0].replace('_', '-')}.{parts[1]}"
    return dir_name.replace("_", ".")


# =============================================================================
# Output generation
# =============================================================================

def generate_markdown(entries: list, output_path: Path, top_n: int = 50) -> None:
    """Generate the design-systems.md reference file in YAML-like format."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    limited = entries[:top_n]

    lines = []
    lines.append("# SaaS Design Systems Reference")
    lines.append(f"# Top {len(limited)} sites - auto-generated by parse-tokens.py")
    lines.append(f"# Source: Dembrandt design token extractions")
    lines.append("")
    lines.append("---")
    lines.append("")

    for entry in limited:
        lines.append(f"## {entry['site']}")
        lines.append(f"industry: {entry['industry']}")
        lines.append(f"vibe: {entry['vibe']}")
        lines.append("")

        # Typography
        typo = entry["tokens"]["typography"]
        lines.append("typography:")
        lines.append(f"  heading_font: {typo['heading_font']}")
        lines.append(f"  heading_weight: {typo['heading_weight']}")
        lines.append(f"  body_font: {typo['body_font']}")
        lines.append(f"  body_weight: {typo['body_weight']}")
        lines.append(f"  h1_size: {typo['h1_size']}")
        lines.append(f"  body_size: {typo['body_size']}")
        lines.append(f"  line_height_heading: {typo['line_height_heading']}")
        lines.append(f"  line_height_body: {typo['line_height_body']}")
        lines.append(f"  letter_spacing: {typo['letter_spacing']}")
        lines.append("")

        # Colors
        for mode in ("light", "dark"):
            colors = entry["tokens"]["colors"].get(mode, {})
            lines.append(f"colors_{mode}:")
            for key in ("bg_primary", "bg_secondary", "text_primary",
                        "text_secondary", "text_muted", "accent", "border"):
                lines.append(f"  {key}: {colors.get(key, 'N/A')}")
            lines.append("")

        # Gradients
        gradients = entry["tokens"].get("gradients", [])
        if gradients:
            lines.append("gradients:")
            for g in gradients:
                lines.append(f"  - {g}")
            lines.append("")

        # Spacing
        spacing = entry["tokens"]["spacing"]
        lines.append("spacing:")
        lines.append(f"  section_padding: {spacing['section_padding']}")
        lines.append(f"  container_max_width: {spacing['container_max_width']}")
        lines.append(f"  card_padding: {spacing['card_padding']}")
        lines.append(f"  card_gap: {spacing['card_gap']}")
        lines.append("")

        # Border radius, shadows, motion
        lines.append(f"border_radius: {entry['tokens']['border_radius']}")
        shadows = entry["tokens"].get("shadows", [])
        if shadows:
            lines.append("shadows:")
            for s in shadows:
                lines.append(f"  - {s}")
        lines.append(f"motion: {entry['tokens']['motion']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  Written: {output_path} ({len(limited)} entries)")


def generate_json(entries: list, output_path: Path) -> None:
    """Generate the design-tokens-db.json reference file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"  Written: {output_path} ({len(entries)} entries)")


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Distill Dembrandt JSON extractions into design token references."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory containing Dembrandt output (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--sites-file",
        type=Path,
        default=DEFAULT_SITES_FILE,
        help=f"Path to sites.txt for industry mapping (default: {DEFAULT_SITES_FILE})",
    )
    parser.add_argument(
        "--references-dir",
        type=Path,
        default=DEFAULT_REFERENCES_DIR,
        help=f"Output directory for reference files (default: {DEFAULT_REFERENCES_DIR})",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=DEFAULT_TOP_N,
        help=f"Number of sites to include in design-systems.md (default: {DEFAULT_TOP_N})",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed processing information",
    )
    args = parser.parse_args()

    print("=" * 60)
    print(" parse-tokens.py - Design Token Distillation")
    print("=" * 60)
    print(f"  Output dir:     {args.output_dir}")
    print(f"  Sites file:     {args.sites_file}")
    print(f"  References dir: {args.references_dir}")
    print()

    # Load industry mapping
    site_to_industry = parse_sites_file(args.sites_file)
    print(f"  Loaded {len(site_to_industry)} site->industry mappings")

    # Discover extracted sites
    sites = discover_sites(args.output_dir)
    if not sites:
        print("\nERROR: No extracted sites found.", file=sys.stderr)
        print(f"Run extract-tokens.sh first to populate {args.output_dir}/", file=sys.stderr)
        sys.exit(1)

    print(f"  Found {len(sites)} extracted sites")
    print()

    # Process each site
    entries = []
    errors = 0

    for dir_name, paths in sorted(sites.items()):
        # Prefer .url file for lossless reverse mapping
        url_file = args.output_dir / dir_name / ".url"
        if url_file.exists():
            domain = url_file.read_text(encoding="utf-8").strip()
        else:
            domain = dir_name_to_domain(dir_name)

        # Determine industry from sites.txt (try full URL first, then domain-only)
        domain_lower = domain.lower()
        industry = site_to_industry.get(domain_lower, "Unknown")
        if industry == "Unknown":
            domain_clean = domain_lower.split("/")[0]
            industry = site_to_industry.get(domain_clean, "Unknown")

        # Try to also match without subdomain
        if industry == "Unknown" and "." in domain_clean:
            parts = domain_clean.split(".")
            if len(parts) > 2:
                shorter = ".".join(parts[-2:])
                industry = site_to_industry.get(shorter, "Unknown")

        # Load and merge light + dark mode data
        merged_data = {}
        for mode in ("light", "dark"):
            json_path = paths.get(mode)
            if json_path and json_path.exists():
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if mode == "light":
                        merged_data = data
                    else:
                        # Merge dark mode data under a dark key
                        merged_data["darkMode"] = data
                except (json.JSONDecodeError, OSError) as e:
                    if args.verbose:
                        print(f"  WARNING: Failed to parse {json_path}: {e}", file=sys.stderr)
                    errors += 1

        if not merged_data:
            if args.verbose:
                print(f"  SKIP: No valid JSON for {domain}")
            errors += 1
            continue

        # Extract tokens
        try:
            tokens = extract_tokens_from_json(merged_data)
        except Exception as e:
            if args.verbose:
                print(f"  ERROR: Token extraction failed for {domain}: {e}", file=sys.stderr)
            errors += 1
            continue

        # Classify vibe
        vibe = classify_vibe(tokens)

        entry = {
            "site": domain,
            "industry": industry,
            "vibe": vibe,
            "tokens": tokens,
        }

        entries.append(entry)

        if args.verbose:
            print(f"  OK: {domain} [{industry}] [{vibe}]")

    print(f"\nProcessed: {len(entries)} sites successfully, {errors} errors")
    print()

    if not entries:
        print("ERROR: No sites were successfully processed.", file=sys.stderr)
        sys.exit(1)

    # Sort entries: prioritize sites with richer data (more non-default values)
    def richness_score(entry):
        """Score how much real (non-default) data an entry has."""
        score = 0
        tokens = entry["tokens"]
        typo = tokens["typography"]
        if typo["heading_font"] != "Inter":
            score += 2
        if typo["body_font"] != "Inter":
            score += 1
        colors = tokens["colors"]["light"]
        if colors["accent"] != "#6366f1":
            score += 2
        if colors["bg_primary"] != "#ffffff":
            score += 1
        if tokens["gradients"]:
            score += 1
        if entry["industry"] != "Unknown":
            score += 1
        return score

    entries.sort(key=richness_score, reverse=True)

    # Generate output files
    print("Generating reference files:")
    md_path = args.references_dir / "design-systems.md"
    json_path = args.references_dir / "design-tokens-db.json"

    generate_markdown(entries, md_path, top_n=args.top)
    generate_json(entries, json_path)

    print()
    print("Done! Reference files are ready for the design system selector.")
    print(f"  Next step: python3 scripts/select-design-system.py --industry 'Developer Tools' --vibe dark")


if __name__ == "__main__":
    main()
