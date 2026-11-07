"""İkili dosya (PDF vb.) indirici.

Kullanım:
    python -I fetch_binary.py <cikti_klasoru> <url1> [<url2> ...]

User-Agent: "etf-research-script/1.0". Ham baytları olduğu gibi kaydeder,
index.tsv'ye tarih/durum/URL ekler.
"""
import sys
import os
import re
import time
import hashlib
import datetime

import requests

UA = "etf-research-script/1.0"


def name_of(url: str) -> str:
    s = re.sub(r"^https?://", "", url)
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")
    if len(s) > 120:
        s = s[:100] + "_" + hashlib.sha1(url.encode()).hexdigest()[:10]
    return s


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    sess = requests.Session()
    sess.headers.update({"User-Agent": UA})
    for url in sys.argv[2:]:
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        nm = name_of(url)
        try:
            r = sess.get(url, timeout=60)
            st, data = r.status_code, r.content
        except Exception as e:  # noqa: BLE001
            st, data = f"ERR:{type(e).__name__}", b""
        with open(os.path.join(out, nm), "wb") as f:
            f.write(data)
        with open(os.path.join(out, "index.tsv"), "a", encoding="utf-8") as f:
            f.write(f"{ts}\t{st}\t{len(data)}\t{url}\t{nm}\n")
        print(f"{st}\t{len(data)}\t{nm}")
        time.sleep(0.8)


if __name__ == "__main__":
    main()
