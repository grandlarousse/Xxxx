"""Denetim S1 ek: kış/yaz etkileşimi anlamlı mı (post-hoc ayrımın sınaması), ay heterojenliği, oynaklık ölçekli prim.
Çalıştırma: python3 -I kod/denetim_enerji_tarim/d_s1_ek.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats as sst
import dsim as D, lib
from d_s1_eia_kold import eve_signal, WIN

k = lib.load("KOLD")
tr = D.sim(k, eve_signal(k), 1, "C0")
tr["kis"] = tr["cikis"].dt.month.isin(WIN)
a = tr.loc[tr.kis, "brut"]; b = tr.loc[~tr.kis, "brut"]
t, p = sst.ttest_ind(a, b, equal_var=False)
print(f"Kış (Kas-Mar) brüt {a.mean()*1e4:.1f} bp (n={len(a)}) vs yaz {b.mean()*1e4:.1f} bp (n={len(b)}): fark t={t:.2f} p(iki yönlü)={p:.3f}")
# ay heterojenliği (Kruskal + ANOVA)
g = [x["brut"].to_numpy() for _, x in tr.groupby(tr["cikis"].dt.month)]
print("Aylar arası fark: ANOVA p=%.3f, Kruskal p=%.3f" % (sst.f_oneway(*g).pvalue, sst.kruskal(*g).pvalue))
# |hareket| ve ort/varyans (risk primi ölçekleme)
print("Rapor günü |r| (bp): kış %.0f, yaz %.0f; ort/var: kış %.2f, yaz %.2f" % (a.abs().mean() * 1e4, b.abs().mean() * 1e4, a.mean() / a.var(), b.mean() / b.var()))
# IS'te seçilseydi: IS içinde kış/yaz farkı ve OOS'ta kış/yaz
for nm, m in (("IS", tr["sig"] <= D.IS_END), ("OOS", tr["sig"] > D.IS_END)):
    x = tr[m]
    aa = x.loc[x.kis, "brut"]; bb = x.loc[~x.kis, "brut"]
    print(f"  {nm}: kış {aa.mean()*1e4:.1f} (t {D.t_of(aa):.2f}, n {len(aa)}) | yaz {bb.mean()*1e4:.1f} (t {D.t_of(bb):.2f}, n {len(bb)})")
# Medyan ve işaret testi
print("Kış işlemleri medyan brüt %.1f bp; işaret testi p=%.3f" % (a.median() * 1e4, sst.binomtest(int((a > 0).sum()), len(a), 0.5, alternative="greater").pvalue))
