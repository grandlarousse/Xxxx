"""cin - Adım 6: Çin sürücüleri (orijinal + alternatif) ile BIST hisseleri.
Zamanlama (cin_lib/ll konvansiyonu): Çin kapanışı 07:00 UTC (HK 08:00) -> BIST t seansından ÖNCE/başında => D_t 'Asya lag0'.
  Asya sürücüsü:  sync   = corr(cc_t, D_t)  [D_t penceresi (07:00 t-1, 07:00 t] => BIST t-1 seansını da içerir]
                  gap    = corr(gap_t, D_t)  (gece/eşzamanlı bilgi)
                  lead   = corr(intra_t, D_t) (İŞLENEBİLİR: Çin kapanışı ~ BIST sürekli işlem açılışı; HK için 1 saat örtüşme var -> D_{t-1} ayrıca)
                  reverse= corr(D_t, intra_{t-1})  (BIST t-1 seansı -> Çin t)
  ABD/COMEX kapanışlı alternatif: sync = corr(cc_t, A_t); gap = corr(gap_t, A_{t-1}) (eşzamansız kapanış, işlenemez);
                  lead = corr(intra_t, A_{t-1}) (işlenebilir); reverse = corr(A_{t+1}, intra_t)... raporlanmaz (A_t zaten BIST t'yi içerir)
Haftalık: BIST takviminde Cuma-Cuma toplam log getiri.
Çıktı: code_cin/bist_pairs.csv  (tüm metrikler)"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_cin")
import cin_lib as C, numpy as np, pandas as pd
ll = C.ll
from pairs_def import ORIG, ALT
OUT = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_cin/"
ASIA_CLOSE = lambda s: s.startswith(("SIDX:", "FUT")) or s.endswith((".SS", ".SZ", ".HK", ".KS", ".T", ".AX", ".TW")) or s in ("^HSI", "^HSCE", "^KS11", "^N225", "^AXJO")
# (hisse, sürücü, rol[orig/alt], eşlenen orijinal)
G = {
 "EREGL KRDMD BRSAN": {"orig": ["FUT:I", "FUT:RB", "FUT:HC", "FUT:J", "FUT:JM", "600019.SS", "000898.SZ", "SIDX:sh000300"],
                       "alt": {"TIO=F": "FUT:I", "FMG.AX": "FUT:I", "RIO.AX": "FUT:I", "BHP": "FUT:I", "SLX": "600019.SS", "MT": "FUT:HC", "PKX": "FUT:HC",
                               "HRC=F": "FUT:HC", "0347.HK": "000898.SZ", "ASHR": "SIDX:sh000300", "HCC": "FUT:JM", "005490.KS": "FUT:HC"}},
 "SASA": {"orig": ["FUT:TA", "FUT:PX", "FUT:PF", "FUT:EG", "600346.SS"], "alt": {"BZ=F": "FUT:TA", "IVL.BK": "FUT:TA", "1326.TW": "FUT:PF", "CL=F": "FUT:PX", "1303.TW": "FUT:EG"}},
 "PETKM": {"orig": ["FUT:PP", "FUT:L", "FUT:V", "FUT:EG", "FUT:MA", "600028.SS"], "alt": {"BZ=F": "FUT:PP", "LYB": "FUT:L", "2010.SR": "FUT:EG", "011170.KS": "FUT:PP", "1301.TW": "FUT:V", "WLK": "FUT:V"}},
 "ARCLK VESTL": {"orig": ["000333.SZ", "600690.SS", "000651.SZ", "000921.SZ", "000100.SZ", "SIDX:sh000300"],
                 "alt": {"0300.HK": "000333.SZ", "6690.HK": "600690.SS", "HSHCY": "600690.SS", "1070.HK": "000100.SZ", "CHIQ": "000333.SZ", "ASHR": "SIDX:sh000300", "WHR": "000333.SZ", "ELUX-B.ST": "000333.SZ"}},
 "SISE": {"orig": ["FUT:FG", "FUT:SA", "000822.SZ", "601636.SS"], "alt": {"0868.HK": "FUT:FG", "5201.T": "FUT:FG", "SGO.PA": "FUT:FG", "TATACHEM.NS": "FUT:SA"}},
 "TRALT": {"orig": ["FUT:AU", "600547.SS", "601899.SS"], "alt": {"GC=F": "FUT:AU", "GLD": "FUT:AU", "GDX": "600547.SS", "1787.HK": "600547.SS", "2899.HK": "601899.SS", "ZIJMF": "601899.SS"}},
 "TRMET": {"orig": ["FUT:CU", "FUT:AU", "601899.SS", "603993.SS"], "alt": {"HG=F": "FUT:CU", "GC=F": "FUT:AU", "COPX": "FUT:CU", "2899.HK": "601899.SS", "CMCLF": "603993.SS"}},
 "TUPRS": {"orig": ["FUT:SC", "600028.SS", "601857.SS"], "alt": {"BZ=F": "FUT:SC", "CL=F": "FUT:SC", "0386.HK": "600028.SS", "SNPMF": "600028.SS", "0857.HK": "601857.SS", "PCCYF": "601857.SS"}},
 "ASTOR": {"orig": ["FUT:CU", "FUT:AL", "600089.SS", "601179.SS", "002028.SZ"], "alt": {"HG=F": "FUT:CU", "COPX": "FUT:CU", "ALI=F": "FUT:AL", "ASHR": "600089.SS"}},
 "FROTO TOASO DOAS": {"orig": ["002594.SZ", "1211.HK", "300750.SZ", "FUT:LC", "SIDX:sh000300"],
                      "alt": {"BYDDY": "1211.HK", "BYDDF": "1211.HK", "KARS": "002594.SZ", "NIO": "002594.SZ", "TSLA": "002594.SZ", "CHIQ": "002594.SZ", "ALB": "FUT:LC", "ASHR": "SIDX:sh000300"}},
 "GUBRF": {"orig": ["FUT:UR"], "alt": {"CF": "FUT:UR", "NTR": "FUT:UR", "YAR.OL": "FUT:UR"}},
 "CIMSA OYAKC": {"orig": ["600585.SS"], "alt": {"0914.HK": "600585.SS", "AHCHY": "600585.SS"}},
 "XU100 XU030": {"orig": ["SIDX:sh000300", "SIDX:sh000001", "^HSI", "^HSCE", "SIDX:USDCNH", "FUT:I", "FUT:CU"],
                 "alt": {"ASHR": "SIDX:sh000300", "CNYA": "SIDX:sh000300", "KBA": "SIDX:sh000300", "FXI": "^HSCE", "MCHI": "^HSCE", "EWH": "^HSI", "KWEB": "^HSI", "CNY=X": "SIDX:USDCNH", "TIO=F": "FUT:I", "HG=F": "FUT:CU"}},
}
_d = {}
def dec(s):
    if s not in _d: _d[s] = ll.decomp(s)
    return _d[s]
XU = ll.ret("XU100")
def tstat(a, b):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if len(df) < 60: return np.nan, np.nan, len(df)
    za = (df.a - df.a.mean()) / df.a.std(); zb = (df.b - df.b.mean()) / df.b.std(); bb, t, n = ll.nw_t(za, zb); return bb, t, n
def weekly(x): return x.groupby(pd.Grouper(freq="W-FRI")).sum(min_count=2)
def analyze(stock, drv):
    y = ll.ret(stock); D = C.ret_bist(drv); asia = ASIA_CLOSE(drv)
    st = max(y.dropna().index[0], D.dropna().index[0], pd.Timestamp("2010-01-01"))
    y = y[y.index >= st]; D = D[D.index >= st]
    df = pd.concat([y.rename("y"), D.rename("d"), XU.rename("m")], axis=1).dropna()
    df = df[df.index >= st]
    if len(df) < 120: return None
    last = df.index[-1]; o = {"stock": stock, "driver": drv, "asia_close": asia, "n": len(df), "start": str(df.index[0].date())}
    o["corr_full"] = df.y.corr(df.d)
    for lab, yrs in [("3y", 3), ("1y", 1)]:
        x = df[df.index >= last - pd.DateOffset(years=yrs)]; o[f"corr_{lab}"] = x.y.corr(x.d)
    o["pcorr_xu100"] = ll.partial_corr(df.y, df.d, [df.m])[0] if stock not in ("XU100", "XU030") else np.nan
    o["beta"] = np.cov(df.y, df.d)[0, 1] / df.d.var()
    _, o["t_sync"], _ = tstat(df.y, df.d)
    # USD bazlı senkron
    yu = (y - ll.ret("TRY=X")); o["corr_usd"] = pd.concat([yu, D], axis=1).dropna().corr().iloc[0, 1]
    # haftalık
    W = pd.concat([weekly(y).rename("y"), weekly(D).rename("d"), weekly(XU).rename("m")], axis=1).dropna()
    W = W[W.index >= st]; o["corr_w"] = W.y.corr(W.d); o["n_w"] = len(W)
    o["pcorr_w_xu100"] = ll.partial_corr(W.y, W.d, [W.m])[0] if stock not in ("XU100", "XU030") else np.nan
    # yıllara göre işaret istikrarı (senkron)
    by = df.groupby(df.index.year).apply(lambda g: g.y.corr(g.d) if len(g) > 60 else np.nan).dropna()
    o["yr_same_sign"] = float((np.sign(by) == np.sign(o["corr_full"])).mean()) if len(by) else np.nan; o["n_years"] = len(by)
    is_ = df[df.index < "2021-01-01"]; oos = df[df.index >= "2021-01-01"]
    o["corr_is"] = is_.y.corr(is_.d) if len(is_) > 120 else np.nan; o["corr_oos"] = oos.y.corr(oos.d)
    # gap / intra
    dd = dec(stock); dd = dd[dd.index >= st]
    sig = D if asia else D.shift(1)
    o["gap_corr"], o["gap_t"], _ = tstat(dd["gap"], sig)
    o["intra_corr"], o["intra_t"], o["n_intra"] = tstat(dd["intra"], sig)
    if asia:
        o["intra_lag1_corr"], o["intra_lag1_t"], _ = tstat(dd["intra"], D.shift(1))   # D_{t-1} -> intra_t (HK için temiz)
        o["rev_corr"], o["rev_t"], _ = tstat(D, dd["intra"].shift(1))                 # BIST t-1 seansı -> Çin t
        o["cc_lag1_corr"], o["cc_lag1_t"], _ = tstat(y, D.shift(1))                    # Asya D_{t-1} -> cc_t (çok günlük sürüklenme)
    else:
        o["intra_lag1_corr"], o["intra_lag1_t"] = o["intra_corr"], o["intra_t"]
        o["rev_corr"], o["rev_t"], _ = tstat(D.shift(-1), dd["intra"])                 # BIST seansı -> ertesi gün ABD getirisi
        o["cc_lag1_corr"], o["cc_lag1_t"], _ = tstat(y, D.shift(2))
    # işlenebilir öncülük backtest'i: sinyal (Asya D_t veya ABD A_{t-1}) -> BIST gün-içi t, 10 bps
    res, _ = ll.backtest(sig, dd["intra"], cost_bps=10.0)
    o["bt_oos_sharpe"] = res["OOS"].get("sharpe", np.nan); o["bt_oos_mean_bps"] = res["OOS"].get("mean_bps", np.nan)
    o["bt_is_sharpe"] = res["IS"].get("sharpe", np.nan); o["bt_oos_t"] = res["OOS"].get("t", np.nan)
    res0, _ = ll.backtest(sig, dd["intra"], cost_bps=0.0); o["bt_oos_mean_bps_gross"] = res0["OOS"].get("mean_bps", np.nan)
    return o
if __name__ == "__main__":
    rows = []
    for grp, spec in G.items():
        for s in grp.split():
            for d in spec["orig"]:
                r = analyze(s, d)
                if r: r.update({"role": "orig", "maps_to": d, "group": grp}); rows.append(r)
            for a, om in spec["alt"].items():
                r = analyze(s, a)
                if r: r.update({"role": "alt", "maps_to": om, "group": grp}); rows.append(r)
        print(grp, "ok", flush=True)
    B = pd.DataFrame(rows); B.to_csv(OUT + "bist_pairs.csv", index=False); print(len(B), "satır")
