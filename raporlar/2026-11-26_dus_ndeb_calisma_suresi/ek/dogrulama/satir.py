#!/usr/bin/env python3
"""İddia defterinden seçili satırları yazdırır.
Kullanım: python3 satir.py <ek dosyası> <satır no> [<satır no> ...]
Satır numarası: defter tablosunda başlık ve ayraç satırlarından sonraki sıra (1'den başlar)."""
import re, sys, os

def satirlar(yol):
    rows = [l.rstrip("\n") for l in open(yol, encoding="utf-8") if l.startswith("|")]
    body = [r for r in rows if not re.match(r"^\|\s*[-:]+", r)]
    if body and ("iddia" in body[0].lower() or "#" in body[0][:6]):
        body = body[1:]
    return body

if __name__ == "__main__":
    ek = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dosya = sys.argv[1]
    yol = dosya if os.path.isabs(dosya) else os.path.join(ek, dosya)
    body = satirlar(yol)
    for n in sys.argv[2:]:
        i = int(n)
        print(f"--- {os.path.basename(yol)} satır {i} ---")
        print(body[i - 1] if 1 <= i <= len(body) else "(yok)")
