#!/usr/bin/env python3
"""Doğrulama sonuçlarını toplar, ek/TUM_LISTE.md ve ek/dogrulama/SONUC.md üretir, RAPOR.md'deki Kaynaklar bölümünü doldurur.
Kullanim: python3 rapor_tamamla.py [DOGRULAMA_JOURNAL ...]"""
import json, os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
rows = json.load(open(os.path.join(HERE, "defter.json"), encoding="utf-8"))
by = {r["id"]: r for r in rows}
links = json.load(open(os.path.join(HERE, "link_durum.json"))) if os.path.exists(os.path.join(HERE, "link_durum.json")) else {}
# 1) dogrulama sonuclari
sp = os.path.join(HERE, "dogrulama", "sonuc.json")
ver = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
ozetler = []
for jp in sys.argv[1:]:
    lab = {}
    for line in open(jp, encoding="utf-8"):
        o = json.loads(line)
        if o.get("type") == "started": lab[o["agentId"]] = o.get("label", "")
        elif o.get("type") == "result" and isinstance(o.get("result"), dict) and "sonuc" in o["result"]:
            r = o["result"]
            ozetler.append((lab.get(o["agentId"], "?"), r.get("arac", ""), r.get("ozet", "")))
            for s in r["sonuc"]:
                i = str(s.get("id", "")).strip()
                if i in by:
                    ver[i] = {"hukum": s.get("hukum"), "duzeltme": html.unescape(s.get("duzeltme") or ""), "not": html.unescape(s.get("not") or ""), "dogrulayici": lab.get(o["agentId"], "?")}
if ver:
    json.dump(ver, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
plan = json.load(open(os.path.join(HERE, "dogrulama", "plan.json"), encoding="utf-8"))
tam, ornek = set(plan["tam"]), set(plan["ornek"])
def say(ids):
    c = {"doğru": 0, "kısmen": 0, "yanlış": 0, "açılamadı": 0, "yok": 0}
    for i in ids: c[ver.get(i, {}).get("hukum", "yok")] = c.get(ver.get(i, {}).get("hukum", "yok"), 0) + 1
    return c
if ver:
    L = ["# Doğrulama sonuçları", "", f"Tam doğrulama: {len(tam)} satır → {say(tam)}", f"Örneklem: {len(ornek)} satır (havuz {plan['ornek_havuzu']}) → {say(ornek)}", "",
         "## Doğrulayıcı özetleri", ""]
    for lab_, arac, oz in sorted(ozetler): L += [f"- **{lab_}** `{arac}`: {html.unescape(oz)}"]
    L += ["", "## Düzeltme gereken satırlar", "", "| kimlik | tür | ad | hüküm | düzeltme | not |", "|---|---|---|---|---|---|"]
    for i in sorted(ver):
        v = ver[i]
        if v["hukum"] != "doğru":
            t = lambda s: str(s).replace("|", "/").replace("\n", " ")
            L.append(f"| {i} | {'tam' if i in tam else 'örnek'} | {t(by[i]['ad'])} | {v['hukum']} | {t(v['duzeltme'])} | {t(v['not'])} |")
    open(os.path.join(HERE, "dogrulama", "SONUC.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
# 2) TUM_LISTE
TEMA = [("Dil ve yabancılar", ["d1_01", "d1_02", "d1_03", "d1_04", "d2_01", "d3_01"]), ("Gönüllülük ve kamu imkânları", ["d1_05", "d1_06", "d3_02"]),
        ("Dans", ["d1_07", "d3_08"]), ("Spor ve doğa", ["d1_08", "d1_09", "d1_10", "d1_11", "d2_06", "d2_07", "d3_03", "d3_04", "d3_05"]),
        ("Yoga ve benzeri", ["d1_12", "d2_05"]), ("Sanat, sahne, atölye", ["d1_13", "d2_10"]), ("Oyun, kitap, sinema, gece", ["d1_14", "d2_08", "d2_09", "d2_04"]),
        ("Uygulamalar ve tanışma etkinlikleri", ["d1_15", "d2_02"]), ("İş ve çevre", ["d1_16", "d3_06"]), ("Dış halka ve gastronomi", ["d3_07"]), ("Araştırma kanıtları", ["d2_03"])]
L = ["# Tüm liste: iddia defteri (698 satır)", "",
     "34 üreticinin defter satırları, temaya göre. **Doğrulama** sütunu: doğrulayıcının hükmü (boşsa o satır doğrulama kümesinde değildi). **Link**: toplu kontrolde dönen HTTP kodu (403 çoğunlukla bot engeli, sayfa tarayıcıda açılır).",
     "Güven etiketi üreticinindir: *düşük* satırlar güncelliği ya da kaynağı zayıf olanlardır; gitmeden teyit et.", ""]
g = lambda s: str(s).replace("|", "/").replace("\n", " ")
for tema, birimler in TEMA:
    rs = [r for r in rows if any(r["birim"].startswith(b) for b in birimler)]
    L += [f"## {tema} ({len(rs)} satır)", "", "| kimlik | ad | ne, kime | semt | ne zaman / ücret | kanal | kaynak | son tarih | güven | doğrulama | link |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rs:
        v = ver.get(r["id"], {})
        dz = v.get("hukum", "")
        if v.get("duzeltme"): dz += ": " + v["duzeltme"]
        u = r["kaynak"].split()[0] if r["kaynak"] else ""
        L.append("| " + " | ".join([r["id"], g(r["ad"]), g(r["iddia"]), g(r["semt"]), g(r["ne_zaman_ucret"]), g(r["kanal"]), f"[kaynak]({u})" if u.startswith("http") else g(r["kaynak"]), r["son_tarih"], r["guven"], g(dz), links.get(u, "")]) + " |")
    L.append("")
open(os.path.join(HERE, "TUM_LISTE.md"), "w", encoding="utf-8").write("\n".join(L))
# 3) RAPOR kaynaklar
rp = os.path.join(ROOT, "RAPOR.md")
txt = open(rp, encoding="utf-8").read()
govde = txt.split("## Kaynaklar")[0]
ids = []
for m in re.finditer(r"`(\d\.\d\d\.\d\d)`", govde):
    if m.group(1) not in ids: ids.append(m.group(1))
eksik = [i for i in ids if i not in by]
K = ["Raporda kodu geçen defter satırları, kaynakları ve doğrulayıcının hükmü. Bütün satırlar (698) ve kaynakları: `ek/TUM_LISTE.md`.", ""]
for i in sorted(ids):
    if i in by:
        u = by[i]["kaynak"].split()[0]
        vv = ver.get(i)
        durum = "doğrulanmadı" if not vv else vv["hukum"]
        if vv and vv["hukum"] != "doğru" and (vv.get("duzeltme") or vv.get("not")):
            durum += " (" + g(vv.get("duzeltme") or vv.get("not"))[:160] + ")"
        K.append(f"- `{i}` {g(by[i]['ad'])}: <{u}> · *{durum}*")
blok = "\n".join(K)
if "<!--KAYNAKLAR-->" in txt:
    txt = txt.replace("<!--KAYNAKLAR-->", "<!--KAYNAKLAR-BAS-->\n" + blok + "\n<!--KAYNAKLAR-SON-->")
else:
    txt = re.sub(r"<!--KAYNAKLAR-BAS-->.*?<!--KAYNAKLAR-SON-->", lambda _: "<!--KAYNAKLAR-BAS-->\n" + blok + "\n<!--KAYNAKLAR-SON-->", txt, flags=re.S)
open(rp, "w", encoding="utf-8").write(txt)
# 4) ozet cikti
print("rapordaki kod sayisi:", len(ids), "| defterde olmayan kod:", eksik)
print("dogrulanan satir:", len(ver), "| tam:", say(tam), "| ornek:", say(ornek))
rap = [i for i in ids if i in ver and ver[i]["hukum"] != "doğru"]
print("RAPORDA GECEN ve dogru olmayan satirlar:")
for i in rap: print(" ", i, "|", by[i]["ad"][:40], "|", ver[i]["hukum"], "|", ver[i]["duzeltme"][:260], "|", ver[i]["not"][:120])
nover = [i for i in ids if i not in ver]
print("raporda gecen ama dogrulama kumesinde olmayan kodlar:", nover)
# kelime sayisi (tablolar ve kaynaklar haric)
body = txt.split("## Kaynaklar")[0]
w = sum(len(l.split()) for l in body.splitlines() if not l.strip().startswith("|"))
print("govde kelime (tablolar haric):", w)
