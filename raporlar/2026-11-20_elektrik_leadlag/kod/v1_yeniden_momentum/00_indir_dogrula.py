"""V1: İş Yatırım'dan yeniden indirilen dosyaları raw/d1 ile karşılaştırır (transactionId hariç).
Kullanım: python3 -I 00_indir_dogrula.py <raw_d1> <yeni_indirme_klasoru>"""
import sys, json, os
raw, new = sys.argv[1], sys.argv[2]
KEYS = ['HG_KAPANIS', 'HGDG_KAPANIS', 'HG_MIN', 'HG_MAX', 'HG_HACIM', 'HGDG_HACIM']
ok_all = True
for f in sorted(os.listdir(new)):
    if not f.endswith('.json'):
        continue
    if f.startswith('IDX_'):
        a = json.load(open(os.path.join(raw, 'isy_endeks', f[4:])))['data']
        b = json.load(open(os.path.join(new, f)))['data']
        da, db = {int(x[0]): x[1] for x in a}, {int(x[0]): x[1] for x in b}
        common = set(da) & set(db)
        diff = [k for k in common if da[k] != db[k]]
        print(f"{f[4:-5]:6s} endeks ham_n={len(da)} yeni_n={len(db)} ortak={len(common)} farkli_deger={len(diff)} "
              f"yalniz_ham={len(set(da) - set(db))} yalniz_yeni={len(set(db) - set(da))}")
        ok_all &= (len(diff) == 0 and len(set(da) ^ set(db)) == 0)
    else:
        a = json.load(open(os.path.join(raw, 'isy_hisse', f)))['value']
        b = json.load(open(os.path.join(new, f)))['value']
        da = {x['HGDG_TARIH']: tuple(x.get(k) for k in KEYS) for x in a}
        db = {x['HGDG_TARIH']: tuple(x.get(k) for k in KEYS) for x in b}
        common = set(da) & set(db)
        diff = [k for k in common if da[k] != db[k]]
        print(f"{f[:-5]:6s} hisse  ham_n={len(da)} yeni_n={len(db)} ortak={len(common)} farkli_satir={len(diff)} "
              f"yalniz_ham={len(set(da) - set(db))} yalniz_yeni={len(set(db) - set(da))}")
        ok_all &= (len(diff) == 0 and len(set(da) ^ set(db)) == 0)
print('SONUC:', 'AYNI' if ok_all else 'FARK VAR')
