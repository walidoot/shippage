#!/bin/bash
# =============================================================================
# detect-stack.sh - Detect the tech stack of a given website
# =============================================================================
# Uses Dembrandt to analyze a website and extract detected technologies,
# frameworks, and libraries.
#
# Prerequisites:
#   npm install -g dembrandt
#   python3 (stdlib only)
#
# Usage:
#   ./scripts/detect-stack.sh <url>
#   ./scripts/detect-stack.sh stripe.com
#   ./scripts/detect-stack.sh https://vercel.com
#
# Output:
#   Prints detected technologies one per line to stdout.
#   JSON report saved to output/<sanitized-url>/
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$PROJECT_DIR/output"

# ---------------------------------------------------------------------------
# Argument validation
# ---------------------------------------------------------------------------
if [ $# -eq 0 ] || [ -z "${1:-}" ]; then
  echo "Usage: $0 <url>"
  echo ""
  echo "Examples:"
  echo "  $0 stripe.com"
  echo "  $0 https://linear.app"
  echo "  $0 vercel.com"
  echo ""
  echo "Detects frameworks, libraries, and technologies used by a website."
  exit 1
fi

URL="$1"

# Strip protocol for display, but keep it for dembrandt
DISPLAY_URL="${URL#https://}"
DISPLAY_URL="${DISPLAY_URL#http://}"

# ---------------------------------------------------------------------------
# Preflight checks
# ---------------------------------------------------------------------------
if ! command -v dembrandt &>/dev/null; then
  echo "ERROR: dembrandt is not installed."
  echo "Install it with: npm install -g dembrandt"
  exit 1
fi

if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 is required but not found."
  exit 1
fi

# ---------------------------------------------------------------------------
# Run Dembrandt extraction
# ---------------------------------------------------------------------------
echo "Analyzing: $DISPLAY_URL" >&2
echo "---" >&2

mkdir -p "$OUTPUT_DIR"

if ! dembrandt "$URL" --json-only --save-output 2>/dev/null; then
  echo "WARNING: dembrandt extraction encountered errors for $DISPLAY_URL" >&2
fi

# ---------------------------------------------------------------------------
# Locate the output file
# ---------------------------------------------------------------------------
# Dembrandt may use various directory naming conventions, so we try multiple
# patterns to find the report JSON.
# Use the same sanitization as extract-tokens.sh (strip protocol, then sanitize)
SANITIZED="$(echo "$DISPLAY_URL" | sed 's|https\?://||' | sed 's|[^a-zA-Z0-9.]|_|g' | sed 's|_*$||')"

# Search for any JSON file in likely output locations
shopt -s nullglob
REPORT_FILE=""
for candidate in \
  "$OUTPUT_DIR/$SANITIZED/report.json" \
  "$OUTPUT_DIR/$SANITIZED/"*.json \
  "$OUTPUT_DIR/${SANITIZED}_dark/report.json" \
  "output/$SANITIZED/report.json" \
  "output/$SANITIZED/"*.json; do
  if [ -f "$candidate" ]; then
    REPORT_FILE="$candidate"
    break
  fi
done
shopt -u nullglob

if [ -z "$REPORT_FILE" ] || [ ! -f "$REPORT_FILE" ]; then
  echo "No report file found for $DISPLAY_URL." >&2
  echo "" >&2
  echo "Possible reasons:" >&2
  echo "  - dembrandt failed to extract data" >&2
  echo "  - The site may block automated access" >&2
  echo "  - Check output directory: $OUTPUT_DIR/$SANITIZED/" >&2
  exit 1
fi

echo "Report: $REPORT_FILE" >&2
echo "---" >&2

# ---------------------------------------------------------------------------
# Parse and display detected technologies
# ---------------------------------------------------------------------------
python3 - "$REPORT_FILE" <<'PYEOF'
import json
import sys
import os

report_path = sys.argv[1]

try:
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except (json.JSONDecodeError, OSError) as e:
    print(f"ERROR: Could not parse {report_path}: {e}", file=sys.stderr)
    sys.exit(1)

# Dembrandt may store technologies under different keys depending on version
tech_keys = [
    "technologies",
    "detected_stack",
    "tech_stack",
    "frameworks",
    "stack",
    "detectedTechnologies",
]

technologies = []
for key in tech_keys:
    val = data.get(key)
    if val:
        if isinstance(val, list):
            technologies.extend(val)
        elif isinstance(val, dict):
            for category, items in val.items():
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            name = item.get("name", item.get("technology", str(item)))
                            technologies.append(f"{category}: {name}")
                        else:
                            technologies.append(f"{category}: {item}")
                else:
                    technologies.append(f"{category}: {items}")

# Deduplicate while preserving order
seen = set()
unique = []
for t in technologies:
    t_str = str(t).strip()
    if t_str and t_str.lower() not in seen:
        seen.add(t_str.lower())
        unique.append(t_str)

if unique:
    print(f"Detected {len(unique)} technologies for {os.path.basename(os.path.dirname(report_path))}:\n", file=sys.stderr)
    for tech in unique:
        print(tech)
else:
    # Fall back to dumping top-level keys for inspection
    print("No technology data found in standard fields.", file=sys.stderr)
    print("Available report keys:", file=sys.stderr)
    for key in sorted(data.keys()):
        val = data[key]
        preview = str(val)[:80] if not isinstance(val, (dict, list)) else f"({type(val).__name__}, {len(val)} items)"
        print(f"  {key}: {preview}", file=sys.stderr)
PYEOF
