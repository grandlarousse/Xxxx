"""s1 (aile a): madenci–altın ve benzeri çiftlerde göreli artık (yuvarlanan beta, yalnız geçmiş).
Bilgi zamanı: e_t = r_Y,t - beta_{t-1} r_X,t ; r = t-1 16:00 ET -> t 16:00 ET kapanış log getirisi (her iki bacak aynı anda, senkron).
Sinyal gün t'de: E^k_{t-1} = e_{t-1}+...+e_{t-k} (t-1 16:00 ET'de biter; gün t 15:00 ET cutoff'undan ~23 saat önce bilinir) -> x_t = E^k.shift(1).
Hedef: log(c_T,t+h / c_T,t) (gün t 16:00 ET giriş). Beta penceresi 120 gün (önceden sabit), sağlamlık 60/250.
"""
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SLV", "SIL", "SPY"]}
PAIRS = [("GDX", ["GLD"]), ("GDXJ", ["GLD"]), ("GDXJ", ["GDX"]), ("SIL", ["SLV"]), ("SLV", ["GLD"]), ("GDX", ["GLD", "SPY"]), ("GDXJ", ["GLD", "SPY"])]

def resid(y, xs, win=120):
    if len(xs) == 1:
        b = roll_beta(R[y], R[xs[0]], win, 60).shift(1)       # beta_{t-1}: t-1'e kadar olan getirilerle
        e = R[y] - b * R[xs[0]]
    else:
        X = pd.concat([R[x] for x in xs], axis=1); X.columns = xs
        B = roll_beta2(R[y], X, max(win, 250) if win >= 120 else win, 60).shift(1)
        e = R[y] - sum(B[x] * R[x] for x in xs)
    return e

rows = []; SIG = {}
for win in (120,):
    for y, xs in PAIRS:
        e = resid(y, xs, win)
        nm = f"{y}~{'+'.join(xs)}"
        for k in (1, 3, 5, 10):
            E = e.rolling(k, min_periods=k).sum()
            x = E.shift(1)                     # gün t'de bilinen
            SIG[(nm, k)] = x
            tg = [y] + [xs[0]]
            for T in tg:
                for h in HS:
                    st = test("a_madenci_artik", f"a1_{nm}_k{k}_{T}_h{h}", x, R[T], h, f"resid[{nm}] k={k} W={win} -> {T}", note=f"win={win}")
                    rows.append(st)
# Basit gecikmeli çapraz getiriler (altın madencilere mi, madenciler altına mı öncülük ediyor)
for a, b in [("GLD", "GDX"), ("GDX", "GLD"), ("GLD", "GDXJ"), ("GDXJ", "GLD"), ("SLV", "GLD"), ("GLD", "SLV")]:
    for k in (1, 5):
        x = R[a].rolling(k, min_periods=k).sum().shift(1)
        for h in HS:
            st = test("a_madenci_artik", f"a2_lag_{a}_k{k}_{b}_h{h}", x, R[b], h, f"r_{a} k={k} (t-1'de biter) -> {b}")
            rows.append(st)
res = pd.DataFrame(rows)
cols = ["test_id", "h", "ic", "t", "t_is", "t_oos", "ic_oos", "t_22", "yrs_same_sign", "yrs", "n"]
res[cols].to_csv(f"{OUT}/s1_madenci_artik.csv", index=False)
pd.to_pickle(SIG, f"{OUT}/s1_signals.pkl")
pd.set_option("display.width", 250)
print(res[cols].round(3).sort_values("t", key=abs, ascending=False).head(40).to_string())
print("n_tests", len(res))
