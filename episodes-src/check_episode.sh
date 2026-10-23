#!/usr/bin/env bash
# Pre-publish checklist for an episode: audio, feed, links. Run after publishing.
#   episodes-src/check_episode.sh episodes-src/001/episode.mp3
set -uo pipefail
MP3="$1"; SITE="https://millillion.org"; FAIL=0
ok() { echo "  ✓ $1"; }; bad() { echo "  ✗ $1"; FAIL=1; }

echo "Audio"
I=$(ffmpeg -hide_banner -nostats -i "$MP3" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | awk '/I:/{print $2}')
TP=$(ffmpeg -hide_banner -nostats -i "$MP3" -af ebur128=peak=true -f null - 2>&1 | grep -A14 Summary | awk '/Peak:/{print $2}')
python3 -c "import sys; sys.exit(0 if -17.5<=float('$I')<=-14.5 else 1)" && ok "loudness $I LUFS" || bad "loudness $I LUFS (want ~-16)"
python3 -c "import sys; sys.exit(0 if float('$TP')<=-1.0 else 1)" && ok "true peak $TP dBFS" || bad "true peak $TP dBFS (want <= -1)"
for t in title artist album; do ffprobe -v error -show_entries format_tags=$t -of csv=p=0 "$MP3" | grep -q . && ok "ID3 $t" || bad "ID3 $t missing"; done
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "$MP3" | grep -q video && ok "embedded cover art" || bad "no embedded cover art"

echo "Feed"
FEED=$(curl -s "$SITE/podcast.xml")
echo "$FEED" | python3 -c "import sys,xml.etree.ElementTree as E; E.fromstring(sys.stdin.read())" && ok "feed XML parses" || bad "feed XML invalid"
SIZE=$(stat -c %s "$MP3")
echo "$FEED" | grep -q "length=\"$SIZE\"" && ok "enclosure length matches file ($SIZE)" || bad "enclosure length != $SIZE"
for u in $(echo "$FEED" | grep -oE '(url|href)="https://[^"]+\.(mp3|jpg|png)"' | cut -d'"' -f2); do
  c=$(curl -s -o /dev/null -w '%{http_code}' -I "$u"); [ "$c" = 200 ] && ok "200 $u" || bad "$c $u"
done
R=$(curl -s -o /dev/null -w '%{http_code}' -r 0-99 "$(echo "$FEED" | grep -oE 'enclosure url="[^"]+"' | head -1 | cut -d'"' -f2)")
[ "$R" = 206 ] && ok "byte-range requests (Apple requirement)" || bad "byte-range returned $R"

echo "Site links"
for p in $(echo "$FEED" | grep -oE '<link>[^<]+</link>' | sed 's/<[^>]*>//g') $SITE/ $SITE/blog/ $SITE/podcast/ $SITE/rss.xml; do
  c=$(curl -s -o /dev/null -w '%{http_code}' "$p"); [ "$c" = 200 ] && ok "200 $p" || bad "$c $p"
done
[ $FAIL = 0 ] && echo "ALL CHECKS PASSED" || { echo "SOME CHECKS FAILED"; exit 1; }
