"""e_: curutme kontrolleri (yalniz okur). python3 -I e_curutme.py"""
import math, sys, traceback, numpy as np, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30); pd.set_option("display.max_rows", 200)
V = "/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri/panel/"
EK = "/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/ek/"
def tt(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x)
    return x.mean() / (x.std(ddof=1) / math.sqrt(n)) if n > 2 and x.std(ddof=1) > 0 else np.nan
def d(x): x = np.asarray(x, float); x = x[np.isfinite(x)]; return f"n={len(x)} ort={x.mean():.1f} t={tt(x):.2f}" if len(x) else "n=0"
fr = pd.read_parquet(V + "fut_ret.parquet"); cal = pd.DatetimeIndex(fr.index).normalize(); fr.index = cal; N = len(cal)
UND = [c for c in fr.columns if c not in ("XU030", "XLBNK", "USDTRY", "XAUUSD", "XAGUSD", "XAUTRY")]
pos = {t: i for i, t in enumerate(cal)}
def sec(name, f):
    print("\n==========", name, flush=True)
    try: f()
    except Exception: traceback.print_exc()

# ---------------- A: S_KUL / S_IKISI / BAZSIZ, E0 vs E2
def A():
    use = ["aile", "hedef", "oncu", "agirlik", "sinyal", "giris", "tutma", "donem", "n", "brut", "t"]
    ps = []
    for c in pd.read_csv(EK + "sonuc_b1.csv", sep=";", usecols=use, chunksize=300000):
        ps.append(c[c.donem.isin(["TAM", "OOS", "SON2Y"]) & c.sinyal.isin(["S_KUL", "S_IKISI", "S_KUL_BAZSIZ", "S_ONCU", "S_KUL_YATAY", "S_KUL_TERS"])])
    s = pd.concat(ps); s = s[~((s.aile == "F1_GRUP") & (s.agirlik == "ESIT"))]
    global SON; SON = s
    for fam in (["F1_GRUP", "F2_SEKTOR", "F4_MAKRO", "F5_VIOP"], ["F2_SEKTOR"], ["PIYASA"]):
        m = s[s.aile.isin(fam) & (s.donem == "TAM") & s.giris.isin(["E0", "E2"])]
        g = m.groupby(["sinyal", "giris", "tutma"]).apply(lambda x: pd.Series(dict(n=x.n.sum(), brut_nw=np.average(x.brut, weights=x.n), cift=len(x))))
        print(fam, "\n", g.unstack("giris").round(1).to_string())
        pv = m[m.tutma == 2].pivot_table(index=["aile", "hedef", "oncu", "agirlik"], columns=["sinyal", "giris"], values="brut")
        for gi in ("E0", "E2"):
            dif = (pv[("S_KUL", gi)] - pv[("S_IKISI", gi)]).dropna()
            print(f"  h2 {gi}: cift basina S_KUL-S_IKISI: ort {dif.mean():.1f} medyan {dif.median():.1f} negatif pay {(dif < 0).mean():.2f} t(ciftler arasi) {tt(dif):.2f} n_cift {len(dif)}")
    k = s[(s.hedef == "KCHOL") & s.oncu.str.startswith("TUPRS.IS+FROTO") & (s.sinyal.isin(["S_KUL", "S_ONCU"])) & (s.tutma == 2)]
    print(k.sort_values(["sinyal", "giris", "donem"]).to_string(index=False))
    for gg in ("ESIT",):
        pass
sec("A sonuc_b1 havuz E0/E2", A)

# ESIT KCHOL ayri
def A2():
    use = ["aile", "hedef", "oncu", "agirlik", "sinyal", "giris", "tutma", "donem", "n", "brut", "t", "net_bireysel"]
    out = []
    for c in pd.read_csv(EK + "sonuc_b1.csv", sep=";", usecols=use, chunksize=300000):
        out.append(c[((c.hedef == "KCHOL") & c.oncu.str.startswith("TUPRS.IS+FROTO") & (c.agirlik == "ESIT") & c.sinyal.isin(["S_KUL", "S_ONCU"]) & (c.tutma == 2) & (c.donem.isin(["TAM", "OOS", "SON2Y"])))
                     | (c.oncu.isin(["VIOP:USDTRY"]) & c.hedef.isin(["FROTO", "ENKAI"]) & c.sinyal.isin(["S_KUL", "S_ONCU", "S_IKISI"]) & (c.donem.isin(["TAM", "OOS", "SON2Y"])))])
    print(pd.concat(out).sort_values(["hedef", "agirlik", "sinyal", "giris", "tutma", "donem"]).to_string(index=False))
sec("A2 KCHOL ESIT + USDTRY satirlari", A2)

# ---------------- B: mekanizma (spot kapanis vs uzlasma) dogrudan
def B():
    sp = pd.read_parquet(V + "spot_gunluk.parquet"); sp["date"] = pd.to_datetime(sp["date"]).dt.normalize()
    ADJ = sp.pivot_table(index="date", columns="sym", values="adj", aggfunc="last").reindex(cal)
    rows = []
    for u in UND:
        s = u + ".IS"
        if s not in ADJ: continue
        r = np.log(ADJ[s] / ADJ[s].shift(1)); r[r.abs() > 0.095] = np.nan
        f = fr[u].copy(); f[f.abs() > 0.095] = np.nan
        sg = r.rolling(120, min_periods=60).std().shift(1); z = r / sg
        gap = r - f
        rows.append(pd.DataFrame(dict(u=u, r=r, f=f, z=z, gap=gap, f1=f.shift(-1), r1=r.shift(-1), f2=f.shift(-2), r2=r.shift(-2), yr=cal.year)))
    D = pd.concat(rows).dropna(subset=["r", "f", "f1", "r1", "z"])
    x = D.gap - D.groupby("u").gap.transform("mean"); y = D.f1 - D.groupby("u").f1.transform("mean")
    b = (x * y).sum() / (x * x).sum(); res = y - b * x; se = math.sqrt((res ** 2).sum() / (len(x) - 1) / (x * x).sum())
    print(f"f(t+1) ~ (spot_t - fut_t) havuz egim {b:.3f} t {b/se:.1f} n {len(x)}")
    x2 = D.r - D.groupby("u").r.transform("mean"); y2 = D.f - D.groupby("u").f.transform("mean")
    print(f"ayni gun f(t) ~ spot(t) egim {(x2*y2).sum()/(x2*x2).sum():.3f}")
    big = D[D.z.abs() >= 1]; sgn = np.sign(big.z)
    print("|z_spot|>=1 gunleri, yon=sign(z) (devam pozitif):")
    print("  ertesi gun vadeli  bps:", d(1e4 * sgn * big.f1), "| ertesi gun spot bps:", d(1e4 * sgn * big.r1))
    print("  t+2 vadeli bps:", d(1e4 * sgn * big.f2), "| t+2 spot:", d(1e4 * sgn * big.r2))
    print("  ayni gun spot - vadeli (gap) bps:", d(1e4 * sgn * big.gap))
    for yr in (2017, 2019, 2021, 2023, 2025, 2026):
        bb = big[big.yr == yr]; print(f"  {yr}: ertesi gun vadeli {d(1e4*np.sign(bb.z)*bb.f1)} | spot {d(1e4*np.sign(bb.z)*bb.r1)}")
sec("B mekanizma", B)

# ---------------- C: KCHOL REG islemleri
def C():
    t = pd.read_csv(EK + "islemler_b1.csv", sep=";", parse_dates=["giris_tarihi"])
    k = t[t.cift.str.startswith("KCHOL<-TUPRS.IS+FROTO") & (t.sinyal == "S_KUL")].reset_index(drop=True)
    br = np.where(k.giris_tarihi.diff().dt.days < 0)[0]; print("blok sinirlari", br, "toplam", len(k))
    reg = k.iloc[:br[0]] if len(br) else k; esit = k.iloc[br[0]:] if len(br) else None
    for nm, x in (("REG", reg), ("ESIT", esit)):
        if x is None: continue
        g = x.brut_bps.values; print(nm, d(g), "isabet", (g > 0).mean().round(2), "medyan", np.median(g).round(1))
        print("  uzun", d(g[x.yon > 0]), "| kisa", d(g[x.yon < 0]))
        srt = np.sort(g)[::-1]
        print("  en iyi 5 cikinca", d(srt[5:]), "| en iyi 10 cikinca", d(srt[10:]), "| en iyi 10 toplam payi", round(srt[:10].sum() / g.sum(), 2))
        print("  yil:", x.groupby(x.giris_tarihi.dt.year).brut_bps.agg(["count", "mean"]).round(0).T.to_string())
        mo = x.groupby(x.giris_tarihi.dt.to_period("M")).brut_bps.agg(["count", "sum"]).sort_values("sum", ascending=False)
        print("  en karli 5 ay:", mo.head(5).to_dict("index"), "| ay sayisi", len(mo), "| ilk5 ay payi", round(mo["sum"].head(5).sum() / g.sum(), 2))
        print("  |z_L|>=2 ", d(g[x.z_L.abs() >= 2]), "| 1-2 ", d(g[x.z_L.abs() < 2]))
        print("  YATAY(dz>=-0.5) ", d(g[(x.yon * x.z_T) >= -0.5]), "| TERS ", d(g[(x.yon * x.z_T) < -0.5]))
    if esit is not None:
        sr, se_ = set(reg.giris_tarihi), set(esit.giris_tarihi)
        print("REG-ESIT ortak giris gunu", len(sr & se_), "yalniz REG", len(sr - se_), "yalniz ESIT", len(se_ - sr))
        print("  REG ortak gunler", d(reg[reg.giris_tarihi.isin(se_)].brut_bps), "| REG yalniz", d(reg[~reg.giris_tarihi.isin(se_)].brut_bps))
        print("  ESIT yalniz", d(esit[~esit.giris_tarihi.isin(sr)].brut_bps))
sec("C KCHOL", C)

# ---------------- D: FROTO <- USDTRY
def D_():
    t = pd.read_csv(EK + "islemler_b1.csv", sep=";", parse_dates=["giris_tarihi"])
    usd = fr["USDTRY"]; usdm = usd - usd.rolling(20, min_periods=15).mean().shift(1)
    for cift, sg in (("FROTO<-VIOP:USDTRY", "S_KUL"), ("ENKAI<-VIOP:USDTRY", "S_ONCU"), ("FROTO<-VIOP:USDTRY", "S_ONCU")):
        x = t[(t.cift == cift) & (t.sinyal == sg)].copy()
        ei = np.array([pos[pd.Timestamp(v)] for v in x.giris_tarihi]); i = ei - 1; hd = cift.split("<-")[0]
        f = fr[hd].values; yon = x.yon.values
        print(cift, sg, d(x.brut_bps), "uzun pay", (yon > 0).mean().round(2))
        for k in (0, 1, 2, 3, 4):
            print(f"   gun t+{k} yonlu vadeli getiri", d(1e4 * yon * f[np.minimum(i + k, N - 1)]))
        u_raw = 1e4 * usd.values[i]; u_dm = 1e4 * usdm.values[i]
        x["yil"] = x.giris_tarihi.dt.year; x["usd_raw"] = u_raw; x["usd_dm"] = u_dm
        print("   yil:", x.groupby("yil").agg(n=("brut_bps", "count"), ort=("brut_bps", "mean"), usd_ham_abs=("usd_raw", lambda v: np.abs(v).median()), usd_dm_abs=("usd_dm", lambda v: np.abs(v).median())).round(1).T.to_string())
        s2 = x[x.giris_tarihi >= "2024-11-10"]
        print("   SON2Y", d(s2.brut_bps), "| USDTRY ham |bps| medyan", np.median(np.abs(s2.usd_raw)).round(1) if len(s2) else None, "| artik |bps| medyan", np.median(np.abs(s2.usd_dm)).round(1) if len(s2) else None)
        wk = x.giris_tarihi.dt.to_period("W").value_counts(); mo = x.groupby(x.giris_tarihi.dt.to_period("M")).brut_bps.agg(["count", "sum"]).sort_values("sum", ascending=False)
        print("   farkli hafta", len(wk), "ayni haftada >=2 islem olan hafta", int((wk >= 2).sum()), "| en karli 5 ay", mo.head(5).to_dict("index"), "| ilk5 ay payi", round(mo["sum"].head(5).sum() / x.brut_bps.sum(), 2))
        srt = np.sort(x.brut_bps.values)[::-1]; print("   en iyi 10 cikinca", d(srt[10:]), "| en kotu 10 cikinca", d(srt[:-10]))
        big = np.abs(u_raw) >= 100; print("   USDTRY |ham|>=100bps sinyal gunleri", d(x.brut_bps[big]), "| digerleri", d(x.brut_bps[~big]))
sec("D USDTRY", D_)

# ---------------- E: SAHOL/AKBNK z60
def E():
    t = pd.read_csv(EK + "islemler_b4.csv", sep=";", parse_dates=["giris_tarihi", "cikis_tarihi"])
    for sv, gi in (("A_ESIK1.5", "E0"), ("A_ESIK1.5", "E2")):
        x = t[(t.kural == "K2_SAHOL_AKBNK") & (t.surum == sv) & (t.giris == gi)].copy()
        net = x.brut_bps - x.c_bireysel
        print(sv, gi, "brut", d(x.brut_bps), "net_bir", d(net), "tutma medyan", x.hold.median(), "max", x.hold.max(), "ort", round(x.hold.mean(), 1))
        for lo, hi in ((1, 1), (2, 3), (4, 7), (8, 999)):
            m = (x.hold >= lo) & (x.hold <= hi); print(f"   tutma {lo}-{hi}: {d(x.brut_bps[m])}")
        s2 = x[x.giris_tarihi >= "2024-11-10"]
        print("   SON2Y", d(s2.brut_bps), "net", d(s2.brut_bps - s2.c_bireysel), "isabet", (s2.brut_bps > 0).mean().round(2), "en kotu 3", np.sort(s2.brut_bps.values)[:3].round(0), "tutma max", s2.hold.max())
        kr = s2[(s2.giris_tarihi >= "2026-09-01")]; print("   2026-09+ islem", d(kr.brut_bps), "| bunlar olmadan SON2Y", d(s2[s2.giris_tarihi < "2026-09-01"].brut_bps))
        print("   SON2Y gun basina (toplam bps / takvim is gunu)", round(s2.brut_bps.sum() / 500, 2), "| pozisyonda gecen gun payi", round(s2.hold.sum() / 500, 2))
        # ortusme kontrolu
        ov = (x.giris_tarihi.values[1:] < x.cikis_tarihi.values[:-1]).sum(); print("   ortusen ardisik islem", ov)
        print("   yil:", x.groupby(x.giris_tarihi.dt.year).brut_bps.agg(["count", "mean"]).round(0).T.to_string())
        if gi == "E0": print(s2[["giris_tarihi", "cikis_tarihi", "yon", "hold", "brut_bps"]].to_string(index=False))
sec("E K2", E)
