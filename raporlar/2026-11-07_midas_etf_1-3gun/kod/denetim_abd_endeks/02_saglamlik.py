"""2) Sağlamlık: yıl yıl, 2020/2022 hariç, en iyi 5 hariç, permütasyonlar (rastgele gün / düşüş günü+VIX kademesi eşleşmeli /
dairesel kaydırma), parametre komşuluğu (IBS eşiği x tutuş x mod), takvim-zamanlı (örtüşmeli, yol bağımsız) sürüm,
IBS'in 'düşüş günü' üstüne katkısı."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dt, lib
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
rng = np.random.default_rng(20261107)
NREP = 2000
SY = ["SPY", "QQQ", "IWM", "DIA", "RSP", "MDY"]
D = {s: lib.load(s) for s in SY}
VIX = lib.vol_index("VIX")
OUT = dt.OUT

def mean_gross(d, sig, h, mode, ex=None):
    tr = dt.sim(d, sig, h, mode, ex)
    return (np.mean([r[3] for r in tr]) * 1e4 if tr else np.nan), len(tr)

CASES = [("S1", "SPY", "C1", None), ("S1", "SPY", "C0", None), ("S1", "QQQ", "C1", None), ("S1", "QQQ", "C0", None), ("S1", "QQQ", "O1", None),
         ("S3", "SPY", "C0", "up"), ("S3", "QQQ", "C0", "up")]
def sigf(name, d): return dt.s1_signal(d) if name == "S1" else dt.s3_signal(d)

# ---------- (1) yıl yıl ve dışlamalar ----------
print("=" * 20, "Yıl yıl net bp (2.500$) ve dışlamalar", "=" * 20)
YR = []
for name, s, m, exn in CASES:
    d = D[s]; ex = dt.up_close(d) if exn else None
    tr = dt.sim(d, sigf(name, d), 3, m, ex); cost = dt.cost_bp(s, 2500)
    df = dt.trades_df(d, tr, cost); df["yil"] = df.sig.dt.year
    y = df.groupby("yil")["net_bp"].agg(["count", "mean", "sum"]).round(0)
    def st(x): return f"n={len(x)} net={x.mean():.1f} t={dt.tstat(x.values):.2f}"
    top5 = df.sort_values("brut_bp", ascending=False).index[:5]
    rec = {"case": f"{name}-{s}-{m}", "tum": st(df.net_bp), "2020_haric": st(df[df.yil != 2020].net_bp),
           "2022_haric": st(df[df.yil != 2022].net_bp), "2020_2022_haric": st(df[~df.yil.isin([2020, 2022])].net_bp),
           "en_iyi5_haric": st(df.drop(top5).net_bp), "2024_sonrasi": st(df[df.yil >= 2024].net_bp),
           "yil_sum_net": y["sum"].to_dict()}
    YR.append(rec)
    for k, v in rec.items(): print(f"  {k}: {v}")
pd.DataFrame(YR).to_csv(os.path.join(OUT, "yil_dislama.csv"), index=False)

# ---------- (2) permütasyonlar ----------
print("=" * 20, f"Permütasyonlar ({NREP} tekrar; istatistik: ortalama brüt bp, aynı çakışmasız simülasyon)", "=" * 20)
PM = []
for name, s, m, exn in CASES:
    d = D[s]; ex = dt.up_close(d) if exn else None; n = len(d)
    sg = sigf(name, d); sg[:dt.WARM] = False
    obs, ntr = mean_gross(d, sg, 3, m, ex)
    k = int(sg.sum())
    c = d["c"].values; down = np.r_[False, c[1:] < c[:-1]]
    vx = VIX.reindex(d.index).ffill().values
    q = pd.qcut(pd.Series(vx[dt.WARM:]), 5, labels=False).values
    qq = np.full(n, -1); qq[dt.WARM:] = q
    elig = np.arange(dt.WARM, n - 5)
    res = {"rastgele_gun": [], "dusus_gunu_VIXkademe": [], "dairesel_kaydirma": []}
    sig_idx = np.where(sg)[0]
    strata = {}
    for i in sig_idx:
        strata.setdefault((down[i], qq[i]), []).append(i)
    pools = {key: elig[(down[elig] == key[0]) & (qq[elig] == key[1])] for key in strata}
    for r in range(NREP):
        z = np.zeros(n, bool); z[rng.choice(elig, k, replace=False)] = True
        res["rastgele_gun"].append(mean_gross(d, z, 3, m, ex)[0])
        z = np.zeros(n, bool)
        for key, lst in strata.items():
            z[rng.choice(pools[key], len(lst), replace=len(lst) > len(pools[key]))] = True
        res["dusus_gunu_VIXkademe"].append(mean_gross(d, z, 3, m, ex)[0])
        sh = rng.integers(250, n - 250)
        z = np.roll(sg, sh); z[:dt.WARM] = False
        res["dairesel_kaydirma"].append(mean_gross(d, z, 3, m, ex)[0])
    rec = {"case": f"{name}-{s}-{m}", "n_islem": ntr, "gozlenen_brut_bp": round(obs, 1)}
    for kname, v in res.items():
        v = np.array(v); rec[kname + "_ort"] = round(np.nanmean(v), 1); rec[kname + "_p"] = round((np.sum(v >= obs) + 1) / (len(v) + 1), 4)
    PM.append(rec); print(rec)
pm = pd.DataFrame(PM); pm.to_csv(os.path.join(OUT, "permutasyon.csv"), index=False)

# ---------- (2b) aile tutarlılığı için ortak dairesel kaydırma (6 çekirdek aynı kaydırma) ----------
print("=" * 20, "Aile ortak dairesel kaydırma: 6 çekirdek ETF'in C1 h3 ortalama net bp'si", "=" * 20)
for m in ("C1", "C0"):
    sigs = {s: dt.s1_signal(D[s]) for s in SY}
    def fam_stat(shift):
        vals = []
        for s in SY:
            z = np.roll(sigs[s], shift) if shift else sigs[s].copy()
            z[:dt.WARM] = False
            g, _ = mean_gross(D[s], z, 3, m); vals.append(g - dt.cost_bp(s, 2500))
        return np.mean(vals), np.sum(np.array(vals) > 0)
    obs, npos = fam_stat(0)
    nn = min(len(D[s]) for s in SY)
    null = [fam_stat(int(rng.integers(250, nn - 250))) for _ in range(1000)]
    nm = np.array([a for a, _ in null]); npz = np.array([b for _, b in null])
    print(f"  {m}: gözlenen ort. net {obs:.1f} bp ({npos}/6 pozitif); null ort {nm.mean():.1f}; p(ort)={(np.sum(nm >= obs) + 1) / 1001:.4f}; "
          f"null'da 6/6 pozitif olasılığı {(npz == 6).mean():.3f}")

# ---------- (3) parametre komşuluğu ----------
print("=" * 20, "Parametre komşuluğu (IBS eşiği x tutuş x mod; düşüş şartı açık); net bp / t  [IS | OOS]", "=" * 20)
NB = []
for s in ("SPY", "QQQ", "IWM"):
    d = D[s]; cost = dt.cost_bp(s, 2500)
    for thr in (0.05, 0.075, 0.10, 0.125, 0.15, 0.20):
        for h in (1, 2, 3, 4, 5):
            for m in ("C0", "O1", "C1"):
                st = dt.summarize(d, dt.sim(d, dt.s1_signal(d, thr), h, m), cost)
                NB.append({"sym": s, "thr": thr, "h": h, "mode": m, **{k: st[k] for k in ("n", "net_bp", "t", "is_net_bp", "oos_net_bp", "yil_poz")}})
nb = pd.DataFrame(NB); nb.to_csv(os.path.join(OUT, "komsu_parametre.csv"), index=False)
for s in ("SPY", "QQQ", "IWM"):
    x = nb[nb.sym == s]
    print(s, "net bp (satır: eşik; sütun: mod-h)")
    print(x.pivot_table(index="thr", columns=["mode", "h"], values="net_bp").round(0).to_string())
    print(s, "t")
    print(x.pivot_table(index="thr", columns=["mode", "h"], values="t").round(1).to_string())
    g = x[(x.h.isin([2, 3, 4])) & (x.thr.between(0.05, 0.20))]
    print(f"  {s}: eşik 0,05-0,20 x h 2-4 x 3 mod ({len(g)} hücre): medyan net {g.net_bp.median():.1f}, t>=2 oranı {(g.t >= 2).mean():.2f}, "
          f"IS>0&OOS>0 oranı {((g.is_net_bp > 0) & (g.oos_net_bp > 0)).mean():.2f}")

# ---------- (4) takvim zamanlı, örtüşmeli (yol bağımsız) sürüm ----------
print("=" * 20, "Takvim-zamanlı örtüşmeli sürüm: her sinyal kendi penceresinde; günlük portföy getirisi", "=" * 20)
CT = []
for s in SY:
    d = D[s]; c = d["c"].values; o = d["o"].values; n = len(c)
    r = np.r_[np.nan, c[1:] / c[:-1] - 1]
    sg = dt.s1_signal(d); sg[:dt.WARM] = False
    for m, (a, b) in (("C0", (1, 3)), ("C1", (2, 4)), ("C2", (3, 5))):
        # gün j getirisi, sinyal i için a<=j-i<=b ise portföyde (eşit ağırlıklı kohortlar)
        act = np.zeros(n)
        for i in np.where(sg)[0]:
            act[i + a:min(n, i + b + 1)] += 1
        held = act > 0
        x = r[held]; u = r[dt.WARM:][~np.isnan(r[dt.WARM:])]
        # her işlem 3 gün; ortalama günlük getiri x 3 = işlem başına brüt yaklaşık
        CT.append({"sym": s, "mode": m, "gun": int(held.sum()), "gunluk_bp": x.mean() * 1e4, "t_gunluk": dt.tstat(x),
                   "kosulsuz_gunluk_bp": u.mean() * 1e4, "islem_basi_brut_yaklasik_bp": 3 * x.mean() * 1e4,
                   "is_gunluk_bp": r[held & (d.index <= dt.IS_END)].mean() * 1e4, "oos_gunluk_bp": r[held & (d.index > dt.IS_END)].mean() * 1e4})
ct = pd.DataFrame(CT); ct.to_csv(os.path.join(OUT, "takvim_zamanli.csv"), index=False)
print(ct.round(2).to_string(index=False))

# ---------- (5) IBS'in katkısı: aynı rejimde 'düşüş günü ama IBS>=0.10' ile karşılaştırma ----------
print("=" * 20, "IBS katkısı: düşüş günü & IBS<0.10 vs düşüş günü & IBS>=0.30 (C1 h3, 2.500$ net)", "=" * 20)
for s in ("SPY", "QQQ", "IWM"):
    d = D[s]; cost = dt.cost_bp(s, 2500); c = d["c"].values; dn = np.r_[False, c[1:] < c[:-1]]
    ib = np.nan_to_num(dt.my_ibs(d), nan=0.5)
    vx = VIX.reindex(d.index).ffill().values
    for lab, z in (("düşüş & IBS<0.10", dn & (ib < 0.1)), ("düşüş & IBS>=0.30", dn & (ib >= 0.3)), ("tüm düşüş günleri", dn),
                   ("düşüş & VIX>=20", dn & (vx >= 20)), ("düşüş & IBS<0.10 & VIX>=20", dn & (ib < 0.1) & (vx >= 20)),
                   ("düşüş & IBS>=0.30 & VIX>=20", dn & (ib >= 0.3) & (vx >= 20)), ("düşüş & IBS<0.10 & VIX<20", dn & (ib < 0.1) & (vx < 20))):
        for m in ("C1", "C0"):
            st = dt.summarize(d, dt.sim(d, z, 3, m), cost)
            print(f"  {s} {m} {lab:30s} n={st['n']:4d} net={st['net_bp']:6.1f} t={st['t']:5.2f} IS={st['is_net_bp']:6.1f} OOS={st['oos_net_bp']:6.1f}")
