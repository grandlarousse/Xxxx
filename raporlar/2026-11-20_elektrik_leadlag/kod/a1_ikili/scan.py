"""A1 hisse -> hisse ikili öncülük taraması (yalnız IS paneli).
Kullanım: python3 -I scan.py <panel_is klasörü> <çıktı klasörü>
T1 doğrusal (Newey-West), T2 eşikli olay, BH-FDR, dairesel kaydırma sıfır dağılımı, kalıcılık,
önceden yazılı hipotezler, küme içi/arası bağ oranı, bayat fiyat (gece/gün içi, likidite üçte birliği).
"""
import sys, os, json, time
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402

PANEL = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)
NREP = int(os.environ.get('A1_NREP', '200'))
SPLIT = pd.Timestamp('2019-12-31')
MIN_N = 250
GROUPS = [['NATEN', 'ESEN', 'MAGEN'], ['ODAS', 'CANTE'], ['AHGAZ', 'ENERY'], ['SMRTG', 'ALFAS', 'EUPWR']]
UYE_CSV = os.path.join(HERE, '..', '..', 'ek', 'xelkt_uyeler.csv')

P = elib.load(PANEL)
R = P['ret_cc']
assert R.index.max() <= elib.IS_END, 'KÖR PROTOKOL: panel IS sonunu aşıyor'
dates = R.index
T = len(dates)
SEC = elib.sector_cols(P)
SRC = elib.sector_cols(P, extra=True)
trad = P['tradable']
Rt = R.where(trad)
mkt = P['idx_ret']['XU100'].reindex(dates).values
secsum = Rt[SEC].fillna(0).sum(axis=1).values
secn = Rt[SEC].notna().sum(axis=1).values
X_src = {j: Rt[j].values.astype(float) for j in SRC}
Y = {}
for h in (1, 2, 3):
    f, fl, _ = elib.fwd_exec(P, h, 'long', SEC)
    Y[h] = f.where(fl)
Yco = P['ret_co'][SEC].shift(-1).where(P['fill_long'][SEC])
Yoc = P['ret_oc'][SEC].shift(-1).where(P['fill_long'][SEC])
first_half = (dates <= SPLIT)
NTEST = {}


def sec_ex(i, j):
    s = secsum - np.nan_to_num(X_src[i])
    n = secn - np.isfinite(X_src[i]).astype(int)
    if j in SEC:
        s = s - np.nan_to_num(X_src[j])
        n = n - np.isfinite(X_src[j]).astype(int)
    return np.where(n >= 3, s / np.maximum(n, 1), np.nan)


def nw(y, X, lag):
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ (X.T @ y)
    u = y - X @ b
    Xu = X * u[:, None]
    S = Xu.T @ Xu
    for q in range(1, lag + 1):
        G = Xu[q:].T @ Xu[:-q]
        S += (1 - q / (lag + 1)) * (G + G.T)
    V = XtXi @ S @ XtXi * (n / (n - k))
    return b, b / np.sqrt(np.maximum(np.diag(V), 1e-30))


def t1(y, xj, xi, s, lag, with_sec=True, sel=None, min_n=MIN_N):
    ok = np.isfinite(y) & np.isfinite(xj) & np.isfinite(xi) & np.isfinite(mkt) & np.isfinite(s)
    if sel is not None:
        ok &= sel
    n = int(ok.sum())
    if n < min_n or np.nanstd(xj[ok]) < 1e-8:
        return None
    cols = [np.ones(n), xj[ok], xi[ok], mkt[ok]] + ([s[ok]] if with_sec else [])
    try:
        b, t = nw(y[ok], np.column_stack(cols), lag)
    except np.linalg.LinAlgError:
        return None
    return n, b[1], t[1]


def roll_valid(x, rng):
    v = np.where(np.isfinite(x))[0]
    if len(v) < 90:
        return None
    a, b = v[0], v[-1] + 1
    k = int(rng.integers(30, (b - a) - 30))
    x2 = x.copy()
    x2[a:b] = np.roll(x[a:b], k)
    return x2


PAIRS = [(j, i) for i in SEC for j in SRC if j != i]


def null_rep(seed):
    rng = np.random.default_rng(1000 + seed)
    xs = {j: roll_valid(X_src[j], rng) for j in SRC}
    mx = {1: 0.0, 2: 0.0, 3: 0.0}
    for (j, i) in PAIRS:
        if xs[j] is None or (j, i) not in VALID:
            continue
        s = sec_ex(i, j)
        for h in (1, 2, 3):
            r = t1(Y[h][i].values, xs[j], X_src[i], s, h)
            if r is not None:
                mx[h] = max(mx[h], abs(r[2]))
    return [mx[1], mx[2], mx[3]]


# ---------------------------------------------------------------- T2 (vektörel)
sd60 = R.rolling(60, min_periods=40).std().shift(1)
Z = (Rt / sd60)
EV = {'up5': (Rt[SRC] >= 0.05), 'dn5': (Rt[SRC] <= -0.05), 'zup2': (Z[SRC] >= 2) & (Rt[SRC] > 0), 'zdn2': (Z[SRC] <= -2) & (Rt[SRC] < 0)}
FSEC = {}
for h in (1, 2, 3):
    M, fl = elib.excess_measures(P, h, 'long', SEC)
    FSEC[h] = M['sec'].where(fl)


def t2_mat(E, F, lag, sel=None):
    """E: T×Ns bool, F: T×Ni (NaN = yok). Dönen: n, ortalama, t (Ns×Ni); elib._hac_mean ile aynı formül."""
    fin = np.isfinite(F)
    if sel is not None:
        fin = fin & sel[:, None]
    F0 = np.where(fin, F, 0.0)
    Ef = E.astype(float)
    fn = fin.astype(float)
    n = Ef.T @ fn
    sm = Ef.T @ F0
    sq = Ef.T @ (F0 * F0)
    with np.errstate(all='ignore'):
        mu = sm / n
        S = sq - n * mu * mu
        for q in range(1, lag + 1):
            w = 1 - q / (lag + 1)
            EE = (E[q:] & E[:-q]).astype(float)
            A = EE.T @ (F0[q:] * F0[:-q])
            B = EE.T @ (F0[q:] * fn[:-q] + fn[q:] * F0[:-q])
            C = EE.T @ (fn[q:] * fn[:-q])
            S = S + 2 * w * (A - mu * B + mu * mu * C)
        t = mu / (np.sqrt(np.maximum(S, 1e-30)) / n)
    return n, mu, t


def t2_null_rep(seed):
    rng = np.random.default_rng(5000 + seed)
    ks = {}
    out = []
    for h in (1, 2, 3):
        mx = 0.0
        for ev, E in EV.items():
            Ev = E.values.copy()
            for c, j in enumerate(SRC):
                v = np.where(np.isfinite(X_src[j]))[0]
                if len(v) < 90:
                    Ev[:, c] = False
                    continue
                a, b = v[0], v[-1] + 1
                k = ks.setdefault(j, int(rng.integers(30, (b - a) - 30)))
                Ev[a:b, c] = np.roll(Ev[a:b, c], k)
            n, mu, t = t2_mat(Ev, FSEC[h].values, h - 1)
            ok = (n >= 15) & SAME_MASK
            if ok.any():
                mx = max(mx, np.nanmax(np.abs(t[ok])))
        out.append(mx)
    return out


SAME_MASK = np.array([[j != i for i in SEC] for j in SRC])
VALID = set()

if __name__ == '__main__':
    t0 = time.time()
    first = R.apply(lambda s: s.first_valid_index())
    print('hisse sayısı', R.shape[1], '| sektör', len(SEC), '| kaynak', len(SRC), '| tarih', dates.min().date(), dates.max().date())
    print('ilk gün / tradable gün:', {c: (str(first[c].date()), int(trad[c].sum())) for c in R.columns})
    print('IS içinde olmayan önceden yazılı semboller:', [s for g in GROUPS for s in g if s not in R.columns] + [s for s in ['ASTOR'] if s not in R.columns])

    # ------------------------------------------------------------ T1
    rows = []
    for (j, i) in PAIRS:
        s = sec_ex(i, j)
        xi, xj = X_src[i], X_src[j]
        for h in (1, 2, 3):
            y = Y[h][i].values
            r = t1(y, xj, xi, s, h)
            if r is None:
                continue
            VALID.add((j, i))
            n, b, t = r
            r0 = t1(y, xj, xi, s, h, with_sec=False)
            row = {'kaynak': j, 'hedef': i, 'h': h, 'n': n, 'b': b, 't': t, 't_sektorsuz': r0[2]}
            ok = np.isfinite(y) & np.isfinite(xj) & np.isfinite(xi) & np.isfinite(mkt) & np.isfinite(s)
            # takvim yarıları
            ra = t1(y, xj, xi, s, h, sel=first_half); rb = t1(y, xj, xi, s, h, sel=~first_half)
            row['t_2019oncesi'] = ra[2] if ra else np.nan; row['t_2020sonrasi'] = rb[2] if rb else np.nan
            # çiftin kronolojik iki yarısı
            idx = np.where(ok)[0]; cut = idx[len(idx) // 2]
            pos = np.arange(T)
            rc = t1(y, xj, xi, s, h, sel=pos < cut, min_n=120); rd = t1(y, xj, xi, s, h, sel=pos >= cut, min_n=120)
            row['t_yari1'] = rc[2] if rc else np.nan; row['t_yari2'] = rd[2] if rd else np.nan
            if h == 1:
                rco = t1(Yco[i].values, xj, xi, s, 1, sel=ok); roc = t1(Yoc[i].values, xj, xi, s, 1, sel=ok)
                row['b_gece'] = rco[1] if rco else np.nan; row['t_gece'] = rco[2] if rco else np.nan
                row['b_gunici'] = roc[1] if roc else np.nan; row['t_gunici'] = roc[2] if roc else np.nan
            rows.append(row)
    T1 = pd.DataFrame(rows)
    T1['p'] = elib.t_to_p(T1['t'].values)
    T1['bh'] = False
    for h in (1, 2, 3):
        m = T1['h'] == h
        T1.loc[m, 'bh'] = elib.bh_fdr(T1.loc[m, 'p'].values, 0.10)
    NTEST['T1_sektor_kontrollu'] = len(T1); NTEST['T1_sektorsuz'] = len(T1)
    NTEST['T1_yari_testleri'] = int(T1[['t_2019oncesi', 't_2020sonrasi', 't_yari1', 't_yari2']].notna().sum().sum())
    NTEST['T1_gece_gunici'] = int(T1[['t_gece', 't_gunici']].notna().sum().sum())
    print(f'\n== T1: {len(VALID)} sıralı çift (>= {MIN_N} ortak gün); {len(T1)} regresyon; süre {time.time()-t0:.0f}s')
    for h in (1, 2, 3):
        d = T1[T1['h'] == h]
        print(f" h={h}: n_çift={len(d)} | BH geçen={int(d['bh'].sum())} | |t|>=2: {(d['t'].abs()>=2).mean():.3f} (sektörsüz {(d['t_sektorsuz'].abs()>=2).mean():.3f}) "
              f"| |t|>=3: {int((d['t'].abs()>=3).sum())} | ort t={d['t'].mean():.2f} (sektörsüz {d['t_sektorsuz'].mean():.2f}) | max|t|={d['t'].abs().max():.2f} "
              f"| t>0 oranı={(d['t']>0).mean():.2f}")
    print(' en büyük |t| 15 bağ (h=1):')
    print(T1[T1['h'] == 1].reindex(T1[T1['h'] == 1]['t'].abs().sort_values(ascending=False).index).head(15)
          [['kaynak', 'hedef', 'n', 'b', 't', 't_sektorsuz', 't_2019oncesi', 't_2020sonrasi', 't_yari1', 't_yari2', 't_gece', 't_gunici', 'bh']].round(2).to_string(index=False))

    # sıfır dağılımı (dairesel kaydırma)
    from multiprocessing import Pool
    with Pool(4) as pool:
        null = np.array(pool.map(null_rep, range(NREP)))
    NTEST['T1_sifir_dagilimi_regresyon'] = int(NREP * len(T1))
    T1null = {}
    for k, h in enumerate((1, 2, 3)):
        real = T1[T1['h'] == h]['t'].abs().max()
        pv = (np.sum(null[:, k] >= real) + 1) / (NREP + 1)
        T1null[h] = {'gercek_max_t': float(real), 'sifir_medyan': float(np.median(null[:, k])), 'sifir_p95': float(np.quantile(null[:, k], 0.95)), 'p': float(pv)}
    print(f' sıfır dağılımı (NREP={NREP}, tüm {len(VALID)} çift) max|t|:', json.dumps(T1null), f'| süre {time.time()-t0:.0f}s')

    # kalıcılık
    def persist(d, a, b, label):
        s = d[d[a].abs() >= 2].dropna(subset=[b])
        allp = d.dropna(subset=[a, b])
        rate = float((np.sign(s[a]) == np.sign(s[b])).mean()) if len(s) else np.nan
        sig2 = float(((np.sign(s[a]) == np.sign(s[b])) & (s[b].abs() >= 2)).mean()) if len(s) else np.nan
        cor = float(allp[[a, b]].corr(method='spearman').iloc[0, 1]) if len(allp) > 5 else np.nan
        la, lb = allp.groupby('kaynak')[a].mean(), allp.groupby('kaynak')[b].mean()
        lcor = float(pd.concat([la, lb], axis=1).corr(method='spearman').iloc[0, 1]) if len(la) > 3 else np.nan
        fa, fb = allp.groupby('hedef')[a].mean(), allp.groupby('hedef')[b].mean()
        fcor = float(pd.concat([fa, fb], axis=1).corr(method='spearman').iloc[0, 1]) if len(fa) > 3 else np.nan
        return {'bolme': label, 'n_cift': int(len(allp)), 'ilk_yarida_anlamli': int(len(s)), 'ayni_isaret_orani': rate, 'ikinci_yarida_da_anlamli': sig2,
                'cift_t_sira_kor': cor, 'n_lider': int(len(la)), 'lider_skoru_sira_kor': lcor, 'izleyici_skoru_sira_kor': fcor}
    PERS = []
    for h in (1, 2, 3):
        d = T1[T1['h'] == h]
        for a, b, lab in [('t_2019oncesi', 't_2020sonrasi', 'takvim'), ('t_yari1', 't_yari2', 'cift_kronolojik')]:
            r = persist(d, a, b, lab); r['h'] = h; PERS.append(r)
    PERS = pd.DataFrame(PERS)
    print('\n== Kalıcılık (T1, sektör kontrollü)'); print(PERS.round(3).to_string(index=False))
    lead = T1[T1['h'] == 1].groupby('kaynak')['t'].agg(['mean', 'count']).sort_values('mean', ascending=False)
    print(' lider skoru (giden bağların ort. t, h=1):', {k: round(v, 2) for k, v in lead['mean'].items()})
    foll = T1[T1['h'] == 1].groupby('hedef')['t'].mean().sort_values(ascending=False)
    print(' izleyici skoru (gelen bağların ort. t, h=1):', {k: round(v, 2) for k, v in foll.items()})

    # ------------------------------------------------------------ T2
    rows = []
    for h in (1, 2, 3):
        F = FSEC[h].values
        for ev, E in EV.items():
            n, mu, t = t2_mat(E.values, F, h - 1)
            na, mua, ta = t2_mat(E.values, F, h - 1, sel=first_half)
            nb, mub, tb = t2_mat(E.values, F, h - 1, sel=~first_half)
            for a, j in enumerate(SRC):
                for b, i in enumerate(SEC):
                    if j == i or n[a, b] < 15:
                        continue
                    rows.append({'kaynak': j, 'hedef': i, 'olay': ev, 'h': h, 'n': int(n[a, b]), 'ort_bps': 1e4 * mu[a, b], 't': t[a, b],
                                 't_2019oncesi': ta[a, b] if na[a, b] >= 8 else np.nan, 't_2020sonrasi': tb[a, b] if nb[a, b] >= 8 else np.nan})
    T2 = pd.DataFrame(rows)
    T2['p'] = elib.t_to_p(T2['t'].values); T2['bh'] = False
    for h in (1, 2, 3):
        m = T2['h'] == h
        T2.loc[m, 'bh'] = elib.bh_fdr(T2.loc[m, 'p'].values, 0.10)
    NTEST['T2_olay'] = len(T2)
    NTEST['T2_yari_testleri'] = int(T2[['t_2019oncesi', 't_2020sonrasi']].notna().sum().sum())
    print(f'\n== T2: {len(T2)} test (>=15 olay)')
    for h in (1, 2, 3):
        d = T2[T2['h'] == h]
        print(f" h={h}: n={len(d)} | BH geçen={int(d['bh'].sum())} | |t|>=2: {(d['t'].abs()>=2).mean():.3f} | max|t|={d['t'].abs().max():.2f} | "
              + ' '.join(f"{ev}: ort={d[d['olay']==ev]['ort_bps'].mean():.0f}bps, t>0={(d[d['olay']==ev]['t']>0).mean():.2f}" for ev in EV))
    print(T2.reindex(T2['t'].abs().sort_values(ascending=False).index).head(12).round(2).to_string(index=False))
    with Pool(4) as pool:
        null2 = np.array(pool.map(t2_null_rep, range(NREP)))
    NTEST['T2_sifir_dagilimi'] = int(NREP * len(T2))
    T2null = {}
    for k, h in enumerate((1, 2, 3)):
        real = T2[T2['h'] == h]['t'].abs().max()
        T2null[h] = {'gercek_max_t': float(real), 'sifir_medyan': float(np.median(null2[:, k])), 'sifir_p95': float(np.quantile(null2[:, k], 0.95)),
                     'p': float((np.sum(null2[:, k] >= real) + 1) / (NREP + 1))}
    print(' T2 sıfır dağılımı max|t|:', json.dumps(T2null))
    d = T2.dropna(subset=['t_2019oncesi', 't_2020sonrasi'])
    s = d[d['t_2019oncesi'].abs() >= 2]
    print(f" T2 kalıcılık: iki yarıda da ölçülen {len(d)}; ilk yarıda |t|>=2 {len(s)}; ikinci yarıda aynı işaret {(np.sign(s['t_2019oncesi'])==np.sign(s['t_2020sonrasi'])).mean():.2f}")

    # ------------------------------------------------------------ Önceden yazılı hipotezler
    print('\n== Önceden yazılı çiftler (T1 t; eşik |t|>=2,5)')
    hyp = []
    for g in GROUPS:
        for j in g:
            for i in g:
                if i != j:
                    hyp.append((j, i))
    H = T1[[(a, b) in hyp for a, b in zip(T1['kaynak'], T1['hedef'])]]
    NTEST['hipotez_cift_T1'] = len(H)
    print(H[['kaynak', 'hedef', 'h', 'n', 'b', 't', 't_sektorsuz', 't_yari1', 't_yari2', 't_gece', 't_gunici']].round(2).to_string(index=False))
    H2 = T2[[(a, b) in hyp for a, b in zip(T2['kaynak'], T2['hedef'])]]
    print(H2.round(2).to_string(index=False))
    missing = [p for p in hyp if p not in VALID]
    print(' IS\'te sınanamayan önceden yazılı çiftler:', missing)
    # büyükler -> diğerleri
    big = [b for b in elib.BIG if b in R.columns]
    d = T1[T1['kaynak'].isin(big) & ~T1['hedef'].isin(big)]
    o = T1[~T1['kaynak'].isin(big) & ~T1['hedef'].isin(big)]
    BIGS = {}
    for h in (1, 2, 3):
        dd, oo = d[d['h'] == h], o[o['h'] == h]
        BIGS[h] = {'n': len(dd), 'ort_t': round(float(dd['t'].mean()), 2), 'abs_t_ge2': round(float((dd['t'].abs() >= 2).mean()), 3), 'abs_t_ge2_5': int((dd['t'].abs() >= 2.5).sum()),
                   'diger_ort_t': round(float(oo['t'].mean()), 2), 'diger_abs_t_ge2': round(float((oo['t'].abs() >= 2).mean()), 3)}
    print(' büyükler', big, '-> diğerleri:', json.dumps(BIGS))
    # havuz zaman serisi: EW küçük f_h ~ EW büyük r + EW küçük r + XU100
    small = [c for c in SEC if c not in big]
    xb = Rt[big].mean(axis=1).where(Rt[big].notna().sum(axis=1) >= 2)
    xs_ = Rt[small].mean(axis=1).where(Rt[small].notna().sum(axis=1) >= 3)
    for h in (1, 2, 3):
        yy = Y[h][small].mean(axis=1).where(Y[h][small].notna().sum(axis=1) >= 3)
        rr = elib.ts_reg(yy, pd.concat([xb.rename('buyuk'), xs_.rename('kucuk'), pd.Series(mkt, index=dates, name='xu100')], axis=1), lag=h)
        print(f"  havuz h={h}: büyük sepet katsayı={rr.loc['buyuk','katsayi']:.3f} t={rr.loc['buyuk','t']:.2f} | küçük sepet (öz) t={rr.loc['kucuk','t']:.2f} | xu100 t={rr.loc['xu100','t']:.2f} | n={int(rr['n'].iloc[0])}")
        NTEST['buyuk_havuz'] = NTEST.get('buyuk_havuz', 0) + 1

    # çift farkı ortalamaya dönüş (hata düzeltme): s = kümülatif (r_i − r_j) 20 günlük z -> i'nin sec-fazla f_h'i
    print('\n== Çift farkı dönüşü (grup çiftleri): f_h(i) sec-fazla ~ z20(kümülatif r_i − r_j) [+ r_i(t)]')
    SP = []
    for (j, i) in hyp:
        if j not in R.columns or i not in SEC:
            continue
        dlt = (Rt[i] - Rt[j])
        C = dlt.fillna(0).cumsum().where(dlt.notna())
        z = (C - C.rolling(20, min_periods=15).mean()) / C.rolling(20, min_periods=15).std()
        for h in (1, 2, 3):
            a = elib.ts_reg(FSEC[h][i], z.rename('z').to_frame(), lag=h)
            b = elib.ts_reg(FSEC[h][i], pd.concat([z.rename('z'), Rt[i].rename('ri')], axis=1), lag=h)
            if a is None:
                continue
            SP.append({'i': i, 'j': j, 'h': h, 'n': int(a['n'].iloc[0]), 'b_z_bps': 1e4 * a.loc['z', 'katsayi'], 't_z': a.loc['z', 't'], 't_z_ozkontrollu': b.loc['z', 't'] if b is not None else np.nan})
    SP = pd.DataFrame(SP)
    NTEST['cift_farki_regresyon'] = 2 * len(SP)
    print(SP.round(2).to_string(index=False))

    # küme içi / kümeler arası
    uy = pd.read_csv(UYE_CSV, usecols=['sym', 'ana_faaliyet'])
    kume = {a: str(b).replace('?', '').strip() for a, b in zip(uy['sym'], uy['ana_faaliyet'])}
    T1['ayni_kume'] = [kume.get(a) is not None and kume.get(a) == kume.get(b) for a, b in zip(T1['kaynak'], T1['hedef'])]
    print('\n== Küme içi / arası (T1, kaynak XELKT üyesi)')
    CL = []
    for h in (1, 2, 3):
        d = T1[(T1['h'] == h) & T1['kaynak'].isin(SEC)]
        for lab, dd in [('kume_ici', d[d['ayni_kume']]), ('kume_arasi', d[~d['ayni_kume']])]:
            CL.append({'h': h, 'tur': lab, 'n': len(dd), 'abs_t_ge2': (dd['t'].abs() >= 2).mean(), 'poz_t_ge2': (dd['t'] >= 2).mean(), 'ort_t': dd['t'].mean(), 'bh': int(dd['bh'].sum())})
    CL = pd.DataFrame(CL); print(CL.round(3).to_string(index=False))
    print(' kümeler:', {k: [s for s in SEC if kume.get(s) == k] for k in sorted(set(kume[s] for s in SEC if s in kume))})

    # bayat fiyat: hedefin adv60 üçte birliği + gece / gün içi
    adv = elib.adv60(P)[SEC].where(trad[SEC])
    pr = adv.rank(axis=1, pct=True)
    avgp = pr.mean()
    terc = pd.qcut(avgp, 3, labels=['dusuk_likidite', 'orta', 'yuksek_likidite'])
    T1['hedef_likidite'] = T1['hedef'].map(terc)
    print('\n== Bayat fiyat kontrolü (T1 h=1)')
    d = T1[T1['h'] == 1]
    ST = d.groupby('hedef_likidite', observed=True).agg(n=('t', 'size'), abs_t_ge2=('t', lambda x: (x.abs() >= 2).mean()), poz_t_ge2=('t', lambda x: (x >= 2).mean()),
                                                       ort_t=('t', 'mean'), ort_t_gece=('t_gece', 'mean'), ort_t_gunici=('t_gunici', 'mean'))
    print(ST.round(3).to_string())
    sg = d[d['t'].abs() >= 2]
    share = (sg['b_gece'] / sg['b']).clip(-2, 3)
    print(f" |t|>=2 bağlar (n={len(sg)}): katsayının gece payı medyan={share.median():.2f}; gece t ile aynı işaret={(np.sign(sg['t_gece'])==np.sign(sg['t'])).mean():.2f}; "
          f"gün içi t ile aynı işaret={(np.sign(sg['t_gunici'])==np.sign(sg['t'])).mean():.2f}; |t_gece|>=2: {(sg['t_gece'].abs()>=2).mean():.2f}; |t_gunici|>=2: {(sg['t_gunici'].abs()>=2).mean():.2f}")
    print(' likidite grupları:', {k: list(terc[terc == k].index) for k in terc.cat.categories})

    T1.to_csv(os.path.join(OUT, 't1_cift.csv'), index=False)
    T2.to_csv(os.path.join(OUT, 't2_olay.csv'), index=False)
    PERS.to_csv(os.path.join(OUT, 'kalicilik.csv'), index=False)
    SP.to_csv(os.path.join(OUT, 'cift_farki.csv'), index=False)
    CL.to_csv(os.path.join(OUT, 'kume.csv'), index=False)
    json.dump({'n_cift': len(VALID), 'T1_null': T1null, 'T2_null': T2null, 'buyukler': BIGS, 'testler': NTEST, 'toplam_test': int(sum(NTEST.values())),
               'bh_T1': {int(h): int(T1[(T1['h'] == h)]['bh'].sum()) for h in (1, 2, 3)}, 'bh_T2': {int(h): int(T2[(T2['h'] == h)]['bh'].sum()) for h in (1, 2, 3)}},
              open(os.path.join(OUT, 'scan_ozet.json'), 'w'), indent=1)
    print('\ntest sayıları:', json.dumps(NTEST), '| toplam', sum(NTEST.values()), f'| süre {time.time()-t0:.0f}s')
