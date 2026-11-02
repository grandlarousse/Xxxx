"""A7: a6 sonuçlarını f_metal.csv'ye ekler (a5 çıktısının üstüne; a5 -> a7 sırasıyla çalıştır)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mh, pandas as pd, numpy as np
R = lambda n: pd.read_csv(os.path.join(mh.RES, n))
F = pd.read_csv(os.path.join(mh.OUT, "f_metal.csv"))
A = R("scan_all.csv"); L = R("x_lead.csv"); XB = R("x_bt.csv"); M = R("x_monthly.csv"); G = R("x_m5_leadlag.csv"); E2 = R("x_events2.csv"); NB = R("x_night_bt.csv"); TM = R("x_turkey_miners.csv")
REG = R("x_reg.csv")
# h1 'intraday_minutes' satırları: hizalama artefaktı notu
m = F.relation == "intraday_minutes"
F.loc[m, "notes"] = F.loc[m, "notes"].astype(str) + " | UYARI: h1 BIST barları :30, sürücü barları :00'da biter -> 'hisse önde' sonucu ARTEFAKT; m5 30-dk tam hizalı satırlara bak"
F.loc[m, "confidence"] = "ÇOK DÜŞÜK"
# TIO=F satırları: ay sonu/roll notu
m = F.driver_yahoo == "TIO=F"
F.loc[m, "notes"] = F.loc[m, "notes"].astype(str) + " | TIO=F (TIO1!) aylık ortalama kontrat: ay son 3 gün sd 34bps vs ay ortası 115bps; ayın ilk 2 günü roll sıçraması (sd 418bps, %12'si >4sd). Ay ortası alt-örneklemde EREGL pc 0,106 (tüm 0,075). TV'de COMEX:TIO2! / SGX:FEF2! (2. ay) tercih et"
rows = []
def bt(test, target_suffix="", mode="sign0.0", cost=15):
    x = XB[(XB.test == test + target_suffix) & (XB["mode"] == mode) & (XB.cost == cost)]; return x.iloc[0] if len(x) else None
def scan_rej(stock, sym):
    x = A[(A.stock == stock) & (A.test == "intra0_preopen") & (A.sym == sym)]; return bool(x.rej.iloc[0]) if len(x) else None
for st, conf in [("EREGL", "YÜKSEK"), ("KRDMD", "YÜKSEK"), ("BRSAN", "ORTA"), ("TRALT", "ÇOK DÜŞÜK"), ("TRMET", "DÜŞÜK"), ("XU100", "ORTA")]:
    l = L[(L.stock == st) & (L.signal == "FMG.AX lag0")].iloc[0]
    b = bt(f"A FMG.AX(t) -> {st} intra") if st in ("EREGL", "KRDMD", "BRSAN") else None
    bz = bt(f"A FMG.AX(t) -> {st} intra", mode="z1.0") if b is not None else None
    rg = REG[(REG.stock == st) & REG.signal.isna()] if st in ("EREGL", "KRDMD", "BRSAN") else pd.DataFrame()
    rows.append(dict(stock=st, driver_yahoo="FMG.AX", driver_desc="Fortescue (ASX; kapanış 05:00-06:00 UTC, BIST açılışından önce) AYNI GÜN getirisi", tv_ticker="ASX:FMG", relation="lead_intra", lag=0,
        corr_full=l.c_intra, t_stat=l.t_intra, gap_corr=l.c_gap, intra_corr=l.c_intra, is_oos=f"IS t={l.t_IS:.2f} / OOS t={l.t_OOS:.2f}", n=l.n,
        bt_oos_sharpe=b.OOS_sharpe if b is not None else np.nan, bt_oos_mean_bps=b.OOS_mean_bps if b is not None else np.nan, confidence=conf,
        mechanism="Asya seansında (ABD kapanışından sonra) gelen Çin çelik/cevher haberi; BIST çeliğine açılışta tam yansımıyor, gün içinde yayılıyor (yavaş difüzyon)",
        notes=(f"XU100-hedged t={l.t_hedged:.2f}; kârlı yıl payı {l.yr_pos_share:.2f}; " + (f"SLX/ES/MT.AS t-1 ve gap_t kontrollü t={rg['t_FMG_t'].iloc[0]:.2f}; " if len(rg) else "") +
               (f"bt 15bps işaret IS {b.IS_mean_bps:.1f}/OOS {b.OOS_mean_bps:.1f} bps; |z|>1 IS {bz.IS_mean_bps:.1f}/OOS {bz.OOS_mean_bps:.1f} bps (t {bz.OOS_t:.2f}); " if b is not None else "") +
               f"önceden belirlenmiş hipotez (veri madenciliği değil); tarama FDR={scan_rej(st if st!='XU100' else 'EREGL','FMG.AX')}; Çin ajanı bulgusunu bağımsız doğrular; korelasyon küçük (0,05-0,08) -> maliyete duyarlı")))
for code, nm in [("HRC", "SHFE HRC"), ("RB", "SHFE inşaat demiri"), ("I", "DCE demir cevheri")]:
    for st in ("KRDMD", "EREGL"):
        l0 = L[(L.stock == st) & (L.signal.str.startswith(nm)) & (L.signal.str.contains("lag0"))].iloc[0]; l1 = L[(L.stock == st) & (L.signal == f"{nm} lag1")].iloc[0]
        bz = bt(f"B {nm}(t) -> {st} intra", mode="z1.0"); bzh = bt(f"B {nm}(t) -> {st} intra", " hedged", mode="z1.0")
        sy = REG[(REG.stock == st) & (REG.signal == nm + " sync")]
        conf = "ORTA" if (st == "KRDMD" and code == "HRC") else ("DÜŞÜK" if abs(l0.t_intra) >= 2 else "ÇOK DÜŞÜK")
        rows.append(dict(stock=st, driver_yahoo=f"SHFE/DCE {code} (Sina, kendi baskın-kontrat serim)", driver_desc=f"{nm} gün seansı (kapanış 07:00 UTC = BIST açılışı; sınırda işlenebilir)",
            tv_ticker="AÇILMAZ (Çin borsası) -> alternatif ASX:FMG, SGX:FEF1! (test edilmedi), COMEX:TIO2!", relation="lead_intra", lag=0, corr_full=l0.c_intra, t_stat=l0.t_intra, gap_corr=l0.c_gap, intra_corr=l0.c_intra,
            is_oos=f"IS t={l0.t_IS:.2f} (2018-12..2020, kısa) / OOS t={l0.t_OOS:.2f}", n=l0.n, bt_oos_sharpe=bz.OOS_sharpe, bt_oos_mean_bps=bz.OOS_mean_bps, confidence=conf,
            mechanism="Çin çelik fiyatı sinyali; büyük ölçüde FMG/Asya seansıyla aynı bilgi",
            notes=f"lag1 (tam işlenebilir) t={l1.t_intra:.2f} -> etki yok; |z|>1 15bps OOS {bz.OOS_mean_bps:.1f}bps t={bz.OOS_t:.2f}, IS {bz.IS_mean_bps:.1f}; hedged OOS t={bzh.OOS_t:.2f}; senkron günlük pc={sy.pc.iloc[0]:.3f} haftalık pc={sy.pcw.iloc[0]:.3f}; Çin ajanının SHFE HRC->KRDMD t=3,33 bulgusunu doğrular (t={l0.t_intra:.2f}) ama IS'te yok"))
jr = REG[REG.signal == "FMG+HC birlikte"]
for _, r in jr.iterrows():
    rows.append(dict(stock=r.stock, driver_yahoo="FMG.AX + SHFE HC", driver_desc="ortak regresyon (intra_t ~ FMG_t + HC_t + gap_t)", tv_ticker="ASX:FMG", relation="lead_intra", lag=0, t_stat=r.t_FMG_t, n=r.n,
        confidence="ORTA", mechanism="hangisi baskın?", notes=f"FMG t={r.t_FMG_t:.2f}, HC t={r.t_HC_t:.2f}: FMG bilgisini HC büyük ölçüde içermiyor değil; ikisi örtüşüyor, FMG daha sağlam (uzun örneklem, net zamanlama)"))
# aylık
SEL = {"EREGL": ["SLX", "MT.AS", "STLD", "NUE", "VALE", "TS", "TIO=F", "HRC=F", "BUS=F", "HG=F"], "KRDMD": ["SLX", "MT.AS", "VALE", "HG=F", "TIO=F", "HRC=F", "BUS=F", "CMC"],
       "BRSAN": ["TS", "OIH", "HRC=F", "CL=F", "NUE", "STLD", "ALI=F"], "TRALT": ["GC=F", "SI=F", "ONS_TL", "HG=F"], "TRMET": ["GC=F", "SI=F", "ONS_TL"]}
for st, ds in SEL.items():
    for d in ds:
        x = M[(M.stock == st) & (M.driver == d) & (~M.usd)]
        if not len(x): continue
        x = x.iloc[0]; xu = M[(M.stock == st) & (M.driver == d) & (M.usd)]
        good = abs(x.pc_m) >= 0.15 and np.sign(x.c_IS) == np.sign(x.c_OOS) and abs(x.t_pc) >= 3
        conf = "YÜKSEK" if good and min(abs(x.c_IS), abs(x.c_OOS)) >= 0.2 else ("ORTA" if abs(x.t_pc) >= 2.5 else ("DÜŞÜK" if abs(x.t_pc) >= 1.5 else "ÇOK DÜŞÜK"))
        rows.append(dict(stock=st, driver_yahoo=d, driver_desc=f"AYLIK getiri (2008+)", tv_ticker=mh.tv(d), relation="sync", lag=0, corr_full=x.c_m, pcorr_xu100=x.pc_m, beta=x.beta_m, t_stat=x.t_pc,
            is_oos=f"IS {x.c_IS:.2f} / OOS {x.c_OOS:.2f}", n=x.n_m, confidence=conf, mechanism="küresel çelik/metal döngüsü (aylık frekansta günlük gürültü ve eşzamansızlık yok olur)",
            notes=f"USD bazı aylık c={xu.c_m.iloc[0]:.2f} pc={xu.pc_m.iloc[0]:.2f}" if len(xu) else ""))
# m5
for _, g in G.iterrows():
    rows.append(dict(stock=g.stock.replace(".IS", ""), driver_yahoo=g.driver, driver_desc="m5 -> 30 dk tam hizalı gün-içi (son ~60 gün, 07:00-15:00 UTC)", tv_ticker=mh.tv(g.driver), relation="intraday_minutes", lag=1,
        corr_full=g.c_sync30, t_stat=g.t_drv_lead30, n=g.n, confidence="ORTA" if (abs(g.t_sync30) >= 3 and g.n > 500) else "DÜŞÜK",
        mechanism="aynı 30 dk pencerede senkron fiyatlama", notes=f"senkron t={g.t_sync30:.1f}; sürücü 30dk önde c={g.c_drv_lead30:.3f} t={g.t_drv_lead30:.1f}; hisse 30dk önde t={g.t_stk_lead30:.1f}; {g.days} gün (Eylül-Ekim 2026 fon krizi dönemi dahil)"))
# olaylar 2
for _, e in E2.iterrows():
    rows.append(dict(stock=e.stock, driver_yahoo="EVENT", driver_desc=e.event, tv_ticker=f"BIST:{e.stock}" if e.bench == "XU100" else mh.tv(e.stock), relation="event", lag=0, t_stat=e.z_m1p1, n=3,
        confidence="DÜŞÜK" if abs(e.z_m1p1) >= 2 else "ÇOK DÜŞÜK", mechanism="ABD 232 çelik vergisi / Türkiye maden riski",
        notes=f"{e.date}: CAR[-1,+1] {e.car_m1p1_pct:.1f}% (z {e.z_m1p1:.1f}), CAR[0,+10] {e.car_0_10_pct:.1f}% (z {e.z_0_10:.1f}) vs {e.bench}" + (" | 2018-08-10 kur kriziyle karışık" if "2018-08" in e.date else "")))
# gece altın backtest
for _, b in NB[NB.cost == 15].iterrows():
    rows.append(dict(stock=b.stock, driver_yahoo="GC=F (saatlik gece)", driver_desc=f"backtest: {b.signal} (2024-06+, IS<2025-08, OOS>=2025-08)", tv_ticker="COMEX:GC1!", relation="lead_intra", lag=0,
        is_oos=f"IS {b.IS_mean_bps:.1f}bps (t {b.IS_t:.2f}) / OOS {b.OOS_mean_bps:.1f}bps (t {b.OOS_t:.2f})", bt_oos_mean_bps=b.OOS_mean_bps, n=b.ALL_n, confidence="ÇOK DÜŞÜK" if b.ALL_t < 1.5 else "DÜŞÜK",
        mechanism="altın gece hareketi açılışta fiyatlanıyor; gap aşırı tepkisi hipotezi", notes=f"tüm dönem {b.ALL_mean_bps:.1f}bps t={b.ALL_t:.2f} Sharpe {b.ALL_sharpe:.2f}; gap'in altına betası ~{b.beta_last:.2f}"))
# Türkiye madenci faktörü
for _, t in TM[TM["sample"] == "ALL"].iterrows():
    rows.append(dict(stock=t.stock, driver_yahoo="TUR", driver_desc="ABD'de işlem gören altın madencisinin Türkiye ETF'ine yüklenmesi (GDX, S&P kontrollü)", tv_ticker="NASDAQ:TUR", relation="hypothesis", lag=0,
        beta=t.b_TUR, t_stat=t.t_TUR, n=t.n, confidence="ÇOK DÜŞÜK" if abs(t.t_TUR) < 2 else "DÜŞÜK", mechanism="Türkiye operasyonu (EGO: Kışladağ/Efemçukuru; SSRM: Çöpler) -> ülke riski", notes="EGO OOS t=2,0, diğerleri ~0"))
for _, t in TM[TM.stock.str.startswith("TRALT")].iterrows():
    rows.append(dict(stock="TRALT", driver_yahoo=t["sample"].split()[2], driver_desc="TRALT (USD) haftalık kısmi corr | GC=F, XU100 USD (+GDX)", tv_ticker=mh.tv(t["sample"].split()[2]), relation="hypothesis", lag=0,
        pcorr_xu100=t.b_GDX, t_stat=t.t_TUR, n=t.n, confidence="ÇOK DÜŞÜK", mechanism="ortak 'Türk altın madencisi' faktörü", notes=f"pc={t.b_GDX:.3f}; GDX de kontrol edilince {t.b_TUR:.3f} -> ortak faktör YOK"))
rows.append(dict(stock="ALL", driver_yahoo="VİOP akşam seansı", driver_desc="Pay vadelileri akşam seansında işlem görüyor mu?", tv_ticker="-", relation="hypothesis", confidence="ORTA",
    mechanism="BIST kapanışı sonrası bilgi (altın, ABD çeliği) pay vadelisinde ertesi sabah 09:30 TSİ'ye kadar işlenemez",
    notes="Kaynaklar (Borsa İstanbul SSS, aracı kurum sayfaları): akşam seansı (19:00-23:00 TSİ) yalnız endeks + kıymetli maden/döviz sözleşmeleri; pay vadelisi normal seans 09:30-18:10. Resmi güncel listeden teyit edilmeli"))
X = pd.DataFrame(rows).reindex(columns=F.columns)
F = pd.concat([F, X], ignore_index=True)
F.to_csv(os.path.join(mh.OUT, "f_metal.csv"), index=False, float_format="%.4f")
print(F.shape, F.confidence.value_counts().to_dict())
print(X[["stock", "driver_yahoo", "relation", "t_stat", "confidence"]].head(12).to_string(index=False))
