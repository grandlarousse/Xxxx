"""Adım 5b: BT3g (küme-göreli gap sapmasının gün-içinde dönüşü) ayrıştırması ve gerçekçi giriş testi.
(1) Regresyon (havuz, 47 hedef): intra_j,t = a + b1 gap_j,t + b2 eşgap_t + b3 XU100gap_t (+ IS/OOS)  -> eşlerin gap'i hedefi gün-içinde 'çekiyor' mu, yoksa sadece kendi gap'in dönüşü mü?
(2) Varyantlar: kendi gap (piyasa-nötr, 47 içinde) / IS-küme göreli / 177-hisse eş göreli; maliyet 0/8/15.
(3) Gecikmeli giriş (saatlik veri, 2023-12..2026-10): sinyal açılışta (günlük o), giriş ilk 60 dk bar kapanışı (~10:30 TSİ), çıkış günün son saatlik bar kapanışı.
Çıktı: res/gapfade.txt
"""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata
sys.path.insert(0, hdata.SCR + "/code"); import ll
import statsmodels.api as sm
D = hdata.load(); cc, gap, intra = D["cc"], D["gap"], D["intra"]
TGT = hdata.VIOP; idx = cc.index; SPLIT = pd.Timestamp(hdata.SPLIT)
LEAD = [c for c in cc.columns if c not in hdata.IDX]
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)
labI = pd.read_csv(os.path.join(hdata.RES, "clusters_is.csv"), index_col=0)["cl"]
# IS eşleri (177 hisseden en yakın 3, IS artık korelasyonu)
ccIS = cc[cc.index < SPLIT]; m = ccIS["XU100"]
def rs(s):
    d = pd.concat([s, m], axis=1).dropna(); b = np.cov(d.iloc[:, 0], d.iloc[:, 1])[0, 1] / d.iloc[:, 1].var() if len(d) > 100 else np.nan
    return s - b * m
CIS = pd.DataFrame({c: rs(ccIS[c]) for c in LEAD}).corr(min_periods=250)
peers = {j: list(CIS[j].drop(j).dropna().sort_values(ascending=False).head(3).index) for j in TGT if CIS[j].notna().sum() > 3}
peers.update({j: [] for j in TGT if j not in peers})
# (1) havuz regresyonu
rows = []
for j in TGT:
    if not peers[j]: continue
    pg = gap[peers[j]].mean(axis=1)
    d = pd.DataFrame({"y": intra[j], "g": gap[j], "pg": pg, "mg": gap["XU100"], "tgt": j}).dropna(); rows.append(d)
Pool = pd.concat(rows)
for nm, msk in [("FULL", np.ones(len(Pool), bool)), ("IS", Pool.index < SPLIT), ("OOS", Pool.index >= SPLIT)]:
    x = Pool[msk]
    mm = sm.OLS(x.y, sm.add_constant(x[["g", "pg", "mg"]])).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x.index)[0]})
    P(f"(1) havuz intra_t ~ kendi gap_t + eş gap_t + XU100 gap_t [{nm}, n={len(x)}, tarih-kümeli SE]: " + ", ".join(f"{k}={mm.params[k]:.3f} (t={mm.tvalues[k]:.1f})" for k in ["g", "pg", "mg"]))
# hedef başına b2 (eş gap) işaret sayısı
b2 = []
for j in TGT:
    if not peers[j]: continue
    x = Pool[Pool.tgt == j]
    mm = sm.OLS(x.y, sm.add_constant(x[["g", "pg", "mg"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    xi = x[x.index < SPLIT]; xo = x[x.index >= SPLIT]
    ti = sm.OLS(xi.y, sm.add_constant(xi[["g", "pg", "mg"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5}).tvalues if len(xi) > 250 else pd.Series(np.nan, index=["g", "pg", "mg"])
    to = sm.OLS(xo.y, sm.add_constant(xo[["g", "pg", "mg"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5}).tvalues
    b2.append({"target": j, "peers": ",".join(peers[j]), "b_own": mm.params["g"], "t_own": mm.tvalues["g"], "b_peer": mm.params["pg"], "t_peer": mm.tvalues["pg"],
               "t_peer_IS": ti["pg"], "t_peer_OOS": to["pg"], "t_own_IS": ti["g"], "t_own_OOS": to["g"]})
B2 = pd.DataFrame(b2).sort_values("t_peer", ascending=False); B2.to_csv(os.path.join(hdata.RES, "gap_peer_reg.csv"), index=False)
P(f"hedef başına eş-gap katsayısı: t>2 {int((B2.t_peer>2).sum())}, t<-2 {int((B2.t_peer<-2).sum())} / {len(B2)}; kendi gap t<-2: {int((B2.t_own<-2).sum())}")
P(B2.head(12).round(2).to_string(index=False))
# (2) varyantlar
def port(Wt, tgt, cost):
    Wt = Wt.reindex(columns=TGT).fillna(0)
    ok = tgt[TGT].notna(); Wt = Wt.where(ok, 0)
    g = Wt.abs().sum(axis=1); Wn = Wt.div(g.replace(0, np.nan), axis=0).fillna(0)
    return (Wn * tgt[TGT].fillna(0)).sum(axis=1) - cost / 1e4 * Wn.abs().sum(axis=1)
def st(p):
    r = {}
    for nm, mk in [("IS", p.index < SPLIT), ("OOS", p.index >= SPLIT)]:
        x = p[mk]; x = x[x != 0]; r[nm] = (1e4 * x.mean(), x.mean() / x.std() * np.sqrt(252), ll.nw_t(x)[1])
    yr = (p.groupby(p.index.year).mean() > 0).mean()
    return " | ".join(f"{k}: {v[0]:.1f}bps SR={v[1]:.2f} t={v[2]:.1f}" for k, v in r.items()) + f" | pozitif yıl %{100*yr:.0f}"
G = gap[TGT]
W_own = -(G.sub(G.mean(axis=1), axis=0))
W_cl = pd.DataFrame(0.0, index=idx, columns=TGT)
for g_, mem in labI.groupby(labI):
    mem = list(mem.index)
    if len(mem) < 2: continue
    x = G[mem]; W_cl[mem] = -(x.sub(x.mean(axis=1), axis=0)).fillna(0)
W_pe = pd.DataFrame({j: -(gap[j] - gap[peers[j]].mean(axis=1)) for j in TGT if peers[j]})
W_peonly = pd.DataFrame({j: gap[peers[j]].mean(axis=1) - gap["XU100"] for j in TGT if peers[j]})  # eşlerin gap'i (kendi hariç) -> hedef gün-içi
for nm, Wt in [("kendi gap, 47 içinde piyasa-nötr", W_own), ("IS küme-göreli (BT3g)", W_cl), ("177-hisse 3 eş göreli", W_pe), ("yalnız eşlerin gap'i (kendi gap yok)", W_peonly)]:
    for c in [0, 8, 15]:
        P(f"(2) {nm:38s} maliyet {c:2d}: " + st(port(Wt, intra, c)))
# yıllık BT3g 8bps
p = port(W_cl, intra, 8); P("BT3g 8bps yıllık ort (bps): " + str((1e4 * p.groupby(p.index.year).mean()).round(1).to_dict()))
# (3) gecikmeli giriş — saatlik
H = hdata.SCR + "/data/h1"
E, X = {}, {}
for j in TGT:
    f = f"{H}/{j}.IS.parquet"
    if not os.path.exists(f): continue
    d = pd.read_parquet(f); d = d[~d.index.duplicated(keep="last")]; d = d[d.index.minute == 30]
    day = d.index.tz_convert(None).normalize()
    g_ = d.groupby(day)
    first_close = g_["c"].first(); first_start = g_.apply(lambda x: x.index[0].hour * 60 + x.index[0].minute)
    last_close = g_["c"].last(); nb = g_.size()
    ok = (first_start == 6 * 60 + 30) & (nb >= 6)
    E[j] = first_close.where(ok); X[j] = last_close.where(ok)
E = pd.DataFrame(E); X = pd.DataFrame(X)
dates = E.index.intersection(idx)
late = np.log(X.loc[dates] / E.loc[dates])  # ~10:30 -> son bar kapanışı
early = intra.loc[dates, late.columns]
P(f"\n(3) Gecikmeli giriş testi: {len(dates)} gün ({dates.min().date()}..{dates.max().date()}); corr(intra, late) medyan {np.nanmedian([early[c].corr(late[c]) for c in late]):.2f}")
for nm, Wt in [("kendi gap piyasa-nötr", W_own), ("IS küme-göreli (BT3g)", W_cl), ("177-eş göreli", W_pe)]:
    Wd = Wt.loc[dates]
    for lab, tg in [("açılıştan (iyimser)", early), ("~10:30'dan (gerçekçi)", late)]:
        for c in [0, 8]:
            pp = port(Wd.reindex(columns=late.columns), tg.reindex(columns=TGT), c)
            pp = pp[pp != 0]
            P(f"   {nm:24s} {lab:22s} maliyet {c}: {1e4*pp.mean():.1f} bps/gün, SR={pp.mean()/pp.std()*np.sqrt(252):.2f}, t={ll.nw_t(pp)[1]:.1f}, n={len(pp)}")
open(os.path.join(hdata.RES, "gapfade.txt"), "w").write("\n".join(out))
