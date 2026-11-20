#!/usr/bin/env python3
"""Doğrulayıcı ve eleştirmen çıktılarını iş akışı günlüklerinden toplar.

Kullanım: python3 dogrulama_topla.py <workflows_klasoru> <ek_klasoru>

Üretir:
- <ek>/dogrulama/sonuc.json : satır başına doğrulama kararı
- <ek>/DOGRULAMA.md         : sayım ve doğrulanmayan satırların listesi
- <ek>/elestiri_<tur>.md    : eleştirmen çıktıları
"""
import glob
import json
import os
import re
import sys

wf_dir, ek = sys.argv[1], sys.argv[2]
MIN_PARTI = int(os.environ.get("MIN_PARTI", "0"))  # aynı oturumdaki başka işlerin partilerini dışarıda bırakır
ELESTIRI = [x for x in os.environ.get("ELESTIRI", "").split(",") if x]
defter = {s["id"]: s for s in json.load(open(os.path.join(ek, "defter.json"), encoding="utf-8"))}
kararlar, notlar, araclar = {}, {}, {}
for j in sorted(glob.glob(os.path.join(wf_dir, "*", "journal.jsonl"))):
    etiket = {}
    for line in open(j, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        if e.get("type") == "started":
            etiket[e["agentId"]] = e.get("label", "")
        elif e.get("type") == "result":
            lab = etiket.get(e.get("agentId"), "")
            r = e.get("result")
            m = re.match(r"Doğrulama parti (\d+)", lab)
            if m and isinstance(r, dict) and "satirlar" in r:
                no = int(m.group(1))
                if no < MIN_PARTI:
                    continue
                notlar[no] = r.get("genel_not", "")
                araclar[no] = r.get("arac", "")
                for s in r["satirlar"]:
                    if s.get("id") in defter:
                        kararlar[s["id"]] = {**s, "parti": no}
            m = re.match(r"Eleştirmen: (\w+)", lab)
            if m and isinstance(r, str) and r.strip() and (not ELESTIRI or m.group(1) in ELESTIRI):
                open(os.path.join(ek, f"elestiri_{m.group(1)}.md"), "w", encoding="utf-8").write(
                    f"# Eleştirmen çıktısı: {m.group(1)}\n\n{r.strip()}\n")

os.makedirs(os.path.join(ek, "dogrulama"), exist_ok=True)
json.dump(sorted(kararlar.values(), key=lambda s: s["id"]), open(os.path.join(ek, "dogrulama", "sonuc.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

say = {}
for s in kararlar.values():
    say[s["sonuc"]] = say.get(s["sonuc"], 0) + 1


def h(x):
    return str(x).replace("|", "/").replace("\n", " ").strip()


md = ["# Doğrulama sonuçları", "",
      "Raporda kullanılan her iddia defteri satırı, gösterdiği kaynağa bakılarak denetlendi. Kararlar: doğrulandı, kısmen (özü doğru, ayrıntı düzeltildi), yanlış, erişilemedi (kaynak ve özeti görülemedi).", "",
      f"Denetlenen satır: {len(kararlar)}", ""]
for k in ("doğrulandı", "kısmen", "yanlış", "erişilemedi"):
    md.append(f"- {k}: {say.get(k, 0)}")
md += ["", "## Doğrulanmayan ya da düzeltilen satırlar", "", "| Satır | Karar | Görülen | Düzeltme | Kaynak |", "|---|---|---|---|---|"]
for s in sorted(kararlar.values(), key=lambda s: s["id"]):
    if s["sonuc"] != "doğrulandı":
        d = defter[s["id"]]
        md.append(f"| {s['id']} | {s['sonuc']} | {s['gordugum']} | {h(s.get('duzeltme', ''))} | [{h(d['kaynak_adi'])[:80]}]({d['url'].strip()}) |")
md += ["", "## Parti notları", ""]
for no in sorted(notlar):
    md.append(f"- Parti {no} ({h(araclar.get(no, ''))[:60]}): {h(notlar[no])}")
open(os.path.join(ek, "DOGRULAMA.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print("denetlenen:", len(kararlar), "| sayım:", say, "| partiler:", sorted(notlar))
