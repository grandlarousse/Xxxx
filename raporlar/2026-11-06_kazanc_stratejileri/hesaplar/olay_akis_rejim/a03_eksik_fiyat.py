"""Eksik hisseler icin Is Yatirim HisseTekil (varsayilan basliklar, sirali, 0.7 sn). Bos donenler '.empty' ile isaretlenir."""
import ortak as O
ks = open(O.MY + "/eksik_hisse.txt").read().split()
for i, k in enumerate(ks):
    d = O.hisse(k, fetch=True)
    print(i, k, None if d is None else (len(d), str(d.index[0].date()), str(d.index[-1].date())), flush=True)
