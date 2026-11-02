"""A5: f_metal.csv üretimi (res/*.csv'den). Tüm hipotez çiftleri (TL bazı) otomatik güven kuralıyla + elle seçilmiş öncülük/backtest/olay satırları."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mh, pandas as pd, numpy as np
H = pd.read_csv(os.path.join(mh.RES, "hyp_pairs.csv")); A = pd.read_csv(os.path.join(mh.RES, "scan_all.csv"))
B = pd.read_csv(os.path.join(mh.RES, "bt.csv")); N = pd.read_csv(os.path.join(mh.RES, "hourly_night.csv")); L = pd.read_csv(os.path.join(mh.RES, "hourly_leadlag.csv"))
E = pd.read_csv(os.path.join(mh.RES, "events.csv"))
pcrej = A[A.test == "pc"].set_index(["stock", "sym"])["rej"].to_dict()
DOM = {"ISDMR.IS", "KRDMA.IS", "KRDMB.IS", "TRENJ.IS", "EREGL.IS", "KRDMD.IS", "TRALT.IS", "TRMET.IS", "BRSAN.IS", "XUSIN.IS"}
def conf(r):
    pc = r.pcorr_xu100; ok_is = np.sign(r.corr_IS) == np.sign(r.corr_OOS); fd = pcrej.get((r.stock, r.driver), False)
    if (abs(r.corr_full) >= .30 or abs(pc) >= .15) and r.yr_same_sign >= .75 and ok_is and fd: return "YÜKSEK"
    if abs(pc) >= .08 and r.yr_same_sign >= .6 and ok_is and fd: return "ORTA"
    if abs(pc) >= .03 or abs(r.pcorr_weekly) >= .10: return "DÜŞÜK"
    return "ÇOK DÜŞÜK"
rows = []
for _, r in H[~H.usd].iterrows():
    U = H[(H.usd) & (H.stock == r.stock) & (H.driver == r.driver)]
    mech = "aynı yurtiçi çelik/grup faktörü" if r.driver in DOM else "küresel fiyat/emsal faktörü"
    rows.append(dict(stock=r.stock, driver_yahoo=r.driver, driver_desc=r.driver_desc, tv_ticker=mh.tv(r.driver), relation="sync", lag=0,
        corr_full=r.corr_full, corr_3y=r.corr_3y, corr_1y=r.corr_1y, pcorr_xu100=r.pcorr_xu100, beta=r.beta, t_stat=r.t_sync,
        gap_corr=r.gap_corr, intra_corr=r.intra_corr, is_oos=f"IS {r.corr_IS:.2f}/OOS {r.corr_OOS:.2f}", bt_oos_sharpe=np.nan, bt_oos_mean_bps=np.nan,
        n=r.n, confidence=conf(r), mechanism=mech,
        notes=f"haftalık c={r.corr_weekly:.2f} pc={r.pcorr_weekly:.2f}; yıl-işaret={r.yr_same_sign:.2f}; lag1 gap t={r.gap_t:.1f} intra t={r.intra_t:.1f} (IS {r.intra_t_IS:.1f}/OOS {r.intra_t_OOS:.1f}); ters t={r.t_rev:.1f}; USD bazı corr={U.corr_full.iloc[0] if len(U) else np.nan:.2f}; pcFDR={pcrej.get((r.stock, r.driver), 'NA')}"))
def bt(test, target="intra", cost=15, mode="sign0.0"):
    x = B[(B.test == test) & (B.target == target) & (B.cost == cost) & (B["mode"] == mode)].iloc[0]; return x
def nrow(s, d, x, y):
    z = N[(N.stock == s) & (N.driver == d) & (N.x == x) & (N.y == y)]; return z.iloc[0] if len(z) else None
CUR = []
for s in ("TRALT", "TRMET"):
    g = nrow(s, "GC=F", "night", "gap"); i = nrow(s, "GC=F", "night", "intra"); gr = nrow(s, "GC=F", "night", "gap_res")
    CUR.append(dict(stock=s, driver_yahoo="GC=F", driver_desc="Altın gece hareketi (15:00 UTC t-1 -> 06:55 UTC t, saatlik)", tv_ticker="COMEX:GC1!", relation="lead_gap", lag=1,
        corr_full=g["corr"], t_stat=g["t"], gap_corr=g["corr"], intra_corr=i["corr"], n=g["n"], confidence="ORTA",
        mechanism="altın fiyatı BIST kapanışından sonra hareket eder, açılış gap'inde fiyatlanır (İŞLENEBİLİR DEĞİL)",
        notes=f"2023-11+ saatlik; XU100-gap'e göre artık gap corr={gr['corr']:.2f} t={gr['t']:.1f}; intra t={i['t']:.1f} -> gün-içine taşma yok"))
for test, s, d, desc, tvt, rel, lag, cf, mech in [
  ("B1 GC=F(t-1) -> TRALT intra", "TRALT", "GC=F", "Altın t-1 getirisi -> TRALT gün-içi", "COMEX:GC1!", "lead_intra", 1, "ÇOK DÜŞÜK", "olumsuz: altın bilgisi açılışta tamamen fiyatlanıyor"),
  ("B3 JP/AU açılış-öncesi(t) -> EREGL intra", "EREGL", "5411.T+5401.T+6301.T+FMG.AX+BHP.AX", "Japon çelik/makine + Avustralya demir cevheri madencileri (aynı gün, BIST açılışından önce kapanır) z-kompozit", "TSE:5411,TSE:5401,TSE:6301,ASX:FMG,ASX:BHP", "lead_intra", 0, "ORTA", "Asya sabah seansında çelik/cevher talebi haberinin BIST gün-içine yavaş yayılması; yalnız |z|>1 günlerde"),
  ("B3b JP/AU açılış-öncesi(t) -> KRDMD intra", "KRDMD", "5411.T+5401.T+6301.T+FMG.AX+BHP.AX", "aynı kompozit", "TSE:5411,TSE:5401,TSE:6301,ASX:FMG,ASX:BHP", "lead_intra", 0, "ORTA", "aynı"),
  ("B2 AvrupaÇelik(t-1) -> EREGL intra", "EREGL", "MT.AS+SSAB-A.ST+VOE.VI+SZG.DE+AAL.L", "Avrupa çelik/madenci t-1 z-kompozit", "EURONEXT:MT,OMXSTO:SSAB_A,VIE:VOE,XETR:SZG,LSE:AAL", "lead_intra", 1, "DÜŞÜK", "tarama FDR'den geçiyor (t~3.5) ama maliyet sonrası kâr ~0"),
  ("B2b AvrupaÇelik(t-1) -> KRDMD intra", "KRDMD", "MT.AS+SSAB-A.ST+VOE.VI+SZG.DE+AAL.L", "Avrupa çelik/madenci t-1 z-kompozit", "EURONEXT:MT,OMXSTO:SSAB_A,VIE:VOE,XETR:SZG,LSE:AAL", "lead_intra", 1, "DÜŞÜK", "aynı"),
  ("B4 SLX(t-1) -> EREGL intra", "EREGL", "SLX", "ABD çelik ETF t-1", "AMEX:SLX", "lead_intra", 1, "DÜŞÜK", "ABD kapanışı gap'te fiyatlanıyor; gün-içi kalıntı maliyeti karşılamıyor"),
  ("B4b ABDçelik NUE/STLD/CLF/MT(t-1) -> EREGL intra", "EREGL", "NUE+STLD+CLF+MT", "ABD çelikçileri t-1", "NYSE:NUE,NASDAQ:STLD,NYSE:CLF,NYSE:MT", "lead_intra", 1, "ÇOK DÜŞÜK", "olumsuz"),
  ("B5 TS(t-1) -> BRSAN intra", "BRSAN", "TS", "Tenaris t-1", "NYSE:TS", "lead_intra", 1, "ÇOK DÜŞÜK", "olumsuz: BRSAN küresel boru/petrol döngüsünü günlük frekansta izlemiyor"),
  ("B6 TRALT cc(t-1) -> TRMET intra (ters işaret)", "TRMET", "TRALT.IS", "TRALT dünkü getirisi (kontra) -> TRMET gün-içi", "BIST:TRALT", "lead_intra", 1, "DÜŞÜK", "Koza grubu ortak faktöründe gap aşırı tepkisi/geri dönüşü; IS+, OOS-"),
  ("B7 TIO=F(t-1) -> EREGL intra", "EREGL", "TIO=F", "Demir cevheri t-1", "COMEX:TIO1!", "lead_intra", 1, "ÇOK DÜŞÜK", "olumsuz")]:
    best = "z1.0" if test.startswith("B3") else "sign0.0"
    x = bt(test, mode=best); x8 = bt(test, cost=8, mode=best); h = bt(test, target="hedged", mode=best)
    CUR.append(dict(stock=s, driver_yahoo=d, driver_desc=desc, tv_ticker=tvt, relation=rel, lag=lag, is_oos=f"IS {x.IS_mean_bps:.1f}bps t={x.IS_t:.2f} / OOS {x.OOS_mean_bps:.1f}bps t={x.OOS_t:.2f} (15bps, {best})",
        bt_oos_sharpe=x.OOS_sharpe, bt_oos_mean_bps=x.OOS_mean_bps, n=x.IS_n + x.OOS_n, t_stat=x.OOS_t, confidence=cf, mechanism=mech,
        notes=f"8bps: IS {x8.IS_mean_bps:.1f}/OOS {x8.OOS_mean_bps:.1f}; XU100-hedged OOS {h.OOS_mean_bps:.1f}bps t={h.OOS_t:.2f}; yıllar+ {x.yrs_pos}"))
for _, e in E.iterrows():
    CUR.append(dict(stock=e.stock, driver_yahoo="EVENT", driver_desc=e.event, tv_ticker=f"BIST:{e.stock}", relation="event", lag=0, corr_full=np.nan,
        t_stat=e.z_0_20, n=21, confidence="ORTA" if abs(e.z_0_20) >= 2 else "DÜŞÜK", mechanism="yönetim/hukuk/ülke riski olayı",
        notes=f"{e.date}: CAR[-1,+1] {e.car_m1p1_pct:.1f}% CAR[0,+20] vs XU100 {e.car_0_20_pct:.1f}% (ham {e.raw_0_20_pct:.1f}%, altın {e.gold_0_20_pct:.1f}%)"))
for (s, d) in [("TRALT", "GC=F"), ("EREGL", "TKA.DE"), ("EREGL", "SZG.DE"), ("EREGL", "VOE.VI"), ("KRDMD", "TKA.DE"), ("BRSAN", "TEN.MI")]:
    z = L[(L.stock == s) & (L.driver == d)]
    if len(z):
        z = z.iloc[0]
        CUR.append(dict(stock=s, driver_yahoo=d, driver_desc="saatlik gün-içi (BIST seansı içinde)", tv_ticker=mh.tv(d), relation="intraday_minutes", lag=1,
            corr_full=z.c_sync, t_stat=z.t_lead1h, n=z.n, confidence="DÜŞÜK" if abs(z.t_lead1h) >= 2 else "ÇOK DÜŞÜK", mechanism="saatlik öncülük",
            notes=f"aynı saat c={z.c_sync:.2f} t={z.t_sync:.1f}; sürücü 1s önde c={z.c_lead1h:.3f} t={z.t_lead1h:.1f}; hisse 1s önde t={z.t_rev1h:.1f}; 2023-11+ (TRALT 2025-11+)"))
CUR.append(dict(stock="KRDMD", driver_yahoo="Türk hurda ithal fiyatı", driver_desc="HMS 1/2 80:20 CFR Türkiye (Yahoo'da yok)", tv_ticker="? (LME:SC1! LME hurda vadelisi, TV'de olabilir)", relation="hypothesis", lag=0,
    confidence="ÇOK DÜŞÜK", mechanism="DÜZELTME: Kardemir entegre yüksek fırın (cevher+kok) tesisi, hurda bazlı EAF değil; hurda sadece katkı", notes="test edilemedi (veri yok); BUS=F (ABD hurda) zayıf vekil"))
CUR.append(dict(stock="EREGL", driver_yahoo="koklaşabilir kömür", driver_desc="Avustralya HCC (Yahoo'da yok; MTF=F API2 termik kömür 2025-12'de bitiyor)", tv_ticker="? (SGX/CME HCC vadelisi)", relation="hypothesis", lag=0,
    confidence="ÇOK DÜŞÜK", mechanism="entegre üreticilerin girdi maliyeti", notes="test edilemedi; MTF=F sonuçları sync satırında"))
F = pd.DataFrame(rows + CUR)
cols = "stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes".split(",")
F = F.reindex(columns=cols); F.to_csv(os.path.join(mh.OUT, "f_metal.csv"), index=False, float_format="%.4f")
print(F.shape, F.confidence.value_counts().to_dict())
# rapor için kısa özet
k = H[~H.usd].set_index(["stock", "driver"], drop=False)
for s, d in [("TRALT", "GC=F"), ("TRALT", "ONS_TL"), ("TRALT", "TRMET.IS"), ("TRMET", "TRENJ.IS"), ("TRMET", "GC=F"), ("EREGL", "ISDMR.IS"), ("EREGL", "KRDMD.IS"), ("EREGL", "MT.AS"), ("EREGL", "SSAB-A.ST"),
             ("EREGL", "TIO=F"), ("EREGL", "HRC=F"), ("EREGL", "VALE"), ("KRDMD", "EREGL.IS"), ("KRDMD", "TIO=F"), ("KRDMD", "BUS=F"), ("KRDMD", "CMC"), ("BRSAN", "TS"), ("BRSAN", "HRC=F"), ("BRSAN", "CL=F"), ("BRSAN", "TRY=X"), ("TRALT", "TRY=X"), ("EREGL", "TRY=X")]:
    r = k.loc[(s, d)]; print(s, d, f"c={r.corr_full:.2f} c1y={r.corr_1y:.2f} pc={r.pcorr_xu100:.2f} pcw={r.pcorr_weekly:.2f} IS/OOS={r.corr_IS:.2f}/{r.corr_OOS:.2f} yr={r.yr_same_sign:.2f} int_t={r.intra_t:.1f} rev_t={r.t_rev:.1f} conf={conf(r)}")
for c in CUR[:2] + CUR[-14:-8]: print(c["stock"], c["driver_yahoo"][:20], c["relation"], c.get("notes", "")[:150])
x = A[(A.rej) & (A.test.isin(["intra1", "intra0_preopen"]))].sort_values("p").groupby("stock").head(3)
print(x[["stock", "test", "sym", "r", "t"]].round(3).to_string(index=False))
print("B3 z1 hedged/8bps:", [(t, round(bt(t, target='hedged', mode='z1.0').OOS_mean_bps, 1), round(bt(t, target='hedged', mode='z1.0').OOS_t, 2)) for t in ["B3 JP/AU açılış-öncesi(t) -> EREGL intra", "B3b JP/AU açılış-öncesi(t) -> KRDMD intra"]])
