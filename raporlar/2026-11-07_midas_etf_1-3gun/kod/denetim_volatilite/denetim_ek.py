"""Denetim ek testleri: vol-eşlemeli permütasyon, vekil sadakati ve 2010-2018 iddiası, SVXY getirisinin hisse betası ayrışması,
QQQ/QLD/TQQQ'ya aktarım (PTP'siz araç), kendi RSI2'si ile karşılaştırma. Çalıştırma: python3 -I kod/denetim_volatilite/denetim_ek.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "ajan_volatilite"))
import numpy as np, pandas as pd
import dlib, lib
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
rng = np.random.default_rng(7)

sv = lib.load("SVXY"); C = sv.c
rsi = dlib.wilder_rsi(C, 2); ma = dlib.sma(C, 200)
SIG = ((rsi < 10) & (C > ma)).fillna(False)
COST = dlib.cost("SVXY")
tr = dlib.sim(sv, SIG, 2, "C0", COST); obs = tr.net.mean() * 1e4
start = SIG[SIG].index[0]
vix = lib.vol_index("VIX").reindex(sv.index)

# --- A) Vol eşlemeli permütasyon: her sinyal gününe, VIX düzeyi ±%10 ve SMA200 üstü, aynı 2 günlük tutuş, sinyal olmayan rastgele gün ---
print("=== A) VIX düzeyi eşlemeli permütasyon (C0 h2 ve O1 h2) ===")
c = C.values; o = sv.o.values; idx = sv.index
elig = np.where((sv.index >= start) & (C > ma).values & (~SIG.values) & np.isfinite(vix.values))[0]
elig = elig[elig + 3 < len(sv)]
# ayrıca 2 günlük düşüşe eşleme: son 2 gün getirisi de benzer (±%30 göreli)
r2 = (C / C.shift(2) - 1).values
for mode in ("C0", "O1"):
    if mode == "C0": base = dlib.sim(sv, SIG, 2, "C0", COST)
    else: base = dlib.sim(sv, SIG, 2, "O1", COST)
    ob = base.net.mean() * 1e4
    sig_ix = [sv.index.get_loc(d) for d in base.sig]
    for match in ("VIX", "VIX+2g_dusus"):
        means = []
        for k in range(3000):
            gs = []
            for i in sig_ix:
                cand = elig[np.abs(vix.values[elig] / vix.values[i] - 1) < 0.10]
                if match == "VIX+2g_dusus":
                    cand = cand[(r2[cand] < 0) & (np.abs(r2[cand] / r2[i] - 1) < 0.5)] if r2[i] < 0 else cand
                if len(cand) == 0: continue
                j = rng.choice(cand)
                ep = c[j] if mode == "C0" else o[j + 1]
                gs.append(c[j + 2] / ep - 1)
            means.append(np.mean(gs) * 1e4 - COST)
        means = np.array(means)
        print(f"  {mode} h2 eşleme={match:<13} gözlenen {ob:6.1f}  rastgele ort {means.mean():6.1f}  p95 {np.percentile(means,95):6.1f}  p={(np.sum(means>=ob)+1)/(len(means)+1):.4f}")

# --- B) Vekil sadakati: aynı kural vekilde 2019-09+ gerçek SVXY ile örtüşüyor mu? ---
print("\n=== B) Vekil (-0,5x) 2019+ dönemde gerçek SVXY ile örtüşme ===")
import vlib
px = vlib.synth_proxy(-0.5)
pc = px.c
prsi = dlib.wilder_rsi(pc, 2); pma = dlib.sma(pc, 200)
PS = ((prsi < 10) & (pc > pma)).fillna(False)
ptr = dlib.sim(px, PS, 2, "C0", COST)
both = ptr[ptr.sig >= start]
print(f"  vekil sinyali 2019-07+ : n={len(both)} net={both.net.mean()*1e4:.1f} t={dlib.tstat(both.net):.2f} | gerçek SVXY n={len(tr)} net={obs:.1f}")
common = set(both.sig) & set(tr.sig)
print(f"  ortak sinyal günü: {len(common)} / vekil {len(both)} / gerçek {len(tr)}")
# Gerçek SVXY sinyal günlerinde vekil getirisi vs gerçek getiri
g_real = tr.set_index("sig").gross
g_px = pd.Series({d: pc.iloc[pc.index.get_loc(d) + 2] / pc.loc[d] - 1 for d in tr.sig if d in pc.index and pc.index.get_loc(d) + 2 < len(pc)})
j = pd.concat([g_real, g_px], axis=1, keys=["real", "proxy"]).dropna()
print(f"  gerçek sinyal günlerinde: gerçek brüt {j.real.mean()*1e4:.1f} bp, vekil brüt {j.proxy.mean()*1e4:.1f} bp, korelasyon {j.corr().iloc[0,1]:.3f}")
# Vekil alt dönemleri
for a, b in [("2010-01-01", "2014-12-31"), ("2015-01-01", "2018-12-31"), ("2019-01-01", "2021-12-31"), ("2022-01-01", "2026-12-31")]:
    q = ptr[(ptr.sig >= a) & (ptr.sig <= b)]
    print(f"  vekil {a[:4]}-{b[:4]}: n={len(q)} net={q.net.mean()*1e4:7.1f} t={dlib.tstat(q.net):5.2f}")
# vekil komşuluk 2010-2018
print("  vekil 2010-2018 komşuluk (C0 h2 net bp / n):")
for thr in (5, 10, 15):
    for m_ in (150, 200, 250):
        s = ((prsi < thr) & (pc > dlib.sma(pc, m_))).fillna(False)
        q = dlib.sim(px, s, 2, "C0", COST); q = q[q.sig < "2019-01-01"]
        print(f"    RSI<{thr} SMA{m_}: n={len(q)} net={q.net.mean()*1e4:6.1f} t={dlib.tstat(q.net):5.2f}")

# --- C) SVXY getirisinin hisse betası ayrışması (sinyal işlemlerinde) ---
print("\n=== C) SVXY işlem getirisi = a + b * QQQ (ve SPY) aynı pencere getirisi ===")
for es in ("SPY", "QQQ"):
    e = lib.load(es).c
    eg = np.array([e.loc[x] / e.loc[g] - 1 for g, x in zip(tr.giris, tr.cikis)])
    X = np.c_[np.ones(len(eg)), eg]; b = np.linalg.lstsq(X, tr.gross.values, rcond=None)[0]
    res = tr.gross.values - X @ b
    print(f"  {es}: beta={b[1]:.2f}, alfa(brüt)={b[0]*1e4:.1f} bp/işlem, artık t={dlib.tstat(res + b[0]):.2f}, {es} ort {eg.mean()*1e4:.1f} bp, R2={1-res.var()/tr.gross.var():.2f}")
# Tüm günlerde 2 günlük regresyon betasıyla 'hisse dışı' kısım
e = lib.load("SPY").c
r_sv = C.pct_change(); r_e = e.pct_change().reindex(C.index)
b_all = np.polyfit(r_e.dropna().loc[r_sv.dropna().index.intersection(r_e.dropna().index)], r_sv.loc[r_sv.dropna().index.intersection(r_e.dropna().index)], 1)[0]
print(f"  tüm günlerde SVXY~SPY günlük beta {b_all:.2f}")

# --- D) PTP'siz araçlar: SVXY sinyali -> QQQ/QLD/TQQQ/SPY/SSO; ayrıca kendi RSI2 sinyalleri ile karşılaştırma ---
print("\n=== D) SVXY sinyali vs aracın kendi RSI2<10&SMA200 sinyali (C0/O1 h2) ===")
rows = []
for sym in ["QQQ", "QLD", "TQQQ", "SPY", "SSO", "UPRO"]:
    d = lib.load(sym); cc = d.c
    own = ((dlib.wilder_rsi(cc, 2) < 10) & (cc > dlib.sma(cc, 200))).fillna(False)
    own[d.index < start] = False
    svs = SIG.reindex(d.index).fillna(False)
    for nm, s in [("SVXY_sinyali", svs), ("kendi_RSI2", own), ("SVXY_sinyali_VE_kendi_degil", svs & ~own)]:
        for mode in ("C0", "O1", "C1"):
            x = dlib.summ(dlib.sim(d, s, 2, mode, dlib.cost(sym)), f"{sym} {nm} {mode}")
            rows.append({k: x.get(k) for k in ["tag", "n", "brut_bp", "net_bp", "t", "is_net_bp", "is_t", "oos_net_bp", "oos_t", "win", "maxdd", "en_kotu_bp", "yil_pozitif"]})
D = pd.DataFrame(rows); print(D.round(2).to_string()); D.to_csv(os.path.join(dlib.OUT, "kacirilan_hisse_araci.csv"), index=False)
q = lib.load("QQQ"); ov = (SIG.reindex(q.index).fillna(False) & ((dlib.wilder_rsi(q.c, 2) < 10) & (q.c > dlib.sma(q.c, 200)))).sum()
print("  SVXY sinyal günlerinden QQQ kendi RSI2 sinyali ile çakışan:", int(ov), "/", int(SIG.sum()))
# QQQ C0 h2 SVXY sinyali: alt örnekler
qt = dlib.sim(q, SIG.reindex(q.index).fillna(False), 2, "C0", dlib.cost("QQQ"))
print("  QQQ (SVXY sinyali) C0 h2 yıl yıl ort net bp:", (qt.groupby(qt.sig.dt.year).net.mean() * 1e4).round(0).to_dict())
print("  en iyi 5 çıkarılınca:", round(qt.drop(qt.nlargest(5, 'net').index).net.mean() * 1e4, 1), "t", round(dlib.tstat(qt.drop(qt.nlargest(5, 'net').index).net), 2))
qo = dlib.sim(q, SIG.reindex(q.index).fillna(False), 2, "O1", dlib.cost("QQQ"))
print("  QQQ O1 h2 en iyi 5 çıkarılınca:", round(qo.drop(qo.nlargest(5, 'net').index).net.mean() * 1e4, 1), "t", round(dlib.tstat(qo.drop(qo.nlargest(5, 'net').index).net), 2))
