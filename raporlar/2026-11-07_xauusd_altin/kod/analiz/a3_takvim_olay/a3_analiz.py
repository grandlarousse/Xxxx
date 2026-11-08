"""a3_takvim_olay — Takvim ve olay etkileri, VİOP F_XAUUSD (giriş gün t uzlaşması ~15:10 UTC, çıkış t+h uzlaşması).
Çalıştır:  python3 -W ignore build_events.py && python3 -W ignore a3_analiz.py
Çıktılar:  results_all.csv (her test bir satır), registry (out/registry/a3_takvim_olay.csv; her çalıştırmada sıfırlanır), stdout özet.

Yöntem
- Takvim/olay kukla testi: D_t=1 ise gün t uzlaşmasında gir, h gün tut. y = fwd{h}. Fark = ort(y|D=1) - ort(y|D=0); t = Newey-West (lag=max(h,5))
  ile y ~ a + b*D regresyonunun t'si (lib_altin.ic, method='pearson' ile aynı). IS 2017-03..2021-12, OOS 2022-01.., yıl yıl fark işareti.
- Koşullu olay testi (CPI/NFP/FOMC tepki yönü): yalnız olay günlerinde x=sign(tepki); y=fwd{h}; olay örnekleminde IC + NW t.
- Erken dönem: aynı tanımlar spot panelde (Dukascopy 15:00 UTC -> 15:00 UTC, sfwd{h}), 2010-01..2017-03.
- Backtest: pos = sign(IS farkı) x D  (yön yalnız IS'ten). bt_summary (5 bps), stres 10 bps, demeaned Sharpe, uzun/kısa bacak.
- Sağlamlık: Mart 2020 ve Ocak-Şubat 2026 hariç; roll günü (v_code değişimi) içeren pencereler hariç; %0,5 winsorize; Spearman.
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
O = os.path.dirname(os.path.abspath(__file__)); S = os.path.abspath(f"{O}/../..")
sys.path.insert(0, f"{S}/code"); sys.path.insert(0, f"{O}/pylib")
from lib_altin import *
import holidays

AG = "a3_takvim_olay"
REG = f"{REG_DIR}/{AG}.csv"
if os.path.exists(REG): os.remove(REG)

d = load_viop(); s = load_spot()
V = d.index; SP = s.index
r_v = d.v_ret; Y_V = {h: d[f"fwd{h}"] for h in (1, 3, 5)}
s_e = s[s.index < "2017-03-06"]; SPE = s_e.index
Y_S = {h: s_e[f"sfwd{h}"] for h in (1, 3, 5)}
OOS0 = IS_END

# ---------------- yardımcılar ----------------
def first_ge(idx, dates, strict=False):
    """her tarih için idx'te ilk >= (strict: >) günün konumu; dışarıda kalanlar atılır."""
    a = idx.values; q = pd.DatetimeIndex(pd.to_datetime(pd.Series(dates)).dropna()).values
    p = np.searchsorted(a, q, side="right" if strict else "left")
    return np.unique(p[p < len(idx)])

def dummy(idx, p, shift=0):
    p = np.asarray(p, int) + shift; p = p[(p >= 0) & (p < len(idx))]
    D = pd.Series(0.0, index=idx); D.iloc[np.unique(p)] = 1.0; return D

def cal_pos(idx):
    """ay içi işlem günü sırası: tdm (1..), tde (0=son gün)."""
    g = pd.Series(np.arange(len(idx)), index=idx).groupby([idx.year, idx.month])
    tdm = g.cumcount() + 1; n = g.transform("size"); tde = n - tdm
    return tdm.values, tde.values

OUTLIER = lambda idx: ((idx >= "2020-03-01") & (idx <= "2020-03-31")) | ((idx >= "2026-01-01") & (idx <= "2026-02-28"))
roll_day = (d.v_code != d.v_code.shift()).astype(float); roll_day.iloc[0] = 0
def touches_roll(h):  # t+1..t+h penceresinde roll günü var mı
    return sum(roll_day.shift(-k).fillna(0) for k in range(1, h + 1)) > 0

def yr_sign(x, y, dummy_mode, min_ev=1, min_obs=4):
    dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna(); out = {}
    for yy, g in dd.groupby(dd.index.year):
        if dummy_mode:
            if (g.x == 1).sum() >= min_ev and (g.x == 0).sum() >= 5: out[yy] = g.y[g.x == 1].mean() - g.y[g.x == 0].mean()
        else:
            if len(g) >= min_obs and g.x.std() > 0: out[yy] = g.x.corr(g.y)
    return pd.Series(out, dtype=float)

def stats_block(x, y, h, dummy_mode):
    L = max(h, 5)
    full = ic(x, y, L, "pearson")
    msk_is = x.index <= OOS0
    isr = ic(x[msk_is], y[msk_is], L, "pearson"); oos = ic(x[~msk_is], y[~msk_is], L, "pearson")
    yr = yr_sign(x, y, dummy_mode); sg = np.sign(full["ic"]) if np.isfinite(full["ic"]) else 0
    o = dict(ic=full["ic"], t=full["t"], n=full["n"], ic_is=isr["ic"], t_is=isr["t"], ic_oos=oos["ic"], t_oos=oos["t"],
             yrs_same_sign=int((np.sign(yr) == sg).sum()), yrs=int(yr.notna().sum()), by_year={int(k): round(v * (1e4 if dummy_mode else 1), 1 if dummy_mode else 3) for k, v in yr.items()})
    dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    if dummy_mode:
        e = dd[dd.x == 1]; ne = dd[dd.x == 0]
        o.update(n_ev=int(len(e)), mean_ev_bps=e.y.mean() * 1e4, mean_non_bps=ne.y.mean() * 1e4, diff_bps=(e.y.mean() - ne.y.mean()) * 1e4,
                 diff_is_bps=(e.y[e.index <= OOS0].mean() - ne.y[ne.index <= OOS0].mean()) * 1e4,
                 diff_oos_bps=(e.y[e.index > OOS0].mean() - ne.y[ne.index > OOS0].mean()) * 1e4, hit_ev=(e.y > 0).mean())
    else:
        o.update(n_ev=int(len(dd)), mean_ev_bps=(np.sign(dd.x) * dd.y).mean() * 1e4, diff_bps=(np.sign(dd.x) * dd.y).mean() * 1e4,
                 diff_is_bps=(np.sign(dd.x) * dd.y)[dd.index <= OOS0].mean() * 1e4, diff_oos_bps=(np.sign(dd.x) * dd.y)[dd.index > OOS0].mean() * 1e4,
                 hit_ev=((np.sign(dd.x) * dd.y) > 0).mean())
    # sağlamlık
    keep = ~OUTLIER(x.index)
    o["t_ex_outlier"] = ic(x[keep], y[keep], L, "pearson")["t"]
    yw = y.clip(y.quantile(0.005), y.quantile(0.995)); o["t_wins"] = ic(x, yw, L, "pearson")["t"]
    o["t_spear"] = ic(x, y, L, "spearman")["t"]
    return o

RESULTS = []
def run(test_id, family, desc, h, xv, xs=None, dummy_mode=True, mech="", info="takvim önceden bilinir", entry="", roll_check=True):
    """xv: VİOP takvimli seri (kukla 0/1 ya da olay günlerinde işaret, diğerleri NaN). xs: spot erken dönem eşleniği."""
    y = Y_V[h]
    st = stats_block(xv, y, h, dummy_mode)
    if roll_check:
        tr = touches_roll(h); keep = ~tr.reindex(xv.index).fillna(False).astype(bool)
        st["t_ex_roll"] = ic(xv[keep], y[keep], max(h, 5), "pearson")["t"]
    # erken dönem spot
    if xs is not None:
        es = stats_block(xs, Y_S[h], h, dummy_mode); st.update(early_t=es["t"], early_diff_bps=es["diff_bps"], early_n_ev=es["n_ev"],
                                                               early_yrs_same=es["yrs_same_sign"], early_yrs=es["yrs"])
    # backtest: yön yalnız IS'ten
    sgn_is = np.sign(st["diff_is_bps"]) if np.isfinite(st["diff_is_bps"]) else 1.0
    pos = (xv.fillna(0) if dummy_mode else np.sign(xv).fillna(0)) * sgn_is
    bs = bt_summary(pos, r_v, h)
    oos = r_v.index > OOS0
    b10 = backtest(pos[oos], r_v[oos], h, 10.0)
    bl = backtest(pos.clip(lower=0)[oos], r_v[oos], h); bsh = backtest(pos.clip(upper=0)[oos], r_v[oos], h)
    bh_oos = backtest(pd.Series(1.0, index=r_v[oos].index), r_v[oos], 1, 0)
    ev_per_yr = float((pos != 0).sum() / (len(V) / 252))
    st.update(sgn_is=sgn_is, sh_full=bs["full"]["sharpe"], sh_is=bs["is"]["sharpe"], sh_oos=bs["oos"]["sharpe"], sh_oos_dm=bs["oos"]["sharpe_demeaned"],
              sh_full_dm=bs["full"]["sharpe_demeaned"], ann_oos=bs["oos"]["ann"], sh_oos_10bps=b10 and round(b10["sharpe"], 2),
              sh_oos_long=bl and round(bl["sharpe"], 2), sh_oos_short=bsh and round(bsh["sharpe"], 2), bh_sh_full=bs["buyhold_sharpe_full"],
              bh_sh_oos=round(bh_oos["sharpe"], 2), exposure=bs["full"]["exposure"], trades_per_year=round(ev_per_yr, 1))
    note = json.dumps(dict(desc=desc, diff_bps=round(st["diff_bps"], 1), n_ev=st["n_ev"], early_t=st.get("early_t"), sh_oos=st["sh_oos"], sh_oos_dm=st["sh_oos_dm"]), ensure_ascii=False)
    register(AG, family, test_id, desc, h, st, note=note)
    row = dict(test_id=test_id, family=family, desc=desc, h=h, mech=mech, info=info, entry=entry, **{k: v for k, v in st.items() if k != "by_year"}, by_year=json.dumps(st["by_year"]))
    RESULTS.append(row)
    return st

# ---------------- takvim konumları ----------------
tdm_v, tde_v = cal_pos(V); tdm_s, tde_s = cal_pos(SPE)
ms_v = pd.Series(V.month, index=V); ms_s = pd.Series(SPE.month, index=SPE)

# ============ 1) Haftanın günü (giriş günü) ============
WD = ["Pzt", "Sal", "Çar", "Per", "Cum"]
for w in range(5):
    for h in (1, 3, 5):
        xv = pd.Series((V.dayofweek == w).astype(float), index=V); xs = pd.Series((SPE.dayofweek == w).astype(float), index=SPE)
        run(f"DOW_entry_{WD[w]}_h{h}", "haftanin_gunu", f"giriş günü={WD[w]} (h=1'de getiri günü = sonraki iş günü)", h, xv, xs,
            mech="zayıf: likidite/hafta sonu riski (Lucey-Tully Pazartesi negatif)", entry=f"{WD[w]} uzlaşması")

# ============ 2) Ay dönümü ============
for lab, cond_v, cond_s in [("TDE3", tde_v == 3, tde_s == 3), ("TDE2", tde_v == 2, tde_s == 2), ("TDE1", tde_v == 1, tde_s == 1), ("TDE0", tde_v == 0, tde_s == 0),
                            ("TDM1", tdm_v == 1, tdm_s == 1), ("TDM2", tdm_v == 2, tdm_s == 2), ("TDM3", tdm_v == 3, tdm_s == 3)]:
    for h in (1, 3, 5):
        run(f"TOM_entry_{lab}_h{h}", "ay_donumu", f"giriş = ayın {lab} günü (TDE0=son işlem günü, TDM1=ilk)", h,
            pd.Series(cond_v.astype(float), index=V), pd.Series(cond_s.astype(float), index=SPE),
            mech="ay sonu/başı fon girişleri, ETF yaratımı, yeniden dengeleme (Incrementum GLD ilk gün)", entry=f"{lab} uzlaşması")

# ============ 3) Ay mevsimselliği (getiri gününün ayı, h=1) ============
nxt_m_v = pd.Series(np.r_[V.month[1:], [np.nan]], index=V); nxt_m_s = pd.Series(np.r_[SPE.month[1:], [np.nan]], index=SPE)
AY = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
for m in range(1, 13):
    run(f"MONTH_{AY[m-1]}_h1", "ay_mevsim", f"getiri günü {AY[m-1]} ayında", 1, (nxt_m_v == m).astype(float), (nxt_m_s == m).astype(float),
        mech="Baur 2013 Eyl/Kas+, WGC Ocak+, Hindistan/Çin talep mevsimi", entry="o aydaki her gün")
run("MONTH_SepNov_h1", "ay_mevsim", "getiri günü Eylül ya da Kasım (Baur 2013)", 1, nxt_m_v.isin([9, 11]).astype(float), nxt_m_s.isin([9, 11]).astype(float),
    mech="Baur 2013 sonbahar etkisi")
run("MONTH_Winter_h1", "ay_mevsim", "getiri günü Ara-Oca-Şub (kış etkisi, Potrykus 2024)", 1, nxt_m_v.isin([12, 1, 2]).astype(float), nxt_m_s.isin([12, 1, 2]).astype(float),
    mech="Potrykus-Augustynowicz 2024 kış etkisi; Çin Yeni Yılı stok")

# ============ 4) Çeyrek ve yıl sonu ============
qm_v = np.isin(V.month, [3, 6, 9, 12]); qm_s = np.isin(SPE.month, [3, 6, 9, 12])
for h in (1, 3, 5):
    run(f"QEND_TDE1_h{h}", "ceyrek_yil", "çeyrek son ayı, sondan 2. gün giriş", h, pd.Series((qm_v & (tde_v == 1)).astype(float), index=V),
        pd.Series((qm_s & (tde_s == 1)).astype(float), index=SPE), mech="çeyrek sonu pencere süsleme/yeniden dengeleme")
    run(f"YEND_TDE1_h{h}", "ceyrek_yil", "Aralık sondan 2. gün giriş (yıl dönümü)", h, pd.Series(((V.month == 12) & (tde_v == 1)).astype(float), index=V),
        pd.Series(((SPE.month == 12) & (tde_s == 1)).astype(float), index=SPE), mech="yıl sonu vergi/yeniden dengeleme, Ocak etkisi")
run("QEND_last5_h5", "ceyrek_yil", "çeyrek son ayının son 5 günü (giriş TDE5)", 5, pd.Series((qm_v & (tde_v == 5)).astype(float), index=V),
    pd.Series((qm_s & (tde_s == 5)).astype(float), index=SPE), mech="çeyrek sonu yeniden dengeleme")

# ============ 5) FOMC ============
fomc = pd.read_csv(f"{O}/events_fomc.csv", parse_dates=["date"]); fomc = fomc[fomc.scheduled]
F_ret_v = first_ge(V, fomc.date, strict=True); F_ret_s = first_ge(SPE, fomc.date, strict=True)   # açıklama uzlaşmadan SONRA -> ertesi günün getirisi
Fe_v = F_ret_v - 1; Fe_s = F_ret_s - 1  # FOMC günü (ya da öncesindeki son) uzlaşması = açıklamayı taşıyan giriş
for h in (1, 3, 5):
    run(f"FOMC_entryF_h{h}", "fomc", "FOMC günü uzlaşmasında gir (açıklama 18/19 UTC'yi taşır)", h, dummy(V, Fe_v), dummy(SPE, Fe_s),
        mech="para politikası sürprizi; gevşek sürprize asimetrik tepki (Awartani+ 2024)", entry="FOMC karar günü uzlaşması")
for k in (1, 2, 3):
    run(f"FOMC_pre_F-{k}_h1", "fomc", f"FOMC'den {k} gün önce gir, 1 gün tut (açıklama öncesi)", 1, dummy(V, Fe_v, -k), dummy(SPE, Fe_s, -k),
        mech="FOMC öncesi sürüklenme (Lucca-Moench hisse; altın için kanıt yok)")
run("FOMC_pre_F-3_h3", "fomc", "FOMC'den 3 gün önce gir, FOMC günü uzlaşmasında çık", 3, dummy(V, Fe_v, -3), dummy(SPE, Fe_s, -3), mech="FOMC öncesi sürüklenme")
run("FOMC_pre_F-5_h5", "fomc", "FOMC'den 5 gün önce gir, FOMC günü uzlaşmasında çık", 5, dummy(V, Fe_v, -5), dummy(SPE, Fe_s, -5), mech="FOMC öncesi belirsizlik primi")
for h in (1, 3, 5):
    run(f"FOMC_post_F+1_h{h}", "fomc", "FOMC ertesi gün uzlaşmasında gir (tepki sonrası)", h, dummy(V, Fe_v, 1), dummy(SPE, Fe_s, 1), mech="FOMC sonrası sürüklenme")
sep = fomc[fomc.label.str.contains(r"\*", regex=True) | fomc.date.dt.month.isin([3, 6, 9, 12])]
run("FOMC_SEP_entryF_h1", "fomc", "yalnız SEP (projeksiyon) toplantıları, FOMC günü gir", 1, dummy(V, first_ge(V, sep.date, True) - 1), dummy(SPE, first_ge(SPE, sep.date, True) - 1),
    mech="SEP/dot-plot daha büyük sürpriz")
# koşullu: FOMC tepkisinin yönü (F+1 günü 15:00 UTC'de bilinen spot değişimi: F 15:00 -> F+1 15:00) ile F+1 girişinde sürüklenme/dönüş
reac_v = np.log(d.xau_p15 / d.xau_p15_prev); reac_s = np.log(s_e.xau_p15 / s_e.xau_p15_prev)
def on_events(series, idx, p):
    x = pd.Series(np.nan, index=idx); p = p[(p >= 0) & (p < len(idx))]; x.iloc[p] = series.iloc[p].values; return x
for h in (1, 3, 5):
    run(f"FOMC_cond_spot_h{h}", "fomc", "F+1 girişinde x=sign(spot 15:00 F->F+1 tepki) [15:00 UTC bilinir]", h, on_events(reac_v, V, F_ret_v), on_events(reac_s, SPE, F_ret_s),
        dummy_mode=False, mech="tepki sürüklenmesi (yetersiz tepki) ya da aşırı tepki dönüşü", info="F+1 15:00 UTC spot (cutoff öncesi)")
    run(f"FOMC_cond_close_h{h}", "fomc", "F+1 girişinde x=sign(v_ret F+1) [KAPANIŞTA HESAPLANAN, 15:10 UTC]", h, on_events(r_v, V, F_ret_v), on_events(s_e.s_ret, SPE, F_ret_s),
        dummy_mode=False, mech="tepki sürüklenmesi/dönüşü", info="F+1 15:10 UTC uzlaşma (kapanışta hesaplanan)")

# ============ 6) CPI / NFP (12:30/13:30 UTC, gün t getirisinin içinde) ============
tr_half = set()
bay = pd.read_csv(f"{O}/events_tr_bayram.csv", parse_dates=["start", "arife"])
tr_half |= set(bay.arife); tr_half |= set(pd.Timestamp(y, 10, 28) for y in range(2009, 2027))
half_v = pd.Series(V.isin(list(tr_half)), index=V)
r1_v = np.log(d.xau_p15 / d.xau_p12).where(~half_v); r1_s = np.log(s_e.xau_p15 / s_e.xau_p12)
for nm, fn in [("CPI", "events_us_cpi.csv"), ("NFP", "events_us_nfp.csv")]:
    ev = pd.read_csv(f"{O}/{fn}", parse_dates=["date"])
    E_v = first_ge(V, ev.date); E_s = first_ge(SPE, ev.date)
    sameday_v = E_v[np.isin(V[E_v], ev.date.values)]  # yalnız VİOP'un açık olduğu yayım günleri (koşullu testler)
    sameday_s = E_s[np.isin(SPE[E_s], ev.date.values)]
    run(f"{nm}_pre_h1", "cpi_nfp", f"{nm} gününden önceki uzlaşmada gir, 1 gün (veri riskini taşı)", 1, dummy(V, E_v, -1), dummy(SPE, E_s, -1),
        mech="veri belirsizlik primi")
    for h in (1, 3, 5):
        run(f"{nm}_post_h{h}", "cpi_nfp", f"{nm} günü uzlaşmasında gir (koşulsuz sonrası)", h, dummy(V, E_v), dummy(SPE, E_s), mech="veri sonrası sürüklenme")
        run(f"{nm}_cond_spot12to15_h{h}", "cpi_nfp", f"{nm} günü x=sign(spot 12:00->15:00 UTC) [15:00 bilinir], gün t uzlaşmasında gir", h,
            on_events(r1_v, V, sameday_v), on_events(r1_s, SPE, sameday_s), dummy_mode=False,
            mech="sürpriz tepkisinin sürüklenmesi/dönüşü (Elder+ 2012: dakikalar içinde söner)", info="gün t 15:00 UTC spot")
        run(f"{nm}_cond_close_h{h}", "cpi_nfp", f"{nm} günü x=sign(v_ret_t) [KAPANIŞTA HESAPLANAN]", h, on_events(r_v, V, sameday_v), on_events(s_e.s_ret, SPE, sameday_s),
            dummy_mode=False, mech="tepki sürüklenmesi/dönüşü", info="gün t 15:10 UTC uzlaşma (kapanışta)")

# ============ 7) Tatiller (piyasa bazında) ============
yrs = range(2009, 2028)
HOL = {"NYSE": set(pd.Timestamp(x) for x in holidays.financial_holidays("NYSE", years=yrs).keys()),
       "LSE": set(pd.Timestamp(x) for x in holidays.financial_holidays("XLON", years=yrs).keys()),
       "SSE": set(pd.Timestamp(x) for x in holidays.financial_holidays("XSHG", years=yrs).keys())}
def blocks(hset):
    """hafta içi tatil blokları: (önceki işlem günü, sonraki işlem günü) — hafta sonları köprü sayılır."""
    hs = sorted(x for x in hset if x.dayofweek < 5); out = []; bd = pd.bdate_range("2008-12-01", "2027-12-31", freq="C", holidays=sorted(hset))
    for x in hs:
        p = bd[bd < x][-1]; n = bd[bd > x][0]; out.append((p, n, x))
    return pd.DataFrame(out, columns=["pre", "post", "hol"]).drop_duplicates(["pre", "post"])
for mk in ["NYSE", "LSE", "SSE"]:
    b = blocks(HOL[mk])
    # (a) tatil öncesi son işlem gününün getirisi: giriş bir önceki gün, h=1
    pv = first_ge(V, b.pre); pv = pv[np.isin(V[pv], b.pre.values)]; ps = first_ge(SPE, b.pre); ps = ps[np.isin(SPE[ps], b.pre.values)]
    run(f"HOL_{mk}_pre_h1", "tatil", f"{mk} tatilinden önceki son işlem gününün getirisi (giriş bir gün önce)", 1, dummy(V, pv, -1), dummy(SPE, ps, -1),
        mech="tatil öncesi etkisi (Fabozzi+ 1994), pozisyon kapatma")
    # (b) tatil(ler)i kapsayan getiri: giriş tatil öncesi son gün, h=1 (VİOP açık ise tatil günü getirisi)
    run(f"HOL_{mk}_over_h1", "tatil", f"{mk} tatil öncesi son gün gir, 1 gün (ince piyasa/tatil günü)", 1, dummy(V, pv), dummy(SPE, ps),
        mech="ana piyasa kapalıyken ince likidite")
    # (c) tatil sonrası ilk günün getirisi
    qv = first_ge(V, b.post); qv = qv[np.isin(V[qv], b.post.values)]; qs = first_ge(SPE, b.post); qs = qs[np.isin(SPE[qs], b.post.values)]
    run(f"HOL_{mk}_post_h1", "tatil", f"{mk} tatil sonrası ilk günün getirisi (giriş bir gün önce)", 1, dummy(V, qv, -1), dummy(SPE, qs, -1),
        mech="tatil dönüşü birikmiş talep")
    if mk == "SSE":
        run(f"HOL_{mk}_post_h5", "tatil", "SSE tatil sonrası ilk günden itibaren 5 gün (giriş ilk gün öncesi)", 5, dummy(V, qv, -1), dummy(SPE, qs, -1), mech="Çin dönüş talebi")

# TR tatilleri: VİOP kapalı -> giriş son VİOP gününde, getiri tatili kapsar. Gün sayısıyla normalize edilmiş (spot iş günü başına) hedef ayrıca.
gaps = pd.Series(V[1:], index=V[:-1]); bdays_between = pd.Series([len(pd.bdate_range(a, b)) - 1 for a, b in zip(V[:-1], V[1:])], index=V[:-1])
trpre = bdays_between[bdays_between > 1].index  # ertesi VİOP günü 1'den fazla iş günü sonra
pv = np.searchsorted(V.values, trpre.values)
for h in (1, 3, 5):
    run(f"HOL_TR_pre_h{h}", "tatil", "TR tatili (VİOP kapalı) öncesi son VİOP gününde gir", h, dummy(V, pv), None,
        mech="Türk yatırımcı tatil öncesi pozisyon kapatma/hedge; tatilde küresel hareket birikir", entry="TR tatil öncesi uzlaşma")
# normalize: fwd1 / kapsanan iş günü
yn = (Y_V[1] / bdays_between.reindex(V).fillna(1))
st = stats_block(dummy(V, pv), yn, 1, True); st["t_ex_roll"] = np.nan
register(AG, "tatil", "HOL_TR_pre_h1_perday", "TR tatili öncesi giriş, getiri / kapsanan iş günü", 1, st, note="normalize")
RESULTS.append(dict(test_id="HOL_TR_pre_h1_perday", family="tatil", desc="TR tatil öncesi giriş; fwd1/iş günü sayısı", h=1, mech="", info="takvim",
                    **{k: v for k, v in st.items() if k != "by_year"}, by_year=json.dumps(st["by_year"])))
qv = pv + 1
for h in (1, 3, 5):
    run(f"HOL_TR_post_h{h}", "tatil", "TR tatili sonrası ilk VİOP günü uzlaşmasında gir", h, dummy(V, qv), None, mech="tatil dönüşü yurt içi talep")
# Bayram (Ramazan/Kurban): arife yarım gün (~10:00 UTC uzlaşma)
ar_v = first_ge(V, bay.arife); ar_v = ar_v[np.isin(V[ar_v], bay.arife.values)]
run("BAYRAM_arifeday_h1", "tatil", "arife (yarım gün) getirisi: arifeden önceki gün gir", 1, dummy(V, ar_v, -1), None, mech="bayram öncesi yurt içi altın talebi (hediye)")
for h in (1, 3, 5):
    pre_b = np.searchsorted(V.values, bay.start.values) - 1; pre_b = pre_b[(pre_b >= 0) & (V[np.clip(pre_b, 0, len(V) - 1)] >= V[0])]
    run(f"BAYRAM_pre_h{h}", "tatil", "bayram öncesi son VİOP günü (arife) uzlaşmasında gir", h, dummy(V, pre_b), None, mech="bayram tatilinde küresel hareket birikir")
    post_b = np.searchsorted(V.values, bay.start.values)
    run(f"BAYRAM_post_h{h}", "tatil", "bayram sonrası ilk VİOP günü gir", h, dummy(V, post_b), None, mech="bayram dönüşü")

# ============ 8) COMEX OG opsiyon vadesi, GC FND, BCOM roll ============
cx = pd.read_csv(f"{O}/events_comex.csv", parse_dates=["og_expiry", "og_alt", "gc_fnd", "bcom_roll_start", "bcom_roll_end"])
OE_v = first_ge(V, cx.og_expiry); OE_s = first_ge(SPE, cx.og_expiry)        # OE günü uzlaşması (13:30 ET vade bitişinden ÖNCE)
maj = cx[cx.month.str[-2:].isin(["01", "03", "05", "07", "09", "11"])]
OEm_v = first_ge(V, maj.og_expiry); OEm_s = first_ge(SPE, maj.og_expiry)
run("OG_pre5_h5", "comex_vade", "OG vadesinden 5 gün önce gir, OE günü uzlaşmasında çık", 5, dummy(V, OE_v, -5), dummy(SPE, OE_s, -5), mech="opsiyon vadesi öncesi pinning/dealer hedge baskısı")
run("OG_pre3_h3", "comex_vade", "OG vadesinden 3 gün önce gir, OE günü uzlaşmasında çık", 3, dummy(V, OE_v, -3), dummy(SPE, OE_s, -3), mech="vade öncesi baskı")
run("OG_OEday_h1", "comex_vade", "OE günü getirisi (önceki gün gir)", 1, dummy(V, OE_v, -1), dummy(SPE, OE_s, -1), mech="vade günü pinning")
for h in (1, 3, 5):
    run(f"OG_post_h{h}", "comex_vade", "OE günü uzlaşmasında gir (vade sonrası serbest kalma)", h, dummy(V, OE_v), dummy(SPE, OE_s), mech="vade sonrası delta-hedge çözülmesi")
run("OGmaj_pre5_h5", "comex_vade", "yalnız ana (GC aktif ay) OG vadesi, 5 gün önce gir", 5, dummy(V, OEm_v, -5), dummy(SPE, OEm_s, -5), mech="ana vade pinning")
run("OGmaj_post_h5", "comex_vade", "yalnız ana OG vadesi, OE günü gir", 5, dummy(V, OEm_v), dummy(SPE, OEm_s), mech="ana vade sonrası")
fnd = cx.gc_fnd.dropna()
FN_v = first_ge(V, fnd); FN_s = first_ge(SPE, fnd)
run("GCFND_roll_h5", "comex_vade", "GC ilk bildirim gününden 6 gün önce gir (roll penceresi FND-5..FND-1)", 5, dummy(V, FN_v, -6), dummy(SPE, FN_s, -6), mech="spekülatif uzun roll/likidasyon baskısı")
run("GCFND_day_h1", "comex_vade", "FND günü getirisi", 1, dummy(V, FN_v, -1), dummy(SPE, FN_s, -1), mech="ilk bildirim")
run("GCFND_post_h5", "comex_vade", "FND günü gir, 5 gün", 5, dummy(V, FN_v), dummy(SPE, FN_s), mech="roll sonrası")
bc = cx.bcom_roll_start.dropna()
BC_v = first_ge(V, bc); BC_s = first_ge(SPE, bc)
run("BCOM_roll_h5", "comex_vade", "BCOM roll penceresi (6.-10. iş günü, Oca/Mar/May/Tem/Kas): 5. iş günü gir", 5, dummy(V, BC_v, -1), dummy(SPE, BC_s, -1), mech="endeks roll akışı (yön değil spread)")

# ============ 9) VİOP kendi vadesi ve roll ============
vexp = pd.Series(pd.to_datetime(d.v_expiry.dropna().unique())); vexp = vexp[vexp <= V[-1]]
VE_v = first_ge(V, vexp); VE_v = np.array([p if V[p] == e else p - 1 for p, e in zip(first_ge(V, vexp), vexp)])
run("VEXP_last5_h5", "viop_vade", "VİOP vade son 5 günü (vade-5'te gir, vade günü çık)", 5, dummy(V, VE_v, -5), None, mech="LBMA PM nihai uzlaşmaya yakınsama, roll akışı")
run("VEXP_day_h1", "viop_vade", "VİOP vade günü getirisi (aktif kontrat)", 1, dummy(V, VE_v, -1), None, mech="nihai uzlaşma günü")
run("VEXP_post_h5", "viop_vade", "VİOP vade günü gir, 5 gün", 5, dummy(V, VE_v), None, mech="vade sonrası")
rp = np.where(roll_day.values == 1)[0]
run("VROLL_day_h1", "viop_vade", "aktif kontrat değişim (roll) günü getirisi", 1, dummy(V, rp, -1), None, mech="roll günü gürültüsü (sağlamlık)", roll_check=False)

# ============ 10) Asya festivalleri ============
asia = pd.read_csv(f"{O}/events_asya_festival.csv", parse_dates=["date"])
bS = blocks(HOL["SSE"])
def sse_block_for(dates):
    pre, post = [], []
    for x in dates:
        m = bS[(bS.pre < x) & (bS.post > x)]
        if len(m): pre.append(m.pre.iloc[0]); post.append(m.post.iloc[0])
    return pd.Series(pre), pd.Series(post)
for ev, lab in [("CNY", "Çin Yeni Yılı"), ("GOLDEN_WEEK", "Ekim Altın Haftası")]:
    dts = asia[asia.event == ev].date
    pre, post = sse_block_for(dts)
    Lv = np.searchsorted(V.values, pre.values, side="right") - 1; Ls = np.searchsorted(SPE.values, pre.values, side="right") - 1   # son SSE günü (ya da öncesi) VİOP konumu
    Pv = first_ge(V, post); Ps = first_ge(SPE, post)
    run(f"{ev}_pre5_h5", "asya", f"{lab} öncesi son 5 gün (SSE kapanmadan önceki 5 günün getirisi)", 5, dummy(V, Lv, -5), dummy(SPE, Ls, -5), mech="tatil öncesi Çin stok yenileme (WGC)")
    run(f"{ev}_pre10_h5", "asya", f"{lab} öncesi 10..6. günler", 5, dummy(V, Lv, -10), dummy(SPE, Ls, -10), mech="erken stok yenileme")
    run(f"{ev}_during_h5", "asya", f"{lab} sırasında (SSE kapalı) 5 gün", 5, dummy(V, Lv), dummy(SPE, Ls), mech="Çin talebi yokken")
    run(f"{ev}_post_h5", "asya", f"{lab} sonrası SSE açılışından itibaren 5 gün", 5, dummy(V, Pv, -1), dummy(SPE, Ps, -1), mech="dönüş talebi")
for ev, lab in [("DHANTERAS", "Dhanteras"), ("AKSHAYA", "Akshaya Tritiya")]:
    dts = asia[asia.event == ev].date
    Ev = first_ge(V, dts); Es = first_ge(SPE, dts)
    run(f"{ev}_pre5_h5", "asya", f"{lab} öncesi 5 gün (Dhanteras/AT'den önceki son 5 getiri)", 5, dummy(V, Ev, -6), dummy(SPE, Es, -6), mech="Hindistan festival alımı")
    run(f"{ev}_post5_h5", "asya", f"{lab} sonrası 5 gün", 5, dummy(V, Ev, 0), dummy(SPE, Es, 0), mech="festival sonrası talep düşüşü")

# ---------------- kayıt ----------------
R = pd.DataFrame(RESULTS)
from scipy import stats as sst
R["p"] = 2 * (1 - sst.norm.cdf(R.t.abs())); R["q_bh"] = bh_fdr(R.p.fillna(1).values)
R.to_csv(f"{O}/results_all.csv", index=False)
print("TOPLAM TEST:", len(R), "| registry satır:", len(pd.read_csv(REG)))
print("|t|>=2:", int((R.t.abs() >= 2).sum()), " |t|>=3:", int((R.t.abs() >= 3).sum()), " min q:", round(R.q_bh.min(), 3))
cols = ["test_id", "n_ev", "diff_bps", "t", "t_is", "t_oos", "yrs_same_sign", "yrs", "early_t", "t_ex_outlier", "t_ex_roll", "t_spear", "sh_oos", "sh_oos_dm", "q_bh"]
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 400)
print(R.sort_values("t", key=abs, ascending=False)[cols].head(40).round(2).to_string(index=False))
