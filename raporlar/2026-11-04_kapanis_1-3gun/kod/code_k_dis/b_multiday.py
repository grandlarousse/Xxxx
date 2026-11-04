"""(b) Çok günlük (k=2,3,5) kümülatif sürücü getirisi -> 47 hisse + F_XU030 uzlaşma t -> t+h (h=1,2,3,5).
Bilgi anı (t kapanışında bilinen):
  gecikmeli (L): ES=F, EEM, BZ=F, GC=F, TUR günlük kapanış t-1 ve öncesi (t günü kapanışı BIST'ten sonra) -> toplam r_{t-k..t-1}
  hizalı (A): VİOP USDTRY uzlaşması, VİOP XAUUSD uzlaşması, DİBS 2y/10y getiri değişimi (BAP kesin alım-satım, ~17:30 TSİ kapanış) -> toplam r_{t-k+1..t}
  saatlik (H): ES, EEM, BZ, GC, TUR, USDTRY 15:00 UTC anlık -> toplam (t-k 15:00, t 15:00]
Biçimler: raw = kümülatif sürücü (geçmiş std ile ölçekli); div = beta x kümülatif sürücü - hisse kümülatif getirisi (hisse geride kaldı mı?)
Mod F: VİOP vadeli 2017+ (IS 2017-21 / OOS 2022-26). Mod S: spot 2014+ (IS 2014-20 / OOS 2021-26). Mod H: saatlik 2023-12/2024-06+ (yarılar).
"""
import sys, numpy as np, pandas as pd
import klib as K, ll

HS = [1, 2, 3, 5]; KS = [2, 3, 5]

def drivers(mode):
    F = K.fut_panel()
    M = pd.read_parquet(K.S + "/out/code_y_makro_y/res/macro_daily.parquet")
    D = {}
    if mode in ("F", "S"):
        for nm, sym in [("ES", "ES=F"), ("EEM", "EEM"), ("BRENT", "BZ=F"), ("GOLD", "GC=F"), ("TUR", "TUR")]:
            D[nm] = (ll.ret(sym), "L")
        D["DIBS2"] = (M["d_dibs2"] / 100.0, "A"); D["DIBS10"] = (M["d_dibs10"] / 100.0, "A")
        if mode == "F":
            D["V_USD"] = (F["USDTRY"], "A"); D["V_XAU"] = (F["XAUUSD"], "A")
    else:
        for nm, sym in [("ES", "ES=F"), ("EEM", "EEM"), ("BRENT", "BZ=F"), ("GOLD", "GC=F"), ("TUR", "TUR"), ("USD", "TRY=X")]:
            D[nm] = (K.r_snap(sym), "A")
    return D

def run(mode):
    F = K.fut_panel(); Sp = K.spot_panel()
    if mode in ("F", "H"):
        R = F[K.STOCKS + ["XU030"]]; start = "2017-03-06" if mode == "F" else "2023-12-05"; split = "2022-01-01" if mode == "F" else "2025-05-01"
    else:
        R = Sp[K.STOCKS + ["XU030"]]; start = "2014-01-01"; split = "2021-01-01"
    w = 250 if mode != "H" else 120; mp = 60 if mode != "H" else 40
    names = list(R.columns)
    Y = {h: K.fwd(R, h) for h in HS}
    rows = []
    for dn, (x, kind) in drivers(mode).items():
        x = x.reindex(R.index)
        if mode == "H": x = x.where(x.index >= "2023-12-05")
        for k in KS:
            lag = 1 if kind == "L" else 0
            ck = K.cum(x, k, lag)
            xz = K.sdscale(ck, w, mp)
            # div: transmisyon betası (hisse r_t ~ sürücü r_{t-lag}), hisse kümülatif (t-k, t]
            xl = x.shift(lag)
            bt = K.roll_beta(R, xl, w, mp)
            sc = K.cum(R, k, 0)
            div = K.sdscale(bt.mul(ck, axis=0) - sc, w, mp)
            for form in ("raw", "div"):
                for s in names:
                    z = xz if form == "raw" else div[s]
                    for h in HS:
                        y = Y[h][s]; y = y[y.index >= start]
                        r = K.reg(y, z, h + 1)
                        ri = K.reg(y[y.index < split], z, h + 1, 40); ro = K.reg(y[y.index >= split], z, h + 1, 40)
                        ev = (np.sign(z) * y).where(z.abs() > 1).dropna()
                        m_, t_, n_ = K.mean_nw(ev, h)
                        evi = ev[ev.index < split]; evo = ev[ev.index >= split]
                        rows.append(dict(mode=mode, driver=dn, kind=kind, k=k, form=form, stock=s, h=h, n=r["n"], b=r["b"] * 1e4, t=r["t"],
                                         t_IS=ri["t"], t_OOS=ro["t"], ev_n=n_, ev_bps=m_ * 1e4, ev_t=t_,
                                         ev_IS=evi.mean() * 1e4 if len(evi) > 10 else np.nan, ev_OOS=evo.mean() * 1e4 if len(evo) > 10 else np.nan))
            print(mode, dn, k, "bitti", flush=True)
    out = pd.DataFrame(rows); out.to_csv(K.RES + f"/b_multiday_{mode}.csv", index=False)
    return out

if __name__ == "__main__":
    for m in sys.argv[1:]: run(m)
