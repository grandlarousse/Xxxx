"""Görev 2: genel kütüphanenin (strategies.LIB, 31 sinyal) aile HAVUZU testi.
Aynı sinyal x mod x h x çıkış, likit (>=10 mn $) bağımsız 1x temsilcilerde (kopyalar hariç) çalıştırılır;
işlemler sinyal tarihine göre kümelenir (aynı gün işlem yapan ETF'lerin ortalaması = 1 gözlem) ->
tarih-kümeli ortalama ve Newey-West t (ortak faktörü ve örtüşmeyi hesaba katar). BH-FDR (q=0.10) tüm kombinasyonlar üzerinde.
Çalıştır: python3 -I kod/ajan_uluslararasi/a2_aile_havuz.py   [--all : 47 bağımsız temsilcinin tamamı]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak, lib
import strategies as S

pooled = ortak.pooled

def main(all_reps=False):
    reps = ortak.independent(None if all_reps else 10)
    ctx = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}
    allt = {}
    for s in reps:
        df = lib.load(s)
        cost = lib.cost_bp(df)
        for name, fn in S.LIB.items():
            sig = fn(df, ctx).reindex(df.index).fillna(False).astype(bool)
            sig.iloc[:200] = False
            for mode in ("C0", "O1", "C1"):
                cfgs = [(h, "sabit") for h in (1, 2, 3)] + ([(3, "kural_max3")] if name in S.EXITS else [])
                for h, ex in cfgs:
                    exs = S.EXITS[name](df) if ex == "kural_max3" else None
                    tr = lib.trades(df, sig, h, mode, exs, cost)
                    if len(tr) == 0: continue
                    tr["sym"] = s
                    allt.setdefault((name, mode, h, ex), []).append(tr)
    rows = []
    for key, lst in allt.items():
        trs = pd.concat(lst, ignore_index=True)
        r = pooled(trs, key[2]); r.update(dict(zip(["sig", "mode", "h", "exit"], key)))
        r["k_etf"] = trs["sym"].nunique()
        rows.append(r)
    R = pd.DataFrame(rows)
    from scipy import stats as st
    R["p"] = st.norm.sf(R["t_nw"])          # tek yönlü (H1: net > 0)
    R["fdr10"] = lib.bh_fdr(R["p"].values, 0.10) & (R["mean_net_bp"] > 0)
    # mod sağlamlığı: aynı sig,h,exit için diğer modlarda brüt ortalama
    gm = R.pivot_table(index=["sig", "h", "exit"], columns="mode", values="mean_gross_bp")
    R = R.merge(gm.add_prefix("gross_").reset_index(), on=["sig", "h", "exit"], how="left")
    R = R.sort_values("t_nw", ascending=False)
    fn = os.path.join(ortak.OUT, "aile_havuz_genel" + ("_tum47" if all_reps else "") + ".csv")
    R.to_csv(fn, index=False)
    print("temsilciler:", len(reps), "kombinasyon (test) sayısı:", len(R), "FDR geçen:", int(R["fdr10"].sum()))
    pd.set_option("display.width", 260)
    cols = ["sig", "mode", "h", "exit", "k_etf", "n_dates", "n_trades", "mean_gross_bp", "mean_net_bp", "t_nw", "is_net_bp", "is_t",
            "oos_net_bp", "oos_t", "years_pos_frac", "pf", "fdr10", "gross_C0", "gross_O1", "gross_C1"]
    print(R[cols].head(25).round(2).to_string(index=False))
    return R

if __name__ == "__main__":
    main("--all" in sys.argv)
