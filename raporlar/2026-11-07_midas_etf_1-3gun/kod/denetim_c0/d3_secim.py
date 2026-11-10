"""Görev 3b: seçim düzeltmesi. 48 öncü x 4 tip x 3 tutuş = 576 kombinasyon; istatistik = hedefler arası medyan t.
Null: olay günleri rastgeleleştirilir, olay (işlem) sayısı korunur.
  A: dairesel kaydırma, TÜM öncüler/hedefler için AYNI ofset (öncüler arası ve hedefler arası bağımlılık korunur)
  B: dairesel kaydırma, her öncüye BAĞIMSIZ ofset (aynı öncünün tipleri/tutuşları/hedefleri ortak) -> daha muhafazakâr
  C: rastgele günler (kümelenme bozulur), her (öncü,tip) için ortak gün havuzu (hedefler arası aynı günler)
Her permütasyonda 576 kombinasyonun medyan t'si ve maksimumu hesaplanır."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *

P = int(sys.argv[1]) if len(sys.argv) > 1 else 500
KINDS = ["L_UP", "L_DN", "GERIDE", "ONDE"]
t0 = time.time()
spy = px("SPY").index
X = leaders(spy)
LEAD = list(X.columns); assert len(LEAD) == 48
combos = [(L, k, h) for L in LEAD for k in KINDS for h in (1, 2, 3)]
cix = {c: i for i, c in enumerate(combos)}
TG = targets()
rng = np.random.default_rng(7)
offA = rng.integers(126, 2434 - 126, size=P)                  # takvim günü ofseti
offB = rng.integers(126, 2434 - 126, size=(len(LEAD), P))
uC = rng.random((len(LEAD) * 4, 260, P)).astype(np.float32)

obs = np.full((len(combos), len(TG)), np.nan, np.float32)
nul = {v: np.full((len(combos), len(TG), P), np.nan, np.float32) for v in "ABC"}

def tvec(G):   # G: (n_e, P) net getiriler -> t (P,)
    n = G.shape[0]; m = G.mean(0); s = G.std(0, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        return m / (s / np.sqrt(n))

for ti, T in enumerate(TG):
    sg, c, df = signals_for(T, X, kinds=tuple(KINDS))
    n = len(c); cost = my_cost(df) / 1e4
    for (L, k), sig in sg.items():
        if sig.sum() < 30: continue
        li = LEAD.index(L); lk = li * 4 + KINDS.index(k)
        for h in (1, 2, 3):
            ent, g = sim_greedy(sig, c, h)
            if len(ent) < 30: continue
            ci = cix[(L, k, h)]
            net = g - cost
            obs[ci, ti] = tstat(net)
            fr = c[h:] / c[:-h] - 1 - cost          # fr[i] = net getiri, giriş i
            m = n - h - 80                          # bölge: [80, n-h-1]
            base = ent - 80
            posA = 80 + (base[:, None] + offA[None, :]) % m
            nul["A"][ci, ti] = tvec(fr[posA])
            posB = 80 + (base[:, None] + offB[li][None, :]) % m
            nul["B"][ci, ti] = tvec(fr[posB])
            u = uC[lk, :len(ent), :]                # (n_e, P)
            posC = 80 + np.floor(u * m).astype(int)
            nul["C"][ci, ti] = tvec(fr[posC])
    if ti % 20 == 0: print(ti, T, round(time.time() - t0, 1), flush=True)

OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "d3_null.npz")   # ~1,1 GB: depo dışına yazın
np.savez_compressed(OUT, obs=obs, A=nul["A"], B=nul["B"], C=nul["C"],
                    combos=np.array(["|".join(map(str, c)) for c in combos]), targets=np.array(TG))
print("bitti", round(time.time() - t0, 1))
