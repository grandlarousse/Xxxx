# T23a: ll.backtest mantığının bağımsız yeniden uygulaması ile birim testleri (ll import edilmez; satır 200-207 aynen yeniden yazıldı)
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji'); sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
import vm, numpy as np, pandas as pd
from universe import VIOP
rng=np.random.default_rng(0); idx=pd.bdate_range('2010-01-01',periods=4000)
y=pd.Series(rng.normal(0,0.02,4000),index=idx)
def bt(s,y,cost=8,mode='sign',thr=0,zw=250):
    df=pd.concat([s.rename('s'),y.rename('y')],axis=1).dropna()
    if mode=='z':
        mu=df.s.rolling(zw,min_periods=60).mean().shift(1); sd=df.s.rolling(zw,min_periods=60).std().shift(1); z=(df.s-mu)/sd; pos=np.sign(z).where(z.abs()>thr,0.0)
    else: pos=np.sign(df.s).where(df.s.abs()>thr,0.0)
    pos=pos.fillna(0); return pos*df.y-cost/1e4*pos.abs(), pos
# 1) gürültü sinyali: ort pnl ≈ -maliyet
s=pd.Series(rng.normal(size=4000),index=idx); p,pos=bt(s,y,mode='z',thr=1); print(f'1) gürültü z-sinyal: aktif gün ort pnl={1e4*p[pos!=0].mean():+.1f} bps (beklenen ≈ -8)')
# 2) z-modunda look-ahead yok: sinyal = gelecek getiri ile ilişkisiz ama seviyesi zamanla kayan seri
s2=pd.Series(np.cumsum(rng.normal(size=4000)),index=idx); p,pos=bt(s2,y,mode='z',thr=1,cost=0); print(f'2) trend sinyal (bilgisiz): {1e4*p[pos!=0].mean():+.2f} bps (≈0 => z-modu ileriye bakmıyor)')
# 3) Kalıcı pozisyonda maliyet: sinyal hep +1 -> ll her gün 8 bps keser; gerçek maliyet ≈ 0
s3=pd.Series(1.0,index=idx); p,pos=bt(s3,y); print(f'3) sürekli long: ll maliyeti toplam={8*len(pos):.0f} bps; |Δpos| tabanlı gerçek maliyet={4*pos.diff().abs().fillna(1).sum():.0f} bps (yarım gidiş-dönüş x |Δpos|)')
# 4) Çağıran hatası: ABD sürücüsü kaydırılmadan (lag0) verilirse
c=vm.cal(); c=c[c>='2014-01-01']; es=vm.ret('ES=F',c=c); g=vm.decomp('XU030.IS')
for lab,sig in [('doğru (ES_{t-1})',es.shift(1)),('HATALI (ES_t, kaydırılmamış)',es)]:
    p,pos=bt(sig,g['intra'],cost=8); print(f'4) {lab:30s} -> XU030 gün-içi: {1e4*p[pos!=0].mean():+.1f} bps/gün')
# T23b: Açılış fiyatı gürültüsü -> corr(gap,intra) mekanik negatif mi? h1 ile 07:30 ve 08:30 'açılış' alternatifleri
rows=[]
for s in VIOP:
    h=vm.raw(s+'.IS','h1').sort_index()
    b0=h[(h.index.hour==6)&(h.index.minute==30)]; b1=h[(h.index.hour==7)&(h.index.minute==30)]
    p0730=pd.Series(b0['c'].values,index=pd.DatetimeIndex(b0['ldate'].values)); p0830=pd.Series(b1['c'].values,index=pd.DatetimeIndex(b1['ldate'].values))
    d=vm.decomp(s+'.IS',start='2023-12-01'); raw=vm.raw(s+'.IS').copy(); raw.index=pd.DatetimeIndex(raw['ldate'].values); raw=raw[~raw.index.duplicated(keep='last')]
    j=pd.concat([d,raw['o'],raw['c'],p0730.rename('p1'),p0830.rename('p2')],axis=1).dropna()
    j=j[~j.index.duplicated()]
    g730=j['gap']+np.log(j.p1/j.o); i730=np.log(j.c/j.p1)
    sig=j['gap'].abs()>0.01
    rows.append(dict(sym=s,n=len(j),c_gap_intra=j['gap'].corr(j['intra']),c_gap_first30=j['gap'].corr(np.log(j.p1/j.o)),c_gap_after0730=j['gap'].corr(i730),c_gap0730_after0730=g730.corr(i730),
                     fade_E0=1e4*(-np.sign(j.gap)*j.intra)[sig].mean(),fade_E3=1e4*(-np.sign(j.gap)*i730)[sig].mean(),fade_0830=1e4*(-np.sign(j.gap)*np.log(j.c/j.p2))[sig].mean()))
R=pd.DataFrame(rows)
print('\nT23b (2023-12..2026-10, 47 hisse medyanı):'); print(R.drop(columns=['sym']).median().round(3).to_string())
print('corr(gap, ilk30dk) < 0 olan hisse oranı:', round((R.c_gap_first30<0).mean(),2), '| fade bps medyan: açılıştan', round(R.fade_E0.median(),1), ' 07:30 (10:30 TSİ) girişte', round(R.fade_E3.median(),1), ' 08:30 girişte', round(R.fade_0830.median(),1))
