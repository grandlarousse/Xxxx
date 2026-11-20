#!/usr/bin/env python3
"""XELKT uye tablosu. Girdi: isy_parse.py'nin JSON ciktisi. python3 -I xelkt_tablo.py <isy.json> <cikti.csv>
Agirlik yaklasiktir: PD x halka aciklik orani / toplam (Is Yatirim verisi); resmi BIST agirligi degildir."""
import csv, json, sys
# sym: (ad, ana_faaliyet, halka_arz_yili, not)   "?" = emin degilim (ajan bilgisi, dogrulanmadi)
M = {
"A1YEN": ("A1 Yenilenebilir Enerji Üretim A.Ş.", "üretim-yenilenebilir", "2021?", "eski Kartal Yenilenebilir (KARYE); İş Yatırım hâlâ eski adla listeliyor"),
"AHGAZ": ("Ahlatcı Doğal Gaz Dağıtım Enerji ve Yatırım A.Ş.", "doğal gaz dağıtımı", "2022", ""),
"AKENR": ("Akenerji Elektrik Üretim A.Ş.", "üretim-termik", "2000", "karma: doğal gaz + hidro"),
"AKFYE": ("Akfen Yenilenebilir Enerji A.Ş.", "üretim-yenilenebilir", "2023", ""),
"AKSEN": ("Aksa Enerji Üretim A.Ş.", "üretim-termik", "2010", "VİOP pay vadelisi var"),
"AKSUE": ("Aksu Enerji ve Ticaret A.Ş.", "üretim-yenilenebilir", "2000", ""),
"ALFAS": ("Alfa Solar Enerji Sanayi ve Ticaret A.Ş.", "güneş paneli-ekipman", "2022", ""),
"ARFYE": ("Arf Bio Yenilenebilir Enerji Üretim A.Ş.", "üretim-yenilenebilir", "2026", "ilk işlem 05.01.2026 (Bloomberg HT)"),
"AYDEM": ("Aydem Yenilenebilir Enerji A.Ş.", "üretim-yenilenebilir", "2021", ""),
"AYEN": ("Ayen Enerji A.Ş.", "üretim-yenilenebilir", "2000", ""),
"BESTE": ("Best Brands Grup Enerji Yatırım A.Ş.", "üretim-yenilenebilir?", "2026", "ilk işlem 11.02.2026, Ana Pazar (KAP)"),
"BIOEN": ("Biotrend Çevre ve Enerji Yatırımları A.Ş.", "üretim-yenilenebilir", "2021", "biyokütle/atık"),
"BIGEN": ("Birleşim Grup Enerji Yatırımları A.Ş.", "üretim-yenilenebilir?", "2025", "talep toplama 28-30.01.2025"),
"CONSE": ("Consus Enerji İşletmeciliği ve Hizmetleri A.Ş.", "üretim-termik?", "2022", "dağıtık üretim (kojenerasyon + güneş)"),
"CWENE": ("CW Enerji Mühendislik Ticaret ve Sanayi A.Ş.", "güneş paneli-ekipman", "2023", ""),
"CANTE": ("Çan2 Termik A.Ş.", "üretim-termik", "2021", "yerli kömür"),
"CATES": ("Çates Elektrik Üretim A.Ş.", "üretim-termik", "2023", "kömür"),
"ARASE": ("Doğu Aras Enerji Yatırımları A.Ş.", "dağıtım-perakende", "2021", ""),
"ECOGR": ("Ecogreen Enerji Holding A.Ş.", "üretim-yenilenebilir?", "2025", "ilk işlem 03.11.2025, Ana Pazar"),
"ENDAE": ("Enda Enerji Holding A.Ş.", "üretim-yenilenebilir", "2025", "talep toplama 05-07.02.2025; ilk işlem ~13.02.2025"),
"ENJSA": ("Enerjisa Enerji A.Ş.", "dağıtım-perakende", "2018", "VİOP pay vadelisi var"),
"ENERY": ("Enerya Enerji A.Ş.", "doğal gaz dağıtımı", "2023", ""),
"ESEN": ("Esenboğa Elektrik Üretim A.Ş.", "üretim-yenilenebilir", "2020", "güneş; EPC de var"),
"GWIND": ("Galata Wind Enerji A.Ş.", "üretim-yenilenebilir", "2021", ""),
"HUNER": ("Hun Yenilenebilir Enerji Üretim A.Ş.", "üretim-yenilenebilir", "2021", ""),
"ENTRA": ("IC Enterra Yenilenebilir Enerji A.Ş.", "üretim-yenilenebilir", "2024", ""),
"IZENR": ("İzdemir Enerji Elektrik Üretim A.Ş.", "üretim-termik", "2023", "ithal kömür"),
"KLYPV": ("Kalyon Güneş Teknolojileri Üretim A.Ş.", "güneş paneli-ekipman", "2025", "gong 13.02.2025"),
"LYDYE": ("Lydia Yeşil Enerji Kaynakları A.Ş.", "üretim-yenilenebilir?", "?", "eski Tetamat Gıda (TETMT); kod 01.10.2024'te değişti; İş Yatırım sektörü hâlâ Gıda"),
"MAGEN": ("Margün Enerji Üretim Sanayi ve Ticaret A.Ş.", "üretim-yenilenebilir", "2021", "güneş"),
"MASFN": ("Masfen Enerji A.Ş.", "diğer?", "2026", "ilk işlem 30.07.2026 (KAP)"),
"METEN": ("Metgün Enerji Yatırımları A.Ş.", "üretim-yenilenebilir?", "2026", "ilk işlem 28.07.2026, Yıldız Pazar"),
"MOGAN": ("Mogan Enerji Yatırım Holding A.Ş.", "üretim-yenilenebilir", "2024", "jeotermal/rüzgâr"),
"NTGAZ": ("Naturelgaz Sanayi ve Ticaret A.Ş.", "doğal gaz dağıtımı", "2021", "taşımalı CNG/LNG"),
"NATEN": ("Naturel Yenilenebilir Enerji Ticaret A.Ş.", "üretim-yenilenebilir", "2019", "güneş; EPC de var"),
"ODAS": ("Odaş Elektrik Üretim Sanayi Ticaret A.Ş.", "üretim-termik", "2013", "VİOP pay vadelisi var"),
"PAMEL": ("Pamukova Yenilenebilir Elektrik Üretimi A.Ş.", "üretim-yenilenebilir", "?", ""),
"SMRTG": ("Smart Güneş Enerjisi Teknolojileri A.Ş.", "güneş paneli-ekipman", "2022", ""),
"TATEN": ("Tatlıpınar Enerji Üretim A.Ş.", "üretim-yenilenebilir", "2023", "rüzgâr"),
"VEYAS": ("Türker Vangölü Enerji Yatırım A.Ş.", "dağıtım-perakende?", "2026", "ilk işlem 20.08.2026 (KAP); fiili dolaşım çok düşük"),
"ZEDUR": ("Zedur Enerji Elektrik Üretim A.Ş.", "üretim-yenilenebilir?", "?", ""),
"ZOREN": ("Zorlu Enerji Elektrik Üretim A.Ş.", "diğer", "2000", "karma: yenilenebilir üretim + dağıtım-perakende"),
}
KAYNAK = "İş Yatırım Temel Değerler ve Oranlar (isyatirim.com.tr), 20.11.2026 çekim; ağırlık = PD x halka açıklık / toplam, yaklaşık"
d = json.load(open(sys.argv[1], encoding="utf-8"))
assert len(M) == 42 and all(k in d for k in M)
tot = sum(d[k]["pd_mn_tl"] * d[k]["hao"] / 100 for k in M)
rows = []
for k, (ad, faal, yil, notu) in M.items():
    v = d[k]
    w = v["pd_mn_tl"] * v["hao"] / 100 / tot * 100
    rows.append([k, ad, "%.1f" % v["pd_mn_tl"], "%.1f" % v["hao"], "%.2f" % w, faal, yil, KAYNAK,
                 (notu + "; " if notu else "") + "isy_sektor=" + v["sektor"]])
rows.sort(key=lambda r: -float(r[4]))
with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["sym", "ad", "piyasa_degeri_mn_tl", "halka_aciklik", "yaklasik_agirlik", "ana_faaliyet", "halka_arz_yili", "kaynak", "not"])
    w.writerows(rows)
print("satir", len(rows), "toplam PD mn TL %.0f" % sum(d[k]["pd_mn_tl"] for k in M), "halka acik PD %.0f" % tot)
print("ilk10 agirlik toplami %.1f" % sum(float(r[4]) for r in rows[:10]), "ilk5 %.1f" % sum(float(r[4]) for r in rows[:5]))
print("ilk10:", " ".join("%s %s" % (r[0], r[4]) for r in rows[:10]))
from collections import defaultdict
g = defaultdict(float)
for r in rows: g[r[5].rstrip("?")] += float(r[4])
print({k: round(v, 1) for k, v in g.items()})
print("VİOP'lu 3 hisse agirlik: %.1f" % sum(float(r[4]) for r in rows if r[0] in ("AKSEN", "ENJSA", "ODAS")))
