"""v_YA1_a — tavan/taban olay tanımı (bağımsız). Çıktı: _ev.parquet + konsol tabloları.
Tanımlar (P10: >=2020-03-13, lim=0,10; P20: 2015-12-01..2020-03-10, lim=0,20):
  b_t = c_{t-1}*f_{t-1}/f_t (temettü/bölünme düzeltilmiş baz), f=adj/c ; R=c/b ; Rh=h/b ; Rl=l/b ; Ro=o/b
  tik_rel = BIST spot tik(c_unadj)/c_unadj ; tol = min(max(tik_rel,0.001)+0.001, 0.0075); c==h toleransı min(0.5*tik_rel, 0.001)
  TC  : R>=1+lim-tol & c>=h*(1-0.5*tik_rel)            (tavan kapanış; tik-temelli, ANA tanım)
  TCL : TC & l>=h*(1-0.5*tik_rel)                       (kilitli tavan)
  TU  : Rh>=1+lim-tol & R<1+lim-0.01                    (tavana dokundu, en az 1 puan altında kapandı)
  BC/BCL/BU simetrik; UP6/DN6 kontrol (|R-1| in [0.06, lim-0.01), limite dokunmadı)
  Alternatif: TC_B (kaynak gibi: R>=1.0925 & c>=0.999h), TC_S (katı: R>=1.098 & c==h)
  Önceki satır bir önceki BIST işlem günü değilse (veri boşluğu/askı) olay sınıflanmaz.
  |R-1|>lim+0.005 -> kurumsal işlem/veri hatası (ca) -> sınıflanmaz.
"""
import numpy as np, pandas as pd, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v0_panel import index_ret, SCR
VIOP = ['AEFES','AKBNK','AKSEN','ALARK','ARCLK','ASELS','ASTOR','BIMAS','BRSAN','CIMSA','DOAS','DOHOL','EKGYO','ENJSA','ENKAI','EREGL','FROTO','GARAN','GUBRF','HALKB','HEKTS','ISCTR','KCHOL','KRDMD','MGROS','ODAS','OYAKC','PETKM','PGSUS','SAHOL','SASA','SISE','SOKM','TAVHL','TCELL','THYAO','TKFEN','TOASO','TRALT','TRMET','TSKB','TTKOM','TUPRS','ULKER','VAKBN','VESTL','YKBNK']

def tick(p):
    p = np.asarray(p, float)
    return np.select([p < 20, p < 50, p < 100, p < 250, p < 500, p < 1000, p < 2500], [0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00], 2.50)

def build():
    P = pd.read_parquet(HERE + '/_panel.parquet').sort_values(['stock', 'date']).reset_index(drop=True)
    # BIST takvimi: hisselerin >=%40'ının işlem gördüğü günler
    cnt = P.groupby('date').size(); nst = P.groupby(P.date.dt.year).stock.nunique()
    cal = cnt[cnt >= 0.4 * nst.reindex(cnt.index.year).values].index
    cpos = pd.Series(np.arange(len(cal)), index=cal)
    P['cp'] = cpos.reindex(P.date).values
    g = P.groupby('stock')
    P['f'] = P.adj / P.c
    P['contig'] = (P.cp - g.cp.shift(1)) == 1
    P['b'] = g.c.shift(1) * g.f.shift(1) / P.f
    P['R'] = P.c / P.b; P['Rh'] = P.h / P.b; P['Rl'] = P.l / P.b; P['Ro'] = P.o / P.b
    P['reg'] = np.where(P.date >= '2020-03-13', 'P10', np.where((P.date >= '2015-12-01') & (P.date <= '2020-03-10'), 'P20', 'old'))
    lim = np.where(P.reg == 'P20', 0.20, 0.10)
    P['lim'] = lim
    P['tik_rel'] = tick(P.c_unadj) / P.c_unadj
    tol = np.minimum(np.maximum(P.tik_rel, 0.001) + 0.001, 0.0075)  # Yahoo bölünme meta eksikliğinde (örn. HEKTS 2015) tik şişmesin
    ca = (P.R - 1).abs() > lim + 0.005
    ok = P.contig & ~ca & (P.reg != 'old') & P.R.notna()
    P['ca'] = ca
    upx = 1 + lim - tol; dnx = 1 - lim + tol
    P['TC'] = ok & (P.R >= upx) & (P.c >= P.h * (1 - np.minimum(0.5 * P.tik_rel, 0.001)))
    P['TCL'] = P.TC & (P.l >= P.h * (1 - np.minimum(0.5 * P.tik_rel, 0.001)))
    P['TU'] = ok & (P.Rh >= upx) & (P.Rh <= 1 + lim + 0.005) & (P.R < 1 + lim - 0.01)
    P['BC'] = ok & (P.R <= dnx) & (P.c <= P.l * (1 + np.minimum(0.5 * P.tik_rel, 0.001)))
    P['BCL'] = P.BC & (P.h <= P.l * (1 + np.minimum(0.5 * P.tik_rel, 0.001)))
    P['BU'] = ok & (P.Rl <= dnx) & (P.Rl >= 1 - lim - 0.005) & (P.R > 1 - lim + 0.01)
    P['UP6'] = ok & (P.R - 1 >= 0.6 * lim) & (P.R < 1 + lim - 0.01) & (P.Rh < upx)
    P['DN6'] = ok & (1 - P.R >= 0.6 * lim) & (P.R > 1 - lim + 0.01) & (P.Rl > dnx)
    P['TC_B'] = ok & (P.R >= 1 + lim - 0.0075) & (P.c >= 0.999 * P.h)
    P['TC_S'] = ok & (P.R >= 1 + lim - 0.002) & (P.c >= P.h * (1 - 1e-6))
    P['BC_B'] = ok & (P.R <= 1 - lim + 0.0075) & (P.c <= 1.001 * P.l)
    # gün getirileri
    P['cc'] = np.where(P.contig & ~ca, np.log(P.R), np.nan)
    P['intra'] = np.log(P.c / P.o)
    P['gap'] = np.log(P.o / P.b)
    P.loc[~(P.contig & ~ca), ['gap']] = np.nan
    X = index_ret('XU100')
    P['xcc'] = X.cc.reindex(P.date).values; P['xgap'] = X.gap.reindex(P.date).values; P['xintra'] = X.intra.reindex(P.date).values
    P['xlc'] = X.lc.reindex(P.date).values
    P['lc'] = np.log(P.adj)
    g = P.groupby('stock')
    for k in [1]:
        for v in ['cc', 'gap', 'intra', 'xcc', 'xgap', 'xintra', 'R', 'Ro', 'Rh', 'Rl', 'date', 'TC', 'BC', 'TCL', 'BCL', 'contig', 'tik_rel', 'c_unadj']:
            P[f'{v}_1'] = g[v].shift(-k)
    for k in [1, 2, 5, 6, 10]:
        P[f'lc_{k}'] = g.lc.shift(-k); P[f'xlc_{k}'] = g.xlc.shift(-k)
    P['date_5'] = g.date.shift(-5)
    P['BC_2'] = g.BC.shift(-2)
    P['dr2_5'] = (P.lc_5 - P.lc_1) - (P.xlc_5 - P.xlc_1)       # t+1 kapanış -> t+5 kapanış, XU100'e göre
    P['dr2_5raw'] = (P.lc_5 - P.lc_1)
    P['dr3_6'] = (P.lc_6 - P.lc_2) - (P.xlc_6 - P.xlc_2)       # t+2 kapanış -> t+6 kapanış
    P['dr2_10'] = (P.lc_10 - P.lc_1) - (P.xlc_10 - P.xlc_1)
    P['tv'] = (P.c * P.v).where(P.v > 0)
    P['tv60'] = g.tv.transform(lambda s: s.rolling(60, min_periods=20).median().shift(1))
    P['age'] = g.cumcount()
    P['viop'] = P.stock.isin(VIOP)
    P['yr'] = P.date.dt.year
    keep = P.TC | P.TU | P.BC | P.BU | P.UP6 | P.DN6 | P.TC_B | P.TC_S | P.BC_B
    E = P[keep].copy()
    E['liq'] = E.groupby('yr').tv60.transform(lambda s: pd.qcut(s.rank(method='first'), 3, labels=['L', 'M', 'H']) if s.notna().sum() > 30 else np.nan)
    E.to_parquet(HERE + '/_ev.parquet')
    cols = ['date','stock','reg','lim','R','Rh','Rl','Ro','c','h','l','o','tik_rel','c_unadj','contig','ca','TC','TU','BC','UP6','intra','gap','cc','xintra','intra_1','gap_1','xintra_1','xgap_1','Ro_1','R_1','TC_1','BC_1','dr2_5','tv60','age','viop','yr']
    P.loc[P.reg != 'old', cols].to_parquet(HERE + '/_full.parquet')
    # tüm-gün paneli (P10) koşulsuz olasılıklar için küçük özet
    P10 = P[(P.reg == 'P10') & P.contig & ~P.ca]
    print('P10 hisse-gün', len(P10), 'P(TC)=%.4f P(BC)=%.4f' % (P10.TC.mean(), P10.BC.mean()))
    return E

def ct(df, v):
    """havuz ortalaması (bps) ve tarih kümelemeli t (gün ortalamalarının t'si)"""
    x = df[['date', v]].dropna()
    if len(x) < 5: return np.nan, np.nan, len(x)
    gm = x.groupby('date')[v].mean()
    t = gm.mean() / (gm.std(ddof=1) / np.sqrt(len(gm))) if len(gm) > 2 else np.nan
    return 1e4 * x[v].mean(), t, len(x)

def summ(E, cls, lab):
    s = E[E[cls]]
    r = {'cls': cls, 'grp': lab, 'n': len(s), 'ndays': s.date.nunique()}
    for v in ['gap_1', 'intra_1', 'dr2_5']:
        m, t, n = ct(s, v); r[v] = round(m, 1); r[v + '_t'] = round(t, 1)
    s2 = s.assign(gx=s.gap_1 - s.xgap_1, ix=s.intra_1 - s.xintra_1)
    for v in ['gx', 'ix']:
        m, t, n = ct(s2, v); r[v] = round(m, 1); r[v + '_t'] = round(t, 1)
    r['p_gap_pos'] = round((s.gap_1.dropna() > 0).mean(), 3)
    r['p_next_TC'] = round(s.TC_1.astype(float).mean(), 3); r['p_next_BC'] = round(s.BC_1.astype(float).mean(), 3)
    return r

if __name__ == '__main__':
    E = build()
    pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
    S177 = set(pd.read_parquet(SCR + '/out/code_y_akis/res_limit_events.parquet', columns=['stock']).stock)
    out = []
    for reg in ['P10', 'P20']:
        Er = E[E.reg == reg]
        for c_ in ['TC', 'TC_B', 'TC_S', 'TCL', 'TU', 'UP6', 'BC', 'BC_B', 'BCL', 'BU', 'DN6']:
            out.append(dict(reg=reg, **summ(Er, c_, 'all217')))
            if reg == 'P10':
                out.append(dict(reg=reg, **summ(Er[Er.stock.isin(S177)], c_, 'src177')))
                out.append(dict(reg=reg, **summ(Er[Er.viop], c_, 'viop47')))
                out.append(dict(reg=reg, **summ(Er[Er.age >= 40], c_, 'noIPO40')))
                out.append(dict(reg=reg, **summ(Er[Er.date < '2021-01-01'], c_, 'IS_2020')))
                out.append(dict(reg=reg, **summ(Er[Er.date >= '2021-01-01'], c_, 'OOS_21_26')))
                out.append(dict(reg=reg, **summ(Er[Er.date < '2023-01-01'], c_, 'IS_20_22')))
                out.append(dict(reg=reg, **summ(Er[Er.date >= '2023-01-01'], c_, 'OOS_23_26')))
    S = pd.DataFrame(out); S.to_csv(HERE + '/res_v1_summary.csv', index=False)
    print(S.to_string())
