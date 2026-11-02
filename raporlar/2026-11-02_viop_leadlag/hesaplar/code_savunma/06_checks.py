"""06: Ek kontroller: LISN/LISP sürprizi, TCELL USD bazlı TKC uyumu, FX maruziyeti, VEON/KYIV, kayan korelasyon özeti, ASELS-XBANK faktörü."""
from sv import *
from sv import _corr
dT = ll.decomp("TCELL")
for s in ["LISN.SW", "LISP.SW", "^SSMI", "NESN.SW"]:
    try:
        r, _ = ll.backtest(R(s).shift(1).reindex(dT.index), dT["intra"], cost_bps=8)
        c, t, n = tstat_corr(dT["intra"], R(s).shift(1))
        print(f"{s}(t-1)->TCELL intra corr {c:.3f} t {t:.2f} | BT IS sh {r['IS'].get('sharpe',np.nan):.2f} OOS sh {r['OOS'].get('sharpe',np.nan):.2f} OOS t {r['OOS'].get('t',np.nan):.2f}")
    except Exception as e: print(s, e)
# diğer 46 VİOP hissesi için LISN etkisi (genel BIST etkisi mi?)
cs = []
for st in ["XU100", "AKBNK", "THYAO", "TTKOM", "ASELS", "BIMAS", "KCHOL"]:
    try:
        d = ll.decomp(st); cs.append((st, round(tstat_corr(d["intra"], R("LISN.SW").shift(1))[1], 2)))
    except Exception as e: cs.append((st, str(e)[:30]))
print("LISN.SW(t-1)->intra t (diğer):", cs)
# TCELL USD vs TKC
a = R("TCELL"); fx = R("FXAL"); tk = R("TKC")
print("corr TCELL(TL) vs TKC:", round(_corr(a, tk)[0], 3), " TCELL(USD)=TL-FX vs TKC:", round(_corr(a - fx, tk)[0], 3), " son 3y:", round(_corr(a - fx, tk, "2023-10-30")[0], 3))
# FX maruziyeti: kısmi korelasyon (XU100 kontrollü) ve IS/OOS
for st in ["TCELL", "TTKOM", "ASELS"]:
    s_ = R(st); m = R("XU100")
    out = {lab: round(ll.partial_corr(s_[(s_.index >= s) & (s_.index < e)], fx, [m])[0], 3) for lab, s, e in [("ALL", "2010", "2027"), ("IS", "2014", "2021"), ("OOS", "2021", "2027"), ("2023+", "2023-07", "2027")]}
    yr = s_.groupby(s_.index.year).apply(lambda x: ll.partial_corr(x, fx, [m])[0])
    print(st, "pc(FX|XU100):", out, " yıl işareti negatif oranı:", round((yr[yr.index >= 2010] < 0).mean(), 2))
# kayan 250g kısmi korelasyon ASELS~EU_DEF (rejim)
A = pd.concat([R("ASELS").rename("a"), R("XU100").rename("m"), drv("EU_DEF").rename("e")], axis=1).dropna()
ra = A.a - A.a.rolling(250).cov(A.m) / A.m.rolling(250).var() * A.m; re = A.e - A.e.rolling(250).cov(A.m) / A.m.rolling(250).var() * A.m
rc = ra.rolling(250).corr(re); rc.to_csv(RES + "/06_roll_pc_asels_eudef.csv")
print("ASELS~EU_DEF kayan 250g kısmi korelasyon (yıl sonu):", rc.groupby(rc.index.year).last().round(2).to_dict())
rc2 = A.a.rolling(250).corr(A.e); print("ham kayan (yıl sonu):", rc2.groupby(rc2.index.year).last().round(2).to_dict())
