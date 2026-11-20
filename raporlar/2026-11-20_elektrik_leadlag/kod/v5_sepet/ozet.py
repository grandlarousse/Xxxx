"""v5_sepet.csv'yi soru soru ekrana döker.  Kullanım: python3 -I ozet.py <v5_sepet.csv> [soru_öneki]"""
import sys
import pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_columns', 60)
df = pd.read_csv(sys.argv[1])
pre = sys.argv[2] if len(sys.argv) > 2 else ''
ORD = ['IS', 'OOS1', 'KASA', 'HAVUZ']


def wide(q, vals, idx=('sinyal', 'varyant')):
    w = q.pivot_table(index=list(idx), columns='donem', values=vals, sort=False)
    w = w.reindex(columns=[(v, p) for v in vals for p in ORD if (v, p) in w.columns])
    return w.round(1)


for soru, q in df.groupby('soru', sort=False):
    if not soru.startswith(pre):
        continue
    q = q.dropna(axis=1, how='all')
    print('\n=====', soru, q.shape)
    if soru == '1_rastgele_N':
        print(wide(q, ['ham_bps', 'ham_medyan_bps', 'ham_p10_bps', 'ham_p90_bps']).to_string())
        print(wide(q, ['ham_std_bps', 'izleme_sapmasi_bps', 'zarar_olasiligi_net_temel', 'per_net_temel_bps']).round(2).to_string())
        print(wide(q, ['yatirimci_per_net_p10_bps', 'yatirimci_per_net_p90_bps', 'yatirimci_per_net_eksi_olasiligi', 'ort_n_hisse']).round(2).to_string())
    elif soru == '2_secim':
        print(wide(q, ['per_bps', 't_per', 'per_net_temel_bps', 'per_net_muh_bps']).to_string())
        print(wide(q, ['ham_bps', 'fark_per_tamsepet_bps', 't_fark_per', 'fark_ham_tamsepet_bps']).to_string())
        print(wide(q, ['n_gun', 'ort_n_hisse', 'maliyet_temel_bps', 'zarar_olasiligi_net_temel', 'ham_std_bps']).round(2).to_string())
        f = q[q.donem == 'IS'][['sinyal', 'varyant', 'uc_donemde_kotu_degil_per', 'uc_donemde_kotu_degil_per_net', 'uc_donemde_kotu_degil_ham']]
        print(f[f.varyant != 'tam_sepet'].to_string(index=False))
    elif soru in ('4_hisse',):
        print(q.drop(columns=['soru', 'sinyal', 'donem'], errors='ignore').round(3).to_string(index=False))
    else:
        print(q.drop(columns=['soru'], errors='ignore').round(2).to_string(index=False))
