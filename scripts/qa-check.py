#!/usr/bin/env python3
"""
qa-check.py - Quality assurance checker for generated SaaS landing pages
========================================================================

Scans a generated project directory and scores it across eight quality
categories (100 points total):

  File Structure          10 pts  - Required files and directories
  Mobile Responsiveness   15 pts  - Tailwind responsive class patterns
  Images & Fonts          15 pts  - Image optimization, font loading
  Semantic HTML           15 pts  - Heading hierarchy, landmark elements
  CSS & Tokens            10 pts  - CSS custom properties, no hardcoded hex
  Meta & SEO              15 pts  - Title, description, OG tags, lang attr
  Performance             10 pts  - Dynamic/lazy imports, reduced-motion, aria
  Conversion              10 pts  - CTA count, social proof, banned words

Supports multiple frameworks via --framework flag:
  nextjs (default), vite, remix, astro

Usage:
  python3 scripts/qa-check.py --dir sites/my-saas/out
  python3 scripts/qa-check.py --dir /path/to/project --framework vite
  python3 scripts/qa-check.py --dir sites/my-saas/out --json
  python3 scripts/qa-check.py --dir sites/my-saas/out --verbose
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# =============================================================================
# Constants
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

BANNED_WORDS = [
    "leverage",
    "unlock",
    "revolutionize",
    "seamlessly",
    "cutting-edge",
    "game-changing",
    "elevate",
    "empower",
    "streamline",
    "robust",
    "innovative",
    "comprehensive",
    "holistic",
    "transform",
    "supercharge",
]

# Symbols for pass/fail
SYM_PASS = "✓"
SYM_FAIL = "✗"


# =============================================================================
# File helpers
# =============================================================================

SKIP_DIRS = {"node_modules", ".next", ".git", "dist", ".turbo", ".vercel", "__pycache__"}


def find_files(directory: Path, extension: str) -> list:
    """Recursively find all files with a given extension under directory."""
    results = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if fname.endswith(extension):
                results.append(Path(root) / fname)
    return results


def read_file(filepath: Path) -> str:
    """Read a file and return its contents, or empty string on failure."""
    try:
        return filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def file_exists(directory: Path, relative_path: str) -> bool:
    """Check if a file exists relative to the project directory."""
    return (directory / relative_path).is_file()


def dir_exists(directory: Path, relative_path: str) -> bool:
    """Check if a directory exists relative to the project directory."""
    return (directory / relative_path).is_dir()


# =============================================================================
# Scoring categories
# =============================================================================

class Category:
    """A scoring category that tracks points and issues."""

    def __init__(self, name: str, max_points: int):
        self.name = name
        self.max_points = max_points
        self.points = 0
        self.issues = []
        self.details = []
        self.checks_passed = 0
        self.checks_total = 0

    def check(self, passed: bool, points: int, fail_message: str, tag: str = ""):
        """Record a check result."""
        self.checks_total += 1
        if passed:
            self.points += points
            self.checks_passed += 1
            self.details.append((True, tag, f"+{points}pts", "OK"))
        else:
            self.issues.append((tag, fail_message))
            self.details.append((False, tag, f"0/{points}pts", fail_message))

    @property
    def score(self) -> int:
        return min(self.points, self.max_points)

    @property
    def passed(self) -> bool:
        return self.score == self.max_points

    def summary_line(self) -> str:
        status = SYM_PASS if self.passed else SYM_FAIL
        name_padded = f"{self.name}:".ljust(25)
        score_str = f"{self.score}/{self.max_points}"
        if self.passed:
            return f"{name_padded} {score_str}  {status} All checks passed"
        else:
            first_issue = self.issues[0][1] if self.issues else "Check failed"
            extras = f", +{len(self.issues) - 1} more" if len(self.issues) > 1 else ""
            return f"{name_padded} {score_str}  {status} {first_issue}{extras}"


# =============================================================================
# Check implementations
# =============================================================================

def check_file_structure(directory: Path, framework: str = "nextjs") -> Category:
    """
    File Structure (10 points):
      - package.json exists                     (2 pts)
      - tailwind.config exists                  (2 pts)
      - Layout/entry file exists                (2 pts)
      - Page/root component exists              (2 pts)
      - Global CSS file exists                  (1 pt)
      - components/ directory exists             (1 pt)
    """
    cat = Category("File Structure", 10)

    # Framework-specific expected files
    if framework == "vite":
        layout_file = "src/main.tsx"
        page_file = "src/App.tsx"
        css_file = "src/index.css"
    elif framework == "remix":
        layout_file = "app/root.tsx"
        page_file = "app/routes/_index.tsx"
        css_file = "app/globals.css"
    elif framework == "astro":
        layout_file = "src/layouts/Layout.astro"
        page_file = "src/pages/index.astro"
        css_file = "src/styles/global.css"
    else:  # nextjs (default)
        layout_file = "app/layout.tsx"
        page_file = "app/page.tsx"
        css_file = "app/globals.css"

    checks = [
        ("package.json", True, 2, "Missing package.json"),
        (None, True, 2, "Missing tailwind.config.{ts,js,mjs}"),  # special: multi-ext
        (layout_file, True, 2, f"Missing {layout_file}"),
        (page_file, True, 2, f"Missing {page_file}"),
        (css_file, True, 1, f"Missing {css_file}"),
        ("components", False, 1, "Missing components/ directory"),
    ]

    for path, is_file, points, msg in checks:
        if path is None:
            # Tailwind config: accept .ts, .js, .mjs
            found = any(
                file_exists(directory, f"tailwind.config.{ext}")
                for ext in ("ts", "js", "mjs")
            )
            cat.check(found, points, msg, "Structure")
        elif is_file:
            cat.check(file_exists(directory, path), points, msg, "Structure")
        else:
            cat.check(dir_exists(directory, path), points, msg, "Structure")

    return cat


def check_mobile_responsiveness(directory: Path) -> Category:
    """
    Mobile Responsiveness (15 points):
      - md: and lg: responsive prefixes found   (3 pts)
      - flex-col md:flex-row pattern             (3 pts)
      - w-full md:w-auto pattern                 (3 pts)
      - hidden md:block or block md:hidden       (3 pts)
      - px-4 md:px-8 padding pattern             (3 pts)
    """
    cat = Category("Mobile Responsiveness", 15)

    # Collect all TSX content from component files and page files
    tsx_files = find_files(directory, ".tsx")
    all_content = "\n".join(read_file(f) for f in tsx_files)

    if not all_content:
        cat.check(False, 3, "No .tsx files found to check", "Mobile")
        return cat

    patterns = [
        (r'(?:md|lg):', 3,
         'Missing responsive prefixes (md: or lg:)',
         'Add responsive Tailwind classes (md:, lg:) to component files'),
        (r'flex-col\s+md:flex-row', 3,
         'Missing "flex-col md:flex-row" responsive pattern',
         'Use "flex-col md:flex-row" for stacking on mobile'),
        (r'w-full\s+md:w-(?:auto|1/[23]|[0-9])', 3,
         'Missing "w-full md:w-auto" responsive pattern',
         'Use "w-full md:w-auto" for responsive width'),
        (r'(?:hidden\s+md:(?:block|flex|grid|inline))|(?:(?:block|flex)\s+md:hidden)', 3,
         'Missing "hidden md:block" or "block md:hidden" pattern',
         'Add "block md:hidden" for mobile-only elements'),
        (r'p[xy]-[0-9]+\s+(?:md|lg):p[xy]-[0-9]+', 3,
         'Missing responsive padding pattern (e.g., px-4 md:px-8)',
         'Use responsive padding like "px-4 md:px-8"'),
    ]

    for pattern, points, fail_short, fail_detail in patterns:
        found = bool(re.search(pattern, all_content))
        cat.check(found, points, fail_short, "Mobile")

    return cat


def check_images_and_fonts(directory: Path, framework: str = "nextjs") -> Category:
    """
    Images & Fonts (15 points):
      Next.js:
        - next/image usage (not raw <img>)       (4 pts)
        - next/font usage in layout.tsx          (4 pts)
        - No external font CDN URLs              (4 pts)
        - Images have width/height or fill        (3 pts)
      Other frameworks:
        - <img> tags have width + height attrs   (4 pts)
        - <img> tags have alt attributes         (4 pts)
        - No external font CDN URLs              (4 pts)
        - <img> tags have loading="lazy"          (3 pts)
    """
    cat = Category("Images & Fonts", 15)

    tsx_files = find_files(directory, ".tsx")
    all_tsx_content = "\n".join(read_file(f) for f in tsx_files)

    if framework == "nextjs":
        # --- Next.js-specific checks ---
        layout_path = directory / "app" / "layout.tsx"
        layout_content = read_file(layout_path)

        # Check next/image usage: no raw <img> in tsx files
        has_raw_img = bool(re.search(r'<img\s', all_tsx_content))
        has_next_image = "next/image" in all_tsx_content
        if has_raw_img:
            cat.check(False, 4, 'Found raw <img> tags; use next/image instead', "Images")
        elif has_next_image:
            cat.check(True, 4, "", "Images")
        else:
            cat.check(True, 4, "", "Images")

        # Check next/font usage in layout
        has_next_font = "next/font" in layout_content
        cat.check(has_next_font, 4, "Not using next/font in layout.tsx", "Fonts")

        # Check for external font CDN
        has_font_cdn = bool(re.search(
            r'fonts\.googleapis\.com|fonts\.gstatic\.com|use\.typekit\.net',
            all_tsx_content + layout_content,
        ))
        cat.check(not has_font_cdn, 4,
                  "Found external font CDN URL; use next/font instead", "Fonts")

        # Check image dimensions
        if "next/image" in all_tsx_content:
            image_usages = re.findall(r'<Image[^>]+>', all_tsx_content, re.DOTALL)
            if image_usages:
                all_have_dims = all(
                    re.search(r'(?:width|height|fill)', usage)
                    for usage in image_usages
                )
                cat.check(all_have_dims, 3,
                          "Some <Image> components missing width/height or fill prop",
                          "Images")
            else:
                cat.check(True, 3, "", "Images")
        else:
            has_any_image = "<img" in all_tsx_content.lower() or "Image" in all_tsx_content
            cat.check(not has_any_image, 3,
                      "Images found but not using next/image component", "Images")
    else:
        # --- Generic framework checks (vite, remix, astro) ---
        img_tags = re.findall(r'<img\s[^>]*>', all_tsx_content, re.DOTALL)

        if not img_tags:
            # No images — pass all checks
            cat.check(True, 4, "", "Images")
            cat.check(True, 4, "", "Images")
            cat.check(True, 4, "", "Fonts")
            cat.check(True, 3, "", "Images")
        else:
            # Check width + height attributes on <img> tags
            all_have_dims = all(
                re.search(r'\bwidth\b', tag) and re.search(r'\bheight\b', tag)
                for tag in img_tags
            )
            cat.check(all_have_dims, 4,
                      "Some <img> tags missing width/height attributes (causes CLS)",
                      "Images")

            # Check alt attributes on <img> tags
            all_have_alt = all(
                re.search(r'\balt\s*=', tag) for tag in img_tags
            )
            cat.check(all_have_alt, 4,
                      "Some <img> tags missing alt attribute (accessibility)",
                      "Images")

            # Check for external font CDN
            has_font_cdn = bool(re.search(
                r'fonts\.googleapis\.com|fonts\.gstatic\.com|use\.typekit\.net',
                all_tsx_content,
            ))
            cat.check(not has_font_cdn, 4,
                      "Found external font CDN URL; use local fonts or fontsource",
                      "Fonts")

            # Check loading="lazy" on <img> tags
            all_have_lazy = all(
                re.search(r'loading\s*=\s*["\']lazy["\']', tag) for tag in img_tags
            )
            cat.check(all_have_lazy, 3,
                      'Some <img> tags missing loading="lazy" attribute',
                      "Images")

    return cat


def check_semantic_html(directory: Path) -> Category:
    """
    Semantic HTML (15 points):
      - Exactly 1 <h1> in page.tsx               (3 pts)
      - Heading hierarchy (no h3 without h2)      (3 pts)
      - <main> tag present                        (3 pts)
      - <nav> tag present                         (2 pts)
      - <footer> tag present                      (2 pts)
      - <section> tags used for page sections     (2 pts)
    """
    cat = Category("Semantic HTML", 15)

    page_path = directory / "app" / "page.tsx"
    page_content = read_file(page_path)

    # Also check components for semantic elements
    tsx_files = find_files(directory, ".tsx")
    all_tsx_content = "\n".join(read_file(f) for f in tsx_files)

    # Check exactly 1 <h1>
    h1_count = len(re.findall(r'<h1[\s>]', all_tsx_content))
    if h1_count == 0:
        cat.check(False, 3, "No <h1> found in page", "HTML")
    elif h1_count > 1:
        cat.check(False, 3, f"Found {h1_count} <h1> tags; should be exactly 1", "HTML")
    else:
        cat.check(True, 3, "", "HTML")

    # Check heading hierarchy: no h3 without h2
    has_h2 = bool(re.search(r'<h2[\s>]', all_tsx_content))
    has_h3 = bool(re.search(r'<h3[\s>]', all_tsx_content))
    if has_h3 and not has_h2:
        cat.check(False, 3, "Found <h3> without <h2>; fix heading hierarchy", "HTML")
    else:
        cat.check(True, 3, "", "HTML")

    # Check <main> tag
    has_main = bool(re.search(r'<main[\s>]', all_tsx_content))
    cat.check(has_main, 3, "Missing <main> tag; wrap page content in <main>", "HTML")

    # Check <nav> tag
    has_nav = bool(re.search(r'<nav[\s>]', all_tsx_content))
    cat.check(has_nav, 2, "Missing <nav> tag for navigation", "HTML")

    # Check <footer> tag
    has_footer = bool(re.search(r'<footer[\s>]', all_tsx_content))
    cat.check(has_footer, 2, "Missing <footer> tag", "HTML")

    # Check <section> tags
    section_count = len(re.findall(r'<section[\s>]', all_tsx_content))
    cat.check(section_count >= 2, 2,
              "Fewer than 2 <section> tags; use <section> for page sections",
              "HTML")

    return cat


def check_css_tokens(directory: Path) -> Category:
    """
    CSS & Tokens (10 points):
      - CSS custom properties in globals.css      (4 pts)
      - No hardcoded hex colors in components     (3 pts)
      - Tailwind config has theme.extend          (3 pts)
    """
    cat = Category("CSS & Tokens", 10)

    globals_path = directory / "app" / "globals.css"
    globals_content = read_file(globals_path)

    tailwind_content = ""
    for ext in ("ts", "js", "mjs"):
        candidate = directory / f"tailwind.config.{ext}"
        if candidate.is_file():
            tailwind_content = read_file(candidate)
            break

    # Check CSS custom properties (support both --background and --color-background patterns)
    has_custom_props = bool(re.search(
        r'--(?:color-)?(?:background|foreground|primary|accent|muted)',
        globals_content,
    ))
    cat.check(has_custom_props, 4,
              "Missing CSS custom properties (--background, --foreground, etc.) in globals.css",
              "CSS")

    # Check for hardcoded hex colors in component files (not in CSS/config)
    component_files = find_files(directory / "components", ".tsx") if dir_exists(directory, "components") else []
    component_content = "\n".join(read_file(f) for f in component_files)

    # Match hex colors in className strings but exclude CSS files and config
    # Look for patterns like #fff, #ffffff, #F5F5F5 in TSX JSX attributes
    hardcoded_hex = re.findall(
        r'(?:className|style)[^>]*#[0-9a-fA-F]{3,8}',
        component_content,
    )
    cat.check(len(hardcoded_hex) == 0, 3,
              "Found hardcoded hex color values in component files; use Tailwind classes",
              "CSS")

    # Check Tailwind config has theme.extend
    has_theme_extend = "theme" in tailwind_content and "extend" in tailwind_content
    cat.check(has_theme_extend, 3,
              "tailwind.config.ts missing theme.extend with custom values",
              "CSS")

    return cat


def check_meta_seo(directory: Path) -> Category:
    """
    Meta & SEO (15 points):
      - <title> or metadata.title in layout       (4 pts)
      - Meta description                           (4 pts)
      - Open Graph tags (og:title, og:description) (4 pts)
      - HTML lang attribute                        (3 pts)
    """
    cat = Category("Meta & SEO", 15)

    layout_path = directory / "app" / "layout.tsx"
    layout_content = read_file(layout_path)

    # Also check page.tsx for metadata exports
    page_path = directory / "app" / "page.tsx"
    page_content = read_file(page_path)
    combined = layout_content + "\n" + page_content

    # Check title
    has_title = bool(re.search(
        r'(?:title\s*[:=]|<title>|metadata.*title)',
        combined, re.DOTALL,
    ))
    cat.check(has_title, 4, "Missing page title in layout.tsx metadata", "SEO")

    # Check description
    has_description = bool(re.search(
        r'(?:description\s*[:=]|meta.*description|metadata.*description)',
        combined, re.DOTALL,
    ))
    cat.check(has_description, 4,
              "Missing meta description in layout.tsx metadata", "SEO")

    # Check Open Graph tags
    has_og = bool(re.search(
        r'(?:openGraph|og:title|og:description|"og"|opengraph)',
        combined, re.IGNORECASE,
    ))
    cat.check(has_og, 4,
              "Missing Open Graph tags (og:title, og:description)", "SEO")

    # Check lang attribute
    has_lang = bool(re.search(r'lang\s*=\s*["\']', layout_content))
    cat.check(has_lang, 3, "Missing HTML lang attribute in layout.tsx", "SEO")

    return cat


def check_performance(directory: Path, framework: str = "nextjs") -> Category:
    """
    Performance (10 points):
      - Dynamic/lazy imports for heavy components  (4 pts)
      - prefers-reduced-motion in globals.css      (3 pts)
      - aria-hidden on decorative elements         (3 pts)
    """
    cat = Category("Performance", 10)

    tsx_files = find_files(directory, ".tsx")
    all_tsx_content = "\n".join(read_file(f) for f in tsx_files)

    # Find globals CSS file based on framework
    if framework == "vite":
        globals_path = directory / "src" / "index.css"
    elif framework == "astro":
        globals_path = directory / "src" / "styles" / "global.css"
    else:
        globals_path = directory / "app" / "globals.css"
    globals_content = read_file(globals_path)

    # Check dynamic/lazy imports
    has_dynamic = bool(re.search(
        r'(?:dynamic\s*\(|next/dynamic)',
        all_tsx_content,
    ))
    has_lazy = bool(re.search(r'React\.lazy|lazy\(', all_tsx_content))
    if framework == "nextjs":
        cat.check(has_dynamic or has_lazy, 4,
                  "No dynamic() imports found for heavy components (use next/dynamic with ssr: false)",
                  "Perf")
    else:
        cat.check(has_lazy or has_dynamic, 4,
                  "No React.lazy() imports found for heavy components",
                  "Perf")

    # Check prefers-reduced-motion
    has_reduced_motion = "prefers-reduced-motion" in globals_content
    cat.check(has_reduced_motion, 3,
              "No @media (prefers-reduced-motion) found in globals.css", "Perf")

    # Check aria-hidden on decorative elements
    has_aria_hidden = "aria-hidden" in all_tsx_content
    cat.check(has_aria_hidden, 3,
              "No aria-hidden attributes found on decorative elements", "Perf")

    return cat


def check_conversion(directory: Path) -> Category:
    """
    Conversion (10 points):
      - At least 3 CTA buttons in page.tsx         (4 pts)
      - Social proof section exists                 (3 pts)
      - No banned AI words                          (3 pts)
    """
    cat = Category("Conversion", 10)

    page_path = directory / "app" / "page.tsx"
    page_content = read_file(page_path)

    tsx_files = find_files(directory, ".tsx")
    all_tsx_content = "\n".join(read_file(f) for f in tsx_files)

    # Check CTA buttons: look for elements with CTA-like text patterns
    cta_patterns = re.findall(
        r'(?:get\s+started|sign\s*up|start\s+(?:free|now|trial|building)|try\s+(?:free|it|now)'
        r'|book\s+(?:a\s+)?demo|request\s+(?:a\s+)?demo|join\s+(?:waitlist|now|free|beta)'
        r'|download|subscribe|buy\s+now|create\s+(?:account|free)|learn\s+more'
        r'|explore|see\s+(?:pricing|plans|how)|contact\s+(?:us|sales)'
        r'|schedule\s+(?:a\s+)?(?:call|demo)|claim\s+(?:your|free))',
        all_tsx_content,
        re.IGNORECASE,
    )
    cta_count = len(cta_patterns)
    cat.check(cta_count >= 3, 4,
              f"Found only {cta_count} CTA phrases; need at least 3 across sections",
              "Conversion")

    # Check social proof section
    has_social_proof = bool(re.search(
        r'(?:social[_-]?proof|logo[s_-]?(?:strip|bar|section|cloud)|trusted\s+by|'
        r'companies?\s+(?:that\s+)?(?:use|trust|love)|as\s+seen)',
        all_tsx_content,
        re.IGNORECASE,
    ))
    cat.check(has_social_proof, 3,
              "No social proof section detected", "Conversion")

    # Check banned AI words — only in visible text (strings/JSX), not in CSS/code
    # Strip style attributes, className props, and CSS blocks to reduce false positives
    text_content = re.sub(r'(?:className|style|css|transform|translate|scale|rotate)\s*[:=][^>}]*[>}]', '', all_tsx_content)
    lower_content = text_content.lower()
    found_banned = []
    for word in BANNED_WORDS:
        # Use word boundary matching to avoid partial matches
        if re.search(r'\b' + re.escape(word) + r'\b', lower_content):
            found_banned.append(word)

    if found_banned:
        word_list = ", ".join(f'"{w}"' for w in found_banned[:5])
        extras = f" (+{len(found_banned) - 5} more)" if len(found_banned) > 5 else ""
        cat.check(False, 3,
                  f"Found banned AI word(s): {word_list}{extras}",
                  "Copy")
    else:
        cat.check(True, 3, "", "Copy")

    return cat


# =============================================================================
# Report generation
# =============================================================================

def generate_report(categories: list, verbose: bool = False) -> str:
    """Generate the human-readable QA report."""
    total_score = sum(c.score for c in categories)
    total_max = sum(c.max_points for c in categories)

    lines = []
    lines.append("=== Shippage QA Report ===")
    lines.append(f"Score: {total_score}/{total_max}")
    lines.append("")

    for cat in categories:
        lines.append(cat.summary_line())
        if verbose:
            for passed, tag, pts, detail in cat.details:
                sym = SYM_PASS if passed else SYM_FAIL
                lines.append(f"    {sym} [{tag}] {pts} — {detail}")

    # Collect all issues
    all_issues = []
    for cat in categories:
        for tag, msg in cat.issues:
            all_issues.append((tag, msg))

    if all_issues:
        lines.append("")
        lines.append("Issues:")
        for i, (tag, msg) in enumerate(all_issues, 1):
            lines.append(f"  {i}. [{tag}] {msg}")
    else:
        lines.append("")
        lines.append("No issues found. Perfect score!")

    return "\n".join(lines)


def generate_json_report(categories: list) -> str:
    """Generate a machine-readable JSON QA report."""
    total_score = sum(c.score for c in categories)
    total_max = sum(c.max_points for c in categories)

    report = {
        "score": total_score,
        "max_score": total_max,
        "categories": [],
        "issues": [],
    }

    for cat in categories:
        report["categories"].append({
            "name": cat.name,
            "score": cat.score,
            "max_points": cat.max_points,
            "passed": cat.passed,
        })
        for tag, msg in cat.issues:
            report["issues"].append({
                "category": cat.name,
                "tag": tag,
                "message": msg,
            })

    return json.dumps(report, indent=2, ensure_ascii=False)


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Quality assurance checker for generated SaaS landing pages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Checks 8 quality categories (100 points total):
  File Structure          10 pts
  Mobile Responsiveness   15 pts
  Images & Fonts          15 pts
  Semantic HTML           15 pts
  CSS & Tokens            10 pts
  Meta & SEO              15 pts
  Performance             10 pts
  Conversion              10 pts

Examples:
  %(prog)s --dir sites/my-saas/out
  %(prog)s --dir /path/to/project --framework vite
  %(prog)s --dir sites/my-saas/out --json --verbose
        """,
    )
    parser.add_argument(
        "--dir",
        type=Path,
        required=True,
        help="Path to the generated project directory",
    )
    parser.add_argument(
        "--framework",
        choices=["nextjs", "vite", "remix", "astro"],
        default="nextjs",
        help="Target framework (default: nextjs). Adjusts file structure and image/font checks.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON instead of human-readable text",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed check information",
    )

    args = parser.parse_args()

    # Resolve the directory path
    target_dir = args.dir.resolve()

    if not target_dir.is_dir():
        print(f"ERROR: Directory not found: {target_dir}", file=sys.stderr)
        sys.exit(1)

    framework = args.framework

    # Quick sanity check: does it look like a project?
    has_package = file_exists(target_dir, "package.json")
    has_app_dir = dir_exists(target_dir, "app") or dir_exists(target_dir, "src")
    if not has_package and not has_app_dir:
        print(
            f"WARNING: {target_dir} does not appear to be a web project "
            f"(no package.json, app/, or src/ directory found).",
            file=sys.stderr,
        )

    if args.verbose:
        print(f"Scanning: {target_dir} (framework: {framework})")
        tsx_count = len(find_files(target_dir, ".tsx"))
        css_count = len(find_files(target_dir, ".css"))
        print(f"Found {tsx_count} .tsx files, {css_count} .css files")
        print()

    # Run all checks
    categories = [
        check_file_structure(target_dir, framework),
        check_mobile_responsiveness(target_dir),
        check_images_and_fonts(target_dir, framework),
        check_semantic_html(target_dir),
        check_css_tokens(target_dir),
        check_meta_seo(target_dir),
        check_performance(target_dir, framework),
        check_conversion(target_dir),
    ]

    # Output
    if args.json_output:
        print(generate_json_report(categories))
    else:
        print(generate_report(categories, verbose=args.verbose))

    # Exit with non-zero if score is below threshold
    total_score = sum(c.score for c in categories)
    if total_score < 70:
        sys.exit(1)


if __name__ == "__main__":
    main()
