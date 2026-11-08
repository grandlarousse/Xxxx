"""DENETİM tahvil_doviz — kaçırılan fırsat/risk kısa testleri.
(1) TLT-IEF 'yetişme' (eğri göreli dönüş): resid_t = r_TLT(t) - beta60(t)*r_IEF(t); z = resid / sd60(resid) (t'ye kadar).
    Önceden belirlenmiş tek eşik |z|>=1.5 (tarama yok). z<=-1.5 -> TLT/TMF long; z>=+1.5 -> TMV long. C0/O1/C1, h=3. Kendi simülasyonum.
(2) S1'in 'kapanışa bağımlılığı': A-3 kapanış -> A-2 açılış (gece/hafta sonu) ve A-2 açılış -> A-1 kapanış parçaları.
Çalıştır: python3 -I kod/denetim_tahvil_doviz/d05_kacirilan.py
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd
import lib
from d01_s1_yeniden import IDX, A10, ROOT, OUT, tstat, cost, apos
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "ajan_tahvil_doviz"))
import td

def px(sym): return td.load(sym).reindex(IDX)

def run(sym, sig, h=3, mode="C0", pos=2500.0):
    d = px(sym); o = d["o"].values; c = d["c"].values; s = sig.values; n = len(IDX); out = []; i = 0
    while i < n:
        if not s[i]: i += 1; continue
        if mode == "C0": e, x, ep = i, i + h, c[i]
        elif mode == "O1": e, x = i + 1, i + h; ep = o[e] if e < n else np.nan
        else: e, x = i + 1, i + 1 + h; ep = c[e] if e < n else np.nan
        if x >= n: break
        out.append((IDX[i], c[x] / ep - 1)); i = x   # çakışmasız: sonraki sinyal en erken çıkış günü
    t = pd.DataFrame(out, columns=["sig_date", "gross"])
    net = t.gross - cost(sym, pos) / 1e4
    is_ = t.sig_date <= pd.Timestamp("2021-12-31")
    yrs = net.groupby(t.sig_date.dt.year).sum()
    return dict(sym=sym, mode=mode, n=len(t), gross_bp=t.gross.mean() * 1e4, net_bp=net.mean() * 1e4, t=tstat(net),
                is_net=net[is_].mean() * 1e4, oos_net=net[~is_].mean() * 1e4, yil_poz=(yrs > 0).mean())

rT = np.log(px("TLT")["c"]).diff(); rI = np.log(px("IEF")["c"]).diff()
beta = rT.rolling(60).cov(rI) / rI.rolling(60).var()
res = rT - beta * rI
z = res / res.rolling(60).std()
rows = []
for lab, sig, syms in (("z<=-1.5 (TLT IEF'e göre geride) -> long", z <= -1.5, ("TLT", "TMF")), ("z>=+1.5 -> TMV long", z >= 1.5, ("TMV", "TBT"))):
    sig = sig.fillna(False); sig.iloc[:80] = False
    for sym in syms:
        for m in ("C0", "O1", "C1"):
            r = run(sym, sig, 3, m); r["kural"] = lab; rows.append(r)
R = pd.DataFrame(rows)
print("=== (1) TLT-IEF yetişme kuralı (h=3, 2.500$) ===")
print(R[["kural", "sym", "mode", "n", "gross_bp", "net_bp", "t", "is_net", "oos_net", "yil_poz"]].round(2).to_string(index=False))
R.to_csv(os.path.join(OUT, "d05_tlt_ief_yetisme.csv"), index=False)

# (2) S1 parçaları (TMV): gece/hafta sonu vs seans
d = px("TMV"); o = d["o"].values; c = d["c"].values
P, _ = apos(A10); P = P[P >= 3]
gap = o[P - 2] / c[P - 3] - 1; rest = c[P - 1] / o[P - 2] - 1; intra3 = c[P - 3] / o[P - 3] - 1
isx = IDX[P - 3] <= pd.Timestamp("2021-12-31")
for nm, x in (("A-3 seansı (açılış->kapanış)", intra3), ("A-3 kapanış -> A-2 açılış (gece/hafta sonu)", gap), ("A-2 açılış -> A-1 kapanış", rest)):
    print(f"TMV {nm:42s}: brüt {np.nanmean(x)*1e4:6.1f} bp (t {tstat(x):5.2f}) | IS {np.nanmean(x[isx])*1e4:6.1f} | OOS {np.nanmean(x[~isx])*1e4:6.1f} (t {tstat(x[~isx]):.2f})")
