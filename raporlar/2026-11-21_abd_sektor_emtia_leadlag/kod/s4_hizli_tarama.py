"""S4 sağlık + temel tüketim: hızlı öncü taraması (eleme amaçlı, corr/t; ayakta kalanlar islem_testi ile sınanır)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, ortak
H = ortak.hizali_getiri
cift = {
 'TNX_fark': (['^TNX'], ['XBI','IBB','LABU','IWM','XLP','XLV']),
 'IWM': (['IWM'], ['XBI','LABU','CRSP','NTLA','BEAM']),
 'XBI': (['XBI'], ['CRSP','NTLA','BEAM','VKTX','MRNA','ARKG','IBB']),
 'XLK_eksi_XLP': (['XLK_XLP'], ['XLP','XLV','KO','PG','PM','MO']),
 'VIX_fark': (['^VIX'], ['XLP','XLV','XBI']),
 'CC=F': (['CC=F'], ['HSY','MDLZ']),
 'KC=F': (['KC=F'], ['SBUX']),
 'ZW=F': (['ZW=F','ZC=F'], ['GIS','CAG','KHC','TSN']),
 'LE/HE': (['LE=F','HE=F'], ['TSN']),
 'ZS/ZM/ZL': (['ZS=F','ZM=F','ZL=F','CRUSH'], ['ADM','BG']),
 'UUP': (['UUP'], ['PG','KO','PM','MDLZ','CL','EL','XLP']),
 'LLY': (['LLY'], ['NVO','VKTX','HIMS']),
 'NVO': (['NVO'], ['LLY','VKTX','HIMS']),
 'UNH': (['UNH'], ['HUM','ELV','CVS','CNC','CI','IHF']),
 'HUM': (['HUM'], ['UNH','ELV','CNC','CVS']),
 'TMO': (['TMO'], ['DHR','IQV','ILMN','A']),
 'WMT/COST': (['WMT','COST'], ['KR','DG','DLTR','TGT']),
 'NOVO-B.CO': (['NOVO-B.CO','AZN.L','NESN.SW'], ['NVO','LLY','AZN','XLP']),
 'kendi': (['XLV','XLP','XBI','KO','PG'], ['XLV','XLP','XBI','KO','PG']),
}
def oncu(s):
    if s == '^TNX':
        c = ortak.oku('^TNX')['close']; d = c.diff(); tk = ortak.takvim(); return d.reindex(tk)
    if s == '^VIX':
        c = ortak.oku('^VIX')['close']; return np.log(c).diff().reindex(ortak.takvim())
    if s == 'XLK_XLP': return H('XLK') - H('XLP')
    if s == 'CRUSH':  # soya kırma marjı ($/bu) günlük değişimi
        zs, zm, zl = [ortak.oku(x)['close'] for x in ['ZS=F','ZM=F','ZL=F']]
        m = (zm*0.022 + zl*0.11 - zs/100).dropna(); return m.diff().reindex(ortak.takvim())
    return H(s)
donem = [('2010-18','2010-01-01','2018-12-31'), ('2019-26','2019-01-01', None), ('2024-26','2024-01-01', None)]
out = []
for k, (os_, hs) in cift.items():
    hs = [h for h in hs if h in ortak.meta().index]
    X = pd.DataFrame({o: oncu(o) for o in os_})
    for h in (1, 3):
        for ad, b, e in donem:
            t = ortak.tarama(X, hs, h=h, bas=b, bit=e, min_n=200)
            if k == 'kendi': t = t[t.oncu == t.hedef] if False else t
            t['h'] = h; t['donem'] = ad; out.append(t)
# kendi gecikmesi (otokorelasyon) ayrı
for s in ['XLV','XLP','XBI','KO','PG','LLY','UNH']:
    X = pd.DataFrame({s + '_oto': H(s)})
    for h in (1, 3):
        for ad, b, e in donem:
            f = ortak.ileri_getiri([s], h); x = X.reindex(f.index)
            m = pd.concat([x, f], axis=1).dropna(); m = m[m.index >= b]; m = m[m.index <= e] if e else m
            c = m.corr().iloc[0, 1]; n = len(m) / h
            out.append(pd.DataFrame([(s + '_oto', s, len(m), c, c*np.sqrt(n-2)/np.sqrt(1-c*c), h, ad)], columns=['oncu','hedef','n','corr','t','h','donem']))
r = pd.concat(out)
p = r.pivot_table(index=['oncu','hedef','h'], columns='donem', values='t').round(1)
p['n19'] = r[r.donem=='2019-26'].set_index(['oncu','hedef','h'])['n']
p = p.reset_index().drop_duplicates(['oncu','hedef','h'])
yol = os.path.join(ortak.KOK, 'ek', 'hipotez', 's4_hizli_tarama.csv'); p.to_csv(yol, index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)
print(p.to_string(index=False))
