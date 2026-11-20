#!/usr/bin/env python3
"""V6 iş 3 — dolum gerçekçiliği: sinyal günlerinde sepet hisselerinin kapanışa kadarki durumu.
 A) tavan kilidi: 17:30'da tavanda olmayıp tavanda kapanan (alım dolmaz), tavana ≤ %1 yakın kapanan
 B) giriş fiyatı: kapanış ile 17:30 / 17:50 / 17:50–17:59 ortalaması / 18:00 son fiyat arasındaki fark
    (hisse: Yahoo saatlik 2023-12+, 5 dk son ~60 gün; endeks düzeyi: XELKT 5 dk, 2017+)
 C) çıkış günü (t+3) kapanışında taban kilidi sıklığı
Sinyal günleri = KAPANIŞ sinyali (S1, S2: sektör sepeti; S3: AKSEN/ENJSA/ODAS).
Kullanım: python3 -I t3_dolum.py <panel_full> <cikti.csv>"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I ile betik klasörü yola eklenmez
import v6lib as V  # noqa: E402
from v6lib import elib, vekil  # noqa: E402

H1_BAS = pd.Timestamp('2023-12-21')
SON = pd.Timestamp('2100-01-01')
rows = []


def ekle(olcu, grup, donem, deger, n, birim, not_=''):
    rows.append({'is': 'dolum', 'olcu': olcu, 'grup': grup, 'donem': donem, 'deger': deger, 'n': n, 'birim': birim, 'not': not_})


def tmean(x):
    x = pd.Series(x).dropna()
    if len(x) < 3:
        return (float(x.mean()) if len(x) else np.nan), np.nan, len(x)
    return float(x.mean()), float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))), len(x)


def main():
    panel, cikti = sys.argv[1], sys.argv[2]
    P = elib.load(panel)
    G = V.gunluk(P)
    kapE, kapX = G['L']['XELKT'], G['L']['XU030']
    idx = P['ret_cc'].index
    sc = elib.sector_cols(P)
    v3 = [c for c in elib.VIOP if c in P["ret_cc"].columns]
    s1 = V.sinyal(G, kapE, kapX, 'S1', 0.0).reindex(idx).fillna(False)
    s2 = V.sinyal(G, kapE, kapX, 'S2', 1.0).reindex(idx).fillna(False)
    s3 = V.sinyal(G, kapE, kapX, 'S3', 1.0, 0.5).reindex(idx).fillna(False)
    hep = pd.Series(True, index=idx)
    GR = {'S1': (s1, sc), 'S2': (s2, sc), 'S1veyaS2': (s1 | s2, sc), 'S3': (s3, v3), 'tum_gunler': (hep, sc),
          'sinyalsiz': (~(s1 | s2), sc)}
    T = P['tradable']
    LU, LD, FL = P['lim_up'], P['lim_dn'], P['fill_long']

    # ---------- A) tavan kilidi
    up17, dn17, has17 = vekil.kilit_vekil(P, 'p_1730')
    # tavan fiyatı: dünkü ham kapanış × 1,10, fiyat adımına aşağı yuvarlanır (kurumsal işlem günleri hariç)
    C = P['close_raw']
    base = C.shift(1)
    ham = base * 1.10
    tick = pd.DataFrame(elib.tick_of(ham.values), index=C.index, columns=C.columns)
    tavan = (np.floor(ham / tick + 1e-6) * tick).where(~P['ca_day'].reindex_like(C).fillna(False))
    tut = float((C[LU] >= tavan[LU] - 1e-6).stack().mean())          # tavan fiyatı kestiriminin sağlaması
    yakin = (C >= tavan * 0.99) & ~LU
    for g, (s, cols) in GR.items():
        for dn, a, b in (('2017+', V.BAS, SON), ('IS17', V.BAS, elib.IS_END), ('H2023', elib.OOS1_START, SON),
                         ('KASA', elib.KASA_START, SON), ('2023-12-21+', H1_BAS, SON)):
            m = s & (idx >= a) & (idx <= b)
            U = T.loc[m, cols]
            n = int(U.values.sum())
            if n == 0:
                continue
            ekle('tavanda_kapanan_oran', g, dn, float(LU.loc[m, cols].where(U).stack().mean()), n, 'oran',
                 'tradable hisse-gün içinde tavanda kapanan: kapanışta alım dolmaz')
            ekle('tavana_1pct_yakin_kilitsiz_oran', g, dn, float(yakin.loc[m, cols].where(U).stack().mean()), n, 'oran',
                 f'kapanış ≥ tavan×0,99, kilitsiz; tavan kestirimi tavan günlerinin %{100 * tut:.0f}ünde tutuyor')
            gun = (LU.loc[m, cols] & U).sum(axis=1) / U.sum(axis=1).replace(0, np.nan)
            ekle('sepetin_tavandaki_payi_gun_ort', g, dn, float(gun.mean()), int(m.sum()), 'oran', 'günlük sepet içinde kilitli pay ortalaması')
            ekle('sepetin_tavandaki_payi_gun_p90', g, dn, float(gun.quantile(0.9)), int(m.sum()), 'oran', '')
        m = s & (idx >= H1_BAS)
        U = T.loc[m, cols] & has17.loc[m, cols]
        n = int(U.values.sum())
        if n:
            lu, u17 = LU.loc[m, cols] & U, up17.loc[m, cols] & U
            ekle('tavan_1730da_yok_kapanista_var_oran', g, '2023-12-21+', float((lu & ~u17).values.sum() / n), n, 'oran',
                 '17:30\'da tavanda değil, tavanda kapandı (17:30\'da görülemeyen dolmama)')
            ekle('tavan_1730da_var_kapanista_var_oran', g, '2023-12-21+', float((lu & u17).values.sum() / n), n, 'oran', '')
            ekle('tavan_1730da_var_kapanista_yok_oran', g, '2023-12-21+', float((~lu & u17).values.sum() / n), n, 'oran', '')
            ekle('tavan_kapanisinin_1730_sonrasi_olusan_payi', g, '2023-12-21+',
                 float((lu & ~u17).values.sum() / max(lu.values.sum(), 1)), int(lu.values.sum()), 'oran', '')

    I = V.endeks_gunici(P)
    E5 = I['E5']

    def karar(T):
        """Karar anındaki (T) XELKT değeriyle kurulan S1 / S2 sinyali: fiyat farkı için ileriye bakmayan koşullama.
        (Kapanış sinyali günleri tanım gereği son dakikaların yükseldiği günleri seçer.)"""
        v = E5[T].dropna()
        a = V.sinyal(G, v, None, 'S1', 0.0).reindex(idx).fillna(False)
        b = V.sinyal(G, v, None, 'S2', 1.0).reindex(idx).fillna(False)
        return {'S1_karar_ani': (a, sc), 'S2_karar_ani': (b, sc), 'S1veyaS2_karar_ani': (a | b, sc)}

    # ---------- B) giriş fiyatı farkı (kapanış / gün içi fiyat − 1), dolabilir sepet, günlük eşit ağırlık
    pc = vekil.snap_fiyat(P, 'p_close').reindex(index=idx)
    sn = P['snap'].assign(date=pd.to_datetime(P['snap']['date']))
    m5gun = sn[sn.bar_1750 == '17:45'].pivot(index='date', columns='sym', values='bar_1750').notna().reindex(index=idx).fillna(False)
    fiy = {'1730': vekil.snap_fiyat(P, 'p_1730').reindex(index=idx[idx >= H1_BAS]).reindex(index=idx),
           '1800son': vekil.snap_fiyat(P, 'p_son').reindex(index=idx),
           '1750_5dk': vekil.snap_fiyat(P, 'p_1750').reindex(index=idx).where(m5gun)}
    # 17:50–17:59 hacim ağırlıklı ortalama (5 dk barları 17:50 ve 17:55; tipik fiyat), ham ölçek
    car = sn.pivot(index='date', columns='sym', values='yahoo_carpan')
    art = vekil.yahoo_artik(P)
    vw = {}
    for c in sc:
        f = os.path.join(str(P['dir']), 'm5', c + '.parquet')
        if not os.path.exists(f):
            continue
        d = pd.read_parquet(f)
        d['ts_tr'] = pd.to_datetime(d['ts_tr'])
        mn = d.ts_tr.dt.hour * 60 + d.ts_tr.dt.minute
        d = d[(mn >= 17 * 60 + 50) & (mn < 18 * 60)].copy()
        d['date'] = d.ts_tr.dt.normalize()
        d['tp'] = (d.h + d.l + d.c) / 3
        d['w'] = d.v.clip(lower=0).fillna(0) + 1e-9
        x = d.groupby('date').apply(lambda z: float((z.tp * z.w).sum() / z.w.sum()), include_groups=False)
        k = car[c].reindex(x.index).fillna(1.0) if c in car.columns else 1.0
        a = art[c].reindex(x.index).fillna(1.0) if c in art.columns else 1.0
        vw[c] = x / k / a
    fiy['1750_1759_ort_5dk'] = pd.DataFrame(vw).reindex(index=idx)
    KT = {'1730': '1730', '1800son': '1800', '1750_5dk': '1750', '1750_1759_ort_5dk': '1750'}
    for ad, p in fiy.items():
        q = (pc.reindex(columns=p.columns) / p - 1) * 1e4
        q = q.where(q.abs() < 1500)
        for g, (s, cols) in {**GR, **karar(KT[ad])}.items():
            cc = [c for c in cols if c in q.columns]
            Q = q.loc[s, cc].where(FL.loc[s, cc])
            gun = Q.mean(axis=1).where(Q.notna().sum(axis=1) >= min(5, len(cc)))
            mu, t, n = tmean(gun)
            if n == 0:
                continue
            ekle(f'kapanis_eksi_{ad}_bps', g, 'veri dönemi', mu, n, 'bps',
                 f't={t:.1f}; hisse düzeyi medyan |fark| {float(Q.stack().abs().median()):.0f} bps; artı = kapanış daha pahalı '
                 f'(erken alan kazanır); ilk gün {gun.dropna().index.min().date()}')
            if ad in ('1730', '1800son'):
                gk = gun[gun.index >= elib.KASA_START]
                mu, t, n = tmean(gk)
                if n:
                    ekle(f'kapanis_eksi_{ad}_bps', g, 'KASA', mu, n, 'bps', f't={t:.1f}')
    # endeks düzeyi (XELKT, 2017+): kapanış / gün içi değer − 1
    KE = {'1730': '1730', '1750': '1750', '1755': '1755', '1800son': '1800', '1750_1759_ort': '1750'}
    e = {'1730': E5['1730'], '1750': E5['1750'], '1755': E5['1755'], '1800son': E5['1800'],
         '1750_1759_ort': E5[['1750', '1755', '1800']].mean(axis=1, skipna=False)}
    for ad, v in e.items():
        q = (kapE.reindex(v.index) / v - 1) * 1e4
        GK = {**GR, **karar(KE[ad])}
        for g in ('S1', 'S2', 'S1veyaS2', 'S1_karar_ani', 'S2_karar_ani', 'S1veyaS2_karar_ani', 'sinyalsiz', 'tum_gunler'):
            s = GK[g][0].reindex(q.index).fillna(False)
            for dn, a, b in (('2017+', V.BAS, SON), ('IS17', V.BAS, elib.IS_END), ('H2023', elib.OOS1_START, SON), ('KASA', elib.KASA_START, SON)):
                x = q[s & (q.index >= a) & (q.index <= b)]
                mu, t, n = tmean(x)
                ekle(f'XELKT_kapanis_eksi_{ad}_bps', g, dn, mu, n, 'bps', f't={t:.1f}; medyan |fark| {float(x.abs().median()):.0f} bps')

    # ---------- C) çıkış günü (t+3) taban kilidi
    f3, fill, gec = elib.fwd_exec(P, 3, 'long', sc)
    ld3 = LD[sc].shift(-3)
    for g, (s, cols) in GR.items():
        for dn, a, b in (('2010+', pd.Timestamp('2000-01-01'), SON), ('IS17', V.BAS, elib.IS_END), ('OOS1', elib.OOS1_START, elib.OOS1_END),
                         ('KASA', elib.KASA_START, SON), ('H2023', elib.OOS1_START, SON)):
            m = s & (idx >= a) & (idx <= b)
            U = FL.loc[m, cols] & ld3.loc[m, cols].notna()
            n = int(U.values.sum())
            if n == 0:
                continue
            k = (ld3.loc[m, cols].fillna(False).astype(bool) & U).values.sum()
            ekle('cikis_gunu_t3_tabanda_kilit_oran', g, dn, float(k / n), n, 'oran', f'{int(k)} işlem; çıkış ertesi kilitsiz kapanışa kayar')
            gg = (ld3.loc[m, cols].fillna(False).astype(bool) & U).sum(axis=1)
            ekle('cikis_gunu_t3_en_az_bir_taban_gun_orani', g, dn, float((gg > 0).mean()), int(m.sum()), 'oran', '')

    R = pd.DataFrame(rows)
    R.to_csv(cikti, index=False)
    pd.set_option('display.width', 250, 'display.max_rows', 900, 'display.max_colwidth', 90)
    R['deger'] = R['deger'].round(4)
    print(R.drop(columns=['is', 'birim']).to_string(index=False))


if __name__ == '__main__':
    main()
