#!/usr/bin/env python3
"""Workflow cikti dosyasindan kesif sonuclarini (D*) ek/parcalar/kesif_D*.json olarak kaydeder ve sikistirilmis liste basar.
Kullanim: python3 kesif_kaydet.py <workflow-output.json> [...]"""
import json, os, sys
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in sys.argv[1:]:
    for item in json.load(open(p))["result"]:
        s = item["sonuc"]
        if not isinstance(s, dict) or "kitaplar" not in s: continue
        json.dump(s, open(f"{K}/parcalar/kesif_{item['id']}.json", "w"), ensure_ascii=False, indent=1)
        print(f"## {item['id']} | {s['arac']} | {len(s['kitaplar'])} kitap")
        for b in sorted(s["kitaplar"], key=lambda b: -b["yakinlik"]):
            print(f"{b['yakinlik']}|{b['yazar'][:30]}|{b['ozgun_ad'][:58]}|{b['yil'][:10]}|{(b.get('turkce_ad') or '')[:30]}|{b.get('tur','')[:14]}")
        if s.get("en_cok_onerilenler"): print("EN COK:", " ; ".join(s["en_cok_onerilenler"]))
        if s.get("elenenler"): print("ELENEN:", " ;; ".join(x[:80] for x in s["elenenler"])[:900])
