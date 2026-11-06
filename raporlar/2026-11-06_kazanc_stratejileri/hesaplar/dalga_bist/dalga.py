"""Dalga tanımı (sonuçlara bakmadan önceden ilan edildi):
 R = küme TL toplam getiri endeksi / XU100.  log R üzerinde zigzag, dönüş eşiği D (taban: %15).
 Yükseliş bacağı [dip T, tepe P] 'BÜYÜK DALGA' sayılır eğer bacak içinde <=126 işlem günlük (6 ay) herhangi bir pencerede
 R >= +%30 arttıysa (taban). Duyarlılık: D=%20 & eşik %50.  Son bacak 'devam' olabilir (tepe teyitsiz)."""
import numpy as np, pandas as pd
def zigzag(lr, d):
    """lr: log seri (np.array). d: log dönüş eşiği. Dönüş: [(i_dip, i_tepe, teyitli)] yükseliş bacakları."""
    n = len(lr); legs = []
    i0 = 0
    while i0 < n and np.isnan(lr[i0]): i0 += 1
    if i0 >= n: return legs
    hi = lo = lr[i0]; ihi = ilo = i0; yon = 0
    for i in range(i0 + 1, n):
        x = lr[i]
        if np.isnan(x): continue
        if yon >= 0:
            if x > hi: hi, ihi = x, i
        if yon <= 0:
            if x < lo: lo, ilo = x, i
        if yon == 0:
            if x - lo >= d: yon = 1; hi, ihi = x, i
            elif hi - x >= d: yon = -1; lo, ilo = x, i
        elif yon == 1 and hi - x >= d:
            legs.append((ilo, ihi, True)); yon = -1; lo, ilo = x, i
        elif yon == -1 and x - lo >= d:
            yon = 1; hi, ihi = x, i
    if yon == 1: legs.append((ilo, ihi, False))
    return legs
def max_pencere_kazanc(lr, a, b, w=126):
    """[a,b] içinde t2-t1<=w olan max lr[t2]-lr[t1] ve başlangıç/bitiş."""
    best = -9; bb = (a, a)
    x = lr[a:b + 1]
    for j in range(len(x)):
        lo = np.nanmin(x[max(0, j - w):j + 1]); k = np.nanargmin(x[max(0, j - w):j + 1]) + max(0, j - w)
        if x[j] - lo > best: best = x[j] - lo; bb = (a + k, a + j)
    return best, bb
def dalgalar(Rel, D=0.15, esik=0.30, w=126):
    """Rel: DataFrame (tarih x küme) göreli endeks. Dönüş: dalga listesi DataFrame."""
    rows = []
    for c in Rel:
        s = Rel[c]; lr = np.log(s.values)
        for a, b, tey in zigzag(lr, np.log(1 + D)):
            g, (p1, p2) = max_pencere_kazanc(lr, a, b, w)
            if g >= np.log(1 + esik):
                rows.append(dict(kume=c, dip=s.index[a], tepe=s.index[b], teyitli=tey, gun=b - a,
                                 rel=np.exp(lr[b] - lr[a]) - 1, ia=a, ib=b,
                                 max6ay=np.exp(g) - 1, p6_bas=s.index[p1], p6_son=s.index[p2]))
    return pd.DataFrame(rows)
