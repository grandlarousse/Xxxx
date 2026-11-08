"""2) genel_tum.csv aile içi tutarlılık. Çalıştır: python3 -I kod/ajan_tahvil_doviz/02_genel_aile.py
* Aile içi BH-FDR (q=0.10) ailenin tüm satırları (40 ETF x 297 satır) üzerinde (iki yönlü p).
* Tutarlılık yalnız grup temsilcilerinde sayılır (td.REPS_TAHVIL: 11, td.REPS_DOVIZ: 8) -> kopyalar ve
  kaldıraçlı kopyalar bağımsız kanıt sayılmaz.
* Seçilen kurallar için temsilci sepeti (aynı gün açılan işlemlerin ortalaması) ile havuzlanmış t yeniden hesaplanır.
Çıktılar: genel_aile_tutarlilik_tahvil.csv, genel_aile_tutarlilik_doviz.csv, genel_aile_fdr.csv, genel_aile_havuz.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import td, lib, strategies as S

pd.set_option("display.width", 260); pd.set_option("display.max_rows", 300); pd.set_option("display.max_columns", 40)
# DİKKAT: sonuclar/genel_tum.csv'deki 33 aile ETF'inde dağıtımlar eksik (bkz. 00_temettu_indir.py); burada
# dağıtım-düzeltmeli yeniden çalıştırma (02a_genel_duzeltilmis.py -> genel_duzeltilmis.csv) kullanılır.
g = pd.read_csv(os.path.join(td.OUT, "genel_duzeltilmis.csv"))
x = g[g.sym.isin(td.FAM)].copy()
x["fdr_aile"] = lib.bh_fdr(x["p"].values, 0.10)
N_TESTS = len(x)
print("Aile satırı (test):", N_TESTS, " FDR geçen:", int(x.fdr_aile.sum()), " pozitif net:", int((x.fdr_aile & (x.mean_net_bp > 0)).sum()))
print("FDR geçen ETF dağılımı (pozitif):", x[x.fdr_aile & (x.mean_net_bp > 0)].sym.value_counts().to_dict())
print("FDR geçen ETF dağılımı (negatif):", x[x.fdr_aile & (x.mean_net_bp < 0)].sym.value_counts().head(20).to_dict())
x[x.fdr_aile].sort_values("t", ascending=False).to_csv(os.path.join(td.OUT, "genel_aile_fdr.csv"), index=False)
# kaldıraçsız ETF'lerde edge (koşulsuz ortalamaya göre fark) bazında FDR: ters/kaldıraçlı drift etkisi dışarıda
xe = x[x.sym.isin(td.REPS)].copy()
xe["fdr_edge_reps"] = lib.bh_fdr(xe["p_edge"].values, 0.10)
print("Temsilcilerde edge-FDR geçen:", int(xe.fdr_edge_reps.sum()))
print(xe[xe.fdr_edge_reps][["sym", "sig", "mode", "h", "exit", "n", "mean_gross_bp", "mean_net_bp", "edge_bp", "t_edge", "is_net_bp", "oos_net_bp"]]
      .sort_values("t_edge").round(2).to_string(index=False))

def consist(reps, nm):
    r = x[x.sym.isin(reps)].copy()
    r["isoos_pos"] = (r.is_net_bp > 0) & (r.oos_net_bp > 0)
    r["isoos_gpos"] = (r.is_net_bp + r.cost_bp > 0) & (r.oos_net_bp + r.cost_bp > 0)
    agg = r.groupby(["sig", "mode", "h", "exit"]).apply(lambda d: pd.Series({
        "n_rep": len(d), "pos_net": int((d.mean_net_bp > 0).sum()), "pos_gross": int((d.mean_gross_bp > 0).sum()),
        "pos_edge": int((d.edge_bp > 0).sum()),
        "isoos_pos": int(d.isoos_pos.sum()), "isoos_gross_pos": int(d.isoos_gpos.sum()), "t_ge2": int((d.t >= 2).sum()),
        "fdr_pos": int((d.fdr_aile & (d.mean_net_bp > 0)).sum()),
        "med_net_bp": d.mean_net_bp.median(), "med_gross_bp": d.mean_gross_bp.median(), "med_edge_bp": d.edge_bp.median(),
        "med_t": d.t.median(), "med_t_edge": d.t_edge.median(), "med_n": d.n.median(), "med_cost": d.cost_bp.median(),
        "best": d.sort_values("t").sym.iloc[-1], "best_t": d.t.max()}), include_groups=False).reset_index()
    agg = agg.sort_values(["isoos_pos", "med_t"], ascending=False)
    agg.to_csv(os.path.join(td.OUT, f"genel_aile_tutarlilik_{nm}.csv"), index=False)
    print(f"\n=== {nm}: temsilciler {reps}")
    print("en tutarlı (IS ve OOS net>0 temsilci sayısına göre):")
    print(agg.head(25).round(2).to_string(index=False))
    print("brüt kenar (edge) en tutarlı:")
    print(agg.sort_values(["pos_edge", "med_t_edge"], ascending=False).head(15).round(2).to_string(index=False))
    return agg

a_t = consist(td.REPS_TAHVIL, "tahvil")
a_d = consist(td.REPS_DOVIZ, "doviz")

# Havuzlanmış sepet t'si: her iki alt ailede, temsilcilerin en az %60'ında net>0 olan kurallar
ctx = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}
rows = []
for agg, reps, nm in ((a_t, td.REPS_TAHVIL, "tahvil"), (a_d, td.REPS_DOVIZ, "doviz")):
    cand = pd.concat([agg[(agg.pos_net >= 0.6 * agg.n_rep)].head(12),
                      agg[agg.pos_edge >= 0.8 * agg.n_rep].sort_values("med_t_edge", ascending=False).head(8)]).drop_duplicates(["sig", "mode", "h", "exit"])
    for _, c in cand.iterrows():
        trs = []
        for s in reps:
            df = td.load(s)
            sig = S.LIB[c.sig](df, ctx).reindex(df.index).fillna(False).astype(bool); sig.iloc[:200] = False
            ex = S.EXITS[c.sig](df) if c.exit == "kural_max3" else None
            _, tr = lib.evaluate(df, sig, int(c.h), c["mode"], td.cost_at(df), exit_sig=ex)
            trs.append(tr)
        tb, nb, mb = td.basket(trs)
        a = pd.concat(trs); b = a.groupby("entry_date")["net"].mean()
        bis = b[b.index <= lib.IS_END]; boos = b[b.index > lib.IS_END]
        bg = a.groupby("entry_date")["gross"].mean()
        rows.append({"alt_aile": nm, "sig": c.sig, "mode": c["mode"], "h": c.h, "exit": c.exit, "pos_net": c.pos_net, "pos_edge": c.pos_edge, "n_rep": c.n_rep,
                     "sepet_brut_bp": bg.mean() * 1e4, "sepet_brut_t": td._t(bg.values),
                     "sepet_gun": nb, "sepet_net_bp": mb, "sepet_t": tb, "sepet_is_bp": bis.mean() * 1e4, "sepet_is_t": td._t(bis.values),
                     "sepet_oos_bp": boos.mean() * 1e4, "sepet_oos_t": td._t(boos.values)})
hv = pd.DataFrame(rows)
hv.to_csv(os.path.join(td.OUT, "genel_aile_havuz.csv"), index=False)
print("\nHavuzlanmış temsilci sepeti:")
print(hv.round(2).to_string(index=False))
