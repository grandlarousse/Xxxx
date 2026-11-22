#!/usr/bin/env python3
"""RAPOR.md içindeki [Rx-yy] etiketlerinden kaynak listesini üretir ve <!--KAYNAKLAR--> işaretinin altına yazar."""
import json, re, sys
B="/root/.claude/projects/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/subagents/workflows"
RAP="/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/RAPOR.md"
led={}
for w in ["wf_2b10254c-2a8","wf_4c497049-182","wf_97dc0597-ab2","wf_0772c853-e96","wf_ca0c94f3-b6d","wf_ba63a727-d2e"]:
    lab={}
    for line in open(f"{B}/{w}/journal.jsonl"):
        try:e=json.loads(line)
        except Exception: continue
        if e.get("type")=="started": lab[e["key"]]=e["label"]
        if e.get("type")=="result" and isinstance(e.get("result"),dict):
            aj=lab[e["key"]].split("·")[0].strip()
            for i,s in enumerate(e["result"].get("defter",[]),1): led[f"{aj}-{i:02d}"]=s
ver={}
for w in ["wf_3705fabe-033","wf_754851be-8da","wf_eee7d503-e4b","wf_0bbe3159-e86","wf_fa460496-cb4"]:
    for line in open(f"{B}/{w}/journal.jsonl"):
        try:e=json.loads(line)
        except Exception: continue
        if e.get("type")=="result" and isinstance(e.get("result"),dict):
            for s in e["result"]["satirlar"]: ver[s["id"]]=s
s=open(RAP).read()
bas,_,son=s.partition("<!--KAYNAKLAR-->")
son_govde=son.split("\n## 6. Devam notu",1)[1]
etiketler=[]
for m in re.finditer(r"\[((?:R\d+-\d+(?:,\s*)?)+)\]", bas+son_govde):
    for t in re.split(r",\s*", m.group(1)):
        if t not in etiketler: etiketler.append(t)
etiketler.sort(key=lambda x:(int(x.split("-")[0][1:]),int(x.split("-")[1])))
satir=["Köşeli parantezli kodlar bu listedeki satırlardır. Her satır bu oturumda kaynağından kontrol edildi; durum sütunu doğrulayıcının kararıdır.",""]
eksik=[]
for t in etiketler:
    v=ver.get(t); l=led.get(t)
    if not v or not l: eksik.append(t); continue
    metin=v.get("dogru_ifade") if v["karar"] in ("düzeltildi","yanlış") and v.get("dogru_ifade") else l["iddia"]
    metin=re.sub(r"\s+"," ",metin).strip()
    if len(metin)>330:
        kes=metin[:330]
        son=max(kes.rfind(". "),kes.rfind("; "))
        metin=(kes[:son+1] if son>150 else kes.rsplit(" ",1)[0]+"…")
    url=" ; ".join(u.strip() for u in v["kaynak"].split(" ; ") if u.strip().startswith("http")) or v["kaynak"]
    satir.append(f"- **[{t}]** ({v['karar']}) {metin} — {url}")
yeni=bas+"<!--KAYNAKLAR-->\n"+"\n".join(satir)+"\n\nBacktest sayıları kendi hesabımızdır; tablolar `ek/veri/` klasöründe, özetleri `ek/ajanlar/` klasöründe.\n\n## 6. Devam notu"+son_govde
open(RAP,"w").write(yeni)
print("etiket:",len(etiketler),"eksik:",eksik)
govde=re.sub(r"(?m)^\|.*$","",yeni.split("## 5. Kaynaklar")[0])
print("gövde kelime (tablolar hariç):",len(govde.split()))
