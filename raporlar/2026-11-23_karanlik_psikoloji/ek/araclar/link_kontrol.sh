#!/bin/bash
# Defterlerdeki ve dogrulama notlarindaki butun baglantilari toplu kontrol eder (8 paralel).
# Cikti: ek/dogrulama/link_kontrol.csv  (http_kodu,url)
cd "$(dirname "$0")/.." || exit 1
grep -ohE "https?://[^ |)>\"'\`]+" defter/*.md dogrulama/*.md 2>/dev/null | sed -E 's/[.,;:]+$//' | sort -u > /tmp/claude-0/-home-user-Xxxx/8659fb41-5d90-5f85-b31f-9c341f76033f/scratchpad/kp_linkler.txt
wc -l < /tmp/claude-0/-home-user-Xxxx/8659fb41-5d90-5f85-b31f-9c341f76033f/scratchpad/kp_linkler.txt
kontrol() { k=$(curl -s -o /dev/null -L --max-time 20 -A "Mozilla/5.0 (X11; Linux x86_64) Chrome/120" -w "%{http_code}" "$1" 2>/dev/null); echo "$k,$1"; }
export -f kontrol
xargs -a /tmp/claude-0/-home-user-Xxxx/8659fb41-5d90-5f85-b31f-9c341f76033f/scratchpad/kp_linkler.txt -P 8 -I{} bash -c 'kontrol "$@"' _ {} > dogrulama/link_kontrol.csv
cut -d, -f1 dogrulama/link_kontrol.csv | sort | uniq -c | sort -rn
