"""e_: TUPRS<-ABD rafineri yeniden uretim (PBF'siz) + FROTO S_KENDI. python3 -I e_curutme2.py"""
import math, traceback, numpy as np, pandas as pd
V = "/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri/panel/"
EK = "/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/ek/"
def tt(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x)
    return x.mean() / (x.std(ddof=1) / math.sqrt(n)) if n > 2 and x.std(ddof=1) > 0 else np.nan
def d(x): x = np.asarray(x, float); x = x[np.isfinite(x)]; return f"n={len(x)} ort={x.mean():.1f} t={tt(x):.2f}" if len(x) else "n=0"
fr = pd.read_parquet(V + "fut_ret.parquet"); cal = pd.DatetimeIndex(fr.index).normalize(); fr.index = cal; N = len(cal)
def W(n): x = pd.read_parquet(V + n); x.index = pd.DatetimeIndex(x.index).normalize(); return x.reindex(cal)
FT, FV, FL = W("fut_trades.parquet"), W("fut_value_tl.parquet"), W("fut_limit.parquet")
pos = {t: i for i, t in enumerate(cal)}

def F():
    use = ["aile", "hedef", "oncu", "sinyal", "giris", "tutma", "donem", "n", "brut", "t"]
    out = []
    for c in pd.read_csv(EK + "sonuc_b1.csv", sep=";", usecols=use, chunksize=300000):
        out.append(c[(c.hedef.isin(["FROTO", "ENKAI"])) & (c.sinyal == "S_KENDI") & (c.donem.isin(["TAM", "SON2Y"])) & (c.giris.isin(["E0", "E2"]))])
    o = pd.concat(out).drop_duplicates(["hedef", "giris", "tutma", "donem"])
    print(o.sort_values(["hedef", "giris", "tutma", "donem"]).to_string(index=False))
print("===== F S_KENDI");
try: F()
except Exception: traceback.print_exc()

def T():
    dg = pd.read_parquet(V + "dis_gunluk.parquet"); dg["date"] = pd.to_datetime(dg["date"]).dt.normalize()
    def asof_p(s):
        x = dg[dg.sym == s].drop_duplicates("date", keep="last").set_index("date")["adj"]
        return x.reindex(x.index.union(cal)).ffill().reindex(cal)
    def R1(s): lp = np.log(asof_p(s)); return lp.shift(1) - lp.shift(2)
    def beta(r, m): return (r.rolling(250, min_periods=120).cov(m) / m.rolling(250, min_periods=120).var()).shift(1)
    def sig(e): return e.rolling(120, min_periods=60).std().shift(1)
    ix = R1("^GSPC"); E = {s: (lambda r: r - beta(r, ix) * ix)(R1(s)) for s in ("VLO", "MPC", "PSX", "PBF")}
    u = "TUPRS"; ok = ((FT[u] >= 20) & (FV[u] >= 1e6) & (FL[u] != 1)).values
    S2 = fr[u].rolling(2, min_periods=2).sum().shift(-2).values
    def run(comps, h=2, sh=0, per=None):
        Ed = pd.concat([E[c] for c in comps], axis=1); okk = Ed.notna().sum(1) >= len(comps) / 2
        eL = Ed.mean(1).where(okk); zL = (eL / sig(eL)).values; dd = np.sign(zL)
        I, Rr = [], []; last = -1
        for i in np.where((np.abs(zL) >= 1) & ~np.isnan(zL))[0]:
            e = i + sh; x = e + h
            if x >= N: break
            if e < last or not (ok[e] and ok[x]) or np.isnan(S2[e]): continue
            I.append(i); Rr.append(1e4 * dd[i] * S2[e]); last = x
        I = np.array(I); Rr = np.array(Rr); dts = cal[I + sh]
        m = (dts >= "2017-03-01"); m2 = dts >= "2024-11-10"; m3 = dts >= "2022-01-01"
        return f"TAM {d(Rr[m])} | OOS {d(Rr[m3])} | SON2Y {d(Rr[m2])} | uzun pay {np.mean(dd[I][m] > 0):.2f}", I, Rr, dd
    for comps in (["VLO", "MPC", "PSX", "PBF"], ["VLO", "MPC", "PSX"], ["PBF"], ["VLO"], ["MPC"], ["PSX"], ["VLO", "MPC", "PBF"], ["VLO", "PSX", "PBF"], ["MPC", "PSX", "PBF"]):
        print("+".join(comps), "E0 h2:", run(comps)[0])
    print("4lu E2 h2:", run(["VLO", "MPC", "PSX", "PBF"], sh=1)[0])
    # gun ayristirma (islemler_b2 resmi listesi)
    t = pd.read_csv(EK + "islemler_b2.csv", sep=";", parse_dates=["giris_tarihi"])
    x = t[(t.cift == "TUPRS<-VLO+MPC+PSX+PBF") & (t.sinyal == "S_ONCU")]
    ei = np.array([pos[pd.Timestamp(v)] for v in x.giris_tarihi]); y = x.yon.values; f = fr[u].values
    print("resmi liste", d(x.brut_bps), "| uzun", d(x.brut_bps[y > 0]), "| kisa", d(x.brut_bps[y < 0]))
    for k in (0, 1, 2, 3):
        print(f"  gun e+{k} yonlu vadeli", d(1e4 * y * f[np.minimum(ei + k, N - 1)]))
    xs = x[x.giris_tarihi >= "2024-11-10"]; print("  SON2Y", d(xs.brut_bps), "| uzun", d(xs.brut_bps[xs.yon > 0]), "| kisa", d(xs.brut_bps[xs.yon < 0]))
    print("  yil:", x.groupby(x.giris_tarihi.dt.year).brut_bps.agg(["count", "mean"]).round(0).T.to_string())
    srt = np.sort(x.brut_bps.values)[::-1]; print("  en iyi 10 cikinca", d(srt[10:]), "| SON2Y en iyi 5 cikinca", d(np.sort(xs.brut_bps.values)[::-1][5:]))
print("===== T TUPRS")
try: T()
except Exception: traceback.print_exc()
