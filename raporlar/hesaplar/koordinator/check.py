from math import log, sqrt, exp
from statistics import NormalDist
N = NormalDist().cdf
def b76(F,K,T,r,s,cp):
    d1=(log(F/K)+0.5*s*s*T)/(s*sqrt(T)); d2=d1-s*sqrt(T); D=exp(-r*T)
    return D*(F*N(d1)-K*N(d2)) if cp=='c' else D*(K*N(-d2)-F*N(-d1))
F=14644; T=64/365; r=0.36
print("== Koordinator bagimsiz kontrol ==")
for s in (0.17,0.24,0.27,0.32):
    st=b76(F,14500,T,r,s,'c')+b76(F,14500,T,r,s,'p')
    ps=b76(F,14000,T,r,s,'p')-b76(F,13000,T,r,s,'p')
    cs=b76(F,14500,T,r,s,'c')-b76(F,15500,T,r,s,'c')
    # risk-neutral probabilities (lognormal around F)
    def p_below(K): return N((log(K/F)+0.5*s*s*T)/(s*sqrt(T)))
    print(f"sigma={s:.2f}: straddle14500={st:6.0f}  putspread14000/13000={ps:5.0f}  callspread14500/15500={cs:5.0f}  "
          f"P(S<13000)={p_below(13000):.2f} P(S<13800)={p_below(13800):.2f} P(S>14840)={1-p_below(14840):.2f}")
# Put spread EV under SEYTAN subjective vs RN
print("\nPut spread @200: payoff at expiry (puan) vs S_T")
for ST in (12500,13000,13500,13800,14000,14644):
    pay=max(0,14000-ST)-max(0,13000-ST)
    print(f"  S_T={ST}: net={pay-200:+}")
# USDTRY carry EV sensitivity (per contract, TL), MAKRO R2 numbers
print("\nUSDTRY short EV/kontrat (TL) vs kuyruk olasiligi (kuyruk kaybi 6300 TL, stopsuz erken sok)")
base_gain=793; mid=95
for pt in (0.0,0.02,0.03,0.04,0.05,0.08):
    # renormalize: 70/20 split of remainder kept proportional
    rest=1-pt; ev=rest*(0.7/0.9*base_gain+0.2/0.9*mid)+pt*(-6300)
    print(f"  p_tail={pt:.2f}: EV={ev:+.0f} TL  (maliyet ~36 TL haric)")
