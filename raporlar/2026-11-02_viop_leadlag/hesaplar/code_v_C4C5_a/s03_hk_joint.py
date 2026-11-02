"""Adim 3: (a) ortak regresyonlar ve kontroller.
 1) TRALT oc_t ~ P0630_t + OVL_t (ayni orneklem 2024-09+): on-bilinen kisim vs ortusen kisim.
 2) Kontroller: TRALT gap_t (acilista bilinir), TRALT cc_{t-1}, XU100 cc_{t-1}, XU100 gap_t.
 3) Altin vadelisi: GC=F gece getirisi (BIST kapanisi 15:00 UTC t' -> 06:00/07:00 UTC t) on-acilis sinyali; HK P0630 bunun otesinde bilgi tasiyor mu?
 4) Yillara gore (CLOSE, OPEN) ve maliyet duyarliligi (8/10/15 bps)."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a")
import vlib as V, numpy as np, pandas as pd
from s02_hk_timing import signals, C, TR, XU
pd.set_option("display.width", 250)

def gc_overnight():
    h = V.rawd("GC=F", "h1").copy(); h["end"] = h.index + pd.Timedelta(hours=1)
    s = h["c"]; s.index = h["end"]  # bar bitis zamani -> fiyat
    s = s[~s.index.duplicated(keep="last")].sort_index()
    def at(day, hh):  # o ana kadar bitmis son bar
        return None
    out = {}
    idx = s.index
    for t_prev, t in zip(C[:-1], C[1:]):
        if t < pd.Timestamp("2024-06-11"): continue
        a = pd.Timestamp(t_prev).tz_localize("UTC") + pd.Timedelta(hours=15)
        for lab, hh in [("GC0600", 6), ("GC0700", 7), ("GC0810", 8)]:
            b = pd.Timestamp(t).tz_localize("UTC") + pd.Timedelta(hours=hh, minutes=10 if hh == 8 else 0)
            ia = idx.searchsorted(a, side="right") - 1; ib = idx.searchsorted(b, side="right") - 1
            if ia < 0 or ib < 0 or (a - idx[ia]) > pd.Timedelta(hours=3) or (b - idx[ib]) > pd.Timedelta(hours=3): continue
            out.setdefault(lab, {})[t] = np.log(s.iloc[ib] / s.iloc[ia])
        # gun-ici altin (BIST seansi ile eszamanli): 07:00 -> 15:00 UTC t
        a2 = pd.Timestamp(t).tz_localize("UTC") + pd.Timedelta(hours=7); b2 = pd.Timestamp(t).tz_localize("UTC") + pd.Timedelta(hours=15)
        ia = idx.searchsorted(a2, side="right") - 1; ib = idx.searchsorted(b2, side="right") - 1
        if ia >= 0 and ib >= 0 and (a2 - idx[ia]) <= pd.Timedelta(hours=2) and (b2 - idx[ib]) <= pd.Timedelta(hours=2):
            out.setdefault("GC_intra", {})[t] = np.log(s.iloc[ib] / s.iloc[ia])
    return pd.DataFrame(out)

def show(lab, y, X, lags=5):
    p, t, n = V.nw(y, X, lags)
    if p is None: print(lab, "n<30"); return
    print(f"{lab:60s} n={n:4d} " + " ".join(f"{k}={p[k]:+.3f}(t={t[k]:+.2f})" for k in X.columns))

if __name__ == "__main__":
    G = gc_overnight()
    S = signals("1787.HK"); S2 = signals("2899.HK"); S3 = signals("600547.SS")
    y = TR["intra"]
    D = pd.concat([y.rename("y"), S.add_prefix("hk_"), S2[["P0630", "CLOSE"]].add_prefix("zj_"), S3[["CLOSE", "P0630"]].add_prefix("sd_"), G,
                   TR["gap"].rename("own_gap"), TR["cc"].shift(1).rename("own_cc1"), XU["cc"].shift(1).rename("xu_cc1"), XU["gap"].rename("xu_gap"), XU["intra"].rename("xu_oc")], axis=1)
    D = D[D.index >= "2024-09-01"]
    print("Korelasyonlar (2024-09+):")
    print(D[["y", "hk_CLOSE", "hk_P0630", "hk_OVL", "hk_OPEN", "GC0600", "GC0700", "GC0810", "GC_intra", "own_gap", "xu_oc"]].corr().round(3).to_string())
    z = lambda c: (D[c] - D[c].mean()) / D[c].std()
    print("\nStandartlastirilmis NW regresyonlar, hedef TRALT oc_t:")
    show("1) hk_P0630 + hk_OVL", z("y"), pd.DataFrame({"P0630": z("hk_P0630"), "OVL": z("hk_OVL")}))
    show("2) hk_P0630 + kontroller(own_gap, own_cc1, xu_cc1, xu_gap)", z("y"), pd.DataFrame({"P0630": z("hk_P0630"), "own_gap": z("own_gap"), "own_cc1": z("own_cc1"), "xu_cc1": z("xu_cc1"), "xu_gap": z("xu_gap")}))
    show("3) GC0600 (gece altin, 15:00 t' -> 06:00 t)", z("y"), pd.DataFrame({"GC0600": z("GC0600")}))
    show("4) GC0600 + hk_P0630", z("y"), pd.DataFrame({"GC0600": z("GC0600"), "P0630": z("hk_P0630")}))
    show("5) GC0700 + hk_P0630 + own_gap", z("y"), pd.DataFrame({"GC0700": z("GC0700"), "P0630": z("hk_P0630"), "own_gap": z("own_gap")}))
    show("6) GC_intra (eszamanli 07-15 UTC) + hk_OVL", z("y"), pd.DataFrame({"GC_intra": z("GC_intra"), "OVL": z("hk_OVL")}))
    show("7) hk_CLOSE + GC_intra", z("y"), pd.DataFrame({"CLOSE": z("hk_CLOSE"), "GC_intra": z("GC_intra")}))
    show("8) hk_OVL ~ GC 07:00->08:10 eszamanli (OVL ne?)", z("hk_OVL"), pd.DataFrame({"GC0810_minus_0700": (D["GC0810"] - D["GC0700"] - (D["GC0810"] - D["GC0700"]).mean()) / (D["GC0810"] - D["GC0700"]).std()}))
    # GC0600 sinyalinin backtesti (TV: COMEX:GC1!)
    for sc in ["GC0600", "GC0700"]:
        for cost in [8, 10, 15]:
            r, _ = V.bt(D[sc], D["y"], cost); print(f"BT {sc} -> TRALT oc cost={cost}: n={r['ALL'].get('n')} net={r['ALL'].get('mean_bps', np.nan):+.1f} bps sh={r['ALL'].get('sharpe', np.nan):+.2f} t={r['ALL'].get('t', np.nan):+.2f} yil={r['yr']}")
    for sc in ["hk_P0630", "hk_CLOSE", "zj_P0630"]:
        for cost in [8, 10, 15]:
            r, _ = V.bt(D[sc], D["y"], cost); print(f"BT {sc} -> TRALT oc cost={cost}: n={r['ALL'].get('n')} net={r['ALL'].get('mean_bps', np.nan):+.1f} bps sh={r['ALL'].get('sharpe', np.nan):+.2f} t={r['ALL'].get('t', np.nan):+.2f} yil={r['yr']}")
    # tum donem yillara gore: CLOSE (orijinal) vs OPEN (on-bilinen) vs CLOSE_{t-1}
    print("\nTum donem 1787.HK -> TRALT oc, yillara gore korelasyon / net10 bps:")
    F = pd.concat([TR["intra"].rename("y"), S["CLOSE"], S["OPEN"], S["CLOSE"].shift(1).rename("CLOSE_l1")], axis=1)
    F = F[F.index >= "2018-10-01"]
    rows = []
    for yr, g in F.groupby(F.index.year):
        rr = {"yil": yr, "n": int(g.dropna(subset=["y", "CLOSE"]).shape[0])}
        for c in ["CLOSE", "OPEN", "CLOSE_l1"]:
            gg = g[["y", c]].dropna(); rr["r_" + c] = gg.y.corr(gg[c])
            r, _ = V.bt(gg[c], gg.y, 10); rr["net_" + c] = r["ALL"].get("mean_bps")
        rows.append(rr)
    print(pd.DataFrame(rows).round(3).to_string())
    for cost in [0, 8, 10, 15]:
        r, _ = V.bt(F["CLOSE"], F["y"], cost); print(f"CLOSE(orijinal) cost={cost}: ALL {r['ALL'].get('mean_bps'):+.1f} IS {r['IS'].get('mean_bps'):+.1f} (sh {r['IS'].get('sharpe'):+.2f}) OOS {r['OOS'].get('mean_bps'):+.1f} (sh {r['OOS'].get('sharpe'):+.2f})")
