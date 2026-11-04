#!/usr/bin/env python3
"""Seri için Instagram açıklamalarını tek dosyada toplar: seri/PAYLASIM_METINLERI.md"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, "seri")
NASIL = ("Nasıl okunur? 1 nokta = 100 kişi. Kırmızı taralı alan Türk yurdudur (köylerin en az %40’ı Türk); köylerin en az "
         "%40’ı Müslüman olan yerler en kalabalık Müslüman topluluğun rengini alır; diğer alanlar yerel çoğunluk.")


def _suf(v):
    s_ = f"{v:.1f}".replace(".", ",")
    return s_, "’" + {0: "ı", 1: "i", 2: "si", 3: "ü", 4: "ü", 5: "i", 6: "sı", 7: "si", 8: "i", 9: "u"}[int(s_[-1])]


def sync_yurt():
    """Türk yurdu açıklamalarındaki km² ve yüzde cümlesini son çizimin istatistiğiyle eşitler."""
    import re
    for n, key in enumerate(("rodoplar", "drama", "deliorman", "dobruca", "makedonya"), 1):
        p = os.path.join(S, f"yurt_{key}.json")
        sp = os.path.join(HERE, "cikti", "turk_yurtlari", f"{n:02d}_{key}_stats.json")
        if not (os.path.exists(p) and os.path.exists(sp)):
            continue
        d = json.load(open(p, encoding="utf-8"))
        st = json.load(open(sp, encoding="utf-8"))
        km = f"{int(round(st['km2_turk'], -2)):,}".replace(",", ".")
        t, ts = _suf(st["turk_in_yurt"])
        m, ms = _suf(st["muslim_in_yurt"])
        cap = re.sub(r"Haritadaki kırmızı Türk yurdu yaklaşık [\d.]+ km²[;.] [Bb]urada yaşayanların %[\d,]+’\w+ Türk, %[\d,]+’\w+ Müslümandı",
                     f"Haritadaki kırmızı Türk yurdu yaklaşık {km} km²; burada yaşayanların %{t}{ts} Türk, %{m}{ms} Müslümandı",
                     d["caption"])
        cap = re.sub(r"Nasıl okunur\?[^\n]*", NASIL, cap)
        if cap != d["caption"]:
            d["caption"] = cap
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("güncellendi:", key, km, t, m)


sync_yurt()
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
out.append("\n\n# RUMELİ TÜRK YURTLARI 1876 — 5 post (Türklerin bariz çoğunlukta olduğu kuşaklar)\n")
out.append("Görseller: `cikti/turk_yurtlari/NN_*_ig.jpg`. Kırmızı taralı alan = Türk yurdu (köylerin en az %40’ı Türk); "
           "köylerin en az %40’ı Müslüman olan yerler en kalabalık Müslüman topluluğun rengini alır; diğer alanlar yerel çoğunluk. "
           "Topluluklar adıyla: Türk, Pomak, Arnavut, Boşnak, Torbeş, Çerkes, Müslüman Roman; Bulgar, Rum, Sırp, Hırvat…\n")
for n, title, key in (("1", "Doğu Rodoplar", "rodoplar"), ("2", "Drama, Kavala ve Sarışaban", "drama"),
                      ("3", "Deliorman ve Gerlovo", "deliorman"), ("4", "Dobruca", "dobruca"),
                      ("5", "Makedonya Türkleri", "makedonya")):
    p = os.path.join(S, f"yurt_{key}.json")
    cap = json.load(open(p, encoding="utf-8")).get("caption", "") if os.path.exists(p) else ""
    out.append(f"\n---\n\n## {n}/5 · {title}\n\nGörsel: `cikti/turk_yurtlari/0{n}_{key}_ig.jpg`\n\n```\n{cap.strip() or '(metin bekleniyor)'}\n```\n")
open(os.path.join(S, "PAYLASIM_METINLERI.md"), "w", encoding="utf-8").write("\n".join(out))
print("yazıldı:", os.path.join(S, "PAYLASIM_METINLERI.md"))
