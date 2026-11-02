# T10: Ajanlar arası tutarsızlık: aynı (hisse, sürücü, ilişki, lag) için farklı sayılar/etiketler
import pandas as pd, numpy as np, glob, os, re
O='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out'
fs=sorted(glob.glob(f'{O}/f_*.csv')); L=[]
for f in fs:
    try: d=pd.read_csv(f,low_memory=False)
    except Exception as e: print('okunamadı',f,e); continue
    d['agent']=os.path.basename(f)[2:-4]; L.append(d)
D=pd.concat(L,ignore_index=True)
print('toplam satır',len(D),' ajan',D.agent.nunique()); print(D.agent.value_counts().to_dict())
def norm_stock(s):
    s=str(s).upper().replace('BIST:','').replace('.IS','').strip(); return s
def norm_drv(s):
    s=str(s).strip(); return s.upper().replace('BIST:','').replace('.IS','') if (s.upper().endswith('.IS') or s.upper().startswith('BIST:')) else s
D['st']=D['stock'].map(norm_stock); D['dr']=D['driver_yahoo'].map(norm_drv)
D['lagn']=pd.to_numeric(D['lag'],errors='coerce')
for c in ['corr_full','pcorr_xu100','beta','t_stat','gap_corr','intra_corr','corr_3y','corr_1y']: D[c]=pd.to_numeric(D[c],errors='coerce')
D['conf']=D['confidence'].astype(str).str.upper().str.replace('Ü','U').str.replace('Ş','S').str.replace('İ','I').str.replace('Ç','C').str.strip()
D.astype(str).to_parquet(f'{O}/code_v_metodoloji/all_findings.parquet')
# sync korelasyon tutarsızlığı
S=D[(D.relation=='sync')&D.corr_full.notna()]
g=S.groupby(['st','dr'])
agg=g.agg(n_agent=('agent','nunique'),cmin=('corr_full','min'),cmax=('corr_full','max'),pcmin=('pcorr_xu100','min'),pcmax=('pcorr_xu100','max'),agents=('agent',lambda x:','.join(sorted(set(x)))),confs=('conf',lambda x:','.join(sorted(set(x)))))
m=agg[agg.n_agent>=2].copy(); m['crange']=m.cmax-m.cmin; m['pcrange']=m.pcmax-m.pcmin
print('\nSENKRON: >=2 ajanın raporladığı çift:',len(m),' |corr farkı|>0,05:',int((m.crange>0.05).sum()),' >0,10:',int((m.crange>0.10).sum()),' pc farkı>0,05:',int((m.pcrange>0.05).sum()))
print(m.sort_values('crange',ascending=False).head(25).to_string())
# etiket tutarsızlığı
print('\nAynı çift farklı güven etiketi (sync):', int(m.confs.str.contains(',').sum()))
X=m[m.confs.str.contains('YUKSEK')&(m.confs.str.contains('DUSUK')|m.confs.str.contains('COK'))]
print('YÜKSEK ve DÜŞÜK/ÇOK DÜŞÜK aynı anda:',len(X)); print(X.head(25)[['agents','confs','cmin','cmax','pcmin','pcmax']].to_string())
