"""Denetim: ajanın 'doğrulanmış gecikmeli öncü' iddiaları (QQQ/SPY -> IGV negatif, EEM/FXI -> KWEB negatif) ve
'öncü değil' iddiaları (NVDA/TSM/AVGO/EWT/EWY -> SMH; QQQ -> SMH; XME -> COPX) bağımsız yeniden hesaplama.
Model: r_T(t+1) = a + b*r_L(t) + c*r_T(t) (+ isteğe bağlı r_L(t+1) eşzamanlı kontrol), Newey-West(5).
python3 -I kod/denetim_sektor_tematik/d4_leadlag.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_ortak import *

pd.set_option("display.width", 250)


def series(sym):
    p = os.path.join(lib.DATA, "etf", sym + ".parquet")
    if os.path.exists(p):
        return np.log(D(sym)["c"]).diff()
    df = pd.read_parquet(os.path.join(lib.DATA, "stock", sym + ".parquet"))
    return np.log(df["c"][df["c"] > 0]).diff()


def lagreg(T, L, h=1, extra_ctrl=None, sub=None, contemp=False, drop_big=None):
    rt = series(T); rl = series(L).reindex(rt.index)
    fwd = sum(rt.shift(-k) for k in range(1, h + 1))
    X = pd.DataFrame({"c": 1.0, "L": rl, "own": rt})
    if contemp: X["L_t1"] = rl.shift(-1)  # yalnız teşhis: hedefin göreli (idiyosenkratik) kısmı
    if extra_ctrl:
        for e in extra_ctrl:
            X[e] = series(e).reindex(rt.index)
    df = pd.concat([fwd.rename("y"), X], axis=1).dropna()
    if sub == "is": df = df[df.index <= IS_END]
    elif sub == "oos": df = df[df.index > IS_END]
    if drop_big is not None:
        df = df[(df["L"].abs() < drop_big) & (df["own"].abs() < drop_big) & (df["y"].abs() < drop_big * h)]
    b, t, n = nw_t(df["y"].values, df.drop(columns="y").values, lags=max(5, h + 2))
    sdL = df["L"].std()
    return {"b": b[1], "t": t[1], "own_t": t[2], "n": n, "bp_per_sd": b[1] * sdL * 1e4}


pairs = [("IGV", "QQQ"), ("IGV", "SPY"), ("KWEB", "EEM"), ("KWEB", "FXI"), ("SMH", "QQQ"), ("SOXX", "QQQ"), ("XBI", "SPY"),
         ("COPX", "XME"), ("SMH", "NVDA"), ("SMH", "TSM"), ("SMH", "AVGO"), ("SMH", "EWT"), ("SMH", "EWY"), ("XLK", "AAPL")]
rows = []
for T, L in pairs:
    for h in (1, 3):
        a = lagreg(T, L, h); i = lagreg(T, L, h, sub="is"); o = lagreg(T, L, h, sub="oos")
        c = lagreg(T, L, h, contemp=True) if h == 1 else {"t": np.nan, "bp_per_sd": np.nan}
        s = lagreg(T, L, h, extra_ctrl=["SPY"] if L != "SPY" else ["QQQ"])
        bg = lagreg(T, L, h, drop_big=0.06)
        rows.append({"hedef": T, "oncu": L, "h": h, "n": a["n"], "t": a["t"], "bp_per_sd": a["bp_per_sd"], "own_t": a["own_t"],
                     "is_t": i["t"], "oos_t": o["t"], "is_bp_sd": i["bp_per_sd"], "oos_bp_sd": o["bp_per_sd"],
                     "t_eszamanli_kontrol": c["t"], "bp_sd_eszamanli_kontrol": c["bp_per_sd"], "t_spy_kontrol": s["t"],
                     "t_buyuk_gun_haric": bg["t"], "p": p_from_t(a["t"], a["n"])})
R = pd.DataFrame(rows)
R["fdr10_bu_tablo"] = bh(R["p"].values, 0.10)
print(R.round(2).to_string())
R.to_csv(os.path.join(OUT, "d4_leadlag.csv"), index=False)

# Kendi gecikmesi & piyasa geneli dönüş: QQQ kendi ertesi günü?
for s in ("QQQ", "SPY", "EEM", "FXI"):
    r = series(s); df = pd.concat([r.shift(-1).rename("y"), r.rename("x")], axis=1).dropna()
    b, t, n = nw_t(df.y.values, np.c_[np.ones(len(df)), df.x.values])
    print(f"{s} kendi gecikmesi: b={b[1]:.3f} t={t[1]:.2f}")

# İşlem kuralları (long-only 'alma' filtresi bağlamında): oncu z>+1 ertesi gün hedef C0 h1 brüt; yıl yıl
def zr(sym):
    r = series(sym); return r / r.rolling(60).std()


out = {}
for T, L in (("IGV", "QQQ"), ("KWEB", "EEM")):
    df = D(T); z = zr(L).reindex(df.index)
    for nm, sg in (("z>+1", z > 1), ("z<-1", z < -1), ("tum", z.notna())):
        tr = sim(df, sg, 1, "C0", cost(T)); s_ = st(tr)
        yy = tr.groupby(tr.sig_date.dt.year)["gross"].mean() * 1e4
        print(f"{L} {nm} -> {T} C0 h1: n={s_['n']} brut={s_['brut_bp']:.1f} net={s_['net_bp']:.1f} t={s_['t']:.2f} IS={s_['is_net_bp']:.1f} OOS={s_['oos_net_bp']:.1f}"
              f" | yıllar brüt<0 oranı {(yy<0).mean():.2f}")
        out[f"{L}{nm}->{T}"] = {k: s_.get(k) for k in ("n", "brut_bp", "net_bp", "t", "is_net_bp", "oos_net_bp")}
        if nm == "z>+1":
            print("   yıl yıl brüt:", yy.round(0).to_dict())
json.dump(out, open(os.path.join(OUT, "d4_kurallar.json"), "w"), ensure_ascii=False, indent=1, default=float)
