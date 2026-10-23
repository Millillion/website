#!/usr/bin/env bash
# Master a podcast episode: clean + level the voice, lay the intro under the opening,
# bookend with the intro reprise, and export a podcast-ready MP3 (-16 LUFS, -1.5 dBTP).
#
#   episodes-src/make_episode.sh episodes-src/001/raw.m4a episodes-src/001/episode.mp3 [voice_end_seconds]
set -euo pipefail
RAW="$1"; OUT="$2"; END="${3:-}"
DIR="$(cd "$(dirname "$0")" && pwd)"
INTRO="$DIR/intro.wav"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

TRIM=(); [ -n "$END" ] && TRIM=(-t "$END")
# Studio voice chain. Input is expected to be DeepFilterNet-enhanced (enhance_voice.py), so no broadband denoise here.
CHAIN="${CHAIN:-highpass=f=80,equalizer=f=250:t=q:w=1.0:g=-2.5,equalizer=f=4200:t=q:w=1.2:g=2.5,treble=g=1.5:f=11000,acompressor=threshold=-22dB:ratio=3:attack=8:release=180:makeup=2,deesser=i=0.4,agate=threshold=0.008:ratio=1.6:attack=5:release=250}"

# pass 1: measure the voice
MEAS=$(ffmpeg -hide_banner -nostats "${TRIM[@]}" -i "$RAW" -af "$CHAIN,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$MEAS" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
# pass 2: level it precisely
ffmpeg -hide_banner -loglevel error -y "${TRIM[@]}" -i "$RAW" \
  -af "$CHAIN,loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=44100" \
  -ac 2 "$TMP/voice.wav"

VLEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/voice.wav")
VOICE_IN=11.0                                        # voice enters as the intro resolves
OUTRO_AT=$(python3 -c "print(max(0, $VOICE_IN + $VLEN - 1.5))")

# intro under the opening (ducked as the voice arrives), reprise at the end, then a final limiter
ffmpeg -hide_banner -loglevel error -y -i "$INTRO" -i "$TMP/voice.wav" -i "$INTRO" -filter_complex "
  [0:a]volume=-3dB,afade=t=out:st=10.5:d=3.5[intro];
  [1:a]adelay=$(python3 -c "print(int($VOICE_IN*1000))")|$(python3 -c "print(int($VOICE_IN*1000))")[voice];
  [2:a]atrim=start=6.3,asetpts=PTS-STARTPTS,volume=-6dB,afade=t=in:st=0:d=1.2,adelay=$(python3 -c "print(int($OUTRO_AT*1000))")|$(python3 -c "print(int($OUTRO_AT*1000))")[outro];
  [intro][voice][outro]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.84:level=false[m]" \
  -map "[m]" -ar 44100 -ac 2 -c:a libmp3lame -b:a 128k -id3v2_version 3 "$OUT"

ffmpeg -hide_banner -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -A12 "Summary:" | grep -E "I:|Peak:"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
