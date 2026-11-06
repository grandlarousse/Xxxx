"""Backtest motoru: olay kuralları (küme durum makinesi + slot portföy) ve rotasyon.
Zamanlama: sinyal t kapanışında (yalnız <=t bilgisi), işlem t+1+L kapanışında (taban L=1: ertesi gün kapanışı),
getiri t+2+L'den itibaren. Maliyet: tek yön c (taban %0.25) x ağırlık değişimi. Boş slot/nakit TL rf kazanır."""
import numpy as np, pandas as pd

class Veri:
    def __init__(self, P, R, C, NU, rf, uyeler, min_uye=2, bas="2011-06-01"):
        self.cal = C.index
        self.kumeler = list(C.columns)
        self.uyeler = {c: [m for m in uyeler[c] if m in R] for c in self.kumeler}
        self.elig = (NU[self.kumeler] >= min_uye).values
        self.C = C.where(NU >= min_uye).values             # küme günlük getiri
        self.Rm = R["XU100"].fillna(0).values
        self.rf = rf.values
        Cz = np.nan_to_num(self.C)
        self.I = np.cumprod(1 + Cz, axis=0)                  # küme fiyat endeksi (uygun olmayan dönemde düz)
        self.Im = np.cumprod(1 + self.Rm)
        self.Rel = self.I / self.Im[:, None]
        self.Irf = np.cumprod(1 + self.rf)
        T, K = self.C.shape
        # uygunluk başlangıcından itibaren yeterli geçmiş sayacı
        self.yas = np.zeros((T, K), int)
        for k in range(K):
            cnt = 0
            for t in range(T):
                cnt = cnt + 1 if self.elig[t, k] else 0
                self.yas[t, k] = cnt
        RelD = pd.DataFrame(self.Rel, index=self.cal, columns=self.kumeler)
        ID = pd.DataFrame(self.I, index=self.cal, columns=self.kumeler)
        self.RelD, self.ID = RelD, ID
        self.ma50rel = RelD.rolling(50).mean().values
        self.hi63 = RelD.rolling(63).max().values
        self.hi126 = RelD.rolling(126).max().values
        self.lag = {L: RelD.shift(L).values for L in (21, 63, 126, 252)}
        self.lag21 = RelD.shift(21).values
        self.lagI = {L: ID.shift(L).values for L in (21, 63, 126, 252)}
        Irf = pd.Series(self.Irf, index=self.cal)
        self.rfL = {L: (Irf / Irf.shift(L) - 1).values for L in (21, 63, 126, 252)}
        xu = pd.Series(self.Im, index=self.cal)
        self.mkt200 = (xu > xu.rolling(200).mean()).values
        # üye bazında: fiyat > 50 GHO (genişlik) ve 63/126g getiri (lider seçimi)
        Pm = P.reindex(self.cal)
        Rr = R.reindex(self.cal)
        self.br = np.full((T, K), np.nan)
        self.mem_idx = {}
        allm = sorted({m for v in self.uyeler.values() for m in v})
        self.allm = allm; mi = {m: i for i, m in enumerate(allm)}
        self.Rmem = Rr[allm].values                          # NaN: veri yok / IPO dışlama
        Pmm = Pm[allm]
        valid = Rr[allm].notna()
        above = (Pmm > Pmm.rolling(50).mean()) & valid & Pmm.rolling(50).mean().notna()
        Imem = (1 + Rr[allm].fillna(0)).cumprod()
        self.mret = {L: (Imem / Imem.shift(L) - 1).where(valid & valid.shift(L, fill_value=False)).values for L in (21, 63, 126, 252)}
        self.mvalid = valid.values
        for k, c in enumerate(self.kumeler):
            ids = [mi[m] for m in self.uyeler[c]]; self.mem_idx[c] = ids
            v = valid.values[:, ids].sum(1); a = above.values[:, ids].sum(1)
            self.br[:, k] = np.where(v > 0, a / np.maximum(v, 1), np.nan)
        self.t0 = int(np.searchsorted(self.cal.values, np.datetime64(bas)))

    def lider(self, t, k, L=63):
        ids = self.mem_idx[self.kumeler[k]]
        x = self.mret[L][t, ids]
        if np.all(np.isnan(x)): return None
        return ids[int(np.nanargmax(x))]

# ---------------- olay kuralları ----------------
def giris_sinyali(V, tip):
    ok = V.elig & (V.yas >= 130)
    with np.errstate(invalid="ignore"):
        if tip == "rs63":   s = V.Rel >= V.hi63 - 1e-12
        elif tip == "rs126": s = V.Rel >= V.hi126 - 1e-12
        elif tip == "br70": s = (V.br >= 0.70) & (V.Rel > V.ma50rel)
        elif tip == "rs63br": s = (V.Rel >= V.hi63 - 1e-12) & (V.br >= 0.60)
        elif tip == "dm6":  s = (V.I / V.lagI[126] - 1 > V.rfL[126][:, None]) & (V.Rel / V.lag[126] > 1)
        elif tip == "dm3":  s = (V.I / V.lagI[63] - 1 > V.rfL[63][:, None]) & (V.Rel / V.lag[63] > 1)
        else: raise ValueError(tip)
    return s & ok

def durum_makinesi(V, giris, cikis, filtre):
    """Küme başına 0/1 durum (slotsuz). Çıkış: 'ma50','rstr10','tr15','ma50|tr15','br40','dm' (giriş koşulu bozulunca)."""
    T, K = V.C.shape
    S = np.zeros((T, K), np.int8)
    E = giris_sinyali(V, giris)
    for k in range(K):
        pos = 0; pI = pR = 0.0
        for t in range(T):
            if not V.elig[t, k]:
                pos = 0; continue
            f = V.mkt200[t] if filtre else True
            I, Rl = V.I[t, k], V.Rel[t, k]
            if pos == 0:
                if E[t, k] and f:
                    pos = 1; pI, pR = I, Rl
            else:
                pI = max(pI, I); pR = max(pR, Rl)
                x = False
                if not f: x = True
                if cikis in ("ma50", "ma50|tr15") and Rl < V.ma50rel[t, k]: x = True
                if cikis in ("tr15", "ma50|tr15") and I < 0.85 * pI: x = True
                if cikis == "tr10" and I < 0.90 * pI: x = True
                if cikis == "rstr10" and Rl < 0.90 * pR: x = True
                if cikis == "br40" and not (V.br[t, k] >= 0.40): x = True
                if cikis == "dm" and not E[t, k]: x = True
                if x: pos = 0
            S[t, k] = pos
    return S

def islemler(V, S, L=1, c=0.0025, lider=False):
    """Slotsuz işlem listesi: her 0->1 geçişi bir işlem. Giriş/çıkış t+1+L kapanışında."""
    T, K = S.shape; out = []
    for k in range(K):
        s = S[:, k]; d = np.diff(np.r_[0, s])
        ent = np.where(d == 1)[0]; ex = np.where(d == -1)[0]
        for e in ent:
            xs = ex[ex > e]; x = xs[0] if len(xs) else T - 1 - (1 + L)
            a, b = e + 1 + L, min(x + 1 + L, T - 1)
            if a >= T - 1 or a >= b: continue
            if lider:
                j = V.lider(e, k)
                if j is None: continue
                r = np.nan_to_num(V.Rmem[a + 1:b + 1, j]); g = np.prod(1 + r) - 1
            else:
                g = V.I[b, k] / V.I[a, k] - 1
            gm = V.Im[b] / V.Im[a] - 1; grf = V.Irf[b] / V.Irf[a] - 1
            net = (1 + g) * (1 - c) ** 2 - 1
            out.append(dict(kume=V.kumeler[k], sinyal=V.cal[e], giris=V.cal[a], cikis=V.cal[b], gun=b - a,
                            acik=len(xs) == 0, getiri=net, xu100=gm, rf=grf, ia=a, ib=b, k=k))
    return pd.DataFrame(out)

def slot_portfoy(V, S, nslot=3, L=1, c=0.0025, lider=False, sira=126):
    """Durumu açık kümeleri slotlara yerleştir (mevcut korunur, boş slot sıra=126g RS ile doldurulur)."""
    T, K = S.shape
    W = np.zeros((T, K)); held = {}  # k -> leader idx or -1
    LJ = np.full((T, K), -1, int)
    for t in range(T):
        for k in list(held):
            if S[t, k] == 0: del held[k]
        free = nslot - len(held)
        if free > 0:
            cand = [k for k in range(K) if S[t, k] == 1 and k not in held]
            if cand:
                sc = [V.Rel[t, k] / V.lag[sira][t, k] if V.lag[sira][t, k] > 0 else -9 for k in cand]
                for i in np.argsort(sc)[::-1][:free]:
                    k = cand[i]; held[k] = V.lider(t, k) if lider else -1
                    if lider and held[k] is None: del held[k]
        for k, j in held.items():
            W[t, k] = 1.0 / nslot; LJ[t, k] = j
    return getiri_seri(V, W, LJ, L, c, lider)

def getiri_seri(V, W, LJ, L, c, lider):
    T, K = W.shape
    sh = 1 + L
    We = np.zeros_like(W); We[sh:] = W[:-sh]
    LJe = np.full_like(LJ, -1); LJe[sh:] = LJ[:-sh]
    if lider:
        Rpos = np.zeros((T, K))
        for k in range(K):
            m = LJe[:, k] >= 0
            idx = np.where(m)[0]
            Rpos[idx, k] = np.nan_to_num(V.Rmem[idx, LJe[idx, k]])
    else:
        Rpos = np.nan_to_num(V.C)
    # ağırlık değişimi (lider değişimi tam devir sayılır)
    Wprev = np.zeros_like(We); Wprev[1:] = We[:-1]
    LJprev = np.full_like(LJe, -1); LJprev[1:] = LJe[:-1]
    to = np.abs(We - Wprev)
    if lider:
        sw = (We > 0) & (Wprev > 0) & (LJe != LJprev)
        to = to + np.where(sw, We + Wprev, 0)
    cost = c * to.sum(1)
    inv = We.sum(1)
    r = (We * Rpos).sum(1) + (1 - inv) * V.rf - cost
    return pd.Series(r, index=V.cal), pd.Series(inv, index=V.cal), pd.Series(to.sum(1), index=V.cal), We

# ---------------- rotasyon ----------------
def rebal_gunleri(cal, freq):
    s = pd.Series(np.arange(len(cal)), index=cal)
    if freq == "W": g = s.groupby([cal.isocalendar().year.values, cal.isocalendar().week.values]).max()
    else: g = s.groupby([cal.year, cal.month]).max()
    return set(g.values.tolist())

def rotasyon(V, skor="r63", K=3, freq="M", absf=False, mktf=False, lider=False, buf=0, L=1, c=0.0025):
    T, NK = V.C.shape
    rb = rebal_gunleri(V.cal, freq)
    W = np.zeros((T, NK)); LJ = np.full((T, NK), -1, int)
    held = {}
    for t in range(T):
        if t in rb and t >= V.t0 - 1:
            ok = V.elig[t] & (V.yas[t] >= 130)
            with np.errstate(invalid="ignore", divide="ignore"):
                if skor == "komp":
                    sc = np.nanmean(np.vstack([V.Rel[t] / V.lag[L_][t] - 1 for L_ in (21, 63, 126)]), 0)
                elif skor == "r252s21":
                    sc = V.lag21[t] / V.lag[252][t] - 1
                else:
                    Lb = int(skor[1:]); sc = V.Rel[t] / V.lag[Lb][t] - 1
            sc = np.where(ok & np.isfinite(sc), sc, -np.inf)
            order = np.argsort(-sc); rank = np.empty(NK, int); rank[order] = np.arange(NK)
            new = {}
            if (not mktf) or V.mkt200[t]:
                keep = [k for k in held if rank[k] < K + buf and np.isfinite(sc[k])]
                sel = list(keep)
                for k in order:
                    if len(sel) >= K: break
                    if np.isfinite(sc[k]) and k not in sel: sel.append(k)
                for k in sel:
                    if absf and not (V.I[t, k] / V.lagI[63][t, k] - 1 > V.rfL[63][t]): continue
                    Lsel = 63 if skor == "komp" else (252 if skor == "r252s21" else int(skor[1:]))
                    new[k] = (V.lider(t, k, Lsel) if lider else -1)
                    if lider and new[k] is None: del new[k]
            held = new
        for k, j in held.items():
            W[t, k] = 1.0 / K; LJ[t, k] = j
    return getiri_seri(V, W, LJ, L, c, lider)

# ---------------- ölçüler ----------------
def olcu(r, inv, to, V, bas, son=None, usd=None):
    r = r.loc[bas:son]; rf = pd.Series(V.rf, index=V.cal).loc[r.index]; rm = pd.Series(V.Rm, index=V.cal).loc[r.index]
    n = len(r); yil = n / 252.0
    nav = (1 + r).cumprod()
    cagr = nav.iloc[-1] ** (1 / yil) - 1
    rfc = (1 + rf).prod() ** (1 / yil) - 1; mc = (1 + rm).prod() ** (1 / yil) - 1
    dd = (nav / nav.cummax() - 1).min()
    ex = r - rf; sh = ex.mean() / ex.std() * np.sqrt(252) if ex.std() > 0 else np.nan
    o = dict(cagr=cagr, rf=rfc, xu100=mc, a_rf=(1 + cagr) / (1 + rfc) - 1, a_xu=(1 + cagr) / (1 + mc) - 1,
             vol=r.std() * np.sqrt(252), sharpe=sh, maxdd=dd, maruz=inv.loc[r.index].mean(), devir_yil=to.loc[r.index].sum() / yil / 2)
    if usd is not None:
        u = usd.loc[r.index]; o["cagr_usd"] = (nav.iloc[-1] / (u.iloc[-1] / u.iloc[0])) ** (1 / yil) - 1
    return o

def yillik(r, V):
    rf = pd.Series(V.rf, index=V.cal); rm = pd.Series(V.Rm, index=V.cal)
    g = lambda x: x.groupby(x.index.year).apply(lambda z: (1 + z).prod() - 1)
    return pd.DataFrame({"strateji": g(r), "rf": g(rf.loc[r.index]), "xu100": g(rm.loc[r.index])})
