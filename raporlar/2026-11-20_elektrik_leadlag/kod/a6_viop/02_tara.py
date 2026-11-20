"""Izgara taraması (yalnız IS paneli). Çıktı: ek/a6_viop_sonuc.csv (bütün satırlar) + özet."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import elib
import rules

panel, out = sys.argv[1], sys.argv[2]
P = elib.load(panel)
SPLIT = pd.Timestamp('2020-01-01')


def halves(p):
    """p: günlük portföy fazla getirisi (sinyal günleri). Sabit bölme (≤2019 / 2020+) ve kronolojik yarı."""
    p = p.dropna()
    a, b = p[p.index < SPLIT], p[p.index >= SPLIT]
    k = len(p) // 2
    c, d = p.iloc[:k], p.iloc[k:]
    dv = p.sort_values(); kk = max(10, int(np.ceil(0.05 * len(dv))))
    return {'yari_sabit1_bps': 1e4 * a.mean() if len(a) else np.nan, 'yari_sabit1_n': len(a),
            'yari_sabit2_bps': 1e4 * b.mean() if len(b) else np.nan, 'yari_sabit2_n': len(b),
            'yari_krono1_bps': 1e4 * c.mean() if len(c) else np.nan, 'yari_krono2_bps': 1e4 * d.mean() if len(d) else np.nan,
            'top10_haric_bps': 1e4 * dv.iloc[:-kk].mean() if len(dv) > kk + 5 else np.nan}


def spot_extra(r, cols):
    M, fl = elib.excess_measures(P, r['h'], r['yon'], cols)
    p, _, _ = elib.day_series(r['sig'][cols].reindex(P['ret_cc'].index).fillna(False), M['own'], fl, r.get('min_n', 1))
    x = halves(p); x.pop('top10_haric_bps')
    return x


def viop_extra(r):
    """evaluate_viop ile aynı tanım (vadeli fiyatı, own_vadeli, dolum); iki fiyat tanımı için yarılar, top10 hariç, t+1 girişi, hisse payı."""
    cols = [c for c in r['sig'].columns if c in elib.VIOP]
    sig = r['sig'][cols].reindex(P['ret_cc'].index).fillna(False).astype(bool)
    sgn = 1.0 if r['yon'] == 'long' else -1.0
    vol = elib.viop_volume(P)[cols]
    res = {}
    for kind in ['settle', 'last']:
        rr = elib.viop_returns(P, kind)[cols]
        L = elib.level(rr); f = L.shift(-r['h']) / L - 1
        own = (f - elib.bench_own(f, r['h'])) * sgn
        fillable = (vol > 0) & rr.notna() & ~(rr.abs() >= 0.095) & (P['fill_long'] if r['yon'] == 'long' else P['fill_short'])[cols]
        p, ntr, X = elib.day_series(sig, own, fillable)
        hv = halves(p)
        p1, _, _ = elib.day_series(sig.shift(1, fill_value=False), own, fillable)
        hv['giris_kapanis1_bps'] = 1e4 * p1.mean()
        cnt = X.notna().sum()
        hv['en_yogun_hisse'] = cnt.idxmax() if cnt.sum() else ''
        hv['en_yogun_pay'] = float(cnt.max() / max(cnt.sum(), 1))
        for c in cols:
            v = X[c].dropna()
            hv[f'{c}_bps'] = 1e4 * v.mean() if len(v) else np.nan; hv[f'{c}_n'] = len(v)
        res[kind] = hv
    o = {}
    for k in res['settle']:
        if k in ('en_yogun_hisse', 'en_yogun_pay') or k.endswith('_n'):
            o[k] = res['settle'][k]
        else:
            o[k] = np.nanmin([res['settle'][k], res['last'][k]]) if not (np.isnan(res['settle'][k]) and np.isnan(res['last'][k])) else np.nan
            o['uzl_' + k] = res['settle'][k]; o['son_' + k] = res['last'][k]
    return o


NOTLAR = {
    'V4_getiri_z1.0_yuk_spotAL_h2': 'yedi ölçütün hepsini karşılıyor; aile düzeyi yer değiştirme p=0,28 (234 testin en iyisi şansla açıklanabilir); vadeliye özgü değil, akran öncülüğü',
    'V4_getiri_z1.0_yuk_spotAL_h3': 'birincilin komşusu (h=3)',
    'V4_getiri_z1.0_yuk_viopAL_h2': 'birincilin vadeli uygulaması; IS geçmişi kısa (2021-04+), t<1, top10 hariç negatif',
    'V1_settle_z1.5_yuk_spotAL_h2': 'en yüksek V1 t; yalnız 37 olay; son fiyat tanımında zayıf (net +23); top10 hariç ≈ 0',
    'V1_settle_z1.0_yuk_spotAL_h3': 'kontrol regresyonunda t=1,3; etkinin çoğu ODAS ve XU100 yukarı günleri',
    'V2_hacim_yuk_spotAL_h3': '53 olay; top10 hariç +11; tek parametre noktası (komşu h=2 t=1,7); t+1 girişinde büyüyor (momentum)',
    'V4K_getiri_z1.0_yuk_kendiz_lt1_spotAL_h2': 'KEŞİF: sonuç görüldükten sonra tanımlandı; aday olamaz, yalnız OOS/kasa için öneri',
}


def neden(x, r):
    if not x.get('karar_satiri', True):
        return 'bilgi satırı (spot fiyatı, VİOP maliyeti); karar vadeli fiyatlı satırda'
    if r['ad'] in NOTLAR:
        return NOTLAR[r['ad']]
    g = lambda k: x.get(k, np.nan)
    n = []
    if not g('n_bagimsiz_IS') >= 40: n.append('olay<40')
    if not g('net_temel_bps_IS') > 0: n.append('net≤0')
    if not g('t_IS') >= 2: n.append('t<2')
    if not (g('yari_krono1_bps') > 0 and g('yari_krono2_bps') > 0): n.append('yarılar tutarsız')
    if not g('top10_haric_bps') > 0: n.append('top10 hariç ≤0')
    if not g('giris_kapanis1_bps') > 0: n.append('t+1 girişinde kayboluyor')
    return '; '.join(n) if n else 'ölçütleri sayısal olarak geçiyor ama komşu/aynı sinyalin daha güçlü hücresi donduruldu ya da olay sayısı düşük'


t0 = time.time()
G = rules.grid(P) + rules.kesif(P)
frozen = rules.FROZEN
rows = []
for r in G:
    rs = elib.eval_rule(r, P, family=r['aile'])
    cols = [c for c in r['sig'].columns if c in P['ret_cc'].columns]
    if r['arac'] == 'viop':
        cols = [c for c in cols if c in elib.VIOP]
    rs[0].update(spot_extra(r, cols))
    for c in (cols if len(cols) <= 3 else []):
        M, fl = elib.excess_measures(P, r['h'], r['yon'], cols)
        v = M['own'][c].where(r['sig'][c].reindex(P['ret_cc'].index).fillna(False) & fl[c]).dropna()
        rs[0][f'{c}_bps'] = 1e4 * v.mean() if len(v) else np.nan; rs[0][f'{c}_n'] = len(v)
    if len(rs) > 1:
        rs[1].update(viop_extra(r))
        rs[1]['net_temel_bps_IS'] = min(rs[1]['settle_net_temel_IS_bps'], rs[1]['last_net_temel_IS_bps'])
        rs[1]['maliyet_temel_bps'] = rs[1]['settle_maliyet_temel_bps']
        rs[0]['karar_satiri'] = False; rs[1]['karar_satiri'] = True
    else:
        rs[0]['karar_satiri'] = True
    for x in rs:
        x['secim'] = ('birincil' if frozen[r['ad']][1] else 'ikincil') if r['ad'] in frozen else 'elendi'
        x['dondurulmus_ad'] = frozen[r['ad']][0] if r['ad'] in frozen else ''
        x['izgara'] = r['aile'] != 'V4-kesif'
        x['not'] = neden(x, r)
    rows += rs
df = pd.DataFrame(rows)
kar = df['karar_satiri'] & df['izgara']
df['bh_gecti'] = False
df.loc[kar, 'bh_gecti'] = elib.bh_fdr(df.loc[kar, 'p_tek_IS'].values, q=0.10)
df['test_sayisi_aile'] = int(kar.sum())
first = ['aile', 'sinyal_tanimi', 'hedef', 'yon', 'h', 'arac', 'karar_satiri', 'secim', 'not', 'n_gun_IS', 'n_bagimsiz_IS', 'ort_fazla_IS_bps', 't_IS',
         'p_tek_IS', 'bh_gecti', 'basabas_IS_bps', 'maliyet_temel_bps', 'net_temel_bps_IS', 'yari_sabit1_bps', 'yari_sabit1_n', 'yari_sabit2_bps',
         'yari_sabit2_n', 'yari_krono1_bps', 'yari_krono2_bps', 'top10_haric_bps', 'giris_kapanis1_bps', 'giris_acilis1_bps', 'gece_payi',
         'en_yogun_hisse', 'en_yogun_pay', 'dolabilir_oran', 'yil_pozitif_orani', 'yillar_bps']
df = df[[c for c in first if c in df.columns] + [c for c in df.columns if c not in first]]
os.makedirs(os.path.dirname(out), exist_ok=True)
elib.to_csv(df.to_dict('records'), out)
print(f'ızgara kuralı (test) sayısı: {int(kar.sum())}; keşif kuralı: {int((df.karar_satiri & ~df.izgara).sum())}; satır: {len(df)}; BH (q=0,10) geçen: {int(df.bh_gecti.sum())}; süre {time.time() - t0:.0f} sn')
k = df[df.karar_satiri]
print('t_IS > 2:', int((k.t_IS > 2).sum()), '| t_IS < -2:', int((k.t_IS < -2).sum()), '| en küçük tek yönlü p:', round(float(k.p_tek_IS.min()), 4))
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
print(df[df.secim != 'elendi'][['dondurulmus_ad', 'arac', 'secim', 'n_bagimsiz_IS', 'ort_fazla_IS_bps', 't_IS', 'net_temel_bps_IS', 'yari_krono1_bps', 'yari_krono2_bps',
      'top10_haric_bps', 'giris_kapanis1_bps', 'en_yogun_pay']].round(1).to_string(index=False))
kalan = k[(k.secim == 'elendi') & k['not'].str.startswith('ölçütleri')]
print('ölçütleri sayısal geçip dondurulmayan:', len(kalan)); print(kalan[['sinyal_tanimi', 'n_bagimsiz_IS', 't_IS', 'net_temel_bps_IS', 'top10_haric_bps', 'giris_kapanis1_bps']].round(1).to_string(index=False))
