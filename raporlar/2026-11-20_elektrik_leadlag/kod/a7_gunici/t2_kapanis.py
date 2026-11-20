#!/usr/bin/env python3
"""T2 — kapanış seansı: (a) p_close/p_nokta − 1 dağılımı, (b) tavan/taban kilidinin geç oluşması/bozulması,
(c) kapanış seansı hacim payı (dolaylı tahmin).
Kullanım: python3 -I t2_kapanis.py <panel> <ek_klasoru>
Çıktılar: a7_kapanis_sapma.csv, a7_kilit_gecis.csv, a7_kapanis_hacim.csv

Hacim yöntemi: Yahoo saatlik barlarında kapanış seansı yok; ayrıca yaz saati aylarında ilk barın (09:30) hacmi 0,
kış aylarında 17:30 barı eksik. Günlük hacim = A (09:30 barı) + B (10:30–16:30 barları) + C (17:30 barı) + K (kapanış seansı).
  kış günü  : günlük − Σbar = C + K        yaz günü : günlük − Σbar = A + K
  K_kış = (C+K)_kış − C_yaz payı ;  K_yaz = (A+K)_yaz − A_kış payı   (paylar günlük hacme oranla, medyan)
İki tahmin de mevsimler arası pay sabitliği varsayar: DOLAYLI tahmindir.
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vekil  # noqa: E402
from vekil import elib  # noqa: E402

BAS = pd.Timestamp('2023-12-21')


def main():
    panel, ek = sys.argv[1], sys.argv[2]
    P = elib.load(panel)
    R = P['ret_cc']
    idx = R.index[R.index >= BAS]
    sc = elib.sector_cols(P, extra=True)
    xel = elib.sector_cols(P)
    meta = P['meta'].set_index('sym')
    tr = P['tradable'].loc[idx, sc]
    kilitsiz = tr & ~P['lim_up'].loc[idx, sc] & ~P['lim_dn'].loc[idx, sc]
    pc = vekil.snap_fiyat(P, 'p_close').reindex(index=idx, columns=sc)
    tick = pd.DataFrame(elib.tick_of(pc.values), index=idx, columns=sc)
    tick_bps = tick / pc * 1e4
    # ---------------- (a) sapma dağılımı
    rows = []
    for ad, kol in (('1730', 'p_1730'), ('1800son', 'p_son')):
        px = vekil.snap_fiyat(P, kol).reindex(index=idx, columns=sc)
        D = (pc / px - 1).where(kilitsiz) * 1e4
        rn = (1 + R.loc[idx, sc]) * (px / pc) - 1                    # nokta anındaki gün getirisi (kapanışı bilmeden)
        sgn, big = np.sign(rn), rn.abs() >= 0.03                     # "büyük gün" = nokta anında |r| ≥ %3 (seçim yanlılığı yok)
        for s in sc + ['HAVUZ']:
            if s == 'HAVUZ':
                d = D[xel].stack().dropna()
                db = D[xel].where(big[xel]).stack().dropna()
                ds = (D[xel] * sgn[xel]).where(big[xel]).stack().dropna()
                tb = tick_bps[xel].where(D[xel].notna()).stack().dropna().median()
            else:
                d, db, ds = D[s].dropna(), D[s].where(big[s]).dropna(), (D[s] * sgn[s]).where(big[s]).dropna()
                tb = tick_bps[s].where(D[s].notna()).median()
            if len(d) < 30:
                continue
            a = d.abs()
            rows.append({'sym': s, 'nokta': ad, 'n': len(d), 'ort_bps': d.mean(), 'std_bps': d.std(),
                         'medyan_mutlak_bps': a.median(), 'p90_mutlak_bps': a.quantile(.9), 'p95_mutlak_bps': a.quantile(.95),
                         'p99_mutlak_bps': a.quantile(.99), 'pay_100bps_ustu': (a > 100).mean(), 'pay_sifir': (a < 1e-6).mean(),
                         'adim_bps_medyan': tb, 'n_buyuk_gun': len(db),
                         'buyuk_gun_medyan_mutlak_bps': db.abs().median() if len(db) else np.nan,
                         'buyuk_gun_yon_devam_bps': ds.mean() if len(ds) else np.nan})
    sap = pd.DataFrame(rows).round(3)
    sap.to_csv(os.path.join(ek, 'a7_kapanis_sapma.csv'), index=False)
    pd.set_option('display.width', 250, 'display.max_rows', 200, 'display.max_columns', 40)
    print(sap[sap.sym.isin(['HAVUZ', 'AKSEN', 'ENJSA', 'ODAS', 'ZOREN', 'AYDEM', 'AHGAZ'])].to_string(index=False))
    for ad in ('1730', '1800son'):
        x = sap[(sap.nokta == ad) & (sap.sym != 'HAVUZ')]
        print(ad, 'hisse bazında medyan_mutlak: min/medyan/max', x.medyan_mutlak_bps.min(), x.medyan_mutlak_bps.median(),
              x.medyan_mutlak_bps.max(), '| p95 medyan', x.p95_mutlak_bps.median(), '| en yüksek 3:',
              x.nlargest(3, 'medyan_mutlak_bps')[['sym', 'medyan_mutlak_bps']].values.tolist())
    # ---------------- (b) kilit geçişleri (yalnız XELKT üyeleri)
    rows = []
    for yon, kap, dok in (('tavan', 'lim_up', 'lim_up_touch'), ('taban', 'lim_dn', 'lim_dn_touch')):
        C = P[kap].loc[idx, xel] & tr[xel]
        T = (P[dok].loc[idx, xel] | P[kap].loc[idx, xel]) & tr[xel]
        for ad, kol in (('1730', 'p_1730'), ('1800son', 'p_son')):
            up, dn, var = vekil.kilit_vekil(P, kol)
            N = (up if yon == 'tavan' else dn).loc[idx, xel]
            V = var.loc[idx, xel]
            c, n, t = C & V, N & V & tr[xel], T & V
            for donem, m in (('tum', slice(None)), ('yari1', slice(None, idx[len(idx) // 2 - 1])), ('yari2', slice(idx[len(idx) // 2], None))):
                cc, nn, tt = c.loc[m].values, n.loc[m].values, t.loc[m].values
                rows.append({'yon': yon, 'nokta': ad, 'donem': donem, 'hisse_gun': int(V.loc[m].values.sum()),
                             'n_gun_ici_degen': int(tt.sum()), 'n_noktada_kilit': int(nn.sum()), 'n_kapanis_kilit': int(cc.sum()),
                             'n_ikisi': int((cc & nn).sum()), 'n_sonradan_olusan': int((cc & ~nn).sum()),
                             'n_bozulan': int((nn & ~cc).sum()),
                             'P_kapanis_kilit_kosul_noktada_kilit': (cc & nn).sum() / max(nn.sum(), 1),
                             'P_noktada_kilit_kosul_kapanis_kilit': (cc & nn).sum() / max(cc.sum(), 1),
                             'degip_kapanista_kilitsiz_orani': (tt & ~cc).sum() / max(tt.sum(), 1)})
    kg = pd.DataFrame(rows).round(3)
    kg.to_csv(os.path.join(ek, 'a7_kilit_gecis.csv'), index=False)
    print(kg.to_string(index=False))
    # kilit riski: nokta anında kilitli DEĞİL; o andaki gün getirisine göre kapanışta kilitlenme olasılığı
    rows = []
    for ad, kol in (('1730', 'p_1730'), ('1800son', 'p_son')):
        px = vekil.snap_fiyat(P, kol).reindex(index=idx, columns=xel)
        rn = ((1 + R.loc[idx, xel]) * (px / pc[xel]) - 1).where(tr[xel])
        up, dn, _ = vekil.kilit_vekil(P, kol)
        for yon, sg, N, C in (('tavan', 1, up, P['lim_up']), ('taban', -1, dn, P['lim_dn'])):
            x = (rn * sg).where(~N.loc[idx, xel])
            c = C.loc[idx, xel]
            for lo_, hi_ in ((-1, 0.03), (0.03, 0.05), (0.05, 0.07), (0.07, 0.09), (0.09, 1)):
                m = (x >= lo_) & (x < hi_)
                rows.append({'yon': yon, 'nokta': ad, 'nokta_getiri_araligi': f'{lo_:.2f}..{hi_:.2f}', 'hisse_gun': int(m.values.sum()),
                             'kapanista_kilit': int((m & c).values.sum()),
                             'olasilik': (m & c).values.sum() / max(m.values.sum(), 1)})
    kr = pd.DataFrame(rows).round(4)
    kr.to_csv(os.path.join(ek, 'a7_kilit_riski.csv'), index=False)
    print(kr.to_string(index=False))
    # örnek: kapanış seansında oluşan tavan kilitleri (18:00 son fiyatı ucun altında)
    up, _, var = vekil.kilit_vekil(P, 'p_son')
    m = (P['lim_up'] & ~up & var & P['tradable']).loc[idx, xel]
    ps, p17 = vekil.snap_fiyat(P, 'p_son'), vekil.snap_fiyat(P, 'p_1730')
    pxl = P['px'].assign(date=pd.to_datetime(P['px']['date'])).set_index(['date', 'sym'])
    ex = [(str(d.date()), s_, p17.loc[d, s_], ps.loc[d, s_], pxl.loc[(d, s_), 'h_raw'], pxl.loc[(d, s_), 'c_raw'],
           round(R.loc[d, s_], 4), bool(P['lim_up_exact'].loc[d, s_]) if 'lim_up_exact' in P else None) for d, s_ in m.stack()[lambda v: v].index[:12]]
    print(pd.DataFrame(ex, columns=['gun', 'sym', 'p_1730', 'p_son', 'h_raw', 'c_raw', 'r_cc', 'exact']).to_string(index=False))
    son_fark = (pc[xel] / ps.reindex(index=idx, columns=xel) - 1).where(m)
    print('kapanış seansında oluşan tavan: n=%d, kapanış/18:00 son fiyat − 1 medyan=%.4f, >%%1 payı=%.2f' % (
        int(m.values.sum()), son_fark.stack().dropna().median(), (son_fark.stack().dropna() > 0.01).mean()))
    print('lim_up & ~touch:', int((P['lim_up'] & ~P['lim_up_touch']).loc[idx].values.sum()),
          'lim_dn & ~touch:', int((P['lim_dn'] & ~P['lim_dn_touch']).loc[idx].values.sum()))
    # ---------------- (c) kapanış seansı hacim payı
    px = P['px'].copy()
    px['date'] = pd.to_datetime(px['date'])
    rows = []
    for s in sc:
        fp = os.path.join(panel, 'h1', s + '.parquet')
        if not os.path.exists(fp):
            continue
        h = pd.read_parquet(fp)
        h['date'] = h.ts_tr.dt.normalize()
        h['hm'] = h.ts_tr.dt.strftime('%H:%M')
        g = h.groupby('date').agg(v=('v', 'sum'), nb=('v', 'size'))
        g['v0930'] = h[h.hm == '09:30'].set_index('date')['v']
        g['v1730'] = h[h.hm == '17:30'].set_index('date')['v']
        d = px[px.sym == s].set_index('date')[['vol_adet', 'vol_tl']].join(g, how='inner')
        d = d[(d.vol_adet > 0) & (d.nb >= 8)]
        d['oran'] = d.v / d.vol_adet
        d = d[(d.oran > 0.3) & (d.oran <= 1.02)]
        kis = d[d.v1730.isna() & (d.v0930 > 0)]
        yaz = d[d.v1730.notna() & (d.v0930.fillna(0) == 0)]
        tam = d[d.v1730.notna() & (d.v0930 > 0)]
        if len(kis) < 20 or len(yaz) < 20:
            continue
        A = (kis.v0930 / kis.vol_adet).median()
        Cs = (yaz.v1730 / yaz.vol_adet).median()
        ck, ak = (1 - kis.oran).median(), (1 - yaz.oran).median()
        K1, K2 = ck - Cs, ak - A
        K = float(np.clip(np.nanmean([K1, K2]), 0, None))
        adv = d.vol_tl.rolling(20, min_periods=10).median().iloc[-1]
        rows.append({'sym': s, 'n_kis': len(kis), 'n_yaz': len(yaz), 'n_tam_gun': len(tam),
                     'pay_0930_bari': A, 'pay_1730_bari': Cs, 'kis_kalan_C_K': ck, 'yaz_kalan_A_K': ak,
                     'K_kis_tahmin': K1, 'K_yaz_tahmin': K2, 'K_ortalama': K,
                     'K_dogrudan_tam_gun': (1 - tam.oran).median() if len(tam) >= 5 else np.nan,
                     'pay_1730_sonrasi': ck, 'hacim_payi_1750': 1 - K - Cs / 3,
                     'gunluk_tl_medyan_20g': adv, 'kapanis_seansi_tl': K * adv,
                     'E9_sinir_tl_%1': 0.01 * adv, 'E9_sinir_kapanis_seansina_orani': 0.01 / K if K > 0 else np.nan,
                     'kapanisin_%10u_tl': 0.10 * K * adv})
    hv = pd.DataFrame(rows)
    hv.round(4).to_csv(os.path.join(ek, 'a7_kapanis_hacim.csv'), index=False)
    print(hv.round(3).to_string(index=False))
    x = hv[hv.sym.isin(xel)]
    print('XELKT üyeleri medyan:', x[['pay_0930_bari', 'pay_1730_bari', 'kis_kalan_C_K', 'yaz_kalan_A_K', 'K_kis_tahmin',
                                      'K_yaz_tahmin', 'K_ortalama', 'hacim_payi_1750', 'kapanis_seansi_tl',
                                      'E9_sinir_kapanis_seansina_orani', 'kapanisin_%10u_tl']].median().round(4).to_dict())
    print('K_ortalama çeyrekler:', x.K_ortalama.quantile([.1, .25, .5, .75, .9]).round(3).to_dict())


if __name__ == '__main__':
    main()
