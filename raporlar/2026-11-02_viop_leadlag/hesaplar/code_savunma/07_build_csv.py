"""07: f_savunma.csv üretimi (sayılar res/ altındaki sonuç dosyalarından çekilir)."""
from sv import *
P1 = pd.read_csv(RES + "/01_pairs.csv").set_index(["stock", "driver"])
BT = pd.read_csv(RES + "/05_backtests.csv")
S4 = pd.read_csv(RES + "/04_scan.csv").set_index(["stock", "driver"])
def bt(name, cost=8.0):
    r = BT[(BT.bt == name) & (BT.cost == cost)].iloc[0]; return r
def base(st, d):
    if (st, d) not in P1.index: return {}
    r = P1.loc[(st, d)]
    return dict(corr_full=r.corr_full, corr_3y=r.corr_3y, corr_1y=r.corr_1y, pcorr_xu100=r.pcorr_xu100, beta=r.beta, n=int(r.n),
                gap_corr=r.gap_l1, intra_corr=r.intra_l1, is_oos=f"pc IS {r.pc_is:.2f} / OOS {r.pc_oos:.2f}; yıl aynı işaret {r.yr_same_sign:.0%}")
# TTKOM imtiyaz olayı (KAP 27.08.2025)
a = ll.ret("TTKOM", clean=False); m = ll.ret("XU100", clean=False); c_ = ll.ret("TCELL", clean=False)
b = (a.rolling(250, min_periods=120).cov(m) / m.rolling(250, min_periods=120).var()).shift(1); ar = a - b * m
ev = {d: (round(1e4 * ar.get(pd.Timestamp(d), np.nan)), round(1e4 * c_.get(pd.Timestamp(d), np.nan))) for d in ["2025-08-27", "2025-08-28", "2025-08-29"]}
ev_car = round(1e4 * ar.loc["2025-08-27":"2025-09-03"].sum())
print("TTKOM imtiyaz AR (bps) / TCELL r:", ev, "CAR 27.08-03.09:", ev_car)
rows = []
def add(stock, drv_y, desc, tv, rel, lag, conf, mech, notes, src=None, **kw):
    r = dict(stock=stock, driver_yahoo=drv_y, driver_desc=desc, tv_ticker=tv, relation=rel, lag=lag)
    if src: r.update(base(*src))
    r.update(kw); r.update(confidence=conf, mechanism=mech, notes=notes); rows.append(r)
p = lambda st, d, k: P1.loc[(st, d), k]
# ---------------- TCELL
add("TCELL", "TKC", "Turkcell NYSE ADR (1 ADS = 2,5 hisse; 2 ADS = 5 hisse)", "NYSE:TKC", "sync", 0, "YÜKSEK", "Aynı şirket (ADR); arbitraj",
    "En güçlü senkron ilişki; USD bazlı TCELL ile corr 0,71 (son 3y 0,83). İşlem sinyali değil, aynı varlık.", ("TCELL", "TKC"), t_stat=p("TCELL", "TKC", "c0_t"))
add("TCELL", "TKC", "TKC günlük getiri t-1 -> TCELL gap t", "NYSE:TKC", "lead_gap", 1, "ORTA", "ABD seansında oluşan bilgi BIST açılışında fiyatlanır (eşzamansız kapanış)",
    "İŞLENEMEZ (VİOP pay vadelileri akşam seansında yok). Saatlik: TKC 15:30->kapanış -> TCELL gap beta 0,20 t 2,9 ama ES=F post-close kontrolünde t 1,3: gap'in çoğu ABD piyasa hareketi. Beklenen 'en güçlü lead' ZAYIF: TKC post-close hareketinin yalnız ~%20'si gap'e geçiyor.",
    ("TCELL", "TKC"), t_stat=p("TCELL", "TKC", "gap_l1_t"))
r1 = bt("BT1u U |U|>50bps"); r15 = bt("BT1u U |U|>50bps", 15.0)
add("TCELL", "TKC+TRY=X", "TKC parite sapması D=ln(TKC*USDTRY/(2,5*TCELL)) - 20g ort.; açılışta kalan U=D-gap", "NYSE:TKC, FX:USDTRY, BIST:TCELL", "lead_intra", 1, "ORTA",
    "ADR'deki BIST-kapanış-sonrası bilgi TCELL açılışında eksik fiyatlanır, gün içinde tamamlanır",
    f"Regresyon intra_t ~ D_(t-1)+gap_t: b_D 0,13 (t 2,8); IS 0,09 (t 2,2) OOS 0,15 (t 2,4). BT |U|>50bps: IS {r1.IS_mean_bps:.1f} bps (Sh {r1.IS_sharpe:.2f}), OOS {r1.OOS_mean_bps:.1f} bps t {r1.OOS_t:.2f}; 15bps maliyette OOS Sh {r15.OOS_sharpe:.2f}. Tüm günlerde işlem: IS negatif. Maliyete çok duyarlı; açılış fiyatına giriş varsayımı iyimser.",
    t_stat=2.80, intra_corr=0.091, gap_corr=0.041, is_oos="IS b 0,086 t2,18 / OOS b 0,148 t2,36 (regresyon); BT IS~0, OOS+", bt_oos_sharpe=r1.OOS_sharpe, bt_oos_mean_bps=r1.OOS_mean_bps, n=int(r1.OOS_n + r1.IS_n))
rh = bt("BT1h tk_post |>50bps|->TCELL rest"); rh15 = bt("BT1h tk_post |>50bps|->TCELL rest", 15.0)
add("TCELL", "TKC (h1)", "TKC 15:30 UTC->ABD kapanışı getirisi -> TCELL ertesi gün 07:30 UTC->kapanış", "NYSE:TKC", "intraday_minutes", 1, "DÜŞÜK",
    "Yavaş bilgi yayılımı: TKC post-close hareketi açılışta değil gün içinde fiyatlanıyor",
    f"rest1 ~ tk_post beta 0,30 t 2,75 (n 694); ilk saat etkisi yok (t -0,9). BT |tk_post|>50bps: OOS {rh.OOS_mean_bps:.1f} bps, t {rh.OOS_t:.2f}, Sh {rh.OOS_sharpe:.2f} (15bps: {rh15.OOS_sharpe:.2f}), n {int(rh.OOS_n)}. Yalnız 2023-12+ saatlik veri -> kısa örneklem.",
    t_stat=2.75, intra_corr=0.118, gap_corr=0.145, is_oos="yalnız OOS (2023-12+)", bt_oos_sharpe=rh.OOS_sharpe, bt_oos_mean_bps=rh.OOS_mean_bps, n=694)
add("TCELL", "TKC", "TKC/TCELL parite primi kapanması (mean reversion)", "NYSE:TKC", "reverse", 1, "ORTA",
    "Arbitraj; çapa BIST tarafı",
    "dP_(t+1) ~ D_t beta -0,43 (t -12,5): sapmanın ~%43'ü ertesi gün kapanıyor; bunun ~%27'si TKC/kur, ~%16'sı TCELL tarafından. Prim seviyesi yıllık medyan -1,4%..+0,9%. Ters yön: TCELL_(t-1)->TKC t 1,3.",
    t_stat=-12.5, n=3094, is_oos="IS/OOS ayrı hesaplanmadı (tam dönem)")
add("TCELL", "TTKOM.IS", "Türk Telekom (yurt içi rakip)", "BIST:TTKOM", "sync", 0, "YÜKSEK", "Sektör faktörü (regülasyon, fiyatlama, BTK)", "Lead yok (gap/intra t<1,6).", ("TCELL", "TTKOM.IS"), t_stat=p("TCELL", "TTKOM.IS", "c0_t"))
add("TCELL", "^VIX", "VIX (risk iştahı) t-1 -> TCELL gap", "TVC:VIX", "lead_gap", 1, "ORTA", "Küresel risk iştahı BIST kapanışından sonra -> açılış gap'i", "İşlenemez (gap). Senkron kısmi ~0.", ("TCELL", "^VIX"), t_stat=p("TCELL", "^VIX", "gap_l1_t"))
for d, desc, tv in [("EM_TEL", "EM telekom sepeti (MTN, Vodacom, AMX, TIM, Bharti, OPL, MTelekom, Telkom, VEON)", "sepet"), ("EU_TEL", "Avrupa telekom sepeti (DTE, ORA, TEF, VOD.L, TEL, TELIA, KPN, OTE)", "sepet"),
                    ("VOD.L", "Vodafone", "LSE:VOD"), ("MTN.JO", "MTN Group", "JSE:MTN"), ("DTE.DE", "Deutsche Telekom", "XETR:DTE"), ("ORA.PA", "Orange", "EURONEXT:ORA"), ("TEF.MC", "Telefonica", "BME:TEF"), ("OPL.WA", "Orange Polska", "GPW:OPL")]:
    add("TCELL", d, desc, tv, "sync", 0, "DÜŞÜK", "Küresel telekom faktörü (zayıf)", "Ham corr piyasa kaynaklı; XU100 kontrollü kısmi ~0-0,08.", ("TCELL", d), t_stat=p("TCELL", d, "c0_t"))
add("TCELL", "VEON", "VEON (Ukrayna/Kazakistan/Pakistan operatörü)", "NASDAQ:VEON", "sync", 0, "ÇOK DÜŞÜK", "EM telekom / bölge riski", "Kısmi 0,01; gap_l1 t 2,6 (ABD kapanışı, işlenemez).", ("TCELL", "VEON"), t_stat=p("TCELL", "VEON", "c0_t"))
add("TCELL", "KYIV", "Kyivstar (2024-12+)", "NASDAQ:KYIV", "sync", 0, "ÇOK DÜŞÜK", "Ukrayna barış teması", "Kısa örneklem (~480g); kısmi 0,06.", ("TCELL", "KYIV"), t_stat=p("TCELL", "KYIV", "c0_t"))
add("TCELL", "TRY=X", "USDTRY (hizalı, ~00:00 UTC t+1)", "FX:USDTRY", "sync", 0, "DÜŞÜK", "TCELL FX gelir/hedge pozisyonu", "XU100 kontrollü kısmi +0,06 (IS 0,07, OOS 0,00) -> 2021 sonrası kayboldu.", ("TCELL", "FXAL"), t_stat=p("TCELL", "FXAL", "c0_t"))
add("TCELL", "LISN.SW", "Lindt (FDR'den geçen tek gün-içi lag1 sürücü)", "SIX:LISN", "lead_intra", 1, "ÇOK DÜŞÜK", "Mekanizma YOK (muhtemelen sahte/veri madenciliği)",
    "intra_l1 corr 0,08 t 4,6 (IS t 3,9, OOS t 2,8; SMI/ES kontrolünde t 4,1) ama BT OOS Sh 0,17; XU100/THYAO'da da benzer -> genel; 1121 testten biri.", t_stat=4.64, intra_corr=0.081, n=3200, bt_oos_sharpe=0.17)
# ---------------- TTKOM
add("TTKOM", "TCELL.IS", "Turkcell", "BIST:TCELL", "sync", 0, "YÜKSEK", "Sektör faktörü", "Kısmi IS 0,19 -> OOS 0,40 (artan).", ("TTKOM", "TCELL.IS"), t_stat=p("TTKOM", "TCELL.IS", "c0_t"))
add("TTKOM", "TKC", "Turkcell ADR", "NYSE:TKC", "sync", 0, "YÜKSEK", "Sektör faktörü (TKC = TCELL)", "TCELL üzerinden; gap_l1 t 3,1 işlenemez; TKC parite sapması TTKOM gün-içini tahmin ETMİYOR (BT1 IS -13 bps t -2,9, OOS ~0).", ("TTKOM", "TKC"), t_stat=p("TTKOM", "TKC", "c0_t"))
add("TTKOM", "TRY=X", "USDTRY (hizalı)", "FX:USDTRY", "sync", 0, "DÜŞÜK", "Net döviz borcu / TL gelir", "Kısmi -0,04 (IS -0,10, OOS -0,05; yılların %76'sında negatif). gap_l1 t -3,9 (kapanış sonrası TL zayıflaması -> düşük açılış; işlenemez).", ("TTKOM", "FXAL"), t_stat=p("TTKOM", "FXAL", "c0_t"))
add("TTKOM", "EVENT", f"İmtiyaz 2050'ye uzatıldı (KAP 27.08.2025; 2,5 mrd USD+KDV, 10 yıl)", "BIST:TTKOM", "event", 0, "DÜŞÜK", "Regülasyon/imtiyaz bedeli",
    f"AR (bps) / TCELL r (bps) günlere göre: {ev}; CAR 27.08-03.09: {ev_car} bps. Tek olay.", n=1)
add("TTKOM", "EU_TEL", "Avrupa telekom sepeti", "sepet", "sync", 0, "ÇOK DÜŞÜK", "Küresel telekom faktörü", "Kısmi ~0; dış sürücü beklentisi düşük -> doğrulandı.", ("TTKOM", "EU_TEL"), t_stat=p("TTKOM", "EU_TEL", "c0_t"))
# ---------------- ASELS
add("ASELS", "EU_DEF", "Avrupa savunma sepeti (RHM, BA., LDO, HO, SAAB, KOG, HAG, R3NK)", "sepet: XETR:RHM, LSE:BA., MIL:LDO, EURONEXT:HO, OMXSTO:SAAB_B, OSL:KOG", "regime", 0, "ORTA",
    "2022 sonrası Avrupa yeniden silahlanma teması; ASELS ihracat payı ~%19-25 (teslimat)",
    "Kısmi (XU100): 2014-21 0,02 -> 2022-26 0,13 (XU100+STOXX kontrollü 0,15). Tam dönem 0,06. Lead yok (gap/intra t<1).", ("ASELS", "EU_DEF"), t_stat=p("ASELS", "EU_DEF", "c0_t"))
for d, desc, tv in [("BA.L", "BAE Systems", "LSE:BA."), ("SAAB-B.ST", "Saab", "OMXSTO:SAAB_B"), ("RHM.DE", "Rheinmetall", "XETR:RHM"), ("HO.PA", "Thales", "EURONEXT:HO"), ("LDO.MI", "Leonardo", "MIL:LDO"),
                    ("HAG.DE", "Hensoldt", "XETR:HAG"), ("R3NK.DE", "RENK (2024-02+)", "XETR:R3NK"), ("KOG.OL", "Kongsberg", "OSL:KOG")]:
    fd = S4.loc[("ASELS", d), "fdr_pc"] if ("ASELS", d) in S4.index else False
    add("ASELS", d, desc, tv, "sync", 0, "DÜŞÜK" if not fd else "ORTA", "Avrupa savunma teması", f"Tarama kısmi pc FDR: {'geçti' if fd else 'geçmedi'}; OOS kısmi daha yüksek.", ("ASELS", d), t_stat=p("ASELS", d, "c0_t"))
add("ASELS", "EVENT", "Yeniden silahlanma haber günleri (n=6: Zeitenwende 28.02.22, Oval Ofis 03.03.25, ReArm 04.03.25, Merz 05.03.25, Bundestag 18.03.25, NATO %5 25.06.25)", "XETR:RHM", "event", 0, "ORTA",
    "Avrupa savunma bütçesi -> ihracat beklentisi", "ASELS AR0 ort +357 bps (t 3,3), işaret uyumu %100, CAR0-5 +769 bps. Küçük n, 2025'e yığılmış. Ertesi gün gün-içi (BT3b, tüm olay tipleri n=20) +87 bps, isabet %60 -> zayıf.", n=6, t_stat=3.3)
add("ASELS", "EVENT", "Ukrayna barış haber günleri (n=9: 13.02.25, 12.03.25, 11.08.25, 19.08.25, 19/21/24.11.25, 16.12.25, 29.12.25)", "XETR:RHM", "event", 0, "DÜŞÜK",
    "Barış -> savunma satışı", "ASELS AR0 ort -85 bps (t -1,9), EU_DEF AR0 -264 bps; işaret uyumu %56; CAR0-5 +200 bps (kalıcı değil). Tarihler haberlerden, orta/düşük güven.", n=9, t_stat=-1.92)
add("ASELS", "EVENT", "Savaş başlangıcı günleri (Kırım 03.03.14, işgal 24.02.22, Hamas 09.10.23, İran 15.04.24, İsrail-İran 13.06.25)", "TVC:VIX", "event", 0, "DÜŞÜK",
    "Jeopolitik şok: savunma + / Türkiye risk -", "AR0 ort +318 bps (t 1,4) ama 24.02.2022'de ASELS -%10,5 (taban; XU100 -%8,5; AR -302) sonra 5 günde CAR +1295 bps. Türkiye risk primi savunma temasını gün 0'da bastırabiliyor.", n=5)
add("ASELS", "EU_DEF", "Veri güdümlü EU savunma şok günleri (STOXX'a göre anormal, |z|>3)", "sepet", "event", 0, "ORTA",
    "Aynı gün (senkron) fiyatlama; BIST Avrupa'dan önce kapandığı için ertesi gün etkisi yok", "2022-26: UP n=13 ASELS AR0 +284 bps, DOWN n=10 -181 bps; 2010-21: UP +100, DOWN -23. corr(AR0,z) 0,03 -> 0,16. BT3 (z_(t-1) -> intra) OOS Sh 0,09: İŞLENEMEZ.", n=23)
r2 = bt("BT2a EU_DEF(t-1)->ASELS intra"); add("ASELS", "EU_DEF", "EU savunma t-1 -> ASELS gün-içi", "sepet", "lead_intra", 1, "ÇOK DÜŞÜK", "Yok (bilgi açılışta/senkron)", "Olumsuz bulgu.", t_stat=p("ASELS", "EU_DEF", "intra_l1_t"), bt_oos_sharpe=r2.OOS_sharpe, bt_oos_mean_bps=r2.OOS_mean_bps, n=int(r2.OOS_n + r2.IS_n), intra_corr=p("ASELS", "EU_DEF", "intra_l1"))
r3 = bt("BT2b KR_DEF(t) z>1->ASELS intra")
add("ASELS", "KR_DEF", "Kore savunma sepeti (012450 Hanwha Aero, 064350 Hyundai Rotem, 079550 LIG Nex1, 047810 KAI) — BIST açılışından önce kapanır", "KRX:012450, KRX:064350, KRX:079550, KRX:047810", "lead_intra", 0, "DÜŞÜK",
    "Asya kapanışı BIST öncesi -> açılışta bilinen bilgi", f"lag0->gap t 4,8 ama KS11+ES(t-1) kontrolünde t 1,6 (piyasa geneli); ->intra t 1,9 (kontrollü). BT z>1: OOS {r3.OOS_mean_bps:.1f} bps t {r3.OOS_t:.2f} Sh {r3.OOS_sharpe:.2f}. Senkron kısmi 2024-26 0,12.",
    ("ASELS", "KR_DEF"), t_stat=1.93, bt_oos_sharpe=r3.OOS_sharpe, bt_oos_mean_bps=r3.OOS_mean_bps)
add("ASELS", "US_DEF", "ABD savunma sepeti (LMT, NOC, RTX, GD, LHX); ITA/XAR/PPA benzer", "NYSE:LMT, NYSE:NOC, NYSE:RTX, NYSE:GD, NYSE:LHX, AMEX:XAR, AMEX:PPA, ITA ?", "sync", 0, "DÜŞÜK",
    "Küresel savunma teması (zayıf)", "Kısmi 0,03 (2022-26 0,09). ITA/XAR/PPA gap_l1 t 2,9-3,9 = ABD piyasası eşzamansızlığı (kısmi ~0).", ("ASELS", "US_DEF"), t_stat=p("ASELS", "US_DEF", "c0_t"))
add("ASELS", "ESLT", "Elbit Systems", "NASDAQ:ESLT", "sync", 0, "DÜŞÜK", "Savunma elektroniği emsali", "Kısmi 0,05 (OOS 0,10).", ("ASELS", "ESLT"), t_stat=p("ASELS", "ESLT", "c0_t"))
add("ASELS", "EUAD", "Select STOXX Europe A&D ETF (2024-10+)", "?", "sync", 0, "DÜŞÜK", "Avrupa savunma ETF'i (tek ticker alternatifi)", "Kısa örneklem; kısmi 0,05; intra_l1 t 2,4 (FDR'den geçmez).", ("ASELS", "EUAD"), t_stat=p("ASELS", "EUAD", "c0_t"))
add("ASELS", "CSG.AS", "CSG N.V. (2026-01+)", "EURONEXT:CSG ?", "hypothesis", 0, "ÇOK DÜŞÜK", "Avrupa mühimmat", "~190 gün veri; test edilemez düzeyde kısa.", n=190)
add("ASELS", "OTKAR.IS", "Otokar (yurt içi savunma emsali)", "BIST:OTKAR", "sync", 0, "ORTA", "Türk savunma sanayi teması (SSB ihaleleri)", "Kısmi IS 0,14 -> OOS 0,06 (zayıflıyor).", ("ASELS", "OTKAR.IS"), t_stat=p("ASELS", "OTKAR.IS", "c0_t"))
xb = S4.loc[("ASELS", "XBANK.IS")]
add("ASELS", "XBANK.IS", "BIST Banka endeksi (yurt içi rotasyon)", "BIST:XBANK", "sync", 0, "ORTA", "Banka vs. büyüme/savunma rotasyonu (iç faktör)", f"XU100 kontrollü kısmi {xb.pc_sync:.2f} (t {xb.t_pc:.1f}); dış sürücü değil, faktör.", corr_full=xb.c_sync, pcorr_xu100=xb.pc_sync, t_stat=xb.t_pc, n=int(xb.n))
add("ASELS", "TUR", "iShares MSCI Turkey (ABD) t-1", "NASDAQ:TUR", "lead_gap", 1, "ORTA", "BIST kapanışı sonrası Türkiye haberi -> açılış", "Gap'te fiyatlanır (işlenemez); gün-içi lag1 -0,08 (t -3,2) = gap aşırı tepkisinin dönüşü, FDR'den geçmez.", ("ASELS", "TUR"), t_stat=p("ASELS", "TUR", "gap_l1_t"))
add("ASELS", "RHM.DE (h1)", "EU savunma saatlik getirisi -> ASELS sonraki saat", "XETR:RHM, LSE:BA., MIL:LDO, OMXSTO:SAAB_B", "intraday_minutes", 0, "ÇOK DÜŞÜK", "Gün-içi yayılım hipotezi", "Saatlik senkron 0,03-0,10; sonraki saat öncülüğü t<1,8 (2023-12+). EU post-close (15:00->16:40) -> ASELS ertesi gap t -1,1, gün-içi t 2,3 (BT OOS Sh 0,49, t 0,8).", n=717)
F = pd.DataFrame(rows)
cols = ["stock", "driver_yahoo", "driver_desc", "tv_ticker", "relation", "lag", "corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr", "is_oos", "bt_oos_sharpe", "bt_oos_mean_bps", "n", "confidence", "mechanism", "notes"]
for c in cols:
    if c not in F: F[c] = np.nan
F = F[cols]
for c in ["corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr", "bt_oos_sharpe", "bt_oos_mean_bps"]: F[c] = pd.to_numeric(F[c], errors="coerce").round(3)
F.to_csv(OUT + "/f_savunma.csv", index=False); print("satır:", len(F)); print(F.confidence.value_counts().to_dict())
