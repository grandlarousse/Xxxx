"""s10: C2 ayrıştırması — madenci artık momentumu GDX'in İLERİ artığını mı (sektöre özgü momentum) yoksa yalnız altın kanalını mı (C1) öngörüyor?
İleri artık: fwd_h(r_GDX) - b_g,t * fwd_h(r_GLD) - b_s,t * fwd_h(r_SPY) (betalar gün t'de bilinen, 250 gün geçmiş).
"""
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SPY"]}
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl")
rows = []
for und in ("GDX", "GDXJ"):
    X = pd.concat([R["GLD"], R["SPY"]], axis=1).set_axis(["GLD", "SPY"], axis=1)
    B = roll_beta2(R[und], X, 250, 120)   # gün t dahil (t kapanışında bilinir; ileri pencere t+1..t+h)
    for k in (1, 3):
        x = SIG1[(f"{und}~GLD+SPY", k)]
        for h in (1, 3, 5):
            fres = fwd(R[und], h) - B["GLD"] * fwd(R["GLD"], h) - B["SPY"] * fwd(R["SPY"], h)
            # split_stats hedefi doğrudan alır: fwd() uygulanmış seriyi vermek için test()'i atla
            st = split_stats(x, fres, h); s22 = sub_ic(x, fres, h, start="2022-01-01")
            st["t_22"] = s22["t"]
            register(AGENT, "a_madenci_artik", f"a6_{und}resid_k{k}_ileri_artik_h{h}", f"{und} artık k={k} -> {und} ileri artığı", h, st, note="C2 ayrıştırma")
            gl = split_stats(x, fwd(R["GLD"], h), h)
            rows.append(dict(und=und, k=k, h=h, ic_ileri_artik=round(st["ic"], 3), t=round(st["t"], 2), t_is=round(st["t_is"], 2), t_oos=round(st["t_oos"], 2), t_22=round(st["t_22"], 2),
                             yrs=f"{st['yrs_same_sign']}/{st['yrs']}", ic_GLD=round(gl["ic"], 3), t_GLD=round(gl["t"], 2)))
o = pd.DataFrame(rows); o.to_csv(f"{OUT}/s10_ayristirma.csv", index=False); print(o.to_string())
