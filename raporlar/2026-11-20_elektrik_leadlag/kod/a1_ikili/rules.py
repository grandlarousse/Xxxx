"""A1 (hisse -> hisse ikili öncülük) kural üreticileri ve dondurulmuş kurallar.

build(P): YONTEM_EK E1 sözleşmesi. Bütün sinyaller yalnız t kapanışına kadarki bilgiyle kurulur
(shift / rolling / cumsum; tam örneklem istatistiği yok). Eşikler sayı olarak yazılıdır.
Üreticiler (grid.py de bunları kullanır):
  ln_signal  : genel "lider ağı" (yürüyen pencerede kestirilen lider skorları)
  gp_signal  : önceden yazılı grup çifti olay kuralı
  ps_signal  : grup çifti farkının 20 günlük z'si (geride kalan / öne geçen)
  pc_signal  : aynı ana faaliyet kümesindeki akranlara göre çift farkı z ortalaması
  fl_signal  : IS'te sabitlenmiş lider listesi (çifte özgü; yeni hisselere genellenemez)
"""
import os
import sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402

# Önceden yazılı ekonomik bağ grupları (YONTEM_EK E10). EUPWR yalnız kaynak (XELKT üyesi değil).
GROUPS = [['NATEN', 'ESEN', 'MAGEN'], ['ODAS', 'CANTE'], ['AHGAZ', 'ENERY'], ['SMRTG', 'ALFAS', 'EUPWR']]
# IS'te sabitlenen lider listesi {hedef: [kaynaklar]}: T1 h=1 t >= 2,5, n >= 1000 ve çiftin iki kronolojik yarısında t > 0.
FL_LINKS = {'ZOREN': ['ODAS', 'AYEN'], 'AKSEN': ['ODAS']}


def _cache(P, key, fn):
    c = P.setdefault('_cache', {})
    if key not in c:
        c[key] = fn()
    return c[key]


def zscore(P):
    """z_j(t) = r_cc(j,t) / (60 günlük, 1 gün gecikmeli std); yalnız tradable günler; ±4'te kırpılır."""
    def f():
        R = P['ret_cc']
        sd = R.rolling(60, min_periods=40).std().shift(1)
        return (R.where(P['tradable']) / sd).clip(-4, 4)
    return _cache(P, 'a1_z', f)


def sec_excess_today(P):
    """e_i(t) = r_cc(i,t) − aynı gün diğer tradable sektör üyelerinin eşit ağırlıklı r_cc'si (en az 4 diğer üye)."""
    def f():
        sec = elib.sector_cols(P)
        Rt = P['ret_cc'][sec].where(P['tradable'][sec])
        s = Rt.fillna(0).sum(axis=1)
        n = Rt.notna().sum(axis=1)
        on = (-Rt.notna().astype(int)).add(n, axis=0)
        os_ = (-Rt.fillna(0)).add(s, axis=0)
        return Rt - os_ / on.where(on >= 4)
    return _cache(P, 'a1_e', f)


def lead_t(P, W, minn=120):
    """Yürüyen lider istatistiği t_ji(t): son W takvim satırında x_j(s−1)·ez_i(s) çarpımının (s <= t) ortalamasının t'si.
    x_j = kaynak z'si; ez_i = hedefin sektöre göre fazla getirisi / kendi 60 günlük gecikmeli std'si (±4 kırpılı);
    hedef s−1'de dolabilir olmalı (tavan taşması dışarıda). Dönen: (t dizisi T×Ns×Ni, kaynak listesi, hedef listesi)."""
    def f():
        sec, src = elib.sector_cols(P), elib.sector_cols(P, extra=True)
        Z = zscore(P)
        e = sec_excess_today(P)
        ez = (e / e.rolling(60, min_periods=40).std().shift(1)).clip(-4, 4)
        Ei = ez.where(P['fill_long'][sec].shift(1, fill_value=False)).values
        Xs = Z[src].shift(1).values
        prod = Xs[:, :, None] * Ei[:, None, :]
        ok = np.isfinite(prod)
        p0 = np.where(ok, prod, 0.0)

        def roll(a):
            c = np.cumsum(a, axis=0, dtype=np.float64)
            out = c.copy()
            out[W:] -= c[:-W]
            return out
        n, s1, s2 = roll(ok), roll(p0), roll(p0 * p0)
        with np.errstate(all='ignore'):
            mu = s1 / n
            var = np.maximum(s2 / n - mu * mu, 1e-12)
            t = mu / np.sqrt(var / n)
        t = np.where(n >= minn, t, 0.0)
        for a, j in enumerate(src):
            if j in sec:
                t[:, a, sec.index(j)] = 0.0
        return np.round(t, 6), src, sec
    return _cache(P, ('a1_lead', W, minn), f)


def ln_score(P, W, c):
    """Skor_i(t) = Σ_j işaret(t_ji)·1{|t_ji| >= c}·z_j(t) / sqrt(K_i(t)); K = z'si olan etkin lider sayısı."""
    def f():
        t, src, sec = lead_t(P, W)
        L = np.where(np.abs(t) >= c, np.sign(t), 0.0)
        x = zscore(P)[src].values
        xv = np.isfinite(x)
        num = np.einsum('tj,tji->ti', np.where(xv, x, 0.0), L)
        K = np.einsum('tj,tji->ti', xv.astype(float), np.abs(L))
        with np.errstate(all='ignore'):
            sc = np.where(K >= 1, num / np.sqrt(np.maximum(K, 1)), np.nan)
        return pd.DataFrame(np.round(sc, 8), index=P['ret_cc'].index, columns=sec), pd.DataFrame(K, index=P['ret_cc'].index, columns=sec)
    return _cache(P, ('a1_score', W, c), f)


def _empty(P):
    sec = elib.sector_cols(P)
    return pd.DataFrame(False, index=P['ret_cc'].index, columns=sec)


def ln_signal(P, W, c, theta):
    sc, _ = ln_score(P, W, c)
    return (sc >= theta) & P['fill_long'][sc.columns]


def _event(P, j, kind, thr, up):
    Rt = P['ret_cc'][j].where(P['tradable'][j])
    x = Rt if kind == 'abs' else zscore(P)[j]
    return ((x >= thr) if up else (x <= -thr)).fillna(False)


def gp_signal(P, kind, thr, up):
    """Grup kardeşi j'de olay (r >= thr ya da z >= thr; aşağı yön simetrik) -> diğer kardeş(ler)de AL."""
    sig = _empty(P)
    cols = set(P['ret_cc'].columns)
    for g in GROUPS:
        for j in g:
            for i in g:
                if i != j and j in cols and i in sig.columns:
                    sig[i] = sig[i] | _event(P, j, kind, thr, up)
    return sig & P['fill_long'][sig.columns]


def pair_z(P, i, j, win=20, minp=15):
    """Kümülatif (r_i − r_j)'nin 20 günlük penceredeki z'si (iki hisse de tradable günlerde)."""
    def f():
        Rt = P['ret_cc'].where(P['tradable'])
        d = Rt[i] - Rt[j]
        C = d.fillna(0).cumsum().where(d.notna())
        return ((C - C.rolling(win, min_periods=minp).mean()) / C.rolling(win, min_periods=minp).std()).round(8)
    return _cache(P, ('a1_pz', i, j, win), f)


def ps_signal(P, theta, lag=True):
    """Grup çiftleri: lag=True -> z_ij <= −theta (i kardeşinin gerisinde) -> i'de AL; lag=False -> z_ij >= +theta."""
    sig = _empty(P)
    cols = set(P['ret_cc'].columns)
    for g in GROUPS:
        for j in g:
            for i in g:
                if i != j and j in cols and i in sig.columns:
                    z = pair_z(P, i, j)
                    sig[i] = sig[i] | ((z <= -theta) if lag else (z >= theta)).fillna(False)
    return sig & P['fill_long'][sig.columns]


def pc_signal(P, theta, kume, min_peers=2):
    """Aynı ana faaliyet kümesindeki akranlara göre z_ij ortalaması <= −theta -> i'de AL. kume: {sembol: küme adı}."""
    sig = _empty(P)
    for i in sig.columns:
        peers = [j for j in sig.columns if j != i and kume.get(j) is not None and kume.get(j) == kume.get(i)]
        if len(peers) < min_peers:
            continue
        Zp = pd.concat([pair_z(P, i, j) for j in peers], axis=1)
        m = Zp.mean(axis=1).where(Zp.notna().sum(axis=1) >= min_peers).round(8)
        sig[i] = (m <= -theta).fillna(False)
    return sig & P['fill_long'][sig.columns]


def fl_signal(P, theta, links=None):
    """IS'te sabitlenmiş lider listesi: Σ_j z_j(t) / sqrt(K) >= theta -> hedefte AL."""
    links = FL_LINKS if links is None else links
    sig = _empty(P)
    Z = zscore(P)
    for i, js in links.items():
        js = [j for j in js if j in Z.columns]
        if i not in sig.columns or not js:
            continue
        K = Z[js].notna().sum(axis=1)
        sc = (Z[js].fillna(0).sum(axis=1) / np.sqrt(K.where(K >= 1))).round(8)
        sig[i] = (sc >= theta).fillna(False)
    return sig & P['fill_long'][sig.columns]


# DONDURULMUŞ KURALLAR (IS 2010-01-04 → 2022-12-30 taramasından; ek/a1_ikili.md).
# BİRİNCİL KURAL YOK: hiçbir ızgara satırı birincil ölçütlerin (i)–(vii) tamamını karşılamadı. Aşağıdakilerin hepsi İKİNCİL (izleme).
# (ad, üretici, argümanlar, h, birincil, açıklama)
FROZEN = [
    ('A1_LN_W250_c2.0_th1.5_h1', ln_signal, dict(W=250, c=2.0, theta=1.5), 1, False,
     'Lider ağı: son 250 günde |t_ji| >= 2 olan liderlerin işaretli z ortalaması (Σ işaret·z_j/√K) >= 1,5 -> hedef XELKT hissesinde AL, 1 gün'),
    ('A1_LN_W250_c2.0_th1.5_h2', ln_signal, dict(W=250, c=2.0, theta=1.5), 2, False,
     'Lider ağı: son 250 günde |t_ji| >= 2 olan liderlerin işaretli z ortalaması >= 1,5 -> hedef XELKT hissesinde AL, 2 gün'),
    ('A1_LN_W500_c1.5_th1.5_h2', ln_signal, dict(W=500, c=1.5, theta=1.5), 2, False,
     'Lider ağı (komşu parametre): son 500 günde |t_ji| >= 1,5 olan liderlerin işaretli z ortalaması >= 1,5 -> hedefte AL, 2 gün'),
    ('A1_FL_th2.0_h1', fl_signal, dict(theta=2.0), 1, False,
     'IS\'te sabitlenmiş liderler (ODAS,AYEN -> ZOREN; ODAS -> AKSEN): Σ z_j/√K >= 2 -> hedefte AL, 1 gün; çifte özgü, IS seçimli'),
]


def build(P):
    out = []
    for ad, fn, kw, h, birincil, aciklama in FROZEN:
        out.append({'ad': ad, 'sig': fn(P, **kw), 'h': h, 'yon': 'long', 'olcu': 'sec', 'arac': 'spot',
                    'birincil': birincil, 'aciklama': aciklama})
    return out
