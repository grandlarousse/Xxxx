F=52.473; S=49.76; n=64; cap=1_000_000
m=0.11*F*1000
scen=[(0.70,0.22),(0.20,0.30)]
ev=0
for p,pace in scen:
    ST=S*(1+pace*n/365); pnl=(F-ST)*1000; ev+=p*pnl; print(f"p={p} pace={pace} ST={ST:.2f} pnl={pnl:.0f}")
shock=-1650; ev+=0.10*shock; print("EV/contract",round(ev),"pct notional",ev/(F*1000)*100,"pct margin",ev/m*100)
cost=0.0006*F*1000+5; print("cost",round(cost),"net",round(ev-cost))
for k in (6,10):
    print(k,"contracts: notional",k*F*1000,"lev",k*F*1000/cap,"margin",k*m,"stoprisk",k*830/cap*100,"shock",k*1650/cap*100,"extreme12%", k*(S*1.12+ (F-S)*0.0 - F)*1000/cap*100 ,"EVnet",k*(ev-cost)/cap*100)
# extreme: spot +12% from path at entry ~ S*1.12 =55.73 vs F 52.47
print("extreme loss/contract", (S*1.12-F)*1000)
# BIST30 basis
f10,f12=13982,14644; print("XU030 Dec/Oct implied", (f12/f10-1)*365/62*100)
fair=f10*(1+0.355*62/365); print("fair Dec",round(fair),"discount pts",round(fair-f12),"pct",(fair/f12-1)*100)
print("July: XU030 0826/1026 implied",(16491/15736-1)*365/61*100, " FX Aug implied TL", ((48.65/47.42)*(1+0.039*32/360)-1)*365/32*100)
# XU030 multiplier check
print("XU030 mult", 35449429230/224342/15736, "USDTRY size", 43214904453/911110/47.435)
print("XU030 margin/contract", 0.114*14644*10)
