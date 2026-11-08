"""2a) Genel kütüphaneyi (kod/strategies.py, aynı parametreler, aynı ısınma/maliyet) dağıtım-düzeltmeli veriyle (td.load)
aile ETF'lerinde yeniden çalıştırır. kod/run_generic.py ile birebir aynı döngü; tek fark veri yükleyici.
Çalıştır: python3 -I kod/ajan_tahvil_doviz/02a_genel_duzeltilmis.py   (tek süreç, ~2-4 dk)
Çıktı: sonuclar/aile_tahvil_doviz/genel_duzeltilmis.csv (genel_tum.csv ile aynı sütunlar)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import td, lib, strategies as S

CTX = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}

def run_one(sym):
    df = td.load(sym)
    if len(df) < 500: return []
    cost = lib.cost_bp(df)
    rows = []
    for name, fn in S.LIB.items():
        try:
            sig = fn(df, CTX).reindex(df.index).fillna(False).astype(bool)
        except Exception:
            continue
        sig.iloc[:200] = False
        nsig = int(sig.sum())
        for mode in ("C0", "O1", "C1"):
            for h in (1, 2, 3):
                s, tr = lib.evaluate(df, sig, h, mode, cost, label=name)
                s.update({"sym": sym, "sig": name, "exit": "sabit", "n_sig_days": nsig}); rows.append(s)
            if name in S.EXITS:
                ex = S.EXITS[name](df)
                s, tr = lib.evaluate(df, sig, 3, mode, cost, exit_sig=ex, label=name)
                s.update({"sym": sym, "sig": name, "exit": "kural_max3", "n_sig_days": nsig}); rows.append(s)
    for r in rows:
        r["p"] = lib.t_to_p(r.get("t", np.nan), r.get("n", 0))
        r["p_edge"] = lib.t_to_p(r.get("t_edge", np.nan), r.get("n", 0))
        r["cat"] = "tahvil" if sym in td.TAHVIL else "doviz"
    return rows

if __name__ == "__main__":
    allrows = []
    for s in td.FAM:
        allrows += run_one(s)
    res = pd.DataFrame(allrows)
    res.to_csv(os.path.join(td.OUT, "genel_duzeltilmis.csv"), index=False)
    g = pd.read_csv(os.path.join(td.ROOT, "sonuclar", "genel_tum.csv"))
    g = g[g.sym.isin(td.FAM)]
    m = res.merge(g, on=["sym", "sig", "mode", "h", "exit"], suffixes=("", "_eski"))
    m["fark_brut"] = m["mean_gross_bp"] - m["mean_gross_bp_eski"]
    print("yazıldı", res.shape)
    print("Düzeltmenin ortalama brüt etkisi (bp), ETF bazında:")
    print(m.groupby("sym")["fark_brut"].mean().round(2).sort_values().to_string())
    print("Sinyal bazında (tüm aile):")
    print(m.groupby("sig")["fark_brut"].mean().round(2).sort_values().to_string())
