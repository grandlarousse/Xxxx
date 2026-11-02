"""Adım 5: Backtestler (yalnız VİOP pay vadelisi olan 47 hedef işlem görür; liderler 177 hisseden sinyal kaynağı olabilir).
BT1  IS'de seçilen lider sepeti (lider cc_{t-1}) -> hedef gün-içi_t (açılışta gir, kapanışta çık).
BT1r Küme-eşi (IS artık korelasyonuna göre en yakın 3 eş, 177 hisseden) rölatif getirisi (eş_{t-1} - kendi_{t-1}) -> hedef gün-içi_t.
BT2  Çift spread (log oran) ortalamaya dönüş: z60>2 gir (ertesi açılış), |z|<0,5 / 20 gün çık. Engle-Granger eşbütünleşme p (IS/OOS). DÜŞÜK güven.
BT3  Küme içi kısa vadeli dönüş: w_j = -(r_j,t-1 - küme ort_t-1), Σ|w|=1 -> gün-içi_t. BT3g: gap_t sapmasıyla (açılışta bilinir) -> gün-içi_t.
BT4  5 günlük küme momentumu: küme ort. (t-5..t-1) - XU100 sıralaması; üst 2 küme al / alt 2 küme sat; (a) gün-içi_t günlük, (b) 5 gün tut (açılış t -> kapanış t+4).
Maliyet: birim brüt pozisyon başına gidiş-dönüş 8 ve 15 bps. IS 2014–2020, OOS 2021–2026.
Çıktı: res/bt.txt, res/bt_summary.csv
"""
import sys, os, itertools, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata
sys.path.insert(0, hdata.SCR + "/code"); import ll
from statsmodels.tsa.stattools import coint
D = hdata.load(); cc, gap, intra = D["cc"], D["gap"], D["intra"]
TGT = hdata.VIOP; idx = cc.index; SPLIT = pd.Timestamp(hdata.SPLIT)
LEAD = [c for c in cc.columns if c not in hdata.IDX]
out = []; summ = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)

def stats_pnl(pnl, act=None, label="", cost=None, ppy=252):
    """pnl: günlük seri (portföy). act: aktif gün bool."""
    res = {}
    for nm, m in [("IS", pnl.index < SPLIT), ("OOS", pnl.index >= SPLIT), ("ALL", np.ones(len(pnl), bool))]:
        p = pnl[m]; a = act[m] if act is not None else (p != 0)
        if a.sum() < 20: res[nm] = {"n": int(a.sum())}; continue
        pa = p[a]; mm, t, _ = ll.nw_t(pa)
        sh = p.mean() / p.std() * np.sqrt(ppy) if p.std() > 0 else np.nan
        res[nm] = {"n": int(a.sum()), "mean_bps": 1e4 * pa.mean(), "t": t, "sharpe": sh, "ann_pct": 100 * p.mean() * ppy, "hit": float((pa > 0).mean())}
    yr = (1e4 * pnl.groupby(pnl.index.year).mean()).round(1)
    return res, yr

def show(label, pnl, act=None, cost=None, ppy=252):
    res, yr = stats_pnl(pnl, act, ppy=ppy)
    s = f"{label:58s} " + " | ".join(f"{k}: n={v.get('n')} {v.get('mean_bps', np.nan):6.1f}bps t={v.get('t', np.nan):5.2f} SR={v.get('sharpe', np.nan):5.2f}" for k, v in res.items())
    P(s)
    summ.append({"strategy": label, **{f"{k}_{m}": v.get(m) for k, v in res.items() for m in ["n", "mean_bps", "t", "sharpe", "hit"]},
                 "years_pos_share": float((yr > 0).mean()), "by_year_bps": yr.to_dict()})
    return res, yr

# ---------- BT1: IS-seçimli lider sepeti -> gün-içi ----------
S = pd.read_parquet(os.path.join(hdata.RES, "scan_long.parquet"))
for c in ["target", "leader", "dep", "lag", "period"]: S[c] = S[c].astype(str)
S = S[S.target != S.leader]
sdIS = cc[cc.index < SPLIT].std()
P("=== BT1: IS (2014–2020) seçimli lider sepeti (|t_IS|>=3, en çok 5) -> hedef gün-içi_t ===")
for seldep in ["intra", "cc"]:
    I = S[(S.period == "IS") & (S.dep == seldep) & (S.lag == "1")]
    pn = {c: {} for c in [0, 8, 15]}; nsel = {}
    for j in TGT:
        x = I[I.target == j].copy(); x["a"] = x.t.abs(); x = x[x.a >= 3].nlargest(5, "a")
        nsel[j] = list(zip(x.leader, x.t.round(1)))
        if not len(x): continue
        sig = sum(np.sign(t) * cc[l].shift(1) / sdIS[l] for l, t in zip(x.leader, x.t))
        for c in [0, 8, 15]:
            _, p = ll.backtest(sig, intra[j], cost_bps=c); pn[c][j] = p
    ntr = sum(1 for v in nsel.values() if v)
    P(f"seçim dep={seldep}: işlem gören hedef {ntr}/47; örnek seçimler: " + "; ".join(f"{j}<-{v[:3]}" for j, v in list(nsel.items()) if v)[:900])
    for c in [0, 8, 15]:
        if not pn[c]: continue
        PP = pd.DataFrame(pn[c]).reindex(idx)
        port = PP.mean(axis=1, skipna=True).fillna(0)
        show(f"BT1[{seldep}] portföy (aktif hedef ort.) maliyet {c}", port)
    # tek tek OOS
    PP = pd.DataFrame(pn[8]).reindex(idx); o = PP[PP.index >= SPLIT]
    srs = (o.mean() / o.std() * np.sqrt(252)).sort_values()
    P(f"  tek hedef OOS SR (8bps): medyan {srs.median():.2f}, >0 olan {int((srs>0).sum())}/{len(srs)}; en iyi 5: {srs.tail(5).round(2).to_dict()}")

# ---------- BT1r: küme-eşi rölatif getirisi -> gün-içi ----------
P("\n=== BT1r: IS artık korelasyonuna göre en yakın 3 eş (177 hisse) rölatif getirisi (eş_{t-1} - kendi_{t-1}) -> gün-içi_t ===")
ccIS = cc[cc.index < SPLIT]; m = ccIS["XU100"]
def rs(s):
    d = pd.concat([s, m], axis=1).dropna(); b = np.cov(d.iloc[:, 0], d.iloc[:, 1])[0, 1] / d.iloc[:, 1].var() if len(d) > 100 else np.nan
    return s - b * m
RIS = pd.DataFrame({c: rs(ccIS[c]) for c in LEAD}); CIS = RIS.corr(min_periods=250)
peers = {j: list(CIS[j].drop(j).dropna().sort_values(ascending=False).head(3).index) for j in TGT if j in CIS and CIS[j].notna().sum() > 3}
P("eşler: " + "; ".join(f"{j}:{','.join(v)}" for j, v in peers.items())[:1500])
rel = {}
for j, pr in peers.items():
    rel[j] = cc[pr].mean(axis=1).shift(1) - cc[j].shift(1)
REL = pd.DataFrame(rel)
# yön: IS havuzlanmış korelasyon
pool = pd.concat([pd.DataFrame({"s": REL[j], "y": intra[j]}) for j in REL], axis=0).dropna()
pool_is = pool[pool.index < SPLIT]; pool_oos = pool[pool.index >= SPLIT]
P(f"havuz corr(rel_{{t-1}}, intra_t): IS {pool_is.s.corr(pool_is.y):.4f} (n={len(pool_is)}), OOS {pool_oos.s.corr(pool_oos.y):.4f}")
sgn = np.sign(pool_is.s.corr(pool_is.y))
for c in [0, 8, 15]:
    pn = {}
    for j in REL:
        _, p = ll.backtest(sgn * REL[j], intra[j], cost_bps=c); pn[j] = p
    show(f"BT1r yakınsama(işaret IS={'+' if sgn>0 else '-'}) maliyet {c}", pd.DataFrame(pn).reindex(idx).mean(axis=1).fillna(0))
    pn = {}
    for j in REL:
        _, p = ll.backtest(sgn * REL[j], intra[j], cost_bps=c, mode="z", thr=1.5); pn[j] = p
    show(f"BT1r z>1,5 filtresi maliyet {c}", pd.DataFrame(pn).reindex(idx).mean(axis=1).fillna(0))

# ---------- BT2: çift spread ortalamaya dönüş ----------
P("\n=== BT2: çift spread (log oran) ortalamaya dönüş, z60, giriş |z|>2 (ertesi açılış), çıkış |z|<0,5 veya 20 gün ===")
PAIRS = [("AKBNK", "GARAN"), ("AKBNK", "YKBNK"), ("GARAN", "YKBNK"), ("ISCTR", "YKBNK"), ("AKBNK", "ISCTR"), ("GARAN", "ISCTR"), ("HALKB", "VAKBN"),
         ("THYAO", "PGSUS"), ("PGSUS", "TAVHL"), ("THYAO", "TAVHL"), ("EREGL", "KRDMD"), ("FROTO", "TOASO"), ("CIMSA", "OYAKC"), ("MGROS", "SOKM"),
         ("BIMAS", "MGROS"), ("BIMAS", "SOKM"), ("TCELL", "TTKOM"), ("KCHOL", "SAHOL"), ("TRALT", "TRMET"), ("TUPRS", "PETKM"), ("HEKTS", "SASA"),
         ("GUBRF", "HEKTS"), ("AKSEN", "ODAS"), ("TKFEN", "ENKAI"), ("SAHOL", "AKBNK"), ("ISCTR", "VAKBN"), ("ARCLK", "VESTL")]
lp = cc.fillna(0).cumsum()
def pair_bt(a, b, cost, zin=2.0, zout=0.5, maxh=20, w=60):
    s = lp[a] - lp[b]
    ok = cc[a].notna() & cc[b].notna()
    mu = s.rolling(w, min_periods=w).mean(); sd = s.rolling(w, min_periods=w).std(); z = (s - mu) / sd
    ra_i, rb_i, ra_c, rb_c = intra[a].fillna(0).values, intra[b].fillna(0).values, cc[a].fillna(0).values, cc[b].fillna(0).values
    zv = z.values; pos = 0; h = 0; pnl = np.zeros(len(s)); act = np.zeros(len(s), bool); trades = []; cur = 0.0
    first = (cc[a].first_valid_index(), cc[b].first_valid_index()); st = max(first)
    for t in range(1, len(s)):
        if idx[t] < st: continue
        zprev = zv[t - 1]
        if pos != 0:
            # tut: bugün cc getirisi
            r = pos * (ra_c[t] - rb_c[t]); pnl[t] += r; cur += r; act[t] = True; h += 1
            if (np.isfinite(zv[t]) and abs(zv[t]) < zout) or h >= maxh or (np.isfinite(zv[t]) and np.sign(zv[t]) == pos):
                # çıkış kapanışta (z_t kapanışta bilinir -> kapanış seansında çık varsayımı; iyimser), maliyet
                pnl[t] -= cost / 1e4; cur -= cost / 1e4; trades.append((idx[t], cur)); pos = 0; h = 0; cur = 0.0
        else:
            if np.isfinite(zprev) and abs(zprev) > zin:
                pos = -int(np.sign(zprev)); h = 1
                r = pos * (ra_i[t] - rb_i[t]) - cost / 1e4; pnl[t] += r; cur = r; act[t] = True
    return pd.Series(pnl, index=idx), pd.Series(act, index=idx), trades, z

bt2 = []; P2 = {}
for a, b in PAIRS:
    la = np.log(ll.daily(a + ".IS")); lb = np.log(ll.daily(b + ".IS"))
    d = pd.concat([la, lb], axis=1).dropna(); d = d[d.index >= pd.Timestamp("2014-01-01")]
    dI = d[d.index < SPLIT]; dO = d[d.index >= SPLIT]
    pI = coint(dI.iloc[:, 0], dI.iloc[:, 1])[1] if len(dI) > 250 else np.nan; pO = coint(dO.iloc[:, 0], dO.iloc[:, 1])[1] if len(dO) > 250 else np.nan
    sp = (lp[a] - lp[b]).diff().dropna(); spl = (lp[a] - lp[b])
    x = pd.concat([spl.shift(1), spl.diff()], axis=1).dropna(); hl = -np.log(2) / np.polyfit(x.iloc[:, 0], x.iloc[:, 1], 1)[0] if len(x) else np.nan
    row = {"pair": f"{a}-{b}", "coint_p_IS": pI, "coint_p_OOS": pO}
    for c in [0, 8, 15]:
        pnl, act, tr, z = pair_bt(a, b, c)
        res, yr = stats_pnl(pnl, act)
        tI = [x for x in tr if x[0] < SPLIT]; tO = [x for x in tr if x[0] >= SPLIT]
        row[f"IS_tr_{c}"] = len(tI); row[f"OOS_tr_{c}"] = len(tO)
        row[f"IS_bps_trade_{c}"] = 1e4 * np.mean([x[1] for x in tI]) if tI else np.nan
        row[f"OOS_bps_trade_{c}"] = 1e4 * np.mean([x[1] for x in tO]) if tO else np.nan
        row[f"OOS_hit_{c}"] = np.mean([x[1] > 0 for x in tO]) if tO else np.nan
        row[f"IS_SR_{c}"] = res["IS"].get("sharpe"); row[f"OOS_SR_{c}"] = res["OOS"].get("sharpe")
        if c == 8: P8 = pnl
    bt2.append(row)
    P2[f"{a}-{b}"] = P8
B2 = pd.DataFrame(bt2); B2.to_csv(os.path.join(hdata.RES, "bt2_pairs.csv"), index=False)
P(B2[["pair", "coint_p_IS", "coint_p_OOS", "IS_tr_8", "IS_bps_trade_8", "IS_SR_8", "OOS_tr_8", "OOS_bps_trade_8", "OOS_hit_8", "OOS_SR_8", "OOS_bps_trade_15", "OOS_SR_15"]].round(3).to_string(index=False))
port2 = pd.DataFrame(P2).mean(axis=1)
show("BT2 eşit ağırlıklı çift portföyü (27 çift) maliyet 8", port2)
selp = list(B2.loc[B2.IS_SR_8 > 0.3, "pair"])
P(f"IS SR(8bps)>0,3 ile seçilen çiftler ({len(selp)}): {selp}")
show("BT2 IS-seçimli çift portföyü (IS SR>0,3) maliyet 8", pd.DataFrame(P2)[selp].mean(axis=1))
hi = ["AKBNK-GARAN", "AKBNK-YKBNK", "GARAN-YKBNK", "ISCTR-YKBNK", "AKBNK-ISCTR", "GARAN-ISCTR", "HALKB-VAKBN", "ISCTR-VAKBN"]
show("BT2 yalnız banka çiftleri (8) maliyet 8", pd.DataFrame(P2)[hi].mean(axis=1))
P(f"Engle-Granger IS p<0,05 çift sayısı: {int((B2.coint_p_IS<0.05).sum())}/{len(B2)}; OOS p<0,05: {int((B2.coint_p_OOS<0.05).sum())}; ikisinde de: {int(((B2.coint_p_IS<0.05)&(B2.coint_p_OOS<0.05)).sum())}")

# ---------- BT3: küme içi kısa vadeli dönüş ----------
P("\n=== BT3: küme içi kısa vadeli dönüş (IS kümeleri, 47 VİOP) ===")
labI = pd.read_csv(os.path.join(hdata.RES, "clusters_is.csv"), index_col=0)["cl"]
labF = pd.read_csv(os.path.join(hdata.RES, "clusters_full.csv"), index_col=0)["cl"]
def cluster_rev(lab, sigdf, tgtdf, cost, minsz=2, sign=-1):
    cl = {g: list(m.index) for g, m in lab.groupby(lab) if len(m) >= minsz}
    Wt = pd.DataFrame(0.0, index=idx, columns=TGT)
    for g, mem in cl.items():
        x = sigdf[mem]; valid = x.notna() & tgtdf[mem].notna()
        x = x.where(valid); cnt = valid.sum(axis=1)
        dev = x.sub(x.mean(axis=1), axis=0); dev.loc[cnt < 2, :] = np.nan
        Wt[mem] = Wt[mem].add(sign * dev.fillna(0), fill_value=0)
    gross = Wt.abs().sum(axis=1); Wn = Wt.div(gross.replace(0, np.nan), axis=0).fillna(0)
    pnl = (Wn * tgtdf[TGT].fillna(0)).sum(axis=1) - cost / 1e4 * Wn.abs().sum(axis=1)
    return pnl, Wn
for c in [0, 8, 15]:
    pnl, _ = cluster_rev(labI, cc.shift(1), intra, c); show(f"BT3 dönüş (cc_t-1 sapması) -> gün-içi_t, IS kümeleri, maliyet {c}", pnl)
for c in [0, 8, 15]:
    pnl, _ = cluster_rev(labI, gap, intra, c); show(f"BT3g dönüş (gap_t sapması) -> gün-içi_t, IS kümeleri, maliyet {c}", pnl)
pnl, _ = cluster_rev(labF, cc.shift(1), intra, 8); show("BT3 (tam dönem kümeleri, bilgi amaçlı look-ahead) maliyet 8", pnl)
# 177 hisse eşleri ile: hedefin eş sepetinden sapması (BT1r'nin tersi) zaten BT1r'de; burada cc->cc (kapanışta işlem varsayımı, işlenemez üst sınır)
pnl, _ = cluster_rev(labI, cc.shift(1), cc, 0); show("BT3 üst sınır: cc_t-1 sapması -> cc_t (kapanış dolumu varsayımı, işlenemez) maliyet 0", pnl)
pnl, _ = cluster_rev(labI, cc.shift(1), gap, 0); show("BT3 ayrıştırma: cc_t-1 sapması -> gap_t (işlenemez) maliyet 0", pnl)

# ---------- BT4: 5 günlük küme momentumu ----------
P("\n=== BT4: 5 günlük küme momentumu (IS kümeleri, boyut>=2) ===")
cl = {g: list(m.index) for g, m in labI.groupby(labI) if len(m) >= 2}
CR = pd.DataFrame({g: cc[mem].mean(axis=1) for g, mem in cl.items()})
CI = pd.DataFrame({g: intra[mem].mean(axis=1) for g, mem in cl.items()})
CC5 = CR.rolling(5, min_periods=4).sum().sub(cc["XU100"].rolling(5, min_periods=4).sum(), axis=0)
sig = CC5.shift(1)  # t-5..t-1
rk = sig.rank(axis=1)
nC = sig.notna().sum(axis=1)
top = rk.ge(nC.values[:, None] - 1) & sig.notna(); bot = rk.le(2) & sig.notna()
Wc = (top.astype(float).div(top.sum(axis=1).replace(0, np.nan), axis=0) * 0.5 - bot.astype(float).div(bot.sum(axis=1).replace(0, np.nan), axis=0) * 0.5).fillna(0)
for sgn, nm in [(1, "momentum"), (-1, "dönüş")]:
    for c in [0, 8, 15]:
        pnl = sgn * (Wc * CI.fillna(0)).sum(axis=1) - c / 1e4 * Wc.abs().sum(axis=1)
        show(f"BT4a 5g küme {nm} -> gün-içi_t (günlük) maliyet {c}", pnl)
# 5 gün tutma, örtüşmesiz
fwd = (CI + CR.shift(-1).fillna(0) + CR.shift(-2).fillna(0) + CR.shift(-3).fillna(0) + CR.shift(-4).fillna(0))  # açılış t -> kapanış t+4
xu_f = 0
for sgn, nm in [(1, "momentum"), (-1, "dönüş")]:
    for c in [0, 8, 15]:
        pnl = sgn * (Wc * fwd.fillna(0)).sum(axis=1) - c / 1e4 * Wc.abs().sum(axis=1)
        pnl5 = pnl.iloc[::5]
        show(f"BT4b 5g küme {nm}, 5 gün tut (örtüşmesiz, işlem başına) maliyet {c}", pnl5, ppy=252/5)

pd.DataFrame(summ).to_csv(os.path.join(hdata.RES, "bt_summary.csv"), index=False)
open(os.path.join(hdata.RES, "bt.txt"), "w").write("\n".join(out))
