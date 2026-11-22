#!/usr/bin/env python3
"""Backtest ajanı sonuçlarını ek/ajanlar/d4_Kx.md olarak yazar; özetleri basar."""
import json, sys, os
B="/root/.claude/projects/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/subagents/workflows"
O="/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/ajanlar"
ws=["wf_75ef031f-ea2","wf_b649a9d9-83d","wf_747f4928-f03","wf_bd8ee477-7ed","wf_1f1ea585-214"]
goster=set(sys.argv[1:])
def t(x): return "" if x is None else str(x).replace("|","/").replace("\n"," ")
kol=["kural_id","ad","hedef","yon","h","giris","korunma","is_net_bps","oos_net_bps","oos_n","oos_t","oos_p","son_net_bps","son_t","girisA_oos_net_bps","basabas_bps","vix30","sinif","gerekce"]
for w in ws:
    lab={}
    p=f"{B}/{w}/journal.jsonl"
    if not os.path.exists(p): continue
    for line in open(p):
        try:e=json.loads(line)
        except Exception: continue
        if e.get("type")=="started": lab[e["key"]]=e["label"]
        if e.get("type")=="result" and isinstance(e.get("result"),dict):
            r=e["result"]; ad=lab[e["key"]].split("·")[0].strip()
            with open(f"{O}/d4_{ad}.md","w") as f:
                f.write(f"# {ad} · backtest\n\n{r['arac']}\n\nSınanan kural × varyant: {r['test_sayisi']} · IS adayı: {r['aday_sayisi']} · OOS'tan geçen: {r['oos_gecen']}\n\n## Özet\n\n{r['ozet']}\n\n## Tablo\n\n| "+" | ".join(kol)+" |\n|"+"---|"*len(kol)+"\n")
                for s in r["tablo"]: f.write("| "+" | ".join(t(s.get(k)) for k in kol)+" |\n")
                for k,b in (("elenenler","Elenenler"),("bugun","Bugünkü durum"),("sapmalar","Sapmalar"),("notlar","Notlar")):
                    f.write(f"\n## {b}\n\n{r.get(k,'')}\n")
                f.write("\n## Dosyalar\n\n"+"\n".join("- "+x for x in r.get("dosyalar",[]))+"\n")
            print(f"== {ad}: {r['arac'][:60]} | test {r['test_sayisi']} aday {r['aday_sayisi']} OOS geçen {r['oos_gecen']}")
            if ad in goster:
                print("ÖZET:",r["ozet"]); print("BUGÜN:",r.get("bugun","")[:1500]); print("SAPMALAR:",r.get("sapmalar","")[:600]); print("NOTLAR:",r.get("notlar","")[:1500])
                for s in r["tablo"]:
                    if s.get("sinif") not in ("ELENDİ","ELENDI"): print("  SATIR:",{k:s.get(k) for k in kol if s.get(k) not in (None,"")})
