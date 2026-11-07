"""Literatür kaynaklarını indirir (ham sayfa/PDF) ve metne çevirir.

Kullanım:  python3 -I lit_indir.py <url_listesi.txt> <cikti_klasoru>
- User-Agent: "etf-research-script/1.0" (tarayıcı taklidi yok, bot koruması aşılmaya çalışılmaz).
- 4xx/5xx/403 alınan sayfalar atlanır ve index.tsv'ye durum kodu yazılır.
- PDF'ler pdftotext ile .txt'ye, HTML'ler basit etiket temizliğiyle .txt'ye çevrilir.
"""
import hashlib
import html
import os
import re
import subprocess
import sys
import time

import requests

UA = {"User-Agent": "etf-research-script/1.0"}


def slug(url: str) -> str:
    s = re.sub(r"^https?://", "", url)
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")
    if len(s) > 120:
        s = s[:100] + "_" + hashlib.sha1(url.encode()).hexdigest()[:10]
    return s


def html_to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", raw)
    raw = re.sub(r"(?is)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n", raw)
    return raw.strip()


def main(url_file: str, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    idx_path = os.path.join(out_dir, "index.tsv")
    done = set()
    if os.path.exists(idx_path):
        with open(idx_path, encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2 and parts[1] == "200":
                    done.add(parts[0])
    urls = []
    with open(url_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    with open(idx_path, "a", encoding="utf-8") as idx:
        for url in urls:
            if url in done:
                continue
            try:
                r = requests.get(url, headers=UA, timeout=40, allow_redirects=True)
            except Exception as e:  # ağ hatası
                idx.write(f"{url}\tERR\t{type(e).__name__}\t0\t\t\n")
                idx.flush()
                continue
            ctype = r.headers.get("Content-Type", "")
            name = slug(url)
            if r.status_code != 200:
                idx.write(f"{url}\t{r.status_code}\t{ctype}\t{len(r.content)}\t\t\n")
                idx.flush()
                time.sleep(1)
                continue
            is_pdf = "pdf" in ctype.lower() or r.content[:5] == b"%PDF-"
            ext = ".pdf" if is_pdf else ".html"
            raw_path = os.path.join(out_dir, name + ext)
            with open(raw_path, "wb") as g:
                g.write(r.content)
            txt_path = os.path.join(out_dir, name + ".txt")
            if is_pdf:
                subprocess.run(["pdftotext", "-layout", raw_path, txt_path],
                               check=False, capture_output=True, timeout=120)
            else:
                enc = r.encoding or "utf-8"
                try:
                    text = r.content.decode(enc, errors="replace")
                except LookupError:
                    text = r.content.decode("utf-8", errors="replace")
                with open(txt_path, "w", encoding="utf-8") as g:
                    g.write(html_to_text(text))
            sha = hashlib.sha256(r.content).hexdigest()[:16]
            idx.write(f"{url}\t200\t{ctype}\t{len(r.content)}\t{os.path.basename(raw_path)}\t{sha}\n")
            idx.flush()
            time.sleep(1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
