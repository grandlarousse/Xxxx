import json,datetime as dt,sys
d=json.load(open(sys.argv[1]))['chart']['result'][0]
ts=d['timestamp']; c=d['indicators']['quote'][0]['close']; h=d['indicators']['quote'][0]['high']
ser=[(dt.datetime.fromtimestamp(t,dt.UTC).date(),x,hh) for t,x,hh in zip(ts,c,h) if x and x>0]
def at(day):
    for D,x,hh in ser:
        if D>=day: return D,x
def window(start,diff,n=64,stop=0.014):
    D0,S0=at(start); F0=S0*(1+diff*n/365); end=D0+dt.timedelta(days=n)
    path=[(D,x,hh) for D,x,hh in ser if D0<D<=end]
    Smax=max(x for _,x,_ in path); Hmax=max((hh or x) for _,x,hh in path)
    ST=path[-1][1]
    # stop check on F_t = S_t*(1+diff*rem/365) > F0*(1+stop) at close
    hit=None
    for D,x,hh in path:
        rem=(end-D).days; Ft=x*(1+diff*rem/365)
        if Ft>F0*(1+stop): hit=(D,x,Ft); break
    pnl_nostop=(F0-ST)/F0
    pnl_stop=(F0-hit[2])/F0 if hit else pnl_nostop
    print(f"{start} S0={S0:.4f} F0={F0:.4f} S64={ST:.4f} spot64={ST/S0-1:+.1%} maxClose={Smax/S0-1:+.1%} maxHigh={Hmax/S0-1:+.1%} | shortF noStop={pnl_nostop:+.1%} withStop={pnl_stop:+.1%} stopday={hit[0] if hit else None}")
eps=[('2018 Ağu',dt.date(2018,7,31),0.18),('2018 Ağu-b',dt.date(2018,8,9),0.18),('2021 Kas-Ara',dt.date(2021,10,18),0.16),('2021 Kas',dt.date(2021,11,17),0.15),
     ('2023 seçim',dt.date(2023,5,26),0.15),('2023 seçim-b',dt.date(2023,6,6),0.15),('2025 Mar',dt.date(2025,3,18),0.38),('2026 Şub savaş',dt.date(2026,2,25),0.31),('2026 May butlan',dt.date(2026,5,15),0.31),('2026 Eyl fon',dt.date(2026,9,14),0.31)]
for name,s,diff in eps:
    print(name,end=': '); window(s,diff)
# distribution of 64-day spot change over whole sample with assumed diffs by year
import statistics
