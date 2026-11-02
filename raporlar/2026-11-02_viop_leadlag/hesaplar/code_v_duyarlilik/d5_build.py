"""v_duyarlilik.csv derleyici: res/d1_long.csv, res/d2_extra.csv, res/d4_*.csv -> out/v_duyarlilik.csv
Sütunlar: madde,hisse,surucu,metrik,donem,v1,v2,v3,v4,fark_v4_v3,ajan_raporu,etiket_v3,etiket_v4,not"""
import vers, numpy as np, pandas as pd
L1 = pd.read_csv(vers.RES + "/d1_long.csv"); X2 = pd.read_csv(vers.RES + "/d2_extra.csv")
FA = pd.read_csv(vers.RES + "/d4_fade_IS_variants.csv"); S = pd.read_csv(vers.RES + "/d4_pair_scan.csv")
AG = {  # ajan raporlarındaki değerler (corr_full/3y/1y, pc, beta) ve etiket
 ("THYAO.IS", "LHA.DE"): ("havacilik r1: 0.313/0.304/0.427, pc 0.182, beta 0.322", "YÜKSEK"),
 ("PGSUS.IS", "EZJ.L"): ("havacilik r1: 0.260/0.220/0.316, pc 0.171, beta 0.256", "YÜKSEK"),
 ("TUPRS.IS", "CRAK"): ("enerji r1: 0.300/0.284/0.342, pc 0.172, beta 0.48", "YÜKSEK"),
 ("TUPRS.IS", "BZ=F"): ("enerji r1: 0.166/0.222/0.341, pc 0.158, beta 0.157", "YÜKSEK"),
 ("TRALT.IS", "GC=F"): ("metal r1: 0.218/0.270/0.413, pc 0.214, beta 0.588", "YÜKSEK"),
 ("EREGL.IS", "MT.AS"): ("metal r1: 0.284/0.225/0.189, pc 0.118, beta 0.230", "ORTA"),
 ("TCELL.IS", "TKC"): ("savunma r1: 0.739/0.836/0.890, pc 0.61, beta 0.69", "YÜKSEK"),
 ("AEFES.IS", "CCOLA.IS"): ("tuketim r1: 0.444/0.521/0.498, pc 0.233, beta 0.471", "YÜKSEK"),
 ("SAHOL.IS", "AKBNK.IS"): ("holding r1: 0.707/0.727/0.794, pc 0.238, beta 0.623", "YÜKSEK"),
 ("EREGL.IS", "ISDMR.IS"): ("metal r1: 0.647/0.724/0.650, pc 0.452, beta 0.614", "YÜKSEK"),
}
rows = []
def add(madde, hisse, surucu, metrik, donem, vals, ajan="", e3="", e4="", note=""):
    v = {k: vals.get(k, np.nan) for k in ["v1", "v2", "v3", "v4"]}
    try: d = float(v["v4"]) - float(v["v3"])
    except (TypeError, ValueError): d = np.nan
    rows.append(dict(madde=madde, hisse=hisse, surucu=surucu, metrik=metrik, donem=donem, **v, fark_v4_v3=d, ajan_raporu=ajan, etiket_v3=e3, etiket_v4=e4, **{"not": note}))
num = lambda x: pd.to_numeric(x, errors="coerce")
# (1) betalar
B = L1[(L1.item == "1_beta") & (L1.metric.isin(["beta", "corr"]))]
for _, r in B.iterrows():
    if r.metric == "corr" and r.period not in ["full", "1y"]: continue
    add("1_beta_XU100", r.stock, "XU100.IS", r.metric, r.period, {k: num(r[k]) for k in ["v1", "v2", "v3", "v4"]},
        note="full=2010-01..2026-10; IS=2014-2020; OOS=2021-2026; ll.ret (BIST takvimi)")
# (1) çiftler
P = L1[L1.item == "1_pair"]
for (a, b), g in P.groupby(["stock", "driver"], sort=False):
    lab = g[g.metric == "label_mech"].iloc[0]
    for _, r in g.iterrows():
        if r.metric in ["n", "label_mech"] or (r.metric == "beta" and r.period != "full"): continue
        add("1_cift", a, b, r.metric, r.period, {k: num(r[k]) for k in ["v1", "v2", "v3", "v4"]}, ajan=AG.get((a, b), ("", ""))[0])
    add("1_cift", a, b, "etiket_mekanik", "full", {}, ajan=AG.get((a, b), ("", ""))[1], e3=lab.v3, e4=lab.v4,
        note="mekanik kural: (|corr|>=0,30 veya |pc|>=0,15) & yıl-işaret>=%75 & pc IS/OOS aynı işaret ve |t|>=2 -> YÜKSEK; pc anlamlı & OOS aynı işaret -> ORTA")
for _, r in X2[X2.item == "1c_pair_robust"].iterrows():
    add("1_cift_saglamlik", r.stock, r.driver, r.metric, r.period, {"v3": r.v3, "v4": r.v4}, note="XU100 kontrollü kısmi korelasyon; winsor %1/%99; Spearman = sıra dönüşümlü")
# (2) bankalar
for _, r in L1[(L1.item == "2_bank_usdtry") & (L1.metric != "n")].iterrows():
    aj = "banka r1: XBANK pc −0,16 (IS −0,18 / OOS −0,15)" if (r.stock == "XBANK.IS" and r.metric == "pc_xu100") else ""
    add("2_banka_USDTRY", r.stock, "TRY=X", r.metric, r.period, {k: num(r[k]) for k in ["v1", "v2", "v3", "v4"]}, ajan=aj,
        note="v1: FX 1 gün kaymalı (hatalı); IS=2014-2020, OOS=2021-2026")
# (3) ES
for _, r in L1[L1.item == "3_es_lag1"].iterrows():
    add("3_ES_lag1", r.stock, r.driver, r.metric, r.period, {k: num(r[k]) for k in ["v1", "v2", "v3", "v4"]}, note="corr(y_t, ES_{t-1}); y=ll.decomp gap/intra/cc")
for _, r in X2[X2.item == "3_es_lag1_spearman"].iterrows():
    add("3_ES_lag1", r.stock, r.driver, r.metric, r.period, {"v3": r.v3, "v4": r.v4})
# (4) gap fade
AJ4 = {("47 medyan", "IS"): "gunici_y: +12,4", ("47 medyan", "OOS"): "gunici_y: +17,8", ("portföy 47", "IS"): "gunici_y: 28,0 (t 7,0)", ("portföy 47", "OOS"): "gunici_y: 16,5 (t 2,8)",
       ("portföy likit23", "OOS"): "gunici_y: 3,1 (t 0,4)", ("portföy illikit24", "OOS"): "gunici_y: 26,9 (t 3,9)", ("OYAKC.IS", "IS"): "gunici_y: +48 (t 2,6)", ("CIMSA.IS", "IS"): "gunici_y: +38 (t 3,4)",
       ("OYAKC.IS", "OOS"): "gunici_y: +50 (t 2,7)", ("CIMSA.IS", "OOS"): "gunici_y: +74 (t 3,8)"}
for _, r in L1[L1.item == "4_gapfade_E0"].iterrows():
    aj = AJ4.get((r.stock, r.period), "") if r.metric in ["mean_bps_gross"] else ""
    add("4_gapfade_E0", r.stock, r.driver, r.metric, r.period, {k: num(r[k]) for k in ["v1", "v2", "v3", "v4"]}, ajan=aj, note="pos=-sign(gap) |gap|>%1, giriş açılış (iyimser), çıkış kapanış; brüt bps/işlem; IS 2014-2020")
F = pd.read_csv(vers.RES + "/d1_fade_stock.csv")
for s in ["OYAKC", "CIMSA", "ALARK", "TRMET", "VESTL"]:
    for per in ["IS", "OOS"]:
        t = F[(F.stock == s) & (F.period == per)].set_index("ver")["t"].to_dict(); add("4_gapfade_E0", s + ".IS", "own |gap|>%1", "t_nw", per, t)
for _, r in FA.iterrows(): pass
for var in FA.variant.unique():
    g = FA[FA.variant == var].set_index("ver")
    for m in ["IS_port_bps", "IS_port_t", "IS_median_stock_bps", "n_trades"]:
        add("4_gapfade_E0_varyant", "portföy 47 / 47 medyan", f"own gap, {var}", m, "IS", g[m].to_dict(), note="|gap|<=%10,5: devre kesici/aşırı açılış günleri (dolum gerçekçi değil) hariç")
for _, r in X2[X2.item.isin(["4b_gapfade_h1", "4c_fade_IS_kaynak"])].iterrows():
    add(r["item"], r.stock, r.driver, r.metric, r.period, {"v3": r.v3, "v4": r.v4}, note=str(r.note) if isinstance(r.note, str) else "")
# yıllara göre portföy (v3 vs v4)
D = {v: {s: vers.L[v].decomp(s + ".IS") for s in vers.VIOP} for v in ["v3", "v4"]}
for v in ["v3", "v4"]:
    gaps = pd.DataFrame({s: D[v][s]["gap"] for s in vers.VIOP}); gaps = gaps[gaps.index >= "2014-01-01"]
    intra = pd.DataFrame({s: D[v][s]["intra"] for s in vers.VIOP}).reindex(gaps.index)
    pos = -np.sign(gaps).where(gaps.abs() > 0.01, 0.0); g = (pos * intra).where((pos != 0) & intra.notna()).mean(axis=1)
    D[v]["_yr"] = (1e4 * g.groupby(g.index.year).mean()).to_dict()
for y in sorted(D["v4"]["_yr"]):
    add("4_gapfade_E0_yil", "portföy 47", "own |gap|>%1", "mean_bps_gross", str(y), {"v3": D["v3"]["_yr"].get(y), "v4": D["v4"]["_yr"].get(y)})
# (5) SASA
AJ5 = {("HEKTS.IS", "corr", "1y"): "hisse ajanı (decomp-cc): 0,547", ("HEKTS.IS", "pc", "full"): "hisse ajanı: 0,301 (YÜKSEK)", ("KMPUR.IS", "corr", "1y"): "hisse ajanı: 0,403",
       ("SMRTG.IS", "corr", "1y"): "hisse ajanı: 0,204", ("BZ=F", "corr", "1y"): "cin/enerji r1: −0,154", ("IVL.BK", "corr", "1y"): "cin/enerji r1: −0,012", ("1326.TW", "corr", "1y"): "cin/enerji r1: −0,075",
       ("CL=F", "corr", "1y"): "cin r1: −0,117", ("CT=F", "corr", "1y"): "enerji r1: 0,109"}
for _, r in L1[L1.item == "5_sasa"].iterrows():
    if r.metric == "n": continue
    add("5_SASA_ret", r.stock, r.driver, r.metric, r.period, {k: num(r[k]) for k in ["v1", "v2", "v3", "v4"]}, ajan=AJ5.get((r.driver, r.metric, r.period), ""),
        note="ll.ret yolu (BIST takvimi; v3'te hacim0 günleri 0 getiri olarak ffill edilir)")
for _, r in X2[X2.item.isin(["5a_sasa_decompcc", "5b_sasa_varshare"])].iterrows():
    if r.metric == "n": continue
    add("5_SASA_" + ("decompcc" if r["item"].startswith("5a") else "varyans"), r.stock, r.driver, r.metric, r.period, {"v3": r.v3, "v4": r.v4}, ajan=str(r.note) if isinstance(r.note, str) else "",
        note="decomp-cc yolu: v3'te hacim0 günleri NaN, ertesi gün çok günlük getiri" if r["item"].startswith("5a") else "R2: XU100 tek değişken; küresel-8 (ES,EEM,STOXX50E,VIX,DXY,BZ,GC,TNX; t ve t-1) düzeltilmiş R2")
# (6) yurt içi çift taraması (hisse ajanı f_y_hisse sync, 138 çift)
S["maxd"] = S[["d_full", "d_IS", "d_1y", "d_corr_1y"]].abs().max(axis=1)
sel = S[(S.maxd >= 0.03) | S.cross015_full | S.cross015_IS].sort_values("maxd", ascending=False)
for _, r in sel.iterrows():
    for m in ["pc_full", "pc_IS", "pc_1y", "corr_1y"]:
        add("6_yurtici_cift_tarama", r.stock + ".IS", r.driver + ".IS", m.split("_")[0], m.split("_")[1], {"v3": r[f"{m}_v3"], "v4": r[f"{m}_v4"]},
            ajan=f"hisse ajanı pc {r.agent_pc} ({r.agent_conf})" if m == "pc_full" else "", note="ll.decomp cc, BIST takvimi, 2014+ (hisse ajanı yöntemi)")
add("6_yurtici_cift_tarama", "138 çift", "-", "medyan |Δpc_full|", "full", {"v4": float(S.d_full.abs().median())}, note=f"max {S.d_full.abs().max():.3f}; IS medyan {S.d_IS.abs().median():.3f} max {S.d_IS.abs().max():.3f}; OOS max {S.d_OOS.abs().max():.3f}; 0,15 eşik geçişi full {int(S.cross015_full.sum())}, IS {int(S.cross015_IS.sum())}")
O = pd.DataFrame(rows)
for c in ["v1", "v2", "v3", "v4", "fark_v4_v3"]:
    O[c] = [round(x, 4) if isinstance(x, (float, np.floating)) and not np.isnan(x) else ("" if (isinstance(x, float) and np.isnan(x)) else x) for x in O[c]]
O.to_csv(vers.OUT + "/v_duyarlilik.csv", index=False)
print(O.shape); print(O.madde.value_counts().to_string())
