"""Roll, temettü ve ince-işlem günleri kontrolü (ana varyantlar)."""
import numpy as np, pandas as pd, cl, ev, c1sig
def exdiv(sym):
    d = cl.dly(sym); j = np.log(d["adj"] / d["c"]).diff(); return set(j[j.abs() > 0.004].index)
u = ev.R("USDTRY"); g = ev.R("XAUUSD")
C = [("REF->TUPRS", c1sig.z_ref(), "TUPRS", 2, "raw", "2017-03-06"), ("ASX->EREGL", c1sig.z_asx(), "EREGL", 3, "hedged", "2017-03-06"),
     ("GOLD->TRALT", cl.zscale(g, 250, 100), "TRALT", 2, "hedged", "2018-12-17"), ("USD5->THYAO", cl.zscale(sum(u.shift(i) for i in range(5)), 250, 100), "THYAO", 3, "raw", "2017-03-06")]
c = cl.cal(); rows = []
for lab, z, und, h, lg, st in C:
    Y = ev.ydict(und, st); f = cl.front(und); tr = cl.trades(z, Y[(h, lg)], h, 1.0, f["roll"])
    extra = 3 if lg == "hedged" else 0; net = tr["gross"] * 1e4 - 8 - extra
    ed = exdiv(und + ".IS"); pos = pd.Series(np.arange(len(c)), index=c)
    span_div = []; thin = []
    trd = f["trades"].reindex(c)
    for t in tr.index:
        i = pos[t]; win = c[i + 1:i + h + 1]; span_div.append(any(w in ed for w in win))
        thin.append(min(trd.iloc[i], trd.iloc[min(i + h, len(c) - 1)]) < 20)
    span_div = np.array(span_div); thin = np.array(thin); roll = tr["rolls"].values > 0
    # Uzlaşma yerine 'close' (son işlem) ile giriş/çıkış: dolum varsayımına duyarlılık
    rows.append(dict(cand=lab, n=len(tr), net=round(net.mean(), 1), t=round(cl.tstat(net), 2),
                     roll_n=int(roll.sum()), roll_net=round(net[roll].mean(), 1), noroll_net=round(net[~roll].mean(), 1),
                     div_n=int(span_div.sum()), div_net=round(net[span_div].mean(), 1) if span_div.any() else np.nan, nodiv_net=round(net[~span_div].mean(), 1),
                     thin_n=int(thin.sum()), thin_net=round(net[thin].mean(), 1) if thin.any() else np.nan, liquid_net=round(net[~thin].mean(), 1), liquid_t=round(cl.tstat(net[~thin]), 2),
                     since2020_net=round(net[net.index >= "2020-01-01"].mean(), 1), since2020_t=round(cl.tstat(net[net.index >= "2020-01-01"]), 2)))
D = pd.DataFrame(rows); pd.set_option("display.width", 250); print(D.to_string()); D.to_csv(cl.OUT + "/c7_rolldiv.csv", index=False)
# roll kuralına duyarlılık: tarayıcının kuralına yakın (>=2) ve daha erken roll (>=5)
for lab, z, und, h, lg, st in C:
    for mt in (2, 5):
        cl._FR.clear(); r = cl.fut_ret(und, und + ".IS", min_td=mt); m = cl.fut_ret("XU030", None, min_td=mt)
        y = cl.fwd(r - cl.roll_beta(r, m, 250, 100) * m if lg == "hedged" else r, h); y = y[y.index >= st]
        tr = cl.trades(z, y, h, 1.0); s = cl.summ(tr, 8 + (3 if lg == "hedged" else 0))
        print(lab, "min_td", mt, "n", s["n"], "net", round(s["net"], 1), "t", round(s["t"], 2))
    cl._FR.clear()
