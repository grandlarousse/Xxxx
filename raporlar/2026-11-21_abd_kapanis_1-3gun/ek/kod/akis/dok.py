#!/usr/bin/env python3
"""İş akışı günlüğündeki ajan sonuçlarını ek/ajanlar altına md olarak yazar.
Kullanım: python3 -I dok.py <journal.jsonl> <çıktı dizini> <önek>"""
import json, sys, os, re
j, out, pre = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
lab = {}
def t(x): return str(x).replace("|", "/").replace("\n", " ")
for line in open(j):
    try: e = json.loads(line)
    except Exception: continue
    if e.get("type") == "started": lab[e["key"]] = e.get("label", "?")
    if e.get("type") != "result" or not isinstance(e.get("result"), dict): continue
    r = e["result"]; name = lab.get(e["key"], "?")
    slug = re.sub(r"[^A-Za-z0-9]+", "_", name.split("·")[0].strip()) or "x"
    fn = os.path.join(out, f"{pre}_{slug}.md")
    with open(fn, "w") as f:
        f.write(f"# {name}\n\n{r.get('arac','')}\n")
        for k, baslik in (("genel_karar", "Genel karar"), ("ozet", "Özet")):
            if r.get(k): f.write(f"\n## {baslik}\n\n{r[k]}\n")
        if r.get("defter"):
            f.write("\n## İddia defteri\n\n| # | iddia | kaynak | alıntı / sayı | güven | kritik |\n|---|---|---|---|---|---|\n")
            for i, s in enumerate(r["defter"], 1):
                f.write(f"| {i} | {t(s['iddia'])} | {t(s['kaynak'])} | {t(s['alinti'])} | {s['guven']} | {'evet' if s.get('kritik') else ''} |\n")
        if r.get("kurallar"):
            f.write("\n## Sınanacak kurallar\n\n| # | ad | aile | girdi | kural | hedef | kaynak | bildirilen etki | güncel geçerlilik |\n|---|---|---|---|---|---|---|---|---|\n")
            for i, s in enumerate(r["kurallar"], 1):
                f.write(f"| {i} | {t(s['ad'])} | {t(s['aile'])} | {t(s['girdi'])} | {t(s['kural'])} | {t(s['hedef'])} | {t(s['kaynak'])} | {t(s['bildirilen_etki'])} | {t(s['guncel_gecerlilik'])} |\n")
        if r.get("itirazlar"):
            f.write("\n## İtirazlar\n\n| # | önem | bölüm | itiraz | düzeltme |\n|---|---|---|---|---|\n")
            for i, s in enumerate(r["itirazlar"], 1):
                f.write(f"| {i} | {s['onem']} | {t(s['bolum'])} | {t(s['itiraz'])} | {t(s['duzeltme'])} |\n")
        if r.get("adaylar"):
            f.write("\n## Adaylar\n\n| kod | tema | sınıf | lehte | aleyhte |\n|---|---|---|---|---|\n")
            for a in r["adaylar"]:
                f.write(f"| {a['kod']} | {t(a.get('tema',''))} | {a['sinif']} | {t(a['tez'])} | {t(a['ayi_tezi'])} |\n")
        for k, baslik in (("dosyalar", "Dosyalar"), ("yukleme_ornegi", "Yükleme örneği"), ("basarisiz_kodlar", "Başarısız kodlar"), ("kalite_ozeti", "Kalite özeti"), ("notlar", "Notlar"), ("ornek_satirlar", "Örnek satırlar"), ("eksik_hipotezler", "Eksik hipotezler"), ("eksik_testler", "Eksik testler"), ("listede_olmayan", "Listede olmayan bulgular"), ("celisen_kanit", "Çelişen kanıt"), ("acik_kalanlar", "Açık kalanlar")):
            v = r.get(k)
            if v:
                if isinstance(v, list): v = "\n".join("- " + str(x) for x in v)
                f.write(f"\n## {baslik}\n\n{v}\n")
    print(f"{name} | {r.get('arac','')} | defter {len(r.get('defter',[]))} | kural {len(r.get('kurallar',[]))} -> {fn}")
