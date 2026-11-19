#!/usr/bin/env python3
"""Havacilik-savunma / DXY analizi: M0-M6 tablolari ve G1-G9 grafikleri.
Kullanim: python3 hesap/02_analiz.py   (rastgelelik yok; ek veri varsa yeniden indirilmez)"""
import os, re, io, json, glob, warnings, urllib.request
import numpy as np, pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from statsmodels.tsa.api import VAR
from scipy import stats
warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = f'{ROOT}/veri'; GR = f'{ROOT}/grafik'; H = f'{ROOT}/hesap'
os.makedirs(GR, exist_ok=True)
R = {}            # sonuclar.json
MD = []           # sonuclar.md
SAPMA = []        # yapilamayanlar ve sapmalar
LN10 = np.log(1.10)

def md_table(df, fmt=3):
    df = df.copy()
    def f(x):
        if isinstance(x, (float, np.floating)):
            if np.isnan(x): return ''
            return f'{x:.{fmt}f}'
        return str(x)
    cols = list(df.columns)
    out = ['| ' + ' | '.join(map(str, cols)) + ' |', '|' + '---|' * len(cols)]
    for _, r in df.iterrows():
        out.append('| ' + ' | '.join(f(r[c]) for c in cols) + ' |')
    return '\n'.join(out)

def sec(title, summary):
    MD.append(f'\n## {title}\n\n{summary}\n')

# ------------------------------------------------------------------ ek indirme
def fetch(url, path, binary=True):
    if os.path.exists(path) and os.path.getsize(path) > 1000: return True
    for _ in range(3):
        try:
            data = urllib.request.urlopen(url, timeout=90).read()
            open(path, 'wb').write(data); return True
        except Exception as e:
            err = e
    SAPMA.append(f'Indirme basarisiz: {url} ({err})'); return False

fetch('https://www.federalreserve.gov/releases/g17/ipdisk/ip_sa.txt', f'{V}/fed_g17_ip_sa.txt')
fetch('https://stats.bis.org/api/v2/data/dataflow/BIS/WS_EER/1.0/M.N.B.US?format=csv', f'{V}/bis_eer_us_broad.csv')
if not os.path.exists(f'{V}/eurostat_imalat_C.csv'):
    import json as _j
    rows = []
    for g in ['FR', 'DE', 'EU27_2020']:
        u = f'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_inpr_m?format=JSON&geo={g}&nace_r2=C&s_adj=SCA&unit=I21'
        j = _j.loads(urllib.request.urlopen(u, timeout=90).read())
        inv = {v: k for k, v in j['dimension']['time']['category']['index'].items()}
        rows += [(inv[int(k)], g, v) for k, v in j['value'].items()]
    pd.DataFrame(rows, columns=['donem', 'geo', 'endeks_2021_100']).sort_values(['geo', 'donem']).to_csv(f'{V}/eurostat_imalat_C.csv', index=False)

# ------------------------------------------------------------------ veri yukleme
d = pd.read_csv(f'{V}/yahoo_gunluk.csv', parse_dates=['tarih'])
ADJ = d.pivot(index='tarih', columns='ticker', values='adjclose').sort_index()
CLS = d.pivot(index='tarih', columns='ticker', values='close').sort_index()
DXYd = CLS['DX-Y.NYB'].dropna()
ym = pd.read_csv(f'{V}/yahoo_aylik.csv'); ym['ay'] = pd.PeriodIndex(ym['ay'], freq='M'); ym = ym.set_index('ay')
ms = pd.read_csv(f'{V}/msci_aylik.csv', parse_dates=['tarih'])
def msci(kod, para):
    s = ms[(ms.kod.astype(str) == str(kod)) & (ms.para == para) & (ms.varyant == 'NETR')].set_index('tarih')['seviye'].sort_index()
    return s
MSW_USD = msci(990100, 'USD'); MSE_USD = msci(990500, 'USD'); MSE_EUR = msci(990500, 'EUR')
MAD_USD = msci(763669, 'USD'); MAD_EUR = msci(763669, 'EUR')
fed = pd.read_csv(f'{V}/fed_ip_havacilik.csv', parse_dates=['tarih'])
FED = fed.pivot(index='tarih', columns='seri', values='deger'); FED.index = FED.index.to_period('M')
# G.17 imalat (GMF)
gm = {}
for line in open(f'{V}/fed_g17_ip_sa.txt', errors='ignore'):
    m = re.match(r'^"GMF"\s+(\d{4})\s+(.*)$', line)
    if m:
        for i, v in enumerate(m.group(2).split()):
            try: gm[pd.Period(f'{m.group(1)}-{i+1:02d}', 'M')] = float(v)
            except ValueError: pass
GMF = pd.Series(gm).sort_index()
es_c303 = pd.read_csv(f'{V}/eurostat_c303.csv'); es_c = pd.read_csv(f'{V}/eurostat_imalat_C.csv')
def es_series(df, geo):
    s = df[df.geo == geo].set_index('donem')['endeks_2021_100']; s.index = pd.PeriodIndex(s.index, freq='M'); return s.sort_index()
ab = pd.read_csv(f'{V}/airbus_boeing_yillik.csv').set_index('yil')
tg = pd.read_csv(f'{V}/teslimat_hedef.csv'); tg['yil'] = tg['yil'].astype(str).str[:4].astype(int)
bis = pd.read_csv(f'{V}/bis_eer_us_broad.csv'); bis = bis.set_index(pd.PeriodIndex(bis['TIME_PERIOD'], freq='M'))['OBS_VALUE']

# ------------------------------------------------------------------ M0 hazirlik
DXYm = DXYd.groupby(DXYd.index.to_period('M')).mean()
DXYq = DXYd.groupby(DXYd.index.to_period('Q')).mean()
DXYy = DXYd.groupby(DXYd.index.year).mean()
dlnY_dxy = np.log(DXYy).diff()
BISy = bis.groupby(bis.index.year).mean(); BISy = BISy[BISy.index <= 2025]; dlnBIS = np.log(BISy).diff()

REC = [('1973-11', '1975-03'), ('1980-01', '1980-07'), ('1981-07', '1982-11'), ('1990-07', '1991-03'),
       ('2001-03', '2001-11'), ('2007-12', '2009-06'), ('2020-02', '2020-04')]
recM = pd.Series(0, index=pd.period_range('1970-01', '2026-12', freq='M'))
for a, b in REC: recM[pd.Period(a, 'M'):pd.Period(b, 'M')] = 1
recY = (recM.groupby(recM.index.year).sum() >= 3).astype(int)
recQ = (recM.groupby(recM.index.asfreq('Q')).sum() >= 2).astype(int)

LASTY = 2025
dl_ = ab['airbus_teslimat']; db_ = ab['boeing_teslimat']; oa = ab['airbus_net_siparis']; ob = ab['boeing_net_siparis']
act = {'Airbus': tg[tg.uretici == 'Airbus'].set_index('yil')['backlog_yilsonu'],
       'Boeing': tg[tg.uretici == 'Boeing'].set_index('yil')['backlog_yilsonu']}
dd = {'Airbus': dl_, 'Boeing': db_}; oo = {'Airbus': oa, 'Boeing': ob}
Brec = {}; chk_rows = []
for u in ['Airbus', 'Boeing']:
    B = {y: float(act[u][y]) for y in range(2018, 2026)}
    for y in range(2017, 1972, -1):
        B[y] = B[y + 1] - oo[u][y + 1] + dd[u][y + 1]
    Brec[u] = pd.Series(B).sort_index()
    for y in range(2019, 2026):
        pred = act[u][y - 1] + oo[u][y] - dd[u][y]
        chk_rows.append([u, y, act[u][y], pred, act[u][y] - pred])
chk = pd.DataFrame(chk_rows, columns=['uretici', 'yil', 'gercek_birikim', 'kimlik_tahmini', 'fark'])
bad = [y for y in range(1973, 2018) if min(Brec['Airbus'][y], Brec['Boeing'][y]) <= 0]
START_B = (max(bad) + 1) if bad else 1973
neg_info = f'Geriye kurulan birikim <=0 olan yillar (en az biri): {bad if bad else "yok"}; kullanilan baslangic: {START_B}.'
Btot = (Brec['Airbus'] + Brec['Boeing']).loc[START_B:LASTY]
Dtot = (dl_ + db_); Otot = (oa + ob)
ratio = (Btot / Dtot.loc[START_B:LASTY])
Y5 = (Otot / Btot.shift(1)).loc[START_B + 1:LASTY]
Brec_df = pd.DataFrame({'Airbus_birikim': Brec['Airbus'], 'Boeing_birikim': Brec['Boeing']}).loc[1973:2025]
ratio_ab = {u: Brec[u] / dd[u] for u in dd}

sec('M0. Hazirlik: birikim yeniden kurulumu',
    f'Sipariş birikimi 2018 gerçek yıl sonu değerinden geriye B(t-1)=B(t)-net_sipariş(t)+teslimat(t) ile kuruldu. '
    f'Kimliğin 2019-2025 gerçek birikimle farkı aşağıda; ASC 606 vb. düzeltmeler farkı oluşturur. {neg_info}')
MD.append('Kimlik kontrolu (gercek birikim - [onceki gercek + siparis - teslimat]):\n\n' + md_table(chk, 0))
MD.append('\nGeriye kurulan toplam birikim ve birikim/teslimat orani (secilen donem):\n\n' +
          md_table(pd.DataFrame({'yil': Btot.index, 'toplam_birikim': Btot.values, 'toplam_teslimat': Dtot.loc[START_B:LASTY].values, 'oran': ratio.values}), 2))
R['M0'] = {'baslangic_birikim': int(START_B), 'negatif_yillar': [int(b) for b in bad],
           'kimlik_ort_mutlak_fark': {u: float(chk[chk.uretici == u].fark.abs().mean()) for u in ['Airbus', 'Boeing']},
           'kimlik_fark': chk.to_dict('records')}

# ------------------------------------------------------------------ yardimci: dagitilmis gecikme
def dl(y, x, kmax, ctrl=None, maxlags=3, level=False):
    df = pd.DataFrame({'y': y})
    for k in range(kmax + 1): df[f'L{k}'] = x.shift(k)
    if ctrl is not None: df = df.join(ctrl, how='left')
    df = df.dropna()
    X = df.drop(columns='y')
    keep = [c for c in X.columns if c.startswith('L') or X[c].std() > 0]
    X = sm.add_constant(X[keep], has_constant='add')
    res = sm.OLS(df['y'], X).fit(cov_type='HAC', cov_kwds={'maxlags': maxlags})
    cols = list(X.columns); Ls = [f'L{k}' for k in range(kmax + 1)]
    Rv = np.zeros(len(cols)); Rm = np.zeros((len(Ls), len(cols)))
    for i, n in enumerate(Ls): Rv[cols.index(n)] = 1; Rm[i, cols.index(n)] = 1
    b = res.params[Ls].values; V_ = np.asarray(res.cov_params()); se_tot = float(np.sqrt(Rv @ V_ @ Rv)); tot = float(Rv @ res.params.values)
    lo, hi = tot - 1.96 * se_tot, tot + 1.96 * se_tot
    pw = float(res.wald_test(Rv.reshape(1, -1), scalar=True).pvalue)
    pf = float(res.wald_test(Rm, use_f=True, scalar=True).pvalue)
    if level: eff = [tot * LN10 * 100, lo * LN10 * 100, hi * LN10 * 100]
    else: eff = [(np.exp(t * LN10) - 1) * 100 for t in (tot, lo, hi)]
    return dict(n=int(res.nobs), b=[float(v) for v in b], toplam=tot, se=se_tot, ga=[lo, hi], etki10=eff[0], etki10_ga=[eff[1], eff[2]],
                wald_p=pw, ortak_F_p=pf, r2=float(res.rsquared), bas=str(df.index[0]), son=str(df.index[-1]))

# ------------------------------------------------------------------ M1
Ys = {'Y1 dln toplam teslimat': np.log(Dtot.loc[:LASTY]).diff(),
      'Y2 dln Airbus teslimat': np.log(dl_.loc[:LASTY]).diff(),
      'Y3 dln Boeing teslimat': np.log(db_.loc[:LASTY]).diff(),
      'Y4 dln birikim/teslimat': np.log(ratio).diff(),
      'Y5 siparis yogunlugu (duzey)': Y5}
dlnGMFy = np.log(GMF.groupby(GMF.index.year).mean()[lambda s: s.index <= 2025]).diff()
EVY = [1995, 1997, 2001, 2002, 2005, 2008, 2009, 2019, 2020, 2021, 2024]
def ctrl_ii(): return pd.DataFrame({'resesyon': recY, 'dln_imalat': dlnGMFy})
def ctrl_iii():
    c = ctrl_ii()
    for e in EVY: c[f'ev{e}'] = (c.index == e).astype(int)
    return c
VARS = {'(i) kontrolsuz': lambda: None, '(ii) +resesyon+imalat': ctrl_ii, '(iii) +olay yili': ctrl_iii}
m1 = []; m1rows = []
for yn, y in Ys.items():
    for vn, cf in VARS.items():
        r = dl(y, dlnY_dxy, 3, cf(), 3, level=yn.startswith('Y5'))
        m1.append((yn, vn, r))
        m1rows.append([yn.split()[0], vn, r['n'], *[round(v, 3) for v in r['b']], r['toplam'], f"[{r['ga'][0]:.3f}, {r['ga'][1]:.3f}]",
                       r['etki10'], f"[{r['etki10_ga'][0]:.1f}, {r['etki10_ga'][1]:.1f}]", r['wald_p'], r['ortak_F_p'], r['r2']])
m1df = pd.DataFrame(m1rows, columns=['Y', 'varyant', 'n', 'b0', 'b1', 'b2', 'b3', 'toplam_b', '%95 GA', 'DXY+10% etki (%; Y5: yuzde puan)', 'GA (etki)', 'Wald p', 'ortak F p', 'R2'])
bh_m1 = multipletests([r['wald_p'] for _, _, r in m1], method='fdr_bh')[1]
m1df['BH p (15 test)'] = bh_m1
n_sig_m1 = int((bh_m1 < 0.05).sum()); n_raw_m1 = int(sum(r['wald_p'] < 0.05 for _, _, r in m1))
sec('M1. Yillik dagitilmis gecikme modeli (OLS, Newey-West maxlags=3)',
    f'Y_t = a + toplam_k=0..3 b_k dln(DXY)_(t-k) + kontroller; 5 bagimli degisken x 3 varyant = 15 model. Toplam etki Wald p<0.05 olan: {n_raw_m1}/15; BH duzeltmesi sonrasi q<0.05: {n_sig_m1}/15. '
    f'Y5 duzey degiskenidir (etki yuzde puan); Y1-Y4 log farkidir (etki yuzde).')
MD.append(md_table(m1df, 3))
R['M1'] = {f'{yn}|{vn}': r for yn, vn, r in m1}
R['M1_bh'] = {'ham_anlamli': n_raw_m1, 'bh_anlamli': n_sig_m1, 'test_sayisi': 15}

# kararlilik: alt donemler (ii)
sub = []
for yn, y in Ys.items():
    for lab, (a, b) in {'1978-1999': (1978, 1999), '2000-2025': (2000, 2025)}.items():
        r = dl(y.loc[a:b] if True else y, dlnY_dxy, 3, ctrl_ii(), 3, level=yn.startswith('Y5'))
        # gecikmeler icin onceki yillar kullanilsin: x'i tam seriden kaydirip y'yi kes
        df_y = y[(y.index >= a) & (y.index <= b)]
        r = dl(df_y, dlnY_dxy, 3, ctrl_ii(), 3, level=yn.startswith('Y5'))
        sub.append([yn.split()[0], lab, r['n'], r['toplam'], f"[{r['ga'][0]:.3f}, {r['ga'][1]:.3f}]", r['etki10'], r['wald_p'], r['ortak_F_p'], r['r2']])
        R.setdefault('M1_alt', {})[f"{yn.split()[0]}|{lab}"] = r
MD.append('\n**Alt donemler, varyant (ii):**\n\n' + md_table(pd.DataFrame(sub, columns=['Y', 'donem', 'n', 'toplam_b', 'GA', 'etki10', 'Wald p', 'ortak F p', 'R2']), 3))
# kayan 20 yil
roll = []
for yn in list(Ys)[:3]:
    y = Ys[yn]
    for s in range(1978, LASTY - 19 + 1):
        r = dl(y[(y.index >= s) & (y.index <= s + 19)], dlnY_dxy, 3, ctrl_ii(), 3)
        roll.append([yn.split()[0], f'{s}-{s+19}', r['n'], r['etki10'], r['wald_p']])
rdf = pd.DataFrame(roll, columns=['Y', 'pencere', 'n', 'etki10 (%)', 'Wald p'])
R['M1_kayan20'] = {y: {'min': float(g['etki10 (%)'].min()), 'maks': float(g['etki10 (%)'].max()), 'medyan': float(g['etki10 (%)'].median()),
                        'pozitif_pencere': int((g['etki10 (%)'] > 0).sum()), 'toplam': int(len(g)), 'p_lt_005': int((g['Wald p'] < 0.05).sum())}
                   for y, g in rdf.groupby('Y')}
MD.append('\n**20 yillik kayan pencere (yalniz betimsel; varyant ii, Y1-Y3; her 3. pencere gosterilir, tamami sonuclar.json ozetinde):**\n\n' +
          md_table(rdf.iloc[::3].reset_index(drop=True), 3))
# BIS saglamlik
bisr = []
for yn in list(Ys)[:3]:
    r = dl(Ys[yn][Ys[yn].index >= 1995], dlnBIS, 3, ctrl_ii(), 3)
    r0 = dl(Ys[yn][Ys[yn].index >= 1995], dlnY_dxy, 3, ctrl_ii(), 3)
    bisr.append([yn.split()[0], r['n'], r['etki10'], f"[{r['etki10_ga'][0]:.1f}, {r['etki10_ga'][1]:.1f}]", r['wald_p'], r0['etki10'], r0['wald_p']])
    R.setdefault('M1_BIS', {})[yn.split()[0]] = {'bis': r, 'dxy_ayni_ornek': r0}
MD.append('\n**Saglamlik: BIS ABD genis nominal efektif kur (WS_EER, M.N.B.US) yillik ort., varyant (ii), 1995-2025:**\n\n' +
          md_table(pd.DataFrame(bisr, columns=['Y', 'n', 'BIS +10% etki (%)', 'GA', 'Wald p', 'ayni orneklemde DXY etki (%)', 'DXY Wald p']), 3))

# korelasyon tablosu
cr = []
for yn, y in Ys.items():
    for k in range(6):
        df = pd.DataFrame({'y': y, 'x': dlnY_dxy.shift(k)}).dropna()
        pr = stats.pearsonr(df.x, df.y); sr = stats.spearmanr(df.x, df.y)
        cr.append([yn.split()[0], k, len(df), pr[0], pr[1], sr[0], sr[1]])
cdf = pd.DataFrame(cr, columns=['Y', 'k', 'n', 'Pearson r', 'Pearson p', 'Spearman rho', 'Spearman p'])
allp = np.r_[cdf['Pearson p'].values, cdf['Spearman p'].values]
bhp = multipletests(allp, method='fdr_bh')[1]
cdf['Pearson BH p'] = bhp[:len(cdf)]; cdf['Spearman BH p'] = bhp[len(cdf):]
NT = len(allp); n_raw_c = int((allp < 0.05).sum()); n_bh_c = int((bhp < 0.05).sum())
sec('M1b. Basit korelasyon (Y_t ile dln DXY_(t-k), k=0..5)',
    f'Toplam test sayisi {NT} (5 Y x 6 gecikme x Pearson ve Spearman). Ham p<0.05: {n_raw_c}/{NT}; BH sonrasi q<0.05: {n_bh_c}/{NT}.')
MD.append(md_table(cdf, 3))
R['M1_korelasyon'] = {'test_sayisi': NT, 'ham_anlamli': n_raw_c, 'bh_anlamli': n_bh_c, 'tablo': cdf.to_dict('records')}
# guc
def mdr(n): return float(np.tanh((stats.norm.ppf(0.975) + stats.norm.ppf(0.8)) / np.sqrt(n - 3)))
pw = pd.DataFrame({'n': sorted(set(cdf.n))}); pw['en kucuk saptanabilir |r| (%80 guc, alfa 0.05)'] = pw.n.map(mdr)
MD.append('\n**Guc (Fisher z):** "anlamsiz" = "iliski yok" degildir; GA\'lara bakiniz.\n\n' + md_table(pw, 3))
R['M1_guc'] = {int(n): mdr(n) for n in pw.n}

# ------------------------------------------------------------------ M2 ceyreklik
def q_mean(s):  # PeriodIndex M serisi -> ceyreklik ortalama (tam ceyrekler)
    g = s.groupby(s.index.asfreq('Q')); m = g.mean(); c = g.count(); return m[c == 3]
AC = q_mean(FED['G336411T3']); AC_def = q_mean(FED['G3364']); dAC = np.log(AC).diff(); dACd = np.log(AC_def).diff()
dX = np.log(DXYq).diff(); dX.index = DXYq.index
GMFq = q_mean(GMF); dGMFq = np.log(GMFq).diff()
ctrlq = pd.DataFrame({'resesyon': recQ, 'dln_imalat': dGMFq})
m2 = []
def run_q(name, y, ctrl, a, b, excl=False):
    yy = y[(y.index >= pd.Period(a, 'Q')) & (y.index <= pd.Period(b, 'Q'))]
    if excl:
        yy = yy[~((yy.index >= pd.Period('2019Q1')) & (yy.index <= pd.Period('2021Q4')))]
    r = dl(yy, dX, 8, ctrl, 12)
    m2.append([name, f'{a}-{b}' + (' (2019Q1-2021Q4 haric)' if excl else ''), r['n'], r['toplam'], f"[{r['ga'][0]:.3f}, {r['ga'][1]:.3f}]", r['etki10'], f"[{r['etki10_ga'][0]:.1f}, {r['etki10_ga'][1]:.1f}]", r['wald_p'], r['ortak_F_p'], r['r2']])
    R.setdefault('M2', {})[m2[-1][0] + '|' + m2[-1][1]] = r
    return r
for (a, b, ex) in [('1973Q1', '2026Q3', False), ('1973Q1', '1999Q4', False), ('2000Q1', '2026Q3', False), ('1973Q1', '2026Q3', True)]:
    run_q('ABD G336411T3', dAC, ctrlq, a, b, ex)
run_q('ABD G3364 (saglamlik)', dACd, ctrlq, '1973Q1', '2026Q3')
for geo in ['FR', 'DE', 'EU27_2020']:
    y = np.log(q_mean(es_series(es_c303, geo))).diff(); c = pd.DataFrame({'dln_imalat': np.log(q_mean(es_series(es_c, geo))).diff()})
    run_q(f'Eurostat C30.3 {geo}', y, c, '1990Q1', '2026Q3')
    run_q(f'Eurostat C30.3 {geo}', y, c, '1990Q1', '2026Q3', True)
m2df = pd.DataFrame(m2, columns=['model', 'donem', 'n', 'toplam_b', 'GA', 'DXY+10% etki (%)', 'GA (etki)', 'Wald p', 'ortak F p', 'R2'])
m2df['BH p'] = multipletests(m2df['Wald p'], method='fdr_bh')[1]
sec('M2. Ceyreklik uretim modeli (gecikme 0-8, HAC maxlags=12)',
    f'Y = dln ceyreklik ort. G336411T3 (ABD) ve Eurostat C30.3; X = dln ceyreklik ort. DXY, gecikme 0..8; kontrol: imalat uretimi (eszamanli; ABD icin ayrica resesyon kuklasi). '
    f'{len(m2df)} modelden Wald p<0.05: {int((m2df["Wald p"]<0.05).sum())}; BH sonrasi: {int((m2df["BH p"]<0.05).sum())}.')
MD.append(md_table(m2df, 3))
R['M2_sayim'] = {'model': len(m2df), 'ham': int((m2df['Wald p'] < 0.05).sum()), 'bh': int((m2df['BH p'] < 0.05).sum())}
# Granger
gr = []
for nm, yser in [('G336411T3', dAC), ('G3364', dACd)]:
    dfv = pd.DataFrame({'y': yser, 'x': dX}).dropna()
    dfv = dfv[dfv.index >= pd.Period('1973Q1', 'Q')]
    dfv.index = dfv.index.to_timestamp()
    res = VAR(dfv).fit(maxlags=8, ic='aic'); p = max(res.k_ar, 1)
    if res.k_ar == 0: res = VAR(dfv).fit(1)
    g1 = res.test_causality('y', ['x'], kind='f'); g2 = res.test_causality('x', ['y'], kind='f')
    gr.append([nm, p, 'DXY -> uretim', g1.pvalue]); gr.append([nm, p, 'uretim -> DXY', g2.pvalue])
grdf = pd.DataFrame(gr, columns=['seri', 'VAR gecikme (AIC)', 'yon', 'Granger F p'])
MD.append('\n**Granger nedensellik (ikincil kanit; ceyreklik VAR [dln uretim, dln DXY], 1973Q2-2026Q3):**\n\n' + md_table(grdf, 4))
R['M2_granger'] = grdf.to_dict('records')
MD.append('\n**G.17 kaynak turu (G336411T3):** Fed G.17 genel metodoloji sayfasi (about.htm): fiziksel urun verisi varsa o, yoksa uretim-isci saatleri kullanilir. G336411T3 icin ozel aciklama (fiziksel birim mi isci saati mi) kontrol edilen 3 sayfada BULUNAMADI.')

# ------------------------------------------------------------------ M3 vaka tablosu
yoy = (DXYm / DXYm.shift(12) - 1).dropna()
flag = pd.Series(np.where(yoy > .10, 1, np.where(yoy < -.10, -1, 0)), index=yoy.index)
eps = []; cur = None
for p, f in flag.items():
    if f != 0:
        if cur and cur['f'] == f and p == cur['end'] + 1: cur['end'] = p; cur['vals'].append(yoy[p])
        else:
            if cur: eps.append(cur)
            cur = {'f': f, 'start': p, 'end': p, 'vals': [yoy[p]]}
    else:
        if cur: eps.append(cur); cur = None
if cur: eps.append(cur)
Dy = Dtot.loc[:LASTY]; Ry = ratio
def pct(s, a, b):
    try: return float((s[b] / s[a] - 1) * 100) if (a in s.index and b in s.index) else np.nan
    except KeyError: return np.nan
def mpct(s, p, h):
    q = p + h
    return float((s[q] / s[p] - 1) * 100) if (p in s.index and q in s.index) else np.nan
case = []
acm = FED['G336411T3']
for e in eps:
    E = e['end'].year; ext = max(e['vals']) if e['f'] > 0 else min(e['vals'])
    case.append([f"{e['start']}..{e['end']}", 'guclenme' if e['f'] > 0 else 'zayiflama', ext * 100,
                 pct(Dy, E, E + 1), pct(Dy, E + 1, E + 2), pct(Ry, E, E + 1), pct(Ry, E + 1, E + 2),
                 mpct(acm, e['end'], 12), mpct(acm, e['end'], 24)])
allD = [pct(Dy, t - 1, t) for t in range(1975, 2026)]
allR = [pct(Ry, t - 1, t) for t in Ry.index[1:]]
a12 = [mpct(acm, p, 12) for p in acm.index]; a24 = [mpct(acm, p, 24) for p in acm.index]
def nm_(x, f): x = [v for v in x if not np.isnan(v)]; return float(f(x))
case.append(['TUM DONEM ortalama', '-', np.nan, nm_(allD, np.mean), nm_(allD, np.mean), nm_(allR, np.mean), nm_(allR, np.mean), nm_(a12, np.mean), nm_(a24, np.mean)])
case.append(['TUM DONEM medyan', '-', np.nan, nm_(allD, np.median), nm_(allD, np.median), nm_(allR, np.median), nm_(allR, np.median), nm_(a12, np.median), nm_(a24, np.median)])
cdfm = pd.DataFrame(case, columns=['bolum', 'yon', 'en uc 12a degisim (%)', 'teslimat izleyen 1. yil (%)', 'teslimat 2. yil (%)', 'birikim/tesl. 1. yil (%)', '2. yil (%)', 'G336411T3 +12 ay (%)', '+24 ay (%)'])
sec('M3. Vaka tablosu (test yok)',
    f'DXY aylik ortalamasinin 12 aylik degisimi +-%10 esigini asan {len(eps)} bolum. "Izleyen 1. yil" = bolumun bittigi takvim yilindan (E) sonraki yil/E; "2. yil" = E+2/E+1. '
    f'Teslimat/oran 2025 sonrasi icin bos (2026 kismi yil). Tum donem satirlari her yil / her ay icin ayni buyuklukler (1. ve 2. yil sutunlari ayni dagilimdir).')
MD.append(md_table(cdfm, 1))
R['M3'] = cdfm.to_dict('records')

# ------------------------------------------------------------------ M4 betimsel
rows = []
ratio_all = {}
Btot_all = pd.Series({y: Brec['Airbus'][y] + Brec['Boeing'][y] for y in range(1973, 2026)})
for y in range(2015, 2027):
    A = ab.loc[y, 'airbus_teslimat']; Bo = ab.loc[y, 'boeing_teslimat']; T = A + Bo
    if y <= 2025: bk = Btot_all[y]
    else: bk = float(tg[(tg.yil == 2026)].backlog_yilsonu.sum())
    gap = (1606 - T) if y >= 2019 else np.nan
    cum = (1606 * (y - 2018) - sum(ab.loc[t, 'airbus_teslimat'] + ab.loc[t, 'boeing_teslimat'] for t in range(2019, y + 1))) if y >= 2019 else np.nan
    ahd = tg[(tg.yil == y) & (tg.uretici == 'Airbus')]
    dev = (float(ahd.gerceklesen.iloc[0]) / float(ahd.hedef_ilk.iloc[0]) - 1) * 100 if (len(ahd) and 2022 <= y <= 2025 and not pd.isna(ahd.hedef_ilk.iloc[0])) else np.nan
    rows.append([str(y) + (' (Oca-Eki)' if y == 2026 else ''), A, Bo, T, gap, cum, bk, bk / T if y < 2026 else np.nan,
                 dev, DXYy.get(y, np.nan), (DXYy[y] / DXYy[y - 1] - 1) * 100])
m4 = pd.DataFrame(rows, columns=['yil', 'Airbus', 'Boeing', 'toplam', 'yillik acik (1606 - toplam)', 'kumulatif acik (2019-)', 'birikim (yil sonu)', 'birikim/teslimat', 'Airbus hedef sapmasi (%)', 'DXY yillik ort', 'DXY degisim (%)'])
sec('M4. Betimsel gecikme gostergeleri 2015-2026 (cikarim yok)',
    '2018 duzeyi 1.606 (Airbus 800 + Boeing 806). 2015-2017 birikimi geriye kurulmustur (M0); 2018-2025 gercektir (2026 Eylul/Ekim sonu, Airbus Eylul). 2026 teslimat Ocak-Ekim, DXY 2026 Ocak-Kasim ortalamasi; 2026 satiri yil-ici kismi.')
MD.append(md_table(m4, 2))
R['M4'] = m4.to_dict('records')

# ------------------------------------------------------------------ M5 hisse ve dolar
adjm = ym.copy()
def mser(s): return s.copy()
def mo(s): s = s.copy(); s.index = s.index.to_period('M'); return s
A_ = {k: adjm[k] for k in ['ITA', 'PPA', 'XAR', 'BA', 'GE', 'RTX', 'LMT', '^GSPC', 'AIR.PA', 'SAF.PA', 'RHM.DE', 'RR.L', 'BA.L']}
A_['MSCI Europe A&D Capped EUR'] = mo(MAD_EUR); A_['MSCI Europe EUR'] = mo(MSE_EUR)
LAST_M = pd.Period('2026-10', 'M')
rets = {k: np.log(v.dropna()).diff().dropna() for k, v in A_.items()}
ddxy = np.log(ym['DX-Y.NYB'].dropna()).diff().dropna()
groups = {'ABD': (['ITA', 'PPA', 'XAR', 'BA', 'GE', 'RTX', 'LMT'], '^GSPC'),
          'Avrupa': (['MSCI Europe A&D Capped EUR', 'AIR.PA', 'SAF.PA', 'RHM.DE', 'RR.L', 'BA.L'], 'MSCI Europe EUR')}
per = {'tumu': (None, LAST_M), '2015-2021': (pd.Period('2015-01', 'M'), pd.Period('2021-12', 'M')), '2022-2026': (pd.Period('2022-01', 'M'), LAST_M)}
m5 = []
for g, (assets, mk) in groups.items():
    for a in assets:
        for pn, (p0, p1) in per.items():
            df = pd.DataFrame({'r': rets[a], 'm': rets[mk], 'd': ddxy}).dropna()
            df = df[df.index <= p1]
            if p0 is not None: df = df[df.index >= p0]
            if len(df) < 24: continue
            res = sm.OLS(df['r'], sm.add_constant(df[['m', 'd']])).fit(cov_type='HAC', cov_kwds={'maxlags': 3})
            ci = res.conf_int().loc['d']
            m5.append([g, a, pn, len(df), res.params['d'], res.bse['d'], res.tvalues['d'], res.pvalues['d'], ci[0], ci[1], res.params['m'], str(df.index[0]), str(df.index[-1])])
m5df = pd.DataFrame(m5, columns=['grup', 'varlik', 'donem', 'n', 'b_d', 'se', 't', 'p', 'GA_alt', 'GA_ust', 'b_piyasa', 'bas', 'son'])
m5df['BH p'] = multipletests(m5df['p'], method='fdr_bh')[1]
n5r = int((m5df.p < .05).sum()); n5b = int((m5df['BH p'] < .05).sum())
sec('M5. Hisse getirileri ve dolar (aylik log getiri; HAC maxlags=3)',
    f'r_varlik = a + b_p*r_piyasa + b_d*dln DXY (ay sonu). ABD varliklari S&P 500, Avrupa varliklari MSCI Europe EUR NETR (yerel para) ile. Ay sonu kapanislar, 2026-10 sonuna kadar (MSCI son veri). '
    f'{len(m5df)} testten ham p<0.05: {n5r}; BH sonrasi q<0.05: {n5b}. EUAD regresyona alinmadi.')
MD.append(md_table(m5df.drop(columns=['GA_alt', 'GA_ust']), 3))
R['M5'] = {'tablo': m5df.to_dict('records'), 'test_sayisi': len(m5df), 'ham_anlamli': n5r, 'bh_anlamli': n5b}
# kayan 36a kismi korelasyon
def pcorr(df):
    X = sm.add_constant(df['m']); ra = sm.OLS(df['r'], X).fit().resid; rd = sm.OLS(df['d'], X).fit().resid
    return float(np.corrcoef(ra, rd)[0, 1])
rollpc = {}
for a, mk in [('ITA', '^GSPC'), ('MSCI Europe A&D Capped EUR', 'MSCI Europe EUR')]:
    df = pd.DataFrame({'r': rets[a], 'm': rets[mk], 'd': ddxy}).dropna(); df = df[df.index <= LAST_M]
    vals = [pcorr(df.iloc[i - 36:i]) for i in range(36, len(df) + 1)]
    s = pd.Series(vals, index=df.index[35:])
    rollpc[a] = s
    R.setdefault('M5_kayan36', {})[a] = {'min': float(s.min()), 'min_tarih': str(s.idxmin()), 'maks': float(s.max()), 'maks_tarih': str(s.idxmax()),
                                          'medyan': float(s.median()), 'son': float(s.iloc[-1]), 'son_tarih': str(s.index[-1]), 'n_pencere': len(s)}
MD.append('\n**36 aylik kayan kismi korelasyon (dln DXY ile, piyasa sabit; betimsel):**\n\n' + md_table(pd.DataFrame(R['M5_kayan36']).T.reset_index().rename(columns={'index': 'varlik'}), 3))
# Europe A&D USD vs EUR
def ret_per(s, a, b):
    return float(s.asof(pd.Timestamp(b)) / s.asof(pd.Timestamp(a)) - 1) * 100
ead = []
for lab, a, b in [('2025', '2024-12-31', '2025-12-31'), ('2026 YTD (30 Ekim)', '2025-12-31', '2026-10-30')]:
    ead.append([lab, ret_per(MAD_USD, a, b), ret_per(MAD_EUR, a, b), ret_per(MSE_USD, a, b), ret_per(MSE_EUR, a, b)])
eadf = pd.DataFrame(ead, columns=['donem', 'Europe A&D Capped NETR USD (%)', 'Europe A&D Capped NETR EUR (%)', 'MSCI Europe NETR USD (%)', 'MSCI Europe NETR EUR (%)'])
MD.append('\n**Kur cevirisi etkisi (MSCI NETR, ay sonu seviyeler):**\n\n' + md_table(eadf, 2))
R['M5_kur'] = eadf.to_dict('records')

# ------------------------------------------------------------------ M6 performans
END = pd.Timestamp('2026-10-30'); END2 = pd.Timestamp('2026-11-18')
SER = [  # ad, seri, tur(D gunluk/M aylik), para, getiri turu, aylik seri (oynaklik), 2026 gunluk
    ('ITA', ADJ['ITA'].dropna(), 'D', 'USD', 'ETF toplam getiri (adjclose)'),
    ('XAR', ADJ['XAR'].dropna(), 'D', 'USD', 'ETF toplam getiri (adjclose)'),
    ('PPA', ADJ['PPA'].dropna(), 'D', 'USD', 'ETF toplam getiri (adjclose)'),
    ('EUAD', ADJ['EUAD'].dropna(), 'D', 'USD', 'ETF toplam getiri (adjclose)'),
    ('S&P 500', CLS['^GSPC'].dropna(), 'D', 'USD', 'fiyat getirisi'),
    ('URTH', ADJ['URTH'].dropna(), 'D', 'USD', 'ETF toplam getiri (adjclose)'),
    ('MSCI World', MSW_USD, 'M', 'USD', 'net toplam getiri (NETR)'),
    ('MSCI Europe', MSE_EUR, 'M', 'EUR', 'net toplam getiri (NETR)'),
    ('MSCI Europe', MSE_USD, 'M', 'USD', 'net toplam getiri (NETR)'),
    ('MSCI Europe A&D Capped', MAD_EUR, 'M', 'EUR', 'net toplam getiri (NETR)'),
    ('MSCI Europe A&D Capped', MAD_USD, 'M', 'USD', 'net toplam getiri (NETR)')]
def val_at(s, kind, ts):
    if s.index[0] > ts: return np.nan
    return float(s.asof(ts))
def val_ago(s, kind, end, n_months):
    if kind == 'M':
        tp = end.to_period('M') - n_months; t = s[s.index.to_period('M') == tp]
        return float(t.iloc[-1]) if len(t) else np.nan
    t = end - pd.DateOffset(months=n_months)
    return val_at(s, kind, t)
perf = []; ytd = []
for nm, s, kind, cur, typ in SER:
    row = {'varlik': nm, 'para': cur, 'getiri turu': typ}
    for y in range(2012, 2026):
        a = val_at(s, kind, pd.Timestamp(f'{y-1}-12-31')); b = val_at(s, kind, pd.Timestamp(f'{y}-12-31'))
        row[str(y)] = (b / a - 1) * 100 if not (np.isnan(a) or np.isnan(b)) else np.nan
    p0 = val_at(s, kind, pd.Timestamp('2025-12-31'))
    row['2026 YTD (30 Eki)'] = (val_at(s, kind, END) / p0 - 1) * 100 if not np.isnan(p0) else np.nan
    row['2026 YTD (18 Kas)'] = (val_at(s, kind, END2) / p0 - 1) * 100 if (kind == 'D' and not np.isnan(p0)) else np.nan
    pe = val_at(s, kind, END)
    for lab, n in [('1 ay', 1), ('3 ay', 3), ('1 yil', 12)]:
        pa = val_ago(s, kind, END, n); row[lab] = (pe / pa - 1) * 100 if not np.isnan(pa) else np.nan
    for lab, n in [('3 yil yillik', 36), ('5 yil yillik', 60), ('10 yil yillik', 120)]:
        pa = val_ago(s, kind, END, n); row[lab] = ((pe / pa) ** (12 / n) - 1) * 100 if not np.isnan(pa) else np.nan
    # oynaklik: aylik seri
    sm_ = s.groupby(s.index.to_period('M')).last() if kind == 'D' else s.groupby(s.index.to_period('M')).last()
    sm_ = sm_[sm_.index <= LAST_M]
    lr = np.log(sm_).diff().dropna().iloc[-36:]
    row['3y yillik oynaklik (aylik, %)'] = float(lr.std() * np.sqrt(12) * 100) if len(lr) >= 36 else np.nan
    ss = s[s.index <= END2] if kind == 'D' else s
    dd_ = ss / ss.cummax() - 1
    row['en buyuk dusus (%)'] = float(dd_.min() * 100); row['dusus dibi'] = str(dd_.idxmin().date())
    row['seri basi'] = str(s.index[0].date()); row['veri sikligi'] = 'gunluk' if kind == 'D' else 'aylik'
    if kind == 'D':
        s26 = s[(s.index >= '2026-01-01') & (s.index <= END2)]
        pk = s26.idxmax(); after = s26[pk:]; tr = after.idxmin()
        row['2026 zirve'] = str(pk.date()); row['zirve sonrasi dip'] = str(tr.date()); row['zirve->dip (%)'] = float((after[tr] / s26[pk] - 1) * 100)
        row['son/zirve (%)'] = float((s26.iloc[-1] / s26[pk] - 1) * 100)
    else:
        row['2026 zirve'] = 'gunluk yok'; row['zirve sonrasi dip'] = ''; row['zirve->dip (%)'] = np.nan; row['son/zirve (%)'] = np.nan
    perf.append(row)
pf = pd.DataFrame(perf)
A_cols = ['varlik', 'para', 'getiri turu'] + [str(y) for y in range(2012, 2026)] + ['2026 YTD (30 Eki)', '2026 YTD (18 Kas)']
B_cols = ['varlik', 'para', '1 ay', '3 ay', '1 yil', '3 yil yillik', '5 yil yillik', '10 yil yillik', '3y yillik oynaklik (aylik, %)', 'en buyuk dusus (%)', 'dusus dibi', 'seri basi', 'veri sikligi', '2026 zirve', 'zirve sonrasi dip', 'zirve->dip (%)', 'son/zirve (%)']
sec('M6. Performans tablolari',
    'Takvim yili getirileri (%), yil sonu-yil sonu; ETF getirileri adjclose (toplam getiri), S&P 500 fiyat, MSCI NETR (net toplam getiri). 2026 YTD 30 Ekim 2026 (ETF icin ayrica 18 Kasim). '
    '1 ay/3 ay/1 yil kumulatif %, 3-5-10 yil yillik bilesik. Oynaklik 3 yillik aylik getirilerden. En buyuk dusus: veri baslangicindan itibaren zirveden dibe (ETF/S&P gunluk, MSCI aylik); 2026 zirve/dip gunluk veriden.')
MD.append('**M6a. Takvim yili ve 2026 YTD getirileri (%)**\n\n' + md_table(pf[A_cols], 2))
MD.append('\n**M6b. Donemsel getiri, oynaklik, dusus (30 Ekim 2026 itibariyla)**\n\n' + md_table(pf[B_cols], 2))
R['M6'] = pf.to_dict('records')

# ------------------------------------------------------------------ GRAFIKLER
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib import font_manager as fm
for f in glob.glob('/usr/share/fonts/opentype/inter/Inter-*.otf') + glob.glob('/usr/share/fonts/truetype/inter/Inter*.ttf'):
    try: fm.fontManager.addfont(f)
    except Exception: pass
fam = 'Inter' if any(f.name == 'Inter' for f in fm.fontManager.ttflist) else 'DejaVu Sans'
if fam != 'Inter': SAPMA.append('Inter yazi tipi bulunamadi; DejaVu Sans kullanildi.')
plt.rcParams.update({'font.family': fam, 'font.size': 9.5, 'axes.labelsize': 9.5, 'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 9,
                     'axes.spines.top': False, 'axes.spines.right': False, 'figure.facecolor': 'white', 'axes.facecolor': 'white',
                     'axes.edgecolor': '#666666', 'axes.labelcolor': '#333333', 'text.color': '#222222', 'xtick.color': '#333333', 'ytick.color': '#333333'})
BLUE, ORNG, GRAY, GRN, PURP, RED, SKY = '#0072B2', '#D55E00', '#7F7F7F', '#009E73', '#CC79A7', '#C0392B', '#56B4E9'
W = 7.2
def fig_(h): return plt.figure(figsize=(W, h), dpi=220)
import textwrap
def finish(fig, title, src, top=None, bottom=None, left=None):
    h = fig.get_size_inches()[1]
    lines = textwrap.wrap(src, 118); nl = len(lines)
    fig.text(0.015, 1 - 0.08 / h, title, ha='left', va='top', fontsize=11.5, fontweight='semibold')
    fig.text(0.015, 0.06 / h, '\n'.join(lines), ha='left', va='bottom', fontsize=7.5, color='#555555', linespacing=1.15)
    xl = any(a.get_xlabel() for a in fig.axes)
    bot = (0.12 + 0.13 * nl + 0.42 + (0.28 if xl else 0)) / h
    kw = dict(top=1 - 0.62 / h, bottom=bot)
    if left: kw['left'] = left
    fig.subplots_adjust(**kw)
def save(fig, name): fig.savefig(f'{GR}/{name}', dpi=220, facecolor='white'); plt.close(fig)

# G1
fig = fig_(4.4); ax = fig.add_subplot(111)
base = pd.Timestamp('2024-12-31')
for t, lab, c, ls in [('ITA', 'ITA (ABD havacılık-savunma)', BLUE, '-'), ('EUAD', 'EUAD (Avrupa havacılık-savunma, USD)', ORNG, '-'),
                      ('^GSPC', 'S&P 500', GRAY, '-'), ('URTH', 'URTH (MSCI World)', GRN, '--')]:
    s = ADJ[t].dropna(); s = s[(s.index >= base) & (s.index <= END2)]; s = s / s.asof(base) * 100
    ax.plot(s.index, s.values, color=c, lw=1.6, ls=ls, label=lab)
ax.axhline(100, color='#999999', lw=0.8)
ax.set_ylim(15, 235); yl = ax.get_ylim()
for dt, lab, yy in [('2026-02-28', '28 Şub: İran savaşı', 0.99), ('2026-08-14', '14 Ağu: zirve', 0.99), ('2026-11-03', '3 Kas: ara seçim', 0.91)]:
    ax.axvline(pd.Timestamp(dt), color='#444444', lw=0.8, ls=':')
    ax.text(pd.Timestamp(dt) - pd.Timedelta(days=5), yl[0] + (yl[1] - yl[0]) * yy, lab, ha='right', va='top', fontsize=8.5, color='#333333')
TR_AY = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']
ax.set_ylabel('31 Aralık 2024 = 100'); ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{TR_AY[mdates.num2date(v).month - 1]} {mdates.num2date(v):%y}"))
ax.legend(frameon=False, loc='lower left', bbox_to_anchor=(0.03, 0.0))
finish(fig, 'Havacılık-savunma fonları 2025-2026: seçilmiş ABD ve Avrupa, geniş piyasalara karşı', 'Kaynak: Yahoo Finance günlük düzeltilmiş kapanış (toplam getiri), 18 Kasım 2026\'ya kadar; ITA 3\'e 1 bölünmeye göre ayarlı.')
save(fig, 'G1_2026_fiyat.png')

# G2
tk = pd.read_csv(f'{V}/msci_takvim_yili.csv'); lab_x = [str(y) if not str(y).startswith('2026') else '2026\nYTD' for y in tk.yil]
fig = fig_(6.4); axs = fig.subplots(2, 1, sharex=True)
for ax, (c1, l1, c2, l2, tt) in zip(axs, [('world_ad_net_usd', 'MSCI World A&D (net, USD)', 'msci_world_net_usd', 'MSCI World (net, USD)', ''),
                                          ('europe_ad_fiyat_usd', 'MSCI Europe A&D (fiyat, USD)', 'msci_europe_fiyat_usd', 'MSCI Europe (fiyat, USD)', '')]):
    x = np.arange(len(tk)); w = 0.38
    ax.bar(x - w / 2, tk[c1], w, color=BLUE, label=l1); ax.bar(x + w / 2, tk[c2], w, color='#B0B0B0', label=l2)
    ax.axhline(0, color='#444444', lw=0.8); ax.set_ylabel('Getiri (%)'); ax.legend(frameon=False, loc='lower left', bbox_to_anchor=(0, 1.0), ncol=2, borderaxespad=0.2)
axs[1].set_xticks(np.arange(len(tk))); axs[1].set_xticklabels(lab_x)
finish(fig, 'Takvim yılı getirileri: havacılık-savunma endeksleri ve geniş piyasa, 2012-2026 YTD', 'Kaynak: MSCI factsheet takvim yılı getirileri; 2026 YTD 30 Ekim 2026. World A&D net toplam getiri, Europe A&D fiyat getirisi.')
save(fig, 'G2_takvim_yili.png')

# G3
fig = fig_(4.0); ax = fig.add_subplot(111)
yy = list(range(2000, 2026))
ax.plot(yy, ab.loc[yy, 'airbus_teslimat'], color=BLUE, lw=1.8, marker='o', ms=3.5, label='Airbus')
ax.plot(yy, ab.loc[yy, 'boeing_teslimat'], color=ORNG, lw=1.8, marker='o', ms=3.5, label='Boeing')
ax.plot([2026], [ab.loc[2026, 'airbus_teslimat']], marker='o', ms=6, mfc='white', mec=BLUE, ls='none')
ax.plot([2026], [ab.loc[2026, 'boeing_teslimat']], marker='o', ms=6, mfc='white', mec=ORNG, ls='none')
ax.text(2026.3, ab.loc[2026, 'airbus_teslimat'] + 30, 'Oca-Eki\n2026', fontsize=8.5, ha='right', va='bottom', color='#333333')
for yv, lab, dy in [(2019, '2019: 737 MAX\nyasağı', (2014.3, 230)), (2020, '2020: COVID', (2020, 45)), (2024, '2024: kalite krizi\nve grev', (2023.8, 190))]:
    ax.annotate(lab, (yv, ab.loc[yv, 'boeing_teslimat']), xytext=dy, fontsize=8.5, ha='center', color='#333333',
                arrowprops=dict(arrowstyle='-', color='#888888', lw=0.7))
ax.set_ylabel('Yıllık teslimat (adet)'); ax.set_xlim(1999.3, 2027); ax.legend(frameon=False, loc='upper left'); ax.set_ylim(0, 950)
finish(fig, 'Airbus ve Boeing yıllık uçak teslimatı, 2000-2026', 'Kaynak: Wikipedia (Competition between Airbus and Boeing); 2026 Ocak-Ekim kısmi yıl (içi boş işaret).')
save(fig, 'G3_teslimat.png')

# G4
fig = fig_(5.6); a1, a2 = fig.subplots(2, 1, sharex=True)
x1 = DXYy.loc[1975:2025]; a1.plot(x1.index, x1.values, color=BLUE, lw=1.8); a1.set_ylabel('DXY, yıllık ort.')
a1.set_title('Dolar endeksi (DXY)', loc='left', fontsize=9.5, fontweight='semibold')
a2.plot(ratio.loc[max(START_B, 1975):].index, ratio.loc[max(START_B, 1975):].values, color=ORNG, lw=1.8)
a2.axvline(2018, color='#888888', lw=0.8, ls=':'); a2.text(2017.5, a2.get_ylim()[1] * 0.97, 'gerçek birikim 2018 ve sonrası →', ha='right', va='top', fontsize=8.5, color='#333333')
a2.set_title('Birikim / teslimat oranı (yıl)', loc='left', fontsize=9.5, fontweight='semibold'); a2.set_ylabel('Yıl'); a2.set_xlim(1975, 2025)
finish(fig, 'Dolar endeksi ve toplam sipariş birikimi/teslimat oranı, 1975-2025', f'Kaynak: Yahoo Finance (DXY); Airbus-Boeing teslimat ve sipariş (Wikipedia), birikim 2018\'den geriye kurulmuş (başlangıç {max(START_B,1975)}). Oran sipariş patlamasında da yükselir.')
save(fig, 'G4_dxy_birikim.png')

# G5
fig = fig_(4.8); ax = fig.add_subplot(111)
xs = (DXYy / DXYy.shift(1) - 1) * 100; ys = (Dtot.loc[:2025] / Dtot.loc[:2025].shift(1) - 1) * 100
dfp = pd.DataFrame({'x': xs, 'y': ys}).loc[1975:2025].dropna()
r_ = np.corrcoef(dfp.x, dfp.y)[0, 1]; sl, ic = np.polyfit(dfp.x, dfp.y, 1)
oth = dfp[~dfp.index.isin(EVY)]; ev = dfp[dfp.index.isin(EVY)]
ax.scatter(oth.x, oth.y, s=22, color='#9A9A9A', label='Diğer yıllar')
ax.scatter(ev.x, ev.y, s=30, color=ORNG, label='Olay yılları (grev, kriz, MAX, COVID)')
offs = {1995: (4, 4), 1997: (4, 4), 2001: (4, 4), 2002: (4, -9), 2005: (4, 4), 2008: (-4, 4), 2009: (4, 4), 2019: (4, 4), 2020: (4, 2), 2021: (4, 4), 2024: (4, 4)}
for e in EVY:
    if e in dfp.index:
        o = offs[e]; ax.annotate(str(e), (dfp.x[e], dfp.y[e]), xytext=o, textcoords='offset points', fontsize=8.5, color='#333333', ha='left' if o[0] > 0 else 'right')
xx = np.linspace(dfp.x.min(), dfp.x.max(), 20); ax.plot(xx, ic + sl * xx, color=BLUE, lw=1.6, label=f'Doğrusal uyum (r = {r_:.2f}, n = {len(dfp)})')
ax.axhline(0, color='#888888', lw=0.7); ax.axvline(0, color='#888888', lw=0.7)
ax.set_xlabel('DXY yıllık değişim (%)'); ax.set_ylabel('Toplam teslimat yıllık değişim (%)'); ax.legend(frameon=False, loc='lower left', fontsize=8.5)
finish(fig, 'Dolar değişimi ile toplam uçak teslimatı değişimi, 1975-2025', 'Kaynak: Yahoo Finance (DXY yıllık ortalama), Airbus+Boeing teslimat (Wikipedia). Eşzamanlı yıllık yüzde değişimler.')
save(fig, 'G5_sacilim.png')

# G6
rowsf = []
lab6 = {'Y1': 'Toplam teslimat', 'Y2': 'Airbus teslimat', 'Y3': 'Boeing teslimat', 'Y4': 'Birikim/teslimat oranı', 'Y5': 'Sipariş yoğunluğu (yüzde puan)'}
for yn, vn, r in m1:
    if vn.startswith('(ii)'): rowsf.append((lab6[yn.split()[0]] + ' (yıllık)', r['etki10'], *r['etki10_ga'], BLUE))
r2 = R['M2']['ABD G336411T3|1973Q1-2026Q3']; rowsf.append(('ABD uçak üretimi (çeyreklik)', r2['etki10'], *r2['etki10_ga'], ORNG))
fig = fig_(3.8); ax = fig.add_subplot(111)
for i, (lb, e, lo, hi, c) in enumerate(rowsf):
    y = len(rowsf) - 1 - i
    ax.errorbar(e, y, xerr=[[e - lo], [hi - e]], fmt='o', color=c, ms=6, lw=1.8, capsize=0)
ax.axvline(0, color='#222222', lw=1.4); ax.set_yticks(range(len(rowsf))); ax.set_yticklabels([r[0] for r in rowsf][::-1])
ax.set_xlabel('DXY %10 yükselirse toplam etki (%; sipariş yoğunluğu için yüzde puan)')
finish(fig, 'Dolar %10 güçlenirse etki ne kadar? Tahmin ve %95 güven aralığı', 'Kaynak: hesap/02_analiz.py; yıllık: M1 varyant (ii), 1975-2025; çeyreklik: M2, 1973Ç1-2026Ç3, gecikme 0-8. Newey-West HAC.', left=0.36)
save(fig, 'G6_gecikme_etkisi.png')

# G7
fig = fig_(5.4)
gs = fig.add_gridspec(6, 1, height_ratios=[5, .42, .42, .42, .42, .42], hspace=0.12)
ax = fig.add_subplot(gs[0]); dx = DXYd['2018-01-01':'2026-11-30']
ax.plot(dx.index, dx.values, color=BLUE, lw=1.1); ax.set_ylabel('DXY (günlük kapanış)'); ax.tick_params(labelbottom=False)
events = [('737 MAX yasağı', '2019-03-01', '2020-11-30', ORNG), ('COVID', '2020-03-01', '2021-06-30', PURP), ('Tedarik/motor\ndarboğazı', '2022-01-01', '2026-11-19', GRAY),
          ('Kapı tapası,\nFAA sınırı', '2024-01-01', '2025-10-31', RED), ('Boeing grevi', '2024-09-01', '2024-11-30', GRN)]
for i, (lb, a, b, c) in enumerate(events):
    axs = fig.add_subplot(gs[i + 1], sharex=ax); axs.axvspan(pd.Timestamp(a), pd.Timestamp(b), color=c, alpha=0.85, lw=0)
    for s_ in ['left', 'right', 'top']: axs.spines[s_].set_visible(False)
    axs.set_yticks([]); axs.text(-0.012, 0.5, lb, transform=axs.transAxes, ha='right', va='center', fontsize=8.5, linespacing=0.95)
    if i < 4: axs.tick_params(labelbottom=False, length=0)
    for s_ in (['bottom'] if i < 4 else []): axs.spines[s_].set_visible(False)
axs.set_xlim(pd.Timestamp('2018-01-01'), pd.Timestamp('2026-11-30')); axs.xaxis.set_major_locator(mdates.YearLocator()); axs.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
fig.subplots_adjust(left=0.2, right=0.985, top=0.92, bottom=0.07)
fig.text(0.015, 0.985, 'Dolar endeksi ve havacılık teslimat krizleri, 2018-2026', ha='left', va='top', fontsize=11.5, fontweight='semibold')
fig.text(0.015, 0.008, 'Kaynak: Yahoo Finance (DXY); kriz tarihleri araştırma notlarından (ek/D_teslimat_gecikmeleri.md), ay doğruluğunda.', fontsize=7.5, color='#555555')
save(fig, 'G7_dxy_olaylar.png')

# G8
fig = fig_(5.8); a1, a2 = fig.subplots(2, 1, sharex=True)
q1 = (DXYq / DXYq.shift(4) - 1) * 100; q2 = (AC / AC.shift(4) - 1) * 100
q1 = q1[q1.index >= pd.Period('1973Q1', 'Q')]; q2 = q2[q2.index >= pd.Period('1973Q1', 'Q')]
for ax_, s, c, tt, yl_ in [(a1, q1, BLUE, 'DXY', 'Yıllık değişim (%)'), (a2, q2, ORNG, 'Uçak ve parçaları üretimi (G336411T3)', 'Yıllık değişim (%)')]:
    ax_.plot(s.index.to_timestamp(), s.values, color=c, lw=1.3); ax_.axhline(0, color='#888888', lw=0.7); ax_.set_ylabel(yl_)
    ax_.set_title(tt, loc='left', fontsize=9.5, fontweight='semibold')
    for a, b in REC: ax_.axvspan(pd.Period(a, 'M').start_time, pd.Period(b, 'M').end_time, color='#D9D9D9', alpha=0.8, lw=0)
a2.set_xlim(pd.Timestamp('1973-01-01'), pd.Timestamp('2026-12-31'))
finish(fig, 'Dolar ve ABD uçak üretimi: çeyreklik yıllık değişim, 1973-2026', 'Kaynak: Yahoo Finance (DXY), Federal Reserve G.17 (G336411T3, mevsimsellikten arındırılmış), çeyreklik ortalama. Gri bant: NBER ABD resesyonları.')
save(fig, 'G8_uretim.png')

# G9
fig = fig_(4.8); ax = fig.add_subplot(111)
t = m5df[m5df.donem == 'tumu'].reset_index(drop=True)
ypos = []; labs = []; y = 0; items = []
for g, c in [('ABD', BLUE), ('Avrupa', ORNG)]:
    sub_ = t[t.grup == g]
    items.append((g, y, None, c)); y += 1
    for _, rw in sub_.iterrows():
        items.append((rw.varlik.replace(' EUR', ' (EUR)'), y, rw, c)); y += 1
    y += 0.6
top = y
for nm, yv, rw, c in items:
    yp = top - yv
    if rw is None: ax.text(ax.get_xlim()[0] if False else -0.02, yp, nm + ' varlıkları', transform=ax.get_yaxis_transform(), ha='right', va='center', fontsize=9.5, fontweight='semibold'); continue
    ax.errorbar(rw.b_d, yp, xerr=[[rw.b_d - rw.GA_alt], [rw.GA_ust - rw.b_d]], fmt='o', color=c, ms=5.5, lw=1.6, capsize=0)
    ax.text(-0.02, yp, nm, transform=ax.get_yaxis_transform(), ha='right', va='center', fontsize=9)
ax.axvline(0, color='#222222', lw=1.3); ax.set_yticks([]); ax.spines['left'].set_visible(False)
ax.set_xlabel('b_d: dolar (DXY) aylık %1 artışında varlık getirisi değişimi (puan; piyasa sabit)')
ax.set_ylim(-0.7, top + 0.9)
finish(fig, 'Hisse getirilerinin dolar duyarlılığı (piyasa sabit), tüm dönem', 'Kaynak: Yahoo Finance, MSCI; aylık log getiri, HAC (Newey-West, 3 gecikme), %95 GA; ABD varlıkları S&P 500\'e, Avrupa varlıkları MSCI Europe (EUR)\'a karşı.', left=0.30)
fig.subplots_adjust(right=0.97)
save(fig, 'G9_hisse_dolar.png')

# ------------------------------------------------------------------ yazim
def conv(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return None if np.isnan(o) else float(o)
    if isinstance(o, (pd.Period, pd.Timestamp)): return str(o)
    return str(o)
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, float) and np.isnan(o): return None
    if isinstance(o, (np.floating,)): return None if np.isnan(o) else float(o)
    if isinstance(o, np.integer): return int(o)
    return o
json.dump(clean(R), open(f'{H}/sonuclar.json', 'w'), ensure_ascii=False, indent=1, default=conv)
SAPMA += ['Ek veri: Fed G.17 imalat = GMF (NAICS) kullanildi; Eurostat imalat nace_r2=C (SCA, I21); BIS WS_EER M.N.B.US yillik ortalama.',
          'Yillik ve ceyreklik modellerde HAC ile (use_t=False) normal yaklasimli GA ve Wald/F p kullanildi; kucuk orneklemde p degerleri iyimser olabilir.',
          'Resesyon kuklasi ceyreklikte: ceyrekte >=2 ay resesyon. Eurostat modellerinde yalniz ayni ulkenin imalat uretimi kontrolu (talimat geregi).',
          'M5: dln DXY ay sonu kapanistan; MSCI son veri 2026-10 oldugu icin tum varliklar 2026-10 sonuna kesildi. EUAD regresyonda yok.',
          'M3: "izleyen 1./2. takvim yili" bolumun bittigi yila (E) gore E+1/E ve E+2/E+1 degisimi olarak yorumlandi; 2025 sonrasi bos.',
          'MSCI World A&D (net) ve Europe A&D (standart) endeks verisi bu hesapta yok; takvim yili G2 yalniz factsheet tablosundan; M6 icin World A&D yerine ITA/XAR/PPA, Europe A&D yerine Capped (763669) kullanildi.',
          'M6: MSCI serilerinin gunluk verisi yok; en buyuk dusus aylik seviyelerden, 2026 zirve/dip yalniz gunluk serilerden. 763669 2014-11 basladigi icin 2014 ve oncesi bos.',
          'G.17 G336411T3 kaynak turu (fiziksel/isci saati): ozel aciklama bulunamadi.',
          'Birikim kimligi Boeing icin 2019-2025 gercekle tutmuyor (2020: -2.271, ASC 606 vb. duzeltme); geriye kurulan seri 2018 gercek degerine capalidir, 1987 oncesi birikim <=0 oldugundan Y4/Y5 orneklemi 1988/1989-2025 (n=38).',
          'Alt donem ve kayan pencere analizleri: Y4/Y5 icin 1978-1999 yalniz n=12 (7 parametre); kayan 20 yillik pencere yalniz Y1-Y3 icin.',
          'Boeing 2026 Ocak-Ekim teslimat: airbus_boeing_yillik.csv 524, teslimat_hedef.csv 523 (M4 ilk dosyayi kullanir). 2026 birikimi Airbus Eylul + Boeing Ekim sonu.',
          'Granger: VAR [dln uretim, dln DXY], AIC gecikmesi (<=8); G3364 de ayrica denendi. M2 ortak F p degerleri HAC ile 9 gecikme uzerinden.']
with open(f'{H}/sonuclar.md', 'w') as f:
    f.write('# Hesap sonuclari (hesap/02_analiz.py)\n\nTum tablolar tek komutla yeniden uretilir. Yorum icermez; hukum ana raporda.\n' + '\n'.join(MD))
    f.write('\n\n## Yapilamayanlar ve sapmalar\n\n' + '\n'.join('- ' + s for s in SAPMA) + '\n')
print('TAMAM'); print('\n'.join(SAPMA[:3]))
