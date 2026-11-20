"""V2 (d) EK: T1 (A8 LightGBM) icin deneysel denetim. MODEL YENIDEN YAZILMADI: sinyal ana ajanin kodundan (kod/a8_model/rules.py + elib)
uretilir; burada yalniz (i) kesme sinamasi (panel 2025-06-30'da kesilince o tarihe kadarki sinyal degisiyor mu) ve
(ii) ayni sinyalin V2'nin kendi getirisi ve kiyaslariyla okunmasi yapilir. T2/K1/K2 yeniden uretiminde bu dosya KULLANILMAZ.
Kullanim: python3 -I 04_T1_denetim.py <WORK_DIR> <PANEL_FULL> <KOD_DIR> <EK_DIR> [PANEL_DEV]"""
import importlib.util
import os
import sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import v2lib as L  # noqa: E402

WORK, PF, KOD, EK = sys.argv[1:5]
PD_ = sys.argv[5] if len(sys.argv) > 5 else None
sys.path.insert(0, os.path.join(KOD, 'ortak'))
import elib  # noqa: E402
spec = importlib.util.spec_from_file_location('a8r', os.path.join(KOD, 'a8_model', 'rules.py'))
a8 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a8)
SP = a8.FROZEN[0]['spec']
assert a8.spec_name(SP) == 'A8_kesit_lgbm_d3_m500_h1_ust20'


def t1(P):
    fe = a8.features(P)
    cache = {}
    return a8.rule_sig(P, fe, SP, cache), a8.predict_sec(P, fe, 1, SP['cfg'], cache)


CUT = pd.Timestamp('2025-06-30')
Pf = elib.load(PF)
s_full, p_full = t1(Pf)
s_tr, p_tr = t1(elib.truncate(Pf, CUT))


def diff(a, b, pa, pb, name, end=CUT):
    idx = a.index[a.index <= end]
    cols = sorted(set(a.columns) & set(b.columns))
    x, y = a.reindex(index=idx, columns=cols).fillna(False), b.reindex(index=idx, columns=cols).fillna(False)
    d = x != y
    dp = (pa.reindex(index=idx, columns=cols) - pb.reindex(index=idx, columns=cols)).abs()
    byy = (d.sum(axis=1).groupby(idx.year).sum() / x.sum(axis=1).groupby(idx.year).sum().clip(lower=1)).round(3)
    fd = d.any(axis=1)
    print(f'{name}: farkli hucre {int(d.values.sum())} / sinyal {int(x.values.sum())} = {d.values.sum() / max(x.values.sum(), 1):.4f}'
          f' | tahmin maks fark {np.nanmax(dp.values):.2e} | ilk farkli gun {fd.idxmax().date() if fd.any() else None}')
    print('   yillara gore oran:', {int(k): float(v) for k, v in byy.items() if v > 0})
    return d


diff(s_tr, s_full, p_tr, p_full, 'KESME SINAMASI (ayni panel, 2025-06-30 kesik vs tam)')
s_dev = None
if PD_ and os.path.isdir(PD_):
    Pd = elib.load(PD_)
    s_dev, p_dev = t1(Pd)
    diff(s_dev, s_full, p_dev, p_full, 'panel_dev vs panel_full (ana ajanin nedensellik_oran sinamasi)')
    sc = sorted(set(elib.sector_cols(Pd)) & set(elib.sector_cols(Pf)))
    for k in ('ret_cc', 'vol_tl', 'lim_up', 'lim_dn', 'lim_up_touch', 'tradable', 'fill_long'):
        A, B = Pd[k][sc], Pf[k][sc].reindex(Pd[k].index)
        if A.dtypes.iloc[0] == bool:
            print(f'   girdi farki {k}: {int((A != B).values.sum())} hucre')
        else:
            dd = (A - B).abs()
            r4 = (A.round(4) != B.round(4)) & A.notna() & B.notna()
            print(f'   girdi farki {k}: maks {np.nanmax(dd.values):.3e}, > 1e-12 hucre {int((dd > 1e-12).values.sum())}, yuvarlanmis (4 hane) farkli {int(r4.values.sum())},'
                  f' biri bos {int((A.isna() != B.isna()).values.sum())}')
    I = (Pd['idx_ret'][['XU030', 'XELKT']] - Pf['idx_ret'][['XU030', 'XELKT']].reindex(Pd['idx_ret'].index)).abs()
    print('   girdi farki idx_ret: maks', float(np.nanmax(I.values)))

# ---- (ii) ayni sinyal, V2 getirisi ve kiyaslari
P = pd.read_pickle(os.path.join(WORK, 'v2_panel.pkl'))
fill = P['fill']
f_sh, f_no = L.fwd(P, 1, True, 5), L.fwd(P, 1, False)
flag = (P['tu'] & ~P['lu']) | (P['td'] & ~P['ld']) | P['ld']
E = {'ortak': L.sec_excess(f_sh, fill), 'kaydirma_yok': L.sec_excess(f_no, fill), 'kiyas_tabansiz': L.sec_excess(f_sh, fill & ~P['ld']),
     'kiyas_bayraksiz': L.sec_excess(f_sh, fill & ~flag), 'kaydirma_yok_kiyas_tabansiz': L.sec_excess(f_no, fill & ~P['ld'])}
rows = []
sigs = {'T1_panel_full': s_full}
if s_dev is not None:
    sigs['T1_panel_dev'] = s_dev
for sn, s in sigs.items():
    s = s.reindex(index=fill.index, columns=fill.columns).fillna(False).astype(bool) & fill
    for vn, Ex in E.items():
        for pn, (a, b) in L.PERIODS.items():
            st = L.stats(Ex, s, a, b)
            rows.append(dict(sinyal=sn, surum=vn, donem=pn, n_gun=st['n_gun'], n_islem=st['n_islem'], ort_bps=round(st['ort_bps'], 2), t=round(st['t'], 2),
                             medyan_islem_bps=round(st['medyan_islem_bps'], 2), isabet_islem=round(st['isabet_islem'], 4)))
    k = s.index >= L.KASA_START
    print(f'{sn}: kasada secilenlerde tabanda kapanan pay {float((s & P["ld"])[k].values.sum() / max(s[k].values.sum(), 1)):.4f}'
          f' | bayrakli pay {float((s & flag)[k].values.sum() / max(s[k].values.sum(), 1)):.4f} | dolabilir evrende tabanda kapanan pay'
          f' {float((fill & P["ld"])[k].values.sum() / fill[k].values.sum()):.4f}')
r = pd.DataFrame(rows)
r.to_csv(os.path.join(EK, 'v2_yeniden_kesit_T1_kiyas.csv'), index=False)
pd.set_option('display.width', 250)
print(r.pivot_table(index=['sinyal', 'surum'], columns='donem', values=['ort_bps', 't'])[[('ort_bps', 'IS'), ('t', 'IS'), ('ort_bps', 'OOS1'), ('t', 'OOS1'),
      ('ort_bps', 'KASA'), ('t', 'KASA'), ('ort_bps', 'HAVUZ2023'), ('t', 'HAVUZ2023')]].to_string())
