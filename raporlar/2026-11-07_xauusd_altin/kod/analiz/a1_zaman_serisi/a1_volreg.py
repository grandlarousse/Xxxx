#!/usr/bin/env python3
"""a1_zaman_serisi — VOLREG (oynaklık rejimine koşullu 5 günlük momentum/dönüş) için komşuluk duyarlılığı ve erken dönem ayrıştırması.
Kural (IS'te seçilen): x = log(spot15_t / spot15_{t-5}); q = rv20 (spot 15:00 günlük log getiri std, 20 gün)'nin 2010'dan beri genişleyen yüzdeliği.
  q < 1/3  → pozisyon = sign(x)   (sakin piyasada momentum)
  q > 2/3  → pozisyon = -sign(x)  (çalkantılı piyasada dönüş)
  aksi     → 0
Bilgi zamanı: gün t 15:00 UTC (spot). Giriş: gün t VİOP uzlaşması (~15:10 UTC). Tutuş h=1/3/5, kademeli.
Önce a1_main.py ve a1_deep.py çalışmış olmalı (kayda ekler). Çalıştır: python3 -W ignore a1_volreg.py
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code"); sys.path.insert(0, f"{S}/out/a1_zaman_serisi")
from lib_altin import *
from a1_feats import *

AG = "a1_zaman_serisi"; OUT = f"{S}/out/{AG}"
H = [1, 3, 5]
d = load_viop(); s = load_spot(); r_v = d.v_ret
lp = np.log(s.s_p15); r_s = lp.diff()


def rolling_pct(x, win):
    return x.rolling(win, min_periods=int(win * 0.8)).rank(pct=True)


def make_pos(k=5, rvwin=20, lo=1 / 3, hi=2 / 3, qmode="exp", side="both"):
    rv = r_s.rolling(rvwin).std()
    q = expanding_pct(rv) if qmode == "exp" else rolling_pct(rv, int(qmode))
    sg = np.sign(lp - lp.shift(k))
    p = pd.Series(np.where(q < lo, sg, np.where(q > hi, -sg, 0.0)), index=s.index).where(q.notna() & sg.notna())
    if side == "lo": p = p.where(q < lo, 0.0)
    if side == "hi": p = p.where(q > hi, 0.0)
    return p


def stats(pos_cal, h):
    pv = to_viop(pd.DataFrame({"p": pos_cal}), d.index).p
    ism = r_v.index <= IS_END
    f = backtest(pv, r_v, h, 5, demean=True); a = backtest(pv[ism], r_v[ism], h, 5, demean=True); b = backtest(pv[~ism], r_v[~ism], h, 5, demean=True)
    bn = backtest(pv[~ism], r_v[~ism], h, 5)
    m = (s.index >= "2010-01-01") & (s.index <= "2016-12-31")
    e = backtest(pos_cal[m], r_s[m], h, 5, demean=True)
    g = f["pnl"].groupby(f["pnl"].index.year).mean()
    return dict(shdm_full=round(f["sharpe"], 2), t_full=round(f["t_daily"], 2), shdm_is=round(a["sharpe"], 2), shdm_oos=round(b["sharpe"], 2), sh_oos=round(bn["sharpe"], 2),
                t_oos=round(b["t_daily"], 2), yrs_pos=f"{int((g > 0).sum())}/{len(g)}", e_shdm=round(e["sharpe"], 2), e_t=round(e["t_daily"], 2), expo=round(f["exposure"], 2),
                _f=f, _e=e)


ROWS = []
grid = []
for k in [3, 5, 10]: grid.append(dict(k=k))
for rvwin in [10, 60]: grid.append(dict(rvwin=rvwin))
for lo, hi in [(0.25, 0.75), (0.5, 0.5), (0.2, 0.8)]: grid.append(dict(lo=lo, hi=hi))
for qm in ["500", "750", "1250"]: grid.append(dict(qmode=qm))
grid += [dict(side="lo"), dict(side="hi")]
for g in grid:
    for h in H:
        st = stats(make_pos(**g), h)
        nm = "VOLREG_5" + "".join(f"|{a}={b}" for a, b in g.items())
        ROWS.append(dict(variant=nm, h=h, **{a: b for a, b in st.items() if not a.startswith("_")}))
        if g != dict(k=5):
            register(AG, "robust_volreg", f"{nm}|h{h}", nm, h, dict(ic=st["shdm_full"], t=st["t_full"], n=st["_f"]["n_days"], t_oos=st["t_oos"], ic_oos=st["shdm_oos"]),
                     "VOLREG komşuluk duyarlılığı (sağlamlık); ic=demeaned Sharpe")
V = pd.DataFrame(ROWS); V.to_csv(f"{OUT}/volreg_sensitivity.csv", index=False)

# erken dönem yıllık ve bacak ayrıştırması; tam spot örneklem (2010-2026, spot hedef)
E = []
for side in ["both", "lo", "hi"]:
    p = make_pos(side=side)
    for h in H:
        for a, b in [("2010-01-01", "2016-12-31"), ("2017-03-01", "2021-12-31"), ("2022-01-01", "2026-12-31"), ("2010-01-01", "2026-12-31")]:
            m = (s.index >= a) & (s.index <= b)
            bt = backtest(p[m], r_s[m], h, 5, demean=True)
            g = bt["pnl"].groupby(bt["pnl"].index.year)
            E.append(dict(side=side, h=h, donem=f"{a[:4]}-{b[:4]}", hedef="spot 15->15", shdm=round(bt["sharpe"], 2), t=round(bt["t_daily"], 2), expo=round(bt["exposure"], 2),
                          yr=json.dumps({int(y): round(v, 2) for y, v in (g.mean() / g.std() * np.sqrt(252)).items()}) if a == "2010-01-01" and b.startswith("2016") else ""))
pd.DataFrame(E).to_csv(f"{OUT}/volreg_spot_periods.csv", index=False)
# rejim payları
q = expanding_pct(r_s.rolling(20).std())
share = pd.DataFrame({"lo": (q < 1 / 3), "hi": (q > 2 / 3)}).groupby(s.index.year).mean().round(2)
share.to_csv(f"{OUT}/volreg_regime_share.csv")
print(V.to_string()); print(pd.DataFrame(E).drop(columns="yr").to_string()); print(share.T.to_string())
print([e["yr"] for e in E if e["yr"]])
