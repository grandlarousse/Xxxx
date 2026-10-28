from datetime import date
t0=date(2026,10,28)
rusd=0.039  # Fed 3.75-4.00 -> ~3.9% (assumption SOFR-ish)
fut={'1026':(date(2026,10,30),49.830),'1126':(date(2026,11,30),51.151),'1226':(date(2026,12,31),52.473),
     '0127':(date(2027,1,29),53.692),'0227':(date(2027,2,26),54.925),'1227':(date(2027,12,31),69.198)}
for S in (49.76,49.84):
    print("Spot",S)
    prev=None
    for k,(d,F) in fut.items():
        n=(d-t0).days
        prem=F/S-1
        simple=prem*365/n
        tl=(F/S*(1+rusd*n/360)-1)*365/n
        cmp_=(F/S)**(365/n)-1
        print(f" {k} n={n:3d} F={F:.3f} prem={prem*100:5.2f}% simpleAnn={simple*100:5.1f}% impliedTL(simple)={tl*100:5.1f}% compAnnPrem={cmp_*100:5.1f}%")
# forward-forward Dec->Feb, Nov->Dec
def ff(a,b):
    (da,Fa),(db,Fb)=fut[a],fut[b]; n=(db-da).days
    p=Fb/Fa-1; return n,p*365/n,((Fb/Fa)*(1+rusd*n/360)-1)*365/n
for a,b in (('1126','1226'),('1226','0127'),('1226','0227'),('0127','0227')):
    n,s,tl=ff(a,b); print(f"fwdfwd {a}->{b}: n={n} premAnn={s*100:.1f}% impliedTL={tl*100:.1f}%")
# realized depreciation paces
pts=[(date(2025,12,31),42.884,'F1225 final settle (Gedik 02.01.26)'),(date(2026,7,30),47.411,'F0726 settle 1d left (Gedik 31.07)'),
     (date(2026,10,9),49.2160,'TCMB satis 09.10'),(date(2026,10,14),49.3939,'serbest 14.10'),(date(2026,10,21),49.6030,'21.10'),(date(2026,10,27),49.7892,'TCMB satis 27.10')]
for i in range(len(pts)-1):
    for j in (i+1,len(pts)-1):
        if j<=i: continue
        (d1,s1,_),(d2,s2,_)=pts[i],pts[j]; n=(d2-d1).days
        print(f"{d1}->{d2} n={n} chg={(s2/s1-1)*100:.2f}% ann_simple={(s2/s1-1)*365/n*100:.1f}%")
# Forward premium at start 2026 for Jan contract
print("Jan26 contract on 31.12.25: prem ann", (43.994/42.884-1)*365/30*100)
print("Jul26 fwd(19.06, 42d) vs settle:", 47.972, 47.411, (47.972-47.411)/47.972*100)
print("Aug26 fwd 30.07 48.65 (32d)")
# Dec trade scenarios
F=52.473; S=49.76; n=64
for pace in (0.15,0.20,0.236,0.30,0.35):
    ST=S*(1+pace*n/365)
    print(f"pace {pace*100:.0f}% -> S_T={ST:.3f} PnL/contract={(F-ST)*1000:,.0f} TL ({(F-ST)/F*100:.2f}% of notional)")
print("breakeven pace", (F/S-1)*365/n*100)
m=0.11*F*1000; print("Takasbank margin per contract (PSR 11%):",round(m))
