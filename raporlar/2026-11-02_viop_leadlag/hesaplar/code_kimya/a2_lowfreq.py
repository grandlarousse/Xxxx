"""A2: düşük frekans (haftalık/aylık) + USD bazlı + lag1 kısmi korelasyon.
Günlük senkron korelasyon eşzamansız kapanış nedeniyle zayıf görünebilir -> haftalık (Cuma-Cuma) getiri ile yeniden test.
Çıktı: res_lowfreq.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc import *
from kc import _corr
from a1_hyp import H

HERE = os.path.dirname(os.path.abspath(__file__))


def agg(r, freq):
    r = r.copy(); ok = r.notna().astype(float)
    s = r.fillna(0).resample(freq).sum(); n = ok.resample(freq).sum()
    return s.where(n >= (3 if freq.startswith("W") else 12))


def lowfreq(stock, drv):
    a = R(stock); b = R(drv); m = R("XU100"); fx = R("TRY=X")
    au = a - fx; mu = m - fx
    o = {"stock": stock, "driver": drv}
    # günlük: lag1 kısmi korelasyon (XU100_t kontrollü) ve lag0+lag1 toplam
    o["pc_l1_d"], _ = pc(a, b.shift(1), [m], "2009-01-01")
    o["pc_l01_d"], _ = pc(a, b + b.shift(1), [m], "2009-01-01")
    for f, lab in [("W-FRI", "w"), ("ME", "m")]:
        A, B, M, AU, MU = agg(a, f), agg(b, f), agg(m, f), agg(au, f), agg(mu, f)
        o[f"c_{lab}"], o[f"n_{lab}"] = _corr(A, B, "2009-01-01", min_n=24)
        o[f"pc_{lab}"], _ = pc(A, B, [M], "2009-01-01", min_n=24)
        o[f"pc_{lab}_IS"], _ = pc(A, B, [M], "2009-01-01", SPLIT, min_n=24)
        o[f"pc_{lab}_OOS"], _ = pc(A, B, [M], SPLIT, min_n=24)
        o[f"c_{lab}_usd"], _ = _corr(AU, B, "2009-01-01", min_n=24)
        o[f"pc_{lab}_usd"], _ = pc(AU, B, [MU], "2009-01-01", min_n=24)
        if lab == "w":
            o["t_w"] = nwt_corr(resid(A, [M]), resid(B, [M]), "2009-01-01")
            o["c_w_3y"], _ = _corr(A, B, "2023-10-30", min_n=24)
            o["pc_w_3y"], _ = pc(A, B, [M], "2023-10-30", min_n=24)
            by = by_year(A, B, [M]).dropna() if False else None
    return o


if __name__ == "__main__":
    rows = []
    for s, drvs in H.items():
        for d in dict.fromkeys(drvs):
            try: rows.append(lowfreq(s, d))
            except Exception as e: print("skip", s, d, e)
    df = pd.DataFrame(rows); df.to_csv(os.path.join(HERE, "res_lowfreq.csv"), index=False)
    pd.set_option("display.width", 250)
    for s, g in df.groupby("stock", sort=False):
        g = g.reindex(g.pc_w.abs().sort_values(ascending=False).index).head(10)
        print(g[["driver", "pc_l1_d", "pc_l01_d", "c_w", "pc_w", "t_w", "pc_w_IS", "pc_w_OOS", "pc_w_3y", "pc_w_usd", "c_m", "pc_m"]].round(2).to_string(index=False))
