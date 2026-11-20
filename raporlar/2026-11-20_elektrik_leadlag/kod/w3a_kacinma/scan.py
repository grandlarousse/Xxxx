"""W3-A tarama: K1–K6 tetikleri (spot AL pozisyonunun fazla getirisi; own ve sec) + VİOP SAT sürümleri.
Kullanım: python3 -I scan.py <panel_dev> <çıktı csv>
Her satır elib.evaluate() / elib.evaluate_viop() çıktısıdır; 'ek_' ile başlayan sütunlar bu betiğin ek hesabıdır
(kapsam, rastgele alıcıya iyileşme, gece / gün içi ayrımı; dönem dönem)."""
import os
import sys
import time

import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), 'ortak'))
import elib  # noqa: E402
import rules  # noqa: E402

PER = {'IS': (rules.LIM0, elib.IS_END), 'OOS1': (elib.OOS1_START, elib.OOS1_END)}


def ek_olcu(sig, P, F, base=None):
    """Ek hesap (elib matrisleriyle): kapsam, rastgele alıcıya iyileşme, f1'in gece / gün içi ayrımı (sektöre göre).
    Evren: dolabilir (fill_long) sektör hisse-günleri; base verilirse (ör. 2013+ rel tanımlı günler) onunla kısılır."""
    sc = F['sc']
    M, fl = elib.excess_measures(P, 1, 'long', sc)
    raw = M['raw']
    U = fl & raw.notna()
    if base is not None:
        U = U & base
    S = sig.reindex_like(raw).fillna(False) & U
    g = P['ret_co'][sc].shift(-1)
    o = P['ret_oc'][sc].shift(-1)
    out = {}
    for per, (a, b) in PER.items():
        m = (raw.index >= a) & (raw.index <= b)
        u, s = U[m], S[m]
        out[f'ek_kapsam_{per}'] = float(s.values.sum() / max(u.values.sum(), 1))
        r = raw[m]
        allm = r.where(u).mean(axis=1)
        keep = r.where(u & ~s).mean(axis=1)
        d = (keep - allm).dropna()
        out[f'ek_iyilesme_{per}_bps'] = 1e4 * d.mean() if len(d) else np.nan      # süzgeç uygulanınca ortalama f1 farkı
        out[f'ek_isaretli_gun_orani_{per}'] = float((s.sum(axis=1) > 0).mean())
        for lab, X in (('gece', g[m]), ('gunici', o[m])):
            ok = u & X.notna()
            xs = X.where(s & ok).mean(axis=1)
            xb = X.where(ok & ~s).mean(axis=1)
            dd = (xs - xb).dropna()
            out[f'ek_{lab}_sektore_gore_{per}_bps'] = 1e4 * dd.mean() if len(dd) else np.nan
            se = dd.std(ddof=1) / np.sqrt(len(dd)) if len(dd) > 2 else np.nan
            out[f'ek_{lab}_t_{per}'] = float(dd.mean() / se) if se and se == se and se > 0 else np.nan
    return out


def main(panel, out):
    t0 = time.time()
    P = elib.load(panel)
    F = rules.feats(P)
    T = rules.triggers(F)
    sc = F['sc']
    V3 = [c for c in elib.VIOP if c in sc]
    R = F['R']
    rows = []

    def spot(ad, sig, hs=(1, 2, 3), olcus=('own', 'sec'), grup='', ek=True):
        e = ek_olcu(sig, P, F) if ek else {}
        for h in hs:
            for olcu in olcus:
                x = dict(e); x.update({'grup': grup, 'tetik': ad})
                rows.append(elib.evaluate(sig, P, h=h, side='long', measure=olcu, name=f'{ad}_AL_h{h}_{olcu}',
                                          family='W3A', extra=x))

    KOMSU = ('K23', 'K4a4', 'K4a7', 'K5z10', 'K5z20', 'K5arti', 'K5yarim_ustu')
    # ---- ana tetikler: h = 1, 2, 3; own ve sec
    for k in T:
        spot(k, T[k], grup='komsu' if k in KOMSU else 'ana')
    # ---- K1 kırılımları
    K1 = T['K1']
    spot('K1_uzak2p', K1 & (F['tavan_uzak'] >= 0.02), grup='K1_kirilim')          # tavanın ≥ %2 altında kapandı
    spot('K1_yakin2', K1 & (F['tavan_uzak'] < 0.02), grup='K1_kirilim')
    spot('K1_uzak5p', K1 & (F['tavan_uzak'] >= 0.05), grup='K1_kirilim')
    spot('K1_gun_arti', K1 & (R > 0), hs=(1,), grup='K1_kirilim')
    spot('K1_gun_eksi', K1 & (R <= 0), hs=(1,), grup='K1_kirilim')
    spot('K1_hacim2x', K1 & (F['vratio'] > 2), hs=(1,), grup='K1_kirilim')
    spot('K1_hacim_olagan', K1 & ~(F['vratio'] > 2), hs=(1,), grup='K1_kirilim')
    # ---- K2 kırılımı, K4 taban hariç
    K2 = T['K2']
    spot('K2_uzak2p', K2 & (F['taban_uzak'] >= 0.02), hs=(1,), grup='K2_kirilim')
    spot('K2_yakin2', K2 & (F['taban_uzak'] < 0.02), hs=(1,), grup='K2_kirilim')
    for k in ('K4q', 'K4a3', 'K4a5'):
        spot(k + '_tabansiz', T[k] & ~F['lim_dn'], grup='K4_tabansiz')
        spot(k + '_taban_ve_K2siz', T[k] & ~F['lim_dn_touch'], hs=(1,), grup='K4_tabansiz')
    # ---- likidite üçte birlikleri, ham fiyat ≥ 5 TL (h = 1)
    for k in ('K1', 'K2', 'K3', 'K4q', 'K4a3', 'K4a5', 'K5', 'K6'):
        for lab in ('likit', 'orta', 'sig'):
            spot(f'{k}_{lab}', T[k] & F[lab], hs=(1,), grup='likidite', ek=False)
        spot(f'{k}_px5', T[k] & F['px5'], hs=(1,), grup='fiyat5', ek=False)
    # ---- kaçınma kaç gün geçerli: sinyal 1 ve 2 gün kaydırılır (t+1→t+2 ve t+2→t+3 getirisi)
    for k in ('K1', 'K2', 'K3', 'K4q', 'K4a3', 'K4a5', 'K5', 'K6'):
        for d in (1, 2):
            spot(f'{k}_gecikme{d}', T[k].shift(d, fill_value=False), hs=(1,), grup='kalicilik', ek=False)
    # ---- birleşimler (spot)
    U = {'B_K1_K2': T['K1'] | T['K2'], 'B_K1_K4a3': T['K1'] | T['K4a3'], 'B_K1_K2_K4a3': T['K1'] | T['K2'] | T['K4a3'],
         'B_K1_K2_K4a5': T['K1'] | T['K2'] | T['K4a5'], 'B_K1_K2_K4a3_K5': T['K1'] | T['K2'] | T['K4a3'] | T['K5'],
         'B_K4a3_haric_K1K2': T['K4a3'] & ~T['K1'] & ~T['K2'] & ~T['K3']}
    for k, s in U.items():
        spot(k, s, grup='birlesim')

    # ---- VİOP SAT (AKSEN/ENJSA/ODAS)
    VT = dict(T); VT.update(U)
    VT['B_hepsi'] = T['K1'] | T['K2'] | T['K4a3'] | T['K5'] | T['K6']
    VT['B_K1_K5'] = T['K1'] | T['K5']
    VT['B_K1_K2_K5'] = T['K1'] | T['K2'] | T['K5']
    VT['B_K1_K2_K4a5_K5'] = T['K1'] | T['K2'] | T['K4a5'] | T['K5']
    for k, s in VT.items():
        sv = s[V3]
        for h in (1, 2, 3):
            x = {'grup': 'viop_sat', 'tetik': k}
            rows.append(elib.evaluate_viop(sv, P, h=h, side='short', name=f'{k}_VIOP_SAT_h{h}', family='W3A', extra=x))
            if h == 1 or k in ('K1', 'K2', 'K4q', 'K4a3', 'K4a5', 'K5', 'B_K1_K2', 'B_K1_K2_K4a3', 'B_K1_K2_K4a3_K5',
                               'B_K1_K5', 'B_K1_K2_K5', 'B_K1_K2_K4a5_K5'):
                x2 = {'grup': 'viop3_spot_tam_gecmis', 'tetik': k}
                rows.append(elib.evaluate(sv, P, h=h, side='long', measure='own', name=f'{k}_3hisse_spotAL_h{h}_own',
                                          family='W3A', extra=x2))
    df = elib.to_csv(rows, out)
    print(f'{len(df)} satır, {time.time() - t0:.0f} sn -> {out}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
