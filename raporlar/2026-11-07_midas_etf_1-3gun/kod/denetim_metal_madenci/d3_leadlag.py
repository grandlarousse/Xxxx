"""D3: Gecikmeli öncü iddialarının yeniden hesabı (kendi regresyonum, Newey-West).
 r_T(t+1..t+h) = a + b*r_L(t) + c*r_T(t) (+ d*r_T(t-1)) ; IS/OOS ayrımı; bp/sd; gece/gün içi ayrışımı
 (bayat fiyat testi: etki yalnız ertesi açılışta mı?); hacim kademesine göre ayrışım.
Çalıştır: python3 -I kod/denetim_metal_madenci/d3_leadlag.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import motor as M, lib

def rets(sym, drop=()):
    d = M.px(sym, drop); c = d["c"]
    return pd.DataFrame({"r": np.log(c).diff(), "on": np.log(d["o"] / c.shift(1)), "id": np.log(c / d["o"]), "dv": d["dv"]})

def leader_series(name):
    if name in ("T10YIE", "DFII10", "DGS10"):
        s = lib.fred(name); s.index = pd.to_datetime(s.index); return s.diff() / 100.0   # yüzde puan -> oran (bp/1e4)
    return rets(name)["r"]

def reg(T, Lname, h=1, part=None, drop=(), target_field="r"):
    t = rets(T, drop); l = leader_series(Lname).reindex(t.index)
    fw = sum(t["r"].shift(-k) for k in range(1, h + 1)) if target_field == "r" else t[target_field].shift(-1)
    df = pd.DataFrame({"y": fw, "x": l, "own": t["r"], "own1": t["r"].shift(1)}).dropna()
    if part == "is": df = df[df.index <= M.IS_END]
    if part == "oos": df = df[df.index > M.IS_END]
    X = np.column_stack([np.ones(len(df)), df["x"], df["own"], df["own1"]])
    b, tt, n = M.nw_t_reg(df["y"].values, X, max(h, 5))
    return b[1], tt[1], n, b[1] * df["x"].std() * 1e4

def catch(T, Lname, h=1, part=None):
    """Yetişme: res(t) = beta60*r_L(t) - r_T(t), kendi getirisi ayrıca kontrol edildiğinde L'nin katkısı."""
    t = rets(T); l = leader_series(Lname).reindex(t.index)
    beta = (t["r"].rolling(60).cov(l) / l.rolling(60).var()).shift(1)
    res = beta * l - t["r"]
    fw = sum(t["r"].shift(-k) for k in range(1, h + 1))
    df = pd.DataFrame({"y": fw, "res": res, "own": t["r"], "x": l}).dropna()
    if part == "is": df = df[df.index <= M.IS_END]
    if part == "oos": df = df[df.index > M.IS_END]
    X1 = np.column_stack([np.ones(len(df)), df["res"]])
    b1, t1, _ = M.nw_t_reg(df["y"].values, X1, max(h, 5))
    X2 = np.column_stack([np.ones(len(df)), df["x"], df["own"]])
    b2, t2, _ = M.nw_t_reg(df["y"].values, X2, max(h, 5))
    return t1[1], t2[1], t2[2]

def main():
    rows = []
    pairs = [("DBB", "KWEB", 1), ("DBB", "FXI", 1), ("CPER", "KWEB", 1), ("COPX", "KWEB", 1), ("GLD", "GDX", 1), ("SLV", "T10YIE", 1),
             ("GLD", "T10YIE", 1), ("PPLT", "GDX", 1), ("COPX", "GDX", 3), ("GDX", "LQD", 1), ("GDXJ", "LQD", 1), ("URA", "SPY", 1), ("XME", "DIA", 1)]
    print("hedef<-öncü h | tüm: b t n bp/sd | IS t | OOS t | gece t | gün içi t")
    for T, Lm, h in pairs:
        b, t, n, bp = reg(T, Lm, h)
        _, ti, _, _ = reg(T, Lm, h, "is"); _, to, _, _ = reg(T, Lm, h, "oos")
        _, ton, _, bpo = reg(T, Lm, 1, target_field="on"); _, tid, _, bpi = reg(T, Lm, 1, target_field="id")
        cst = M.cost_static(M.px(T))
        print(f"{T}<-{Lm} h{h}: b={b:.3f} t={t:.2f} n={n} {bp:.1f} bp/sd (maliyet {cst:.0f}) | IS {ti:.2f} | OOS {to:.2f} | gece {ton:.2f} ({bpo:.1f}bp) | gün içi {tid:.2f} ({bpi:.1f}bp)")
        rows.append(dict(hedef=T, oncu=Lm, h=h, b=b, t=t, n=n, bp_per_sd=bp, is_t=ti, oos_t=to, gece_t=ton, gece_bp_sd=bpo, gunici_t=tid, gunici_bp_sd=bpi, maliyet_bp=cst))
    # DBB bayat fiyat: hacmi düşük günlerde etki büyür mü?
    t = rets("DBB"); l = rets("KWEB")["r"].reindex(t.index)
    lowv = t["dv"] < t["dv"].rolling(60).median().shift(1)
    for nm, m in (("DBB düşük hacimli gün", lowv), ("DBB yüksek hacimli gün", ~lowv)):
        df = pd.DataFrame({"y": t["r"].shift(-1), "x": l, "own": t["r"]})[m].dropna()
        b, tt, n = M.nw_t_reg(df["y"].values, np.column_stack([np.ones(len(df)), df["x"], df["own"]]), 5)
        print(f"  {nm}: b={b[1]:.3f} t={tt[1]:.2f} n={n}")
        rows.append(dict(hedef="DBB", oncu="KWEB", h=1, b=b[1], t=tt[1], n=n, not_=nm))
    zero = (M.px("DBB")["v"] == 0).sum(); print(f"  DBB sıfır hacimli gün: {zero}; medyan $ hacim son 1y {M.px('DBB')['dv'].tail(252).median()/1e6:.1f} mn")
    # Yetişme: madenci <- metal ; kendi getirisi kontrollü
    print("\nYetişme (res=beta60*r_L - r_T): kontrolsüz res t | L katsayısı (kendi getirisi kontrollü) t | kendi getirisi t")
    for T, Lm in (("GDX", "GLD"), ("GDXJ", "GLD"), ("SIL", "SLV"), ("SILJ", "SLV"), ("COPX", "CPER"), ("IAU", "GLD")):
        for h in (1, 3):
            a, b2, c2 = catch(T, Lm, h)
            ai, bi, _ = catch(T, Lm, h, "is"); ao, bo, _ = catch(T, Lm, h, "oos")
            print(f"  {T}<-{Lm} h{h}: res t={a:.2f} | L t={b2:.2f} (IS {bi:.2f} / OOS {bo:.2f}) | own t={c2:.2f}")
            rows.append(dict(hedef=T, oncu=Lm, h=h, tip="yetisme", res_t=a, L_t=b2, L_t_is=bi, L_t_oos=bo, own_t=c2))
    # IAU hatalı bar kontrolü
    iau = M.px("IAU"); gld = M.px("GLD")
    w = slice("2021-03-03", "2021-03-11")
    print("\nIAU/GLD 2021-03 kontrol:\n", pd.DataFrame({"IAU_c": iau["raw_c"].loc[w], "IAU_r%": iau["c"].pct_change().loc[w] * 100,
                                                       "GLD_r%": gld["c"].pct_change().loc[w] * 100}).round(2).to_string())
    a, b2, c2 = catch("IAU", "GLD", 1)
    pd.DataFrame(rows).to_csv(os.path.join(M.OUTD, "d3_leadlag.csv"), index=False)

if __name__ == "__main__":
    main()
