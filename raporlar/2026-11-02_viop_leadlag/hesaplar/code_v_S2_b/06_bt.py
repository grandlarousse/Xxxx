"""06: Backtest çürütme. |U|>50 (U=D-gap_{t+1}) replikasyonu; U'nun kârının ne kadarının gap-fade (açılış gürültüsü/bid-ask) olduğunu
karıştırılmış-D plasebosu ile ölç; yalnız-D; eşik/varyant seçimi (veri madenciliği); kısa yanlılığı."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
df=pd.read_parquet(RES+'/02_daily.parquet')
T=raw('TCELL.IS'); T=T[T.v>0].reindex(bistcal())
intra_raw=np.log(T.c/T.o); ccr=T.adj/T.adj.shift(1)-1; gapr=np.log(T.o*(T.adj/T.c)/T.adj.shift(1))
ok=((ccr.abs()<=0.105)|ccr.isna())&(((np.exp(gapr)-1).abs()<=0.105)|gapr.isna())
df['intra1_raw']=intra_raw.where(ok).shift(-1); df['gap1_raw']=gapr.where(ok).shift(-1)
q=df.loc['2014':]; q=q[q.D.abs()<0.15].copy()
q['U']=q.D-q.gap1_raw
S={'IS':('2014','2020-12-31'),'OOS':('2021','2026-12-31')}
def rep(sig,y,thr,cost=8):
    o=[]
    for k,(s,e) in S.items():
        r,_=bt(sig,y,thr,cost,s,e); o.append(f"{k}: n {r['n']} {r['mean']:+.1f}bps t {r['t']:+.2f} Sh {r['sh']:+.2f}")
    return ' | '.join(o)
Y=q.intra1_raw
print('== Replikasyon |U|>50, 8 bps:',rep(q.U,Y,0.005))
print('== Benim temizliğimle hedef (|intra|>10,5% NaN):',rep(q.D-q.gap1,q.intra1,0.005))
print('== Varyant ızgarası (OOS/IS, 8 bps) — 1. tur ajanının denediği 5 varyant + fazlası')
for nm,sig in [('D',q.D),('U',q.U),('-gap (saf gap-fade)',-q.gap1_raw)]:
    for thr in [0,0.0025,0.005,0.01]:
        print(f'  {nm:22s} |s|>{thr*1e4:>4.0f}: ',rep(sig,Y,thr))
# Karıştırılmış-D plasebosu: D'yi yıl içinde rastgele permüte et, U_p = D_p - gap1 ; |U_p|>50 -> PnL dağılımı
rng=np.random.default_rng(7); res=[]
yrs=q.index.year
for it in range(500):
    arr=q.D.values.copy()
    for y in np.unique(yrs):
        m=(yrs==y)&q.D.notna().values; arr[m]=rng.permutation(arr[m])
    Dp=pd.Series(arr,index=q.index)
    Up=Dp-q.gap1_raw
    ro,_=bt(Up,Y,0.005,8,'2021','2026-12-31'); ri,_=bt(Up,Y,0.005,8,'2014','2020-12-31')
    res.append((ro['mean'],ro['sh'],ri['mean'],ri['sh']))
R=pd.DataFrame(res,columns=['oos_m','oos_sh','is_m','is_sh'])
ro,_=bt(q.U,Y,0.005,8,'2021','2026-12-31')
print(f"== Karıştırılmış-D plasebosu (500 tekrar, U_p=D_perm-gap): OOS ort {R.oos_m.mean():+.1f} bps (sd {R.oos_m.std():.1f}), Sh {R.oos_sh.mean():+.2f}; IS ort {R.is_m.mean():+.1f}, Sh {R.is_sh.mean():+.2f}")
print(f"   gerçek U OOS {ro['mean']:+.1f} bps Sh {ro['sh']:.2f}; plasebo>gerçek oranı (p) = {(R.oos_m>=ro['mean']).mean():.3f}")
print(f"   => U'nun OOS brüt kârının ({ro['mean']+8:.1f} bps) yaklaşık {100*(R.oos_m.mean()+8)/(ro['mean']+8):.0f}%'i D bilgisi OLMADAN da (gap-fade + kısa yanlılığı) oluşuyor")
# Kısa yanlılığı: sabit kısa TCELL gün-içi
for k,(s,e) in S.items():
    z=Y.loc[s:e].dropna(); print(f'  Sürekli KISA TCELL gün-içi {k}: {-1e4*z.mean()-8:+.1f} bps/gün net (brüt {-1e4*z.mean():+.1f})')
# U işlemlerinin kısa oranı
z=pd.concat([q.U,Y],axis=1).dropna(); z=z[z.U.abs()>0.005]
for k,(s,e) in S.items():
    w=z.loc[s:e]; print(f'  |U|>50 işlemlerde kısa oranı {k}: {(w.U<0).mean():.2f}; uzun ort {1e4*w[w.U>0].intra1_raw.mean():+.1f} kısa ort {-1e4*w[w.U<0].intra1_raw.mean():+.1f} (brüt)')
# Yalnız-D, işaret dengeli: D'yi geçmiş 250g medyanına göre merkezle (önyargısız)
Dc=q.D-q.D.rolling(250,min_periods=60).median().shift(1)
print('== D merkezli (geçmiş medyan) |D|>50:',rep(Dc,Y,0.005))
# Piyasa-nötr hedef (XU030 hedge): TCELL intra - beta*XU030 intra, beta önceki 250g
b=(q.intra1_raw.rolling(250,min_periods=100).cov(q.x30_intra1)/q.x30_intra1.rolling(250,min_periods=100).var()).shift(2)
Yh=q.intra1_raw-b*q.x30_intra1
print('== XU030 hedge (beta önceki 250g, maliyet 8+3=11):')
for nm,sig in [('D',q.D),('U',q.U)]:
    for thr in [0,0.005]: print(f'   {nm} |s|>{thr*1e4:.0f}:',rep(sig,Yh,thr,11))
# En iyi 10 işlemin payı (D |D|>50 ve U |U|>50, OOS)
for nm,sig in [('D',q.D),('U',q.U)]:
    r,p=bt(sig,Y,0.005,8,'2021','2026-12-31'); top=p.sort_values(ascending=False)
    print(f'  {nm} |>50| OOS: toplam {p.sum():.0f} bps, en iyi 10 payı {100*top.iloc[:10].sum()/p.sum():.0f}%, en iyi 10 hariç ort {top.iloc[10:].mean():+.1f}; en iyi 5 tarih {[d.strftime("%Y-%m-%d") for d in top.index[:5]]}')
q.to_parquet(RES+'/06_q.parquet')
