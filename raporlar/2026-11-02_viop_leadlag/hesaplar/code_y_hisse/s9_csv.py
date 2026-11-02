"""Adım 9: Bulgular CSV'si (out/f_y_hisse.csv): aile özetleri + senkron kümeler + ekonomik çiftler (iki yön) + en güçlü (FDR'siz) adaylar + backtestler."""
import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata
RES = hdata.RES
COLS = "stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes".split(",")
rows = []
def add(**k):
    r = {c: k.get(c, "") for c in COLS}; rows.append(r)
def tv(s): return f"BIST:{s}" if not s.startswith("TÜMÜ") else ""
def fut(s): return f" | hedef VİOP: BIST:{s}1!" if s in hdata.VIOP else " | hedef VİOP'ta yok (spot)"
liq = pd.read_csv(os.path.join(hdata.CACHE, "liq.csv"), index_col=0)
def desc(s): return f"{s} ({liq.loc[s,'sector'] if s in liq.index else '?'})"
# ---------- 1. aile özetleri ----------
fam = pd.read_csv(os.path.join(RES, "family_summary.csv"))
for _, f in fam.iterrows():
    rel = {"cc": "lead_multiday" if f.lag != "1" else "lead_cc", "gap": "lead_gap", "intra": "lead_intra", "intra_g": "lead_intra"}[f.dep]
    nul = f"; null(20 kaydırma) p<0,05 ort {f.null_n05:.0f}, |t|>3 ort {f.null_n3:.1f}, BH ort {f.null_nbh:.2f}" if pd.notna(f.get("null_n05")) else ""
    add(stock="TÜMÜ(47)", driver_yahoo="TÜMÜ(177 BIST hissesi)", driver_desc=f"AİLE ÖZETİ: lider cc_t-{f.lag} -> hedef {f.dep}_t (kendi lag, XU100, sektör kontrollü)", relation=rel, lag=f.lag,
        n=int(f.tests), confidence="—", mechanism="çoklu test özeti",
        notes=f"test={f.tests}; p<0,05={f.p05}; |t|>3={f.t3}; BH05(dep,lag)={f.bh}; BH05(dep ailesi, tüm laglar)={f.bh_fam}; IS-BH={f.is_bh}{nul}")
rel_txt = open(os.path.join(RES, "rel.txt")).read().splitlines()
add(stock="TÜMÜ(47)", driver_yahoo="TÜMÜ(177)", driver_desc="AİLE ÖZETİ: piyasa-göreli (hedef-β·XU100) lag1/2/c5, cc/gap/intra; +EW177 kontrol", relation="lead_rel", lag="1,2,c5", n=74439,
    confidence="—", mechanism="çoklu test özeti", notes="9 aile x 8271 test; BH05 keşif 0 (tümünde); IS top-200 -> OOS replikasyon cc 3,0% / gap 3,5% / intra 2,5% vs null 1,4/1,6/2,0% (null maks 4,0/4,5/3,5%); IS&OOS ayrı ayrı |t|>2 aynı işaret 23 çift (bağımsızlık altında beklenen ≈26)")
add(stock="TÜMÜ(47)", driver_yahoo="TÜMÜ(97 saatlik)", driver_desc="AİLE ÖZETİ: saatlik lider r_{h-1} -> hedef r_h (aynı gün)", relation="lead_hourly", lag="1h", n=4512, confidence="—",
    mechanism="çoklu test özeti", notes="2023-12..2026-10; p<0,05=353 (beklenen 226); |t|>3=18; BH05=0; ilk yarı top-200 -> ikinci yarı replikasyon %2,0 (null ≈%2,5)")
# ---------- 2. senkron: 47 hedefin en güçlü artık-korelasyonlu eşleri ----------
CA = pd.read_parquet(os.path.join(RES, "resid_corr_all177.parquet"))
pairs = pd.read_csv(os.path.join(RES, "pairs.csv"))
pairs["key"] = pairs.apply(lambda r: "-".join(sorted([r.leader, r.target])), axis=1)
econ_keys = set(pairs.key)
D = hdata.load(); cc = D["cc"]; m = cc["XU100"]; SPLIT = pd.Timestamp(hdata.SPLIT)
def resid(s, mk):
    d = pd.concat([s, mk], axis=1).dropna(); b = np.cov(d.iloc[:, 0], d.iloc[:, 1])[0, 1] / d.iloc[:, 1].var(); return s - b * mk
def sync_stats(a, b):
    ra, rb = resid(cc[a], m), resid(cc[b], m)
    d = pd.concat([cc[a], cc[b]], axis=1).dropna(); last = d.index[-1]
    c3 = d[d.index >= last - pd.DateOffset(years=3)].corr().iloc[0, 1]; c1 = d[d.index >= last - pd.DateOffset(years=1)].corr().iloc[0, 1]
    r = pd.concat([ra, rb], axis=1).dropna(); pIS = r[r.index < SPLIT].corr().iloc[0, 1] if (r.index < SPLIT).sum() > 250 else np.nan; pO = r[r.index >= SPLIT].corr().iloc[0, 1]
    yy = r.groupby(r.index.year).apply(lambda x: x.iloc[:, 0].corr(x.iloc[:, 1]) if len(x) > 60 else np.nan).dropna()
    beta = np.cov(d.iloc[:, 1], d.iloc[:, 0])[0, 1] / d.iloc[:, 0].var()
    return d.corr().iloc[0, 1], c3, c1, r.corr().iloc[0, 1], beta, pIS, pO, float((yy > 0).mean()), len(d)
def conf_sync(pc, pIS, pO, ys, short):
    if short: return "ORTA" if (pc >= 0.15 and ys >= 0.75) else "DÜŞÜK"
    if pc >= 0.15 and ys >= 0.75 and pIS > 0.05 and pO > 0.05: return "YÜKSEK"
    if pc >= 0.08 and pO > 0.03: return "ORTA"
    return "DÜŞÜK"
labF = pd.read_csv(os.path.join(RES, "clusters_full.csv"), index_col=0)["cl"]
done = set()
for t in hdata.VIOP:
    s = CA[t].drop(t).dropna().sort_values(ascending=False)
    for p_, v in s.head(3).items():
        key = "-".join(sorted([t, p_]))
        if v < 0.15 or key in done or key in econ_keys: continue
        done.add(key)
        c, c3, c1, pc, be, pIS, pO, ys, n = sync_stats(t, p_)
        short = pd.isna(pIS)
        add(stock=t, driver_yahoo=p_ + ".IS", driver_desc=desc(p_), tv_ticker=tv(p_), relation="sync", lag=0, corr_full=round(c, 3), corr_3y=round(c3, 3), corr_1y=round(c1, 3),
            pcorr_xu100=round(pc, 3), beta=round(be, 3), is_oos=f"IS {pIS:.2f} / OOS {pO:.2f}", n=n, confidence=conf_sync(pc, pIS, pO, ys, short),
            mechanism="aynı sektör/grup/tema (senkron, XU100 artığı)", notes=f"yıllık artık korelasyon >0 payı {ys:.2f}; kısa örneklem" * short + f"yıllık artık korelasyon >0 payı {ys:.2f}" * (not short) + fut(t))
# küme satırları
sync_txt = open(os.path.join(RES, "sync.txt")).read()
cy = pd.read_csv(os.path.join(RES, "cluster_year_corr.csv"))
for _, r in cy.iterrows():
    yrs = [c for c in cy.columns if c.isdigit()]; v = r[yrs].astype(float)
    add(stock=r.members.replace(" ", "+"), driver_yahoo="küme", driver_desc=f"Hiyerarşik küme (XU100 artığı, ort. bağlantı, 1-ρ<0,86)", relation="sync", lag=0,
        pcorr_xu100=round(float(np.nanmean(v)), 3), confidence="YÜKSEK" if (v > 0.1).mean() >= 0.75 else "ORTA", mechanism="senkron küme (sektör/grup)",
        notes="küme-içi ort. artık korelasyon yıllara göre: " + " ".join(f"{y}:{float(r[y]):.2f}" for y in yrs if pd.notna(r[y])))
# ---------- 3. ekonomik çiftler ----------
def conf_lead(r):
    t = r.intra_l1_t; ti, to = r.intra_l1_t_IS, r.intra_l1_t_OOS
    same = (np.sign(ti) == np.sign(t)) and (np.sign(to) == np.sign(t))
    if abs(t) >= 3 and r.intra_l1_years_same_sign >= 0.75 and same and abs(ti) > 2 and abs(to) > 2 and r.intra_l1_bh: return "YÜKSEK"
    pre_bad = pd.notna(r.cc_l1_t_PRE) and abs(r.cc_l1_t_PRE) > 2 and np.sign(r.cc_l1_t_PRE) != np.sign(r.cc_l1_t)
    if abs(t) >= 2.5 and same and abs(ti) > 1.5 and abs(to) > 1.5 and not pre_bad: return "DÜŞÜK-ORTA"
    if abs(t) >= 2: return "DÜŞÜK"
    return "ÇOK DÜŞÜK"
sync_done = set()
for _, r in pairs.iterrows():
    if r.key not in sync_done:
        sync_done.add(r.key); short = pd.isna(r.pc_IS)
        add(stock=r.target, driver_yahoo=r.leader + ".IS", driver_desc=f"{desc(r.leader)} — ekonomik çift [{r.group}]", tv_ticker=tv(r.leader), relation="sync", lag=0,
            corr_full=round(r.corr_full, 3), corr_3y=round(r.corr_3y, 3), corr_1y=round(r.corr_1y, 3), pcorr_xu100=round(r.pcorr_xu100, 3), beta=round(r.beta, 3),
            is_oos=f"IS {r.pc_IS:.2f} / OOS {r.pc_OOS:.2f}", n=int(r.cc_l1_n) if pd.notna(r.cc_l1_n) else "",
            confidence=conf_sync(r.pcorr_xu100, r.pc_IS, r.pc_OOS, r.sync_years_pos_share, short), mechanism=f"{r.group}: tedarik zinciri/rakip/grup (senkron)",
            notes=f"yıllık işaret tutarlılığı {r.sync_years_pos_share:.2f}" + (" ; kısa örneklem (2023+)" if short else "") + fut(r.target))
    c = conf_lead(r)
    stale = " ; BAYAT FİYAT RİSKİ: lider hedeften >3x likit" if r.liq_ratio > 3 else ""
    add(stock=r.target, driver_yahoo=r.leader + ".IS", driver_desc=f"{desc(r.leader)} — ekonomik çift [{r.group}] ÖNCÜLÜK", tv_ticker=tv(r.leader), relation="lead_intra", lag=1,
        pcorr_xu100=round(r.cc_l1_pc, 3), beta=round(r.intra_l1_b, 4), t_stat=round(r.intra_l1_t, 2), gap_corr=round(r.gap_l1_pc, 3), intra_corr=round(r.intra_l1_pc, 3),
        is_oos=f"cc t IS {r.cc_l1_t_IS:.2f} / OOS {r.cc_l1_t_OOS:.2f} / PRE(2005-13) {r.cc_l1_t_PRE:.2f}; intra t IS {r.intra_l1_t_IS:.2f} / OOS {r.intra_l1_t_OOS:.2f}",
        bt_oos_sharpe=round(r.bt8_oos_sharpe, 2) if pd.notna(r.bt8_oos_sharpe) else "", bt_oos_mean_bps=round(r.bt8_oos_bps, 1) if pd.notna(r.bt8_oos_bps) else "",
        n=int(r.cc_l1_n) if pd.notna(r.cc_l1_n) else "", confidence=c, mechanism=f"{r.group}: bilgi yayılımı hipotezi (lider_t-1 -> hedef_t)",
        notes=f"kontroller: hedef cc_t-1, XU100_t-1, sektör_t-1; t: cc {r.cc_l1_t:.2f}, gap {r.gap_l1_t:.2f}, intra {r.intra_l1_t:.2f}, intra|gap {r.intra_g_l1_t:.2f}, Σ5g {r.cc_lc5_t:.2f}, hacim filtreli {r.cc_l1_t_volf:.2f}; "
              f"t_stat=gün-içi t; pcorr_xu100=cc lag1 kısmi korelasyonu; gün-içi yılların {r.intra_l1_years_same_sign:.0%}'i aynı işaret; BH(214 yönlü çift, intra) {'geçti' if r.intra_l1_bh else 'geçmedi'}; BT: sign(lider_t-1)->hedef gün-içi, 8 bps; 15 bps OOS SR {r.bt15_oos_sharpe:.2f}{stale}{fut(r.target)}")
# ---------- 4. tarama adayları (FDR'siz veya dar aile FDR) ----------
W = pd.read_parquet(os.path.join(RES, "wide.parquet"))
x = W[W.bh_deplag]
for _, r in x.iterrows():
    add(stock=r.target, driver_yahoo=r.leader + ".IS", driver_desc=desc(r.leader), tv_ticker=tv(r.leader), relation="lead_gap", lag=r.lag, pcorr_xu100=round(r.pc_FULL, 3), beta=round(r.b_FULL, 4),
        t_stat=round(r.t_FULL, 2), is_oos=f"IS t {r.t_IS:.2f} / OOS t {r.t_OOS:.2f}", n=int(r.n_FULL), confidence="DÜŞÜK",
        mechanism="şüpheli: illikit küçük hisse -> büyük hisse gap'i; büyük olasılıkla küçük/bireysel faktörün (EW-XU100)_{t-2} yansıması",
        notes=f"BH05 yalnız (gap,lag={r.lag}) ailesinde (8271 test); gap-ailesi BH'de geçmedi; gap işlenemez (pay vadelisinde akşam seansı yok); likidite oranı {r.liq_ratio:.2f}" + fut(r.target))
for dep, lab in [("intra", "lead_intra"), ("cc", "lead_cc")]:
    y = W[(W.dep == dep) & (W.lag == "1")].copy(); y["a"] = y.t_FULL.abs()
    for _, r in y.nlargest(8, "a").iterrows():
        add(stock=r.target, driver_yahoo=r.leader + ".IS", driver_desc=desc(r.leader), tv_ticker=tv(r.leader), relation=lab, lag=1, pcorr_xu100=round(r.pc_FULL, 3), beta=round(r.b_FULL, 4),
            t_stat=round(r.t_FULL, 2), is_oos=f"IS t {r.t_IS:.2f} / OOS t {r.t_OOS:.2f}", n=int(r.n_FULL), confidence="ÇOK DÜŞÜK" if not (abs(r.t_IS) > 2 and abs(r.t_OOS) > 2) else "DÜŞÜK",
            mechanism="FDR'den geçmeyen en güçlü tarama adayı (8271 testten en büyük |t|)",
            notes=f"BH geçmedi; null'da |t|>3 sayısı ort ≈21; hacim filtreli t {r.t_volf:.2f}; likidite oranı {r.liq_ratio:.2f}" + fut(r.target))
WR = pd.read_parquet(os.path.join(RES, "wide_rel.parquet"))
y = WR[(WR.lag == "1")].copy(); y["both"] = (np.sign(y.t_IS) == np.sign(y.t_OOS)) & (y.t_IS.abs() > 2) & (y.t_OOS.abs() > 2); y["a"] = y.t_FULL.abs()
for _, r in y[y.both].nlargest(10, "a").iterrows():
    add(stock=r.target, driver_yahoo=r.leader + ".IS", driver_desc=desc(r.leader), tv_ticker=tv(r.leader), relation="lead_rel", lag=1, pcorr_xu100=round(r.pc_FULL, 3), beta=round(r.b_FULL, 4),
        t_stat=round(r.t_FULL, 2), is_oos=f"IS t {r.t_IS:.2f} / OOS t {r.t_OOS:.2f}", n=int(r.n_FULL), confidence="DÜŞÜK" if r.leader in ("CCOLA", "AGHOL") else "ÇOK DÜŞÜK",
        mechanism="piyasa-göreli ({}) IS&OOS ayrı ayrı |t|>2".format(r.dep), notes="BH geçmedi; bu nitelikte 23 çift var, bağımsızlık altında ≈26 beklenir -> seçilim gürültüsü olması muhtemel" + fut(r.target))
# ---------- 5. piyasa düzeyi ----------
add(stock="XU030", driver_yahoo="THYAO.IS", driver_desc="THYAO idiosenkratik getiri_t-1", tv_ticker="BIST:THYAO", relation="lead_intra", lag=1, t_stat=3.32,
    is_oos="intra t IS 1.35 / OOS 3.08", bt_oos_sharpe=0.09, bt_oos_mean_bps=1.0, n=3180, confidence="DÜŞÜK",
    mechanism="'sistematik lider' görünümü: THYAO_t-1 -> 47 hedefin 20'sinde intra t>2; aslında tek piyasa zamanlaması (XU030 gün-içi)",
    notes="177 liderli piyasa ailesinde BH geçmedi; null'da herhangi bir liderin bu |t|'ye ulaşma olasılığı 0,12; sign BT 3 bps: OOS SR 0,09; z>1 OOS SR 1,35 ama IS 0,16 | VİOP: BIST:XU0301!")
add(stock="XU030", driver_yahoo="EW177-XU100", driver_desc="Küçük/bireysel faktör: eşit ağırlıklı 177 hisse − XU100, t-2", tv_ticker="? (BIST:XUTUM−BIST:XU100 yaklaşığı)", relation="lead_gap", lag=2,
    t_stat=3.71, is_oos="gap t IS 2.28 / OOS 3.10", n=3180, confidence="DÜŞÜK", mechanism="bireysel yatırımcı akışı/gecikmeli fiyatlama hipotezi; mekanizma belirsiz",
    notes="hisse taramasındaki gap lag-2 fazlalığının (908 p<0,05; ort t +0,56) ortak kaynağı; F>0 filtresi koşulsuz gece-long'a ek değer katmıyor (OOS SR 2,97 vs 3,76); işaret BT 3 bps SR≈0")
# ---------- 6. backtestler ----------
bt = pd.read_csv(os.path.join(RES, "bt_summary.csv"))
for _, r in bt.iterrows():
    add(stock="47 VİOP portföy" if "BT2" not in r.strategy else "VİOP çift portföyü", driver_yahoo="strateji", driver_desc=r.strategy, relation="backtest", lag=1,
        t_stat=round(r.OOS_t, 2) if pd.notna(r.OOS_t) else "", is_oos=f"IS {r.IS_mean_bps:.1f}bps SR {r.IS_sharpe:.2f} / OOS {r.OOS_mean_bps:.1f}bps SR {r.OOS_sharpe:.2f}",
        bt_oos_sharpe=round(r.OOS_sharpe, 2) if pd.notna(r.OOS_sharpe) else "", bt_oos_mean_bps=round(r.OOS_mean_bps, 1) if pd.notna(r.OOS_mean_bps) else "", n=r.OOS_n,
        confidence="—", mechanism="backtest", notes=f"pozitif yıl payı {r.years_pos_share:.2f}; yıllık bps {r.by_year_bps}")
gf = open(os.path.join(RES, "gapfade.txt")).read()
add(stock="47 VİOP portföy", driver_yahoo="küme gap sapması", driver_desc="BT3g gerçekçi giriş: küme-göreli gap_t sapması -> ~10:30'dan kapanışa", relation="backtest", lag=0,
    is_oos="2023-12..2026-10 (saatlik)", bt_oos_sharpe=-1.04, bt_oos_mean_bps=-3.0, n=717, confidence="(olumsuz) YÜKSEK",
    mechanism="kendi gap'in gün-içi kısmi dönüşü; dönüşün çoğu ilk 30 dk'da", notes="açılıştan (iyimser) 0 bps maliyet 16,3 bps/gün SR 4,4; ~10:30 girişte brüt 5,0 bps; 8 bps maliyetle -3,0 bps/gün")
F = pd.DataFrame(rows, columns=COLS)
F.to_csv(os.path.join(hdata.OUT, "f_y_hisse.csv"), index=False)
print(F.shape); print(F.relation.value_counts()); print(F.confidence.value_counts())
