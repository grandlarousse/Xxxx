"""Denetim: gecikmeli öncü iddialarının bağımsız yeniden hesaplanması.
(1) r_hisse(t+1) = a + b*r_piyasa(t) + c*r_hisse(t), Newey-West (5) t; tam / IS (2016-11..2021) / OOS (2022+).
    Ek: 'yetişme' u = beta60*r_piyasa(t) - r_hisse(t) (beta yalnız t'ye kadar), kendi gecikmesine EK katkı ayrıca.
    Ekonomik büyüklük: 1 sd öncü hareketinin 2x ETF'te ertesi gün beklenen etkisi (2*b*sd) ve maliyet (16 bp) karşılaştırması.
(2) BTC 16:00 ET -> ertesi gün 09:00 ET (saatlik, 09:00 başlangıçlı mumun açılışı) ile MSTR açılış boşluğu (gerçek zamanlı izleme gücü).
(3) leadlag_sweep.csv'de aile hedefleri için FDR bayrakları.
Çalıştır: python3 -I kod/denetim_tek_hisse_kaldiracli/d5_leadlag.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib, math
import numpy as np, pandas as pd
import dk, lib

def ols_nw(y, X, lags=5):
    X = np.column_stack([np.ones(len(y)), X]); b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b; n = len(y)
    XtXi = np.linalg.inv(X.T @ X)
    S = (X * e[:, None]).T @ (X * e[:, None]) / n
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1); G = (X[k:] * e[k:, None]).T @ (X[:-k] * e[:-k, None]) / n
        S += w * (G + G.T)
    V = n * XtXi @ S @ XtXi
    return b, b / np.sqrt(np.diag(V))

def main():
    pairs = [("AMZN", "SPY"), ("GOOGL", "SPY"), ("AAPL", "SPY"), ("MSFT", "SPY"), ("NVDA", "XLK"), ("NVDA", "SMH"), ("NVDA", "SPY"),
             ("TSLA", "QQQ"), ("META", "SPY")]
    rows = []
    print("(1) Gecikmeli öncü regresyonları (hisse 2016-11..2026-11; NW t):")
    for st, ld in pairs:
        s = dk.load_stock(st)["c"]; L = lib.load(ld)["c"]
        df = pd.concat([np.log(s).diff().rename("rs"), np.log(L).diff().rename("rl")], axis=1).dropna()
        beta = (df.rs.rolling(60).cov(df.rl) / df.rl.rolling(60).var())
        df["u"] = beta * df.rl - df.rs
        df["y"] = df.rs.shift(-1)
        df = df.dropna()
        for per, m in (("tam", slice(None)), ("IS", df.index <= dk.IS_END), ("OOS", df.index > dk.IS_END)):
            d = df.loc[m] if per != "tam" else df
            b1, t1 = ols_nw(d.y.values, d[["rl", "rs"]].values)
            b2, t2 = ols_nw(d.y.values, d[["u", "rs"]].values)
            sd_l = d.rl.std(); sd_u = d.u.std()
            rows.append(dict(hedef=st, oncu=ld, donem=per, n=len(d), b_lag=b1[1], t_lag=t1[1], t_kendi=t1[2],
                             etki_2x_bp_1sd=2 * b1[1] * sd_l * 1e4, b_yetisme=b2[1], t_yetisme=t2[1], etki_yetisme_2x_bp_1sd=2 * b2[1] * sd_u * 1e4))
        r = [x for x in rows if x["hedef"] == st and x["oncu"] == ld]
        print(f"  {st:5s} <- {ld:4s}: lag t tam {r[0]['t_lag']:5.2f} IS {r[1]['t_lag']:5.2f} OOS {r[2]['t_lag']:5.2f} | 2x etki/1sd {r[0]['etki_2x_bp_1sd']:6.1f} bp (OOS {r[2]['etki_2x_bp_1sd']:6.1f}) | "
              f"yetişme t tam {r[0]['t_yetisme']:5.2f} IS {r[1]['t_yetisme']:5.2f} OOS {r[2]['t_yetisme']:5.2f} | yetişme 2x etki/1sd {r[0]['etki_yetisme_2x_bp_1sd']:6.1f} bp")
    R = pd.DataFrame(rows); R.to_csv(os.path.join(dk.OUT, "d5_leadlag_regresyon.csv"), index=False)
    print("  Not: maliyet 2x ETF'te ~16 bp gidiş-dönüş; 1 sd'lik sinyal günlerinin yalnız ~%32'sinde |öncü|>1 sd.")

    print("\n(2) BTC gece hareketi -> MSTR açılış boşluğu (2023-06+):")
    h = pd.read_parquet(os.path.join(dk.ROOT, "data", "crypto", "BTC-USD_h1.parquet"))
    h.index = h.index.tz_convert("America/New_York")
    p16 = lib.btc_at_us_close("BTC-USD")
    o9 = h[h.index.hour == 9]["o"]; o9.index = o9.index.tz_localize(None).normalize(); o9 = o9[~o9.index.duplicated(keep="last")]
    ms = dk.load_stock("MSTR")
    gap = np.log(ms["o"] / ms["c"].shift(1))
    prev16 = p16.reindex(ms.index).shift(1)
    bt = np.log(o9.reindex(ms.index) / prev16)
    d = pd.concat([gap.rename("gap"), bt.rename("btc")], axis=1).dropna(); d = d[d.index >= "2023-06-01"]
    c = d.corr().iloc[0, 1]; b = np.polyfit(d.btc, d.gap, 1)[0]
    print(f"  n {len(d)} corr {c:.3f} beta {b:.2f} R2 {c * c:.2f}")
    for st in ("COIN",):
        x = dk.load_stock(st); g2 = np.log(x["o"] / x["c"].shift(1))
        dd = pd.concat([g2.rename("gap"), bt.rename("btc")], axis=1).dropna(); dd = dd[dd.index >= "2023-06-01"]
        print(f"  {st}: n {len(dd)} corr {dd.corr().iloc[0, 1]:.3f}")
    print("\n(3) leadlag_sweep.csv, aile hedefleri, FDR bayrakları:")
    S = pd.read_csv(os.path.join(dk.ROOT, "sonuclar", "leadlag_sweep.csv"))
    fam = ["NVDL", "TSLL", "MSTU", "CONL", "NVDU", "TSLQ", "NVDS", "AAPU", "AMZU", "METU", "MSFU", "GGLL"]
    tcol = [c for c in S.columns if c.startswith("fdr10")]
    tgt = [c for c in S.columns if c in ("target", "hedef", "sym", "T")]
    T = S[S[tgt[0]].isin(fam)]
    print(f"  satır {len(T)}; FDR sütunları {tcol}; bayrak toplamları:", {c: int(T[c].fillna(False).astype(bool).sum()) for c in tcol})

if __name__ == "__main__":
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main()
    txt = buf.getvalue(); print(txt)
    open(os.path.join(dk.OUT, "d5_cikti.txt"), "w").write(txt)
