"""A3 ek kontroller (yalnız IS): bağımsız sağlama, beşte birlik profili, taban ayrıştırması, VİOP kısa yön,
en iyi 10 gün hariç, yer değiştirme (kaydırma) testi. Kullanım: python3 -I scan2.py <panel_is> <cikti_klasoru>"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ortak'))
import elib  # noqa: E402
import rules as RL  # noqa: E402

panel, out = sys.argv[1], sys.argv[2]
P = elib.load(panel)
assert P['ret_cc'].index.max() <= elib.IS_END
F = RL.feats(P)
sc = F['sc']
H1_END = pd.Timestamp('2019-12-31')
L = []


def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    L.append(s)


# 1) bağımsız sağlama: rel1 alt beşte birlik, h=1 (kütüphane kullanmadan; kilit kaydırması yok)
R = P['ret_cc'][sc]; T = P['tradable'][sc]; FL = P['fill_long'][sc]
f1 = R.shift(-1)
X = f1.where(FL)
S, N = X.sum(axis=1, min_count=1), X.notna().sum(axis=1)
exc = pd.DataFrame({c: f1[c] - ((S - X[c].fillna(0)) / (N - X[c].notna())).where((N - X[c].notna()) >= 4) for c in sc})
sig = RL.sig_quint(F, 1, 'bottom')
pm = exc.where(sig & FL).mean(axis=1).dropna()
say('1) bağımsız sağlama T2_rel1_alt5_h1: gün', len(pm), 'ort bps', round(1e4 * pm.mean(), 2),
    't(basit)', round(pm.mean() / pm.std() * np.sqrt(len(pm)), 2))

# 2) beşte birlik profili (sec fazla getiri, gün kümeli)
say('2) beşte birlik profili (sec, bps/gün; q1 = en geride kalan):')
for k in (1, 3, 5):
    rel = F[f'rel{k}']
    n = rel.notna().sum(axis=1)
    pct = rel.rank(axis=1, pct=True)
    q = np.ceil(pct * 5).where(rel.notna())
    for h in (1, 3):
        M, fl = elib.excess_measures(P, h, 'long', sc)
        vals = []
        for j in range(1, 6):
            p = M['sec'].where((q == j) & fl & (n.values[:, None] >= RL.MIN_N)).mean(axis=1).dropna()
            vals.append(f'q{j}:{1e4 * p.mean():.1f}')
        say(f'   rel{k} h{h}:', ' '.join(vals))

rows = []


def ev(s, h, name, measure='sec', tarama='tani', **kw):
    s = s.reindex(columns=sc).fillna(False).astype(bool)
    M, fl = elib.excess_measures(P, h, 'long', sc)
    p, _, _ = elib.day_series(s, M[measure], fl, 1)
    a, b = p[p.index <= H1_END].dropna(), p[p.index > H1_END].dropna()
    d = p.dropna().sort_values()
    ex = {'tarama': tarama, 'yari1_bps': 1e4 * a.mean(), 'yari1_n': len(a), 'yari2_bps': 1e4 * b.mean(), 'yari2_n': len(b),
          'top10gun_haric_bps': 1e4 * d.iloc[:-10].mean() if len(d) > 20 else np.nan,
          'alt10gun_haric_bps': 1e4 * d.iloc[10:].mean() if len(d) > 20 else np.nan}
    r = elib.evaluate(s, P, h=h, side='long', name=name, family='A3', measure=measure, extra=ex)
    rows.append(r)
    return r


# 3) taban ayrıştırması
LD = P['lim_dn'][sc]
for h in (1, 2, 3):
    ev(RL.sig_quint(F, 1, 'bottom') & ~LD, h, f'T2_rel1_alt5_h{h}_tabansiz')
    ev(RL.sig_quint(F, 1, 'bottom') & LD, h, f'T2_rel1_alt5_h{h}_yalniz_taban')

# 4) aday satırlar için "en iyi 10 gün hariç" (kütüphane max(10, %5) gün çıkarıyor)
cands = {
    'T2_rel1_alt5_h1': (RL.sig_quint(F, 1, 'bottom'), 1, 'sec'),
    'T2_rel5_alt5_h3': (RL.sig_quint(F, 5, 'bottom'), 3, 'sec'),
    'T2_rel5_ust5_h3': (RL.sig_quint(F, 5, 'top'), 3, 'sec'),
    'T2_rel5_ust5_h2': (RL.sig_quint(F, 5, 'top'), 2, 'sec'),
    'T4_vhi_z15_yukari_vlo_h3_own': (RL.sig_xgroup(F, 'vhi', 'vlo', 1.5), 3, 'own'),
    'T4_vhi_z15_yukari_vlo_h2_own': (RL.sig_xgroup(F, 'vhi', 'vlo', 1.5), 2, 'own'),
    'T3_big_z10_yukari_small_h3_own': (RL.sig_xgroup(F, 'big', 'small', 1.0), 3, 'own'),
    'T3_big_z10_asagi_small_h1_own': (RL.sig_xgroup(F, 'big', 'small', 1.0, -1), 1, 'own'),
}
say('4/5) aday satırlar: ort | en iyi 10 gün hariç | en kötü 10 gün hariç | kaydırma p (üst kuyruk) | p (alt kuyruk)')
for nm, (s, h, ms) in cands.items():
    r = ev(s, h, nm + '_tani', measure=ms)
    real, pv, null = elib.shift_null(s.reindex(columns=sc), P, h=h, side='long', measure=ms, n=300, seed=1)
    null = null[np.isfinite(null)]
    p_lo = (np.sum(null <= real) + 1) / (len(null) + 1)
    say(f'   {nm}: {r["ort_fazla_IS_bps"]:.1f} | {r["top10gun_haric_bps"]:.1f} | {r["alt10gun_haric_bps"]:.1f} | {pv:.3f} | {p_lo:.3f}')

# 6) VİOP kısa yön (ızgaranın yön tamamlayıcısı): alt beşte birlikteki AKSEN/ENJSA/ODAS → SAT
vrows = []
for k in (1, 3, 5):
    for h in (1, 2, 3):
        s = RL.sig_quint(F, k, 'bottom')[[c for c in elib.VIOP if c in sc]]
        r = elib.evaluate(s, P, h=h, side='short', name=f'T2v_rel{k}_alt5_viop_sat_h{h}', family='A3', measure='sec',
                          instrument='viop', extra={'tarama': 'T2_viop_kisa'})
        vrows.append(r)
        if 'viop_front' in P:
            rv = elib.evaluate_viop(s, P, h=h, side='short', name=f'T2v_rel{k}_alt5_viop_sat_h{h}_vadeli', family='A3',
                                    extra={'tarama': 'T2_viop_kisa_vadeli'})
            vrows.append(rv)
say('6) VİOP kısa (alt beşte birlik, AKSEN/ENJSA/ODAS): ad | n_gun | sec fazla bps | t | net temel | own bps (t)')
for r in vrows:
    if r['arac'] == 'viop':
        say(f"   {r['sinyal_tanimi']}: {r['n_gun_IS']} | {r['ort_fazla_IS_bps']:.1f} | {r['t_IS']:.2f} | {r['net_temel_bps_IS']:.1f} | "
            f"{r['dol_own_IS_bps']:.1f} ({r['dol_own_IS_t']:.2f})")
    else:
        say(f"   {r['sinyal_tanimi']}: {r['n_gun_IS']} | own_vadeli {r['ort_fazla_IS_bps']:.1f} | t {r['t_IS']:.2f} | "
            f"settle net {r.get('settle_net_temel_IS_bps', np.nan):.1f} | last net {r.get('last_net_temel_IS_bps', np.nan):.1f}")

say('3) taban ayrıştırması: ad | n_gun | n_islem | sec bps | t | yarı1 | yarı2 | kapanış+1')
for r in rows:
    if 'taban' in r['sinyal_tanimi']:
        say(f"   {r['sinyal_tanimi']}: {r['n_gun_IS']} | {r['n_islem_IS']} | {r['ort_fazla_IS_bps']:.1f} | {r['t_IS']:.2f} | "
            f"{r['yari1_bps']:.1f} | {r['yari2_bps']:.1f} | {r['giris_kapanis1_bps']:.1f}")

# 7) KEŞİF (ızgara dışı; aday olamaz): likidite etkileşimi ve hacimli sepetin kendi devamı
n0 = len(rows)
vcols = [c for c in elib.VIOP if c in sc]
for h in (1, 2, 3):
    b1 = RL.sig_quint(F, 1, 'bottom')
    ev(b1 & F['big'], h, f'K_rel1_alt5_buyuk_h{h}', tarama='kesif')
    ev(b1 & F['small'] & ~LD, h, f'K_rel1_alt5_kucuk_tabansiz_h{h}', tarama='kesif')
    ev(RL.sig_quint(F, 5, 'top') & F['big'], h, f'K_rel5_ust5_buyuk_h{h}', tarama='kesif')
    for ms in ('own', 'sec'):
        ev(RL.sig_xgroup(F, 'vhi', 'vhi', 1.5), h, f'K_vhi_z15_yukari_vhi_h{h}_{ms}', measure=ms, tarama='kesif')
    s = b1[vcols]
    r = elib.evaluate(s, P, h=h, side='long', name=f'K_rel1_alt5_viop_al_h{h}', family='A3', measure='sec', instrument='viop',
                      extra={'tarama': 'kesif_viop'})
    vrows.append(r)
    say(f"7v) {r['sinyal_tanimi']}: gün {r['n_gun_IS']} bağımsız {r['n_bagimsiz_IS']} | sec {r['ort_fazla_IS_bps']:.1f} t {r['t_IS']:.2f} net "
        f"{r['net_temel_bps_IS']:.1f} | own {r['dol_own_IS_bps']:.1f} ({r['dol_own_IS_t']:.2f}) | kap1 {r['giris_kapanis1_bps']:.1f} | "
        f"yoğun {r['en_yogun_hisse']} {r['en_yogun_pay']:.2f} | yıllar {r['yillar_bps']}")
    rv = elib.evaluate_viop(s, P, h=h, side='long', name=f'K_rel1_alt5_viop_al_h{h}_vadeli', family='A3', extra={'tarama': 'kesif_viop_vadeli'})
    vrows.append(rv)
    say(f"    vadeli: gün {rv['n_gun_IS']} | own_vadeli(kötüsü) {rv['ort_fazla_IS_bps']:.1f} t {rv['t_IS']:.2f} | settle net "
        f"{rv['settle_net_temel_IS_bps']:.1f} last net {rv['last_net_temel_IS_bps']:.1f} | yıllar {rv['settle_yillar_bps']}")
say('7) keşif satırları: ad | n_gun | n_islem | fazla bps | t | net temel | yarı1 | yarı2 | en iyi 10 gün hariç | kapanış+1 | yoğun pay')
for r in rows[n0:]:
    say(f"   {r['sinyal_tanimi']}: {r['n_gun_IS']} | {r['n_islem_IS']} | {r['ort_fazla_IS_bps']:.1f} | {r['t_IS']:.2f} | {r['net_temel_bps_IS']:.1f} | "
        f"{r['yari1_bps']:.1f} | {r['yari2_bps']:.1f} | {r['top10gun_haric_bps']:.1f} | {r['giris_kapanis1_bps']:.1f} | {r['en_yogun_pay']:.2f}")

elib.to_csv(rows + vrows, os.path.join(out, 'scan_rows2.csv'))
open(os.path.join(out, 'tanilama.txt'), 'w').write('\n'.join(L) + '\n')
