"""oos_degerlendir.py — dondurulmuş kuralların tek ortak değerlendirmesi (YONTEM_EK E1, E6, E7).

Kullanım:
    python3 -I oos_degerlendir.py <panel_is> <panel_degerlendirme> <cikti.csv> <ajan1> <ajan2> ...
    (ajan = kod/<ajan>/rules.py içinde build(P) fonksiyonu olan klasör adı)

Yaptıkları:
1. Her ajanın build() fonksiyonunu hem panel_is hem değerlendirme paneliyle çağırır.
2. Nedensellik denetimi: iki panelden üretilen sinyaller IS tarihlerinde aynı olmalı (fark oranı raporlanır; > %0,5 ise kural elenir).
3. Kuralları değerlendirme panelinde elib.eval_rule ile hesaplar (IS, OOS1 ve varsa KASA sütunları).
4. Birincil kurallara OOS-1 tek yönlü p-değerleriyle Benjamini–Hochberg (q=0,10), ikincil kurallara Bonferroni uygular.
5. Aday şartlarını sütun olarak yazar.
"""
import importlib.util
import os
import sys
import traceback

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import elib  # noqa: E402

KOD = os.path.dirname(HERE)


def load_rules(agent, P):
    path = os.path.join(KOD, agent, 'rules.py')
    spec = importlib.util.spec_from_file_location(f'rules_{agent}', path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    try:
        spec.loader.exec_module(mod)
        rules = mod.build(P)
    finally:
        sys.path.pop(0)
    return rules


def causality(sig_is, sig_ev, trad_ev=None):
    """IS tarihlerinde iki sinyal matrisinin farkı / IS'teki True sayısı.
    Değerlendirme panelinde IS'te hiç bulunmayan (sonradan halka arz olan) sütunlar yalnız o tarihte işlem görebilir
    oldukları hücrelerde sayılır: IS tarihlerinde işlem görmeyen bir hissede True olması sonucu etkilemez."""
    idx = sig_is.index[sig_is.index <= elib.IS_END]
    cols = sorted(set(sig_is.columns) | set(sig_ev.columns))
    a = sig_is.reindex(index=idx, columns=cols).fillna(False).astype(bool)
    b = sig_ev.reindex(index=idx, columns=cols).fillna(False).astype(bool)
    d = (a != b)
    extra = [c for c in cols if c not in sig_is.columns]
    if trad_ev is not None and extra:
        tr = trad_ev.reindex(index=idx, columns=extra).fillna(False).astype(bool)
        d[extra] = d[extra] & tr
    diff = int(d.values.sum())
    tot = int(a.values.sum())
    return diff, tot, (diff / max(tot, 1))


def main():
    panel_is, panel_ev, out = sys.argv[1], sys.argv[2], sys.argv[3]
    agents = sys.argv[4:]
    P_is = elib.load(panel_is)
    P_ev = elib.load(panel_ev)
    rows, log = [], []
    for ag in agents:
        try:
            r_is = {r['ad']: r for r in load_rules(ag, P_is)}
            r_ev = {r['ad']: r for r in load_rules(ag, P_ev)}
        except Exception:
            log.append(f'{ag}: build() HATA\n{traceback.format_exc()}')
            continue
        n_bir = sum(1 for r in r_ev.values() if r.get('birincil'))
        log.append(f'{ag}: {len(r_ev)} kural ({n_bir} birincil)')
        if n_bir > 4:
            log.append(f'  UYARI: {ag} birincil kural sayısı {n_bir} > 4; ilk 4 birincil sayıldı')
            k = 0
            for r in r_ev.values():
                if r.get('birincil'):
                    k += 1
                    if k > 4:
                        r['birincil'] = False
        for ad, r in r_ev.items():
            try:
                if ad not in r_is:
                    diff, tot, frac = -1, 0, 1.0
                else:
                    diff, tot, frac = causality(r_is[ad]['sig'], r['sig'], P_ev['tradable'])
                for row in elib.eval_rule(r, P_ev, family=ag):
                    row['ajan'] = ag
                    row['nedensellik_fark'] = diff; row['nedensellik_oran'] = frac
                    row['nedensellik_ok'] = bool(frac <= 0.005)
                    rows.append(row)
            except Exception:
                log.append(f'{ag}/{ad}: değerlendirme HATA\n{traceback.format_exc()}')
    df = pd.DataFrame(rows)
    if len(df):
        # karar satırı: spot kurallarda spot satırı; viop kurallarında vadeli fiyatlı satır
        is_dec = ~((df['arac'] == 'viop') & df['sinyal_tanimi'].isin(df.loc[df['arac'] == 'viop_vadeli', 'sinyal_tanimi']))
        df['karar_satiri'] = is_dec
        for per in ['OOS1', 'KASA']:
            col = f'p_tek_{per}'
            if col not in df.columns:
                continue
            m_b = df['karar_satiri'] & df['birincil'] & df['nedensellik_ok']
            df[f'bh_{per}'] = False
            df.loc[m_b, f'bh_{per}'] = elib.bh_fdr(df.loc[m_b, col].values, 0.10)
            m_s = df['karar_satiri'] & ~df['birincil'] & df['nedensellik_ok']
            df[f'bonf_{per}'] = False
            ns = max(int(m_s.sum()), 1)
            df.loc[m_s, f'bonf_{per}'] = df.loc[m_s, col].values <= 0.10 / ns
            df[f'holm_{per}'] = False
            m_a = df['karar_satiri'] & df['nedensellik_ok']
            df.loc[m_a, f'holm_{per}'] = elib.holm(df.loc[m_a, col].values, 0.10)
        if 't_OOS1' in df.columns:
            eff_is, eff_o = df['ort_fazla_IS_bps'], df['ort_fazla_OOS1_bps']
            df['s2_oos_yon_buyukluk'] = (df['t_OOS1'] >= 1.5) & (eff_o >= 0.5 * eff_is) & (eff_is > 0)
            net = df.get('net_temel_bps_OOS1')
            thr = np.where(df['arac'].astype(str).str.startswith('viop'), 10.0, 15.0)
            if net is not None:
                netv = net.where(net.notna(), df.get('settle_net_temel_OOS1_bps'))
                df['s3_net_temel'] = netv >= thr
            nb = df.get('n_bagimsiz_IS', 0).fillna(0) + df.get('n_bagimsiz_OOS1', 0).fillna(0)
            df['n_bagimsiz_toplam'] = nb
            df['s4_olay_sayisi'] = (nb >= 100) & (df.get('n_bagimsiz_OOS1', 0).fillna(0) >= 30)
            df['s5_top10'] = df.get('top10_haric_bps', pd.Series(np.nan, index=df.index)) > 0
            geç = (df['bh_OOS1'] | df['bonf_OOS1'])
            df['aday'] = geç & df['s2_oos_yon_buyukluk'] & df['s3_net_temel'].fillna(False) & df['s4_olay_sayisi'] & df['nedensellik_ok']
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    df.to_csv(out, index=False)
    with open(out.replace('.csv', '_log.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(log))
    print('\n'.join(log))
    print('satır:', len(df), '→', out)


if __name__ == '__main__':
    main()
