"""results/*.csv -> out/f_gunici.csv (ortak format)."""
import numpy as np, pandas as pd, g_common as g
R = g.RES; rows = []
DESC = {"ES=F": "S&P500 e-mini vadeli", "NQ=F": "Nasdaq100 vadeli", "BZ=F": "Brent vadeli", "GC=F": "Altın vadeli", "TRY=X": "USD/TRY", "EURTRY=X": "EUR/TRY",
        "TUR": "iShares MSCI Turkey ETF (gölge BIST)", "TKC": "Turkcell ADR", "EEM": "MSCI EM ETF", "^GDAXI": "DAX (15:00->Avrupa kapanışı)", "^STOXX": "Stoxx600 (15:00->kapanış)", "BTC-USD": "Bitcoin"}
COLS = "stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes".split(",")
def add(**k): rows.append({c: k.get(c, np.nan) for c in COLS})
# 1) gece sürücüsü -> açılış gap'i (işlenemez) + gün-içi
A = pd.read_csv(R + "/t1_absorb.csv")
rej, padj = g.ll.fdr(g.ll.t_to_p(A["t_gap"].values)); A["fdr"] = rej
reji, _ = g.ll.fdr(g.ll.t_to_p(A["t_intra"].values)); A["fdr_i"] = reji
for _, r in A.iterrows():
    same = np.sign(r.corr_gap_IS) == np.sign(r.corr_gap_OOS) and min(abs(r.corr_gap_IS), abs(r.corr_gap_OOS)) >= 0.10
    if abs(r.t_gap) >= 5 and same and r.fdr and abs(r.corr_gap) >= 0.30: conf = "YÜKSEK"
    elif abs(r.t_gap) >= 3 and same and r.fdr: conf = "ORTA"
    elif abs(r.t_gap) >= 2: conf = "DÜŞÜK"
    else: conf = "ÇOK DÜŞÜK"
    if r.driver == "BZ=F" and not same: conf = "DÜŞÜK"
    add(stock=r.stock, driver_yahoo=r.driver, driver_desc=DESC.get(r.driver, ""), tv_ticker=g.tvb(r.driver), relation="lead_gap", lag="gece(15:00->07:00 UTC)",
        corr_full=round(r.corr_gap, 3), corr_1y=round(r.corr_gap_1y, 3), beta=round(r.beta_gap, 3), t_stat=round(r.t_gap, 2), gap_corr=round(r.corr_gap, 3), intra_corr=round(r.corr_intra, 3),
        is_oos=f"IS(<2025-07) {r.corr_gap_IS:.2f} / OOS {r.corr_gap_OOS:.2f}", n=r.n, confidence=conf,
        mechanism="BIST kapalıyken gelen küresel bilgi açılış müzayedesinde fiyatlanır",
        notes=f"İŞLENEMEZ (pay vadelisi akşam seansında yok). gün-içi t={r.t_intra:.2f}{' FDR-geçer' if r.fdr_i else ''}; ilk1,5s c={r.corr_r1:.2f}, 08:30->kapanış c={r.corr_rest:.2f}; R2={r.r2:.3f}")
# 2) ortak model R2 + devam/dönüş + backtest
J = pd.read_csv(R + "/t1_joint.csv").set_index("stock"); C = pd.read_csv(R + "/t1_cont.csv").set_index("stock")
BT = pd.read_csv(R + "/t1_bt.csv")
def bt(st, strat, cost=8.0, thr=0.0):
    x = BT[(BT.stock == st) & (BT.strat == strat) & (BT.cost_bps == cost) & (BT.thr_sd == thr)].set_index("period")
    return x
for st in C.index:
    c = C.loc[st]; j = J.loc[st] if st in J.index else None
    b = bt(st, "ghat_cont_0730"); bo = b.loc["OOS"] if "OOS" in b.index else None
    add(stock=st, driver_yahoo="ES=F+BZ=F+GC=F+TRY=X+TUR+^GDAXI", driver_desc="gece sürücü sepeti (genişleyen OLS tahmini gap)", tv_ticker="çoklu", relation="lead_intra", lag="gece->gün-içi",
        corr_full=round(c.c_r_0730_close_ghat, 3), t_stat=round(c.t_r_0730_close_ghat, 2), gap_corr=round(np.sqrt(j.r2_joint), 3) if j is not None else np.nan, intra_corr=round(c.c_intra_ghat, 3),
        is_oos=f"bt8bps IS {b.loc['IS','mean_bps']:.1f} / OOS {bo.mean_bps:.1f} bps" if bo is not None else "", bt_oos_sharpe=round(bo.sharpe, 2) if bo is not None else np.nan,
        bt_oos_mean_bps=round(bo.mean_bps, 1) if bo is not None else np.nan, n=int(c.n), confidence="DÜŞÜK" if abs(c.t_r_0730_close_ghat) >= 2 else "ÇOK DÜŞÜK",
        mechanism="açılışın gece bilgisine eksik tepki vermesi (devam) hipotezi",
        notes=f"ortak R2(gap)={j.r2_joint:.3f}" + (f", +BTC R2={j.r2_joint_btc:.3f}" if j is not None else "") + "; giriş 07:30, çıkış kapanış; IS'te var OOS'ta kayboluyor")
    b = bt(st, "resid_rev_open"); bo = b.loc["OOS"] if "OOS" in b.index else None
    add(stock=st, driver_yahoo="gap kalıntısı (gap - tahmin)", driver_desc="açıklanamayan gap kısmı", tv_ticker=g.tvb(st), relation="lead_intra", lag="açılış->ilk 30dk",
        corr_full=round(c.c_r30_resid, 3), t_stat=round(c.t_r30_resid, 2), intra_corr=round(c.c_intra_resid, 3), gap_corr=np.nan,
        is_oos=f"c(07:30->kapanış, kalıntı)={c.c_r_0730_close_resid:.2f} t={c.t_r_0730_close_resid:.2f}", bt_oos_sharpe=round(bo.sharpe, 2) if bo is not None else np.nan,
        bt_oos_mean_bps=round(bo.mean_bps, 1) if bo is not None else np.nan, n=int(c.n),
        confidence="DÜŞÜK" if c.t_r30_resid <= -2 else "ÇOK DÜŞÜK", mechanism="açılış müzayedesi aşırı tepkisi/gürültüsü ilk 30 dakikada düzelir",
        notes="dönüş büyük ölçüde ilk 30 dk'da; 07:30 sonrası kalıntı yok. Açılış fiyatından işlem gerekir (müzayede), maliyet sonrası zayıf")
    b = bt(st, "short_open_cover_close", cost=8.0); bo = b.loc["OOS"] if "OOS" in b.index else None
    add(stock=st, driver_yahoo="(yok) açılış->kapanış", driver_desc="gece/gün-içi ayrışması: gap ortalaması >0, gün-içi <0", tv_ticker=g.tvb(st), relation="regime", lag="gün-içi",
        corr_full=np.nan, t_stat=np.nan, is_oos=f"bt8bps IS {b.loc['IS','mean_bps']:.1f} / OOS {bo.mean_bps:.1f} bps" if bo is not None else "", bt_oos_sharpe=round(bo.sharpe, 2) if bo is not None else np.nan,
        bt_oos_mean_bps=round(bo.mean_bps, 1) if bo is not None else np.nan, n=int(c.n), confidence="ORTA" if st in ("XU030", "XU100") else "DÜŞÜK",
        mechanism="gece risk primi / açılış müzayedesinde alım baskısı", notes=f"h1 dönemi ort. gap {c.mean_gap_bps:.1f} bps, gün-içi {c.mean_intra_bps:.1f} bps; uzun örneklem 2014-2026 t1b_drift.csv (XU030 gün-içi 11/13 yıl negatif)")
# 3) akşam seansı pencereleri (ES alt pencereleri) + TUR/TKC/DAX kısmi
Wn = pd.read_csv(R + "/t1_windows.csv")
for _, r in Wn.iterrows():
    add(stock=r.stock, driver_yahoo="ES=F (15-16 / 16-20 / 20-07 UTC)", driver_desc="ES gece alt pencereleri", tv_ticker="CME_MINI:ES1!", relation="lead_gap", lag="w1/w2/w3",
        corr_full=np.nan, beta=f"{r.b_w1:.2f}/{r.b_w2:.2f}/{r.b_w3:.2f}", t_stat=f"{r.t_w1:.1f}/{r.t_w2:.1f}/{r.t_w3:.1f}", n=r.n,
        confidence="ORTA" if r.stock in g.IDX else "DÜŞÜK", mechanism="VİOP akşam seansı (16-20 UTC) sadece endeks vadelisinde; w3 bilgisi hiçbir TR piyasasında işlenemez",
        notes=f"R2 w1+w2={r.r2_w12_only:.3f}, w3={r.r2_w3_only:.3f}, hepsi={r.r2_all:.3f}; kısmi(TUR|ES)={r.pc_TUR_given_ES:.3f}; kısmi(TKC|ES,TUR)={r.pc_TKC_given_ES_TUR:.3f}; kısmi(DAX kalan|ES)={r.pc_DAXrem_given_ES:.3f}")
# 4) 5 dk
DL = pd.read_csv(R + "/t2_distlag.csv"); CC = pd.read_csv(R + "/t2_ccf.csv"); B2 = pd.read_csv(R + "/t2_bt.csv")
for _, r in DL[(DL.window.isin(["all", "USopen"]))].iterrows():
    c0 = CC[(CC.stock == r.stock) & (CC.driver == r.driver) & (CC.window == r.window) & (CC.lag == 0)]["corr"]
    c1 = CC[(CC.stock == r.stock) & (CC.driver == r.driver) & (CC.window == r.window) & (CC.lag == 1)]["corr"]
    bb = B2[(B2.stock == r.stock) & (B2.h == 3) & (B2.z == 2.0) & (B2.window == r.window) & (B2.period == "H2")] if r.driver == "ES=F" else pd.DataFrame()
    add(stock=r.stock, driver_yahoo=r.driver, driver_desc=DESC.get(r.driver, "") + " 5dk", tv_ticker=g.tvb(r.driver), relation="intraday_minutes", lag="0..6 bar (5dk)",
        corr_full=round(c0.iloc[0], 3) if len(c0) else np.nan, beta=round(r.b0, 3), t_stat=round(r.t_sum_b1_6, 2), gap_corr=np.nan, intra_corr=round(c1.iloc[0], 3) if len(c1) else np.nan,
        is_oos=f"pencere={r.window}; lag1 t={r.t1:.2f}; gecikmeli pay={r.delayed_share:.2f}",
        bt_oos_mean_bps=round(bb.gross_bps.iloc[0] - 8, 1) if len(bb) else np.nan, n=r.n,
        confidence="ÇOK DÜŞÜK" if abs(r.t_sum_b1_6) < 2 else "DÜŞÜK", mechanism="BIST'in ABD vadelisine dakikalar mertebesinde gecikmeli tepkisi (hipotez)",
        notes="lag0 eşzamanlı ilişki var; lag1..6 toplamı anlamsız -> işlenebilir gecikme YOK. ~50 gün örneklem. corr_full=lag0, intra_corr=lag1 korelasyonu, t_stat=lag1-6 toplam t; bt=ES şoku(2σ) 15dk tut, 8bps sonrası (2. yarı)")
# 5) Asya
AS = pd.read_csv(R + "/t4_asia.csv")
AD = {"HSI_late": ("^HSI", "HSI 07:30->kapanış (BIST açılışından sonra)"), "HSI_day": ("^HSI", "HSI gün getirisi"), "HSI_to0730": ("^HSI", "HSI önceki kapanış->07:30"),
      "^N225_day": ("^N225", "Nikkei gün getirisi (06:30 UTC kapanış)"), "^KS11_day": ("^KS11", "KOSPI gün getirisi"), "000001.SS_day": ("000001.SS", "Şanghay Bileşik gün getirisi (07:00 UTC)"),
      "CNH_0700_0830": ("CNH=X", "USD/CNH 07:00->08:30"), "ES_0700_0830": ("ES=F", "ES 07:00->08:30 (kontrol)")}
for _, r in AS.iterrows():
    y, dsc = AD[r.signal]; tradable = r.target != "gap"
    conf = ("ORTA" if (abs(r.t) >= 3 and np.sign(r.c_IS) == np.sign(r.c_OOS)) else "DÜŞÜK" if abs(r.t) >= 2 else "ÇOK DÜŞÜK")
    add(stock=r.stock, driver_yahoo=y, driver_desc=dsc, tv_ticker=g.tvb(y), relation="lead_gap" if r.target == "gap" else "lead_intra", lag=f"aynı gün -> {r.target}",
        corr_full=round(r["corr"], 3), t_stat=round(r.t, 2), gap_corr=round(r["corr"], 3) if r.target == "gap" else np.nan, intra_corr=round(r["corr"], 3) if r.target != "gap" else np.nan,
        pcorr_xu100=np.nan, is_oos=f"IS {r.c_IS:.2f} / OOS {r.c_OOS:.2f}; kısmi(|ES 07-08:30)={r.pc_given_ES0830:.3f}" if r.target == "rest" else f"IS {r.c_IS:.2f} / OOS {r.c_OOS:.2f}",
        bt_oos_mean_bps=round(r.bt_OOS_bps, 1) if tradable else np.nan, n=r.n, confidence=conf if tradable else (conf if conf != "ORTA" else "ORTA"),
        mechanism="Asya kapanışı BIST açılışından önce/başında; gap'te fiyatlanır" if r.target == "gap" else "Asya'nın BIST açılışı sonrası kısmının gün-içi öngörüsü",
        notes=("İŞLENEMEZ (gap); ES ile büyük ölçüde örtüşür" if r.target == "gap" else "brüt, maliyetsiz OOS bps") + ("; Çin borsası TV'de açılmıyor: alternatif FX:USDCNH, AMEX:ASHR/FXI (ABD saatinde), SGX:CN1!?" if y == "000001.SS" else "") + ("; HKEX TV'de açılmayabilir" if y == "^HSI" else ""))
# 6) hafta sonu BTC
H = pd.read_csv(R + "/t6_weekend.csv")
for _, r in H.iterrows():
    add(stock=r.stock, driver_yahoo="BTC-USD", driver_desc="BTC hafta sonu getirisi (Cuma->Pazartesi)", tv_ticker=g.tvb("BTC-USD"), relation="event", lag="hafta sonu -> Pazartesi gap",
        corr_full=round(r.c_gap_long, 3), corr_3y=round(r.c_gap_2021p, 3), corr_1y=np.nan, beta=round(r.beta_gap_long, 3), t_stat=round(r.t_gap_long, 2), gap_corr=round(r.c_gap_wkend_h1, 3), intra_corr=round(r.c_intra_long, 3),
        is_oos=f"2015-20 {r.c_gap_pre2021:.2f} / 2021+ {r.c_gap_2021p:.2f}", bt_oos_mean_bps=round(r.bt_intra_long_bps, 1), n=int(r.n_long),
        confidence="DÜŞÜK" if (r.c_gap_2021p > 0.15 and r.t_gap_long > 2) else "ÇOK DÜŞÜK", mechanism="bireysel yatırımcı risk iştahı / genel risk duyarlılığı; hafta sonu tek açık risk varlığı BTC",
        notes=f"h1 (2024-11+, n={r.n_h1_wkend}) hafta sonu c={r.c_gap_wkend_h1:.2f} vs hafta içi gece c={r.c_gap_weekday_h1:.2f} -> hafta sonuna özgü değil; gün-içi devam yok; İŞLENEMEZ (gap); bt=sign(BTC)*Pazartesi gün-içi")
F = pd.DataFrame(rows)[COLS]; F.to_csv(g.OUT + "/f_gunici.csv", index=False)
print(len(F), F.relation.value_counts().to_dict(), F.confidence.value_counts().to_dict())
print("FDR lead_gap tests", len(A), "pass", int(A.fdr.sum()), "intra pass", int(A.fdr_i.sum()))
print(A[A.fdr_i][["stock", "driver", "corr_intra", "t_intra"]].round(3).to_string(index=False))
