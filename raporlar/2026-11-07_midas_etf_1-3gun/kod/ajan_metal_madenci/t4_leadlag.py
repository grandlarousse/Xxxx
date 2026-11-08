"""Görev 4: lead-lag (aile). leadlag_sweep.csv özeti + ek testler.
(1) Her aile ETF'i için: eşzamanlı sürücüler (corr_1y, beta_1y; öncü DEĞİL), gecikmeli aday öncüler
    (lag/catch t, FDR bayrağı, IS/OOS işareti, ekonomik büyüklük vs maliyet).
(2) Ek regresyonlar (Newey-West): r_T(t+1..t+h) = a + b*r_T(t) + c*r_L(t)  ve  = a + b*r_T(t) + k*gap_t
    (gap_t = beta60*r_L(t) - r_T(t)). Yetişme etkisinin kendi gecikmesinden ayrılması.
(3) Bir işlem kuralı: GDX'in GLD'ye göre artığı >= +1.5 sd -> GLD long (GLD<-GDX gecikme bulgusu; MM02'nin aynası).
Çalıştır: python3 -I kod/ajan_metal_madenci/t4_leadlag.py
Çıktı: sonuclar/aile_metal_madenci/leadlag_aile.csv, leadlag_ek_regresyon.csv, testler_t4.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import mm, lib

KOD_MAP = {"VIX_dlog": "CBOE:VIX", "VIXTS_d": "CBOE:VIX/CBOE:VIX3M", "OVX_dlog": "CBOE:OVX", "GVZ_dlog": "CBOE:GVZ",
           "VVIX_dlog": "CBOE:VVIX", "BTC_16ET": "COINBASE:BTCUSD", "ETH_16ET": "COINBASE:ETHUSD", "DGS10_d": "TVC:US10Y",
           "DGS2_d": "TVC:US02Y", "DGS30_d": "TVC:US30Y", "DFII10_d": "FRED:DFII10", "T10YIE_d": "FRED:T10YIE"}

def nw(y, X, lags):
    from leadlag_sweep import nw_t  # aynı NW uygulaması
    return nw_t(y, X, lags)

def fwd(r, h):
    return r[::-1].rolling(h).sum()[::-1].shift(-1)

def main():
    sys.path.insert(0, mm.KOD)
    tvm = mm.tv_map()
    L = pd.read_csv(os.path.join(mm.ROOT, "sonuclar", "leadlag_sweep.csv"))
    L = L[L.target.isin(mm.FAM)].copy()
    L["leader_tv"] = L.leader.map(lambda x: KOD_MAP.get(x, tvm.get(x, "")))
    scr = pd.read_csv(os.path.join(mm.ROOT, "sonuclar", "tarama.csv")).set_index("sym")
    L["cost_rt_bp"] = L.target.map(scr["cost_rt_bp"])
    # gecikmeli öncü ölçütü: FDR (lag ya da catch, h1 ya da h3) + IS/OOS aynı işaret + |etki/sd| > maliyet
    def ok(r, kind, h):
        t = r[f"{kind}_t_h{h}"]; ti = r.get(f"{kind}_t_h{h}_is"); to = r.get(f"{kind}_t_h{h}_oos")
        same = np.sign(ti) == np.sign(to) == np.sign(t)
        big = abs(r[f"{kind}_bp_per_sd_h{h}"]) * 2 > r["cost_rt_bp"]   # 2 sd'lik hareketin etkisi maliyetin üstünde mi
        return bool(r[f"fdr10_{kind}_t_h{h}"]) and bool(same), bool(big)
    rows = []
    for _, r in L.iterrows():
        rec = {"target": r.target, "leader": r.leader, "leader_tv": r.leader_tv, "corr_1y": r.corr_1y, "beta_1y": r.beta_1y,
               "cost_rt_bp": r.cost_rt_bp}
        best = None
        for kind in ("lag", "catch"):
            for h in (1, 3):
                f, big = ok(r, kind, h)
                rec[f"{kind}_h{h}_t"] = r[f"{kind}_t_h{h}"]; rec[f"{kind}_h{h}_bp_sd"] = r[f"{kind}_bp_per_sd_h{h}"]
                rec[f"{kind}_h{h}_fdr_isoos"] = f; rec[f"{kind}_h{h}_buyuk"] = big
                if f and (best is None): best = f"{kind}_h{h}" + ("" if big else "(ekonomik olarak küçük)")
        rec["dogrulanmis"] = best
        rows.append(rec)
    A = pd.DataFrame(rows)
    A.to_csv(os.path.join(mm.OUTD, "leadlag_aile.csv"), index=False)
    print("FDR + IS/OOS aynı işaret geçen çiftler:")
    print(A[A.dogrulanmis.notna()][["target", "leader", "leader_tv", "corr_1y", "lag_h1_t", "lag_h1_bp_sd", "lag_h3_t", "lag_h3_bp_sd",
                                     "catch_h1_t", "catch_h3_t", "cost_rt_bp", "dogrulanmis"]].round(2).to_string(index=False))
    # en güçlü 3 eşzamanlı sürücü (|corr_1y|)
    drv = (A.assign(ac=A.corr_1y.abs()).sort_values("ac", ascending=False).groupby("target").head(4)
           [["target", "leader", "leader_tv", "corr_1y", "beta_1y"]])
    drv.to_csv(os.path.join(mm.OUTD, "leadlag_suruculer.csv"), index=False)
    # ---------------- (2) ek regresyonlar
    reg = mm.Registry("t4")
    R = {s: np.log(mm.load(s)["c"]).diff() for s in set(mm.FAM) | {"KWEB", "FXI", "SPY", "UUP"}}
    idx = mm.load("SPY").index
    R = pd.DataFrame(R).reindex(idx)
    pairs = [("GDX", "GLD"), ("GDXJ", "GLD"), ("RING", "GLD"), ("NUGT", "GLD"), ("SIL", "SLV"), ("SILJ", "SLV"), ("COPX", "CPER"),
             ("GLD", "GDX"), ("SLV", "GDX"), ("GLD", "SLV"), ("SLV", "GLD"), ("DBB", "KWEB"), ("CPER", "FXI"), ("CPER", "KWEB"),
             ("URA", "SPY"), ("URNM", "SPY"), ("XME", "CPER"), ("GLD", "UUP")]
    out = []
    for T, Ld in pairs:
        y0 = R[T]; x = R[Ld]
        b60 = y0.rolling(60).cov(x) / x.rolling(60).var()
        gap = b60 * x - y0
        for h in (1, 3):
            d = pd.DataFrame({"fy": fwd(y0, h), "own": y0, "x": x, "gap": gap}).dropna()
            for per, m in (("tum", np.ones(len(d), bool)), ("is", d.index <= lib.IS_END), ("oos", d.index > lib.IS_END)):
                dd = d[m]
                Xl = np.column_stack([np.ones(len(dd)), dd.own, dd.x]); b, t = nw(dd.fy.values, Xl, h)
                Xc = np.column_stack([np.ones(len(dd)), dd.own, dd.gap]); bc, tc = nw(dd.fy.values, Xc, h)
                Xo = np.column_stack([np.ones(len(dd)), dd.gap]); bo, to = nw(dd.fy.values, Xo, h)
                out.append({"target": T, "leader": Ld, "h": h, "donem": per, "n": len(dd),
                            "lag_b": b[2], "lag_t": t[2], "lag_bp_per_sd": b[2] * dd.x.std() * 1e4,
                            "catch_kendi_kontrollu_k": bc[2], "catch_kendi_kontrollu_t": tc[2], "kendi_t(catch_reg)": tc[1],
                            "catch_kontrolsuz_t": to[1], "catch_kendi_kontrollu_bp_per_sd": bc[2] * dd.gap.std() * 1e4})
                if per == "tum":
                    reg.add(f"LL_lag_{T}<-{Ld}", T, "reg", h, len(dd), t[2])
                    reg.add(f"LL_catch_kontrollu_{T}<-{Ld}", T, "reg", h, len(dd), tc[2])
    O = pd.DataFrame(out); O.to_csv(os.path.join(mm.OUTD, "leadlag_ek_regresyon.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30); pd.set_option("display.max_rows", 300)
    print(O.round(2).to_string(index=False))
    # ---------------- (3) işlem kuralı: GDX artığı >= +1.5 sd -> GLD long
    gld = mm.load("GLD"); gdx = mm.load("GDX")["c"].reindex(gld.index)
    rt = np.log(gdx).diff(); rl = np.log(gld["c"]).diff()
    b = rt.rolling(60).cov(rl) / rl.rolling(60).var(); res = rt - b * rl
    sig = res >= 1.5 * res.rolling(60).std().shift(1)
    for m in ("C0", "O1", "C1"):
        for h in (1, 2, 3):
            s, _ = mm.full("GLD", sig, h, m, df=gld)
            reg.add("LL_kural_GDXartik_pos_GLDal", "GLD", m, h, s["n"], s["t"], s["mean_net_bp"])
            print("GLD<-GDX artık kuralı", m, h, mm.fmt(s))
    reg.save()

if __name__ == "__main__":
    main()


def ek_breakeven():
    """Sweep'te IS ve OOS'ta aynı işaretli (FDR'siz) çıkan T10YIE_d -> metal(t+1) bulgusunu işlem kuralına çevirme.
    T10YIE = DGS10 - DFII10 (Hazine, ~15:30 ET kotasyonları, kapanıştan SONRA yayımlanır) -> gerçekçi modlar O1/C1;
    C0 yalnız bilgi amaçlı (gerçek zamanlı bilinmez). Eşik: günlük değişim >= +5 bp (~1.6 sd). Tutuş h=1..3."""
    reg = mm.Registry("t4b")
    be = lib.fred("T10YIE")
    for s in ("SLV", "GLD", "GDX", "SIL"):
        df = mm.load(s)
        b = be.reindex(df.index).ffill(); sig = (b - b.shift(1)) >= 0.05
        for m in ("C0", "O1", "C1"):
            for h in (1, 2, 3):
                st, _ = mm.full(s, sig, h, m, df=df)
                reg.add("LL_kural_T10YIE_d_ge5bp", s, m, h, st["n"], st["t"], st["mean_net_bp"])
                print("T10YIE>=+5bp ->", s, m, h, mm.fmt(st, ("n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "is_t", "oos_net_bp", "oos_t", "years_pos_frac")))
    reg.save()

if __name__ == "__main__" and "--breakeven" in sys.argv:
    ek_breakeven()


def ek_gdx_oncu():
    """Sweep'teki FDR'siz ama IS/OOS aynı işaretli GDX-öncülüğü bulgularını kurala çevirme:
    GDX 1g z (60g) >= +1.5 -> PPLT (h1 bulgusu) ve COPX (h3 bulgusu) long; ayrıca <= -1.5 -> long (simetri kontrolü, beklenti negatif)."""
    reg = mm.Registry("t4c")
    z = lib.zret(mm.load("GDX")["c"], 1)
    for tgt in ("PPLT", "COPX"):
        df = mm.load(tgt)
        for nm, sig in (("GDX_z1_ge1.5", (z >= 1.5).reindex(df.index)), ("GDX_z1_le-1.5", (z <= -1.5).reindex(df.index))):
            for m in ("C0", "O1", "C1"):
                for h in (1, 3):
                    st, _ = mm.full(tgt, sig, h, m, df=df)
                    reg.add(f"LL_kural_{nm}", tgt, m, h, st["n"], st["t"], st["mean_net_bp"])
                    print(nm, "->", tgt, m, h, mm.fmt(st, ("n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac")))
    reg.save()

if __name__ == "__main__" and "--gdxoncu" in sys.argv:
    ek_gdx_oncu()
