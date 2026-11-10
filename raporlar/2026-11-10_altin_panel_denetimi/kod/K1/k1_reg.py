"""K1 analiz 1: artimsal regresyonlar (Newey-West), FDR, artefakt kontrolu, gecenler icin islem kurali + plasebo.
Girdi: SCR/k1_panel.pkl (k1_prep.py). Bagimsiz kod; scipy/statsmodels yok."""
import numpy as np, pandas as pd, math
SCR = '/tmp/claude-0/-home-user-Xxxx/e31e33e0-f360-5bc6-a008-2cee330297de/scratchpad'
OUT = '/home/user/Xxxx/raporlar/2026-11-10_altin_panel_denetimi/hesap/K1'
log = open(OUT + '/reg.log', 'w')
def L(*a):
    s = ' '.join(str(x) for x in a); print(s); log.write(s + '\n')
P = pd.read_pickle(SCR + '/k1_panel.pkl')
idx = P.index; N = len(P)
def sig(x): return x.shift(1).rolling(250, min_periods=100).std()
def sigs(x): return x.shift(1).rolling(250, min_periods=60).std()
def rbeta(a, b):
    return (a.rolling(250, min_periods=100).cov(b) / b.rolling(250, min_periods=100).var()).shift(1)
g = P['r_XAU']
X = pd.DataFrame(index=idx)
X['gz'] = g / (sig(g) * np.sqrt(P['dgap']))
X['rTz'] = P['r_TRALT'] / sig(P['r_TRALT'])
raw = {}
raw['gnight'] = np.log(P['gc07'] / P['gc14_prev']); raw['gday'] = np.log(P['gc14'] / P['gc07'])
for s in ['GLD', 'GDX', 'GDXJ', 'PHYS']: raw['r' + s] = P['us_' + s]
bGDX = rbeta(P['us_GDX'], P['us_GLD']); bGDXJ = rbeta(P['us_GDXJ'], P['us_GDX']); bSLV = rbeta(P['us_SLV'], P['us_GLD'])
raw['eGDX'] = P['us_GDX'] - bGDX * P['us_GLD']
raw['eGDXJ'] = P['us_GDXJ'] - bGDXJ * P['us_GDX']
raw['ePHYS'] = P['us_PHYS'] - P['us_GLD']
raw['gdxT'] = np.log(P['o1430_GDX'] / P['close_GDX']) - bGDX * np.log(P['o1430_GLD'] / P['close_GLD'])
bT = rbeta(P['r_TRALT'], g)
raw['u'] = P['r_TRALT'] - bT * g
raw['tr3'] = P['r_TRALT'].rolling(3, min_periods=3).sum()
bM = rbeta(P['r_TRMET'], P['r_TRALT']); rel = P['r_TRMET'] - bM * P['r_TRALT']
raw['trm1'] = rel; raw['trm3'] = rel.rolling(3, min_periods=3).sum()
raw['usd'] = P['r_USDTRY']
def tech(r):
    pi = np.exp(r.fillna(0).cumsum()); ma = pi.rolling(20).mean(); sd = pi.rolling(20).std()
    return (pi - (ma - 2 * sd)) / (4 * sd), np.sign(pi - ma)
raw['pbT'], raw['maT'] = tech(P['r_TRALT']); raw['pbX'], raw['maX'] = tech(P['r_XAU'])
raw['g3'] = g.rolling(3, min_periods=3).sum(); raw['g5'] = g.rolling(5, min_periods=5).sum()
raw['eSLV'] = P['us_SLV'] - bSLV * P['us_GLD']
raw['dxy'] = P['us_DX-Y.NYB']; raw['tnx'] = P['us__TNX']; raw['tip'] = P['us_TIP']; raw['vix'] = P['us__VIX']; raw['spy'] = P['us_SPY']
for k, v in raw.items():
    sg = sigs(v) if k in ('gnight', 'gday', 'gdxT') else sig(v)
    X[k] = v / sg
X = X.replace([np.inf, -np.inf], np.nan)
SHORT = ['gnight', 'gday', 'gdxT']
ART = ['u', 'tr3', 'trm1', 'trm3', 'pbT', 'maT', 'pbX', 'maX', 'g3', 'g5']
DISC = ['eSLV', 'dxy', 'tnx', 'tip', 'vix', 'spy']
BASE = ['gnight', 'gday', 'rGLD', 'rGDX', 'rGDXJ', 'rPHYS', 'eGDX', 'eGDXJ', 'ePHYS', 'gdxT', 'u', 'tr3', 'trm1', 'trm3', 'usd', 'pbT', 'maT', 'pbX', 'maX']
GOLD_EXTRA = ['g3', 'g5']
bU = rbeta(P['r_TRALT'], P['r_XU030'])
Y = {}; elig = {}
base_ok = (~P['arife'].values) & (idx >= '2018-12-17')
for k in (1, 2, 3):
    Y[('A1', k)] = P[f'yT{k}']; Y[('A3', k)] = P[f'yT{k}'] - bT * P[f'yXa{k}']
    Y[('A2', k)] = P[f'yT{k}'] - bU * P[f'yU{k}']; Y[('B1', k)] = P[f'yX{k}']
eT = base_ok & (P['q_TRALT'].fillna(0).values > 0) & (~P['lock'].values)
eX = base_ok & (P['q_XAU'].fillna(0).values > 0)
for t in ('A1', 'A2', 'A3'): elig[t] = eT
elig['A3'] = eT & eX; elig['B1'] = eX

def nw(y, Xm, ok, L_):
    ok = ok & np.isfinite(y) & np.isfinite(Xm).all(1)
    n = int(ok.sum())
    if n < 60: return None
    Xo, yo = Xm[ok], y[ok]
    XtXi = np.linalg.pinv(Xo.T @ Xo); b = XtXi @ Xo.T @ yo
    e = yo - Xo @ b
    S = np.zeros_like(Xm); S[ok] = Xo * e[:, None]
    Om = S.T @ S
    for j in range(1, L_ + 1):
        G = S[j:].T @ S[:-j]; Om += (1 - j / (L_ + 1)) * (G + G.T)
    V = XtXi @ Om @ XtXi
    return b, np.sqrt(np.diag(V)), n
def pval(t): return math.erfc(abs(t) / math.sqrt(2))

def periods(vm, name):
    d = idx
    out = {'full': np.ones(N, bool), '<2022': d < '2022-01-01', '>=2022': d >= '2022-01-01', '>=2024': d >= '2024-01-01'}
    vd = d[vm]
    if len(vd) > 0:
        med = vd[len(vd) // 2]; out['h1'] = d < med; out['h2'] = d >= med
    if name == 'gdxT':
        out['kis'] = ~P['us_summer'].values; out['yaz'] = P['us_summer'].values
    return out

def run(pred, tgt, k, fam, xcol=None, xv=None, model=None):
    xv = X[pred].values if xv is None else xv
    y = Y[(tgt, k)].values; okb = elig[tgt]
    gz = X['gz'].values; rT = X['rTz'].values
    if model == 'g_alone': M = np.c_[np.ones(N), gz]; ci = 1
    elif model == 'g_r': M = np.c_[np.ones(N), gz, rT]; ci = 1
    elif fam == 'TRALT' and pred != 'u': M = np.c_[np.ones(N), gz, rT, xv]; ci = 3
    else: M = np.c_[np.ones(N), gz, xv]; ci = 2
    if fam == 'DISC' and tgt == 'A1': M = np.c_[np.ones(N), gz, rT, xv]; ci = 3
    if fam == 'DISC' and tgt == 'B1': M = np.c_[np.ones(N), gz, xv]; ci = 2
    vm = okb & np.isfinite(y) & np.isfinite(M).all(1)
    rows = []
    for pn, pm in periods(vm, pred).items():
        r = nw(y, M, okb & pm, k + 1)
        if r is None: continue
        b, se, n = r
        rows.append(dict(fam=fam, pred=pred, tgt=tgt, k=k, period=pn, n=n, coef=b[ci], se=se[ci], t=b[ci] / se[ci], mde=2.8 * se[ci]))
    return rows

rows = []
for tgt in ('A1', 'A3', 'A2'):
    for k in (1, 2, 3):
        rows += run('gz', tgt, k, 'TRALT', model='g_alone'); rows += run('gz_r', tgt, k, 'TRALT', model='g_r', xv=None) if False else []
for tgt in ('A1', 'A3', 'A2'):
    for k in (1, 2, 3):
        for r in run('gz', tgt, k, 'TRALT', model='g_r'):
            r['pred'] = 'g|r'; rows.append(r)
for k in (1, 2, 3):
    rows += run('gz', 'B1', k, 'GOLD', model='g_alone')
for tgt in ('A1', 'A3', 'A2'):
    for k in (1, 2, 3):
        for p in BASE: rows += run(p, tgt, k, 'TRALT')
for k in (1, 2, 3):
    for p in BASE + GOLD_EXTRA: rows += run(p, 'B1', k, 'GOLD')
for tgt in ('A1', 'B1'):
    for k in (1, 2, 3):
        for p in DISC: rows += run(p, tgt, k, 'DISC')
T = pd.DataFrame(rows)
# FDR / Bonferroni: tam donem satirlari, aile = TRALT (A1,A3), GOLD (B1), DISC; A2 ve g-alone aileye dahil degil (kiyas)
T['q'] = np.nan; T['bonf'] = np.nan; T['p'] = T['t'].apply(pval)
fam_mask = {'TRALT': T['tgt'].isin(['A1', 'A3']) & (T['pred'] != 'g|r') & (T['pred'] != 'gz'),
            'GOLD': (T['fam'] == 'GOLD'), 'DISC': (T['fam'] == 'DISC')}
# g tek basina: aileye dahil (TRALT icin g|r, GOLD icin gz)
fam_mask['TRALT'] = T['fam'].eq('TRALT') & T['tgt'].isin(['A1', 'A3']) & (T['pred'] != 'gz')
FAMN = {}
for f, m in fam_mask.items():
    m = m & (T['period'] == 'full'); ii = T.index[m]
    p = T.loc[ii, 'p'].values; mm = len(p); FAMN[f] = mm
    o = np.argsort(p); q = np.empty(mm); prev = 1.0
    for r_, j in enumerate(o[::-1]):
        rank = mm - r_; prev = min(prev, p[j] * mm / rank); q[j] = prev
    T.loc[ii, 'q'] = q; T.loc[ii, 'bonf'] = np.minimum(1, p * mm)
L('aile test sayilari (tam donem)', FAMN)
def sgn(x): return np.sign(x)
dec = []
for (fam, pred, tgt, k), gdf in T.groupby(['fam', 'pred', 'tgt', 'k']):
    G = gdf.set_index('period'); f = G.loc['full']
    if pd.isna(f['q']): continue
    cond1 = abs(f['t']) >= 3 or (abs(f['t']) >= 2 and f['q'] <= 0.10)
    short = pred in SHORT
    if not short:
        try:
            c2 = sgn(G.loc['<2022', 'coef']) == sgn(G.loc['>=2022', 'coef']) == sgn(f['coef']) and abs(G.loc['>=2022', 't']) >= 1.5
            c3 = sgn(G.loc['>=2024', 'coef']) == sgn(f['coef'])
        except KeyError: c2 = c3 = False
    else:
        try: c2 = sgn(G.loc['h1', 'coef']) == sgn(G.loc['h2', 'coef']) == sgn(f['coef']); c3 = True
        except KeyError: c2 = c3 = False
    ok = bool(cond1 and c2 and c3)
    d_ = 'gecti' if ok else ('yetersiz guc' if (short and f['mde'] > 10) else 'gecmedi')
    dec.append(dict(fam=fam, pred=pred, tgt=tgt, k=k, n=f['n'], coef=f['coef'], t=f['t'], q=f['q'], bonf=f['bonf'], mde=f['mde'], karar=d_))
D = pd.DataFrame(dec)
T.round(4).to_csv(OUT + '/regresyon_tam_tablo.csv', index=False)
D.round(4).to_csv(OUT + '/karar_tablosu.csv', index=False)
L('Karar sayilari:', D.groupby(['fam', 'karar']).size().to_dict())
L('GECENLER'); L(D[D.karar == 'gecti'].round(3).to_string())
L('Aile basina en yuksek |t| (tam, A1/A3/B1 aileleri, A2 haric):')
top = D[D.tgt != 'A2'].assign(at=lambda x: x.t.abs()).sort_values('at', ascending=False).head(28)
L(top.drop(columns='at').round(3).to_string())
L('G tek basina (tam donem):')
L(T[(T.pred.isin(['gz', 'g|r'])) & (T.period.isin(['full', '<2022', '>=2022', '>=2024']))].pivot_table(index=['pred', 'tgt', 'k'], columns='period', values='t').round(2).to_string())
L('Kisa orneklem satirlari (tam):')
L(D[D.pred.isin(SHORT)].round(3).to_string())
L('gdxT kis/yaz:'); L(T[(T.pred == 'gdxT') & T.period.isin(['kis', 'yaz', 'h1', 'h2'])].pivot_table(index=['fam', 'tgt', 'k'], columns='period', values=['coef', 't']).round(2).to_string())

# ---- artefakt kontrolu (t-1 degerleriyle)
ar = []
for fam, tg, plist in (('TRALT', ['A1', 'A3'], [p for p in ART if p not in ('g3', 'g5')]), ('GOLD', ['B1'], ART)):
    for tgt in tg:
        for k in (1, 2, 3):
            for p in plist:
                a = [r for r in run(p, tgt, k, fam) if r['period'] == 'full'][0]
                xl = X[p].shift(1).values
                b = [r for r in run(p, tgt, k, fam, xv=xl) if r['period'] == 'full'][0]
                ar.append(dict(fam=fam, pred=p, tgt=tgt, k=k, coef_t=a['coef'], t_t=a['t'], coef_t1=b['coef'], t_t1=b['t'], isaret_degisti=bool(np.sign(a['coef']) != np.sign(b['coef']))))
A = pd.DataFrame(ar); A.round(3).to_csv(OUT + '/artefakt_kontrolu.csv', index=False)
L('ARTEFAKT: t-1 ile isaret degisen satir', int(A.isaret_degisti.sum()), '/', len(A))
L(A.pivot_table(index=['fam', 'pred'], columns=['tgt', 'k'], values='t_t', aggfunc='first').round(2).to_string())
L(A.pivot_table(index=['fam', 'pred'], columns=['tgt', 'k'], values='t_t1', aggfunc='first').round(2).to_string())

# ---- islem kurali (gecenler)
dates = idx; yrs = (pd.Timestamp('2026-11-09') - pd.Timestamp('2018-12-17')).days / 365.25
COST = {'A1': (8, 23), 'A3': (8, 23), 'B1': (3, 10)}
def engine(sig_dir, y, cost_extra, tgt, lo_hi, kk=2):
    ci = lo_hi
    c0 = COST[tgt][ci]
    take = []; i = 0
    while i < N:
        if sig_dir[i] != 0 and np.isfinite(y[i]) and elig[tgt][i]:
            take.append(i); i += kk
        else: i += 1
    take = np.array(take, int)
    if len(take) == 0: return take, np.array([]), np.array([])
    gross = sig_dir[take] * y[take]
    net = gross - c0 - (cost_extra[take] * (3, 10)[ci] if cost_extra is not None else 0)
    return take, gross, net
def tstat(x): return x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 and x.std(ddof=1) > 0 else np.nan
passers = D[D.karar == 'gecti']
strat = []
rng = np.random.default_rng(1)
done = set()
for _, pr in passers.iterrows():
    if pr.tgt not in COST: continue
    key = (pr.pred, pr.tgt)
    if key in done: continue
    done.add(key)
    pname = 'gz' if pr.pred in ('g|r',) else pr.pred
    xv = X[pname].values
    dsg = np.sign(pr.coef)
    sd = np.where(np.abs(xv) > 1, np.sign(xv) * dsg, 0.0); sd[~np.isfinite(xv)] = 0
    for kk in (1, 2, 3):
        y = Y[(pr.tgt, kk)].values
        ce = np.abs(bT.values) if pr.tgt == 'A3' else None
        res = {'pred': pr.pred, 'tgt': pr.tgt, 'k': kk}
        for ci, nm in ((0, 'dusuk'), (1, 'bireysel')):
            take, gr, net = engine(sd, y, ce, pr.tgt, ci, kk)
            res['n'] = len(take); res['yilda'] = len(take) / yrs
            res['brut'] = gr.mean(); res['net_' + nm] = net.mean(); res['t_' + nm] = tstat(net); res['isabet_' + nm] = (net > 0).mean()
            if ci == 1:
                dd_ = dates[take]
                for nmr, a_, b_ in (('r1920', '2019', '2020'), ('r2123', '2021', '2023'), ('r2426', '2024', '2026')):
                    m = (dd_ >= a_ + '-01-01') & (dd_ <= b_ + '-12-31'); res['net_' + nmr] = net[m].mean() if m.sum() else np.nan; res['n_' + nmr] = int(m.sum())
                cut = int(np.ceil(0.02 * len(net))); res['net_en_iyi2pct_haric'] = np.sort(net)[:-cut].mean()
                s_ = sd[take]; res['net_long'] = net[s_ > 0].mean(); res['n_long'] = int((s_ > 0).sum()); res['net_short'] = net[s_ < 0].mean(); res['n_short'] = int((s_ < 0).sum())
                obs = net.mean(); cnt = 0; shifts = rng.integers(20, N - 20, 500)
                for s in shifts:
                    _, _, n2 = engine(np.roll(sd, s), y, ce, pr.tgt, 1, kk)
                    if len(n2) and n2.mean() >= obs: cnt += 1
                res['plasebo_p'] = (cnt + 1) / 501
        ok = elig[pr.tgt] & np.isfinite(y); res['taban_long'] = np.nanmean(y[ok])
        strat.append(res)
S = pd.DataFrame(strat)
S.round(3).to_csv(OUT + '/islem_kurali.csv', index=False)
L('ISLEM KURALI (k=1,2,3, |z|>1, orttusmesiz)'); L(S.round(2).to_string() if len(S) else 'gecen yok')
L('KOSULSUZ TABAN (her zaman long, ort bps; tum/19-20/21-23/24-26):')
for tgt in ('A1', 'A3', 'B1'):
    for k in (1, 2, 3):
        y = Y[(tgt, k)].values; ok = elig[tgt] & np.isfinite(y)
        parts = [np.nanmean(y[ok])] + [np.nanmean(y[ok & (idx >= a) & (idx <= b)]) for a, b in (('2019', '2020-12-31'), ('2021', '2023-12-31'), ('2024', '2026-12-31'))]
        L(tgt, k, int(ok.sum()), np.round(parts, 1))
L('ornek n', int((idx >= '2018-12-17').sum()), 'gz dolu', int(X['gz'][idx >= '2018-12-17'].notna().sum()))

L('GECENLERIN DONEM t-degerleri:')
for _, pr in D[D.karar == 'gecti'].iterrows():
    L(T[(T.pred == pr.pred) & (T.tgt == pr.tgt) & (T.k == pr.k)][['period', 'n', 'coef', 't']].round(2).to_string())
