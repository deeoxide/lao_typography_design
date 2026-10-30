#!/usr/bin/env bash
# Install the bundled Lao fonts for the current user, so LibreOffice, Chromium, WeasyPrint,
# Pillow (RAQM) and other tools can find them by family name (for example "Noto Sans Lao").
#
#   bash scripts/setup_fonts.sh            # install all bundled fonts
#   bash scripts/setup_fonts.sh default    # install only the default, Noto Sans Lao
#
# Needs no network. Works on Linux and macOS. On Windows, double-click the font files and choose Install.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$here/assets/fonts"
if [ "$(uname -s)" = "Darwin" ]; then dest="$HOME/Library/Fonts"; else dest="$HOME/.fonts"; fi
mkdir -p "$dest"

count=0
for f in "$src"/*.ttf "$src"/*.otf; do
  [ -e "$f" ] || continue
  if [ "${1:-all}" = "default" ] && [[ "$(basename "$f")" != NotoSansLao* ]]; then continue; fi
  cp -f "$f" "$dest/"
  count=$((count + 1))
done

if command -v fc-cache >/dev/null 2>&1; then fc-cache -f "$dest" >/dev/null 2>&1 || true; fi
echo "Installed $count font file(s) to $dest"
if command -v fc-list >/dev/null 2>&1; then
  fc-list | grep -i "lao" | head -5 || echo "Warning: fc-list does not list a Lao font yet; open a new shell or check the path."
fi
