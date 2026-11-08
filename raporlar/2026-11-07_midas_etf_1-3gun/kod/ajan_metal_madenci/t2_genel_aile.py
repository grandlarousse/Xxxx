"""Görev 2: genel kütüphanenin (31 sinyal x mod x h [+erken çıkış]) aile içinde tutarlılığı.
(a) genel_tum.csv satırlarından ETF başına sayım (REP17: kaldıraçsız, kopyasız 17 ETF)
(b) Aile havuzu testi: 12 küme temsilcisi (REP12) üzerinde aynı sinyal günündeki işlemler ortalanır -> olay serisi,
    Newey-West t (lag=h). 297 kombinasyonun tamamı test edilir, BH-FDR q=0.10 (seçim yanlılığı yok).
Çalıştır: python3 -I kod/ajan_metal_madenci/t2_genel_aile.py
Çıktı: sonuclar/aile_metal_madenci/genel_aile_havuz.csv, testler_t2.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import mm, lib, strategies as S

def main():
    ctx = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}
    dfs = {s: mm.load(s) for s in mm.REP12 + ["SPY"]}
    g = pd.read_csv(os.path.join(mm.ROOT, "sonuclar", "genel_tum.csv"))
    g = g[g.sym.isin(mm.REP17)]
    reg = mm.Registry("t2")
    rows = []
    for name, fn in S.LIB.items():
        sigs = {s: fn(dfs[s], ctx).reindex(dfs[s].index).fillna(False).astype(bool) for s in mm.REP12}
        for mode in ("C0", "O1", "C1"):
            combos = [(h, None, "sabit") for h in (1, 2, 3)]
            if name in S.EXITS: combos.append((3, "kural", "kural_max3"))
            for h, ex, exname in combos:
                T = []
                for s in mm.REP12:
                    df = dfs[s]; sig = sigs[s].copy(); sig.iloc[:200] = False
                    exs = S.EXITS[name](df) if ex else None
                    tr = lib.trades(df, sig, h, mode, exit_sig=exs, cost=mm.cost(df))
                    if len(tr): tr["sym"] = s; T.append(tr)
                if not T: continue
                T = pd.concat(T)
                E = T.groupby("sig_date").agg(gross=("gross", "mean"), net=("net", "mean")).sort_index()
                x = E["net"].values
                t = mm.nw_tstat(x, h)
                isx = E[E.index <= lib.IS_END]["net"].values; oos = E[E.index > lib.IS_END]["net"].values
                yr = E.groupby(E.index.year)["net"].sum()
                sm = (E.index >= mm.SHOCK_WIN[0]) & (E.index <= mm.SHOCK_WIN[1])
                per = T.groupby("sym")["net"].mean()
                gg = g[(g.sig == name) & (g["mode"] == mode) & (g.h == h) & (g["exit"] == exname)]
                r = {"sig": name, "mode": mode, "h": h, "exit": exname, "n_ev": len(E), "n_tr": len(T),
                     "gross_bp": E["gross"].mean() * 1e4, "net_bp": x.mean() * 1e4, "t_nw": t,
                     "is_net_bp": isx.mean() * 1e4, "is_t": mm.nw_tstat(isx, h), "oos_net_bp": oos.mean() * 1e4,
                     "oos_t": mm.nw_tstat(oos, h), "yil_pozitif": float((yr > 0).mean()),
                     "net_ex2026sok_bp": E.loc[~sm, "net"].mean() * 1e4,
                     "rep12_pozitif": int((per > 0).sum()),
                     "rep17_pozitif": int((gg.mean_net_bp > 0).sum()), "rep17_t2": int((gg.t >= 2).sum()),
                     "rep17_edge_pozitif": int((gg.edge_bp > 0).sum())}
                r["p"] = mm.p_from_t(t, len(E))
                rows.append(r)
                reg.add(f"havuz_{name}_{exname}", "REP12", mode, h, len(E), t, r["net_bp"])
    R = pd.DataFrame(rows)
    R["fdr10"] = lib.bh_fdr(R["p"].values, 0.10)
    # SPY karşılaştırması (takvim sinyalleri genel hisse etkisi mi?)
    spy = []
    for name in ["CA_ay_sonu", "CA_tatil_oncesi", "CA_ay_sonu_3", "VX_backw_donus", "VX_backwardation", "MR_ibs_lt01_dusus"]:
        for mode in ("C0", "O1", "C1"):
            for h in (1, 2, 3):
                sig = S.LIB[name](dfs["SPY"], ctx).reindex(dfs["SPY"].index).fillna(False)
                s, _ = mm.full("SPY", sig, h, mode, df=dfs["SPY"])
                spy.append({"sig": name, "mode": mode, "h": h, "SPY_gross_bp": s.get("mean_gross_bp"), "SPY_t": s.get("t")})
    R = R.merge(pd.DataFrame(spy), on=["sig", "mode", "h"], how="left")
    R.to_csv(os.path.join(mm.OUTD, "genel_aile_havuz.csv"), index=False)
    reg.save()
    pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 400)
    print("toplam havuz testi:", len(R), " FDR(q=0.10) geçen:", int(R.fdr10.sum()),
          " pozitif & FDR:", int((R.fdr10 & (R.net_bp > 0)).sum()))
    cols = ["sig", "mode", "h", "exit", "n_ev", "gross_bp", "net_bp", "t_nw", "p", "fdr10", "is_net_bp", "is_t", "oos_net_bp", "oos_t",
            "yil_pozitif", "net_ex2026sok_bp", "rep12_pozitif", "rep17_pozitif", "rep17_t2", "SPY_gross_bp", "SPY_t"]
    print(R.sort_values("t_nw", ascending=False)[cols].head(30).round(3).to_string(index=False))

if __name__ == "__main__":
    main()
