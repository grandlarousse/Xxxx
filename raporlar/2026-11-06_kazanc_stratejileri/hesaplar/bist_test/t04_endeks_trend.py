"""TEST 4 (+6): Endeks trend takibi (XU100, XU030, XBANK, XUTUM). Disaridayken nakit TL rf kazanir.
Kurallar (onceden belirlendi, optimizasyon yok): A) Kapanis>SMA200, B) SMA50>SMA200, C) ay sonu kapanis > 10-aylik SMA,
D/E/F) TSMOM 12/6/3 ay (endeks getirisi > ayni donem rf), ay sonu. Sinyal t kapanisi, islem t+1 kapanisi.
Maliyet: VIOP 12.5 bp gidis-donus (6.25/yon), spot 25 bp (12.5/yon). Varyantlar: 2x VIOP kaldirac, vol-hedefleme (%25, max 2x).
Placebo: ayni 'iceride' surelerinin ve 'disarida' surelerinin karistirilmasiyla rastgele zamanlama (500 cekilis)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
B = base(); cal = B.index
START = pd.Timestamp("2010-01-04")
rng = np.random.default_rng(7)

def monthly_signal(px, fn):
    me = rebal_dates("M", cal, "2009-01-01")
    s = fn(px.reindex(me), me)
    return s.reindex(cal).ffill()   # ay sonu kapanista bilinir, ertesi gun islem (asagida shift)

def signals(px):
    sma50, sma200 = px.rolling(50).mean(), px.rolling(200).mean()
    rfc = (1 + B.rf_d).cumprod()
    out = {"A_P>SMA200": (px > sma200).astype(float).where(sma200.notna()),
           "B_SMA50>200": (sma50 > sma200).astype(float).where(sma200.notna()),
           "C_10ay_SMA": monthly_signal(px, lambda m, d: (m > m.rolling(10).mean()).astype(float).where(m.rolling(10).mean().notna()))}
    for k in (12, 6, 3):
        out[f"TSMOM_{k}ay"] = monthly_signal(px, lambda m, d, k=k: ((m / m.shift(k)) > (rfc.reindex(d) / rfc.reindex(d).shift(k))).astype(float).where(m.shift(k).notna()))
    return out

def run(px, sig, cost_side, lev=1.0, volt=None):
    r = px.pct_change().fillna(0)
    pos = sig.shift(2).fillna(0)            # t kapanisi sinyali -> t+1 kapanisinda islem -> t+2 getirisi
    if volt is not None:
        rv = r.rolling(60).std() * np.sqrt(252)
        w = (volt / rv).clip(upper=2.0).shift(2).fillna(1.0)
        pos = pos * w
    else:
        pos = pos * lev
    trade = pos.diff().abs().fillna(0)     # pozisyon degisimi exec gununden sonraki getiriye uygulanir; maliyeti exec gununde say
    cost = trade.shift(-1).fillna(0) * cost_side
    ret = B.rf_d + pos * (r - B.rf_d) - cost   # kaldiracli VIOP: rf + k*(r - rf)
    return ret, pos

def spells(pos):
    p = (pos > 0).astype(int).values
    ch = np.flatnonzero(np.diff(p)) + 1
    seg = np.split(np.arange(len(p)), ch)
    return [(p[s[0]], len(s)) for s in seg]

def placebo(px, sig, cost_side, n=500):
    r = px.pct_change().fillna(0); pos0 = sig.shift(2).fillna(0)
    m = pos0.index >= START
    sp = spells(pos0[m]); ins = [l for v, l in sp if v == 1]; outs = [l for v, l in sp if v == 0]
    first = sp[0][0]; res = []
    rr = r[m].values; rf = B.rf_d[m].values
    for _ in range(n):
        a = list(rng.permutation(ins)); b = list(rng.permutation(outs)); seq = []; cur = first
        while a or b:
            if cur == 1 and a: seq += [1] * a.pop()
            elif cur == 0 and b: seq += [0] * b.pop()
            elif a: seq += [1] * a.pop()
            else: seq += [0] * b.pop()
            cur = 1 - cur
        p = np.array(seq[:len(rr)], float)
        tr = np.abs(np.diff(np.r_[0, p])); ret = rf + p * (rr - rf) - np.r_[tr[1:], 0] * cost_side
        ex = ret - rf; res.append(ex.mean() / ex.std() * np.sqrt(252))
    return np.array(res)

if __name__ == "__main__":
    rows = []; yearly_tab = {}; detail = {}
    for code in ("XU100", "XU030", "XBANK", "XUTUM"):
        px = load_index(code).reindex(cal).ffill()
        sigs = signals(px)
        m = cal >= START
        bh = px.pct_change().fillna(0)
        for cur in ("TL", "USD"):
            rb = bh[m] if cur == "TL" else to_usd(bh[m], B.fx_r[m])
            rff = B.rf_d[m] if cur == "TL" else B.tb_d[m]
            rows.append(dict(endeks=code, kural="AL-TUT (fiyat endeksi)", maliyet="-", para=cur, zaman_ici=1.0, islem_yil=0, **stats(rb, rff, ppy=252)))
            rows.append(dict(endeks=code, kural="%100 TL rf (mevduat/PPF)", maliyet="-", para=cur, zaman_ici=0.0, islem_yil=0,
                             **stats(B.rf_d[m] if cur == "TL" else to_usd(B.rf_d[m], B.fx_r[m]), rff, ppy=252)))
        for name, sg in sigs.items():
            for cname, cs in (("VIOP12.5bp", 0.000625), ("spot25bp", 0.00125)):
                variants = [("1x", dict())]
                if cname == "VIOP12.5bp": variants += [("2x VIOP", dict(lev=2.0)), ("volhedef%25", dict(volt=0.25))]
                for vn, kw in variants:
                    ret, pos = run(px, sg, cs, **kw)
                    ret = ret[m]; pos = pos[m]
                    ntr = ((pos > 0).astype(int).diff().abs() > 0).sum() / ((cal[m][-1] - cal[m][0]).days / 365.25)
                    for cur in ("TL", "USD"):
                        rs = ret if cur == "TL" else to_usd(ret, B.fx_r[m])
                        rff = B.rf_d[m] if cur == "TL" else B.tb_d[m]
                        st = stats(rs, rff, ppy=252)
                        st24 = stats(rs[rs.index >= "2024-01-01"], rff[rff.index >= "2024-01-01"], ppy=252)
                        rows.append(dict(endeks=code, kural=name + (" " + vn if vn != "1x" else ""), maliyet=cname, para=cur,
                                         zaman_ici=(pos > 0).mean(), islem_yil=ntr, **st, **{"CAGR_2024_26": st24.get("CAGR"), "Fazla_2024_26": st24.get("Fazla"), "MaxDD_2024_26": st24.get("MaxDD")}))
                        if vn == "1x" and cname == "VIOP12.5bp":
                            yearly_tab[(code, name, cur)] = yearly(rs.values, rs.index)
        # placebo (sadece 1x VIOP, TL)
        for name, sg in sigs.items():
            ret, pos = run(px, sg, 0.000625); ret = ret[m]
            ex = ret - B.rf_d[m]; shr = ex.mean() / ex.std() * np.sqrt(252)
            pl = placebo(px, sg, 0.000625, n=300)
            detail[f"{code}|{name}"] = {"Sharpe": float(shr), "placebo_medyan": float(np.median(pl)), "placebo_p95": float(np.percentile(pl, 95)), "yuzdelik": float((pl < shr).mean())}
        bhy = bh[m]
        yearly_tab[(code, "AL-TUT", "TL")] = yearly(bhy.values, bhy.index)
        yearly_tab[(code, "AL-TUT", "USD")] = yearly(to_usd(bhy, B.fx_r[m]).values, bhy.index)
    yearly_tab[("rf", "TL rf", "TL")] = yearly(B.rf_d[m].values, cal[m])
    df = pd.DataFrame(rows); df.to_csv(f"{OUTD}/t04_ozet.csv", index=False)
    Y = pd.DataFrame({" ".join(k): v for k, v in yearly_tab.items()}); Y.to_csv(f"{OUTD}/t04_yillik.csv")
    json.dump(detail, open(f"{OUTD}/t04_placebo.json", "w"), indent=1)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
    print(df[["endeks", "kural", "maliyet", "para", "zaman_ici", "islem_yil", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_2024_26", "Fazla_2024_26"]].round(3).to_string())
    print(json.dumps(detail, indent=0))
