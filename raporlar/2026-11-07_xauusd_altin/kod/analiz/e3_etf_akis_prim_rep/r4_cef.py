"""E3-3 / E3-4: PHYS/GLD, PSLV/SLV ve CEF artık sapması (bağımsız)."""
from rc import *
import warnings; warnings.filterwarnings("ignore")
pd.set_option("display.width", 250)
days = nyse_days("2008-01-01")
C = {t: yh(t).reindex(days) for t in ["PHYS", "GLD", "PSLV", "SLV", "CEF"]}
r = {t: np.log(C[t]).diff() for t in C}
# veri kalitesi: hacim sıfır / aynı kapanış tekrar
for t in ["PHYS", "PSLV", "CEF"]:
    v = yh(t, "volume").reindex(days); c = yh(t, "close").reindex(days)
    print(t, "ilk", C[t].first_valid_index().date(), "| hacim 0 gün:", int((v == 0).sum()), "| kapanış değişmeyen gün:", int((c.diff() == 0).sum()), "| NaN:", int(C[t][C[t].first_valid_index():].isna().sum()))
def roll_resid(y, X, win=250):
    dd = pd.concat([y.rename("y")] + [x.rename(f"x{i}") for i, x in enumerate(X)], axis=1).dropna()
    Y = dd.y.values; XX = np.column_stack([np.ones(len(dd))] + [dd[f"x{i}"].values for i in range(len(X))])
    e = np.full(len(dd), np.nan); B = np.full((len(dd), XX.shape[1]), np.nan)
    for i in range(win, len(dd)):
        b, *_ = np.linalg.lstsq(XX[i - win:i], Y[i - win:i], rcond=None)
        e[i] = Y[i] - XX[i, 1:] @ b[1:]; B[i] = b
    return pd.Series(e, index=dd.index).reindex(days), pd.DataFrame(B, index=dd.index).reindex(days)
eC, BC = roll_resid(r["CEF"], [r["GLD"], r["SLV"]])
print("CEF beta ortalamaları (g, s):", BC.iloc[:, 1:].mean().round(3).tolist(), "| 2018 öncesi/sonrası:", BC[:"2017"].iloc[:, 1:].mean().round(2).tolist(), BC["2018":].iloc[:, 1:].mean().round(2).tolist())
pairs = {"PHYS-GLD": (np.log(C["PHYS"] / C["GLD"]), r["PHYS"] - r["GLD"]),
         "PSLV-SLV": (np.log(C["PSLV"] / C["SLV"]), r["PSLV"] - r["SLV"]),
         "CEF-mix": (eC.cumsum().where(eC.notna()), eC)}
# not: eC.cumsum() NaN'ları atlar (pandas skipna) -> fillna(0).cumsum ile eşdeğer
rows, Z = [], {}
for nm, (lvl, sp) in pairs.items():
    print(nm, "spread günlük std bps", round(sp.std() * 1e4, 1), "AC1", round(sp.autocorr(1), 3))
    for k in (20, 60):
        dev = lvl - lvl.rolling(k, min_periods=k // 2).median()
        z = (dev / dev.rolling(250, min_periods=120).std()).shift(1)
        Z[(nm, k)] = z
        for h in (1, 3, 5):
            st = stats(z, fwd(sp, h), h); st.update(pair=nm, k=k, h=h, tgt="spread"); rows.append(st)
        a = nm.split("-")[0]
        st = stats(z, fwd(r[a], 5), 5); st.update(pair=nm, k=k, h=5, tgt=f"{a} kendi"); rows.append(st)
res = pd.DataFrame(rows)[["pair", "k", "h", "tgt", "n", "ic", "t", "ic_is", "t_is", "ic_oos", "t_oos", "t_22", "yrs"]]
res.to_csv(f"{OUT}/r4_cef_tests.csv", index=False); print(res.to_string())
# placebo (daha eski sinyal)
for nm in pairs:
    z = Z[(nm, 60)]
    print(nm, "z60 h5 placebo shift 0/1/2/5:", [round(ic(z.shift(s), fwd(pairs[nm][1], 5), 5)["ic"], 3) for s in (0, 1, 2, 5)])
# büyüklük: z dilimleri, 5 günlük spread bps (IS/OOS)
mag = []
for nm in pairs:
    for k in (60, 20):
        y = fwd(pairs[nm][1], 5); dd = pd.concat([Z[(nm, k)].rename("z"), y.rename("y")], axis=1).dropna()
        for seg, msk in [("IS", dd.index <= IS_END), ("OOS", dd.index > IS_END)]:
            g = dd[msk]; b = pd.cut(g.z, [-np.inf, -2, -1, 1, 2, np.inf])
            mm = g.groupby(b).y.agg(["mean", "count"])
            mag.append(dict(pair=nm, k=k, seg=seg, **{str(i): f"{v*1e4:+.1f} ({int(n)})" for (i, v), n in zip(mm["mean"].items(), mm["count"])}))
mag = pd.DataFrame(mag); mag.to_csv(f"{OUT}/r4_cef_magnitude.csv", index=False); print(mag.to_string())
# z<-1.5 PHYS seçimi (maliyetsiz araç seçimi) — 5 gün
for nm in ["PHYS-GLD", "CEF-mix", "PSLV-SLV"]:
    for thr in (1.0, 1.5):
        y = fwd(pairs[nm][1], 5); z = Z[(nm, 60)]
        for seg, msk in [("IS", y.index <= IS_END), ("OOS", y.index > IS_END)]:
            sel = (z < -thr) & msk & y.notna()
            print(f"{nm} z60<-{thr} {seg}: 5g ort spread {y[sel].mean()*1e4:+.1f} bps (n={sel.sum()}), koşulsuz {y[msk].mean()*1e4:+.1f}")
# ---------------- geçiş stratejisi: varsayılan referans; z<-thr iken fona geç; maliyet her geçişte 2 bacak (10+10 bps), stres 20+20
def stag(w, h):
    w = w.fillna(0); return sum(w.shift(k).fillna(0) for k in range(h)) / h
EXR = {"PHYS-GLD": np.expm1(r["PHYS"]) - np.expm1(r["GLD"]), "PSLV-SLV": np.expm1(r["PSLV"]) - np.expm1(r["SLV"]), "CEF-mix": eC}
EXT = {"2008": ("2008-01-01", "2008-12-31"), "2013-04": ("2013-04-01", "2013-04-30"), "2020-03": ("2020-03-01", "2020-03-31"), "2026-01/02": ("2026-01-01", "2026-02-28")}
allc = []
for nm in pairs:
    exr = EXR[nm].dropna()
    for k in (20, 60):
        for thr in (1.0, 1.5, 2.0):
            for h in (1, 3, 5):
                w = (Z[(nm, k)] < -thr).astype(float).reindex(exr.index)
                eff = stag(w, h)
                res_ = {}
                for c in (0, 20, 40):
                    ex = eff.shift(1) * exr - eff.diff().abs().shift(1).fillna(0) * c / 2e4
                    ex = ex.iloc[1:]
                    res_[c] = ex
                ex = res_[20]
                msk = pd.Series(True, index=ex.index)
                for a, b in EXT.values(): msk[a:b] = False
                row = dict(pair=nm, k=k, thr=thr, h=h, frac=round(eff.mean(), 3), entries_yr=round(((eff > 0) & (eff.shift(1) == 0)).sum() / len(eff) * 252, 1),
                           IRg_IS=seg_sh(res_[0])["IS"], IRg_OOS=seg_sh(res_[0])["OOS"], IR_IS=seg_sh(ex)["IS"], IR_OOS=seg_sh(ex)["OOS"], IR_22=seg_sh(ex)["s22"],
                           IRs_OOS=seg_sh(res_[40])["OOS"], IR_OOS_exext=sharpe(ex[msk & (ex.index > IS_END)]), IR_full_exext=sharpe(ex[msk]),
                           ann_OOS_bps=round(ex[ex.index > IS_END].mean() * 252 * 1e4, 1),
                           **{f"x_{kk}": round(ex[a:b].sum() * 100, 2) for kk, (a, b) in EXT.items()})
                allc.append(row)
sw = pd.DataFrame(allc); sw.to_csv(f"{OUT}/r4_switch.csv", index=False)
for nm in pairs:
    g = sw[sw.pair == nm]; pk = g.sort_values("IR_IS", ascending=False).iloc[0]
    print(f"{nm} IS seçimi:", pk.to_dict())
print(sw.to_string())
