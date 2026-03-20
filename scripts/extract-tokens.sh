#!/bin/bash
# =============================================================================
# extract-tokens.sh - Batch extract design tokens from SaaS websites
# =============================================================================
# Reads URLs from sites/sites.txt and runs Dembrandt against each one in both
# light and dark mode, saving JSON output for later parsing.
#
# Prerequisites:
#   npm install -g dembrandt
#
# Usage:
#   ./scripts/extract-tokens.sh                  # Extract all sites
#   ./scripts/extract-tokens.sh --resume         # Skip sites that already have output
#   ./scripts/extract-tokens.sh --site stripe.com # Extract a single site
#
# Recommended: run overnight on a dedicated machine
#   nohup ./scripts/extract-tokens.sh > extraction.log 2>&1 &
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SITES_FILE="$PROJECT_DIR/sites/sites.txt"
OUTPUT_DIR="$PROJECT_DIR/output"
SLEEP_BETWEEN=3
RESUME=false
SINGLE_SITE=""

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --resume)
      RESUME=true
      shift
      ;;
    --site)
      if [[ -z "${2:-}" || "${2:-}" == --* ]]; then
        echo "ERROR: --site requires a URL argument"
        exit 1
      fi
      SINGLE_SITE="$2"
      shift 2
      ;;
    --sleep)
      if [[ -z "${2:-}" || "${2:-}" == --* ]]; then
        echo "ERROR: --sleep requires a number argument"
        exit 1
      fi
      SLEEP_BETWEEN="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --resume          Skip sites that already have output files"
      echo "  --site <url>      Extract a single site instead of all"
      echo "  --sleep <secs>    Seconds to wait between requests (default: 3)"
      echo "  -h, --help        Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Run $0 --help for usage information."
      exit 1
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Preflight checks
# ---------------------------------------------------------------------------
if ! command -v dembrandt &>/dev/null; then
  echo "ERROR: dembrandt is not installed."
  echo "Install it with: npm install -g dembrandt"
  exit 1
fi

if [ ! -f "$SITES_FILE" ]; then
  echo "ERROR: Sites file not found at $SITES_FILE"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ---------------------------------------------------------------------------
# Counters (use $((var + 1)) to avoid set -e trap with ((var++)) when var=0)
# ---------------------------------------------------------------------------
total=0
success=0
failed=0
skipped=0

# ---------------------------------------------------------------------------
# Helper: sanitize URL to a filesystem-safe directory name
# Also writes a .url file so reverse mapping is lossless
# ---------------------------------------------------------------------------
sanitize_url() {
  echo "$1" | sed 's|https\?://||' | sed 's|[^a-zA-Z0-9.]|_|g' | sed 's|_*$||'
}

# ---------------------------------------------------------------------------
# Helper: validate URL format (reject anything that isn't https?://domain.tld)
# Prevents shell argument injection via malicious entries in sites.txt
# ---------------------------------------------------------------------------
validate_url() {
  local url="$1"
  if [[ ! "$url" =~ ^https?://[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}(/[a-zA-Z0-9_.~:/?#\[\]@!$\&\'()*+,;=%-]*)?$ ]]; then
    echo "WARNING: Invalid URL format, skipping: $url" >&2
    return 1
  fi
  return 0
}

# ---------------------------------------------------------------------------
# Helper: extract a single site
# ---------------------------------------------------------------------------
extract_site() {
  local site="$1"

  # Validate URL format before passing to external command
  if ! validate_url "$site"; then
    failed=$((failed + 1))
    return 0
  fi

  local sanitized
  sanitized="$(sanitize_url "$site")"
  local site_dir="$OUTPUT_DIR/$sanitized"

  # Resume mode: skip if output already exists
  if [ "$RESUME" = true ] && [ -d "$site_dir" ] && ls "$site_dir"/*.json &>/dev/null 2>&1; then
    echo "$(date '+%H:%M:%S') SKIP (already extracted): $site"
    skipped=$((skipped + 1))
    return 0
  fi

  echo "$(date '+%H:%M:%S') Extracting: $site"
  total=$((total + 1))

  mkdir -p "$site_dir"

  # Write .url file for lossless reverse mapping (used by parse-tokens.py)
  echo "$site" > "$site_dir/.url"

  local light_ok=false
  local dark_ok=false

  # Light mode extraction
  if dembrandt "$site" --json-only --output-dir "$site_dir" 2>/dev/null; then
    echo "$(date '+%H:%M:%S')   [OK] light mode"
    light_ok=true
  else
    echo "$(date '+%H:%M:%S')   [FAIL] light mode: $site"
  fi

  # Dark mode extraction
  if dembrandt "$site" --json-only --output-dir "$site_dir" --dark-mode 2>/dev/null; then
    echo "$(date '+%H:%M:%S')   [OK] dark mode"
    dark_ok=true
  else
    echo "$(date '+%H:%M:%S')   [FAIL] dark mode: $site"
  fi

  # Only count as success if at least one mode extracted
  if [ "$light_ok" = true ] || [ "$dark_ok" = true ]; then
    success=$((success + 1))
  else
    failed=$((failed + 1))
  fi

  # Be respectful to servers
  sleep "$SLEEP_BETWEEN"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
echo "============================================="
echo " SaaS Design Token Extraction"
echo " Started: $(date)"
echo " Sites file: $SITES_FILE"
echo " Output dir: $OUTPUT_DIR"
echo "============================================="
echo ""

if [ -n "$SINGLE_SITE" ]; then
  extract_site "$SINGLE_SITE"
else
  # Read sites.txt, skip comments (#) and empty lines
  while IFS= read -r line || [ -n "$line" ]; do
    # Trim whitespace (pure bash, no xargs edge cases)
    line="${line#"${line%%[![:space:]]*}"}"
    line="${line%"${line##*[![:space:]]}"}"

    # Skip empty lines and comments
    [ -z "$line" ] && continue
    [[ "$line" == \#* ]] && continue

    extract_site "$line"
  done < "$SITES_FILE"
fi

echo ""
echo "============================================="
echo " Extraction Complete: $(date)"
echo " Total processed: $total"
echo " Successful: $success"
echo " Failed extractions: $failed"
echo " Skipped (resume): $skipped"
echo "============================================="
echo ""
echo "Next step: run python3 scripts/parse-tokens.py to distill design tokens."
