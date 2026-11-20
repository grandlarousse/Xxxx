#!/usr/bin/env python3
"""Is akisi gunluklerinden (journal.jsonl) ajan donuslerini cikarir.
Kullanim: python3 defter_topla.py JOURNAL [JOURNAL ...]
Yazar: ek/<etiket>.md (ajan basina ozet + defter), ek/defter.json (tum satirlar, kimlikli)."""
import json, sys, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
def temiz(s):
    return html.unescape(str(s or "")).replace("\n", " ").replace("|", "/").strip()
rows, units = [], []
for jp in sys.argv[1:]:
    label = {}
    for line in open(jp, encoding="utf-8"):
        o = json.loads(line)
        if o.get("type") == "started":
            label[o["agentId"]] = o.get("label", o["agentId"])
        elif o.get("type") == "result" and isinstance(o.get("result"), dict):
            lab = label.get(o["agentId"], o["agentId"])
            r = o["result"]
            if "defter" not in r:
                continue
            key = re.sub(r"[^0-9A-Za-z_]+", "_", lab).strip("_")
            units.append((key, r))
units.sort(key=lambda x: x[0])
for key, r in units:
    kisa = re.sub(r"^d(\d)r?_(\d+).*$", r"\1.\2", key)
    md = [f"# {key}", "", f"`{temiz(r.get('arac'))}`", "", "## Özet", "", html.unescape(r.get("ozet", "")), "", "## İddia defteri", "",
          "| no | ad | tür | iddia | semt | ne zaman / ücret | kanal | kaynak | alıntı | son tarih | güven |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, d in enumerate(r.get("defter", []), 1):
        rid = f"{kisa}.{i:02d}"
        row = {"id": rid, "birim": key}
        for k in ("ad", "tur", "iddia", "semt", "ne_zaman_ucret", "kanal", "kaynak", "alinti", "son_tarih", "guven"):
            row[k] = temiz(d.get(k))
        rows.append(row)
        md.append("| " + " | ".join([rid] + [row[k] for k in ("ad", "tur", "iddia", "semt", "ne_zaman_ucret", "kanal", "kaynak", "alinti", "son_tarih", "guven")]) + " |")
    for baslik, alan in (("Listede olmayan bulgular", "liste_disi"), ("Çelişen kanıt", "celisen"), ("Açık kalanlar", "acik_kalanlar"), ("Kaynaklar", "kaynaklar")):
        if r.get(alan):
            md += ["", f"## {baslik}", ""] + [f"- {html.unescape(str(x))}" for x in r[alan]]
    open(os.path.join(HERE, key + ".md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
json.dump(rows, open(os.path.join(HERE, "defter.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(units)} birim, {len(rows)} satir")
for key, r in units:
    g = [d.get("guven") for d in r.get("defter", [])]
    print(f"{key}: {len(g)} satir (yuksek {g.count('yüksek')}, orta {g.count('orta')}, dusuk {g.count('düşük')}) | {temiz(r.get('arac'))[:110]}")
