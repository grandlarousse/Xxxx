"""V5 — sektör sepetinin uygulanabilir sürümleri (BETİMSEL; yeni doğrulanmış kural üretmez).

Kullanım:  python3 -I v5.py <panel_full> <ek_klasoru>
Çıktı:     <ek>/v5_sepet.csv  (uzun biçim: soru, sinyal, varyant, donem, ölçüler)

Sinyaller (dondurulmuş kurallardan, değiştirilmeden):
  S1 = a5_rotasyon:A5_zirve20_sepet_h3   (XELKT 20 günlük en yüksek kapanış)
  S2 = a2_endeks:A2_xelkt_z1_tum_h3      (XELKT günlük getirisi / 60 günlük gecikmeli std >= 1)
Ölçüler: ham = c(t+3)/c(t) − 1 (çıkışta taban kilidi varsa kaydırmalı; elib.fwd_exec);
         per = ham − hissenin o dönemdeki dolabilir günlerinin ortalaması (IS / OOS1 / KASA; HAVUZ = 2023-01-02 →).
Maliyet: gidiş-dönüş temel 25, muhafazakâr 50 bps + yarım fiyat adımı (o günün ham fiyatından; elib.cost_bps ile aynı).
"""
import os
import sys
import importlib.util
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(KOD, 'ortak'))
import elib  # noqa: E402

H = 3
SEED = 20261120
NDRAW = 2000
PER = {'IS': (None, elib.IS_END), 'OOS1': (elib.OOS1_START, elib.OOS1_END), 'KASA': (elib.KASA_START, None),
       'HAVUZ': (elib.OOS1_START, None)}
GRUP = {'yenilenebilir': 'üretim-yenilenebilir', 'termik': 'üretim-termik', 'dagitim': 'dağıtım-perakende',
        'gaz': 'doğal gaz dağıtımı', 'panel_ekipman': 'güneş paneli-ekipman'}
FUT_RT = {'temel': 10.0, 'muhafazakar': 20.0}      # XU030 vadelisi gidiş-dönüş bps (VARSAYIM; maliyet.md: doğrulanmadı)


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pmask(index, per):
    a, b = PER[per]
    m = np.ones(len(index), dtype=bool)
    if a is not None:
        m &= index >= a
    if b is not None:
        m &= index <= b
    return m


def demean(P, f, fl, mode):
    old = elib.PERIOD_MODE
    elib.PERIOD_MODE = mode
    try:
        return elib.period_demean(P, f, fl)
    finally:
        elib.PERIOD_MODE = old


def hac(x, d, lag=H - 1):
    return elib._hac_mean(np.asarray(x, float), np.asarray(d, float), lag)


class Ctx:
    pass


def setup(panel):
    C = Ctx()
    P = elib.load(panel)
    C.P = P
    sc = elib.sector_cols(P)
    C.sc = sc
    C.idx = P['ret_cc'].index
    f, fl, delayed = elib.fwd_exec(P, H, 'long', sc)
    fl = fl.reindex_like(f).fillna(False)
    C.f, C.fl, C.delayed = f, fl, delayed
    C.per3 = demean(P, f, fl, 'uc_parca')
    C.perH = demean(P, f, fl, 'havuz')
    cr = P['close_raw'][sc].reindex(C.idx)
    tick = pd.DataFrame(elib.tick_of(cr.values), index=cr.index, columns=sc)
    old = cr.index < pd.Timestamp('2023-11-06')
    tick.loc[old] = tick.loc[old].where(cr.loc[old] < 100, 0.10)
    C.tickbps = 1e4 * tick / cr
    C.cost = {s: (elib.COST[s]['spot'] + 0.5 * C.tickbps) / 1e4 for s in ('temel', 'muhafazakar')}
    C.nfl = fl.sum(axis=1)
    # --- sinyaller
    a5 = load_mod('a5rules', os.path.join(KOD, 'a5_rotasyon', 'rules.py'))
    a2 = load_mod('a2rules', os.path.join(KOD, 'a2_endeks', 'rules.py'))
    s1 = {r['ad']: r for r in a5.build(P)}['A5_zirve20_sepet_h3']['sig'].reindex(C.idx).fillna(False).any(axis=1)
    s2 = {r['ad']: r for r in a2.build(P)}['A2_xelkt_z1_tum_h3']['sig'].reindex(C.idx).fillna(False).any(axis=1)
    C.S = {'S1': s1, 'S2': s2, 'S1veyaS2': s1 | s2, 'S1veS2': s1 & s2, 'yalnizS1': s1 & ~s2, 'yalnizS2': s2 & ~s1}
    # --- seçim maskeleri (hepsi t kapanışında bilinir)
    a3 = load_mod('a3rules', os.path.join(KOD, 'a3_kesit', 'rules.py'))
    w3a = load_mod('w3arules', os.path.join(KOD, 'w3a_kacinma', 'rules.py'))
    w3b = load_mod('w3brules', os.path.join(KOD, 'w3b_damitma', 'rules.py'))
    F3 = a3.feats(P)
    K1 = a3.sig_quint(F3, 1, 'bottom').reindex(index=C.idx, columns=sc).fillna(False)
    Fw = w3a.feats(P)
    K2 = w3a.triggers(Fw)['K4a5'].reindex(index=C.idx, columns=sc).fillna(False)
    T2 = w3b.sade_sig(P).reindex(index=C.idx, columns=sc).fillna(False)
    rel1 = Fw['rel1'].reindex(index=C.idx, columns=sc)
    tavan_uzak = Fw['tavan_uzak'].reindex(index=C.idx, columns=sc)
    adv = elib.adv60(P)[sc].where(fl)
    C.adv = adv
    rk = adv.rank(axis=1, ascending=False, method='first')
    n = adv.notna().sum(axis=1)
    true = pd.DataFrame(True, index=C.idx, columns=sc)
    V = {'tam_sepet': true}
    for k in (3, 5, 10, 15, 20):
        V[f'likit{k}'] = rk <= k
    V['likidite_orta_ucte_bir'] = rk.gt(n / 3, axis=0) & rk.le(2 * n / 3, axis=0)
    V['likit6_15'] = (rk >= 6) & (rk <= 15)
    V['likidite_alt_yari'] = rk.gt(n / 2, axis=0)
    V['likit6_20'] = (rk >= 6) & (rk <= 20)
    V['likit5_haric_hepsi'] = rk >= 6
    V['sira_her_2de1'] = (rk % 2 == 0)            # likidite sırası çift olanlar (2., 4., 6. …): yarı sepet
    V['sira_her_3te1'] = (rk % 3 == 0)            # sırası 3'ün katı olanlar (3., 6., 9. …): üçte bir sepet
    V['fiyat_ge5'] = cr >= 5.0
    V['fiyat_lt5'] = cr < 5.0
    u = pd.read_csv(os.path.join(KOD, '..', 'ek', 'xelkt_uyeler.csv'))
    u['g'] = u['ana_faaliyet'].str.replace('?', '', regex=False).str.strip()
    C.uyeler = u
    for kisa, uzun in GRUP.items():
        mem = [s for s in u.loc[u.g == uzun, 'sym'] if s in sc]
        V['grup_' + kisa] = pd.DataFrame(np.repeat(np.isin(sc, mem)[None, :], len(C.idx), axis=0), index=C.idx, columns=sc)
    mem = [s for s in u.loc[u.g.isin([GRUP['dagitim'], GRUP['gaz']]), 'sym'] if s in sc]
    V['grup_dagitim_ve_gaz'] = pd.DataFrame(np.repeat(np.isin(sc, mem)[None, :], len(C.idx), axis=0), index=C.idx, columns=sc)
    V['gun_sektor_ustu'] = rel1 > 0
    V['gun_sektor_alti'] = rel1 < 0
    V['tavana_ge2_uzak'] = tavan_uzak >= 0.02
    V['K1K2_gecen'] = ~K1 & ~K2
    V['K2_gecen'] = ~K2
    V['K1_veya_K2_takilan'] = K1 | K2
    V['T2_secilen'] = T2
    V['viop3_AKSEN_ENJSA_ODAS'] = pd.DataFrame(np.repeat(np.isin(sc, elib.VIOP)[None, :], len(C.idx), axis=0), index=C.idx, columns=sc)
    V['likit10_fiyat_ge5'] = (cr >= 5.0) & ((adv.where(cr >= 5.0)).rank(axis=1, ascending=False, method='first') <= 10)
    V['likit10_K1K2_gecen'] = (~K1 & ~K2) & ((adv.where(~K1 & ~K2)).rank(axis=1, ascending=False, method='first') <= 10)
    C.V = {k: v.reindex(index=C.idx, columns=sc).fillna(False).astype(bool) for k, v in V.items()}
    return C


def day_frames(C, mask, per, min_n=1):
    """mask & dolabilir üzerinde günlük eşit ağırlıklı seriler (dönemin per ölçüsüyle)."""
    PX = C.perH if per == 'HAVUZ' else C.per3
    M = mask & C.fl & C.f.notna()
    n = M.sum(axis=1)
    ok = n >= min_n
    out = {'n': n.where(ok)}
    out['ham'] = C.f.where(M).mean(axis=1).where(ok)
    out['per'] = PX.where(M).mean(axis=1).where(ok)
    for s in ('temel', 'muhafazakar'):
        out['c_' + s] = C.cost[s].where(M).mean(axis=1).where(ok)
    pm = pmask(C.idx, per)
    return {k: v[pm] for k, v in out.items()}


def summarize(D, base=None):
    d = D['per'].notna().values
    r = {'n_gun': int(d.sum())}
    if d.sum() < 3:
        return r
    ham, per = D['ham'].fillna(0).values, D['per'].fillna(0).values
    r['ort_n_hisse'] = float(D['n'][d].mean())
    r['ham_bps'], r['t_ham'] = [v * (1e4 if i == 0 else 1) for i, v in enumerate(hac(ham, d))]
    r['per_bps'], r['t_per'] = [v * (1e4 if i == 0 else 1) for i, v in enumerate(hac(per, d))]
    ct, cm = D['c_temel'][d].mean(), D['c_muhafazakar'][d].mean()
    r['maliyet_temel_bps'] = 1e4 * ct
    r['per_net_temel_bps'] = r['per_bps'] - 1e4 * ct
    r['per_net_muh_bps'] = r['per_bps'] - 1e4 * cm
    r['ham_net_temel_bps'] = r['ham_bps'] - 1e4 * ct
    r['ham_net_muh_bps'] = r['ham_bps'] - 1e4 * cm
    h = D['ham'][d]
    hn = h - D['c_temel'][d]
    r['ham_medyan_bps'] = 1e4 * h.median()
    r['ham_p10_bps'], r['ham_p90_bps'] = 1e4 * h.quantile(0.10), 1e4 * h.quantile(0.90)
    r['ham_p05_bps'] = 1e4 * h.quantile(0.05)
    r['ham_std_bps'] = 1e4 * h.std()
    r['zarar_olasiligi_ham'] = float((h < 0).mean())
    r['zarar_olasiligi_net_temel'] = float((hn < 0).mean())
    if base is not None:
        both = d & base['per'].notna().values
        if both.sum() >= 3:
            dp = (D['per'] - base['per']).where(both, 0).fillna(0).values
            dh = (D['ham'] - base['ham']).where(both, 0).fillna(0).values
            m, t = hac(dp, both)
            r['fark_per_tamsepet_bps'], r['t_fark_per'] = 1e4 * m, t
            m, t = hac(dh, both)
            r['fark_ham_tamsepet_bps'], r['t_fark_ham'] = 1e4 * m, t
            dn = dp - (D['c_temel'] - base['c_temel']).where(both, 0).fillna(0).values
            r['fark_per_net_temel_bps'] = 1e4 * dn.sum() / both.sum()
    return r


def sigmask(C, s):
    return pd.DataFrame(np.repeat(s.values[:, None], len(C.sc), axis=1), index=C.idx, columns=C.sc)


# ------------------------------------------------------------------------------------------------ Soru 2 (+ taban satırlar)
def q2(C):
    rows = []
    for sn in ('S1', 'S2', 'S1veyaS2'):
        sm = sigmask(C, C.S[sn])
        for per in PER:
            base = day_frames(C, sm, per, min_n=5)
            for vn, vm in C.V.items():
                D = day_frames(C, sm & vm, per, min_n=5 if vn == 'tam_sepet' else 1)
                # tam sepetin geçerli olduğu günlerle sınırla (günde >= 5 dolabilir)
                okb = base['per'].notna()
                D = {k: v.where(okb) for k, v in D.items()}
                r = {'soru': '2_secim', 'sinyal': sn, 'varyant': vn, 'donem': per}
                r.update(summarize(D, None if vn == 'tam_sepet' else base))
                rows.append(r)
    df = pd.DataFrame(rows)
    # üç dönemde de tam sepetten kötü değil mi? (per farkı >= 0: IS, OOS1, KASA)
    for sn in df.sinyal.unique():
        for vn in df.varyant.unique():
            q = df[(df.sinyal == sn) & (df.varyant == vn) & df.donem.isin(['IS', 'OOS1', 'KASA'])]
            if vn == 'tam_sepet' or 'fark_per_tamsepet_bps' not in q:
                continue
            ok = bool((q['fark_per_tamsepet_bps'] >= 0).all() and q['fark_per_tamsepet_bps'].notna().all())
            okn = bool((q['fark_per_net_temel_bps'] >= 0).all() and q['fark_per_net_temel_bps'].notna().all())
            okh = bool((q['fark_ham_tamsepet_bps'] >= 0).all() and q['fark_ham_tamsepet_bps'].notna().all())
            df.loc[(df.sinyal == sn) & (df.varyant == vn), 'uc_donemde_kotu_degil_per'] = ok
            df.loc[(df.sinyal == sn) & (df.varyant == vn), 'uc_donemde_kotu_degil_per_net'] = okn
            df.loc[(df.sinyal == sn) & (df.varyant == vn), 'uc_donemde_kotu_degil_ham'] = okh
    return df


# ------------------------------------------------------------------------------------------------ Soru 1
def q1(C):
    rows = []
    rng = np.random.default_rng(SEED)
    f, p3, pH, ct = C.f.values, C.per3.values, C.perH.values, C.cost['temel'].values
    okm = (C.fl & C.f.notna()).values
    for sn in ('S1', 'S2', 'S1veyaS2'):
        s = C.S[sn].values
        ev = np.where(s & (okm.sum(axis=1) >= 5))[0]
        for N in (0, 3, 5, 8, 12, 20):
            E = {k: np.full((len(ev), NDRAW if N else 1), np.nan) for k in ('ham', 'net', 'p3', 'pH')}
            nk = np.zeros(len(ev))
            for j, t in enumerate(ev):
                c = np.where(okm[t])[0]
                k = len(c) if N == 0 else min(N, len(c))
                nk[j] = k
                if N == 0 or k == len(c):
                    sel = np.repeat(c[None, :], E['ham'].shape[1], axis=0)
                else:
                    sel = c[np.argsort(rng.random((NDRAW, len(c))), axis=1)[:, :k]]
                E['ham'][j] = f[t][sel].mean(axis=1)
                E['net'][j] = (f[t][sel] - ct[t][sel]).mean(axis=1)
                # dönemde 60'tan az dolabilir günü olan (yeni) hissenin 'per'i yoktur: ortalama kalanlardan alınır
                with np.errstate(all='ignore'), warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    E['p3'][j] = np.nanmean(p3[t][sel] - ct[t][sel], axis=1)
                    E['pH'][j] = np.nanmean(pH[t][sel] - ct[t][sel], axis=1)
            if N == 0:
                FULL = {k: v[:, 0].copy() for k, v in E.items()}
            for per in PER:
                pm = pmask(C.idx[ev], per)
                if pm.sum() < 3:
                    continue
                ham, net = E['ham'][pm], E['net'][pm]
                pn = (E['pH'] if per == 'HAVUZ' else E['p3'])[pm]
                r = {'soru': '1_rastgele_N', 'sinyal': sn, 'varyant': 'tam_sepet' if N == 0 else f'rastgele{N}', 'donem': per,
                     'n_gun': int(pm.sum()), 'ort_n_hisse': float(nk[pm].mean()),
                     'ham_bps': 1e4 * ham.mean(), 'ham_medyan_bps': 1e4 * np.median(ham),
                     'ham_p10_bps': 1e4 * np.quantile(ham, 0.10), 'ham_p90_bps': 1e4 * np.quantile(ham, 0.90),
                     'ham_p05_bps': 1e4 * np.quantile(ham, 0.05), 'ham_std_bps': 1e4 * ham.std(),
                     'ham_net_temel_bps': 1e4 * net.mean(), 'per_net_temel_bps': 1e4 * np.nanmean(pn),
                     'zarar_olasiligi_ham': float((ham < 0).mean()), 'zarar_olasiligi_net_temel': float((net < 0).mean())}
                if N:
                    r['izleme_sapmasi_bps'] = 1e4 * (ham - FULL['ham'][pm][:, None]).std()
                    inv = np.nanmean(pn, axis=0)          # yatırımcı düzeyi: dönem boyunca her olayda yeniden rastgele N
                    r['yatirimci_per_net_p10_bps'] = 1e4 * np.quantile(inv, 0.10)
                    r['yatirimci_per_net_p50_bps'] = 1e4 * np.quantile(inv, 0.50)
                    r['yatirimci_per_net_p90_bps'] = 1e4 * np.quantile(inv, 0.90)
                    r['yatirimci_per_net_eksi_olasiligi'] = float((inv < 0).mean())
                    invh = net.mean(axis=0)
                    r['yatirimci_ham_net_p10_bps'] = 1e4 * np.quantile(invh, 0.10)
                    r['yatirimci_ham_net_p90_bps'] = 1e4 * np.quantile(invh, 0.90)
                rows.append(r)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ Soru 3
def episodes(spos, T, policy):
    eps, k = [], 0
    while k < len(spos):
        t0 = spos[k]
        ex = t0 + H
        k += 1
        if policy == 'uzat':
            while k < len(spos) and spos[k] <= ex:
                ex = spos[k] + H
                k += 1
        elif policy == 'yoksay':
            while k < len(spos) and spos[k] < ex:
                k += 1
        if ex > T - 1:
            break
        eps.append((t0, ex))
    return eps


def losing_streak(x):
    best = cur = 0
    for v in x:
        cur = cur + 1 if v < 0 else 0
        best = max(best, cur)
    return best


def q3(C):
    rows = []
    P = C.P
    idx, sc = C.idx, C.sc
    T = len(idx)
    R = P['ret_cc'][sc]
    L = elib.level(R).values
    ld = P['lim_dn'][sc].values
    flv = (C.fl & C.f.notna()).values
    # --- örtüşme
    for per in PER:
        pm = pmask(idx, per)
        ok = (C.nfl >= 5).values & pm
        a, b = C.S['S1'].values & ok, C.S['S2'].values & ok
        rows.append({'soru': '3_ortusme', 'sinyal': 'S1,S2', 'varyant': 'gun_sayilari', 'donem': per,
                     'n_gun': int(pm.sum()), 'n_S1': int(a.sum()), 'n_S2': int(b.sum()), 'n_ikisi': int((a & b).sum()),
                     'n_biri': int((a | b).sum()), 'S2_gunlerinin_S1_payi': float((a & b).sum() / max(b.sum(), 1)),
                     'S1_gunlerinin_S2_payi': float((a & b).sum() / max(a.sum(), 1))})
    # --- birleşik sinyaller (olay düzeyi, tam sepet)
    for sn in ('S1', 'S2', 'S1veyaS2', 'S1veS2', 'yalnizS1', 'yalnizS2'):
        sm = sigmask(C, C.S[sn])
        for per in PER:
            r = {'soru': '3_birlesim', 'sinyal': sn, 'varyant': 'tam_sepet_her_sinyal_gunu', 'donem': per}
            r.update(summarize(day_frames(C, sm, per, min_n=5)))
            rows.append(r)
    # --- pozisyon yenileme politikaları
    Ldf = elib.level(R)
    _mu = {}

    def muk(per, k):
        if (per, k) not in _mu:
            pm = pmask(idx, per)
            fk = elib.fwd_exec(P, k, 'long', sc)[0][pm].where(C.fl[pm])
            _mu[(per, k)] = fk.mean().where(fk.notna().sum() >= 60).values
        return _mu[(per, k)]
    ct, cm = C.cost['temel'].values, C.cost['muhafazakar'].values
    for sn in ('S1', 'S2', 'S1veyaS2'):
        s = C.S[sn].values & (C.nfl >= 5).values
        spos = np.where(s)[0]
        for pol in ('her_gun_yeni_dilim', 'uzat', 'yoksay'):
            if pol == 'her_gun_yeni_dilim':
                eps = [(t, t + H) for t in spos if t + H <= T - 1]
            else:
                eps = episodes(list(spos), T, pol)
            rec = []
            for t0, ex in eps:
                c = np.where(flv[t0])[0]
                exi = np.full(len(c), ex)
                for _ in range(5):                      # çıkışta taban kilidi: ilk kilitsiz kapanışa kaydır
                    lock = ld[exi, c] & (exi + 1 <= T - 1)
                    exi = np.where(lock, exi + 1, exi)
                ret = L[exi, c] / L[t0, c] - 1
                ret[ld[exi, c]] = np.nan                # 5 kaydırmadan sonra hâlâ kilitli: elib sözleşmesi gibi dışarıda (bkz. 5_risk)
                good = np.isfinite(ret)
                rec.append((t0, ex, ret[good].mean(), c[good], ct[t0, c][good].mean(), cm[t0, c][good].mean()))
            for per in PER:
                pm = pmask(idx, per)
                yrs = pm.sum() / 250.0
                e = [x for x in rec if pm[x[0]]]
                if len(e) < 3:
                    continue
                ham = np.array([x[2] for x in e])
                dur = np.array([x[1] - x[0] for x in e])
                # sıradan gün kıyası: hissenin o dönemdeki DOLABİLİR günlerinden k günlük ortalama getirisi (k = tutma süresi)
                drift = np.array([np.nanmean(muk(per, x[1] - x[0])[x[3]]) for x in e])
                c_t = np.array([x[4] for x in e]); c_m = np.array([x[5] for x in e])
                inpos = np.zeros(T, dtype=bool)
                for x in e:
                    inpos[x[0] + 1:x[1] + 1] = True
                w = 1.0 / H if pol == 'her_gun_yeni_dilim' else 1.0      # dilim başına sermaye payı
                r = {'soru': '3_politika', 'sinyal': sn, 'varyant': pol, 'donem': per, 'n_gun': int(len(e)),
                     'giris_yilda': len(e) / yrs, 'ort_tutma_gun': float(dur.mean()),
                     'pozisyonda_gun_orani': float(inpos[pm].sum() / pm.sum()), 'sermaye_payi_islem_basina': w,
                     'ham_bps': 1e4 * ham.mean(), 'per_bps': 1e4 * (ham - drift).mean(),
                     'maliyet_temel_bps': 1e4 * c_t.mean(),
                     'ham_net_temel_bps': 1e4 * (ham - c_t).mean(), 'ham_net_muh_bps': 1e4 * (ham - c_m).mean(),
                     'per_net_temel_bps': 1e4 * (ham - drift - c_t).mean(), 'per_net_muh_bps': 1e4 * (ham - drift - c_m).mean(),
                     'yillik_toplam_ham_net_temel_pct': 100 * w * (ham - c_t).sum() / yrs,
                     'yillik_toplam_per_net_temel_pct': 100 * w * (ham - drift - c_t).sum() / yrs,
                     'yillik_toplam_per_net_muh_pct': 100 * w * (ham - drift - c_m).sum() / yrs,
                     'yillik_maliyet_temel_pct': 100 * w * c_t.sum() / yrs,
                     'zarar_olasiligi_ham': float((ham < 0).mean()), 'zarar_olasiligi_net_temel': float(((ham - c_t) < 0).mean()),
                     'ham_p05_bps': 1e4 * np.quantile(ham, 0.05), 'en_kotu_bps': 1e4 * ham.min(),
                     'en_uzun_zarar_serisi': losing_streak(ham - c_t)}
                r['per_gun_basina_bps'] = 1e4 * (ham - drift).sum() / dur.sum()
                r['maliyet_gun_basina_bps'] = 1e4 * c_t.sum() / dur.sum()
                m_, t_ = hac(np.bincount([x[0] for x in e], weights=ham - drift, minlength=T)[pm],
                             np.bincount([x[0] for x in e], minlength=T)[pm] > 0, lag=int(min(dur.max(), 10)))
                r['t_per'] = t_
                rows.append(r)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ Soru 4
def q4(C, ek):
    P, sc = C.P, C.sc
    last = C.idx[-1]
    tr = P['tradable'][sc].loc[last]
    syms = [s for s in sc if tr[s]]
    px = P['close_raw'][sc].loc[last]
    adv = P['vol_tl'][sc].tail(60).median()
    kh = pd.read_csv(os.path.join(ek, 'a7_kapanis_hacim.csv')).set_index('sym')
    share = kh['K_ortalama'].reindex(syms)
    med = float(kh['K_ortalama'].median())
    tahmini = share.isna()
    share = share.fillna(med)
    kap = share * adv[syms]
    tick = pd.Series(elib.tick_of(px[syms].values), index=syms)
    tb = 1e4 * tick / px[syms]
    rank = adv[syms].rank(ascending=False, method='first')
    rows = []
    sizes = {'100bin': 1e5, '1mn': 1e6, '5mn': 5e6}
    for s in syms:
        r = {'soru': '4_hisse', 'sinyal': '', 'varyant': s, 'donem': str(last.date()), 'fiyat_tl': float(px[s]),
             'adim_bps': float(tb[s]), 'adv60_tl': float(adv[s]), 'likidite_sirasi': int(rank[s]),
             'kapanis_payi': float(share[s]), 'kapanis_payi_tahmini_medyan': bool(tahmini[s]), 'kapanis_seansi_tl': float(kap[s])}
        for k, v in sizes.items():
            r[f'oran_kapanis_{k}'] = float(v / len(syms) / kap[s])
        rows.append(r)
    sets = {'tam_sepet': syms, 'likit20': list(rank[rank <= 20].index), 'likit10': list(rank[rank <= 10].index),
            'likit5': list(rank[rank <= 5].index), 'fiyat_ge5': [s for s in syms if px[s] >= 5],
            'likit10_fiyat_ge5': list(adv[[s for s in syms if px[s] >= 5]].rank(ascending=False).pipe(lambda x: x[x <= 10]).index)}
    for nm, ss in sets.items():
        n = len(ss)
        for k, v in sizes.items():
            ratio = (v / n) / kap[ss]
            rd = (v / n) / adv[ss]
            adet = np.floor((v / n) / px[ss])
            rows.append({'soru': '4_kapasite', 'sinyal': '', 'varyant': nm, 'donem': k, 'ort_n_hisse': n,
                         'hisse_basina_tl': v / n, 'oran_kapanis_medyan': float(ratio.median()),
                         'oran_kapanis_max': float(ratio.max()), 'en_dar_hisse': ratio.idxmax(),
                         'n_oran_gt10': int((ratio > 0.10).sum()), 'n_oran_gt25': int((ratio > 0.25).sum()),
                         'n_oran_gt100': int((ratio > 1.0).sum()), 'gunluk_hacme_oran_max': float(rd.max()),
                         'n_gunluk_hacmin_1pct_ustu': int((rd > 0.01).sum()),
                         'yarim_adim_bps_ort': float(0.5 * tb[ss].mean()), 'yarim_adim_bps_max': float(0.5 * tb[ss].max()),
                         'min_adet': float(adet.min()),
                         'sepet_ust_siniri_hepsi_le10_tl': float(n * 0.10 * kap[ss].min()),
                         'sepet_ust_siniri_p80_le10_tl': float(n * 0.10 * kap[ss].quantile(0.20)),
                         'sepet_ust_siniri_hepsi_le25_tl': float(n * 0.25 * kap[ss].min())})
    # sinyal günü hacmi / adv60 (sinyal günleri normalden hareketli mi?)
    vr = (P['vol_tl'][sc] / elib.adv60(P)[sc]).where(C.fl)
    for sn in ('S1', 'S2'):
        for per in ('OOS1', 'KASA'):
            pm = pmask(C.idx, per)
            x = vr[pm & C.S[sn].values].stack()
            rows.append({'soru': '4_sinyal_gunu_hacim', 'sinyal': sn, 'varyant': 'hacim/adv60', 'donem': per,
                         'oran_medyan': float(x.median()), 'oran_p25': float(x.quantile(0.25))})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ Soru 5
def q5(C):
    P, sc, idx = C.P, C.sc, C.idx
    rows = []
    xr = P['idx_ret']['XU030'].reindex(idx)
    beta = elib.beta_lagged(P['ret_cc'][sc], xr)
    bb = beta.where(C.fl).mean(axis=1)
    vf = P['viop_front']
    x = vf[vf['und'].astype(str).str.replace('.E', '', regex=False) == 'XU030'].copy()
    rf = pd.Series(x['ret_settle'].values, index=pd.to_datetime(x['date'])).reindex(idx)
    Lf = elib.level(rf.to_frame('f'))['f']
    fut3 = Lf.shift(-H) / Lf - 1
    idx3 = elib.fwd_simple(xr.to_frame('m'), H)['m']
    hed = fut3.where(fut3.notna(), idx3)
    ok5 = C.nfl >= 5
    okm = C.fl & C.f.notna()
    ball = C.f.where(okm).mean(axis=1).where(ok5)
    hall = ball - bb * hed
    ld = P['lim_dn'][sc]
    any_ld = (ld.shift(-1, fill_value=False) | ld.shift(-2, fill_value=False) | ld.shift(-3, fill_value=False))
    ct = C.cost['temel'].where(okm).mean(axis=1)
    # --- kilit sınırı olmadan çıkış (elib: 5 kaydırmadan sonra hâlâ tabanda kilitli işlem NaN olur ve hesaptan düşer)
    Lv = elib.level(P['ret_cc'][sc]).values
    n_ = len(idx)
    exi = np.minimum(np.arange(n_)[:, None] + H, n_ - 1) * np.ones((1, len(sc)), dtype=int)
    val = (np.arange(n_)[:, None] + H <= n_ - 1) * np.ones((1, len(sc)), dtype=bool)
    for _ in range(60):
        lk = np.take_along_axis(ld.values, exi, axis=0) & (exi + 1 <= n_ - 1)
        exi = np.where(lk, exi + 1, exi)
    fu = np.take_along_axis(Lv, exi, axis=0) / Lv - 1
    fu[~val] = np.nan
    fu = pd.DataFrame(fu, index=idx, columns=sc)
    oku = C.fl & fu.notna()
    ball_u = fu.where(oku).mean(axis=1).where(ok5)
    uzun = C.fl & fu.notna() & C.f.isna()            # elib'de düşen (5 günden uzun kilit) işlemler
    for sn in ('S1', 'S2', 'S1veyaS2'):
        s = C.S[sn] & ok5
        for per in PER:
            pm = pmask(idx, per)
            d = (s & ball.notna()).values & pm
            if d.sum() < 5:
                continue
            u = ball[d]; un = u - ct[d]
            k = max(int(np.ceil(0.05 * len(u))), 1)
            r = {'soru': '5_risk', 'sinyal': sn, 'varyant': 'tam_sepet', 'donem': per, 'n_gun': int(d.sum()),
                 'ham_bps': 1e4 * u.mean(), 'ham_std_bps': 1e4 * u.std(), 'ham_p05_bps': 1e4 * u.quantile(0.05),
                 'en_kotu5pct_ort_bps': 1e4 * np.sort(u.values)[:k].mean(), 'en_kotu_bps': 1e4 * u.min(),
                 'en_kotu_gun': str(u.idxmin().date()),
                 'en_uzun_zarar_serisi': losing_streak(un.values), 'zarar_olasiligi_net_temel': float((un < 0).mean())}
            M = okm[d] & True
            tr_n = int(M.values.sum())
            dl = (C.delayed[d] & M)
            al = (any_ld[d] & M)
            r['kilit_cikis_kaydi_islem_orani'] = float(dl.values.sum() / tr_n)
            r['kilit_cikis_kaydi_olay_orani'] = float(dl.any(axis=1).mean())
            r['taban_kapanis_gordu_islem_orani'] = float(al.values.sum() / tr_n)
            r['taban_kapanis_gordu_olay_orani'] = float(al.any(axis=1).mean())
            v = C.f[d].where(dl).stack()
            r['kilitli_islem_ham_ort_bps'] = 1e4 * float(v.mean()) if len(v) else np.nan
            uu = uzun[d]
            r['n_islem'] = tr_n
            r['n_islem_5gunden_uzun_kilit'] = int(uu.values.sum())
            r['uzun_kilit_islem_ham_ort_bps'] = 1e4 * float(fu[d].where(uu).stack().mean()) if uu.values.sum() else np.nan
            r['uzun_kilit_hisseler'] = ' '.join(sorted(uu.columns[uu.any()]))
            du = (s & ball_u.notna()).values & pm
            r['ham_kilit_sinirsiz_bps'] = 1e4 * ball_u[du].mean()
            r['per_kilit_sinirsiz_bps'] = 1e4 * (ball_u[du].mean() - ball_u[pm].mean())
            r['en_kotu_kilit_sinirsiz_bps'] = 1e4 * ball_u[du].min()
            rows.append(r)
            # --- koruma
            for nm, ser in (('korumasiz_sepet_duzeyi', ball), ('XU030_vadeli_korumali', hall)):
                allp = ser[pm].dropna()
                z = ser[d].dropna()
                dd = (s & ser.notna()).values & pm
                xx = (ser - allp.mean()).where(pd.Series(dd, index=idx), 0).fillna(0)[pm].values
                m, t = hac(xx, dd[pm])
                rr = {'soru': '5_koruma', 'sinyal': sn, 'varyant': nm, 'donem': per, 'n_gun': int(len(z)),
                      'ham_bps': 1e4 * z.mean(), 'ham_std_bps': 1e4 * z.std(), 'per_bps': 1e4 * m, 't_per': t,
                      'ham_p05_bps': 1e4 * z.quantile(0.05), 'en_kotu_bps': 1e4 * z.min(),
                      'zarar_olasiligi_ham': float((z < 0).mean()), 'her_gun_ortalama_bps': 1e4 * allp.mean(),
                      'ort_beta': float(bb[d].mean())}
                if nm.startswith('XU030'):
                    rr['vadeli_maliyet_temel_bps'] = FUT_RT['temel'] * float(bb[d].mean())
                    rr['vadeli_maliyet_muh_bps'] = FUT_RT['muhafazakar'] * float(bb[d].mean())
                    rr['vadeli_ham_bps_sinyal_gunu'] = 1e4 * float(hed[d].mean())
                    rr['vadeli_veri_payi'] = float(fut3[d].notna().mean())
                rows.append(rr)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ Soru 6 + giriş gecikmesi + 17:50 vekili
def q6(C, panel):
    P, sc, idx = C.P, C.sc, C.idx
    rows = []

    def basket(h, entry='close'):
        f, fl, _ = elib.fwd_exec(P, h, 'long', sc)
        fl = fl.reindex_like(f).fillna(False)
        if entry == 'open1':
            f = (1 + f) / (1 + P['ret_co'][sc].shift(-1)) - 1
        b = f.where(fl).mean(axis=1).where(fl.sum(axis=1) >= 5)
        return b
    xel = P['idx_ret']['XELKT'].reindex(idx)
    series = {
        'sepet_giris_t_kapanis_h3': (basket(3), 0), 'sepet_giris_t_kapanis_h2': (basket(2), 0),
        'sepet_giris_t_kapanis_h1': (basket(1), 0), 'sepet_giris_t1_acilis_cikis_t3': (basket(3, 'open1'), 0),
        'sepet_giris_t1_kapanis_cikis_t4': (basket(3), 1), 'sepet_giris_t1_kapanis_cikis_t3': (basket(2), 1),
        'XELKT_endeksi_giris_t_kapanis_h3_(alinamaz)': (elib.fwd_simple(xel.to_frame('m'), 3)['m'], 0),
        'XELKT_endeksi_giris_t1_kapanis_cikis_t4_(fon_benzeri)': (elib.fwd_simple(xel.to_frame('m'), 3)['m'], 1),
        'XELKT_endeksi_giris_t1_kapanis_cikis_t3_(fon_benzeri)': (elib.fwd_simple(xel.to_frame('m'), 2)['m'], 1),
        'XELKT_endeksi_giris_t1_kapanis_cikis_t2_(fon_benzeri)': (elib.fwd_simple(xel.to_frame('m'), 1)['m'], 1),
    }
    for sn in ('S1', 'S2'):
        for nm, (ser, lag) in series.items():
            s = C.S[sn].shift(lag, fill_value=False) if lag else C.S[sn]
            for per in PER:
                pm = pmask(idx, per)
                allp = ser[pm].dropna()
                dd = (s & ser.notna()).values & pm
                if dd.sum() < 5:
                    continue
                xx = (ser - allp.mean()).where(pd.Series(dd, index=idx), 0).fillna(0)[pm].values
                m, t = hac(xx, dd[pm], lag=3)
                rows.append({'soru': '6_giris_gecikmesi', 'sinyal': sn, 'varyant': nm, 'donem': per, 'n_gun': int(dd.sum()),
                             'ham_bps': 1e4 * ser[dd].mean(), 'per_bps': 1e4 * m, 't_per': t,
                             'her_gun_ortalama_bps': 1e4 * allp.mean()})
    # --- 17:50 vekili (XELKT 5 dakikalık; damga = bar başlangıcı, değer = bar sonu → 17:45 damgalı bar = 17:50 değeri)
    fn = os.path.join(panel, 'm5_isy', 'XELKT.parquet')
    if os.path.exists(fn):
        m5 = pd.read_parquet(fn)
        ts = pd.to_datetime(m5['ts_tr'])
        hm = ts.dt.hour * 60 + ts.dt.minute
        d = ts.dt.normalize()
        Lx = P['idx']['XELKT'].reindex(idx)
        sub = m5[(hm >= 17 * 60) & (hm < 17 * 60 + 50)]
        v = sub.groupby(d[sub.index])['c'].last().reindex(idx)
        last_bar = m5.groupby(d)['c'].last().reindex(idx)
        scale = (last_bar / Lx)
        info = {'soru': '6_vekil_1750', 'sinyal': '', 'varyant': 'olcek_denetimi', 'donem': 'm5',
                'oran_medyan': float(scale.median()), 'oran_p25': float((scale - 1).abs().quantile(0.95))}
        rows.append(info)
        v = v / scale.rolling(5, min_periods=1).median().shift(1).fillna(1.0)       # olası ölçek farkına karşı (≈ 1)
        prev_max = Lx.shift(1).rolling(19, min_periods=19).max()
        p1 = v >= prev_max
        std = xel.rolling(60, min_periods=40).std().shift(1)
        z = (v / Lx.shift(1) - 1) / std
        p2 = z >= 1.0
        zc = xel / std
        b3 = basket(3)
        for sn, pr, marj in (('S1', p1, v / prev_max - 1), ('S2', p2, (z - 1) * std)):
            tr = C.S[sn]
            for per in PER:
                pm = pmask(idx, per) & v.notna().values & (C.nfl >= 5).values & b3.notna().values
                if pm.sum() < 50:
                    continue
                mu = b3[pmask(idx, per)].mean()
                a, b = tr.values & pm, pr.values & pm
                def ex(mask):
                    return 1e4 * (b3[mask].mean() - mu) if mask.sum() else np.nan
                r = {'soru': '6_vekil_1750', 'sinyal': sn, 'varyant': 'XELKT_1750_degeriyle_sinyal', 'donem': per,
                     'n_gun': int(pm.sum()), 'n_kapanis_sinyali': int(a.sum()), 'n_vekil_sinyali': int(b.sum()),
                     'yakalama': float((a & b).sum() / max(a.sum(), 1)), 'kesinlik': float((a & b).sum() / max(b.sum(), 1)),
                     'per_kapanis_sinyali_bps': ex(a), 'per_vekil_sinyali_bps': ex(b),
                     'per_kacan_bps': ex(a & ~b), 'n_kacan': int((a & ~b).sum()),
                     'per_yanlis_alarm_bps': ex(b & ~a), 'n_yanlis_alarm': int((b & ~a).sum())}
                # eşiğin en az 25 bps üstünde olan vekil sinyali
                bm = b & (marj.values >= 0.0025)
                r['n_vekil_marj25'] = int(bm.sum()); r['kesinlik_marj25'] = float((a & bm).sum() / max(bm.sum(), 1))
                r['per_vekil_marj25_bps'] = ex(bm)
                rows.append(r)
    return pd.DataFrame(rows)


def main():
    panel, ek = sys.argv[1], sys.argv[2]
    C = setup(panel)
    parts = [q1(C), q2(C), q3(C), q4(C, ek), q5(C), q6(C, panel)]
    df = pd.concat(parts, ignore_index=True, sort=False)
    num = df.select_dtypes(include=[float]).columns
    df[num] = df[num].round(4)
    out = os.path.join(ek, 'v5_sepet.csv')
    df.to_csv(out, index=False)
    print('yazıldı:', out, df.shape)


if __name__ == '__main__':
    main()
