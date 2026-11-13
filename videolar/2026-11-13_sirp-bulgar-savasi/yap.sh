#!/usr/bin/env bash
# Videoyu baştan üretir: kareler -> ses -> mp4.
# Gerekenler: node + playwright (Chromium), python3 (numpy, scipy), ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
TMP="${TMPDIR:-/tmp}/rumeli-1885"; mkdir -p "$TMP" cikti
OUT=cikti/560-yil-rumeli_sirp-bulgar-savasi-1885.mp4
[ -d node_modules ] || npm install --silent
rm -rf "$TMP/kare"; node render.js tam "$TMP/kare" 4
python3 ses.py "$TMP/ses.wav"
# ses yüksekliği: -14 LUFS (iki geçişli, doğrusal)
LN=$(ffmpeg -hide_banner -i "$TMP/ses.wav" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | python3 -c "
import sys, json
t = sys.stdin.read(); j = json.loads(t[t.rindex('{'):t.rindex('}') + 1])
print('loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true' % (j['input_i'], j['input_tp'], j['input_lra'], j['input_thresh'], j['target_offset']))")
ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$TMP/kare/%05d.jpg" -i "$TMP/ses.wav" \
  -vf "scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p" \
  -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high -level 4.2 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -r 30 \
  -af "$LN" -ar 48000 -c:a aac -b:a 256k -movflags +faststart -shortest "$OUT"
echo "hazır: $OUT"
