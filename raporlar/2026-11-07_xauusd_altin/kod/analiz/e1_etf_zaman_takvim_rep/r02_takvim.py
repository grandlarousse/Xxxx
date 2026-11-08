"""2) Takvim iddiaları: C1 madenci takvim sepeti (ayın ilk işlem günü ∪ tatil öncesi son gün), C2 GDX tatil öncesi, C4 GLD Ocak.
Maske M_D: getiri günü D (D-1 kapanış -> D kapanış). Giriş pozisyonu pos_t = M_{t+1} (D'den önceki seansın kapanışında al)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_rep")
from rep_lib import *
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
rng = np.random.default_rng(12345)

ix = pd.Series(SESS, index=SESS)
ym = ix.dt.to_period("M")
FIRST = (ym != ym.shift(1)); FIRST.iloc[0] = True       # 2008-01-02 ayın ilk işlem günü
H = regular_holidays()
nxt = ix.shift(-1)
# tatil öncesi: d ile sonraki seans arasında düzenli (önceden ilan edilmiş) bir tatil var
hol_idx = H.index
PRE = pd.Series(False, index=SESS); PRE_NAME = pd.Series("", index=SESS)
for d, n_ in zip(SESS, nxt):
    if pd.isna(n_):
        # son seans 2026-11-06: sonraki seans 11-09, arada tatil yok
        continue
    hh = hol_idx[(hol_idx > d) & (hol_idx < n_)]
    if len(hh): PRE[d] = True; PRE_NAME[d] = H.loc[hh[0], "name"]
JAN = pd.Series(SESS.month == 1, index=SESS)
BASKET = FIRST | PRE
print("ilk gün:", int(FIRST.sum()), " tatil öncesi:", int(PRE.sum()), " sepet:", int(BASKET.sum()), " kesişim:", int((FIRST & PRE).sum()))

# analistin tatil öncesi listesiyle karşılaştırma (yalnız tarih listesi, hesap değil)
A = pd.read_csv(f"{S}/out/e1_etf_zaman_takvim/f_tatil_oncesi_gunler.csv", parse_dates=["gun"])
mine = SESS[PRE.values]
print("tatil öncesi: analist", len(A), "ben", len(mine), " yalnız analist:", list(pd.DatetimeIndex(A.gun).difference(mine).date), " yalnız ben:", list(mine.difference(pd.DatetimeIndex(A.gun)).date))

def entry(M):  # getiri günü maskesi -> giriş günü pozisyonu
    return M.astype(float).shift(-1).fillna(0.0)

R = {t: logret(t) for t in ["GLD", "IAU", "GDX", "GDXJ", "SPY", "NUGT", "JNUG", "GLDM"]}
RS = {t: np.expm1(r) for t, r in R.items()}
COST = {"GLD": (10, 20), "IAU": (10, 20), "GLDM": (10, 20), "GDX": (10, 20), "GDXJ": (10, 20), "NUGT": (20, 40), "JNUG": (20, 40)}
LEV = {"GDX": "NUGT", "GDXJ": "JNUG", "GLD": None}

def stats_block(name, M, t, h=1):
    pos = entry(M)
    y = fwd_log(R[t], h)
    x = pos.where(y.notna())
    st = dummy_test(x, y, max(h, 5))
    # NW lag duyarlılığı
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    st["t_L0"] = nw_ols(d.y.values, d.x.values, 0)[1][1]; st["t_L10"] = nw_ols(d.y.values, d.x.values, 10)[1][1]
    return pos, st

rows, bts, yrs_tab, ext_rows = [], [], [], []
CLAIMS = {"C1_sepet": BASKET, "C1a_ilk_gun": FIRST, "C2_tatil_oncesi": PRE, "C4_Ocak": JAN}
TICK = {"C1_sepet": ["GDXJ", "GDX"], "C1a_ilk_gun": ["GDXJ", "GDX"], "C2_tatil_oncesi": ["GDX", "GDXJ", "GLD"], "C4_Ocak": ["GLD", "IAU", "GLDM"]}
EXT = {"2008": ("2008-01-01", "2008-12-31"), "2013-04": ("2013-04-01", "2013-04-30"), "2020-03": ("2020-03-01", "2020-03-31"), "2026-01/02": ("2026-01-01", "2026-02-28")}
for cn, M in CLAIMS.items():
    for t in TICK[cn]:
        pos, st = stats_block(cn, M, t)
        rows.append(dict(claim=cn, etf=t, **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in st.items()}))
        rl = R[t]; rs = RS[t]
        for stress in (False, True):
            c = COST[t][1 if stress else 0]
            net, tr = bt(pos, rs, 1, c)
            for k in PERIODS:
                p = per(net, k); o = perf(p, tr)
                bh = perf(rs.reindex(p.index).dropna())["sh"]
                bts.append(dict(claim=cn, etf=t, version="yalniz_uzun", cost="stres" if stress else "temel", period=k, **o, bh_sh=bh))
            lt = LEV.get(t)
            if lt:
                cl = COST[lt][1 if stress else 0]
                netl, trl = bt(pos, RS[lt], 1, cl)
                for k in PERIODS:
                    p = per(netl, k); o = perf(p, trl)
                    bts.append(dict(claim=cn, etf=lt, version=f"kaldiracli_{lt}", cost="stres" if stress else "temel", period=k, **o, bh_sh=perf(RS[lt].reindex(p.index).dropna())["sh"]))
        for k in PERIODS:
            bts.append(dict(claim=cn, etf=t, version="demeaned_analist(donem_log)", cost="temel", period=k, sh=demeaned_sharpe(pos, rl, 1, COST[t][0], k, "period_log")))
            bts.append(dict(claim=cn, etf=t, version="demeaned_alt(tam_basit)", cost="temel", period=k, sh=demeaned_sharpe(pos, rl, 1, COST[t][0], k, "full_simple")))
        # yıl yıl net P&L
        net, tr = bt(pos, rs, 1, COST[t][0])
        yy = net.groupby(net.index.year).sum() * 100
        yy = yy[net.groupby(net.index.year).size() > 20]
        yrs_tab.append(pd.Series(yy.round(2), name=f"{cn}|{t}"))
        # uç dönemler
        allm = np.zeros(len(net), bool)
        for kk, (a, b) in EXT.items():
            m = (net.index >= a) & (net.index <= b); allm |= m
            ext_rows.append(dict(claim=cn, etf=t, donem=kk, donem_ici_net_pct=round(net[m].sum() * 100, 2), haric_sh=round(perf(net[~m])["sh"], 2)))
        ex = net[~allm]
        ext_rows.append(dict(claim=cn, etf=t, donem="hepsi_haric", donem_ici_net_pct=round(net[allm].sum() * 100, 2), haric_sh=round(perf(ex)["sh"], 2), haric_sh_oos=round(perf(ex[ex.index >= OOS_START])["sh"], 2)))

ST = pd.DataFrame(rows); ST.to_csv(f"{OUT}/r02_takvim_testleri.csv", index=False)
print(ST[["claim", "etf", "n", "n_ev", "ic", "b_bps", "ev_bps", "oth_bps", "t", "t_is", "t_oos", "t_22", "yrs", "t_L0", "t_L10"]].to_string())
BT = pd.DataFrame(bts); BT.to_csv(f"{OUT}/r02_takvim_backtest.csv", index=False)
q = BT[BT.cost == "temel"].pivot_table(index=["claim", "etf", "version"], columns="period", values="sh", aggfunc="first")[PERIODS].round(2)
print(q.to_string())
q2 = BT[(BT.period == "oos") & BT.version.str.startswith(("yalniz", "kald"))].pivot_table(index=["claim", "etf", "version"], columns="cost", values=["sh", "ann", "rt_yr", "mdd", "bh_sh"], aggfunc="first").round(2)
print(q2.to_string())
YT = pd.concat(yrs_tab, axis=1); YT.to_csv(f"{OUT}/r02_yillik_net.csv")
print(YT.round(1).to_string())
print("pozitif yıl:", {c: f"{int((YT[c].dropna() > 0).sum())}/{int(YT[c].notna().sum())}" for c in YT.columns})
EX = pd.DataFrame(ext_rows); EX.to_csv(f"{OUT}/r02_uc_donem.csv", index=False); print(EX.to_string())

# ---------- sağlamlık: SPY kontrolü, komşu gün placebo, permütasyon, tatil türü ----------
print("\nSPY kontrolü (r_ETF ~ c + r_SPY + PRE + FIRST, NW5)")
for t in ["GDX", "GDXJ", "GLD"]:
    d = pd.concat([R[t].rename("r"), R["SPY"].rename("s"), PRE.astype(float).rename("pre"), FIRST.astype(float).rename("first")], axis=1).dropna()
    for lab, dd in [("tam", d), ("OOS", d[d.index >= OOS_START])]:
        b, tv = nw_ols(dd.r.values, dd[["s", "pre", "first"]].values, 5)
        print(f"  {t} {lab}: beta_SPY={b[1]:.2f}  pre {b[2]*1e4:.1f} bps t={tv[2]:.2f} | first {b[3]*1e4:.1f} bps t={tv[3]:.2f}")

print("\nKomşu gün placebo (GDXJ / GDX ort. bps; getiri günü)")
pos_in_m = ix.groupby(ym).cumcount() + 1; pos_end = ix.groupby(ym).cumcount(ascending=False) + 1
plc = {"ilk_gun": FIRST, "2.gun": pos_in_m == 2, "3.gun": pos_in_m == 3, "son_gun": pos_end == 1, "sondan_2": pos_end == 2,
       "tatil_oncesi": PRE, "tatil_oncesinden_once": PRE.shift(-1).fillna(False).astype(bool), "tatil_sonrasi": PRE.shift(1).fillna(False).astype(bool)}
pr = []
for nm, m in plc.items():
    row = dict(gun=nm)
    for t in ["GDXJ", "GDX"]:
        r = R[t].dropna(); mm = m.reindex(r.index)
        row[f"{t}_bps"] = round(r[mm].mean() * 1e4, 1); row[f"{t}_n"] = int(mm.sum())
        b, tv = nw_ols(r.values, mm.astype(float).values, 5); row[f"{t}_t"] = round(tv[1], 2)
    pr.append(row)
PL = pd.DataFrame(pr); PL.to_csv(f"{OUT}/r02_komsu_gun.csv", index=False); print(PL.to_string())

print("\nYıl-içi permütasyon (5000; tek yönlü p; olay günü ortalama getiri)")
perm = []
for nm, m in [("sepet", BASKET), ("ilk_gun", FIRST), ("tatil_oncesi", PRE)]:
    for t in ["GDXJ", "GDX"]:
        r = R[t].dropna(); mm = m.reindex(r.index).values; yrs = r.index.year.values; rv = r.values
        obs = rv[mm].mean()
        groups = [(np.where(yrs == y)[0], int(mm[yrs == y].sum())) for y in np.unique(yrs)]
        B = 5000; sims = np.zeros(B)
        tot = mm.sum()
        for b in range(B):
            s = 0.0
            for idx, k in groups:
                if k: s += rv[rng.choice(idx, k, replace=False)].sum()
            sims[b] = s / tot
        p = (np.sum(sims >= obs) + 1) / (B + 1)
        perm.append(dict(test=nm, etf=t, obs_bps=round(obs * 1e4, 1), sim_mean_bps=round(sims.mean() * 1e4, 1), p=round(p, 4)))
PM = pd.DataFrame(perm); PM.to_csv(f"{OUT}/r02_permutasyon.csv", index=False); print(PM.to_string())

print("\nTatil türüne göre (tatil öncesi gün getirisi, bps)")
tt = pd.DataFrame({"tatil": PRE_NAME[PRE], "GDX": R["GDX"][PRE] * 1e4, "GDXJ": R["GDXJ"][PRE] * 1e4, "GLD": R["GLD"][PRE] * 1e4})
g = tt.groupby("tatil")[["GDX", "GDXJ", "GLD"]].mean().round(1); g["n"] = tt.groupby("tatil").size()
print(g.sort_values("GDX", ascending=False).to_string()); g.to_csv(f"{OUT}/r02_tatil_turu.csv")

# erken kapanışla çakışan olay günleri (bilgi: çıkış 13:00 ET kapanışında)
EC = early_closes()
print("\nerken kapanış günü olan tatil öncesi günler:", int(PRE[PRE.index.isin(EC)].sum()), "/", int(PRE.sum()))
# sepet: ardışık olay günü (2 gün tutuş) sayısı
pos = entry(BASKET); print("sepet giriş sayısı (0->1):", int((pos.diff() == 1).sum()), " olay günü:", int(BASKET.sum()))
