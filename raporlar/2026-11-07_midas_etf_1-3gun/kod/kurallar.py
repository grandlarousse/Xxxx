"""Nihai kural kataloğu (RAPOR.md kodları) — kartlar, izleme tablosu ve uzlaştırma bu tek kaynağı kullanır.
Her kural: aile strateji kimliği, kısa tanım (kesilmeden), sinyal kaynağı, araçlar (ana araç ilk), kademe."""

RULES = {
    "A1": {"id": "abd_endeks_S2", "kisa": "QQQ IBS<0,10 + düşüş günü · C1 (ertesi gün kapanışta gir) · 3 gün", "sinyal": "QQQ",
           "araclar": {"QQQ": "ana araç", "QLD": "2x araç (dayanak tutarının ~1/2'si)", "TQQQ": "3x araç (dayanak tutarının ~1/3'ü)"}, "kademe": "A"},
    "A2": {"id": "sektor_tematik_S1", "kisa": "SMH IBS<0,20 · C0 (kapanış/after-hours limit) · 1 gün", "sinyal": "SMH",
           "araclar": {"SMH": "ana araç", "SOXX": "kopya araç (aynı sinyal SMH'den)"}, "kademe": "A"},
    "A2-3x": {"id": "sektor_tematik_S2", "kisa": "A2 sinyaliyle SOXL (3x) · C0 · 1 gün (zayıf: Midas doğrulanmadı, maxDD −%53)", "sinyal": "SMH",
              "araclar": {"SOXL": "3x araç (SMH tutarının ~1/3'ü)"}, "kademe": "B"},
    "B1": {"id": "abd_endeks_S1", "kisa": "SPY IBS<0,10 + düşüş · C1 · 3 gün (QQQ ile aynı gün sinyal verirse yalnız A1)", "sinyal": "SPY",
           "araclar": {"SPY": "ana araç", "SSO": "2x araç", "SPXL": "3x araç (1/3 boyut)"}, "kademe": "B"},
    "B2": {"id": "metal_madenci_S3", "kisa": "GDXJ IBS<0,10 + düşüş · C0 · 3 gün (kapanışa bağımlı)", "sinyal": "GDXJ",
           "araclar": {"GDXJ": "ana araç", "JNUG": "2x araç (Midas doğrulanmadı)"}, "kademe": "B"},
    "B3a": {"id": "metal_madenci_S1", "kisa": "Ay sonu: son işlem günü kapanışı → 3. işlem günü kapanışı · GDX", "sinyal": "takvim",
            "araclar": {"GDX": "ana araç", "NUGT": "2x araç (Midas doğrulanmadı)"}, "kademe": "B"},
    "B3b": {"id": "metal_madenci_S2", "kisa": "Ay sonu: son işlem günü kapanışı → 3. işlem günü kapanışı · GLD (B3a ile aynı bahis)", "sinyal": "takvim",
            "araclar": {"GLD": "ana araç", "IAU": "kopya araç", "GLDM": "kopya araç"}, "kademe": "B"},
    "B4": {"id": "uluslararasi_S1", "kisa": "SPY ≤ −%1,5 gününde SPY'dan çok düşen Asya ETF'leri · C0 · 1 gün (gün kümeli t 1,9: eşik altı)", "sinyal": "SPY + ETF",
           "araclar": {s: "sepet üyesi" for s in ["EWJ", "EWY", "EWT", "FXI", "EWA", "EWH"]}, "kademe": "B"},
    "B5": {"id": "uluslararasi_S2", "kisa": "EWY IBS<0,10 + düşüş · C0 · 1 gün", "sinyal": "EWY",
           "araclar": {"EWY": "ana araç", "KORU": "3x araç (Midas doğrulanmadı, en fazla 1 gün)"}, "kademe": "B"},
    "B6": {"id": "tahvil_doviz_S1", "kisa": "10Y Hazine ihalesinden 3 iş günü önce kapanışta al → ihaleden 1 gün önce kapanışta sat", "sinyal": "takvim",
           "araclar": {"TBT": "tercih edilen araç (−2x, daha düşük kuyruk)", "TMV": "−3x araç"}, "kademe": "B"},
    "B7": {"id": "enerji_tarim_S1", "kisa": "EIA doğalgaz raporundan önceki gün kapanışta KOLD al → rapor günü kapanışında sat (yalnız Kasım-Mart)", "sinyal": "takvim",
           "araclar": {"KOLD": "ana araç (⚠ PTP)"}, "kademe": "B"},
    "B8": {"id": "enerji_tarim_S2", "kisa": "USO alt Bollinger(20,2) kırılımı → ertesi gün kapanışta al (C1) · 2 gün", "sinyal": "USO",
           "araclar": {"USO": "ana araç (⚠ PTP)", "UCO": "kaldıraçlı araç (2026 betası ~1,1)"}, "kademe": "B"},
    "B9": {"id": "volatilite_S1", "kisa": "SVXY RSI(2)<10 ve SVXY>SMA200 · C0 · 2 gün (PTP teyidi yoksa aynı sinyalle QQQ)", "sinyal": "SVXY",
           "araclar": {"SVXY": "ana araç (⚠ PTP)"}, "kademe": "B"},
    "B10": {"id": "tek_hisse_kaldiracli_S1", "kisa": "Hisse RSI(2)<10 ve hisse>SMA200 → 2x ETF (ya da hisse) · C0 · hisse>SMA5'te ya da en geç 3 günde çık", "sinyal": "dayanak hisse",
            "araclar": {"NVDL": "NVDA'nın 2x aracı", "TSLL": "TSLA'nın 2x aracı", "AMZU": "AMZN'nin 2x aracı", "MSFU": "MSFT'nin 2x aracı",
                        "GGLL": "GOOGL'ün 2x aracı", "AAPU": "AAPL'nin 2x aracı (en zayıf dayanak)", "METU": "META'nın 2x aracı (gerçek ETF'te negatif)"}, "kademe": "B"},
    "F": {"id": "kripto_S2", "kisa": "FİLTRE, strateji değil: BTC/IBIT kapanış>SMA10>SMA50 ise trend yukarı (IBIT döneminde t 0,6)", "sinyal": "IBIT",
          "araclar": {"IBIT": "filtre", "GBTC": "filtre", "FBTC": "filtre", "ETHA": "filtre (ETH'de de çalışmıyor)"}, "kademe": "C"},
}
ID2CODE = {v["id"]: k for k, v in RULES.items()}

def rules_for(sym):
    return [(k, v, v["araclar"][sym]) for k, v in RULES.items() if sym in v["araclar"]]

def kademe_for(sym):
    ks = [v["kademe"] for k, v, _ in rules_for(sym)]
    return "A" if "A" in ks else ("B" if "B" in ks else "C")

# Aile içi strateji kısaltmalarını RAPOR kodlarına çevirme (kart metinlerinde 'S1' her ailede başka kural demek)
FAM_S = {
    "abd_endeks": {"S1": "B1", "S2": "A1", "S3": "S3 (çürütüldü)"},
    "sektor_tematik": {"S1": "A2", "S2": "A2-3x"},
    "tek_hisse_kaldiracli": {"S1": "B10"},
    "enerji_tarim": {"S1": "B7", "S2": "B8"},
    "metal_madenci": {"S1": "B3a", "S2": "B3b", "S3": "B2", "S4": "S4 (çürütüldü)", "S5": "S5 (çürütüldü)"},
    "tahvil_doviz": {"S1": "B6"},
    "volatilite": {"S1": "B9"},
    "kripto": {"S1": "S1 (çürütüldü)", "S2": "F (filtre)"},
    "uluslararasi": {"S1": "B4", "S2": "B5"},
}

# PTP/K-1 yapısı (ihraççı/fon yapısına göre; Midas'ta kesinti uygulanıp uygulanmadığı uygulamada teyit edilmeli)
PTP_EXTRA = {"UNG", "USO", "BNO", "USL", "UNL", "UGA", "CPER",                      # USCF
             "BOIL", "KOLD", "UCO", "SCO", "UVXY", "SVXY", "VIXY", "VIXM", "UGL", "GLL", "AGQ", "ZSL", "YCS", "YCL", "EUO", "ULE",  # ProShares Trust II
             "DBA", "DBB", "DBC", "DBO", "UUP", "UDN",                               # Invesco DB
             "CORN", "WEAT", "SOYB", "CANE",                                         # Teucrium
             "GSG", "SVIX", "UVIX"}

# Kart metni düzeltmeleri (denetçi düzeltmeleri ve eleştiri bulguları)
STRAT_PATCH = {
    "sektor_tematik_S1": {"giris": "ANA YOL: resmî ABD kapanışından sonra kesin IBS'yi gör (SMH günlük mum); IBS<0,20 ise after-hours'ta (tercihen TR 00:00-01:00 kış / 23:00-00:00 yaz) "
                          "resmî kapanış fiyatı + 2-5 sent LİMİT emirle, tam adet al (denetçi bu yolun maliyetini ~6 bp ölçtü). İKİNCİ YOL: kapanıştan dakikalar önce (kış TR 23:45-23:58) anlık IBS ile "
                          "piyasa/agresif limit emir (kapanış öncesi sınıflama hatası ~15-20 bp maliyet). Ertesi açılışta (O1) GİRME: kenar ~17 bp'ye, C1'de ~0'a düşer."},
    "metal_madenci_S3": {"guven": "dusuk", "giris": "C0: sinyal günü kapanışında (kış TR ~23:45-23:55 anlık IBS ile ya da kapanış sonrası after-hours limit). Kapanış kaçarsa bu işlemi ATLA "
                         "(denetçi: O1 sonucu tek tutuş süresindeki sivri tepe; kural kapanışa bağımlı)."},
    "uluslararasi_S1": {"cikis": "t+1 kapanışına ~10 dk kala sat (kış TR ~23:50, yaz ~22:50). Stop kullanılmadı. Ertesi açılışta GİRME (O1 sepette −3 bp; FXI'de −33 bp)."},
    "volatilite_S1": {"islem_etf": ["SVXY"], "notlar_on": "SVIX nihai olarak elendi (−1x yapı, Şubat 2018 tipi olayda ~%90+ kayıp). PTP kesintisi yoksa SVXY; teyit yoksa aynı SVXY sinyaliyle QQQ/QLD (denetçi önerisi). "},
    "tek_hisse_kaldiracli_S1": {"notlar_on": "Kaldıraçlı ETF Midas'ta yoksa ya da riski fazla geliyorsa aynı sinyalle hissenin kendisi (denetçi: 1x hisse daha sağlam araç). Aynı anda en çok 2 hisse. "},
    "kripto_S2": {"ad_on": "FİLTRE (strateji değil) — ", "notlar_on": "Aşağıdaki 'Geçmiş (ajan)' rakamı dayanak BTC'nin 00:00 UTC serisine (2016+) aittir; ETF'te geçerli değildir (son kontrol: IBIT C0 +30 bp, t 0,6). Yalnız 'BTC trendi yukarı mı' filtresi olarak kullanın. "},
}
GEREKCE_PATCH = {
    "SPY": "S&P 500'ün ana, en likit aracı (41,6 mlr $/gün, makas ~1 bp). B1 (zayıf) kuralının aracı ve A1 için piyasa teyidi; CME_MINI:ES1! ile izlenir.",
    "GLD": "Altının ana ve PTP olmayan aracı (3,7 mlr $/gün, ~13 bp). Doğrulanmış strateji yok; yalnız B3b (ay sonu, zayıf). COMEX:GC1! ile izlenir; getirisi çoğunlukla gece oluşur.",
    "GDX": "Altın madencilerinin ana aracı (1,9 mlr $/gün, ~13 bp). Yalnız B3a (ay sonu, zayıf: en iyi 5 işlem çıkarılınca t<1,2). IBS kuralı GDX'te çalışmıyor (GDXJ'de B2).",
    "SBIT": "Kısa BTC görüşü için −2x araç (yedek). Perşembe kuralı (S1) çürütüldü; doğrulanmış strateji yok.",
}
TEXT_FIX = [
    ("OSE gündüz seansı TR 02:45-09:15, gece seansı TR 10:30-00:00", "OSE gündüz seansı TR 02:45-09:45, gece seansı TR 11:00-00:00"),
]
UNDERLYING_CARD = {"QLD": "QQQ", "TQQQ": "QQQ", "SSO": "SPY", "SPXL": "SPY", "SOXX": "SMH", "SOXL": "SMH", "JNUG": "GDXJ", "NUGT": "GDX",
                   "KORU": "EWY", "TBT": "TMV", "UCO": "USO", "IAU": "GLD", "GLDM": "GLD", "YINN": "FXI", "BITX": "IBIT", "ETHU": "ETHA"}
