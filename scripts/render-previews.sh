#!/usr/bin/env bash
# Render the example pages to PNG previews with headless Google Chrome.
# Usage: scripts/render-previews.sh [output-dir]   (default: previews/)
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
out="${1:-$root/previews}"
chrome="${CHROME:-google-chrome}"
mkdir -p "$out"

# name  page  width  height
pages=(
  "brand examples/brand-sheet.html 1200 1100"
  "design-sheet examples/design-sheet.html 1280 3660"
  "buyer-lookup-phone examples/buyer-lookup.html 390 2240"
  "buyer-lookup-desktop examples/buyer-lookup.html 1280 1320"
  "alert-card examples/alert-card.html 390 1420"
)

for entry in "${pages[@]}"; do
  read -r name page width height <<<"$entry"
  [ -f "$root/$page" ] || { echo "skip $page (missing)"; continue; }
  "$chrome" --headless=new --disable-gpu --hide-scrollbars \
    --allow-file-access-from-files --force-device-scale-factor=1 \
    --window-size="$width,$height" \
    --screenshot="$out/$name.png" "file://$root/$page" >/dev/null 2>&1
  echo "rendered $out/$name.png (${width}x${height})"
done
