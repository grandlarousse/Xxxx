"""res/*.csv -> out/f_banka.csv (BRIEF formatı) + rapor için kilit rakamların kısa dökümü."""
import bk, numpy as np, pandas as pd, json
RS = bk.RES
TV = {"BBVA.MC": "BME:BBVA", "BBVA": "NYSE:BBVA", "SAN.MC": "BME:SAN", "UCG.MI": "MIL:UCG", "ISP.MI": "MIL:ISP", "BNP.PA": "EURONEXT:BNP", "DBK.DE": "XETR:DBK",
      "EUFN": "NASDAQ:EUFN", "KBE": "AMEX:KBE", "KRE": "AMEX:KRE", "XLF": "AMEX:XLF", "ETE.AT": "ATHEX:ETE", "EUROB.AT": "ATHEX:EUROB", "TPEIR.AT": "ATHEX:TPEIR",
      "ALBKY": "OTC:ALBKY (alt ATHEX:ALPHA)", "PKO.WA": "GPW:PKO", "PEO.WA": "GPW:PEO", "OTP.BD": "BET:OTP ?", "SBK.JO": "JSE:SBK", "FSR.JO": "JSE:FSR", "ITUB": "NYSE:ITUB",
      "BBD": "NYSE:BBD", "TUR": "NASDAQ:TUR", "AKBTY": "OTC:AKBTY", "TKGBY": "OTC:TKGBY", "^TNX": "TVC:US10Y", "^FVX": "TVC:US05Y", "2YY=F": "CBOT:2YY1! / TVC:US02Y",
      "^IRX": "TVC:US03MY", "DX-Y.NYB": "TVC:DXY", "^VIX": "CBOE:VIX", "^MOVE": "TVC:MOVE ?", "EMB": "NASDAQ:EMB", "EMLC": "AMEX:EMLC", "HYG": "AMEX:HYG", "TLT": "NASDAQ:TLT",
      "CEW": "AMEX:CEW", "EEM": "AMEX:EEM", "ZAR=X": "FX:USDZAR", "BRL=X": "FX_IDC:USDBRL", "MXN=X": "FX:USDMXN", "HUF=X": "FX:USDHUF", "PLN=X": "FX:USDPLN",
      "TRY=X": "FX:USDTRY", "EURTRY=X": "FX:EURTRY", "EURUSD=X": "FX:EURUSD", "GC=F": "COMEX:GC1!", "BZ=F": "ICEEUR:BRN1!", "CL=F": "NYMEX:CL1!", "ES=F": "CME_MINI:ES1!",
      "^STOXX50E": "TVC:SX5E", "^GDAXI": "XETR:DAX", "GD.AT": "ATHEX:GD ?", "EZA": "AMEX:EZA", "EWZ": "AMEX:EWZ", "EPOL": "AMEX:EPOL", "GREK": "AMEX:GREK"}
COLS = "stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes".split(",")
MECH = {"bank_eu": "küresel banka/risk faktörü; Türk bankalarına yalnız piyasa (XU100) kanalıyla", "fx": "EM kur/risk iştahı", "rate": "küresel faiz", "tr": "aynı Türkiye riski (ABD'de işlem gören)"}
H = pd.read_csv(RS + "/hyp.csv")
rows = []
def lab(o):
    pcv = abs(o.pcorr_xu100) if pd.notna(o.pcorr_xu100) else 0
    big = abs(o.corr_full) >= 0.30 or pcv >= 0.15
    same = np.sign(o.is_corr) == np.sign(o.oos_corr) == np.sign(o.corr_full)
    pcs = np.sign(o.is_pc) == np.sign(o.oos_pc) and abs(o.oos_pc) >= 0.05
    if pcv >= 0.15 and pcs and o.yr_same_sign >= 0.75: return "YÜKSEK"
    if big and same and o.yr_same_sign >= 0.75: return "ORTA (sadece piyasa kanalı)" if pcv < 0.05 else "ORTA"
    if same and abs(o.sync_t) >= 3: return "DÜŞÜK (sadece piyasa kanalı)" if pcv < 0.05 else "DÜŞÜK"
    return "ÇOK DÜŞÜK"
for o in H.itertuples():
    rows.append(dict(stock=o.stock, driver_yahoo=o.driver, driver_desc=o.desc, tv_ticker=TV.get(o.driver, "?"), relation="sync", lag=0, corr_full=o.corr_full, corr_3y=o.corr_3y,
                     corr_1y=o.corr_1y, pcorr_xu100=o.pcorr_xu100, beta=o.beta, t_stat=o.sync_t, gap_corr=o.gap_corr, intra_corr=o.intra_corr,
                     is_oos=f"IS c={o.is_corr:.2f}/pc={o.is_pc:.2f}; OOS c={o.oos_corr:.2f}/pc={o.oos_pc:.2f}", bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan, n=o.n,
                     confidence=lab(o), mechanism="", notes=f"lag1->gap t={o.gap_t:.1f} (gap|XU100gap pc={o.gap_pc_xugap:.2f}); lag1->intra t={o.intra_t:.1f} (IS {o.intra_is_t:.1f}/OOS {o.intra_oos_t:.1f}); ters t={o.rev_t:.1f}; yıl-işaret={o.yr_same_sign:.2f}; FX ll.FX_FIX düzeltmeli"))
# saatlik lead_gap / lead_intra
HT = pd.read_csv(RS + "/hourly_tests.csv")
sigdesc = {"TUR_post": ("TUR", "TUR 15:30 UTC->ABD kapanışı (BIST kapanışı sonrası)", "NASDAQ:TUR"), "ES_ovn": ("ES=F", "ES 15:00->06:00 UTC gece", "CME_MINI:ES1!"),
           "ES_post": ("ES=F", "ES 15:00->21:00 UTC", "CME_MINI:ES1!"), "BBVA_post": ("BBVA", "BBVA ADR 15:30->ABD kapanışı", "NYSE:BBVA"), "EEM_post": ("EEM", "EEM 15:30->ABD kapanışı", "AMEX:EEM"),
           "USDTRY_ovn": ("TRY=X", "USDTRY 15:00->06:00 UTC gece", "FX:USDTRY")}
for o in HT.itertuples():
    if o.stock not in bk.ALL: continue
    y, dsc, tv = sigdesc[o.signal]
    g = HT[(HT.stock == o.stock) & (HT.signal == o.signal) & (HT.target == "intra")]
    if o.target != "gap": continue
    gi = g.iloc[0]
    conf = "YÜKSEK (açılışta fiyatlanır; spot'ta işlenemez)" if abs(o.t) >= 3 and np.sign(o.h1_corr) == np.sign(o.h2_corr) and abs(o.corr) >= 0.15 else ("ORTA" if abs(o.t) >= 2.5 else "DÜŞÜK")
    rows.append(dict(stock=o.stock, driver_yahoo=y, driver_desc=dsc, tv_ticker=tv, relation="lead_gap", lag=1, corr_full=o.corr, gap_corr=o.corr, intra_corr=gi["corr"], beta=o.beta, t_stat=o.t, n=o.n,
                     is_oos=f"1.yarı c={o.h1_corr:.2f} t={o.h1_t:.1f}; 2.yarı c={o.h2_corr:.2f} t={o.h2_t:.1f}", confidence=conf,
                     mechanism="BIST kapalıyken gelen ABD seansı/gece bilgisi ertesi açılışta fiyatlanıyor (eşzamansız kapanış)",
                     notes=f"saatlik 2023-12+; gün-içi (açılış->kapanış) etkisi corr={gi['corr']:.3f} t={gi['t']:.1f} => devam/ters dönüş YOK. XLBNK endeks vadelisi akşam seansında (16:00-20:00 UTC) işlenebilir olabilir - test edilmedi (veri yok)"))
# backtestler
B = pd.read_csv(RS + "/backtests.csv")
for o in B[B.cost.isin([10, 20])].itertuples():
    if "BT3x" in o.bt and o.cost != 20: continue
    if "BT3x" not in o.bt and o.cost != 10: continue
    g = B[(B.bt == o.bt) & (B.stock == o.stock) & (B.cost == 0)].iloc[0]
    rows.append(dict(stock=o.stock, driver_yahoo=o.bt, driver_desc="backtest", tv_ticker="", relation="lead_intra", lag=1, t_stat=o.OOS_t, is_oos=f"IS net {o.IS_mean_bps:.1f}bps t={o.IS_t:.1f} SR={o.IS_sharpe:.2f}; OOS brüt {g.OOS_mean_bps:.1f}bps",
                     bt_oos_sharpe=o.OOS_sharpe, bt_oos_mean_bps=o.OOS_mean_bps, n=o.OOS_n, confidence="ÇOK DÜŞÜK (backtest başarısız)" if not (o.OOS_sharpe > 0.5 and o.IS_sharpe > 0.5) else "DÜŞÜK",
                     mechanism="", notes=f"maliyet {o.cost}bps; yön IS'ten={o.dir}; {o.note if isinstance(o.note, str) else ''}"))
# rejim / olay / hipotez (elle; rakamlar res/ dosyalarından)
TRG = pd.read_csv(RS + "/try_regimes.csv").set_index("period")
for p in TRG.index:
    r = TRG.loc[p]
    rows.append(dict(stock="XBANK", driver_yahoo="TRY=X", driver_desc=f"USDTRY rejim: {p}", tv_ticker="FX:USDTRY", relation="regime", lag=0, corr_full=r["corr"], pcorr_xu100=r["pc_xu100"],
                     beta=r["beta_TRY|XU"], t_stat=r["t"], n=r["n"], confidence="", mechanism="TL değer kaybı -> banka özkaynak/sermaye yeterliliği (YP aktif risk ağırlığı), fonlama maliyeti, yabancı çıkışı",
                     notes=f"TRY günlük sd={r['TRY_sd_bps']:.0f}bps; işaret hiçbir rejimde pozitife dönmüyor, büyüklük değişiyor"))
EVN = pd.read_csv(RS + "/events.csv")
for o in EVN.itertuples():
    rows.append(dict(stock=o.stock, driver_yahoo="EVENT", driver_desc=o.event, tv_ticker=f"BIST:{o.stock}", relation="event", lag=0, corr_full=np.nan, t_stat=o.t0, n=1,
                     is_oos=o.date, confidence="DÜŞÜK (tek olay)", mechanism="", notes=f"AR0={o.CAR0_pct:.2f}% CAR0-2={o.CAR0_2_pct:.2f}% CAR0-5={o.CAR0_5_pct:.2f}% (ham {o.raw0_pct:.2f}%, bench {o.bench0_pct:.2f}%)"))
SH = pd.read_csv(RS + "/shift_2026.csv")
for o in SH[SH.period == "2025-11..2026-10"].itertuples():
    rows.append(dict(stock="XBANK", driver_yahoo=o.driver, driver_desc="2025-11..2026-10 kısmi corr kayması", tv_ticker=TV.get(o.driver, "?"), relation="regime", lag=0, corr_1y=o.corr, pcorr_xu100=o.pc_xu, n=o.n,
                     is_oos="2021-2024 pc=" + str(SH[(SH.driver == o.driver) & (SH.period == "2021-2024")].pc_xu.values[0]), confidence="DÜŞÜK (kısa örneklem, yeni rejim)" if abs(o.pc_xu) >= 0.15 else "ÇOK DÜŞÜK",
                     mechanism="2026: bankalar XU100'ün ötesinde küresel risk/petrol (İran savaşı?) faktörüne bağlandı", notes=f"winsorize pc={o.pc_xu_wins}; TRY de kontrollü pc={o.pc_xu_try}"))
hyp = [("XBANK", "TR CDS 5Y", "Türkiye 5y CDS", "? (TV'de CDS yok gibi; aday: TVC:TR10Y, TVC:TR02Y faiz)", "Yahoo/stooq/FRED'de günlük seri bulunamadı (stooq JS duvarı, FRED sadece aylık OECD). Proxy: TUR/EMB/USDTRY - DÜŞÜK GÜVEN"),
       ("XBANK", "TR 2Y faiz", "TL 2 yıllık gösterge faiz", "TVC:TR02Y ?", "Veri yok; TCMB EVDS API anahtarı gerektirir. Test edilmedi."),
       ("XBANK", "XLBNK1! akşam", "VİOP XLBNK vadelisi akşam seansı (19:00-23:00 TSİ)", "BIST:XLBNK1! ?", "TUR_post bilgisinin akşam seansında fiyatlanıp fiyatlanmadığı test edilemedi (vadeli tick verisi yok)"),
       ("HALKB", "TCMB PPK", "TCMB faiz kararları / BDDK düzenlemeleri", "", "Sistematik PPK tarihli olay çalışması yapılmadı (sadece 2023-06-22 tek olay)")]
for st, d, desc, tv, note in hyp:
    rows.append(dict(stock=st, driver_yahoo=d, driver_desc=desc, tv_ticker=tv, relation="hypothesis", lag=np.nan, confidence="ÇOK DÜŞÜK / SPEKÜLATİF", mechanism="", notes=note))
F = pd.DataFrame(rows).reindex(columns=COLS)
for c in ["corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr", "bt_oos_sharpe", "bt_oos_mean_bps"]:
    F[c] = pd.to_numeric(F[c], errors="coerce").round(3)
F.to_csv(bk.OUT + "/f_banka.csv", index=False)
print("f_banka satır:", len(F), F.relation.value_counts().to_dict())
# ---- kilit rakamlar
pd.set_option("display.width", 230)
k = H[H.stock == "XBANK"].set_index("driver")
print(k.loc[["TUR", "TRY=X", "BBVA.MC", "AKBTY", "TKGBY", "^VIX", "MXN=X", "^MOVE", "GC=F", "BZ=F", "EMB", "SAN.MC"], ["corr_full", "corr_1y", "pcorr_xu100", "is_pc", "oos_pc", "yr_same_sign", "gap_t", "intra_t", "intra_oos_t", "rev_t"]].round(2).to_string())
print(open(RS + "/02_scan.log").read()[-600:])
print(HT[(HT.stock == "XBANK")].round(3).to_string(index=False))
print(B[(B.cost == 0) | (B.cost == 10)].groupby(["bt", "cost"])[["OOS_mean_bps", "OOS_sharpe", "IS_mean_bps"]].median().round(1).to_string())
print(pd.read_csv(RS + "/garan_bbva.csv").round(3).to_string(index=False))
print(TRG.round(3).to_string())
print(EVN[["stock", "date", "CAR0_pct", "t0", "CAR0_2_pct"]].to_string(index=False))
print(pd.read_csv(RS + "/state_spread_drivers.csv").to_string(index=False))
