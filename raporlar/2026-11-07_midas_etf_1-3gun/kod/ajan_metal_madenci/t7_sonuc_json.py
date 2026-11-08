"""Sonuç JSON'unu (sonuclar/aile_metal_madenci/sonuc.json) diğer betiklerin CSV çıktılarından üretir.
Önce: t1, t2, t3, t3b, t3c, t4 (+ --breakeven --gdxoncu), t5, t6 çalışmış olmalı.
Çalıştır: python3 -I kod/ajan_metal_madenci/t7_sonuc_json.py"""
import os, sys, json, ast
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import mm

R = mm.ROOT; O = mm.OUTD
TV = mm.tv_map()
VALID = mm.tv_valid()
LTV = {"VIX_dlog": "CBOE:VIX", "GVZ_dlog": "CBOE:GVZ", "DFII10_d": "FRED:DFII10", "T10YIE_d": "FRED:T10YIE", "DGS10_d": "TVC:US10Y"}

def tvc(x):
    return LTV.get(x, TV.get(x, x))

SW = pd.read_csv(os.path.join(R, "sonuclar", "leadlag_sweep.csv"))
def sw(t, l):
    r = SW[(SW.target == t) & (SW.leader == l)]
    return r.iloc[0] if len(r) else None

def drv(t, leaders):
    out = []
    for l in leaders:
        r = sw(t, l)
        if r is None: continue
        out.append({"ad": l + " (eşzamanlı sürücü, öncü değil)", "tv": tvc(l), "corr_1y": round(float(r.corr_1y), 2), "beta_1y": round(float(r.beta_1y), 2)})
    return out

def lead(t, l, kind="lag", h=1, etki="", maliyet=""):
    r = sw(t, l)
    if r is None: return None
    tt = float(r[f"{kind}_t_h{h}"]); ti = float(r[f"{kind}_t_h{h}_is"]); to = float(r[f"{kind}_t_h{h}_oos"])
    bp = float(r[f"{kind}_bp_per_sd_h{h}"])
    return {"ad": l, "tv": tvc(l), "tip": ("gecikmeli (r_L(t) -> r_T(t+1..t+%d), kendi gecikmesi kontrollü)" % h) if kind == "lag"
            else ("yetişme (beta60*r_L(t) - r_T(t) -> r_T(t+1..t+%d))" % h),
            "etki": f"{bp:+.1f} bp / 1 sd öncü hareketi (h={h}); " + etki, "t": round(tt, 2), "is_t": round(ti, 2), "oos_t": round(to, 2),
            "fdr": bool(r[f"fdr10_{kind}_t_h{h}"]), "ufuk": f"{h} gün", "maliyet_sonrasi": maliyet}

def main():
    isl = pd.read_csv(os.path.join(O, "islenebilirlik.csv")).set_index("sym")
    ad = pd.read_csv(os.path.join(O, "aday_ozet.csv")).set_index("id")
    fdr = pd.read_csv(os.path.join(O, "fdr_tum_testler.csv"))
    NT = len(fdr)
    ER = pd.read_csv(os.path.join(O, "leadlag_ek_regresyon.csv"))
    def er(T, L, h, per="tum"):
        r = ER[(ER.target == T) & (ER.leader == L) & (ER.h == h) & (ER.donem == per)]
        return r.iloc[0] if len(r) else None

    # ---------------- izleme listesi
    K = {  # karar, gerekçe
        "GLD": ("kabul", "Altının ana aracı: 3,7 mlr $ medyan hacim, gidiş-dönüş ~13 bp (maliyet/1g oynaklık 0,07), grantor trust (PTP değil). S2 (ay sonu) ve S4 (IBS) adayları; gerçek zamanlı sürücü COMEX:GC1!."),
        "IAU": ("yedek", "GLD kopyası (korelasyon 0,998); maliyet 14 bp. Veride 2021-03-08 hatalı bar var (lead-lag'de sahte 'yetişme' üretiyor). GLD yerine ancak hisse fiyatı/kesir tercihi için."),
        "GLDM": ("yedek", "GLD kopyası (0,999), maliyet 14 bp, geçmiş 2018-06'dan. Uzun vadeli tutuş için ucuz gider oranı; 1-3 günde GLD'ye üstünlüğü yok."),
        "UGL": ("red", "2x altın; ProShares Trust II = PTP/K-1 -> %10 brüt satış stopajı (1446(f)) riski; Midas'ta PTP ibaresi kontrol edilmeli. Kaldıraç gerekiyorsa pozisyon büyütmek (GLD) daha güvenli."),
        "GLL": ("red", "-2x altın, PTP/K-1 riski; doğrulanmış kısa yön sinyali yok (FOMC sonrası düşüş anlamsız: t -1,6)."),
        "SLV": ("kabul", "Gümüşün ana aracı: 1,4 mlr $, ~14 bp, 1g oynaklık ~400 bp (maliyet/oynaklık 0,035). Doğrulanmış strateji YOK; COMEX:SI1! ve altın ile izlenir. 30.01.2026'da -%28,5 (tek gün) gerçek kuyruk riski."),
        "SIVR": ("yedek", "SLV kopyası (1,000), maliyet 16 bp, hacim 123 mn $."),
        "AGQ": ("red", "2x gümüş, PTP/K-1 riski; 30.01.2026'da -%60 gün; strateji yok."),
        "ZSL": ("red", "-2x gümüş, PTP/K-1 riski; kısa yön sinyali yok."),
        "PPLT": ("yedek", "Platin: 44 mn $, ~20 bp, oynaklık 320 bp. Strateji yok; NYMEX:PL1! ile izlenir. GDX sert düştüğü günün ertesinde PPLT de zayıf (kaçınma işareti, FDR'siz)."),
        "PALL": ("red", "Paladyum: 26,5 mn $, ~20 bp; ay sonu ve IBS kurallarında negatif; strateji/öncü yok."),
        "CPER": ("red", "Bakır vadeli fonu: 20,8 mn $, ~20 bp (maliyet/oynaklık 0,11), USCF emtia havuzu (PTP/K-1 olasılığı yüksek). Bakıra maruziyet için COPX daha likit; ay sonu/IBS kuralları CPER'de çalışmıyor."),
        "DBB": ("red", "5,9 mn $ hacim, ~27 bp maliyet (maliyet/oynaklık 0,22), Invesco DB emtia havuzu (PTP/K-1). KWEB öncülüğü FDR'yi geçiyor ama 1 sd'de ~10 bp (< 27 bp maliyet)."),
        "GDX": ("kabul", "Altın madencilerinin ana aracı: 1,9 mlr $, ~13 bp, oynaklık 322 bp (maliyet/oynaklık 0,04). S1 (ay sonu) adayı; IBS kuralı GDX'te de pozitif (IS zayıf)."),
        "GDXJ": ("kabul", "563 mn $, ~14 bp, oynaklık 356 bp. Ailenin en güçlü adayı S3 (IBS dip alımı) bu ETF'de."),
        "RING": ("red", "GDX kopyası (0,979/1y 0,995), 30 mn $, ~20 bp: GDX daha likit ve ucuz."),
        "NUGT": ("yedek", "2x GDX (1940 Kanunu, PTP değil; Midas'ta bulunurluğu doğrulanmadı). 2020-Q2'ye kadar 3x idi. S1'in kaldıraçlı uygulaması; 2x dönemde 3 günlük oynaklık kaybı ~-5 bp (küçük), ama maxDD ve tek işlem kaybı ~2 kat."),
        "DUST": ("red", "-2x GDX; doğrulanmış kısa yön sinyali yok; ters ürün."),
        "JNUG": ("yedek", "2x GDXJ (PTP değil; Midas'ta doğrulanmadı), 48 mn $, ~20 bp. S3'ün kaldıraçlı uygulaması; maxDD -%51, en kötü işlem -%21."),
        "JDST": ("red", "-2x GDXJ; kısa yön sinyali yok; 23 mn $."),
        "SIL": ("yedek", "Gümüş madencileri: 135 mn $, ~16 bp; GDX ile 1y korelasyon 0,97 (bağımsız değil). S3 kuralı SIL'de de geçiyor (t 2,22)."),
        "SILJ": ("yedek", "Genç gümüş madencileri: 139 mn $, ~16 bp; S5 (düşük güven) bu ETF'de; GDX ile 0,96 korelasyon."),
        "COPX": ("kabul", "Bakır madencileri: 239 mn $, ~14 bp, oynaklık 302 bp; CPER'in likit/PTP'siz alternatifi. Strateji yok; COMEX:HG1! ve Çin göstergeleriyle izlenir."),
        "XME": ("yedek", "Metal-madencilik hisseleri: 226 mn $, ~14 bp. Ay sonu kuralı XME'de de eşikte (t 2,33) -> S1 ailesinin kanıtı; tek başına strateji değil."),
        "URA": ("yedek", "Uranyum: 171 mn $, ~16 bp, oynaklık 320 bp. Strateji yok; risk iştahı (ES/NQ) ve EEM ile eşzamanlı hareket; SPY ile ters gecikmeli ilişki zayıf (FDR yok)."),
        "URNM": ("red", "URA'nın yakın kopyası (0,947), 34 mn $, ~20 bp, geçmiş 2019-12'den."),
        "LIT": ("red", "17,9 mn $, ~20 bp (maliyet/oynaklık 0,105), strateji/öncü yok."),
        "REMX": ("red", "68 mn $, ~16 bp; strateji yok, belirgin sürücü yok (GDX 0,69, EEM 0,64); haber/politika (Çin ihracat kısıtları) güdümlü."),
    }
    izleme = []
    for s in mm.FAM:
        r = isl.loc[s]
        izleme.append({"sym": s, "tv": TV.get(s, ""), "karar": K[s][0], "gerekce": K[s][1],
                       "likidite_mn_usd": round(float(r.med_dollar_vol_m), 1), "maliyet_bp": round(float(r.cost_rt_bp), 1),
                       "vol_1d_bp": round(float(r.vol_1d_bp), 1)})
    order = {"kabul": 0, "yedek": 1, "red": 2}
    izleme.sort(key=lambda x: (order[x["karar"]], -x["likidite_mn_usd"]))

    # ---------------- stratejiler
    def fstat(i):
        r = ad.loc[i]
        ms = {m: ast.literal_eval(str(r[m]).replace("np.float64(", "(")) for m in ("C0", "O1", "C1")}
        return r, ms
    def P(i):  # fdr satırı
        a = {"metal_madenci_S1": ("genel_CA_ay_sonu_sabit", "GDX", "C0", 3), "metal_madenci_S2": ("genel_CA_ay_sonu_sabit", "GLD", "C0", 3),
             "metal_madenci_S3": ("genel_MR_ibs_lt01_dusus_sabit", "GDXJ", "C0", 3), "metal_madenci_S4": ("genel_MR_ibs_lt01_dusus_sabit", "GLD", "C0", 3),
             "metal_madenci_S5": ("genel_MR_bb20_alt_sabit", "SILJ", "C1", 3)}[i]
        x = fdr[(fdr.test == a[0]) & (fdr.sym == a[1]) & (fdr["mode"] == a[2]) & (fdr.h == a[3])].iloc[0]
        return (f"BH q=0,10, toplam {NT} test: tek yönlü (net>0) {'GEÇER' if x.fdr1 else 'GEÇMEZ'} (p1={x.p1:.4f}; eşik ~6,7e-5); "
                f"iki yönlü (lib.bh_fdr) {'GEÇER' if x.fdr2 else 'GEÇMEZ'} (p2={x.p2:.4f}; eşik ~0,0045).")
    def mstr(ms):
        return "; ".join(f"{m}: n={int(v[0])}, brüt {v[1]:.1f} bp, net {v[2]:.1f} bp, t {v[3]:.2f}" for m, v in ms.items())
    def cstr(r):
        return f"1.000$: net {r.net_1000_bp:.1f} bp | 2.500$: net {r.mean_net_bp:.1f} bp | 10.000$: net {r.net_10000_bp:.1f} bp (2.500$ maliyeti {r.cost_bp:.1f} bp)"
    BET = "python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_metal_madenci/t5_adaylar.py"
    TXT = {
        "metal_madenci_S1": dict(
            ad="Ay sonu (turn-of-month) - altın madencileri (GDX)",
            kural="Takvim kuralı, gösterge yok: NYSE'de ayın SON işlem günü AMEX:GDX kapanışta alınır, yeni ayın 3. işlem gününün kapanışında satılır (3 işlem günü). Sinyal ve işlem aynı ETF (AMEX:GDX); kaldıraçlı alternatif AMEX:NUGT (aynı tarihler). Filtre/stop yok. Tatiller NYSE takvimine göre (sonraki sinyaller: 30.11.2026 Pzt -> çıkış 03.12.2026; 31.12.2026 Per -> çıkış 06.01.2027; 29.01.2027 Cum -> çıkış 03.02.2027).",
            giris="C0: ayın son işlem günü kapanıştan hemen önce; kış saatinde (1 Kas 2026 - 14 Mar 2027) TR ~23:45-23:59, yaz saatinde TR ~22:45-22:59. Midas'ta MOC/LOC yok: son dakikalarda piyasa emri ya da son fiyatın 1-2 sent üstüne limit emir. Kaçırılırsa O1 (yeni ayın ilk açılışı TR 17:30 kış/16:30 yaz) zayıf da olsa pozitif (net 44,5 bp, t 1,23).",
            tutus="3 işlem günü (girişten sonraki 3. kapanış).",
            cikis="Yeni ayın 3. işlem günü kapanışından hemen önce (TR ~23:45-23:59 kış / 22:45-22:59 yaz) sat; erken çıkış ve stop yok.",
            sinyal_etf="Takvim (NYSE); işlem AMEX:GDX",
            islem_etf=["GDX", "NUGT (kaldıraçlı, Midas'ta doğrulanmadı)"],
            aile_ici="Aynı kural (C0, h=3) kendi verisiyle: GDXJ 82 bp/t1,98; RING 89/t2,25; XME 91/t2,33; COPX 74/t1,89; URA 93/t1,96; GLD 40/t2,45; SLV 47/t1,38; SIL 50/t1,19; SILJ 57/t1,25; REMX 47/t1,07; LIT 20/t0,56; PPLT 24/t0,76; PALL -20/t-0,57; CPER 1/t0,05; DBB -21/t-1,01. Madenci havuzu (5 ETF, tek küme) t 1,83; 12 küme temsilcisi havuzu t 1,67 (eşik 2,5'in altında); 7 madencilik hissesi havuzu t 1,97. SPY'de aynı kural net 21 bp/t 1,11.",
            notlar="Eşik ölçütlerini tek ETF düzeyinde geçer (net>0, t≥2, IS ve OOS>0, yılların %90'ı pozitif, n=111, O1/C1 brüt>0) ama FDR'yi geçmez ve aile havuzu t<2,5. Etkinin yaklaşık yarısı ay başının ilk gecesinde (C0 h1 brüt 66 bp vs O1 h1 26 bp) -> 'büyük ölçüde kapanışa bağımlı'. Getiri boğa yıllarında yoğun (2020: 273 bp, 2025: 247, 2026: 189/işlem); yıl ortalaması çıkarılmış kenar 72,5 bp (t 1,92); en iyi yıl hariç t 1,58; 2020/2025/2026 hariç net 16 bp (t 0,42). 2023'te -74 bp. 30.01.2026 şoku hariç net 81 bp. Hisse piyasalarında bilinen ay dönümü etkisiyle (Lakonishok-Smidt 1988, McConnell-Xu 2008) uyumlu ama bu örneklemde SPY'de zayıf. NUGT ile: net 188 bp, t 2,19, maxDD -%37, en kötü işlem -%17,6.",
            guven="dusuk"),
        "metal_madenci_S2": dict(
            ad="Ay sonu (turn-of-month) - altın (GLD)",
            kural="S1 ile aynı takvim kuralı, işlem AMEX:GLD: ayın SON NYSE işlem günü kapanışında al, yeni ayın 3. işlem günü kapanışında sat. Gösterge yok. S1 ile AYNI etkidir (GLD-GDX 1y korelasyon 0,86); ikisini birlikte açmak aynı bahsi ikiye katlar.",
            giris="C0: ayın son işlem günü TR ~23:45-23:59 (kış) / ~22:45-22:59 (yaz); MOC yok, piyasa ya da limit emir. O1 alternatifi: net 18,7 bp, t 1,19.",
            tutus="3 işlem günü.",
            cikis="Yeni ayın 3. işlem günü kapanışında (TR ~23:45-23:59 kış) sat.",
            sinyal_etf="Takvim (NYSE); işlem AMEX:GLD",
            islem_etf=["GLD", "IAU/GLDM (kopya)"],
            aile_ici="Kopyalar aynı sonucu veriyor (takvim kuralı OHLC'den bağımsız): IAU 40 bp/t2,45, GLDM 49/t2,58, UGL (2x, PTP) 79/t2,38. Gümüş SLV 47/t1,38, SIVR 46/t1,33; PPLT 24/t0,76; PALL -20; CPER 1; DBB -21 -> etki değerli metallerde (altın>gümüş), baz metallerde yok. Metal havuzu (GLD,SLV,PPLT,PALL,CPER) C0 h3 t 0,80.",
            notlar="Tek ETF eşiğini geçer (t 2,45; IS 33,8/t1,65; OOS 45,4/t1,81; yılların %70'i pozitif; O1/C1 brüt 31,7/36,7 bp) ama FDR'yi geçmez. Yıl ortalaması çıkarılmış kenar 36,4 bp (t 2,28, yılların %90'ı pozitif); en iyi yıl (2025) hariç t 1,65. Etkinin bir kısmı ilk gece (C0 h1 31 bp vs O1 h1 9,5 bp). Düşük oynaklıklı (maxDD -%8) ve PTP'siz olduğundan S1'den daha sakin bir uygulama.",
            guven="dusuk"),
        "metal_madenci_S3": dict(
            ad="Genç altın madencileri IBS dip alımı (GDXJ)",
            kural="AMEX:GDXJ günlük (1D) mum. IBS = (close - low) / (high - low). Sinyal: high > low VE IBS < 0.10 VE close < close[1]. Pine: ibs=(close-low)/(high-low); sinyal = high>low and ibs<0.10 and close<close[1]. Sinyal ve işlem AMEX:GDXJ; kaldıraçlı alternatif AMEX:JNUG (sinyal yine GDXJ mumundan). Pozisyon açıkken gelen yeni sinyaller yok sayılır.",
            giris="C0: sinyal günü kapanıştan önce TR ~23:45-23:55 (kış) / ~22:45-22:55 (yaz) anlık fiyatla IBS'yi hesapla (fiyat günün dibine çok yakın ve dünkü kapanışın altında) -> piyasa/limit emir. Kapanışta kaçırılırsa ertesi gün açılışta al (O1, TR 17:30 kış / 16:30 yaz): O1 sürümü de güçlü (net 72 bp, t 2,74).",
            tutus="3 işlem günü.",
            cikis="Girişten sonraki 3. işlem günü kapanışında (TR ~23:45-23:59 kış) sat; stop/erken çıkış yok.",
            sinyal_etf="AMEX:GDXJ (kendi mumu)",
            islem_etf=["GDXJ", "JNUG (kaldıraçlı, Midas'ta doğrulanmadı)"],
            aile_ici="Aynı kural (C0, h=3): GDX 63 bp/t2,14 (IS -2,6 bp!), RING 66/t2,03 (IS -11), SIL 68/t2,22 (IS 35), SILJ 47/t1,28 (IS -50), XME 52/t1,93, GLD 39/t2,07, COPX 31/t0,83; SLV -6, PPLT -6, PALL 0, URA -19, REMX -37. Madenci havuzu (GDX,GDXJ,RING,SIL,SILJ; tek küme) net 54 bp, t 2,49 (IS 14 bp/t0,51; OOS 113 bp/t3,45); 12 küme havuzu t 0,61. Etki altın kompleksine (altın+madenciler) özgü.",
            notlar="Ailenin en güçlü sonucu: n=240, net 107 bp, t 3,39, IS 85 (t1,82) / OOS 128 (t2,99), yılların %80'i pozitif; O1'de de güçlü (t 2,74), komşu h: h1 t2,81, h2 t2,48; yıl ortalaması çıkarılmış kenar 98 bp (t 3,14); en iyi yıl (2020) hariç t 2,76; 30.01.2026 şoku hariç 102 bp (t 3,23). C1'de zayıf (31 bp, t 0,93): sinyalden sonra bir gün beklemek kenarın çoğunu kaçırır. FDR: iki yönlü BH'de geçer, tek yönlü BH'de geçmez. Uyarılar: genel taramada (31 sinyal x 9 kombinasyon x 28 ETF) en iyiler arasından geldiği için seçim yanlılığı var; geniş madenci havuzunda IS dönemi zayıf; boğa piyasasında (2024-2026) dip alımı. JNUG ile: net 173 bp, t 2,70, maxDD -%51, en kötü işlem -%21.",
            guven="orta"),
        "metal_madenci_S4": dict(
            ad="Altın IBS dip alımı (GLD)",
            kural="S3 kuralı AMEX:GLD mumunda: IBS=(close-low)/(high-low) < 0.10 VE close < close[1] (1D). İşlem AMEX:GLD, 3 işlem günü tutuş.",
            giris="C0: sinyal günü TR ~23:45-23:55 (kış) / ~22:45-22:55 (yaz) anlık fiyatla kontrol -> al. O1 (TR 17:30 kış) alternatifi: net 23 bp, t 1,43.",
            tutus="3 işlem günü.",
            cikis="Girişten sonraki 3. kapanışta sat (TR ~23:45-23:59 kış).",
            sinyal_etf="AMEX:GLD (kendi mumu)",
            islem_etf=["GLD"],
            aile_ici="Kopyalarda ZAYIF: IAU 19 bp/t0,98, GLDM 37/t1,60 (aynı varlık; IBS gün içi yüksek/düşük ayrıntısına duyarlı -> kırılgan). UGL 47/t1,20. Madencilerde S3 bkz.",
            notlar="Eşik ölçütlerini geçer (n=140, net 39 bp, t 2,07, IS 54,6/t1,90, OOS 27,4/t1,08, yılların %70'i pozitif, O1 brüt 36 bp) ama FDR'yi geçmez; komşu h2 daha güçlü (t 2,69) ama h1 t 1,66. 2026'da -24 bp, 2023'te -4. Kopya ETF'lerdeki zayıflık nedeniyle bağımsız bir strateji olarak değil, S3'ün altın tarafındaki teyidi olarak okunmalı.",
            guven="dusuk"),
        "metal_madenci_S5": dict(
            ad="Genç gümüş madencileri Bollinger alt bant, 1 gün bekle (SILJ)",
            kural="AMEX:SILJ 1D: close < ta.sma(close,20) - 2*ta.stdev(close,20,false) (backtest örneklem std'si kullandı; Pine'da ta.stdev varsayılanı popülasyon std'sidir -> biased=false verin; standart Bollinger Bands göstergesiyle eşdeğeri 20 / StdDev 2.05). Sinyal gününde ALINMAZ; ertesi işlem günü kapanışında alınır (C1). İşlem AMEX:SILJ.",
            giris="C1: sinyal gününden sonraki işlem günü kapanıştan hemen önce TR ~23:45-23:59 (kış) / ~22:45-22:59 (yaz).",
            tutus="3 işlem günü (C1 girişinden sonra).",
            cikis="Girişten sonraki 3. kapanışta sat.",
            sinyal_etf="AMEX:SILJ (kendi mumu)",
            islem_etf=["SILJ"],
            aile_ici="Aynı kural (C1, h=3): GDXJ 213 bp/t2,15, GDX 136/t1,63, SIL 77/t1,48, RING 91/t1,30, SLV 75/t1,15, URA 44, REMX 36, XME 9, GLD 16; COPX -45, LIT -52. 12 küme havuzu t 0,93.",
            notlar="Eşik ölçütlerini geçer (n=48, net 193 bp, t 3,10, IS 189/OOS 195, yılların %90'ı pozitif) ve iki yönlü BH'de geçer, ama: 8.316 aile satırının en iyileri arasından seçildi (seçim yanlılığı yüksek), komşu h zayıf (h1 t 0,87; h2 t 1,83), C0'da zayıf (t 1,03), yılda 2-8 işlem (çok seyrek, sonuç birkaç büyük işleme bağlı: 2020 762 bp, 2025 845 bp/işlem). Bilgi amaçlı; S3 ile aynı 'madencide aşırı satım' temasının seyrek ve gürültülü bir türevi.",
            guven="dusuk"),
    }
    strat = []
    for i in ["metal_madenci_S3", "metal_madenci_S1", "metal_madenci_S2", "metal_madenci_S4", "metal_madenci_S5"]:
        r, ms = fstat(i); T = TXT[i]
        strat.append({"id": i, "ad": T["ad"], "kural": T["kural"], "giris": T["giris"], "tutus": T["tutus"], "cikis": T["cikis"],
                      "sinyal_etf": T["sinyal_etf"], "islem_etf": T["islem_etf"],
                      "n": int(r.n), "brut_bp": round(float(r.mean_gross_bp), 1), "net_bp": round(float(r.mean_net_bp), 1),
                      "kazanma": round(float(r.win), 3), "pf": round(float(r.pf), 2), "t": round(float(r.t), 2),
                      "is_net_bp": round(float(r.is_net_bp), 1), "oos_net_bp": round(float(r.oos_net_bp), 1),
                      "yil_pozitif": round(float(r.years_pos_frac), 2), "maxdd": round(float(r.maxdd), 3), "en_kotu_bp": round(float(r.worst_bp), 1),
                      "maliyet_duyarlilik": cstr(r), "mod_saglamlik": mstr(ms), "aile_ici": T["aile_ici"], "test_sayisi": NT, "fdr": P(i),
                      "guven": T["guven"], "betik": BET, "notlar": T["notlar"] + f" (IS t={r.is_t:.2f}, OOS t={r.oos_t:.2f})"})

    # ---------------- elenenler
    elenen = [
        {"ad": "Genel kütüphane, aile havuzu (31 sinyal x C0/O1/C1 x h1-3 [+erken çıkış] = 297 kombinasyon, 12 küme temsilcisi, aynı gün olaylar ortalanarak)",
         "neden": "Pozitif net ve BH-FDR'de anlamlı tek kombinasyon yok; en iyisi CA_ay_sonu C0 h2/h3 (t 1,69/1,67; OOS t ~0,55). Anlamlı çıkanların hepsi negatif (maliyet)."},
        {"ad": "Tatil öncesi (CA_tatil_oncesi)", "neden": "Aile havuzu C0 h1 net -7,9 bp (t -0,48); madenci havuzu C0 h1 net 4 bp (t 0,15); O1/C1 negatif. Genel taramadaki tek ETF pozitiflikleri tesadüf."},
        {"ad": "VIX backwardation dönüşü (VX_backw_donus) ve VX_backwardation", "neden": "VX_backw_donus: madenci havuzu C0 h2 net 85 bp ama t 1,65, n=55; h3'te negatif; 12 küme havuzunda t ≤ 0,76. VX_backwardation: en iyi 12 küme havuzu C1 h2 t 1,12. Eşik altı, h'ye duyarlı."},
        {"ad": "MM02: madencilerin GLD'ye gecikmeli tepkisi (artık <= -1,5 sd -> GDX/GDXJ/RING long; SIL/SILJ<-SLV; COPX<-CPER)",
         "neden": "GDX t ≤ 1,16, madenci havuzu t ≤ 0,94, COPX negatif. Regresyonda GDX<-GLD yetişme katsayısı kendi gecikmesi kontrol edilince t 0,11 (IS 0,53 / OOS -0,93). Kısa vadeli 'yetişme' yok."},
        {"ad": "MM03: reel faiz düşüşü + dolar düşüşü -> GLD (DFII10 t-1..t-4 ≤ -10 bp ve UUP 3g ≤ -%0,5)", "neden": "GLD/SLV/GDX havuzu C0 h3 net -27 bp; tüm modlarda negatif. 2022'de kopan ilişkiyle uyumlu."},
        {"ad": "DFII10 günlük değişimi (±5 bp, O1/C1) ve UUP günlük düşüşü (z<-1,5) -> metaller", "neden": "Hepsi negatif ya da anlamsız (en iyi t 0,41); UUP düşüşü sonrası GLD negatif (t -1,8)."},
        {"ad": "MM04: FOMC günü kapanışında altın al, 3 gün tut; FOMC öncesi (D-3->D, D-1->D)", "neden": "FOMC sonrası İŞARET TERS: GLD/SLV/GDX havuzu C0 h3 net -69 bp (t -1,6), 30.01.2026 hariç -44 bp; öncesi anlamsız (t 0,03/0,33). Kısa yön için de anlamlı değil."},
        {"ad": "MM05: GLD RSI(2)<10 & SMA200 üstü, SMA5 çıkışı", "neden": "GLD C0 net -4,9 bp (IS -31), SLV -66, GDX -37."},
        {"ad": "Altın/gümüş oranı (GLD/SLV log oranı 20g z ±2) dönüşü", "neden": "z>2 -> SLV: t ≤ 0,02; z<-2 -> GLD: t ≤ 0,76 (bazı modlarda t -3,7)."},
        {"ad": "GVZ sıçrama (>%15) ve GVZ gerilme (>1,1x SMA10) -> GLD/SLV/GDX", "neden": "Havuz t ≤ 1,07; işaret moda göre değişiyor."},
        {"ad": "MM01: 'kapanışta al, açılışta sat' gece primi", "neden": "Gece getirisi gerçek ve güçlü (GLD +5,1 bp/gün t 3,20; madencilerde +6..+18 bp; gün içi ≈0 ya da negatif) ama tek gecelik işlem maliyeti karşılamıyor (GLD net -7,9 bp). Sonuç uygulamaya yön veriyor: girişi kapanışta (C0) yapmak, açılışta değil. Resmî açılış fiyatı ölçüm sorunu (Quantpedia) geçerli."},
        {"ad": "Başabaş enflasyon (FRED:T10YIE) artışı ≥ +5 bp -> SLV/GLD/GDX/SIL (sweep'te IS/OOS aynı işaretli, FDR'siz bulgu)", "neden": "Hazine verisi kapanıştan sonra yayımlandığı için gerçekçi modlar O1/C1: hepsi negatif ya da anlamsız (OOS negatif). Etki yalnız erişilemeyen C0 gecesinde."},
        {"ad": "Çin -> baz metal (KWEB/FXI 1g z>1 -> DBB/CPER/COPX)", "neden": "DBB<-KWEB gecikmesi FDR'yi geçiyor (t 4,05; IS 2,45 / OOS 3,20) ama 1 sd başına ~10 bp < 27 bp maliyet; kural DBB'de tüm modlarda net negatif (t -0,6 ile -6,1 arası)."},
        {"ad": "SPY büyük düşüşü (z<-1,5) -> URA/URNM long (negatif gecikme katsayısı)", "neden": "t ≤ 1,50; FDR yok."},
        {"ad": "GLD<-GDX gecikmesi (GDX artığı ≥ +1,5 sd -> GLD long)", "neden": "Regresyonda t 2,40 (h1) ama FDR yok; kural C0 h3 net 22 bp (t 1,29), O1 h1 negatif."},
        {"ad": "GDX 1g z ≥ +1,5 -> PPLT / COPX long", "neden": "Uzun yön zayıf (PPLT C0 h1 t 0,43; COPX C0 h1 t 1,35, O1 negatif). Simetrik taraf (GDX z ≤ -1,5) sonrası PPLT/COPX ertesi gün zayıf (PPLT O1 h1 net -40 bp, t -3,55): yalnız 'o gün alma' filtresi, FDR'siz."},
        {"ad": "MM06: kaldıraçlı madenci/metal ürünlerinde 1-3 günlük oynaklık kaybı", "neden": "Strateji değil, ölçüm: 2x dönemde 3 günlük ortalama sapma NUGT -5 bp, JNUG -6, AGQ -7, UGL -6 bp (formül öngörüsü -3..-22 bp; gerçekleşen kayıp öngörüden küçük). 1-3 günde kayıp küçük; asıl risk tek işlem kaybının ~2 katına çıkması. Ters ürünler (DUST, JDST, GLL, ZSL) için kısa yön sinyali bulunamadı."},
        {"ad": "Ay sonu kuralı baz metal/paladyumda (CPER, DBB, PALL)", "neden": "CPER 1 bp, DBB -21 bp, PALL -20 bp (C0 h3): etki değerli metal ve madenci hisseleriyle sınırlı."},
    ]

    # ---------------- lead-lag
    def ll(sym, suruculer, onculer, gz, notu, takvim):
        return {"sym": sym, "suruculer": suruculer, "onculer": [o for o in onculer if o], "gercek_zamanli": gz, "not": notu, "takvim_riskleri": takvim}
    GZ_GOLD = [{"ad": "COMEX altın vadeli (sürekli)", "tv": "COMEX:GC1!", "neden": "~23 saat işler (TR kış 02:00-01:00); ETF kapalıyken oluşan hareket açılış boşluğunu gösterir. İzleme aracı, öncü değil."},
               {"ad": "Spot altın", "tv": "OANDA:XAUUSD", "neden": "Asya/Londra seansı; TR 12:00-17:30 arasında GLD açılışını önceden gösterir."},
               {"ad": "Dolar endeksi", "tv": "TVC:DXY", "neden": "Altınla eşzamanlı ters hareket (UUP corr_1y -0,42); gece/sabah değişimi açılış yönü için."},
               {"ad": "ABD 10y getiri / T-Note vadeli", "tv": "CBOT:ZN1!", "neden": "Faiz şokları (CPI/NFP 08:30 ET = TR 16:30 kış) açılıştan önce altına yansır. Alternatif: TVC:US10Y."}]
    GZ_SILVER = [{"ad": "COMEX gümüş vadeli", "tv": "COMEX:SI1!", "neden": "~23 saat işler; SLV/SIL açılış boşluğunu önceden gösterir."},
                 {"ad": "Spot gümüş", "tv": "OANDA:XAGUSD", "neden": "Asya/Londra seansı gümüş fiyatı."},
                 {"ad": "COMEX altın vadeli", "tv": "COMEX:GC1!", "neden": "Gümüşün ana eşzamanlı sürücüsü (SLV-GLD 0,84)."}]
    GZ_MINER = [{"ad": "COMEX altın vadeli", "tv": "COMEX:GC1!", "neden": "Madencilerin ana sürücüsü (GDX-GLD 0,86, beta 1,53); gece hareketi madenci açılışına ~1,5x yansır."},
                {"ad": "COMEX gümüş vadeli", "tv": "COMEX:SI1!", "neden": "İkincil sürücü (GDX-SLV 0,81)."},
                {"ad": "S&P 500 e-mini", "tv": "CME_MINI:ES1!", "neden": "Madenciler hisse olduğu için genel risk iştahı; açılış öncesi yön."}]
    GZ_COPPER = [{"ad": "COMEX bakır vadeli", "tv": "COMEX:HG1!", "neden": "~23 saat işler; COPX açılış boşluğunu önceden gösterir (COPX-CPER 0,82, beta 1,39)."},
                 {"ad": "Hang Seng vadeli", "tv": "HKEX:HSI1!", "neden": "Çin risk iştahı; TR sabahı Asya seansı."},
                 {"ad": "USD/CNH", "tv": "FX_IDC:USDCNH", "neden": "Çin para birimi; bakır talebi beklentisi."},
                 {"ad": "S&P 500 e-mini", "tv": "CME_MINI:ES1!", "neden": "Genel risk iştahı (madencilik hissesi)."}]
    TK_GOLD = "FOMC 09.12.2026 14:00 ET (TR 22:00; örneklemde FOMC sonrası altın zayıf, anlamsız); CPI 10.11 ve 10.12.2026, NFP 04.12.2026 08:30 ET (TR 16:30, açılıştan 1 saat önce); COMEX teminat değişiklikleri (30.01.2026 gümüş şoku); Çin tatilleri Asya seansını inceltir; ay sonu 30.11.2026 (S1/S2)."
    TK_MINER = TK_GOLD + " Ek: madenci bilanço dönemleri (Şub, Nis-May, Tem-Ağu, Eki-Kas)."
    TK_COPPER = "Çin PMI/ticaret verileri (TR 04:30-05:00), ABD tarife kararları (30.07.2025 CPER -%19), FOMC/CPI genel risk."
    LL = []
    LL.append(ll("GLD", drv("GLD", ["GDX", "SLV", "UUP", "DFII10_d", "FXE"]),
                 [lead("GLD", "GDX", "lag", 1, "GDX'in GLD'ye göre artığı ≥+1,5 sd kuralı: C0 h3 net 22 bp (t 1,29), O1 h1 negatif.", "doğrulanmadı (FDR yok; kural maliyet sonrası anlamsız)"),
                  lead("GLD", "T10YIE_d", "lag", 1, "Veri kapanıştan sonra yayımlanır; O1/C1 kuralı negatif.", "maliyet altında (7 bp/sd < 13 bp)"),
                  lead("GLD", "DFII10_d", "lag", 1, "IS ve OOS işaretleri ters (2022 kırılması).", "kullanılamaz"),
                  lead("GLD", "UUP", "lag", 1, "Eşzamanlı ters ilişki güçlü, gecikmeli yok.", "yok")],
                 GZ_GOLD, "Doğrulanmış gecikmeli öncü yok. Altın günlük frekansta ABD kapanışından sonra gelen bilgiye (Asya/Londra seansı) tepki verir: bu 'öncü' değil, gerçek zamanlı izlenecek açılış boşluğudur. Getirinin tamamına yakını gece oluşuyor (gece +5,1 bp/gün t 3,20; gün içi -0,6 bp).", TK_GOLD))
    LL.append(ll("IAU", drv("IAU", ["GLD", "SLV", "GDX"]),
                 [lead("IAU", "GLD", "catch", 1, "SAHTE: 2021-03-08 hatalı bar (IAU +%8,5, GLD -%1, ertesi gün geri dönüş). Bar atılınca t -0,43.", "veri hatası")],
                 GZ_GOLD[:2], "GLD kopyası; doğrulanmış gecikmeli öncü yok.", TK_GOLD))
    LL.append(ll("GLDM", drv("GLDM", ["GLD", "SLV", "GDX"]), [], GZ_GOLD[:2], "GLD kopyası; doğrulanmış gecikmeli öncü yok.", TK_GOLD))
    LL.append(ll("SLV", drv("SLV", ["GLD", "GDX", "CPER", "UUP"]),
                 [lead("SLV", "T10YIE_d", "lag", 1, "Kural (≥+5 bp -> SLV): O1 h1 net -7 bp, OOS negatif; etki yalnız C0 gecesinde (veri o an bilinmez).", "kullanılamaz"),
                  lead("SLV", "GDX", "lag", 1, "", "anlamsız"), lead("SLV", "GLD", "catch", 1, "", "anlamsız")],
                 GZ_SILVER, "Doğrulanmış gecikmeli öncü yok. 30.01.2026 (-%28,5) gibi teminat/likidasyon şokları gece oluşur; gerçek zamanlı COMEX:SI1! izlenmeli.", TK_GOLD))
    LL.append(ll("SIVR", drv("SIVR", ["SLV", "GLD"]), [], GZ_SILVER[:2], "SLV kopyası; doğrulanmış gecikmeli öncü yok.", TK_GOLD))
    LL.append(ll("GDX", drv("GDX", ["GLD", "SLV", "UUP", "DFII10_d", "EEM"]),
                 [lead("GDX", "GLD", "catch", 1, f"Kendi gecikmesi kontrollü yetişme t {er('GDX','GLD',1).catch_kendi_kontrollu_t:.2f}; artık kuralı (MM02) t ≤ 1,16.", "yok (madenciler altına gecikmeli yetişmiyor)"),
                  lead("GDX", "GLD", "catch", 3, "", "yok"),
                  lead("GDX", "LQD", "lag", 1, "IS 3,25 / OOS -0,01: işaret OOS'ta kayboldu.", "kullanılamaz"),
                  lead("GDX", "DFII10_d", "lag", 1, "", "anlamsız")],
                 GZ_MINER, "Doğrulanmış gecikmeli öncü yok. GDX, GLD ile aynı gün ~1,5 beta ile hareket eder; 'altın yükseldi, madenci geride kaldı, yarın yetişir' fikri veride desteklenmiyor.", TK_MINER))
    LL.append(ll("GDXJ", drv("GDXJ", ["GDX", "GLD", "SLV"]),
                 [lead("GDXJ", "GLD", "catch", 1, f"Kendi gecikmesi kontrollü t {er('GDXJ','GLD',1).catch_kendi_kontrollu_t:.2f}.", "yok"),
                  lead("GDXJ", "LQD", "lag", 1, "IS 3,42 / OOS ~0.", "kullanılamaz")],
                 GZ_MINER, "Doğrulanmış gecikmeli öncü yok; S3 (IBS) kendi fiyatına dayalı bir ortalamaya dönüş kuralıdır, öncü değildir.", TK_MINER))
    LL.append(ll("NUGT", drv("NUGT", ["GDX", "GLD", "SLV"]),
                 [lead("NUGT", "GLD", "catch", 1, "", "yok")], GZ_MINER, "2x GDX; sinyaller GDX'ten alınır. Doğrulanmış gecikmeli öncü yok.", TK_MINER))
    LL.append(ll("JNUG", drv("JNUG", ["GDX", "GLD", "SLV"]),
                 [lead("JNUG", "GLD", "catch", 1, "", "yok")], GZ_MINER, "2x GDXJ; sinyaller GDXJ'den alınır. Doğrulanmış gecikmeli öncü yok.", TK_MINER))
    LL.append(ll("SIL", drv("SIL", ["GDX", "GLD", "SLV"]),
                 [lead("SIL", "SLV", "catch", 1, f"Kendi gecikmesi kontrollü t {er('SIL','SLV',1).catch_kendi_kontrollu_t:.2f}; artık kuralı t ≤ 1,04.", "yok")],
                 GZ_MINER[:1] + GZ_SILVER[:1] + GZ_MINER[2:], "Doğrulanmış gecikmeli öncü yok (SIL<-SLV yetişmesi yok).", TK_MINER))
    LL.append(ll("SILJ", drv("SILJ", ["GDX", "GLD", "SLV"]),
                 [lead("SILJ", "SLV", "catch", 1, f"Kendi gecikmesi kontrollü t {er('SILJ','SLV',1).catch_kendi_kontrollu_t:.2f}.", "yok")],
                 GZ_MINER[:1] + GZ_SILVER[:1] + GZ_MINER[2:], "Doğrulanmış gecikmeli öncü yok.", TK_MINER))
    LL.append(ll("COPX", drv("COPX", ["CPER", "GDX", "EEM", "FXI"]),
                 [lead("COPX", "CPER", "lag", 1, "IS 2,19 / OOS -2,08: işaret değişti.", "kullanılamaz"),
                  lead("COPX", "GDX", "lag", 3, "Kural GDX z≥+1,5 -> COPX: C0 h3 net 40 bp (t 1,27), O1 negatif; GDX z≤-1,5 sonrası COPX zayıf (C0 h1 net -48 bp, t -1,95).", "doğrulanmadı (FDR yok)")],
                 GZ_COPPER, "Doğrulanmış gecikmeli öncü yok. Bakır vadeli (HG1!) ve Asya seansı açılış boşluğunu gösterir.", TK_COPPER))
    LL.append(ll("XME", drv("XME", ["GDX", "IWM", "CPER", "EEM"]),
                 [lead("XME", "DIA", "lag", 1, "Negatif katsayı (DIA yükselince ertesi gün XME zayıf), FDR yok.", "kullanılamaz"),
                  lead("XME", "CPER", "lag", 1, "", "anlamsız")],
                 [{"ad": "COMEX bakır vadeli", "tv": "COMEX:HG1!", "neden": "Baz metal fiyatı."},
                  {"ad": "Russell 2000 e-mini", "tv": "CME_MINI:RTY1!", "neden": "XME küçük/orta ölçekli döngüsel hisse; IWM ile 0,72."},
                  {"ad": "COMEX altın vadeli", "tv": "COMEX:GC1!", "neden": "Altın madencisi ağırlığı (GDX ile 0,75)."}],
                 "Doğrulanmış gecikmeli öncü yok.", "ABD çelik/alüminyum tarife kararları, Çin PMI, ay sonu (S1 ailesi). FOMC/CPI genel risk."))
    LL.append(ll("URA", drv("URA", ["EEM", "IWM", "SMH", "SPY"]),
                 [lead("URA", "SPY", "lag", 1, "Negatif (SPY yükselince ertesi gün URA zayıf); IS -2,22 / OOS -1,48; kural (SPY z≤-1,5 -> URA long) t ≤ 1,25.", "doğrulanmadı (FDR yok)")],
                 [{"ad": "S&P 500 e-mini", "tv": "CME_MINI:ES1!", "neden": "URA'nın SPY betası ~2,4 (1y); risk iştahı."},
                  {"ad": "Nasdaq 100 e-mini", "tv": "CME_MINI:NQ1!", "neden": "Yapay zekâ/veri merkezi enerji teması (URA-SMH 0,67)."}],
                 "Doğrulanmış gecikmeli öncü yok. Fiziki uranyum (Sprott SPUT) ve Cameco gerçek zamanlı izlenebilir ama TradingView kodları doğrulanmadı (tv_dogrulanacak).",
                 "Kazatomprom/Cameco üretim açıklamaları, SPUT fon alımları, ABD enerji politikası haberleri; genel risk (FOMC/CPI)."))
    LL.append(ll("PPLT", drv("PPLT", ["SLV", "GLD", "GDX", "CPER"]),
                 [lead("PPLT", "GDX", "lag", 1, "Kural: GDX z≥+1,5 -> PPLT C0 h1 net 6,6 bp (t 0,43); GDX z≤-1,5 -> PPLT ertesi gün zayıf (O1 h1 net -40 bp, t -3,55): yalnız 'o gün PPLT alma' filtresi.", "uzun yön kullanılamaz; kaçınma filtresi FDR'siz")],
                 [{"ad": "NYMEX platin vadeli", "tv": "NYMEX:PL1!", "neden": "~23 saat; açılış boşluğu."},
                  {"ad": "COMEX altın vadeli", "tv": "COMEX:GC1!", "neden": "Değerli metal kompleksi (PPLT-GLD 0,76)."}],
                 "Doğrulanmış gecikmeli öncü yok.", "WPIC arz-talep raporları, Rusya/Güney Afrika arz haberleri, otomotiv talebi; FOMC/CPI."))
    order_sym = [x["sym"] for x in izleme if x["karar"] in ("kabul", "yedek")]
    LL = sorted(LL, key=lambda d: order_sym.index(d["sym"]) if d["sym"] in order_sym else 99)
    # tv doğrulama kontrolü
    bad = []
    for d in LL:
        for k in ("suruculer", "onculer", "gercek_zamanli"):
            for e in d[k]:
                c = e["tv"]
                ok = c in VALID or c in TV.values()
                if not ok: bad.append(c)
    out = {
        "family": "metal_madenci",
        "ozet": "",
        "izleme": izleme, "stratejiler": strat, "elenen": elenen, "leadlag": LL,
        "tv_dogrulanacak": sorted(set(bad) | {"TSX:U.UN (Sprott Physical Uranium Trust; URA için gerçek zamanlı izleme önerisi)", "NYSE:CCJ (Cameco; URA için gerçek zamanlı izleme önerisi)"}),
        "dosyalar": [],
    }
    out["ozet"] = (
        f"metal_madenci (28 ETF): {NT} test (genel_tum aile satırları 8.316 + kendi testlerim {NT-8316}). Tek yönlü BH-FDR (q=0,10, net>0) altında HİÇBİR strateji geçmiyor; "
        "aile havuz testlerinde (aynı gün olaylar ortalanarak) hiçbir kural t≥2,5'e ulaşmıyor. Tek ETF eşik ölçütlerini geçen 5 aday var: "
        "S3 GDXJ IBS<0,10 & düşüş, C0, 3 gün (n=240, net 107 bp, t 3,39, IS/OOS pozitif, O1'de de t 2,74; iki yönlü BH'de geçer) -> 'orta'; "
        "S1/S2 ay sonu (son işlem günü kapanışı -> 3. gün kapanışı) GDX (t 2,20) ve GLD (t 2,45) -> 'düşük' (FDR yok, boğa yıllarına bağımlı, kısmen kapanışa bağımlı); "
        "S4 GLD IBS (t 2,07, kopyalarda zayıf) ve S5 SILJ Bollinger C1 (n=48, seçim yanlılığı) -> 'düşük'. Yönlendirmedeki diğer hipotezler (madenci yetişmesi, SIL<-SLV, altın/gümüş oranı, GVZ, reel faiz+dolar, FOMC, tatil öncesi, VIX backwardation) "
        "maliyet sonrası çalışmıyor; FOMC sonrası altın beklenenin tersine zayıf (anlamsız). Lead-lag: ailede ekonomik olarak kullanılabilir doğrulanmış gecikmeli öncü YOK "
        "(tek FDR geçen DBB<-KWEB maliyetin altında); altın/gümüş/bakır vadelileri (COMEX:GC1!, SI1!, HG1!) gece işlediği için gerçek zamanlı izleme aracıdır. "
        "Gece getirisi (kapanış->açılış) güçlü, gün içi ≈0/negatif: girişleri kapanışta yapmak (C0) açılışa göre belirgin avantajlı. İzleme: kabul GLD, GDX, GDXJ, SLV, COPX; "
        "kaldıraçlı ProShares metal ürünleri (UGL/GLL/AGQ/ZSL) ile CPER/DBB PTP/K-1 (%10 brüt stopaj) riski nedeniyle red. 30.01.2026 gümüş şoku sonuçları değiştirmiyor.")
    keep = ["sonuc.json", "aday_ozet.csv", "aday_yillik.csv", "fdr_tum_testler.csv", "hipotez_etf.csv", "hipotez_havuz.csv",
            "genel_aile_havuz.csv", "islenebilirlik.csv", "leadlag_aile.csv", "leadlag_ek_regresyon.csv", "gece_gunici.csv", "kaldirac_sapma.csv"]
    kod = sorted(os.path.join(mm.HERE, f) for f in os.listdir(mm.HERE) if f.endswith(".py"))
    out["dosyalar"] = [os.path.join(R, "notlar", "aile_metal_madenci.md")] + kod + [os.path.join(O, f) for f in keep]
    json.dump(out, open(os.path.join(O, "sonuc.json"), "w"), ensure_ascii=False, indent=1)
    print("yazıldı", os.path.join(O, "sonuc.json"), "| doğrulanmamış tv:", bad)

if __name__ == "__main__":
    main()
