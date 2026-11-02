# T05: ret() içindeki 12-sigma filtresi (BIST dışı) hangi günleri siliyor? Gerçek şok mu, roll/veri hatası mı?
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji')
import vm, numpy as np, pandas as pd
cat=pd.read_csv('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/catalog.csv')
syms=[s for s in cat.sym if not s.endswith('.IS')]
c=vm.cal()
rows=[]; allrem=[]
x=vm.ret('XU100.IS',c=c)
for s in syms:
    try: r=np.log(vm.on_cal(vm.px(s),c)).diff()
    except Exception: continue
    r=r[r.index>=pd.Timestamp('2005-01-01')]
    sd=r.rolling(250,min_periods=60).std().shift(1); m=(r.abs()>12*sd)&sd.notna()
    if m.sum():
        for t in r[m].index:
            nxt=r.shift(-1).get(t,np.nan)
            allrem.append(dict(sym=s,group=cat.set_index('sym').group.get(s),date=t.date(),r=round(r[t],4),sigma=round(r[t]/sd[t],1),next_r=round(nxt,4) if pd.notna(nxt) else np.nan,xu100_r=round(x.get(t,np.nan),4)))
    rows.append((s,int(m.sum())))
R=pd.DataFrame(allrem)
print('Toplam BIST-dışı sembol',len(rows),' en az 1 gün silinen sembol',(pd.Series(dict(rows))>0).sum(),' toplam silinen gün',len(R))
# geri dönüş (sonraki gün ters işaret ve benzer büyüklük) => veri hatası/roll; yoksa gerçek şok
R['reverts']=(np.sign(R['r'])!=np.sign(R['next_r']))&(R['next_r'].abs()>0.5*R['r'].abs())
print('Ertesi gün >%50 geri dönen (veri hatası/roll olası):',int(R['reverts'].sum()),' dönmeyen (gerçek şok olası):',int((~R['reverts']).sum()))
key=['TRY=X','EURTRY=X','GBPTRY=X','BZ=F','CL=F','NG=F','TTF=F','GC=F','SI=F','HG=F','^VIX','^MOVE','BTC-USD','TUR','TKC','EURCHF=X','CHF=X','RUB=X','ES=F','^GSPC','ZW=F','HRC=F','TIO=F','UX=F','^OVX','USO','EWZ','EEM','AKBTY','TKGBY']
print(R[R.sym.isin(key)].to_string(index=False))
R.to_csv('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji/sigma12_removed.csv',index=False)
print(R.groupby('group').size().sort_values(ascending=False).head(15).to_dict())
