#!/usr/bin/env python3
"""İş akışı günlüklerinden (journal.jsonl) ajan çıktılarını toplar.

Kullanım: python3 defter_topla.py <workflows_klasoru> <cikti_klasoru> [ozet_klasoru]

- <cikti_klasoru>/Kxx_*.md : konu başına ham ajan çıktısı (özet + iddia defteri)
- <cikti_klasoru>/defter.json : bütün satırlar, kimlikleriyle (K03-07 gibi)
- [ozet_klasoru]/Kxx.txt : URL'siz sıkıştırılmış görünüm (ana ajanın okuması için)
"""
import glob
import json
import os
import re
import sys

wf_dir, out_dir = sys.argv[1], sys.argv[2]
ozet_dir = sys.argv[3] if len(sys.argv) > 3 else None
os.makedirs(out_dir, exist_ok=True)
if ozet_dir:
    os.makedirs(ozet_dir, exist_ok=True)

TR = str.maketrans("çğıöşüÇĞİÖŞÜ–", "cgiosuCGIOSU-")


def slug(s):
    s = s.translate(TR).lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


konular = {}  # kod -> dict
for j in sorted(glob.glob(os.path.join(wf_dir, "*", "journal.jsonl"))):
    etiket = {}
    for line in open(j, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        if e.get("type") == "started":
            etiket[e["agentId"]] = e.get("label", "")
        elif e.get("type") == "result" and isinstance(e.get("result"), dict):
            lab = etiket.get(e.get("agentId"), "")
            m = re.match(r"([A-Z]\d{2}[a-z]?)\s+(.*)", lab)
            if not m or "defter" not in e["result"]:
                continue
            kod, ad = m.group(1), re.sub(r"\s*\(2\. deneme\)$", "", m.group(2))
            # Aynı konu iki kez bittiyse ilk biten geçerli (yinelenen çalıştırma yok sayılır)
            if kod in konular:
                continue
            konular[kod] = {"kod": kod, "ad": ad, "ajan": e.get("agentId"), "akis": os.path.basename(os.path.dirname(j)), **e["result"]}

tum = []
for kod in sorted(konular):
    k = konular[kod]
    satirlar = []
    for i, d in enumerate(k.get("defter", []), 1):
        sid = f"{kod}-{i:02d}"
        satirlar.append({"id": sid, "konu": kod, **d})
    tum.extend(satirlar)

    def hucre(x):
        return str(x).replace("|", "/").replace("\n", " ").strip()

    md = [f"# {kod} {k['ad']}", "", f"`{k['arac']}`", "", "## Özet", "", k["ozet"].strip(), "", "## İddia defteri", "",
          "| No | İddia | Kaynak | Alıntı ya da sayı | Tür | Görülen | Güven |", "|---|---|---|---|---|---|---|"]
    for s in satirlar:
        md.append(f"| {s['id']} | {hucre(s['iddia'])} | [{hucre(s['kaynak_adi'])}]({s['url'].strip()}) | {hucre(s['alinti'])} | {s['kanit_turu']} | {s['gorulen']} | {s['guven']} |")
    for baslik, alan in (("Listede olmayan bulgular", "listede_olmayan"), ("Çelişen kanıt", "celisen_kanit"), ("Açık kalanlar", "acik_kalanlar")):
        md += ["", f"## {baslik}", ""] + [f"- {x}" for x in k.get(alan, [])]
    open(os.path.join(out_dir, f"{kod}_{slug(k['ad'])}.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")

    if ozet_dir:
        t = [f"## {kod} {k['ad']}", k["arac"], k["ozet"].strip(), "DEFTER"]
        for s in satirlar:
            t.append(f"{s['id']} | {hucre(s['iddia'])} | {hucre(s['kaynak_adi'])} | \"{hucre(s['alinti'])}\" | {s['kanit_turu']}; {s['gorulen']}; {s['guven']}")
        t.append("LİSTEDE OLMAYAN: " + " ; ".join(k.get("listede_olmayan", [])))
        t.append("ÇELİŞEN: " + " ; ".join(k.get("celisen_kanit", [])))
        t.append("AÇIK: " + " ; ".join(k.get("acik_kalanlar", [])))
        open(os.path.join(ozet_dir, f"{kod}.txt"), "w", encoding="utf-8").write("\n".join(t) + "\n")

json.dump(tum, open(os.path.join(out_dir, "defter.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("konu:", len(konular), "satır:", len(tum))
for kod in sorted(konular):
    print(" ", kod, konular[kod]["ad"], "|", len(konular[kod].get("defter", [])), "satır |", konular[kod]["arac"][:90])
