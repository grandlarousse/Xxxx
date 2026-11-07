"""Midas koşulları araştırması için sayfa indirici.

Kullanım:
    python -I fetch_pages.py <cikti_klasoru> <url1> [<url2> ...]

- User-Agent: "etf-research-script/1.0" (tarayıcı taklidi yok, bot korumasını aşma yok)
- Her URL için ham HTML (.html) ve kaba metin (.txt) kaydeder, ayrıca index.tsv'ye
  tarih/durum/URL satırı ekler.
"""
import sys
import os
import re
import hashlib
import datetime
import html as htmlmod

import time

import requests

UA = "etf-research-script/1.0"


def slug(url: str) -> str:
    s = re.sub(r"^https?://", "", url)
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")
    if len(s) > 120:
        s = s[:100] + "_" + hashlib.sha1(url.encode()).hexdigest()[:10]
    return s


def html_to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</(p|div|li|h[1-6]|tr|td|th|section|article)>", "\n", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = htmlmod.unescape(raw)
    raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n", raw)
    return raw.strip()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    idx = os.path.join(out, "index.tsv")
    sess = requests.Session()
    sess.headers.update({"User-Agent": UA})
    for url in sys.argv[2:]:
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        name = slug(url)
        try:
            r = sess.get(url, timeout=30, allow_redirects=True)
            status = r.status_code
            body = r.text
            final = r.url
        except Exception as e:  # noqa: BLE001
            status = f"ERR:{type(e).__name__}"
            body = ""
            final = url
        with open(os.path.join(out, name + ".html"), "w", encoding="utf-8") as f:
            f.write(body)
        txt = html_to_text(body) if body else ""
        with open(os.path.join(out, name + ".txt"), "w", encoding="utf-8") as f:
            f.write(txt)
        with open(idx, "a", encoding="utf-8") as f:
            f.write(f"{ts}\t{status}\t{len(body)}\t{url}\t{final}\t{name}\n")
        print(f"{status}\t{len(body)}\t{len(txt)}\t{name}")
        time.sleep(0.8)


if __name__ == "__main__":
    main()
