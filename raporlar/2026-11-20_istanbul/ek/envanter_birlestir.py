#!/usr/bin/env python3
"""Ajan dosyalarındaki (W*-*.md) "Envanter" tablolarını tek dosyada birleştirir.

Kullanım: python3 envanter_birlestir.py  ->  ../ENVANTER.md
Yalnızca biçim işi yapar; içerik ajan dosyalarından değiştirilmeden alınır.
"""
import re
from pathlib import Path

EK = Path(__file__).resolve().parent
HEDEF = EK.parent / "ENVANTER.md"

# Dosya öneki -> bölüm başlığı. Sıra rapordaki sırayı belirler.
BOLUMLER = [
    ("B1_", "Dil değişimi buluşmaları ve konuşma kulüpleri"),
    ("G5a_", "Dil buluşmaları: diğer diller ve okul kulüpleri"),
    ("B2_", "Yabancı toplulukları ve uluslararası buluşmalar"),
    ("G5b_", "Erasmus çevresi, Couchsurfing, uluslararası kulüpler"),
    ("B3_", "Kültür enstitüleri, dil kursları, tandem"),
    ("H3_", "Enstitü ve kurs takibi"),
    ("N7_", "Erasmus+ ve uluslararası gençlik projeleri"),
    ("B12_", "Uygulamalar ve etkinlik platformları"),
    ("G6_", "Tanışma etkinlikleri ve yerli sosyal kulüpler"),
    ("B4_", "Koşu, bisiklet, triatlon"),
    ("G2_", "Sosyal koşu ve yürüyüş kulüpleri"),
    ("B5_", "Dans: swing ve tango"),
    ("G3_", "Dans: salsa, bachata, milonga, halk dansları"),
    ("B6_", "Tırmanış ve okçuluk"),
    ("G4_", "Padel, tenis, voleybol ve takım sporları"),
    ("N1_", "Doğa yürüyüşü, gezi ve su sporları grupları"),
    ("N6_", "Yoga, fitness ve dövüş sporları toplulukları"),
    ("N2_", "Yaratıcı atölyeler ve sahne"),
    ("N3_", "Fikir ve oyun toplulukları"),
    ("N4_", "Gönüllülük ve gençlik örgütleri"),
    ("N5_", "Ortak çalışma alanları ve profesyonel ağlar"),
    ("B15_", "Semt karşılaştırması"),
    ("H2_", "Semt takibi: deprem, ortak yaşam, kira"),
    ("A1_", "Müzeler ve sergi kurumları"),
    ("A2_", "Tiyatro, opera, konser, festival"),
    ("A3_", "Belediye ve kamu olanakları"),
    ("A4_", "Semt rotaları ve rehberli yürüyüşler"),
    ("A5_", "Doğa, deniz, günübirlik"),
    ("A6_", "Yeme-içme ve gece hayatı"),
    ("N8_", "Etkinlik takvimi"),
]


def envanter_al(metin):
    """'## Envanter' başlığından sonraki ilk tabloyu döndürür."""
    m = re.search(r"^#{1,4}\s*.*envanter.*$", metin, flags=re.I | re.M)
    if not m:
        return []
    satirlar = []
    for satir in metin[m.end():].splitlines():
        if satir.startswith("|"):
            satirlar.append(satir.rstrip())
        elif satirlar and satir.strip() == "":
            continue
        elif satirlar:
            break
        elif satir.startswith("#"):
            break
    return satirlar


def main():
    dosyalar = sorted(EK.glob("W*-*.md"))
    cikti = [
        "# Envanter: bütün topluluk, mekân ve etkinlikler",
        "",
        "Bu dosya araştırmacıların envanter tablolarının birleşimidir; ana rapor `RAPOR.md`.",
        "Tarihler ve ücretler 20 Kasım 2026'da görülen kaynaklara dayanır. "
        "Gitmeden önce bağlantıdan günü, saati ve ücreti teyit et; "
        "\"güncelliği belirsiz\" ve \"doğrulanmadı\" notlu satırlara güvenme.",
        "",
    ]
    toplam = 0
    kullanilan = set()
    for onek, baslik in BOLUMLER:
        for dosya in dosyalar:
            if not dosya.name.split("-", 1)[1].startswith(onek):
                continue
            tablo = envanter_al(dosya.read_text(encoding="utf-8"))
            if len(tablo) < 3:
                continue
            kullanilan.add(dosya.name)
            toplam += len(tablo) - 2
            cikti += [f"## {baslik}", "", f"Kaynak dosya: `ek/{dosya.name}`", ""] + tablo + [""]
    atlanan = [d.name for d in dosyalar if d.name not in kullanilan]
    HEDEF.write_text("\n".join(cikti), encoding="utf-8")
    print(f"{HEDEF} yazıldı: {len(kullanilan)} dosya, {toplam} satır")
    if atlanan:
        print("Envanteri alınmayan dosyalar:", ", ".join(atlanan))


if __name__ == "__main__":
    main()
