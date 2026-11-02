# T14: Çoklu test: rapor edilen test sayıları toplamı, küresel Bonferroni/BH eşikleri; güven etiketli bulgular bu eşiklerden geçiyor mu?
import pandas as pd, numpy as np, re
from scipy import stats
D=pd.read_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji/all_findings.parquet')
for c in ['corr_full','pcorr_xu100','t_stat','n','bt_oos_mean_bps','bt_oos_sharpe']: D[c]=pd.to_numeric(D[c].replace('nan',np.nan),errors='coerce')
counts={'r1_tarama':481000,'r1_banka':61100,'r1_havacilik':16365,'r1_holding':39276,'r1_kimya':39132,'r1_metal':28440,'r1_otomotiv':35220,'r1_savunma':13662,'r1_tuketim':22480,'r1_enerji':39060,'r1_cin':474,'r1_gunici':1934,'r1_olay':200,
        'ry_hisse':240000,'ry_ag':82000,'ry_endeks':17526,'ry_grup':1000,'ry_gunici_y':3000,'ry_viop':2600,'ry_akis':500}
N=sum(counts.values()); print('Raporlanan birincil test toplamı ≈',N)
for a in [0.05]:
    zb=stats.norm.isf(a/2/N); print(f'Küresel Bonferroni (α={a}) |t| eşiği = {zb:.2f}')
# 'n_eff' kabaca: tarama tekrarları nedeniyle bağımsız test sayısı çok daha az; alternatif: 50k bağımsız test
for Ne in [50000,10000]:
    print(f'  bağımsız test ≈{Ne}: |t| eşiği = {stats.norm.isf(0.025/Ne):.2f}')
D['conf2']=D['conf'].str.replace(' ','').str.replace('(','').str[:6]
def bucket(c):
    c=str(c)
    if c.startswith('YUKSEK') or c.startswith('YÜKSEK'): return 'YUKSEK'
    if c.startswith('ORTA'): return 'ORTA'
    if c.startswith('COK') or c.startswith('ÇOK'): return 'COK_DUSUK'
    if c.startswith('DUSUK') or c.startswith('DÜŞÜK'): return 'DUSUK'
    return 'diger'
D['cb']=D['confidence'].astype(str).str.upper().str.strip().map(bucket)
# t yoksa corr ve n'den yaklaşık t
D['t_eff']=D['t_stat']
m=D['t_eff'].isna()&D['corr_full'].notna()&D['n'].notna()
D.loc[m,'t_eff']=D.loc[m,'corr_full']*np.sqrt(D.loc[m,'n'])
tradable=['lead_intra','lead_multiday','lead_auction','intraday_minutes','lead_hourly','lead_5m','backtest','event','flow','liquidity','intraday_momentum']
X=D[D.cb.isin(['YUKSEK','ORTA'])]
print('\nYÜKSEK/ORTA etiketli satır:',len(X))
tab=X.assign(pass55=X.t_eff.abs()>=5.47,pass45=X.t_eff.abs()>=4.5,has_t=X.t_eff.notna()).groupby(['relation','cb']).agg(n=('agent','size'),t_var=('has_t','sum'),bonf_gecen=('pass55','sum'),t45=('pass45','sum'),medyan_abs_t=('t_eff',lambda x: x.abs().median())).reset_index()
pd.set_option('display.width',220); print(tab[tab.n>=3].sort_values(['relation','cb']).to_string(index=False))
# işlenebilir ilişki türlerinde YÜKSEK/ORTA olup |t|<3 olanlar
Y=X[X.relation.isin(tradable)&(X.t_eff.abs()<3)]
print('\nİşlenebilir türde YÜKSEK/ORTA ama |t|<3:',len(Y)); print(Y[['agent','st','dr','relation','lag','t_eff','bt_oos_mean_bps','confidence']].head(30).to_string())
Z=X[X.relation.isin(tradable)&(X.t_eff.abs()>=5.47)]
print('\nİşlenebilir türde küresel Bonferroni geçen YÜKSEK/ORTA:',len(Z)); print(Z[['agent','st','dr','relation','lag','t_eff','corr_full','bt_oos_mean_bps','confidence']].sort_values('t_eff').to_string())
