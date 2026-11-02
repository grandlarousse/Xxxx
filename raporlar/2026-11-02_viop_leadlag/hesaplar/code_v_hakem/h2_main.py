"""H2: ANA TEST — 'sektöre özgü bilgi açılışta eksik fiyatlanıyor' hipotezi, 47 hisse, ön-kayıtlı sepetler.
BİRİNCİL (ön-kayıt): y = hedge'li gün-içi (Y_h), x = z(X_res) [emsal - beta*bölge endeksi, geçmiş 250g z, ±4 kırpma].
Çıktılar: res/h2_*.csv, res/h2_summary.txt
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vh
from peers import PEERS, SECTOR, FAMOUS

t0 = time.time()
L = lambda k: pd.read_parquet(vh.RES + f"/{k}.parquet").loc[vh.START:vh.END]
Y_h, Y_raw, G_h = L("Y_h"), L("Y_raw"), L("G_h")
X = {k: L(k) for k in ["X_res", "X_raw", "X_mkt", "X_d1", "X_res_AM", "X_res_EU", "X_res_ASIA", "X_dom", "OWN_l1"]}
PR = L("PR")
STOCKS = list(PEERS.keys())
Z = {k: v.apply(vh.zscore) for k, v in X.items()}
idx = Y_h.index
PERS = ["ALL", "IS", "OOS"]
out_txt = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); out_txt.append(s)

def per_stock(Y, Zx, label):
    rows = []
    for s in STOCKS:
        r = {"def": label, "stock": s, "sector": SECTOR[s]}
        for per in PERS:
            m = vh.period_mask(idx, per)
            b, t, n, c = vh.ols_nw(Y[s].values[m].astype(float), Zx[s].values[m].astype(float))
            r[f"b_{per}"] = 1e4 * b; r[f"t_{per}"] = t; r[f"n_{per}"] = n; r[f"c_{per}"] = c
        rows.append(r)
    D = pd.DataFrame(rows)
    D["p_ALL"] = vh.p2(D.t_ALL); D["q_ALL"] = vh.bh(D.p_ALL.values)
    D["p_IS"] = vh.p2(D.t_IS); D["q_IS"] = vh.bh(D.p_IS.values)
    D["p_OOS"] = vh.p2(D.t_OOS); D["q_OOS"] = vh.bh(D.p_OOS.values)
    return D

def pooled(Y, Zlist, per="ALL", stocks=None, fe=True):
    m = vh.period_mask(idx, per)
    cols = stocks or STOCKS
    return vh.pooled_dk(Y.loc[m, cols], [z.loc[m, cols] for z in Zlist], fe=fe)

def summ(D, label):
    pos = (D.b_ALL > 0).sum(); t2 = (D.t_ALL > 2).sum(); tn2 = (D.t_ALL < -2).sum()
    fdr = (D.q_ALL < 0.05).sum(); fdr_is = (D.q_IS < 0.05).sum()
    rep = D[(D.q_IS < 0.05)]; rep_ok = ((rep.t_OOS > 1.96)).sum()
    oos_pos = (D.b_OOS > 0).sum(); oos_t2 = (D.t_OOS > 1.96).sum()
    return {"def": label, "n_stock": len(D), "b>0": int(pos), "t>2": int(t2), "t<-2": int(tn2), "BH_q05_full": int(fdr), "BH_q05_IS": int(fdr_is),
            "IS_BH->OOS_t>1.96": f"{rep_ok}/{len(rep)}", "OOS_b>0": int(oos_pos), "OOS_t>1.96": int(oos_t2),
            "median_b_bps": round(D.b_ALL.median(), 2), "median_t": round(D.t_ALL.median(), 2)}

# ================= 1) TANIM MERDİVENİ (aynı veri, tanımlar yan yana) =================
LADDER = [
    ("L1 ham sepet -> ham gün-içi", Y_raw, ["X_raw"]),
    ("L2 artık sepet -> ham gün-içi", Y_raw, ["X_res"]),
    ("L3 ham sepet -> hedge'li gün-içi", Y_h, ["X_raw"]),
    ("L4b beta=1 fark -> hedge'li gün-içi", Y_h, ["X_d1"]),
    ("L4 artık sepet -> hedge'li gün-içi [BİRİNCİL]", Y_h, ["X_res"]),
]
allD = []; lad = []
for label, Y, xs in LADDER:
    D = per_stock(Y, Z[xs[0]], label); allD.append(D)
    s = summ(D, label)
    for per in PERS:
        r = pooled(Y, [Z[xs[0]]], per)
        s[f"pool_b_{per}"] = round(1e4 * r["b"][0], 2); s[f"pool_tDK_{per}"] = round(r["t_dk"][0], 2); s[f"pool_tCL_{per}"] = round(r["t_cl"][0], 2)
    lad.append(s)
LAD = pd.DataFrame(lad); LAD.to_csv(vh.RES + "/h2_ladder.csv", index=False)
DD = pd.concat(allD); DD.to_csv(vh.RES + "/h2_per_stock_all_defs.csv", index=False)
P("== TANIM MERDİVENİ (47 hisse; b = 1σ sinyal başına gün-içi bps; pool t = Driscoll–Kraay) =="); P(LAD.to_string(index=False))

PRIM = DD[DD["def"].str.contains("BİRİNCİL")].copy()
P("\n== BİRİNCİL: hisse bazında (t sıralı) =="); P(PRIM.sort_values("t_ALL", ascending=False)[["stock", "sector", "b_ALL", "t_ALL", "q_ALL", "b_IS", "t_IS", "b_OOS", "t_OOS", "q_OOS"]].round(3).to_string(index=False))

# ================= 2) L0: tek emsal ham (tarama tanımı) — aile içi BH =================
rows = []
for s in STOCKS:
    for p in PEERS[s]:
        if p not in PR.columns: continue
        for per in ["ALL", "IS", "OOS"]:
            m = vh.period_mask(idx, per)
            c, t, n = vh.corr_hc(Y_raw[s].values[m].astype(float), PR[p].values[m].astype(float))
            ch, th, nh = vh.corr_hc(Y_h[s].values[m].astype(float), PR[p].values[m].astype(float))
            rows.append({"stock": s, "peer": p, "region": vh.region_name(p), "per": per, "c_raw": c, "t_raw": t, "n": n, "c_h": ch, "t_h": th})
L0 = pd.DataFrame(rows)
L0f = L0[L0.per == "ALL"].copy()
L0f["q_raw_fam"] = vh.bh(vh.p2(L0f.t_raw.values)); L0f["q_h_fam"] = vh.bh(vh.p2(L0f.t_h.values))
# 48.124'lük tarama ailesine gömülü olsaydı (diğerleri null varsayımıyla) BH eşiği: k. sırada p <= 0.05*k/48124
L0f["pass_48k_rank1"] = vh.p2(L0f.t_raw) <= 0.05 / 48124
L0.to_csv(vh.RES + "/h2_L0_pairs.csv", index=False); L0f.to_csv(vh.RES + "/h2_L0_full.csv", index=False)
P(f"\n== L0 tek emsal (tarama tanımı: ham gün-içi ~ ham emsal_t-1/Asya t) aile = {len(L0f)} çift ==")
P(f" ham: t>0 oranı {np.mean(L0f.t_raw>0):.3f}, |t|>2: {(L0f.t_raw.abs()>2).sum()}, t>2: {(L0f.t_raw>2).sum()}, t<-2: {(L0f.t_raw<-2).sum()}, aile-içi BH q<0,05: {(L0f.q_raw_fam<0.05).sum()}, 48k-ailesi 1. sıra eşiği (t>~4,9) geçen: {L0f.pass_48k_rank1.sum()}")
P(f" hedge'li: t>0 oranı {np.mean(L0f.t_h>0):.3f}, t>2: {(L0f.t_h>2).sum()}, t<-2: {(L0f.t_h<-2).sum()}, aile-içi BH q<0,05: {(L0f.q_h_fam<0.05).sum()}")
P(" en iyi 12 (ham t):"); P(L0f.sort_values("t_raw", ascending=False).head(12)[["stock", "peer", "c_raw", "t_raw", "q_raw_fam", "c_h", "t_h", "q_h_fam"]].round(3).to_string(index=False))
# IS-en iyi seçim (kazananın laneti) — tarama yöntemi bu aile içinde
L0i = L0[L0.per == "IS"].set_index(["stock", "peer"]); L0o = L0[L0.per == "OOS"].set_index(["stock", "peer"])
top = L0i.reindex(L0i.t_raw.abs().sort_values(ascending=False).index).head(10)
top = top.join(L0o[["c_raw", "t_raw"]], rsuffix="_OOS")
P(" IS |t|'ye göre seçilen 10 çift (ham) -> OOS:"); P(top[["c_raw", "t_raw", "c_raw_OOS", "t_raw_OOS"]].round(3).to_string())
P(f"  OOS'ta IS ile aynı işaret: {(np.sign(top.t_raw)==np.sign(top.t_raw_OOS)).sum()}/10; OOS |t|>1,96 aynı işaret: {((np.sign(top.t_raw)==np.sign(top.t_raw_OOS))&(top.t_raw_OOS.abs()>1.96)).sum()}/10")

# ================= 3) PİYASA BİLEŞENİ vs SEKTÖR ARTIĞI (hipotezin ikinci yarısı) =================
P("\n== Piyasa bileşeni (beta*bölge endeksi) ve sektör artığı birlikte, havuzlanmış ==")
mk = []
for tgt_name, Y in [("hedge'li gün-içi", Y_h), ("ham gün-içi", Y_raw), ("hedge'li gap", G_h)]:
    for per in PERS:
        r = pooled(Y, [Z["X_res"], Z["X_mkt"]], per)
        mk.append({"hedef": tgt_name, "per": per, "b_artik_bps": 1e4 * r["b"][0], "t_artik": r["t_dk"][0], "b_piyasa_bps": 1e4 * r["b"][1], "t_piyasa": r["t_dk"][1], "nobs": r["nobs"]})
MK = pd.DataFrame(mk); MK.to_csv(vh.RES + "/h2_market_vs_resid.csv", index=False); P(MK.round(2).to_string(index=False))
# açılışta fiyatlanma oranı: gap ve gün-içi tepkisi (aynı sinyal)
gi = []
for per in PERS:
    rg = pooled(G_h, [Z["X_res"]], per); ri = pooled(Y_h, [Z["X_res"]], per)
    bg, bi = 1e4 * rg["b"][0], 1e4 * ri["b"][0]
    gi.append({"per": per, "b_gap": bg, "t_gap": rg["t_dk"][0], "b_intra": bi, "t_intra": ri["t_dk"][0], "gun_ici_payi": bi / (bg + bi) if (bg + bi) != 0 else np.nan})
GI = pd.DataFrame(gi); GI.to_csv(vh.RES + "/h2_gap_vs_intra.csv", index=False)
P("\n== Sektör artığı sinyalinin ne kadarı açılışta (gap), ne kadarı gün içinde fiyatlanıyor (hedge'li) =="); P(GI.round(3).to_string(index=False))

# ================= 4) BÖLGE AYRIŞTIRMASI =================
P("\n== Bölge alt-sepetleri (birlikte; havuzlanmış hedge'li gün-içi) ==")
rg = []
for per in PERS:
    for regs in [["X_res_AM"], ["X_res_EU"], ["X_res_ASIA"]]:
        cols = [s for s in STOCKS if Z[regs[0]][s].notna().sum() > 500]
        r = pooled(Y_h, [Z[regs[0]]], per, stocks=cols)
        rg.append({"per": per, "bolge": regs[0], "n_hisse": len(cols), "b_bps": 1e4 * r["b"][0], "t_dk": r["t_dk"][0], "nobs": r["nobs"]})
RG = pd.DataFrame(rg); RG.to_csv(vh.RES + "/h2_regions.csv", index=False); P(RG.round(2).to_string(index=False))

# ================= 5) GENEL Mİ, SEÇİLMİŞ Mİ? =================
P("\n== Genellik: ünlü örnekler hariç / sektör bazında / sektör-dışarıda (birincil tanım, havuzlanmış DK t) ==")
gen = []
non_f = [s for s in STOCKS if s not in FAMOUS]
for nm, cols in [("47 hisse", STOCKS), ("ünlüler hariç (41)", non_f), ("yalnız ünlüler (6)", FAMOUS)] + \
        [(f"sektör={sec}", [s for s in STOCKS if SECTOR[s] == sec]) for sec in sorted(set(SECTOR.values()))] + \
        [(f"hariç {sec}", [s for s in STOCKS if SECTOR[s] != sec]) for sec in sorted(set(SECTOR.values()))]:
    rr = {"grup": nm, "n": len(cols)}
    for per in PERS:
        r = pooled(Y_h, [Z["X_res"]], per, stocks=cols)
        rr[f"b_{per}"] = 1e4 * r["b"][0]; rr[f"t_{per}"] = r["t_dk"][0]
    gen.append(rr)
GEN = pd.DataFrame(gen); GEN.to_csv(vh.RES + "/h2_generality.csv", index=False); P(GEN.round(2).to_string(index=False))
# işaret testi
from scipy import stats as st
k = int((PRIM.b_ALL > 0).sum()); P(f"\nİşaret testi (birincil, tam dönem): {k}/47 pozitif, binom p(tek yön) = {st.binom.sf(k-1, 47, 0.5):.4f}")
k2 = int((PRIM.b_OOS > 0).sum()); P(f"İşaret testi OOS: {k2}/47 pozitif, binom p = {st.binom.sf(k2-1, 47, 0.5):.4f}")
kn = int((PRIM[~PRIM.stock.isin(FAMOUS)].b_ALL > 0).sum()); P(f"Ünlüler hariç: {kn}/41 pozitif, binom p = {st.binom.sf(kn-1, 41, 0.5):.4f}")

# ================= 6) PLASEBO / NULL =================
P("\n== Plasebo ==")
pl = []
for nm, Zx in [("sinyal 1 gün bayat (t-1 penceresi -> t)", Z["X_res"].shift(1)), ("sinyal 2 gün bayat", Z["X_res"].shift(2))]:
    for per in PERS:
        r = pooled(Y_h, [Zx], per); pl.append({"plasebo": nm, "per": per, "b_bps": 1e4 * r["b"][0], "t_dk": r["t_dk"][0]})
PL = pd.DataFrame(pl); P(PL.round(2).to_string(index=False))
# sektör-karıştırma permütasyonu: her hisseye FARKLI sektörden rastgele bir hissenin sepeti verilir
rng = np.random.default_rng(20261102)
Zr = Z["X_res"]; Yd = Y_h
def CQ(per):
    m = vh.period_mask(idx, per)
    Yv = Yd.loc[m, STOCKS].values; C = np.zeros((47, 47)); Q = np.zeros((47, 47))
    for j, sj in enumerate(STOCKS):
        zj = Zr.loc[m, sj].values
        mm = ~np.isnan(Yv) & ~np.isnan(zj)[:, None]
        Yc = np.where(mm, Yv, np.nan); Ym = np.nanmean(Yc, 0)
        zc = np.where(mm, zj[:, None], np.nan); zm = np.nanmean(zc, 0)
        C[:, j] = np.nansum((Yc - Ym) * (zc - zm), 0); Q[:, j] = np.nansum((zc - zm) ** 2, 0)
    return C, Q
sec = np.array([SECTOR[s] for s in STOCKS])
perm_res = []
for per in PERS:
    C, Q = CQ(per)
    b_obs = np.trace(C) / np.trace(Q)
    bs = []
    for it in range(5000):
        pi = np.empty(47, int)
        for i in range(47):
            cand = np.where(sec != sec[i])[0]; pi[i] = rng.choice(cand)
        bs.append(C[np.arange(47), pi].sum() / Q[np.arange(47), pi].sum())
    bs = np.array(bs)
    perm_res.append({"per": per, "b_gercek_bps": 1e4 * b_obs, "null_ort_bps": 1e4 * bs.mean(), "null_sd_bps": 1e4 * bs.std(), "null_%95_bps": 1e4 * np.quantile(bs, 0.95),
                     "p_tek_yon": (np.sum(bs >= b_obs) + 1) / (len(bs) + 1), "z": (b_obs - bs.mean()) / bs.std()})
PERM = pd.DataFrame(perm_res); PERM.to_csv(vh.RES + "/h2_perm.csv", index=False)
P("\n== Sektör-karıştırma permütasyon null'ı (5.000; her hisseye başka sektörün sepeti) =="); P(PERM.round(3).to_string(index=False))

# ================= 7) YILLARA GÖRE =================
yr = []
for y in range(2014, 2027):
    m = (idx.year == y)
    r = vh.pooled_dk(Y_h.loc[m, STOCKS], [Z["X_res"].loc[m, STOCKS]])
    r2 = vh.pooled_dk(Y_h.loc[m, non_f], [Z["X_res"].loc[m, non_f]])
    yr.append({"yil": y, "b_47": 1e4 * r["b"][0], "t_47": r["t_dk"][0], "b_unluhariç": 1e4 * r2["b"][0], "t_unluhariç": r2["t_dk"][0]})
YR = pd.DataFrame(yr); YR.to_csv(vh.RES + "/h2_years.csv", index=False)
P("\n== Yıllara göre havuzlanmış eğim (birincil) =="); P(YR.round(2).to_string(index=False))
P(f" pozitif yıl: 47 hisse {int((YR.b_47>0).sum())}/13, ünlüler hariç {int((YR.b_unluhariç>0).sum())}/13")

open(vh.RES + "/h2_summary.txt", "w").write("\n".join(out_txt))
print(f"bitti {time.time()-t0:.1f}s")
