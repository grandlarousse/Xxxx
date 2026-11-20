"""Betimleme: kontrat×yıl likidite, uzlaşma−son fark, baz/taşıma, vadeli−spot getiri farkı. Çıktı: ek/a6_viop_likidite.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import elib, front_wide, ca_mask, TRIO
panel, out = sys.argv[1], sys.argv[2]
P = elib.load(panel)
vf = P['viop_front'].copy(); vf['date'] = pd.to_datetime(vf['date'])
vd = P['viop_daily'].copy(); vd['date'] = pd.to_datetime(vd['date'])
cal = P['ret_cc'].index
rows = []
for u in TRIO + ['XU030']:
    x = vf[vf.und == u].set_index('date').sort_index()
    if not len(x):
        continue
    if u == 'XU030':
        spot = P['idx']['XU030'].reindex(x.index); rs = P['idx_ret']['XU030'].reindex(x.index)
        cm = pd.Series(False, index=x.index)
        tick = 0.25 / x.fiyat_carpani  # endeks vadelisi adımı: bugünkü ölçekte 0,25 puan
    else:
        spot = P['close_raw'][u].reindex(x.index); rs = P['ret_cc'][u].reindex(x.index)
        cm = ca_mask(P, [u])[u].reindex(x.index)
        tick = pd.Series(elib.tick_of(x.uzlasma.values, elib.TICK_TABLE_FUT), index=x.index)
    lvl = x.uzlasma * (x.fiyat_carpani if u == 'XU030' else 1.0)
    lvl_last = x.kapanis * (x.fiyat_carpani if u == 'XU030' else 1.0)
    baz = np.log(lvl / spot)
    baz_l = np.log(lvl_last / spot)
    carry = baz / (x.vkg.clip(lower=1) / 365.0)
    sl = 1e4 * (x.uzlasma / x.kapanis - 1)
    dif = (x.ret_settle - rs).where(~cm)
    difl = (x.ret_last - rs).where(~cm)
    gap = pd.Series(x.index, index=x.index).diff().dt.days
    tick_bps = 1e4 * tick / x.uzlasma
    # bütün vadelerde işlemsiz kontrat-gün oranı
    d = vd[vd.und == u]
    for yr, g in list(x.groupby(x.index.year)) + [('hepsi', x)]:
        i = g.index
        calu = cal[(cal >= i.min()) & (cal <= i.max())]
        dd = d[d.date.isin(i)]
        rows.append({
            'kontrat': u, 'yil': yr, 'gun': len(g), 'ilk': i.min().date(), 'son': i.max().date(),
            'hacim_tl_ort_mn': g.toplam_hacim_tl.mean() / 1e6, 'hacim_tl_medyan_mn': g.toplam_hacim_tl.median() / 1e6,
            'hacim_tl_p10_mn': g.toplam_hacim_tl.quantile(.10) / 1e6,
            'spot_hacim_medyan_mn': (P['vol_tl'][u].reindex(i).median() / 1e6) if u != 'XU030' else np.nan,
            'islem_sayisi_medyan': g.islem_sayisi.median(), 'islem_sayisi_p10': g.islem_sayisi.quantile(.10),
            'acik_poz_medyan': g.toplam_acik_poz.median(),
            'acik_poz_tl_medyan_mn': (g.toplam_acik_poz * g.uzlasma * (100 if u != 'XU030' else 10 * g.fiyat_carpani)).median() / 1e6,
            'islemsiz_gun_orani': float(1 - len(set(i[g.hacim_tl.fillna(0) > 0])) / max(len(calu), 1)),
            'islemsiz_kontrat_gun_orani_tum_vadeler': float((dd.hacim_tl.fillna(0) == 0).mean()) if len(dd) else np.nan,
            'islem_lt100_gun_orani': float((g.islem_sayisi < 100).mean()),
            'uzl_eksi_son_ort_bps': sl[i].mean(), 'uzl_eksi_son_medyan_bps': sl[i].median(),
            'uzl_eksi_son_mutlak_ort_bps': sl[i].abs().mean(), 'uzl_eksi_son_p5_bps': sl[i].quantile(.05),
            'uzl_eksi_son_p95_bps': sl[i].quantile(.95), 'uzl_esit_son_oran': float((sl[i].abs() < 1e-9).mean()),
            'baz_uzl_medyan_bps': 1e4 * baz[i].median(), 'baz_son_medyan_bps': 1e4 * baz_l[i].median(),
            'baz_uzl_p5_bps': 1e4 * baz[i].quantile(.05), 'baz_uzl_p95_bps': 1e4 * baz[i].quantile(.95),
            'tasima_yillik_medyan_yuzde': 100 * carry[i][g.vkg >= 5].median(),
            'vkg_medyan': g.vkg.median(),
            'vadeli_eksi_spot_gunluk_ort_bps': 1e4 * dif[i].mean(), 'vadeli_eksi_spot_gunluk_medyan_bps': 1e4 * dif[i].median(),
            'vadeli_eksi_spot_son_fiyat_ort_bps': 1e4 * difl[i].mean(),
            'vadeli_eksi_spot_haftaici_ort_bps': 1e4 * dif[i][gap[i] == 1].mean(),
            'vadeli_eksi_spot_haftasonu_ort_bps': 1e4 * dif[i][gap[i] >= 3].mean(),
            'dbaz_uzl_std_bps': 1e4 * dif[i].std(), 'dbaz_son_std_bps': 1e4 * difl[i].std(),
            'vadeli_spot_getiri_kor': float(pd.concat([x.ret_settle[i], rs[i]], axis=1).corr().iloc[0, 1]),
            'fiyat_adimi_medyan_bps': float(pd.Series(tick_bps, index=x.index)[i].median()),
            'uzlasma_medyan': g.uzlasma.median(),
            'limit_gun_orani': float((g.ret_settle.abs() >= 0.095).mean()),
        })
df = pd.DataFrame(rows)
os.makedirs(os.path.dirname(out), exist_ok=True)
df.to_csv(out, index=False, float_format='%.4g')
pd.set_option('display.width', 280); pd.set_option('display.max_columns', 60); pd.set_option('display.max_rows', 200)
print(df.round(2).T.to_string())
