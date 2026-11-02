"""Rejim/yıl kırılımları: BT2 gap fade (E0, E2) 2026 aylık + Eyl-Eki 2026 fon krizi; BT5 kapanış müzayedesi dönüşü yıllara göre ve vade sonu hariç.
Çıktı: res/a8_regime.csv"""
import numpy as np, pandas as pd, c_common as c
ll = c.ll; TG = c.VIOP
H = {s: c.h1_panel(s) for s in TG}; days = H["AKBNK"].index
TP = {}
for s in TG:
    raw = ll.raw(ll.T(s), "h1"); raw = raw[~raw.index.duplicated(keep="last")]
    fb = raw[(raw.index.hour == 6) & (raw.index.minute == 30)].copy(); fb.index = pd.DatetimeIndex(fb.index.tz_convert(None).normalize())
    TP[s] = ((fb["h"] + fb["l"] + fb["c"]) / 3).reindex(days)
df = lambda f: pd.DataFrame({s: f(s) for s in TG})
ok = df(lambda s: H[s]["intra"].notna())
g = df(lambda s: H[s]["gap"]).where(ok)
pos = -np.sign(g).where(g.abs() > 0.01, 0.0).fillna(0)
rows = []
for en, Y in [("E0", df(lambda s: H[s]["intra"])), ("E2", df(lambda s: np.log(H[s]["C"] / TP[s])).where(ok))]:
    pp = (pos * Y).where(pos != 0).mean(axis=1)
    for lab, m in [("2024", pp.index.year == 2024), ("2025", pp.index.year == 2025), ("2026-01..08", (pp.index >= "2026-01-01") & (pp.index < "2026-09-01")), ("2026-09..10 fon krizi", pp.index >= "2026-09-01"), ("2025-03 (Imamoglu)", (pp.index >= "2025-03-01") & (pp.index < "2025-04-01"))]:
        x = pp[m].dropna(); rows.append(dict(bt=f"BT2_{en}_|gap|>1%", sub=lab, n_days=len(x), mean_bps=1e4 * x.mean(), t=ll.nw_t(x.reset_index(drop=True))[1] if len(x) > 30 else np.nan))
CA = df(lambda s: H[s]["ca"]); n730 = df(lambda s: (H[s]["gap"] + H[s]["r1"]).shift(-1))
cal = ll.bist_cal(); s_ = pd.Series(cal, index=cal); eom = pd.DatetimeIndex(s_.groupby([cal.year, cal.month]).max().values)
for thr in [0.0025, 0.005]:
    p5 = -np.sign(CA).where(CA.abs() > thr, 0.0).fillna(0)
    pp = (p5 * n730).where(p5 != 0).mean(axis=1)
    for lab, m in [("2024", pp.index.year == 2024), ("2025", pp.index.year == 2025), ("2026", pp.index.year == 2026), ("vade sonu hariç", ~pp.index.isin(eom)), ("yalnız vade sonu", pp.index.isin(eom))]:
        x = pp[m].dropna(); rows.append(dict(bt=f"BT5_|CA|>{thr*1e4:.0f}bps_->07:30", sub=lab, n_days=len(x), mean_bps=1e4 * x.mean(), t=ll.nw_t(x.reset_index(drop=True))[1] if len(x) > 30 else np.nan))
    # likit vs illikit
    LQ = pd.read_csv(c.RES + "/a0_liq.csv").set_index("stock")
    for grp, mem in [("likit23", [s for s in TG if LQ.loc[s, "liq_rank"] <= 23]), ("illikit24", [s for s in TG if LQ.loc[s, "liq_rank"] > 23])]:
        x = (p5[mem] * n730[mem]).where(p5[mem] != 0).mean(axis=1).dropna()
        rows.append(dict(bt=f"BT5_|CA|>{thr*1e4:.0f}bps_->07:30", sub=grp, n_days=len(x), mean_bps=1e4 * x.mean(), t=ll.nw_t(x.reset_index(drop=True))[1]))
R = pd.DataFrame(rows); R.to_csv(c.RES + "/a8_regime.csv", index=False); print(R.round(2).to_string())
