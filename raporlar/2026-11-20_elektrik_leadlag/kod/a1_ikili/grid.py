"""A1 kural ızgarası: bütün satırlar elib.evaluate(measure='sec') ile üretilir (yalnız IS paneli).
Kullanım: python3 -I grid.py <panel_is klasörü> <çıktı klasörü> [sonuç csv yolu]
"""
import sys, os, json, time
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
sys.path.insert(0, HERE)
import elib   # noqa: E402
import rules  # noqa: E402

PANEL = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'out')
CSV = sys.argv[3] if len(sys.argv) > 3 else os.path.join(OUT, 'a1_ikili_sonuc.csv')
os.makedirs(OUT, exist_ok=True)
SPLIT = pd.Timestamp('2019-12-31')


def kume_map():
    uy = pd.read_csv(os.path.join(HERE, '..', '..', 'ek', 'xelkt_uyeler.csv'), usecols=['sym', 'ana_faaliyet'])
    return {a: str(b).replace('?', '').strip() for a, b in zip(uy['sym'], uy['ana_faaliyet'])}


def grid_specs():
    """(ad, üretici, argümanlar, h, alt aile). Izgara önceden yazılıdır."""
    S = []
    for W in (250, 500):
        for c in (1.5, 2.0):
            for th in (1.0, 1.5, 2.0):
                for h in (1, 2, 3):
                    S.append((f'A1_LN_W{W}_c{c}_th{th}_h{h}', rules.ln_signal, dict(W=W, c=c, theta=th), h, 'lider_agi'))
    for kind, thrs in (('abs', (0.03, 0.05, 0.07)), ('z', (1.5, 2.0))):
        for thr in thrs:
            for up in (True, False):
                for h in (1, 2, 3):
                    S.append((f"A1_GP_{kind}{thr}_{'yukari' if up else 'asagi'}_h{h}", rules.gp_signal, dict(kind=kind, thr=thr, up=up), h, 'grup_cifti_olay'))
    for th in (1.0, 1.5, 2.0):
        for lag in (True, False):
            for h in (1, 2, 3):
                S.append((f"A1_PS_z{th}_{'geride' if lag else 'onde'}_h{h}", rules.ps_signal, dict(theta=th, lag=lag), h, 'grup_cifti_fark'))
    km = kume_map()
    for th in (1.0, 1.5, 2.0):
        for h in (1, 2, 3):
            S.append((f'A1_PC_z{th}_geride_h{h}', rules.pc_signal, dict(theta=th, kume=km), h, 'kume_fark'))
    for th in (1.0, 1.5, 2.0):
        for h in (1, 2, 3):
            S.append((f'A1_FL_th{th}_h{h}', rules.fl_signal, dict(theta=th), h, 'sabit_lider_listesi'))
    return S


def all_rules(P):
    return [{'ad': ad, 'sig': fn(P, **kw), 'h': h} for ad, fn, kw, h, _ in grid_specs()]


def halves(sig, P, h):
    cols = list(sig.columns)
    M, fl = elib.excess_measures(P, h, 'long', cols)
    p, ntr, X = elib.day_series(sig, M['sec'], fl)
    p = p[p.index <= elib.IS_END]
    d = p.dropna()
    a = elib.stats_block(p, ntr.reindex(p.index), X.reindex(p.index), h, None, SPLIT)
    b = elib.stats_block(p, ntr.reindex(p.index), X.reindex(p.index), h, SPLIT + pd.Timedelta(days=1), None)
    tur = 'takvim'
    if min(a['n_gun'], b['n_gun']) < 20 and len(d) >= 20:
        mid = d.index[len(d) // 2]
        a = elib.stats_block(p, ntr.reindex(p.index), X.reindex(p.index), h, None, mid - pd.Timedelta(days=1))
        b = elib.stats_block(p, ntr.reindex(p.index), X.reindex(p.index), h, mid, None)
        tur = 'kronolojik'
    ds = d.sort_values()
    ex10 = 1e4 * ds.iloc[:-10].mean() if len(ds) > 15 else np.nan
    return {'en_iyi_10_gun_haric_bps': ex10, 'yari_turu': tur, 'yari1_n': a['n_gun'], 'yari1_bps': a['ort_gun_bps'], 'yari1_t': a['t'],
            'yari2_n': b['n_gun'], 'yari2_bps': b['ort_gun_bps'], 'yari2_t': b['t']}


def criteria(r):
    """Birincil ölçütler (i)–(v) mekanik; (vi)–(vii) notta elle."""
    fail = []
    if not (r.get('net_temel_bps_IS', np.nan) > 0):
        fail.append('i:net<=0')
    if not (r.get('yari1_bps', np.nan) > 0 and r.get('yari2_bps', np.nan) > 0):
        fail.append('ii:yarılar')
    if not (r.get('top10_haric_bps', np.nan) > 0):
        fail.append('iii:top10')
    if not (r.get('giris_kapanis1_bps', np.nan) > 0):
        fail.append('iv:kapanis1')
    if r.get('en_yogun_pay', 1) > 0.5:
        fail.append('v:tek hisse')
    if r.get('n_bagimsiz_IS', 0) < 40:
        fail.append('olay<40')
    return fail


if __name__ == '__main__':
    t0 = time.time()
    P = elib.load(PANEL)
    assert P['ret_cc'].index.max() <= elib.IS_END, 'KÖR PROTOKOL: panel IS sonunu aşıyor'
    tb = time.time()
    frozen = {r['ad']: r for r in rules.build(P)}
    build_s = time.time() - tb
    rows = []
    for ad, fn, kw, h, alt in grid_specs():
        sig = fn(P, **kw)
        r = elib.evaluate(sig, P, h=h, side='long', measure='sec', name=ad, family='A1', extra={'alt_aile': alt})
        r.update(halves(sig, P, h))
        f = criteria(r)
        r['olcut_eksik'] = ';'.join(f)
        r['secim'] = ('birincil' if frozen[ad]['birincil'] else 'ikincil') if ad in frozen else 'elendi'
        r['not'] = ('ölçütler i–v tamam' if not f else 'karşılanmayan: ' + ', '.join(f))
        rows.append(r)
    # ızgara dışı dondurulmuş kural varsa onu da yaz
    for ad, r0 in frozen.items():
        if ad not in {r['sinyal_tanimi'] for r in rows}:
            r = elib.evaluate(r0['sig'], P, h=r0['h'], side='long', measure='sec', name=ad, family='A1', extra={'alt_aile': 'izgara_disi'})
            r.update(halves(r0['sig'], P, r0['h'])); f = criteria(r)
            r['olcut_eksik'] = ';'.join(f); r['secim'] = 'birincil' if r0['birincil'] else 'ikincil'; r['not'] = 'ızgara dışı (keşif); ' + ', '.join(f)
            rows.append(r)
    notes_path = os.path.join(HERE, 'notlar.json')
    if os.path.exists(notes_path):
        notes = json.load(open(notes_path, encoding='utf-8'))
        for r in rows:
            ks = [k for k in notes if r['sinyal_tanimi'].startswith(k)]
            if ks:
                r['not'] = notes[max(ks, key=len)] + ' | ' + r['not']
    df = elib.to_csv(rows, CSV)
    df['bh_gecti'] = False
    for alt in df['alt_aile'].unique():
        for h in (1, 2, 3):
            m = (df['alt_aile'] == alt) & (df['h'] == h)
            df.loc[m, 'bh_gecti'] = elib.bh_fdr(df.loc[m, 'p_tek_IS'].values, 0.10)
    df['bh_tum_izgara'] = elib.bh_fdr(df['p_tek_IS'].values, 0.10)
    df['aday_mi'] = df['secim'] == 'birincil'
    df.to_csv(CSV, index=False)
    show = ['sinyal_tanimi', 'n_gun_IS', 'n_bagimsiz_IS', 'n_islem_IS', 'ort_fazla_IS_bps', 't_IS', 'basabas_IS_bps', 'maliyet_temel_bps', 'net_temel_bps_IS',
            'yari1_n', 'yari1_bps', 'yari2_n', 'yari2_bps', 'top10_haric_bps', 'giris_kapanis1_bps', 'gece_payi', 'en_yogun_hisse', 'en_yogun_pay',
            'yil_pozitif_orani', 'dol_own_IS_bps', 'bh_gecti', 'olcut_eksik']
    pd.set_option('display.width', 400); pd.set_option('display.max_columns', 50); pd.set_option('display.max_rows', 500)
    print(df[show].round(2).to_string(index=False))
    print(f'\nızgara satırı: {len(df)} | ölçüt i–v tamam: {int((df["olcut_eksik"] == "").sum())} | BH (alt aile × h): {int(df["bh_gecti"].sum())} | BH (tüm ızgara): {int(df["bh_tum_izgara"].sum())}')
    # nedensellik öz-denetimi: ızgaranın tamamı + dondurulmuş kurallar
    chk = elib.self_check_causal(all_rules, P)
    bad = {k: v for k, v in chk.items() if v != 0}
    print(f'öz-denetim (ızgara, {len(chk)} kural): sıfırdan farklı = {len(bad)}', bad)
    chk2 = elib.self_check_causal(rules.build, P)
    print('öz-denetim (rules.build):', json.dumps(chk2))
    print(f'rules.build süresi {build_s:.1f}s | birincil {sum(r["birincil"] for r in frozen.values())} | ikincil {sum(not r["birincil"] for r in frozen.values())}')
    json.dump({'izgara_satir': len(df), 'build_s': build_s, 'oz_denetim_izgara_hatali': bad, 'oz_denetim_build': chk2, 'sure_s': time.time() - t0},
              open(os.path.join(OUT, 'grid_ozet.json'), 'w'), indent=1)
    print(f'süre {time.time()-t0:.0f}s')
