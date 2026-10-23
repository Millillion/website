#!/usr/bin/env bash
# Render every Short listed in episodes-src/NNN/shorts.tsv (see the make-videos skill).
#   episodes-src/make_shorts.sh NNN
set -euo pipefail
NNN=$1; HERE=$(cd "$(dirname "$0")" && pwd)
grep -v '^#' "$HERE/$NNN/shorts.tsv" | while IFS=$'\t' read -r slug a b first last hook _desc; do
  [ -n "$slug" ] && python3 "$HERE/make_short.py" "$NNN" "$slug" "$a" "$b" "$first" "$last" "$hook" </dev/null
done
