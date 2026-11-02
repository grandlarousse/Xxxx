# T22: 'lag0 -> BIST gün-içi' testlerinde sürücü kapanışı BIST açılış müzayedesinden (06:55 UTC) SONRA mı? Kapanış saatini h1 son bar sonundan ölç; yoksa tz'den tahmin.
import warnings; warnings.filterwarnings("ignore")
import pandas as pd, numpy as np, os
S='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
cat=pd.read_csv(f'{S}/data/catalog.csv').set_index('sym')
D=pd.read_parquet(f'{S}/out/code_v_metodoloji/all_findings.parquet')
D['t']=pd.to_numeric(D.t_stat.replace('nan',np.nan),errors='coerce')
L=D[(D.relation.isin(['lead_intra','intraday_minutes']))&(D.lag.astype(str).str.strip().isin(['0','0.0']))].copy()
print('lag0 -> gün-içi satırı:',len(L))
# kapanış saati ölçümü
close={}
for s in L.dr.unique():
    sy=s
    p=f'{S}/data/h1/{sy}.parquet'
    if os.path.exists(p):
        h=pd.read_parquet(p); e=(h.index+pd.Timedelta(hours=1)); last=pd.Series(e,index=h.index).groupby(h.index.normalize()).max()
        close[s]=float(np.median(last.dt.hour+last.dt.minute/60))
tzc={'Asia/Tokyo':6.0,'Asia/Seoul':6.5,'Asia/Taipei':5.5,'Asia/Shanghai':7.0,'Asia/Hong_Kong':8.1,'Asia/Singapore':9.0,'Asia/Kolkata':10.0,'Asia/Jakarta':9.0,'Asia/Bangkok':9.5,'Asia/Kuala_Lumpur':9.0,'Australia/Sydney':5.2,'Asia/Riyadh':12.0,'Asia/Dubai':10.0,'Asia/Qatar':10.2,'Africa/Cairo':12.5,'Asia/Jerusalem':14.4,'Europe/Moscow':15.8,'Pacific/Auckland':4.0,'Asia/Manila':7.0,'Asia/Karachi':10.5,'Asia/Ho_Chi_Minh':8.0}
def cl(s):
    if s in close: return close[s],'h1'
    tz=cat.tz.get(s,None) if s in cat.index else None
    return (tzc.get(tz,np.nan),f'tz:{tz}')
L[['kapanis_utc','kaynak']]=L.dr.apply(lambda s: pd.Series(cl(s)))
L['lookahead']=L.kapanis_utc>6.92
print('Kapanış saati ölçülebilen satır:',int(L.kapanis_utc.notna().sum()),' BIST açılış müzayedesinden SONRA kapanan sürücü (look-ahead):',int(L.lookahead.sum()))
pd.set_option('display.width',250)
print(L[L.lookahead][['agent','st','dr','kapanis_utc','kaynak','t','bt_oos_mean_bps','confidence']].sort_values('t',key=abs,ascending=False).head(30).to_string())
print(L.groupby(['lookahead','confidence']).size())
