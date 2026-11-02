"""Ortak yardımcılar (grup ajanı). ll.py'yi değiştirmeden kullanır."""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
sys.path.insert(0, SCR + '/code'); import ll
OUT = SCR + '/out'; HERE = OUT + '/code_y_grup'
SPLIT = pd.Timestamp('2021-01-01')
def S(x): return x if x.endswith('.IS') else x + '.IS'
_rc, _dc = {}, {}
def R(sym):
    s = S(sym)
    if s not in _rc:
        r = ll.ret(s); _rc[s] = r[r.index <= pd.Timestamp('2026-10-30')]
    return _rc[s]
LAST = pd.Timestamp('2026-10-30')  # son tam gün; 02.11 kısmi barları at
def DC(sym):
    s = S(sym)
    if s not in _dc:
        d = ll.decomp(s); _dc[s] = d[d.index <= LAST]
    return _dc[s]
def px(sym, field='c'):
    d = ll.raw(S(sym)).copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]
    return d[d.index <= LAST]
def liq(sym, start='2025-10-30'):
    d = px(sym); d = d[d.index >= pd.Timestamp(start)]
    tl = (d['c'] * d['v']).median() / 1e6
    r = np.log(d['c']).diff(); z = float((r == 0).mean())
    return tl, z
# Grup çiftleri: (ana, yavru, grup, tür)  tür: ps=ana-yavru, sib=kardeş, cls=pay grubu, jv=ortak girişim
PAIRS = [
 ('ISCTR','SISE','IS','ps'),('ISCTR','TSKB','IS','ps'),('ISCTR','ANSGR','IS','ps'),('ISCTR','ANHYT','IS','ps'),('ISCTR','ISMEN','IS','ps'),
 ('ISCTR','ISGYO','IS','ps'),('ISCTR','ISFIN','IS','ps'),('ISCTR','ISGSY','IS','ps'),('ISCTR','ISYAT','IS','ps'),('ISMEN','ISGSY','IS','ps'),('ANSGR','ANHYT','IS','sib'),
 ('ISCTR','ISBTR','IS','cls'),('ISCTR','ISATR','IS','cls'),('ISCTR','ISKPL','KONTROL','none'),
 ('KCHOL','TUPRS','KOC','ps'),('KCHOL','FROTO','KOC','ps'),('KCHOL','TOASO','KOC','ps'),('KCHOL','ARCLK','KOC','ps'),('KCHOL','YKBNK','KOC','ps'),
 ('KCHOL','AYGAZ','KOC','ps'),('KCHOL','OTKAR','KOC','ps'),('KCHOL','TTRAK','KOC','ps'),('AYGAZ','TUPRS','KOC','sib'),('FROTO','TOASO','KOC','sib'),
 ('SAHOL','AKBNK','SAB','ps'),('SAHOL','ENJSA','SAB','ps'),('SAHOL','CIMSA','SAB','ps'),('SAHOL','BRISA','SAB','ps'),('SAHOL','KORDS','SAB','ps'),
 ('SAHOL','AKGRT','SAB','ps'),('SAHOL','AGESA','SAB','ps'),('SAHOL','AKCNS','SAB','ps'),('SAHOL','CRFSA','SAB','ps'),('SAHOL','TKNSA','SAB','ps'),('CIMSA','AKCNS','SAB','sib'),
 ('AGHOL','AEFES','AG','ps'),('AGHOL','MGROS','AG','ps'),('AGHOL','CCOLA','AG','ps'),('AGHOL','ASUZU','AG','ps'),('AGHOL','ADEL','AG','ps'),('AEFES','CCOLA','AG','ps'),('AEFES','MGROS','AG','sib'),
 ('EREGL','ISDMR','OYAK','ps'),('EREGL','OYAKC','OYAK','sib'),('EREGL','HEKTS','OYAK','sib'),('OYAKC','HEKTS','OYAK','sib'),('EREGL','TKFEN','OYAK','sib26'),('OYAKC','TKFEN','OYAK','sib26'),
 ('VESTL','VESBE','ZORLU','ps'),('ZOREN','VESTL','ZORLU','sib'),('ZOREN','VESBE','ZORLU','sib'),
 ('DOHOL','GWIND','DOGAN','ps'),('DOHOL','DITAS','DOGAN','ps'),
 ('BRYAT','BRSAN','BORUSAN','ps'),('BRYAT','BORLS','BORUSAN','ps'),('BRSAN','BORLS','BORUSAN','sib'),
 ('ULKER','SOKM','YILDIZ','sib'),('GOZDE','SOKM','YILDIZ','ps'),('ULKER','GOZDE','YILDIZ','sib'),
 ('TRMET','TRALT','TR','ps'),('TRENJ','TRMET','TR','ps'),('TRENJ','TRALT','TR','ps'),
 ('KRDMD','KRDMA','KARDEMIR','cls'),('KRDMD','KRDMB','KARDEMIR','cls'),('KRDMA','KRDMB','KARDEMIR','cls'),
 ('ALARK','ALCAR','ALARKO','ps'),('ALARK','ALGYO','ALARKO','ps'),
 ('ECZYT','ECILC','ECZ','ps'),('ECZYT','INTEM','ECZ','ps'),('ECILC','INTEM','ECZ','sib'),
 ('GLYHO','CONSE','GLOBAL','ps'),('GLYHO','NATEN','GLOBAL','ps'),('GLYHO','GLBMD','GLOBAL','ps'),('GLYHO','PASEU','GLOBAL','?'),
 ('TKFEN','AKMGY','TEKFEN','ps'),('AKSA','AKENR','AKKOK','sib'),('AKSA','AKMGY','AKKOK','sib'),
 ('AKFGY','AKFYE','AKFEN','sib'),('ODAS','CANTE','ODAS','ps'),('TEHOL','TERA','TERA','ps'),('TEHOL','PEKGY','TERA','sib'),('TERA','PEKGY','TERA','sib'),
 ('THYAO','DOCO','JV','jv'),('THYAO','PGSUS','KONTROL','none'),('TAVHL','CLEBI','KONTROL','none'),('GUBRF','BAGFS','?','?'),
 ('HALKB','HLGYO','TVF','ps'),('VAKBN','VAKFN','TVF','ps'),('VAKBN','VKGYO','TVF','ps'),
]
TVF = ['THYAO','TCELL','TTKOM','HALKB','VAKBN','TURSG','TRALT','TRMET','TRENJ']
def nwreg(y, X, lags=5):
    import statsmodels.api as sm
    df = pd.concat([y.rename('y'), X], axis=1).dropna()
    if len(df) < 60: return None
    m = sm.OLS(df['y'].values, sm.add_constant(df.drop(columns='y').values)).fit(cov_type='HAC', cov_kwds={'maxlags': lags})
    return m, df
def zs(x): return (x - x.mean()) / x.std()
