"""7) Kaçırılan risk/fırsat testleri: (a) SPY sinyali -> QQQ işlemi (bağımsız), (b) 'yeni sinyalde süreyi uzat' varyantı
(çakışma kuralının etkisi), (c) VIX<20 rejiminde 1.000$ maliyetle sonuç, (d) kriz kümelenmesi: ardışık işlemlerde en kötü seri."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dt, lib
D = {s: lib.load(s) for s in ("SPY", "QQQ", "TQQQ", "SPXL")}
VIX = lib.vol_index("VIX")

def sim_extend(d, sig, h, mode):
    """Pozisyondayken yeni sinyal gelirse çıkış tarihi yeni sinyale göre uzatılır (tek işlem)."""
    c = d["c"].values; n = len(c); sig = np.asarray(sig, bool).copy(); sig[:dt.WARM] = False
    off = 0 if mode == "C0" else 1
    out = []; i = 0
    while i < n:
        if not sig[i]: i += 1; continue
        e = i + off
        if e + h >= n: break
        x = e + h; j = i + 1
        while j <= x - off and j < n:   # çıkış kapanışından önce bilinen yeni sinyal
            if sig[j] and j + off + h < n: x = max(x, j + off + h)
            j += 1
        out.append((i, e, x, c[x] / c[e] - 1)); i = x if mode == "C0" else x
    return out

for s in ("SPY", "QQQ"):
    d = D[s]; cost = dt.cost_bp(s, 2500)
    for m in ("C0", "C1"):
        a = dt.summarize(d, dt.sim(d, dt.s1_signal(d), 3, m), cost); b = dt.summarize(d, sim_extend(d, dt.s1_signal(d), 3, m), cost)
        print(f"{s} {m}: katı kural n={a['n']} net={a['net_bp']:.1f} t={a['t']:.2f} | uzatmalı n={b['n']} net={b['net_bp']:.1f} t={b['t']:.2f} IS={b['is_net_bp']:.0f} OOS={b['oos_net_bp']:.0f}")

# (a) SPY sinyali -> QQQ / TQQQ işlemi
sp = pd.Series(dt.s1_signal(D["SPY"]), index=D["SPY"].index)
for inst in ("QQQ", "TQQQ", "SPXL"):
    d = D[inst]; z = sp.reindex(d.index).fillna(False).values
    for m in ("C0", "O1", "C1"):
        st = dt.summarize(d, dt.sim(d, z, 3, m), dt.cost_bp(inst, 2500))
        print(f"SPY sinyali -> {inst} {m}: n={st['n']} net={st['net_bp']:.1f} t={st['t']:.2f} IS={st['is_net_bp']:.0f} OOS={st['oos_net_bp']:.0f} en kötü={st['en_kotu_bp']:.0f}")

# (c) VIX rejimi x pozisyon büyüklüğü
for s in ("SPY", "QQQ"):
    d = D[s]; tr = dt.sim(d, dt.s1_signal(d), 3, "C1")
    v = VIX.reindex(d.index).ffill().values
    g = np.array([r[3] for r in tr]) * 1e4; vv = np.array([v[r[0]] for r in tr])
    for lab, msk in (("VIX<20", vv < 20), ("VIX>=20", vv >= 20)):
        print(f"{s} C1 {lab}: n={msk.sum()} brüt={g[msk].mean():.1f}  net 1.000$={g[msk].mean() - dt.cost_bp(s, 1000):.1f}  2.500$={g[msk].mean() - dt.cost_bp(s, 2500):.1f}  t_brüt={dt.tstat(g[msk]):.2f}")

# (d) kriz kümelenmesi: 60 takvim günü içindeki ardışık işlemlerin bileşik net getirisi, en kötü pencere
for s in ("SPY", "QQQ", "TQQQ"):
    base = "QQQ" if s in ("QQQ", "TQQQ") else "SPY"
    d = D[s]; z = pd.Series(dt.s1_signal(D[base]), index=D[base].index).reindex(d.index).fillna(False).values
    tdf = dt.trades_df(d, dt.sim(d, z, 3, "C1"), dt.cost_bp(s, 2500))
    worst = (0, None)
    for i in range(len(tdf)):
        w = tdf[(tdf.giris >= tdf.giris.iloc[i]) & (tdf.giris < tdf.giris.iloc[i] + pd.Timedelta(days=60))]
        r = np.prod(1 + w.net_bp / 1e4) - 1
        if r < worst[0]: worst = (r, (tdf.giris.iloc[i].date(), len(w)))
    print(f"{s} (sinyal {base}) C1: en kötü 60 günlük işlem kümesi bileşik {worst[0] * 100:.1f}% başlangıç/işlem sayısı {worst[1]}")
