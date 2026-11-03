#!/usr/bin/env python3
"""Seri için Instagram açıklamalarını tek dosyada toplar: seri/PAYLASIM_METINLERI.md"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, "seri")
ORDER = [("01", "Genel harita · Rumeli’nin Son Işıkları", "rakamlar", "caption_post1"),
         ("02", "Tuna Vilâyeti: Deliorman ve Dobruca", "tuna", "caption"),
         ("03", "Edirne Vilâyeti: Trakya ve Rodoplar", "edirne", "caption"),
         ("04", "Makedonya ve Teselya", "makedonya", "caption"),
         ("05", "Arnavutluk, Kosova ve Epir", "arnavut", "caption"),
         ("06", "Bosna-Hersek ve Yenipazar", "bosna", "caption"),
         ("07", "Bulgaristan 1875, il il", "bulgaristan", "caption"),
         ("08", "Rakamlarla Rumeli 1876 · 93 Harbi", "rakamlar", "caption")]
out = ["# RUMELİ 1876 — Paylaşım metinleri\n",
       "Görseller: `cikti/seri/NN_*_ig.jpg` (Instagram 1080×1350). Tam çözünürlük: aynı adlı `.png` (2160×2700).\n",
       "Önerilen akış: 1/8 kapak (genel harita) → 2–6 bölgeler → 7 Bulgaristan → 8 rakamlar ve 93 Harbi. "
       "Her gönderi tek başına da anlaşılır; açıklamalarda seri numarası var.\n"]
for n, title, key, field in ORDER:
    p = os.path.join(S, f"icerik_{key}.json")
    cap = ""
    if os.path.exists(p):
        cap = json.load(open(p, encoding="utf-8")).get(field, "") or ""
    out.append(f"\n---\n\n## {n}/8 · {title}\n\nGörsel: `cikti/seri/{n}_*_ig.jpg`\n\n```\n{cap.strip() or '(metin bekleniyor)'}\n```\n")
open(os.path.join(S, "PAYLASIM_METINLERI.md"), "w", encoding="utf-8").write("\n".join(out))
print("yazıldı:", os.path.join(S, "PAYLASIM_METINLERI.md"))
