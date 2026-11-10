import io,contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(open('v1.py').read())
rTa=np.abs(F['TR']['r']); 
def sim_shift(kind,k=2):
    sig=(np.abs(z.values)>1)&ok&np.isfinite(z.values); nf=0; rows=[]
    for i in range(N):
        if i<nf or not sig[i]: continue
        e=k
        while e<k+3 and i+e<N and rTa[i+e]>=thr[i+e]: e+=1
        if i+e>=N or F['TR']['front'][i]<0: continue
        sl=lambda f: np.sum(F[f]['R'][i+1:i+e+1,F[f]['front'][i]])
        lt=sl('TR')
        if kind=='A1': leg=lt; cl,ci=8,23
        else: leg=lt-bt[i]*sl('XU'); cl,ci=8+abs(bt[i])*3,23+abs(bt[i])*8
        if not np.isfinite(leg): continue
        br=np.sign(z.values[i])*leg*1e4; rows.append((cal[i],br,br-cl,br-ci)); nf=i+e
    t=pd.DataFrame(rows,columns=['date','brut','low','ind']); print('cikis-kaydirmali',kind,'n',len(t),'brut %.1f low %.1f (t %.2f) ind %.1f (t %.2f)'%(t.brut.mean(),t.low.mean(),tt(t.low),t.ind.mean(),tt(t.ind)))
sim_shift('A1'); sim_shift('A2')
# e: XU030 hedefi, kontrol olarak XU030'un kendi t getirisi
zU=(rU/(sd(rU)*np.sqrt(dd))).values
def reg2(y,e,ctrl,mask):
    m=ok&mask&np.isfinite(y)&np.isfinite(z.values)&np.isfinite(ctrl)&np.isfinite(e)
    X=np.c_[np.ones(m.sum()),z.values[m],ctrl[m],e[m]]; be,t=nw(y[m]*1e4,X); return be[3],t[3]
for pn,pm in per.items(): print('e2 XU030 hedef, kontrol zU',pn,'d %.1f t %.2f'%reg2(fX[3],E['eJ'],zU,pm))
# eJ otokorelasyon ve XU030/TRALT ile ortak: eJ(d*) ile eJ(d*-1) korelasyonu
a=E['eJ'];b_=E['eJ-1'];m=np.isfinite(a)&np.isfinite(b_); print('corr(eJ,eJ-1)=%.3f'%np.corrcoef(a[m],b_[m])[0,1])
m=np.isfinite(a)&np.isfinite(z.values); print('corr(eJ,gz)=%.3f'%np.corrcoef(a[m],z.values[m])[0,1])
# gunluk (g_z,rTz,eJ) -> yarin TRALT 1g: g_z ile birlikte cokluk testi: 2 yan etki - sayi sayisi
print('toplam regresyon sayisi K1: BASE 19 x A1,A3,A2 x k3 + B1 + DISC (Bonferroni 0.05/~200 -> |t|>~3.6)')
