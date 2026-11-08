"""Görev 4-6: izleme listesi, lead-lag özetleri ve sonuc.json. Önce a1..a5 ve strateji_S1/S2 betikleri çalışmış olmalı
(sonuclar/aile_uluslararasi/*.csv). Çalıştır: python3 -I kod/ajan_uluslararasi/a6_sonuc_json.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak, lib

OUT = ortak.OUT
REL = lambda p: os.path.join("/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun", p)
scr = ortak.screen()
LL = pd.read_csv(os.path.join(ortak.ROOT, "sonuclar", "leadlag_sweep.csv"))
TVOK = ortak.tv_ok_leaders()
MACRO_TV = {"VIX_dlog": "CBOE:VIX", "VIXTS_d": "CBOE:VIX3M", "OVX_dlog": "CBOE:OVX", "GVZ_dlog": "CBOE:GVZ", "VVIX_dlog": "CBOE:VVIX",
            "BTC_16ET": "COINBASE:BTCUSD", "ETH_16ET": "COINBASE:ETHUSD", "DGS10_d": "TVC:US10Y", "DGS2_d": "TVC:US02Y",
            "DGS30_d": "TVC:US30Y", "DFII10_d": "FRED:DFII10", "T10YIE_d": "FRED:T10YIE"}
def tvl(name):
    return MACRO_TV.get(name) or ortak.tv(name)

def r2(x, k=1):
    try:
        return None if x is None or not np.isfinite(float(x)) else round(float(x), k)
    except Exception:
        return None

# ---------------- izleme kararları ----------------
KABUL = {
    "EWY": "En likit (medyan 2,36 mlr $/gün) ve en ucuz (13 bp) aile üyesi; maliyet/oynaklık 0,03 (ailenin en düşüğü). S1 sepetinin en güçlü üyesi (C0 h=1 net +108 bp, t 2,41, IS ve OOS > 0) ve S2'nin (keşifsel) işlem aracı. Güçlü negatif 1 günlük otokorelasyon (IS -0,16 / OOS -0,12).",
    "EWT": "Likit (450 mn $), 14 bp maliyet, maliyet/oynaklık 0,06. S1 sepet üyesi (C0 h=1 net +63 bp, t 2,00; IS +79 / OOS +56).",
    "FXI": "Çin büyük şirketleri için en likit araç (872 mn $, 15 bp). S1 sepet üyesi (C0 h=1 net +37 bp, t 1,17; h=2 +108 bp, t 2,19). MCHI aynı hisseleri taşır (kopya; daha az likit).",
    "EWJ": "Japonya için tek likit ve ucuz araç (482 mn $, 14 bp). S1 sepet üyesi ama tek başına zayıf (n=32, net +30 bp, t 1,21, OOS +5 bp). Gerçek zamanlı izleme kolay (OSE Nikkei vadelisi, USDJPY).",
}
YEDEK = {
    "EWA": "S1 sepet üyesi (C0 h=1 net +51 bp) ama OOS negatif (-8 bp); 86 mn $, 16 bp.",
    "EWH": "S1 sepet üyesi (C0 h=1 net +49 bp, n=29; OOS +8 bp); 67 mn $, 16 bp.",
    "EEM": "Ailenin genel EM ölçütü, çok likit (1,6 mlr $, 13,7 bp). Doğrulanmış strateji yok (S1 kuralı EEM'de n=46, net +57 bp, t 1,6). Kopyalar (IEMG, VWO) arasından en likidi.",
    "IEMG": "EEM'in kopyası (MSCI EM IMI); bağımsız kanıt değil. 897 mn $, 14 bp; EEM'e yedek.",
    "EFA": "Gelişmiş ülkeler (EAFE) için en likit araç (1,5 mlr $, 13 bp) ama 1 günlük oynaklık düşük (104 bp; maliyet/oynaklık 0,125). Doğrulanmış strateji yok.",
    "VGK": "Avrupa temsilcisi (234 mn $, 14 bp). Doğrulanmış strateji yok; FDAX/SX5E ile gerçek zamanlı izlenebilir. EZU yakın kopya.",
    "EWZ": "Likit (977 mn $, 15 bp), yüksek oynaklık (222 bp). Doğrulanmış strateji/öncü yok (S1 plasebo grubunda; USO öncülüğü yok).",
    "INDA": "Hindistan için en likit (299 mn $, 14 bp). S1 kuralı INDA'da C0 h=1 net +111 bp (n=33, t 1,82) ama OOS -8 bp; doğrulanmış değil. EPI kopya.",
    "ASHR": "Çin A payları (148 mn $, 16 bp). S1 genişletilmiş kontrolde C0 h=1 net +51 bp (t 1,60), IS ve OOS > 0.",
    "CQQQ": "Çin teknoloji (46 mn $, 20 bp). S1 genişletilmiş kontrolde C0 h=1 net +47 bp (t 1,60), IS ve OOS > 0.",
    "KORU": "EWY'nin 3x kaldıraçlısı (405 mn $, 26 bp). Kendi sinyali yok; EWY sinyaliyle (S1/S2) kaldıraçlı uygulama aracı. Midas'ta bulunurluk doğrulanmadı; 1 günlük oynaklık 1.100 bp, son 1 yılda en kötü gün -%42.",
    "YINN": "FXI'nin 3x kaldıraçlısı (56 mn $, 16 bp). FXI sinyaliyle S1 uygulaması (C0 h=2 net +336 bp, t 2,27; C0 h=1 t 1,25). Midas'ta bulunurluk doğrulanmadı.",
}
RED_OZEL = {
    "VWO": "EEM/IEMG kopyası (FTSE EM); bağımsız kanıt değil. EEM daha likit.",
    "VEA": "EFA kopyası; EFA daha likit.", "IEFA": "EFA kopyası; EFA daha likit.",
    "EZU": "VGK'nın yakın kopyası (Euro Bölgesi); VGK daha likit/ucuz.",
    "MCHI": "FXI ile büyük ölçüde aynı hisseler (kopya); FXI daha likit/ucuz.",
    "DXJ": "EWJ'nin kur korumalı yakın kopyası (50 mn $, 20 bp). Taramada QQQ/SPY'dan ters yönlü gecikme FDR'yi geçti ama eşik kuralına çevrildiğinde (SPY z<=-2 -> DXJ al) kâr yok (C0 h=1 net -1 bp).",
    "EPI": "INDA kopyası; INDA daha likit.",
    "EWW": "Likit (98 mn $) ama strateji/öncü yok; S1 plasebosunda negatif (eşzamanlı piyasa).",
    "EWC": "ABD ile eşzamanlı; düşük oynaklık (95 bp), maliyet/oynaklık 0,17; strateji yok.",
    "ILF": "Latin Amerika 40 (%60 Brezilya) — EWZ ile örtüşür; strateji yok.",
    "YANG": "FXI'nin 3x tersi; uzun-tek yönlü stratejimiz yok. Ters yön için KWEB/FXI düşüşü sonrası FXI ertesi gün ortalaması negatif değil (dönüş) -> kullanım alanı yok.",
    "CWEB": "KWEB 2x; likidite sınırda (12 mn $). S1 kuralı KWEB sinyaliyle C0 h=1 net +145 bp (t 2,33) — ilginç ama dayanak KWEB başka ailede ve araç ince.",
    "EWS": "25 mn $, 20 bp; S1 genişletilmiş kontrolde pozitif (t 1,16) ama strateji yok.",
    "VNM": "S1 genişletilmiş kontrolde güçlü (C0 h=1 net +98 bp, t 2,07) fakat likidite sınırda (12 mn $), 20 bp; tek ETF seçimi seçim yanlılığı riski taşır.",
    "TUR": "Türk yatırımcı için ilginç ama ince: medyan 6,8 mn $/gün, tahmini makas 15 bp (gidiş-dönüş 27 bp; 1.000$'da 45 bp). Gecikmeli öncü yok (SPY/DIA/XLF'ten ters gecikme yalnız IS'te); genel kütüphanede hiçbir sinyal maliyeti geçmiyor. İzlenecekse BIST:XU100 ve FX_IDC:USDTRY gerçek zamanlı; uzatılmış saatte yalnız limit emir.",
    "EDC": "EEM 3x; likidite ince (7 mn $), 27 bp.", "EDZ": "EEM -3x; ince (3,8 mn $).", "BRZU": "EWZ 2x; ince (3,7 mn $).",
    "CHAU": "ASHR 2x; ince (2,3 mn $).", "EURL": "VGK 3x; çok ince (1 mn $).", "INDL": "INDA 2x; çok ince (0,9 mn $).", "MEXX": "EWW 3x; çok ince (0,6 mn $).",
}
def karar_satiri(s):
    r = scr.loc[s]
    if s in KABUL: k, g = "kabul", KABUL[s]
    elif s in YEDEK: k, g = "yedek", YEDEK[s]
    elif s in RED_OZEL: k, g = "red", RED_OZEL[s]
    else:
        dv = r["med_dollar_vol_m"]
        if dv < 10:
            k, g = "red", f"Likidite yetersiz (medyan {dv:.1f} mn $/gün < 10), tahmini gidiş-dönüş maliyet {r['cost_rt_bp']:.0f} bp; strateji yok."
        else:
            k, g = "red", f"Doğrulanmış strateji/öncü yok (genel kütüphane ve aile hipotezlerinde maliyet sonrası anlamlı sonuç yok); medyan {dv:.0f} mn $, maliyet {r['cost_rt_bp']:.0f} bp, maliyet/oynaklık {r['cost_over_1d_vol']:.2f}."
    return {"sym": s, "karar": k, "gerekce": g, "tv": ortak.tv(s), "likidite_mn_usd": r2(r["med_dollar_vol_m"], 1),
            "maliyet_bp": r2(r["cost_rt_bp"], 1), "vol_1d_bp": r2(r["vol_1d_bp"], 0)}

IZ = [karar_satiri(s) for s in ortak.FAM]
order = {"kabul": 0, "yedek": 1, "red": 2}
IZ.sort(key=lambda x: (order[x["karar"]], -(x["likidite_mn_usd"] or 0)))
pd.DataFrame(IZ).to_csv(os.path.join(OUT, "izleme.csv"), index=False)

# ---------------- lead-lag ----------------
RT = {  # gerçek zamanlı izleme (yerel piyasa kapalıyken işleyen), yalnız doğrulanmış kodlar; öncü DEĞİL
    "kore": [("KOSPI (seans TR 03:00-09:30)", "KRX:KOSPI", "EWY açılış boşluğunu belirleyen yerel seans"),
             ("Nasdaq 100 vadelisi", "CME_MINI:NQ1!", "gece yön; yarı iletken ağırlığı"), ("S&P 500 vadelisi", "CME_MINI:ES1!", "gece risk iştahı")],
    "tayvan": [("Nasdaq 100 vadelisi", "CME_MINI:NQ1!", "gece yön; yarı iletken ağırlığı"), ("S&P 500 vadelisi", "CME_MINI:ES1!", "gece risk iştahı")],
    "cin": [("Hang Seng vadelisi", "HKEX:HSI1!", "gece seansı ~TR 12:15-22:00"), ("Hang Seng endeksi", "TVC:HSI", "yerel kapanış TR 11:00"),
            ("USD/CNH", "FX:USDCNH", "24 saat kur"), ("FTSE China A50 vadelisi", "SGX:CN1!", "uzun seans Çin duyarlılığı")],
    "cin_a": [("CSI 300", "SSE:000300", "dayanak; kapanış TR 10:00"), ("FTSE China A50 vadelisi", "SGX:CN1!", "gece seansı"), ("USD/CNH", "FX:USDCNH", "24 saat kur")],
    "japonya": [("Nikkei 225 vadelisi", "OSE:NK2251!", "gece seansı ~TR 10:45-00:00; açılış boşluğu"), ("Nikkei 225", "TVC:NI225", "yerel kapanış TR 09:30"),
                ("USD/JPY", "FX_IDC:USDJPY", "24 saat; EWJ kur korumasız")],
    "avustralya": [("AUD/USD", "FX:AUDUSD", "24 saat kur"), ("Bakır vadelisi", "COMEX:HG1!", "madencilik ağırlığı"), ("S&P 500 vadelisi", "CME_MINI:ES1!", "gece risk iştahı")],
    "hongkong": [("Hang Seng vadelisi", "HKEX:HSI1!", "gece seansı"), ("Hang Seng endeksi", "TVC:HSI", "yerel kapanış TR 11:00")],
    "em": [("Hang Seng vadelisi", "HKEX:HSI1!", "Çin ağırlığı"), ("KOSPI", "KRX:KOSPI", "Kore ağırlığı"), ("USD/CNH", "FX:USDCNH", "24 saat kur"),
           ("S&P 500 vadelisi", "CME_MINI:ES1!", "gece risk iştahı")],
    "eafe": [("DAX vadelisi", "EUREX:FDAX1!", "Avrupa açılışı öncesi yön"), ("Euro Stoxx 50", "TVC:SX5E", "kapanış kış TR 19:30"),
             ("Nikkei 225 vadelisi", "OSE:NK2251!", "Japonya ağırlığı"), ("EUR/USD", "FX:EURUSD", "24 saat kur")],
    "avrupa": [("DAX vadelisi", "EUREX:FDAX1!", "Avrupa açılışı öncesi yön"), ("Euro Stoxx 50", "TVC:SX5E", "kapanış kış TR 19:30"),
               ("FTSE 100", "TVC:UKX", "İngiltere ağırlığı"), ("EUR/USD", "FX:EURUSD", "24 saat kur")],
    "brezilya": [("Ibovespa", "BMFBOVESPA:IBOV", "ABD ile büyük ölçüde eşzamanlı"), ("USD/BRL", "FX_IDC:USDBRL", "kur getirinin büyük kısmı"), ("Brent vadelisi", "ICEEUR:BRN1!", "Petrobras ağırlığı")],
    "hindistan": [("Nifty 50", "NSE:NIFTY", "yerel kapanış TR 13:00"), ("S&P 500 vadelisi", "CME_MINI:ES1!", "gece risk iştahı")],
    "cin_tekno": [("Hang Seng vadelisi", "HKEX:HSI1!", "gece seansı"), ("USD/CNH", "FX:USDCNH", "24 saat kur")],
}
RT_MAP = {"EWY": "kore", "KORU": "kore", "EWT": "tayvan", "FXI": "cin", "YINN": "cin", "EWJ": "japonya", "EWA": "avustralya", "EWH": "hongkong",
          "EEM": "em", "IEMG": "em", "EFA": "eafe", "VGK": "avrupa", "EWZ": "brezilya", "INDA": "hindistan", "ASHR": "cin_a", "CQQQ": "cin_tekno"}
TAKVIM = {
    "asya_ortak": "ABD: CPI 10 Kas, NFP 4 Ara, CPI 10 Ara, FOMC 9 Ara 2026 (Asya'ya ertesi sabah yansır); NYSE 26 Kas kapalı, 27 Kas/24 Ara erken kapanış (TR 21:00). Yerel tatillerde ETF NAV'sız işlem görür.",
    "kore": "Kore: Seollal (Şub 2027 başı), çeyreklik vade 10 Ara 2026; KORU'da 3x günlük yeniden dengeleme.",
    "cin": "Çin/HK: Ay Yeni Yılı (Şub 2027 başı, teyit edilmeli), teşvik/kur haberleri; YINN 3x.",
    "japonya": "Japonya: BoJ Aralık toplantısı (teyit edilmeli), 31 Ara-3 Oca tatili; USDJPY şokları.",
    "tayvan": "Tayvan: Ay Yeni Yılı, TSMC aylık satışları (~her ayın 10'u); temettü ex-günleri düzeltilmemiş grafikte sahte düşüş gösterebilir.",
    "avrupa": "Avrupa: ECB Aralık toplantısı (teyit edilmeli), Noel tatilleri; yerel kapanış kış TR 19:30.",
    "brezilya": "Brezilya: Copom kararları, Karnaval (Şub 2027), BRL oynaklığı.",
    "hindistan": "Hindistan: RBI Aralık toplantısı (teyit edilmeli), bütçe 1 Şub; seçim şokları.",
    "em": "EM: Çin+Kore+Tayvan+Hindistan takvimleri; MSCI Kasım endeks değişikliği ay sonu (teyit edilmeli).",
}
TK_MAP = {"EWY": ["asya_ortak", "kore"], "KORU": ["asya_ortak", "kore"], "EWT": ["asya_ortak", "tayvan"], "FXI": ["asya_ortak", "cin"], "YINN": ["asya_ortak", "cin"],
          "ASHR": ["asya_ortak", "cin"], "CQQQ": ["asya_ortak", "cin"], "EWH": ["asya_ortak", "cin"], "EWJ": ["asya_ortak", "japonya"], "EWA": ["asya_ortak"],
          "EEM": ["asya_ortak", "em"], "IEMG": ["asya_ortak", "em"], "EFA": ["avrupa", "japonya"], "VGK": ["avrupa"], "EWZ": ["brezilya"], "INDA": ["asya_ortak", "hindistan"]}
S1_UYELER = {"EWJ", "EWY", "EWT", "FXI", "EWA", "EWH"}
S1_ETF = pd.read_csv(os.path.join(OUT, "S1_etf.csv"))
KAL = pd.read_csv(os.path.join(OUT, "S1_kaldiracli.csv"))
def s1_satir(s):
    x = S1_ETF[(S1_ETF["sym"] == s) & (S1_ETF["mode"] == "C0")]
    return x.iloc[0] if len(x) else None

LLROWS = []; LLJ = []
for it in IZ:
    s = it["sym"]
    if it["karar"] not in ("kabul", "yedek"): continue
    x = LL[LL["target"] == s].copy()
    x = x[~x["leader"].isin(ortak.GROUPS.get(ortak.SYM2GRP[s], []))]
    x["a"] = x["corr_1y"].abs()
    drv = []
    if s in ortak.LEV:
        u = ortak.UNDERLYING[s]
        a = np.log(lib.load(s)["c"]).diff(); b = np.log(lib.load(u)["c"]).diff()
        d = pd.concat([a, b], axis=1, keys=["a", "b"]).dropna().tail(252)
        drv.append({"ad": f"{u} (dayanak)", "tv": ortak.tv(u), "corr_1y": r2(d.a.corr(d.b), 3), "beta_1y": r2(np.cov(d.a, d.b)[0, 1] / d.b.var(), 2)})
    for r in x.sort_values("a", ascending=False).head(4).itertuples():
        drv.append({"ad": r.leader, "tv": tvl(r.leader), "corr_1y": r2(r.corr_1y, 2), "beta_1y": r2(r.beta_1y, 2)})
    # gecikmeli öncü: aile içi BH-FDR (lag_t_h1/h3) + IS/OOS aynı işaret + ekonomik büyüklük > maliyet
    onc = []
    if s in S1_UYELER or s in ("KORU", "YINN"):
        base = "EWY" if s == "KORU" else "FXI" if s == "YINN" else s
        rr = s1_satir(base)
        if s in ("KORU", "YINN"):
            kk = KAL[(KAL["arac"] == s) & (KAL["mode"] == "C0") & (KAL["h"] == 1)].iloc[0]
            etki = f"Koşul {base}'de sağlandığında {s} ertesi gün brüt {kk['mean_gross_bp']:.0f} bp (n={int(kk['n'])}); en kötü {kk['worst_bp']:.0f} bp"
            tt, ms = kk["t"], f"{s} için 2.500$'da net {kk['mean_net_bp']:.0f} bp (IS {kk['is_net_bp']:.0f} / OOS {kk['oos_net_bp']:.0f}); t<2 -> eşik altında"
        else:
            etki = f"Koşul sağlandığında {base} ertesi gün brüt {rr['mean_gross_bp']:.0f} bp (n={int(rr['n'])}); sepet net +56 bp"
            tt, ms = rr["t"], f"net {rr['mean_net_bp']:.0f} bp (IS {rr['is_net_bp']:.0f} / OOS {rr['oos_net_bp']:.0f})"
        onc.append({"ad": "SPY koşullu kuralı (S1: SPY<=-%1,5 ve ETF<=SPY)", "tv": "AMEX:SPY",
                    "tip": "koşullu eşik; doğrusal testte doğrulanmadı", "etki": etki,
                    "t": r2(tt, 2), "is_t": None, "oos_t": None, "fdr": False, "ufuk": "t+1", "maliyet_sonrasi": ms})
    best = x.assign(m=x[["lag_t_h1", "lag_t_h3"]].abs().max(axis=1)).sort_values("m", ascending=False).head(1)
    en_iyi = "; ".join(f"{b.leader} h1 t={b.lag_t_h1:.2f} (IS {b.lag_t_h1_is:.2f}/OOS {b.lag_t_h1_oos:.2f}), h3 t={b.lag_t_h3:.2f}" for b in best.itertuples())
    rt = [{"ad": a, "tv": t, "neden": n} for a, t, n in RT[RT_MAP[s]] if t in TVOK or t.startswith(("AMEX:", "NASDAQ:", "CBOE:"))]
    not_ = f"Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): {en_iyi}. Sürücüler eşzamanlıdır, öncü değildir."
    if s in S1_UYELER or s in ("KORU", "YINN"):
        not_ += " SPY satırı S1'in koşullu kuralıdır, doğrusal öncü değildir."
    if s in ("EEM", "IEMG"):
        not_ += " KWEB(t)->EEM(t+1) kısmi katsayısı pozitif (t 3,4) ama tek başına kural olarak ters işaretli -> kullanılamaz."
    if s in ("EWY", "KORU", "EWT", "EWJ"):
        not_ += " Reel faiz düşüşü (FRED:DFII10) 3 gün ufkunda pozitif aday (IS/OOS aynı işaret, FDR yok)."
    if s == "EWA":
        not_ += " IWM(t)->EWA(t+1) pozitif (t 3,1; IS 2,3/OOS 2,1), FDR yok, keşifsel."
    tk = " ".join(TAKVIM[k] for k in TK_MAP.get(s, []))
    LLJ.append({"sym": s, "suruculer": drv, "onculer": onc, "gercek_zamanli": rt, "not": not_, "takvim_riskleri": tk})
    for dd in drv: LLROWS.append({"sym": s, "tur": "surucu", **dd})
    for dd in rt: LLROWS.append({"sym": s, "tur": "gercek_zamanli", **dd})
pd.DataFrame(LLROWS).to_csv(os.path.join(OUT, "leadlag_izleme.csv"), index=False)

# ---------------- stratejiler ----------------
P1 = pd.read_csv(os.path.join(OUT, "S1_havuz.csv")).set_index("set")
UL = pd.read_csv(os.path.join(OUT, "ul03_saglamlik_havuz.csv"))
def ps(name): return P1.loc[name]
a = ps("S1 sepet6 C0 h=1"); o1 = ps("S1 sepet6 O1 h=1"); c1 = ps("S1 sepet6 C1 h=1"); a2 = ps("S1 sepet6 C0 h=2"); o2 = ps("S1 sepet6 O1 h=2")
p1000 = ps("S1 sepet6 C0 h=1 poz=1000$"); p10000 = ps("S1 sepet6 C0 h=1 poz=10000$"); ek = ps("Aynı kural, listede olmayan 6 Asya ETF'i C0 h=1")
def ul(set_, mode="C0", h=1):
    return UL[(UL["set"] == set_) & (UL["mode"] == mode) & (UL["h"] == h)].iloc[0]
am = ul("plasebo_Amerika"); av = ul("plasebo_Avrupa"); sp = ul("plasebo_SPY_kendisi(SPY<=-1.5)"); tu = ul("tumleyen_ETF>SPY_Asya6")
k1 = ul("komsu_esik_-1.0_Asya6"); k2 = ul("komsu_esik_-2.0_Asya6")
H2 = pd.read_csv(os.path.join(OUT, "hipotez_havuz.csv")); A2 = pd.read_csv(os.path.join(OUT, "aile_havuz_genel.csv"))
IB = pd.read_csv(os.path.join(OUT, "ibs_bolge_havuz.csv"))
N_TEST = len(A2) + len(H2) + len(UL) + len(IB)
S1 = {
    "id": "uluslararasi_S1", "ad": "ABD sert düşüş günü Asya aşırı tepki dönüşü (UL03, sepet)",
    "kural": ("Günlük veri (TradingView'da temettü düzeltmesi 'ADJ' açık). Sinyal günü t: AMEX:SPY günlük değişimi = close/close[1]-1 <= -%1,50. "
              "Bu günde sepetteki her ETF için (AMEX:EWJ, AMEX:EWY, AMEX:EWT, AMEX:FXI, AMEX:EWA, AMEX:EWH) kendi günlük değişimi SPY'ın günlük değişiminden "
              "küçük ya da eşitse (ETF SPY'dan daha çok düştüyse) o ETF'te long aç; diğerlerinde işlem yok. Eşit tutar (ör. ETF başına 2.500 $). "
              "Çıkış: bir sonraki işlem günü kapanışı (h=1). Çıkış günü yeniden sinyal varsa pozisyon korunur. Açığa satış yok; yalnız long. "
              "Pine: spy=request.security(\"AMEX:SPY\",\"D\",close/close[1]-1); sig = spy<=-0.015 and (close/close[1]-1)<=spy."),
    "giris": ("C0: t günü ABD kapanışına ~10-15 dk kala (kış saati TR 23:45-23:50; yaz saati TR 22:45-22:50) koşul o anki fiyatlarla sağlanıyorsa piyasa/limit emirle al. "
              "Kaçırılırsa kapanış sonrası after-hours (kış TR 00:00-04:00) yalnız limit emirle, kapanış fiyatına yakın limitle. Kapanışa kadar fiyat değiştiğinden C0 hafif iyimserdir."),
    "tutus": "1 işlem günü (birincil, önceden belirlenmiş). Varyant h=2: sepet net +73 bp, t 2,33 (seçim yapılmadı, yalnız rapor).",
    "cikis": "t+1 kapanışına ~10 dk kala sat (kış TR ~23:50, yaz ~22:50). Stop kullanılmadı (testte yok). Yedek giriş: t+1 açılışında (TR 17:30 kış) alındıysa h=2 tut (O1 h=2: net +38 bp, t 1,76).",
    "islem_etf": ["EWY", "EWT", "FXI", "EWJ", "EWA", "EWH"], "sinyal_etf": "SPY (koşul) + işlem yapılan ETF'in kendi günlük getirisi",
    "n": int(a["n_dates"]), "brut_bp": r2(a["mean_gross_bp"]), "net_bp": r2(a["mean_net_bp"]), "t": r2(a["t_nw"], 2),
    "is_net_bp": r2(a["is_net_bp"]), "oos_net_bp": r2(a["oos_net_bp"]), "kazanma": r2(a["win_dates"], 2), "pf": r2(a["pf"], 2),
    "maxdd": r2(a["maxdd"], 3), "en_kotu_bp": -1356.2, "yil_pozitif": r2(a["years_pos_frac"], 2),
    "maliyet_duyarlilik": (f"Sepet C0 h=1 net: 1.000$ {p1000['mean_net_bp']:.1f} bp (t {p1000['t_nw']:.2f}); 2.500$ {a['mean_net_bp']:.1f} bp (t {a['t_nw']:.2f}); "
                           f"10.000$ {p10000['mean_net_bp']:.1f} bp (t {p10000['t_nw']:.2f}). Brüt {a['mean_gross_bp']:.1f} bp; ETF başı maliyet 13-16 bp (2.500$)."),
    "mod_saglamlik": (f"h=1: C0 brüt {a['mean_gross_bp']:.0f} bp / O1 {o1['mean_gross_bp']:.0f} bp / C1 {c1['mean_gross_bp']:.0f} bp. h=2: C0 {a2['mean_gross_bp']:.0f} / O1 {o2['mean_gross_bp']:.0f} (net {o2['mean_net_bp']:.0f}, t {o2['t_nw']:.2f}) / C1 {ps('S1 sepet6 C1 h=2')['mean_gross_bp']:.0f}. "
                      "O1 ve C1'de brüt kenar pozitif ama kenarın büyük kısmı t kapanışı -> t+1 açılışı gece boşluğunda: AĞIRLIKLA KAPANIŞA BAĞIMLI."),
    "aile_ici": (f"Listede olmayan 6 Asya ETF'inde (INDA, EWS, ASHR, CQQQ, EIDO, VNM) aynı kural C0 h=1 net {ek['mean_net_bp']:.0f} bp (t {ek['t_nw']:.2f}; IS {ek['is_net_bp']:.0f} / OOS {ek['oos_net_bp']:.0f}). "
                 f"Plasebo (eşzamanlı piyasalar): Amerika ETF'leri brüt {am['mean_gross_bp']:.0f} bp (net {am['mean_net_bp']:.0f}), Avrupa brüt {av['mean_gross_bp']:.0f} (net {av['mean_net_bp']:.0f}), SPY'ın kendisi brüt {sp['mean_gross_bp']:.0f}. "
                 f"Aynı günlerde SPY'dan az düşen Asya ETF'leri brüt {tu['mean_gross_bp']:.0f} bp. Eşleştirilmiş fark (aynı gün): ETF<=SPY eksi ETF>SPY +39,7 bp (t 2,88); Asya eksi Amerika +43,8 bp (t 2,40) -> mekanizma (eşzamansız fiyatlamada ABD'ye aşırı tepki) ile tutarlı. "
                 f"Komşu eşikler (seçim için değil): -%1,0 net {k1['mean_net_bp']:.0f} bp (OOS {k1['oos_net_bp']:.0f}); -%2,0 net {k2['mean_net_bp']:.0f} bp (OOS {k2['oos_net_bp']:.0f}). "
                 "ETF bazında C0 h=1 t: EWY 2,41, EWT 2,00, FXI 1,17, EWJ 1,21, EWA 0,97, EWH 1,54 (hepsi net > 0). EEM: net +57 bp (t 1,6)."),
    "test_sayisi": N_TEST,
    "fdr": ("Önceden belirlenmiş 6 literatür hipotezinin birincil spesifikasyonları (UL01-UL06) içinde BH q=0,10 GEÇER (tek yönlü p=0,013 <= 0,0167). "
            f"Tüm {N_TEST} havuz testi (genel kütüphane 297 + aile hipotezleri 135 + sağlamlık 108 + IBS-bölge 24) içinde GEÇMEZ."),
    "guven": "orta",
    "betik": REL("kod/ajan_uluslararasi/strateji_S1_ul03_asya.py"),
    "notlar": ("Sinyal seyrek: 10 yılda 110 gün (yılda ~11), sinyal başına ortalama 2,7 ETF; 6 ETF için ~15.000 $ sermaye gerekebilir. Getiri yüksek oynaklık dönemlerinde yoğun: 2020 hariç net 41 bp (t 1,78), 2020 ve 2026 birlikte hariç net 21 bp (t 1,03). "
               "Yıllar: 2018 -6, 2019 +74, 2020 +122, 2021 +76, 2022 +18, 2023 +30, 2024 -46, 2025 +34, 2026 +200 bp (sinyal günü ortalaması). En kötü tek işlem EWA 11 Mar 2020 -1.356 bp; en kötü sepet günü -1.202 bp. "
               "EWY hariç sepet net 51 bp (t 2,10). Kaldıraçlı uygulama (dayanak sinyaliyle, Midas'ta bulunurluk doğrulanmadı): KORU<-EWY C0 h=1 net +257 bp (t 1,95), h=2 +337 bp (t 2,12), en kötü -3.776 bp; "
               "YINN<-FXI C0 h=1 t 1,25, h=2 +336 bp (t 2,27). Kaldıraçlı sürümler t>=2 eşiğini birincil spesifikasyonda geçmiyor; 3x ürünlerde tek gün -%30..-40 mümkün. "
               "TradingView'da düzeltilmemiş grafikte EWT/EWY Aralık temettü ex-günleri sahte 'düşüş' gibi görünebilir: ADJ açık kullanın ya da ex-div gününü atlayın.")
}
S2 = pd.read_csv(os.path.join(OUT, "S2_ewy.csv"))
def s2(arac, mode, h): return S2[(S2["arac"] == arac) & (S2["mode"] == mode) & (S2["h"] == h)].iloc[0]
b = s2("EWY", "C0", 1); bo = s2("EWY", "O1", 1); bc = s2("EWY", "C1", 1); kk = s2("KORU", "C0", 1)
S2A = pd.read_csv(os.path.join(OUT, "S2_aile.csv"))
S2J = {
    "id": "uluslararasi_S2", "ad": "EWY gün sonu dip dönüşü (IBS<0,10 ve düşüş günü) — KEŞİFSEL",
    "kural": ("AMEX:EWY günlük mum: IBS = (close-low)/(high-low) < 0,10 VE close < close[1] ise EWY long (t kapanışı); t+1 kapanışında çık. "
              "Pine: ibs=(close-low)/(high-low); sig = ibs<0.10 and close<close[1]. İsteğe bağlı kaldıraçlı uygulama: sinyal EWY'den, işlem AMEX:KORU."),
    "giris": "C0: EWY kapanışına ~5-10 dk kala (kış TR 23:50, yaz 22:50) gün içi düşük seviyeye çok yakın ve önceki kapanışın altında ise al. IBS kapanış fiyatına bağlı -> C0 iyimser; after-hours limit emriyle de denenebilir.",
    "tutus": "1 işlem günü", "cikis": "t+1 kapanışına ~10 dk kala sat.",
    "islem_etf": ["EWY"], "sinyal_etf": "EWY",
    "n": int(b["n"]), "brut_bp": r2(b["mean_gross_bp"]), "net_bp": r2(b["mean_net_bp"]), "t": r2(b["t"], 2), "is_net_bp": r2(b["is_net_bp"]),
    "oos_net_bp": r2(b["oos_net_bp"]), "kazanma": r2(b["win"], 2), "pf": r2(b["pf"], 2), "maxdd": r2(b["maxdd"], 3), "en_kotu_bp": r2(b["worst_bp"]),
    "yil_pozitif": r2(b["years_pos_frac"], 2),
    "maliyet_duyarlilik": f"Net: 1.000$ {b['net_1000_bp']:.1f} bp; 2.500$ {b['mean_net_bp']:.1f} bp; 10.000$ {b['net_10000_bp']:.1f} bp (brüt {b['mean_gross_bp']:.1f}, maliyet 13 bp).",
    "mod_saglamlik": f"C0 brüt {b['mean_gross_bp']:.0f} bp / O1 {bo['mean_gross_bp']:.0f} bp (net {bo['mean_net_bp']:.0f}) / C1 {bc['mean_gross_bp']:.0f} bp. Kenar neredeyse tamamen gece boşluğunda: KAPANIŞA BAĞIMLI.",
    "aile_ici": (f"Aynı kural ailenin 29 likit bağımsız ETF'inde: pozitif net oranı {(S2A['mean_net_bp'] > 0).mean():.2f}, t>=2 yalnız EWY. Asya havuzu brüt 24 bp, net 7 bp (t 1,46); Amerika havuzu net -12 bp. "
                 "Ailede tutarlı DEĞİL; EWY'nin ayırt edici özelliği en düşük maliyet/oynaklık oranı (0,034) ve güçlü negatif otokorelasyon (IS -0,16 / OOS -0,12)."),
    "test_sayisi": 20196, "fdr": "genel_tum aile satırları (20.196) içinde tek yönlü BH q=0,10 GEÇMEZ (geçen 0). Seçilmiş sonuç.",
    "guven": "dusuk", "betik": REL("kod/ajan_uluslararasi/strateji_S2_ewy_ibs.py"),
    "notlar": (f"Kabul eşiğini biçimsel olarak geçiyor (t {b['t']:.2f}, IS {b['is_net_bp']:.0f} / OOS {b['oos_net_bp']:.0f} bp, yılların %70'i pozitif, n={int(b['n'])}, O1 brüt > 0) ama tarama içinden seçildi ve FDR'yi geçmiyor. "
               "Getirinin yarıdan fazlası 2026'dan (21 işlem, ort. +232 bp) ve 2020'den; 2020 ve 2026 hariç net ~+12 bp. "
               f"KORU (EWY sinyaliyle) C0 h=1 net {kk['mean_net_bp']:.0f} bp (t {kk['t']:.2f}), en kötü {kk['worst_bp']:.0f} bp. S1 ile EWY'de çakışabilir (aynı gün iki sinyal = tek pozisyon).")
}
STR = [S1, S2J]

ELENEN = [
    {"ad": "Genel kütüphane (31 sinyal x mod x h, 297 kombinasyon) aile havuzu", "neden": "29 likit bağımsız ETF'te gün-kümeli havuz testinde hiçbir kombinasyon BH-FDR'yi geçmedi; en iyi t 1,69 (CA_tatil_oncesi C1 h=3, mekanizmasız). ETF başına Stouffer toplamları (ör. tatil öncesi 6,9) aynı tarihlerde ortak faktörü saydığı için yanıltıcı."},
    {"ad": "genel_tum aile satırları (20.196) — tek ETF sonuçları", "neden": "Tek yönlü BH q=0,10 ile geçen yok. İki yönlü p ile görülen 22 'geçen' (BRZU, CWEB, KORU, EWY...) çok sayıda anlamlı negatif sonucun eşiği gevşetmesinden kaynaklanan yapay sonuç."},
    {"ad": "UL01 ülke IBS<0,20 (C0 h=1)", "neden": f"10 ETF havuzu brüt {H2[(H2.hyp=='UL01_ulke_IBS')&(H2['mode']=='C0')&(H2.h==1)].iloc[0]['mean_gross_bp']:.1f} bp < maliyet (~15 bp); net -9 bp, OOS -17 bp. Pandey-Joshi (2009-2019, maliyetsiz) etkisi maliyet sonrası yok."},
    {"ad": "UL02 kesitsel en düşük IBS 3 ülke", "neden": "Brüt 8 bp, net -8 bp (t -3,1); her gün işlem maliyeti öldürüyor."},
    {"ad": "UL04 (vekil) SPY'a göre kalıntı z<=-2 dönüşü / 'yetişme' sinyali", "neden": "iNAV verisi yok; kalıntı vekili 29 ETF'te brüt 6 bp, net -12 bp; Avrupa'da kalıntı dönüşü ters (devam). Yetişme testindeki FDR sonuçları ilgisiz öncülerle de çıkıyor -> ETF'in kendi dönüşü; öncü katkısı yok."},
    {"ad": "UL05 ülke ay dönümü (T-1 -> yeni ayın 2. günü)", "neden": "9 ETF havuzu net -5 bp (C0 h=3). Ay sonu kapanışı -> 3. gün varyantı brüt 46 bp ama OOS +4 bp, t 1,38."},
    {"ad": "UL06 FOMC öncesi (D-1 -> D)", "neden": "Net +7 bp, t 0,52; 2 ve 3 günlük tutuşta negatif. Literatürle uyumlu (2015 sonrası drift yok)."},
    {"ad": "Y1 Asya <- SPY/QQQ gecikmesi (SPY z<=-2 ya da QQQ z<=-2 -> Asya long)", "neden": "Koşulsuz büyük ABD düşüşü sonrası Asya ETF'leri: net +16 bp (t 0,75), O1/C1 negatif. Ayırt edici olan ETF'in SPY'dan fazla düşmesi (S1)."},
    {"ad": "DXJ <- QQQ/SPY ters gecikmesi (taramada FDR geçti)", "neden": "Eşik kuralına çevrildiğinde (SPY z<=-2 -> DXJ al) C0 h=1 net -1 bp; doğrusal ilişki uzun-tek yönlü işleme dönüşmüyor."},
    {"ad": "Y2 KWEB -> EEM/Asya (taramada t~3,4, IS/OOS aynı işaret)", "neden": "KWEB z>=1 sonrası hedeflerde brüt -2 bp (10 ETF, 338 gün); kısmi regresyon katsayısı kendi gecikmesine koşullu. KWEB düşüşü sonrası EEM/FXI ertesi gün yükseliyor (ters işaret) -> öncü olarak kullanılamaz."},
    {"ad": "Y3 EWZ <- USO (USO z>=1,5 -> EWZ)", "neden": "Net -16 bp (C0 h=1), IS negatif, OOS pozitif; tarama da gecikmeli ilişki göstermiyor (lag_t_h1 -0,47)."},
    {"ad": "Kaldıraçlı ürünlerin kendi sinyalleri (BRZU, CWEB, KORU, YINN genel kütüphane)", "neden": "Tek yönlü FDR'yi geçmiyor; bunlar dayanak sinyaliyle (S1/S2) uygulama aracı olarak değerlendirildi."},
    {"ad": "26 ince ETF (medyan dolar hacim < 10 mn $: EIS, EDC, TUR, EWM, EWD, EWN, GREK, UAE, EPU, THD, EDZ, BRZU, EPHE, CHAU, EURL, EWO, INDL, NORW, ENZL, MEXX, EDEN, EFNL, EWK, CHIQ, QAT, KEMQ)", "neden": "Tahmini makas 15-35 bp (gidiş-dönüş 27-47 bp); hiçbir sinyal bu maliyeti tutarlı biçimde aşmıyor."},
    {"ad": "Kopyalar (VWO/IEMG ~ EEM; VEA/IEFA ~ EFA; EZU ~ VGK; MCHI ~ FXI; EPI ~ INDA; DXJ ~ EWJ)", "neden": "Bağımsız kanıt değil; en likit/ucuz temsilci seçildi."},
]
DOSYALAR = [REL(p) for p in [
    "notlar/aile_uluslararasi.md", "sonuclar/aile_uluslararasi/sonuc.json",
    "kod/ajan_uluslararasi/ortak.py", "kod/ajan_uluslararasi/a1_islenebilirlik_genel.py", "kod/ajan_uluslararasi/a2_aile_havuz.py",
    "kod/ajan_uluslararasi/a3_hipotezler.py", "kod/ajan_uluslararasi/a4_ul03_saglamlik.py", "kod/ajan_uluslararasi/a5_ibs_bolge.py",
    "kod/ajan_uluslararasi/strateji_S1_ul03_asya.py", "kod/ajan_uluslararasi/strateji_S2_ewy_ibs.py", "kod/ajan_uluslararasi/a6_sonuc_json.py",
    "sonuclar/aile_uluslararasi/islenebilirlik.csv", "sonuclar/aile_uluslararasi/genel_aile_tutarlilik.csv", "sonuclar/aile_uluslararasi/aile_havuz_genel.csv",
    "sonuclar/aile_uluslararasi/hipotez_havuz.csv", "sonuclar/aile_uluslararasi/hipotez_etf.csv", "sonuclar/aile_uluslararasi/ul03_saglamlik_havuz.csv",
    "sonuclar/aile_uluslararasi/ul03_etf.csv", "sonuclar/aile_uluslararasi/ibs_bolge_havuz.csv", "sonuclar/aile_uluslararasi/ibs_bolge_etf.csv",
    "sonuclar/aile_uluslararasi/S1_havuz.csv", "sonuclar/aile_uluslararasi/S1_etf.csv", "sonuclar/aile_uluslararasi/S1_kaldiracli.csv",
    "sonuclar/aile_uluslararasi/S2_ewy.csv", "sonuclar/aile_uluslararasi/S2_aile.csv", "sonuclar/aile_uluslararasi/izleme.csv",
    "sonuclar/aile_uluslararasi/leadlag_izleme.csv"]]
TVD = ["KRX:K2001! (KOSPI 200 vadelisi)", "FX_IDC:USDKRW", "TAIFEX:TXF1! (Tayvan endeks vadelisi)", "TWSE:TAIEX (tv_dogrulama'da 'yonlendirildi'; doğru TAIEX kodu doğrulanmalı)",
       "NSEIX:NIFTY1! (GIFT Nifty vadelisi)", "FX_IDC:USDINR", "ASX24:AP1! (ASX SPI 200 vadelisi)", "ICEUS:MME1! (MSCI EM vadelisi)",
       "EUREX:FESX1! (Euro Stoxx 50 vadelisi)", "HKEX:HTI1! (Hang Seng Tech vadelisi)", "BMFBOVESPA:WIN1! (mini Ibovespa vadelisi)"]
n_kabul = sum(1 for i in IZ if i["karar"] == "kabul"); n_yedek = sum(1 for i in IZ if i["karar"] == "yedek")
OZET = (f"Uluslararası ailede (68 ETF; 42'si >= 10 mn $/gün, 29 likit bağımsız temsilci) genel kütüphane ve aile hipotezleri gün-kümeli havuz testleriyle sınandı (toplam {N_TEST} havuz testi). "
        "Genel kütüphanede (IBS, RSI2, takvim, VIX rejimi) ailede tutarlı ve FDR'den geçen sinyal YOK; ülke IBS etkisi (Pandey-Joshi) maliyet sonrası negatif. "
        "Tek aday: uluslararasi_S1 (UL03, Levy-Lieberman): SPY <= -%1,5 olan günde SPY'dan daha çok düşen Asya ETF'lerini (EWJ, EWY, EWT, FXI, EWA, EWH) kapanışta al, ertesi kapanışta sat. "
        f"Sepet: 110 sinyal günü, net +{a['mean_net_bp']:.0f} bp (2.500$), t {a['t_nw']:.2f}, IS +{a['is_net_bp']:.0f} / OOS +{a['oos_net_bp']:.0f} bp, yılların %78'i pozitif; listede olmayan 6 Asya ETF'inde de pozitif, eşzamanlı Amerika/Avrupa plasebolarında zayıf (mekanizma tutarlı). "
        "Zayıflıklar: kapanışa bağımlı (kenarın çoğu gece boşluğunda), getiri 2020 ve 2026 gibi yüksek oynaklık dönemlerinde yoğun, tüm varyantlarla birlikte FDR'yi geçmiyor (yalnız önceden belirlenmiş 6 birincil hipotez içinde geçiyor) -> güven orta. "
        "uluslararasi_S2 (EWY IBS dip dönüşü) eşiği biçimsel geçse de taramadan seçilmiş ve FDR'siz -> düşük güven, keşifsel. "
        "Lead-lag: aile içi 2.685 hedef-öncü çiftinde doğrusal gecikmeli öncü FDR'den geçmiyor; 'yetişme' sinyalleri ETF'in kendi dönüşünü yansıtıyor; KWEB->EEM ilişkisi kural olarak işe yaramıyor. "
        f"İzleme: {n_kabul} kabul (EWY, EWT, FXI, EWJ), {n_yedek} yedek (EWA, EWH, EEM, IEMG, EFA, VGK, EWZ, INDA, ASHR, CQQQ, KORU, YINN). TUR ince (6,8 mn $, 27 bp) -> red. "
        "Kaldıraçlı ürünler (KORU/YINN) yalnız dayanak sinyaliyle uygulama aracı; Midas bulunurluğu doğrulanmadı. Bu ailede PTP/K-1 ürünü yok.")
def _temiz(o):
    if isinstance(o, dict): return {k: _temiz(v) for k, v in o.items() if v is not None}
    if isinstance(o, list): return [_temiz(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    return o
SON = {"family": "uluslararasi", "ozet": OZET, "izleme": IZ, "stratejiler": STR, "elenen": ELENEN, "leadlag": LLJ, "dosyalar": DOSYALAR, "tv_dogrulanacak": TVD}
SON = _temiz(SON)
json.dump(SON, open(os.path.join(OUT, "sonuc.json"), "w"), ensure_ascii=False, indent=1)
print("yazıldı:", os.path.join(OUT, "sonuc.json"), "| izleme", len(IZ), "kabul", n_kabul, "yedek", n_yedek, "| leadlag", len(LLJ), "| test", N_TEST)
for s in STR: print(s["id"], s["n"], s["net_bp"], s["t"], s["is_net_bp"], s["oos_net_bp"], s["guven"])
