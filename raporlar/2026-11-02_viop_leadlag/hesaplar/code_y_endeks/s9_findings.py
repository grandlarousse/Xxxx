"""Bulgular CSV'si: out/f_y_endeks.csv (ana brifing sütunları)."""
from ye_common import *
COLS = ["stock", "driver_yahoo", "driver_desc", "tv_ticker", "relation", "lag", "corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr",
        "is_oos", "bt_oos_sharpe", "bt_oos_mean_bps", "n", "confidence", "mechanism", "notes"]
rows = []
def add(**k): rows.append({c: k.get(c, np.nan) for c in COLS})
def dsc(I): return IDX_DESC.get(I, I)
def f2(x, d=2):
    return "nan" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{d}f}"
# ---------- 1. SENKRON ----------
S = pd.read_csv(RES + "/sync.csv"); B1 = pd.read_csv(RES + "/sync_best.csv").set_index("stock"); PY = pd.read_csv(RES + "/sync_pc_years.csv")
for s in VIOP:
    g = S[S.stock == s].set_index("idx")
    want = ["XU100", "XU030", "XUTUM", "XYUZO", "XTUMY"] + [x for x in SECT[s] if x in g.index] + [B1.loc[s, "best_2f_idx"], B1.loc[s, "best_ex_3y"]]
    seen = set()
    for I in want:
        if I in seen or I not in g.index: continue
        seen.add(I); r = g.loc[I]
        py = PY[(PY.stock == s) & (PY.idx == I)]
        pcex = py.pc_ex_full.iloc[0] if len(py) else np.nan; fy = py.frac_years_same_sign.iloc[0] if len(py) else np.nan
        pis = py.pc_ex_IS.iloc[0] if len(py) else np.nan; poos = py.pc_ex_OOS.iloc[0] if len(py) else np.nan
        mech = r.w_last > 0.02
        if I in ("XU100", "XU030", "XUTUM", "XYUZO", "XTUMY"):
            conf = "YÜKSEK" if r.corr_full >= 0.3 else "ORTA"
            mechs = "ulusal piyasa faktörü (ortak beta)" + ("; XYUZO/XTUMY hisseyi İÇERMEZ -> mekanik içerme yok" if I in ("XYUZO", "XTUMY") else "")
        else:
            ok = np.isfinite(pcex) and abs(pcex) >= 0.15 and fy >= 0.75 and np.sign(pis if np.isfinite(pis) else poos) == np.sign(poos)
            conf = "YÜKSEK" if ok else ("ORTA" if np.isfinite(pcex) and abs(pcex) >= 0.08 else "DÜŞÜK")
            mechs = "sektör faktörü (XU100 ötesi ortak sektör şoku)"
        note = (f"t_stat=XU100+endeks iki faktörlü modelde endeks katsayısının t'si; R2={f2(r.r2)} (3y R2={f2(r.corr_3y**2)}); hisse ağırlığı w≈{f2(r.w_last,3)} (NNLS tahmini); hisse-hariç endeks corr={f2(r.get('corr_ex'))}, "
                f"hisse-hariç kısmi(|XU100)={f2(pcex)} (IS {f2(pis)} / OOS {f2(poos)}, yılların %{f2(100*fy,0) if np.isfinite(fy) else 'nan'}'inde aynı işaret)"
                + ("; MEKANİK İÇERME: ham korelasyon hissenin endeksteki payı nedeniyle şişkin" if mech else "")
                + (f"; 3y'da en yüksek R2 (ham) endeks={B1.loc[s,'best_raw_3y']}, hisse-hariç={B1.loc[s,'best_ex_3y']}" if I == SECT[s][0] else ""))
        add(stock=s, driver_yahoo=I + ".IS", driver_desc=dsc(I), tv_ticker=tv(I), relation="sync", lag=0, corr_full=r.corr_full, corr_3y=r.corr_3y, corr_1y=r.corr_1y,
            pcorr_xu100=r.get("pcorr_xu100"), beta=r.beta, t_stat=r.get("t_i_2f"), is_oos=f"corr IS {f2(r.get('corr_IS'))} / OOS {f2(r.get('corr_OOS'))}", n=r.n,
            confidence=conf, mechanism=mechs, notes=note)
# ---------- 2. GÜNLÜK ÖNCÜLÜK ----------
A = pd.concat([pd.read_csv(RES + f"/A_{t}_fdr.csv") for t in ["cc", "gap", "intra"]])
Aall = pd.read_csv(RES + "/lead_idx_to_stock.csv")
def conf_lead(r):
    if r.get("fdr", False) and r.get("rep", False): return "ORTA"
    if abs(r.t_full) >= 3 and np.sign(r.t_IS) == np.sign(r.t_OOS): return "DÜŞÜK"
    return "ÇOK DÜŞÜK"
rel = {"cc": "lead_multiday", "gap": "lead_gap", "intra": "lead_intra"}
for s in VIOP:
    for I in ["XU030", SECT[s][0], "XU100"]:
        sub = Aall[(Aall.stock == s) & (Aall.idx == I)]
        if not len(sub): continue
        var = "ex" if (sub["var"] == "ex").any() else "raw"; sub = sub[sub["var"] == var].set_index("target")
        for tgt in ["cc", "gap", "intra"]:
            if tgt not in sub.index: continue
            r = sub.loc[tgt]; fr = A[(A.stock == s) & (A.idx == I) & (A.target == tgt)]
            rr = dict(r);
            if len(fr): rr.update(fdr=bool(fr.fdr.iloc[0]), rep=bool(fr.rep.iloc[0]))
            add(stock=s, driver_yahoo=I + ".IS", driver_desc=dsc(I) + (" (hisse-hariç)" if var == "ex" else ""), tv_ticker=tv(I), relation=rel[tgt], lag=1,
                corr_full=r.b_full, t_stat=r.t_full, gap_corr=sub.loc["gap", "b_full"] if "gap" in sub.index else np.nan, intra_corr=sub.loc["intra", "b_full"] if "intra" in sub.index else np.nan,
                is_oos=f"IS b {f2(r.b_IS,3)} (t {f2(r.t_IS)}) / OOS b {f2(r.b_OOS,3)} (t {f2(r.t_OOS)})", n=r.n_full, confidence=conf_lead(pd.Series(rr)),
                mechanism="endeks_{t-1} -> hisse_t; kontroller: hisse cc_{t-1}" + (", XU100_{t-1} (XU030/sektör ile kısmen eşdoğrusal: katsayı XU100'e göre ARTIMSAL etki; büyüklüğü değil t'yi yorumlayın)" if I != "XU100" else "") + ("" if tgt != "gap" else "; gap işlenemez (açılış müzayedesi)"),
                notes=f"hedef={tgt}; standart katsayı (z-skor) ~ kısmi korelasyon; 47x{Aall.idx.nunique()}x3 testte BH-FDR q={f2(fr.q.iloc[0],3) if len(fr) else 'nan'}; dairesel kaydırma null |t|>3 oranı %0,4")
# ek: |t|>=3 olan tüm A testleri (yukarıda yoksa)
for _, r in A[(A.t_full.abs() >= 3) & (A["var"] == "raw")].iterrows():
    if r.idx in ("XU030", "XU100", SECT[r.stock][0]): continue
    add(stock=r.stock, driver_yahoo=r.idx + ".IS", driver_desc=dsc(r.idx), tv_ticker=tv(r.idx), relation=rel[r.target], lag=1, corr_full=r.b_full, t_stat=r.t_full,
        is_oos=f"IS b {f2(r.b_IS,3)} (t {f2(r.t_IS)}) / OOS b {f2(r.b_OOS,3)} (t {f2(r.t_OOS)})", n=r.n_full, confidence=conf_lead(r),
        mechanism="tarama sonucu (|t|>=3); ekonomik mekanizma belirsiz", notes=f"hedef={r.target}; FDR q={f2(r.q,3)}; çoklu test kaynaklı olabilir")
# ters yön
Bf = pd.read_csv(RES + "/B_fdr.csv")
for _, r in Bf[(Bf.idx.isin(["XU100", "XU030"])) | (Bf.t_full.abs() >= 3)].iterrows():
    add(stock=r.stock, driver_yahoo=r.idx + ".IS", driver_desc=f"{r.stock}_(t-1) -> {dsc(r.idx)}_t (TERS YÖN: hisse önde)", tv_ticker=tv(r.idx), relation="reverse", lag=-1,
        corr_full=r.b_full, t_stat=r.t_full, is_oos=f"IS t {f2(r.t_IS)} / OOS t {f2(r.t_OOS)}", n=r.n_full, confidence="DÜŞÜK" if abs(r.t_full) >= 3 else "ÇOK DÜŞÜK",
        mechanism="hisse_{t-1} -> endeks_t; kontroller endeks_{t-1}, XU100_{t-1}", notes=f"BH-FDR q={f2(r.q,3)} (2350 test)")
# endeks -> endeks
Cf = pd.read_csv(RES + "/C_fdr.csv")
key = [("XBANK", "XUSIN"), ("XUSIN", "XBANK"), ("XUMAL", "XHOLD"), ("XHOLD", "XUMAL"), ("XLBNK", "X10XB"), ("X10XB", "XLBNK"), ("XBANK", "XHOLD"), ("XUMAL", "XBANK"), ("XUHIZ", "XBANK"), ("XULAS", "XHOLD")]
for _, r in Cf[Cf.apply(lambda x: (x.leader, x.follower) in key or abs(x.t_full) >= 3.2, axis=1)].iterrows():
    add(stock=f"{r.follower} (endeks)", driver_yahoo=r.leader + ".IS", driver_desc=f"{dsc(r.leader)} -> {dsc(r.follower)}", tv_ticker=tv(r.leader), relation="lead_multiday", lag=1,
        corr_full=r.b_full, t_stat=r.t_full, is_oos=f"IS b {f2(r.b_IS,3)} (t {f2(r.t_IS)}) / OOS b {f2(r.b_OOS,3)} (t {f2(r.t_OOS)})", n=r.n_full,
        confidence="DÜŞÜK" if abs(r.t_full) >= 3 else "ÇOK DÜŞÜK", mechanism="sektörler arası öncülük (takipçi kendi lag'i + XU100_{t-1} kontrollü)", notes=f"2450 endeks çiftinde 0 FDR; q={f2(r.q,3)}")
# Lo–MacKinlay
L = pd.read_csv(RES + "/lomac_tests.csv")
for _, r in L[L.per == "full"].iterrows():
    li = L[(L.test == r.test) & (L.target == r.target)].set_index("per")
    add(stock=r.test.split("->")[1] + " (portföy/endeks)", driver_yahoo=r.test.split("_lag1")[0], driver_desc=f"Lo–MacKinlay: {r.test} ({r.target})", tv_ticker=tv(r.test.split("_lag1")[0]) if r.test.startswith("X") else "",
        relation="liquidity", lag=1, corr_full=r.b, t_stat=r.t, n=r.n, is_oos=f"IS b {f2(li.loc['IS','b'],3)} (t {f2(li.loc['IS','t'])}) / OOS b {f2(li.loc['OOS','b'],3)} (t {f2(li.loc['OOS','t'])})",
        confidence="DÜŞÜK" if abs(r.t) >= 2 else "ÇOK DÜŞÜK", mechanism="büyük->küçük çapraz otokorelasyon (bayat fiyat); takipçinin kendi lag'i kontrollü",
        notes="Q1=en illikit beşli (veri setindeki 176 hisse; gerçek küçük ölçek değil), Q5=en likit. Kontrolsüz corr(Q1_t,Q5_{t-1})=0,053 vs corr(Q5_t,Q1_{t-1})=-0,008; kendi lag kontrolüyle kayboluyor")
# ---------- 3. GÜN-İÇİ ----------
for tag, relname, lab in [("isy_h1", "lead_hourly", "h1 İş Yatırım 2017–2026"), ("yh_m5", "lead_5m", "m5 Yahoo 60 gün")]:
    p = RES + f"/intraday_{tag}.csv"
    if not os.path.exists(p): continue
    R = pd.read_csv(p)
    for (s, I), g in R[(R["var"] == "ex") & (R.dir == "idx->stk")].groupby(["stock", "idx"]):
        f = g[g.per == "full"].iloc[0]
        isr = g[g.per == "IS"]; oos = g[g.per == "OOS"]; cr = g[g.per.isin(["fon_krizi_16Eyl+", "2026_EylEki_fon_krizi"])]
        rv = R[(R["var"] == "ex") & (R.dir == "stk->idx") & (R.stock == s) & (R.idx == I) & (R.per == "full")]
        raw = R[(R["var"] == "raw") & (R.dir == "idx->stk") & (R.stock == s) & (R.idx == I) & (R.per == "full")]
        if tag == "isy_h1":
            ok = abs(f.t_sum_lag) >= 3 and len(isr) and len(oos) and np.sign(isr.sum_lag.iloc[0]) == np.sign(oos.sum_lag.iloc[0]) == np.sign(f.sum_lag)
            conf = "YÜKSEK" if ok and abs(oos.t_sum_lag.iloc[0]) >= 2 and abs(isr.t_sum_lag.iloc[0]) >= 2 else ("ORTA" if ok else ("DÜŞÜK" if abs(f.t_sum_lag) >= 2 else "ÇOK DÜŞÜK"))
            iso = f"IS Σβlag {f2(isr.sum_lag.iloc[0],3)} (t {f2(isr.t_sum_lag.iloc[0])}) / OOS {f2(oos.sum_lag.iloc[0],3)} (t {f2(oos.t_sum_lag.iloc[0])})" if len(isr) and len(oos) else ""
        else:
            conf = "DÜŞÜK" if abs(f.t_sum_lag) >= 3 else "ÇOK DÜŞÜK"
            pre = g[g.per == "pre_crisis"]; iso = f"kriz öncesi Σβlag {f2(pre.sum_lag.iloc[0],3)} / fon krizi {f2(cr.sum_lag.iloc[0],3) if len(cr) else 'nan'}"
        L_ = 3 if tag == "isy_h1" else 6
        add(stock=s, driver_yahoo=I + ".IS", driver_desc=f"{dsc(I)} (hisse-hariç) {lab}", tv_ticker=tv(I), relation=relname, lag=f"1..{L_} bar",
            corr_full=f.sum_lag, beta=f.b0, t_stat=f.t_sum_lag, n=f.n, is_oos=iso, confidence=conf,
            mechanism="endeks barı -> hisse sonraki barlar (hisse kendi lag'leri kontrollü); 5 dk'da fiyat adımı ayrıklığı/bayat son fiyat ile uyumlu; İŞLENEBİLİR DEĞİL (maliyet>getiri)",
            notes=(f"corr_full=Σβ_lag(1..{L_}) (regresyon katsayısı, standart değil); beta=senkron bar betası b0; gecikmeli pay={f2(f.lag_share)}; b1={f2(f.b1,3)} (t {f2(f.t1)}); "
                   f"ham endeksle Σβlag={f2(raw.sum_lag.iloc[0],3) if len(raw) else 'nan'} (fark=mekanik içerme payı); ters yön (hisse->endeks) Σβlag={f2(rv.sum_lag.iloc[0],3) if len(rv) else 'nan'} (t {f2(rv.t_sum_lag.iloc[0]) if len(rv) else 'nan'})"))
    pi = RES + f"/intraday_idx_{tag}.csv"
    if os.path.exists(pi):
        RR = pd.read_csv(pi)
        for (a, b), g in RR.groupby(["leader", "follower"]):
            f = g[g.per == "full"].iloc[0]; isr = g[g.per == "IS"]; oos = g[g.per == "OOS"]
            iso = (f"IS {f2(isr.sum_lag.iloc[0],3)} (t {f2(isr.t_sum_lag.iloc[0])}) / OOS {f2(oos.sum_lag.iloc[0],3)} (t {f2(oos.t_sum_lag.iloc[0])})" if len(isr) and len(oos) else "")
            ok = abs(f.t_sum_lag) >= 3 and (not len(isr) or np.sign(isr.sum_lag.iloc[0]) == np.sign(oos.sum_lag.iloc[0]))
            add(stock=f"{b} (endeks)", driver_yahoo=a + ".IS", driver_desc=f"{dsc(a)} -> {dsc(b)} ({lab})", tv_ticker=tv(a), relation=relname, lag="1..3 bar" if tag == "isy_h1" else "1..6 bar",
                corr_full=f.sum_lag, beta=f.b0, t_stat=f.t_sum_lag, n=f.n, is_oos=iso, confidence=("ORTA" if ok and tag == "isy_h1" else ("DÜŞÜK" if abs(f.t_sum_lag) >= 3 else "ÇOK DÜŞÜK")),
                mechanism="endeks hesaplaması bileşenlerin SON işlem fiyatını kullanır: illikit bileşenli endeks (XTUMY/XYUZO/XHOLD) mekanik olarak gecikir (bayat fiyat); endeks spot olarak işlenemez",
                notes=f"gecikmeli pay={f2(f.lag_share)}; b1={f2(f.b1,3)} (t {f2(f.t1)})")
# ---------- 4. REJİM ----------
G = pd.read_csv(RES + "/regimes.csv").set_index("regime")
for rg in G.index:
    r = G.loc[rg]
    add(stock="XTUMY/XYUZO vs XU030", driver_yahoo="XU030.IS", driver_desc=f"rejim: {rg}", tv_ticker="BIST:XTUMY / BIST:XYUZO / BIST:XU030", relation="regime", lag=0,
        corr_full=r.corr_XU030_XTUMY, beta=r.beta_XTUMY_on_XU030, t_stat=r["lead_XU030->XTUMY_t"], n=r.n_days,
        confidence="ORTA" if "fon" in rg else "DÜŞÜK", mechanism="rejim: büyük/küçük ayrışması, korelasyon ve öncülük değişimi",
        notes=(f"kümülatif: XU030 {f2(r['cum_XU030_%'],1)}%, XYUZO {f2(r['cum_XYUZO_%'],1)}%, XTUMY {f2(r['cum_XTUMY_%'],1)}% (XTUMY-XU030 {f2(r['rel_XTUMY-XU030_%'],1)} puan); "
               f"corr(XU030,XYUZO)={f2(r.corr_XU030_XYUZO)}; XU030_(t-1)->XTUMY b={f2(r['lead_XU030->XTUMY_b'])}; XTUMY özgecikme b={f2(r.autocorr_XTUMY_b)} (t {f2(r.autocorr_XTUMY_t)}); "
               f"VİOP ort. ikili corr={f2(r.avg_pair_corr_VIOP)}; kesit dağılımı {f2(r.xsec_disp_bps,0)} bps; hacim oranı (önceki 120g'e göre medyan)={f2(r.turnover_ratio_vs_prev120_median)}"))
# ---------- 5. BACKTEST ----------
BT = pd.read_csv(RES + "/backtests.csv")
for _, r in BT[BT.stock.isin(["XU030", "47 hisse L/S", "illikit16", "likit16"]) | BT.stock.str.startswith("Q1")].iterrows():
    if r.cost == 0: continue
    add(stock=r.stock, driver_yahoo="XU030.IS" if "XU030" in r.bt else "sektör endeksleri", driver_desc=f"BACKTEST {r.bt} (maliyet {int(r.cost)} bps, yön={'+' if r.sign > 0 else '-'} IS'te seçildi)",
        tv_ticker="BIST:XU030D1!" if r.stock == "XU030" else ("BIST:XU030" if "XU030" in r.bt else ""), relation="lead_intra" if "intra" in r.bt else ("lead_gap" if "gap" in r.bt else "lead_multiday"),
        lag=1, t_stat=r.OOS_t, is_oos=f"IS {f2(r.IS_mean_bps,1)} bps (t {f2(r.IS_t)}, n {int(r.IS_n) if np.isfinite(r.IS_n) else 'nan'}) / OOS {f2(r.OOS_mean_bps,1)} bps (t {f2(r.OOS_t)}, n {int(r.OOS_n) if np.isfinite(r.OOS_n) else 'nan'})",
        bt_oos_sharpe=r.OOS_sharpe, bt_oos_mean_bps=r.OOS_mean_bps, n=r.OOS_n, confidence="DÜŞÜK" if (r.OOS_t > 2 and r.IS_t > 1) else "ÇOK DÜŞÜK",
        mechanism="backtest (look-ahead yok)", notes=f"yıllar (bps): {r.by_year}"[:400])
per = BT[~(BT.stock.isin(["XU030", "47 hisse L/S", "illikit16", "likit16"]) | BT.stock.str.startswith("Q1"))]
for (b, c), g in per.groupby(["bt", "cost"]):
    if c == 0: continue
    add(stock=f"{len(g)} hisse (medyan)", driver_yahoo="", driver_desc=f"BACKTEST {b} hisse başına (maliyet {int(c)} bps)", tv_ticker="", relation="lead_intra" if "intra" in b else "lead_gap",
        lag=1, is_oos=f"medyan IS {f2(g.IS_mean_bps.median(),1)} / OOS {f2(g.OOS_mean_bps.median(),1)} bps; OOS>0 oranı {f2((g.OOS_mean_bps>0).mean())}", bt_oos_sharpe=g.OOS_sharpe.median(),
        bt_oos_mean_bps=g.OOS_mean_bps.median(), n=len(g), confidence="ÇOK DÜŞÜK", mechanism="backtest", notes=f"OOS t>2 olan hisse: {int((g.OOS_t>2).sum())}")
T4 = pd.read_csv(RES + "/bt_thyao_lead.csv"); TR = pd.read_csv(RES + "/thyao_robust.csv")
for _, r in T4[T4.cost.isin([8, 15])].iterrows():
    add(stock="XU030 (vadeli ile)", driver_yahoo="THYAO.IS", driver_desc=f"BACKTEST {r.bt} (maliyet {int(r.cost)} bps)", tv_ticker="BIST:THYAO -> BIST:XU030D1!", relation="lead_intra", lag=1,
        t_stat=r.OOS_t, is_oos=f"IS(2000-2020) {f2(r.IS_mean_bps,1)} bps (t {f2(r.IS_t)}) / OOS {f2(r.OOS_mean_bps,1)} bps (t {f2(r.OOS_t)})", bt_oos_sharpe=r.OOS_sharpe, bt_oos_mean_bps=r.OOS_mean_bps,
        n=r.OOS_n, confidence="DÜŞÜK", mechanism="likit/yabancı ağırlıklı 'öncü' hisse (THYAO) rölatif performansı ertesi gün endekse yayılıyor (hipotez)",
        notes="Regresyon: THYAO_{t-1} -> XU030 gün-içi_t b=0,08 (t 3,2; ES/BZ/USDTRY kontrollü t 3,0); alt dönemler 2014–17 +0,12, 2017–20 0,00, 2021–23 +0,18, 2023–26 +0,02 (t 0,4) -> son 3 yılda YOK; 2350 testlik taramadan seçildi (seçim yanlılığı). " + f"yıllar: {r.by_year}"[:250])
M5 = pd.read_csv(RES + "/bt_m5_shock.csv")
for c, g in M5.groupby("cost"):
    add(stock="47 hisse (medyan)", driver_yahoo="XU030.IS", driver_desc=f"BACKTEST 5 dk XU030 şoku (|z|>2) -> hisse sonraki 15 dk (maliyet {c})", tv_ticker="BIST:XU030", relation="intraday_minutes", lag="1..3 bar",
        is_oos=f"medyan IS {f2(g.IS_mean_bps.median(),1)} / OOS {f2(g.OOS_mean_bps.median(),1)} bps; brüt {f2(g.gross_bps.median(),1)} bps", bt_oos_mean_bps=g.OOS_mean_bps.median(), n=int(g.n.median()),
        confidence="ÇOK DÜŞÜK", mechanism="5 dk gecikmeli tepki fiyat adımından küçük; spread'i karşılamıyor", notes=f"OOS>0 hisse sayısı {(g.OOS_mean_bps>0).sum()}/47; HEKTS/SASA brüt 12–19 bps ama 1 tik ≈ 42–44 bps")
H6 = pd.read_csv(RES + "/bt_h1_idx.csv")
for _, r in H6[H6.cost.isin([4, 8])].iterrows():
    add(stock=f"{r.follower} (endeks)", driver_yahoo=r.lead + ".IS", driver_desc=f"BACKTEST saatlik {r.lead} barı |z|>1 -> {r.follower} sonraki 3 saat (maliyet {int(r.cost)} bps; yön IS'te {'+' if r.sign>0 else '-'})",
        tv_ticker={"XU030": "BIST:XU030D1!", "X10XB": "BIST:X10XBD1!", "XBANK": "BIST:XLBNKD1!"}.get(r.follower, tv(r.follower)), relation="lead_hourly", lag="1..3 bar", t_stat=r.OOS_t,
        is_oos=f"IS {f2(r.IS_mean_bps,1)} bps (t {f2(r.IS_t)}) / OOS {f2(r.OOS_mean_bps,1)} bps (t {f2(r.OOS_t)})", bt_oos_mean_bps=r.OOS_mean_bps, n=r.OOS_n,
        confidence="DÜŞÜK" if (r.OOS_t > 1 and r.IS_t > 1) else "ÇOK DÜŞÜK", mechanism="saatlik endeks->endeks; spot endeks işlenemez, vadeli spotu önceleyebilir (iyimser üst sınır)", notes=f"yıllar: {r.by_year}"[:300])
H6b = pd.read_csv(RES + "/bt_h1_spread.csv")
for _, r in H6b[H6b.cost_per_leg.isin([4])].iterrows():
    add(stock=f"{r.follower}-{r.lead} ({r.target})", driver_yahoo=r.lead + ".IS", driver_desc=f"BACKTEST saatlik spread ({r.follower}-{r.lead}) |z|>1 -> {r.target} sonraki 3 saat (bacak başı 4 bps)",
        tv_ticker="BIST:X10XBD1! / BIST:XLBNKD1!" if r.lead == "XLBNK" else "", relation="lead_hourly", lag="1..3 bar", t_stat=r.OOS_t,
        is_oos=f"IS {f2(r.IS_mean_bps,1)} bps (t {f2(r.IS_t)}) / OOS {f2(r.OOS_mean_bps,1)} bps (t {f2(r.OOS_t)})", bt_oos_mean_bps=r.OOS_mean_bps, n=r.OOS_n,
        confidence="DÜŞÜK", mechanism="sektör spread'i saatlik devam (brüt OOS +6 bps, t 3,5); maliyet sonrası ~0/negatif; kısmen spot endeks bayatlığı",
        notes="Regresyon (takipçi kendi lag'leri kontrollü) XBANK->XUSIN Σβ1..3=-0,088 (t -6,5; IS -5,5 / OOS -4,6) ama basit işaret stratejisi kârsız")
TK = pd.read_csv(RES + "/tick_yh_m5.csv")
for _, r in TK.iterrows():
    add(stock="47 hisse (kesit)", driver_yahoo=r.idx + ".IS", driver_desc=f"5 dk gecikmeli pay ~ fiyat adımı ayrıklığı ({r.idx})", tv_ticker=tv(r.idx), relation="liquidity", lag="1..6 bar",
        corr_full=r["spearman(lag_share,zero_bar)"], is_oos="", n=47, confidence="ORTA", mechanism="mikro yapı: göreli tik büyük / sıfır getirili bar oranı yüksek hisseler endeksi 5–30 dk gecikmeyle izliyor",
        notes=f"Spearman(gecikmeli pay, sıfır-getiri bar oranı)={f2(r['spearman(lag_share,zero_bar)'])}; (göreli tik)={f2(r['spearman(lag_share,rel_tick)'])}; (log TL hacim)={f2(r['spearman(lag_share,log_turnover)'])}")
FK = pd.read_csv(RES + "/fon_krizi_kesit.csv", index_col=0)
add(stock=f"{len(FK)} BIST hissesi (kesit)", driver_yahoo="", driver_desc="Fon krizi 01.09–30.10.2026 kesit getirisi", tv_ticker="BIST:XTUMY / BIST:XU030", relation="regime", lag=0,
    n=len(FK), confidence="ORTA", mechanism="tasfiye satışı: spekülatif/yüksek hacimli BIST100 dışı isimlerde taban serileri",
    notes=(f"medyan: VİOP hisseleri {f2(FK[FK.viop]['crisis_%'].median(),1)}% vs VİOP dışı {f2(FK[~FK.viop]['crisis_%'].median(),1)}%; 15 hisse -%86..-97 (ODINE, BIGEN, OZATD, IEYHO, RALYH, ANELE, DSTKF, TEHOL, PEKGY, TERA, KTLEV, TRHOL...; 25–37 taban günü); "
           f"Spearman(kriz getirisi, 2026 Oca–Ağu getirisi)={f2(FK['crisis_%'].corr(FK['pre_2026_%'], method='spearman'))} (doğrusal değil: en çok yükselen VE en çok düşen beşliler en kötü); VİOP'ta en kötü: VESTL -52, ASTOR -51, GUBRF -48, ODAS -42, HEKTS -41"))
F = pd.DataFrame(rows, columns=COLS)
for c in ["corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr", "bt_oos_sharpe", "bt_oos_mean_bps"]:
    F[c] = pd.to_numeric(F[c], errors="coerce").round(4)
F.to_csv(OUT + "/f_y_endeks.csv", index=False)
print(len(F), F.relation.value_counts().to_dict(), F.confidence.value_counts().to_dict())
