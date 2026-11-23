#!/usr/bin/env python3
"""Her kitap dosyasinin kunyesindeki Turkce baski cumlesini bkmkitap taramasindaki (turkce_bkm.json) yazar kayitlariyla yan yana koyar.
Cikti: ek/dogrulama/turkce_karsilastirma.md (elle karar icin tablo)."""
import json, os, re, glob
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bkm = json.load(open(K + "/dogrulama/turkce_bkm.json"))
satir = ["dosya | künyedeki Türkçe cümlesi | bkmkitap'ta yazarın kitapları (ad · yayınevi · sayfa)", "---|---|---"]
for yol in sorted(glob.glob(K + "/kitaplar/K*.md")):
    d = os.path.basename(yol)[:-3]
    m = re.search(r"\*\*Künye\.\*\*(.*)", open(yol).read())
    kun = m.group(1) if m else ""
    cum = [c.strip() for c in re.split(r"(?<=[.;])\s+", kun) if re.search(r"[Tt]ürkçe", c)]
    hits = bkm.get(d, {}).get("bulunan", [])
    h = "; ".join(f'{x["ad"]} · {x["yayinevi"]} · {x["sayfa"]}' for x in hits[:8]) or "—"
    satir.append(f'{d} | {" ".join(cum)[:400] or "(Türkçe cümlesi yok)"} | {h}')
open(K + "/dogrulama/turkce_karsilastirma.md", "w").write("# Türkçe baskı karşılaştırması (künye ve bkmkitap)\n\n" + "\n".join(satir) + "\n")
print(len(satir) - 2, "satır")
