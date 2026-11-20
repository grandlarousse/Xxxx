#!/usr/bin/env python3
"""T1 — sinyal vekili: r_cc(t) yerine r_nokta(t) = p_nokta(t)/p_close(t−1) − 1 kullanılınca korelasyon ve eşik
sinyallerinin kesinlik / yakalama oranı. Çıktı: ek/a7_vekil_tablosu.csv (uzun biçim).

Vekil noktaları (panel_dev'de 5 dk hisse verisi yok):
  hisse : 1730 (saatlik 16:30 barı kapanışı = 17:30 fiyatı; snap'te p_1750 de budur), 1800son (17:30 barı kapanışı =
          sürekli işlemin son fiyatı; yalnız yaz saati ayları). Gerçek 17:50 bu ikisinin arasındadır.
  XELKT : 1730, 1750 (gerçek, 5 dk), 1755son   |  XU030: 1700 (İş Yatırım saatlik), 1730 (Yahoo saatlik), 1750 (5 dk; 2017–2018/02)
Kullanım: python3 -I t1_vekil_tablosu.py <panel> <cikti.csv>
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vekil  # noqa: E402
from vekil import elib  # noqa: E402

H1_BAS = pd.Timestamp('2023-12-21')


def sinyaller(rt, rp, sd, lim=None):
    """rt, rp, sd: hizalı numpy dizileri. Dönen: [(sinyal, n_gercek, n_vekil, n_ortak)]."""
    zt, zp = rt / sd, rp / sd
    same = np.sign(rt) == np.sign(rp)
    out = []
    for ad, thr in (('abs3', 0.03), ('abs5', 0.05)):
        a, b = np.abs(rt) >= thr, np.abs(rp) >= thr
        out.append((ad, a.sum(), b.sum(), (a & b & same).sum()))
    for ad, thr in (('up3', 0.03), ('up5', 0.05)):
        a, b = rt >= thr, rp >= thr
        out.append((ad, a.sum(), b.sum(), (a & b).sum()))
    for ad, thr in (('dn3', -0.03), ('dn5', -0.05)):
        a, b = rt <= thr, rp <= thr
        out.append((ad, a.sum(), b.sum(), (a & b).sum()))
    ok = np.isfinite(zt) & np.isfinite(zp)
    for ad, thr in (('absz1', 1.0), ('absz1.5', 1.5), ('absz2', 2.0)):
        a, b = ok & (np.abs(zt) >= thr), ok & (np.abs(zp) >= thr)
        out.append((ad, a.sum(), b.sum(), (a & b & same).sum()))
    if lim is not None:
        for ad, (a, b) in lim.items():
            out.append((ad, a.sum(), b.sum(), (a & b).sum()))
    return out


def satirlar(sym, tur, vek, donem, rt, rp, sd, lim=None):
    ok = np.isfinite(rt) & np.isfinite(rp)
    if ok.sum() < 20:
        return []
    rt, rp, sd = rt[ok], rp[ok], sd[ok]
    lim = None if lim is None else {k: (a[ok], b[ok]) for k, (a, b) in lim.items()}
    corr = np.corrcoef(rt, rp)[0, 1]
    mad = np.median(np.abs(rt - rp)) * 1e4
    p95 = np.quantile(np.abs(rt - rp), 0.95) * 1e4
    rows = []
    for ad, na, nb, nt in sinyaller(rt, rp, sd, lim):
        rows.append({'sym': sym, 'tur': tur, 'vekil': vek, 'donem': donem, 'n_gun': int(ok.sum()), 'corr': round(corr, 4),
                     'medyan_mutlak_fark_bps': round(mad, 1), 'p95_mutlak_fark_bps': round(p95, 1), 'sinyal': ad,
                     'n_gercek': int(na), 'n_vekil': int(nb), 'n_ortak': int(nt),
                     'kesinlik': round(nt / nb, 3) if nb else np.nan, 'yakalama': round(nt / na, 3) if na else np.nan})
    return rows


def donemler(idx, bas=H1_BAS):
    idx = idx[idx >= bas]
    mid = idx[len(idx) // 2]
    return {'tum': (idx[0], idx[-1]), 'yari1': (idx[0], mid - pd.Timedelta(days=1)), 'yari2': (mid, idx[-1])}


def main():
    panel, out = sys.argv[1], sys.argv[2]
    P = elib.load(panel)
    R = P['ret_cc']
    sd = R.rolling(60, min_periods=30).std().shift(1)
    tr = P['tradable']
    per = donemler(R.index)
    rows, bant = [], []
    stocks = elib.sector_cols(P, extra=True)
    sc = elib.sector_cols(P)
    for vek, kol in (('1730', 'p_1730'), ('1800son', 'p_son')):
        q = vekil.snap_oran(P, kol).reindex(columns=R.columns)
        RP = ((1 + R) * q - 1).where(tr)
        RT = R.where(tr & q.notna())
        up, dn, _ = vekil.kilit_vekil(P, kol)
        for dn_ad, (a, b) in per.items():
            sl = slice(a, b)
            havuz = [[], [], [], [], [], [], []]
            for s in stocks:
                rt, rp, s_ = RT[s][sl].values, RP[s][sl].values, sd[s][sl].values
                lim = {'tavan': (P['lim_up'][s][sl].values, up[s][sl].values),
                       'taban': (P['lim_dn'][s][sl].values, dn[s][sl].values)}
                if dn_ad == 'tum':
                    rows += satirlar(s, 'hisse' if s in sc else 'komsu', vek, dn_ad, rt, rp, s_, lim)
                if s in sc:
                    for k, v in enumerate((rt, rp, s_, lim['tavan'][0], lim['tavan'][1], lim['taban'][0], lim['taban'][1])):
                        havuz[k].append(v)
            hv = [np.concatenate(x) for x in havuz]
            rows += satirlar('HAVUZ', 'havuz', vek, dn_ad, hv[0], hv[1], hv[2],
                             {'tavan': (hv[3], hv[4]), 'taban': (hv[5], hv[6])})
            if dn_ad == 'tum':                                     # eşik çevresi bant tablosu (havuz)
                rt_, rp_ = hv[0], hv[1]
                ok = np.isfinite(rt_) & np.isfinite(rp_)
                rt_, rp_ = rt_[ok], rp_[ok]
                kenar = [-1e9, -100, -50, -25, 0, 25, 50, 100, 1e9]
                for thr in (0.03, 0.05):
                    a = (np.abs(rp_) - thr) * 1e4
                    hit = (np.abs(rt_) >= thr) & (np.sign(rt_) == np.sign(rp_))
                    for lo_, hi_ in zip(kenar[:-1], kenar[1:]):
                        m = (a >= lo_) & (a < hi_) & (np.abs(rp_) >= thr - 0.02)
                        bant.append({'vekil': vek, 'esik': thr, 'vekil_eksi_esik_bps': f'{max(lo_, -200):.0f}..{min(hi_, 999):.0f}',
                                     'n': int(m.sum()), 'P_kapanista_esik_ustu': round(hit[m].mean(), 3) if m.sum() else np.nan})
            # eşit ağırlıklı sektör sepeti (aynı üyelerle)
            m = RT[sc].notna() & RP[sc].notna()
            bt = RT[sc].where(m).mean(axis=1).where(m.sum(axis=1) >= 5)
            bp = RP[sc].where(m).mean(axis=1).where(m.sum(axis=1) >= 5)
            bsd = elib.ew_basket(P).rolling(60, min_periods=30).std().shift(1)
            rows += satirlar('SEPET', 'sepet', vek, dn_ad, bt[sl].values, bp[sl].values, bsd[sl].values)
    # endeksler
    I = P['idx_ret']
    isd = I.rolling(60, min_periods=30).std().shift(1)
    snap = P['snap'].copy()
    snap['date'] = pd.to_datetime(snap['date'])

    def endeks(sym, vek, ratio, dset):
        r = I[sym]
        rp = (1 + r) * ratio.reindex(r.index) - 1
        for dn_ad, (a, b) in dset.items():
            sl = slice(a, b)
            rows.extend(satirlar(sym, 'endeks', vek, dn_ad, r[sl].values, rp[sl].values, isd[sym][sl].values))

    uzun = {'uzun_2017_2025H1': (pd.Timestamp('2017-01-02'), R.index[-1])}
    for sym in ('XELKT', 'XU030', 'XU100'):
        s = snap[snap.sym == sym].set_index('date')
        m5 = s[s.kaynak == 'isy_m5']
        h1 = s[s.kaynak == 'isy_h1']
        if len(m5) > 100:
            d = {**per, **uzun} if sym == 'XELKT' else {'m5_gunleri': (m5.index[0], m5.index[-1])}
            for vek, kol in (('1730', 'p_1730'), ('1750', 'p_1750'), ('1755son', 'p_son')):
                endeks(sym, vek, (m5[kol] / m5['p_close']), d)
        if len(h1) > 100:
            endeks(sym, '1700', (h1['p_1700'] / h1['p_close']), {**per, **uzun})
        yp = os.path.join(panel, 'h1', sym + '.parquet')
        if os.path.exists(yp):
            y = pd.read_parquet(yp)
            y = y[y.ts_tr.dt.strftime('%H:%M') == '16:30']
            y = y.set_index(y.ts_tr.dt.normalize())['c']
            pc = s['p_close'].reindex(y.index)
            ratio = (y / pc)
            ratio = ratio.where((ratio > 0.9) & (ratio < 1.1))
            endeks(sym, '1730', ratio, per)
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df.to_csv(out, index=False)
    bt = pd.DataFrame(bant)
    bt.to_csv(out.replace('.csv', '_bant.csv'), index=False)
    print(bt.to_string(index=False))
    pd.set_option('display.width', 250, 'display.max_rows', 400)
    ozet = df[df.sym.isin(['HAVUZ', 'SEPET', 'XELKT', 'XU030', 'XU100'])]
    print(ozet.pivot_table(index=['sym', 'vekil', 'donem'], columns='sinyal', values='yakalama', sort=False).round(2).to_string())
    print(ozet.pivot_table(index=['sym', 'vekil', 'donem'], columns='sinyal', values='kesinlik', sort=False).round(2).to_string())
    print(ozet.drop_duplicates(['sym', 'vekil', 'donem'])[['sym', 'vekil', 'donem', 'n_gun', 'corr', 'medyan_mutlak_fark_bps', 'p95_mutlak_fark_bps']].to_string(index=False))
    print(ozet[ozet.donem == 'tum'].pivot_table(index=['sym', 'vekil'], columns='sinyal', values='n_gercek', sort=False).to_string())
    h = df[(df.tur == 'hisse') & (df.sinyal.isin(['abs3', 'abs5', 'absz2']))]
    print(h.groupby(['vekil', 'sinyal'])[['corr', 'kesinlik', 'yakalama']].describe().round(3).T.to_string())


if __name__ == '__main__':
    main()
