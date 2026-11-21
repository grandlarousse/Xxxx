#!/usr/bin/env python3
"""K2 - Bagimsiz yeniden hesap ve curutme (01_backtest.py'ye bakilmadan yazildi).

Kullanim:  python3 02_bagimsiz_kontrol.py <veri_klasoru> [cikti.txt]
Tanimlar:
  r_t      = Close_t / Close_{t-1} - 1 (basit, duzeltilmis kapanis), ABD takvimi = UNG takvimi
  z_t      = r_t / sigma60_{t-1}  (60 gunluk std, t-1'e kadar)
  islem    = t kapanisinda al, t+h kapanisinda sat; islem getirisi = P_{t+h}/P_t - 1
  t ist.   = gunluk strateji P&L serisi (acik lot sayisi x gunluk getiri), Newey-West gecikme h
  IS       = 2011-10-06..2021-12-31, OOS = 2022-01-03..son
  Kis      = Kas-Mar (giris gunune gore)
"""
import sys
import numpy as np
import pandas as pd
from scipy import stats

D = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = sys.argv[2] if len(sys.argv) > 2 else None
_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    _lines.append(s)
    print(s)


IS0, IS1, OOS0 = pd.Timestamp("2011-10-06"), pd.Timestamp("2021-12-31"), pd.Timestamp("2022-01-03")
COST = {"UNG": 10, "BOIL": 15, "KOLD": 15}
rng = np.random.default_rng(20261121)


def load(t):
    df = pd.read_csv(f"{D}/d_{t}.csv", parse_dates=["Date"]).set_index("Date").sort_index()
    return df[~df.index.duplicated()]


ung = load("UNG")
CAL = ung.index
TICK = ["UNG", "BOIL", "KOLD", "UNL", "EQT", "AR", "RRC", "EXE", "CNX", "CRK", "GPOR", "LNG"]
px, op, vol = {}, {}, {}
for t in TICK:
    d = load(t).reindex(CAL)
    px[t], op[t], vol[t] = d["Close"], d["Open"], d["Volume"]
C = pd.DataFrame(px)
O = pd.DataFrame(op)
V = pd.DataFrame(vol)
R = C / C.shift(1) - 1
GAP = O / C.shift(1) - 1          # kapanis t-1 -> acilis t
INTRA = C / O - 1                 # acilis t -> kapanis t


def sig60(x):
    return x.rolling(60, min_periods=50).std().shift(1)


Z = R / sig60(R)
ZGAP = GAP / sig60(GAP)


def nw_t(x, lag):
    x = np.asarray(pd.Series(x).dropna(), float)
    n = len(x)
    if n < 5:
        return np.nan
    e = x - x.mean()
    g = e @ e / n
    for l in range(1, lag + 1):
        g += 2 * (1 - l / (lag + 1)) * (e[l:] @ e[:-l]) / n
    return x.mean() / np.sqrt(g / n) if g > 0 else np.nan


def per(idx, name):
    idx = pd.DatetimeIndex(idx)
    if name == "IS":
        return (idx >= IS0) & (idx <= IS1)
    if name == "OOS":
        return idx >= OOS0
    if name == "24-26":
        return idx >= pd.Timestamp("2024-01-01")
    if name == "ALL":
        return idx >= IS0
    if name == "1221":
        return (idx.year >= 2012) & (idx.year <= 2021)
    if name == "2226":
        return idx.year >= 2022
    raise ValueError(name)


def fwd(asset, h):
    """t kapanisinda alinan h gunluk islem getirisi."""
    return C[asset].shift(-h) / C[asset] - 1


def event_test(sig, asset, h, pname, cost=None):
    """sig: CAL uzerinde bool seri (t gunu kapanisinda giris). Donus: n, ort bps, t, net bps, isabet."""
    sig = sig.reindex(CAL).fillna(False).astype(bool)
    tr = fwd(asset, h)[sig]
    m = per(tr.index, pname)
    tr = tr[m].dropna()
    lots = sum(sig.shift(k).fillna(False).astype(int) for k in range(1, h + 1))
    pnl = (lots * R[asset]).where(R[asset].notna())
    pm = per(pnl.index, pname)
    t = nw_t(pnl[pm], h)
    c = COST.get(asset, 0) if cost is None else cost
    n = len(tr)
    mu = tr.mean() * 1e4 if n else np.nan
    return dict(n=n, mu=mu, t=t, net=mu - c, hit=(tr > 0).mean() if n else np.nan, tr=tr)


def fmt(r):
    return f"n={r['n']:4d} ort={r['mu']:7.1f} t={r['t']:5.2f} net={r['net']:7.1f} isabet={r['hit']:.2f}"


ALLD = pd.Series(True, index=CAL)
win = pd.Series(CAL.month.isin([11, 12, 1, 2, 3]), index=CAL)

# ---------------------------------------------------------------- A1
P("## A1 kosulsuz ortalama gunluk getiri (bps, NW t lag1)")
for pn in ["1221", "2226"]:
    for sn, s in [("tum", ALLD), ("kis", win), ("yaz", ~win)]:
        row = []
        for a in ["UNG", "BOIL", "KOLD"]:
            x = R[a][s & per(CAL, pn)].dropna()
            row.append(f"{a} {x.mean()*1e4:6.1f} ({nw_t(x,1):5.2f}) n={len(x)}")
        P(f"{pn} {sn}: " + " | ".join(row))

# ---------------------------------------------------------------- A2
P("## A2 erime: gercek h gunluk - (+/-2 x birikimli UNG h gunluk), ortusmeyen pencere, bps")
for pn in ["ALL", "IS", "OOS"]:
    for h in [1, 3]:
        out = []
        for a, k in [("BOIL", 2), ("KOLD", -2)]:
            ok = C[[a, "UNG"]].dropna().index
            ok = ok[ok >= IS0]
            sub = C.loc[ok]
            sub = sub.iloc[::h]
            ra = sub[a].pct_change().shift(-1)
            ru = sub["UNG"].pct_change().shift(-1)
            dif = (ra - k * ru).dropna()
            dif = dif[per(dif.index, pn)]
            out.append(f"{a} {dif.mean()*1e4:7.1f} (n={len(dif)}, t={stats.ttest_1samp(dif,0).statistic:5.2f})")
        P(f"{pn} h={h}: " + " | ".join(out))

for h in [3]:
    for a, k in [("BOIL", 2), ("KOLD", -2)]:
        sub0 = C.loc[C.index >= IS0, [a, "UNG"]].dropna()
        out = []
        for ph in range(h):
            sub = sub0.iloc[ph::h]
            dif = (sub[a].pct_change() - k * sub["UNG"].pct_change()).dropna()
            out.append(f"faz{ph} {dif.mean()*1e4:6.1f}")
        P(f"A2 faz duyarliligi ALL h={h} {a}: " + " ".join(out))

# ---------------------------------------------------------------- A3
P("## A3 UNG'ye ayni gun beta ve R2")
for t in ["EQT", "AR", "CRK", "EXE", "RRC", "CNX", "LNG", "BOIL", "KOLD"]:
    if t not in R:
        continue
    out = []
    for nm, sel in [("son250", R.index[-250:]), ("2022+", R.index[R.index >= OOS0])]:
        x = R.loc[sel, ["UNG", t]].dropna()
        b, a0, rr, _, _ = stats.linregress(x["UNG"], x[t])
        out.append(f"{nm} b={b:5.2f} R2={rr**2:.2f}")
    P(f"{t}: " + " | ".join(out))

# ---------------------------------------------------------------- A4
thu = pd.Series(CAL.dayofweek == 3, index=CAL)
P("## A4 KOLD Persembe getirisi (Car kapanis->Per kapanis), bps")
wed = thu.shift(-1).fillna(False).astype(bool)   # Persembe'den onceki islem gunu girisi
for pn in ["IS", "OOS", "24-26"]:
    P(f"{pn}: " + fmt(event_test(wed, "KOLD", 1, pn)))

# ---------------------------------------------------------------- A5
P("## A5 UNG gece bosluk z>+1 -> KOLD h=1")
for pn in ["IS", "OOS", "24-26"]:
    P(f"{pn}: " + fmt(event_test(ZGAP["UNG"] > 1, "KOLD", 1, pn)))

LGAP = np.log1p(GAP["UNG"]); ZLGAP = LGAP / sig60(LGAP)
for pn in ["IS", "OOS"]:
    P(f"A5 log-z duyarliligi {pn}: " + fmt(event_test(ZGAP["UNG"] > 1, "KOLD", 1, pn) if False else event_test(ZLGAP > 1, "KOLD", 1, pn)))
    m = per(CAL, pn)
    e = (ZGAP["UNG"] > 1).reindex(CAL).fillna(False)
    nx1 = fwd("KOLD", 1)
    P(f"A5 {pn} olay - kosulsuz KOLD ertesi gun farki: {(nx1[e & m].mean()-nx1[m].mean())*1e4:.1f} bps, Welch t={stats.ttest_ind(nx1[e&m].dropna(), nx1[~e&m].dropna(), equal_var=False).statistic:.2f}")

# ---------------------------------------------------------------- A6 TTF
ttf = load("TTF_F")
posv = (ttf["Volume"] > 0).rolling(60).mean()
start = posv[posv > 0.9].index.min()
tt = ttf.loc[start:].copy()
P(f"## A6 TTF baslangic {start.date()}, sonrasinda hacim=0 gun: {(tt['Volume']==0).sum()}")
tr_ttf = tt["Close"].pct_change()
z_ttf = (tr_ttf / sig60(tr_ttf)).clip(-4, 4)
ttf_sig = (z_ttf > 2).reindex(CAL).fillna(False).astype(bool)
for a in ["BOIL", "UNG"]:
    for pn in ["IS", "OOS"]:
        P(f"{a} h=3 {pn}: " + fmt(event_test(ttf_sig, a, 3, pn)))
ok90 = posv.reindex(tt.index) > 0.9
P(f"TTF hacim>0 orani(60g)<=%90 olan gun (baslangic sonrasi): {(~ok90).sum()}, yila gore " + str((~ok90).groupby(tt.index.year).sum().to_dict()))
lr_ttf = np.log(tt["Close"]).diff()
zl = lr_ttf / sig60(lr_ttf)
for nm, sg in [("yalniz hacim orani>%90 gunleri", (z_ttf > 2) & ok90), ("log-z", zl > 2), ("log-z + orani>%90", (zl > 2) & ok90)]:
    sg = sg.reindex(CAL).fillna(False).astype(bool)
    for a in ["UNG", "BOIL"]:
        P(f"A6 duyarlilik [{nm}] {a} h=3: IS " + fmt(event_test(sg, a, 3, "IS")) + " || OOS " + fmt(event_test(sg, a, 3, "OOS")))

# ---------------------------------------------------------------- A7
P("## A7 UNG z>+1 -> gaz ureticisi esit agirlik sepet h=1 (ham)")
base = ["EQT", "AR", "RRC", "CNX", "CRK"]
late = ["EXE", "GPOR"]
Rb = R[base + late].copy()
Rb.loc[Rb.index < "2021-01-01", late] = np.nan
basket = Rb.mean(axis=1)
C["SEPET"] = (1 + basket.fillna(0)).cumprod()
R["SEPET"] = basket
for pn in ["IS", "OOS", "24-26"]:
    P(f"{pn}: " + fmt(event_test(Z["UNG"] > 1, "SEPET", 1, pn, cost=0)))

# ---------------------------------------------------------------- A8
P("## A8 UNG z>+2 -> ertesi gun UNG (ve KOLD)")
for a in ["UNG", "KOLD"]:
    for pn in ["IS", "OOS", "24-26"]:
        P(f"{a} {pn}: " + fmt(event_test(Z["UNG"] > 2, a, 1, pn)))

LZ = np.log1p(R["UNG"]) / sig60(np.log1p(R["UNG"]))
for pn in ["IS", "OOS"]:
    P(f"A8 log-z duyarliligi UNG {pn}: " + fmt(event_test(LZ > 2, "UNG", 1, pn)))

# ================================================================= B1 EIA
P("## B1 EIA gunu takvimi")
hol = []
for y in range(2007, 2027):
    nov1 = pd.Timestamp(f"{y}-11-01")
    tg = nov1 + pd.Timedelta(days=(3 - nov1.dayofweek) % 7 + 21)
    for nm, d in [("Sukran", tg), ("Noel", pd.Timestamp(f"{y}-12-25")), ("Yilbasi", pd.Timestamp(f"{y}-01-01")),
                  ("4Temmuz", pd.Timestamp(f"{y}-07-04")), ("Juneteenth", pd.Timestamp(f"{y}-06-19")),
                  ("11Kasim", pd.Timestamp(f"{y}-11-11"))]:
        if nm == "Juneteenth" and y < 2021:
            continue
        if d.dayofweek == 3:
            hol.append((nm, d))
P("Persembe'ye denk gelen tatiller: " + ", ".join(f"{n} {d.date()}" for n, d in hol))
calS = pd.Series(np.arange(len(CAL)), index=CAL)
eia = pd.Series(CAL.dayofweek == 3, index=CAL)
shift_flag = pd.Series(False, index=CAL)   # kayma haftasi gunleri (Car ve Per)
for nm, d in hol:
    wd = d - pd.Timedelta(days=1)                       # varsayim: rapor Carsamba'ya kayar
    if d in eia.index:
        eia[d] = False
        shift_flag[d] = True
    if wd in eia.index:
        eia[wd] = True
        shift_flag[wd] = True
eia_dahil = eia.copy()
P(f"EIA gunu (dahil) sayisi 2007+: {eia_dahil.sum()}, kayma haftasi gunleri: {shift_flag.sum()}")


def diff_stats(r, e, mask):
    x = r[mask & e].dropna()
    y = r[mask & ~e].dropna()
    if len(x) < 3:
        return np.nan, np.nan, np.nan, np.nan, len(x)
    tt_ = stats.ttest_ind(x, y, equal_var=False).statistic
    return x.mean() * 1e4, y.mean() * 1e4, (x.mean() - y.mean()) * 1e4, tt_, len(x)


P("### yil yil: UNG EIA / diger / fark / t(fark) | KOLD fark t | BOIL fark t  (dahil; hariç fark parantezde UNG)")
yrs = CAL.year
for y in range(2007, 2027):
    m = pd.Series(yrs == y, index=CAL)
    a = diff_stats(R["UNG"], eia_dahil, m)
    ah = diff_stats(R["UNG"], eia_dahil, m & ~shift_flag)
    s = f"{y} UNG {a[0]:6.1f} {a[1]:6.1f} {a[2]:6.1f} {a[3]:5.2f} n={a[4]} (har {ah[2]:6.1f})"
    if y >= 2012:
        k = diff_stats(R["KOLD"], eia_dahil, m)
        b = diff_stats(R["BOIL"], eia_dahil, m)
        s += f" | KOLD {k[0]:6.1f} {k[2]:6.1f} {k[3]:5.2f} | BOIL {b[2]:6.1f} {b[3]:5.2f}"
    P(s)
P("### donem toplamlari (dahil / hariç)")
for lab, y0, y1 in [("2007-2018", 2007, 2018), ("2007-2013", 2007, 2013), ("2014-2018", 2014, 2018),
                    ("2019-2021", 2019, 2021), ("IS 2011-10..2021", 0, 0), ("2022-2026", 2022, 2026),
                    ("2024-2026", 2024, 2026)]:
    m = pd.Series(per(CAL, "IS") if y0 == 0 else (yrs >= y0) & (yrs <= y1), index=CAL)
    for a in ["UNG", "KOLD", "BOIL"]:
        if a != "UNG" and y0 and y0 < 2012:
            continue
        d1 = diff_stats(R[a], eia_dahil, m)
        d2 = diff_stats(R[a], eia_dahil, m & ~shift_flag)
        P(f"{lab} {a}: EIA {d1[0]:6.1f} diger {d1[1]:6.1f} fark {d1[2]:6.1f} t {d1[3]:5.2f} n={d1[4]} | har: fark {d2[2]:6.1f} t {d2[3]:5.2f}")

P("### haftanin gunleri (bps, t) IS / OOS")
for a in ["UNG", "KOLD", "BOIL"]:
    for pn in ["IS", "OOS"]:
        m = per(CAL, pn)
        row = []
        for dw, nm in enumerate(["Pzt", "Sal", "Car", "Per", "Cum"]):
            x = R[a][m & (CAL.dayofweek == dw)].dropna()
            row.append(f"{nm} {x.mean()*1e4:6.1f}({nw_t(x,1):4.1f})")
        P(f"{a} {pn}: " + " ".join(row))


def perm_test(a, nperm=2000):
    """Hafta ici etiket permutasyonu. Skor(d,s)=min(s*t_IS, s*t_OOS), t = gun d vs diger Welch."""
    r = R[a][CAL >= IS0].dropna()
    lab0 = r.index.dayofweek.values
    iso = r.index.isocalendar()
    wk = (iso["year"].values * 100 + iso["week"].values)
    isg = per(r.index, "IS")
    v = r.values

    def score(lab):
        best = -np.inf
        sc = {}
        for dw in range(5):
            ts = []
            for g in [isg, ~isg]:
                x = v[g & (lab == dw)]
                y = v[g & (lab != dw)]
                ts.append((x.mean() - y.mean()) / np.sqrt(x.var(ddof=1) / len(x) + y.var(ddof=1) / len(y)))
            for s in (1, -1):
                sc[(dw, s)] = min(s * ts[0], s * ts[1])
                best = max(best, sc[(dw, s)])
        return best, sc

    best_obs, sc_obs = score(lab0)
    idx = np.arange(len(v))
    mx = np.empty(nperm)
    for i in range(nperm):
        order = np.lexsort((rng.random(len(v)), wk))
        lab = np.empty_like(lab0)
        lab[order] = lab0[idx]
        mx[i] = score(lab)[0]
    s_thu = sc_obs[(3, 1 if a == "KOLD" else -1)]
    return s_thu, best_obs, (mx >= s_thu).mean(), (mx >= best_obs).mean(), sc_obs


for a in ["UNG", "KOLD"]:
    s_thu, best, p_thu, p_best, sc = perm_test(a)
    bd = max(sc, key=sc.get)
    P(f"permutasyon {a}: Persembe(KOLD yonu) skoru={s_thu:.2f}, en iyi={best:.2f} gun={bd[0]} yon={bd[1]}; "
      f"p(max>=Per)={p_thu:.3f}, p(max>=enIyi)={p_best:.3f}")

# saatlik ayristirma
P("### saatlik ayristirma 2023-12+ (bps; EIA gunu vs diger gunler, Welch t)")
for a in ["UNG", "KOLD", "BOIL"]:
    h = pd.read_csv(f"{D}/h_{a}.csv")
    h["dt"] = pd.to_datetime(h["Datetime"], utc=True).dt.tz_convert("America/New_York")
    h["d"] = h["dt"].dt.tz_localize(None).dt.normalize()
    h["hm"] = h["dt"].dt.strftime("%H:%M")
    g = {}
    for d, grp in h.groupby("d"):
        b = grp.set_index("hm")
        if not all(k in b.index for k in ["09:30", "10:30", "11:30", "15:30"]) or d not in C.index:
            continue
        f = C.loc[d, a] / b.loc["15:30", "Close"]
        g[d] = dict(o=b.loc["09:30", "Open"] * f, p1030=b.loc["09:30", "Close"] * f,
                    p1130=b.loc["10:30", "Close"] * f, p1130o=b.loc["11:30", "Open"] * f, c=C.loc[d, a])
    H = pd.DataFrame(g).T.sort_index()
    pc = C[a].shift(1).reindex(H.index)
    seg = pd.DataFrame({"gece": H.o / pc - 1, "0930-1030": H.p1030 / H.o - 1,
                        "1030-1130": H.p1130 / H.p1030 - 1, "1130-1600": H.c / H.p1130o - 1,
                        "toplam": H.c / pc - 1})
    e = eia_dahil.reindex(seg.index).fillna(False)
    row = []
    for col in seg:
        x, y = seg[col][e].dropna(), seg[col][~e].dropna()
        row.append(f"{col} {x.mean()*1e4:6.1f}/{y.mean()*1e4:5.1f} t={stats.ttest_ind(x,y,equal_var=False).statistic:5.2f}")
    P(f"{a} (nEIA={int(e.sum())}): " + " | ".join(row))

# islenebilir kural
P("### islenebilir kural: EIA'dan onceki kapanista KOLD al, EIA kapanisinda sat")
unl_ok = (V["UNL"] > 0) & (C["UNL"] != C["UNL"].shift(1))
dd = (R["UNG"] - R["UNL"]).where(unl_ok)
cnt = dd.rolling(20).count()
cont = (dd.rolling(20, min_periods=15).sum() < 0) & (cnt >= 15)
entry = eia_dahil.shift(-1).fillna(False).astype(bool)
trk = fwd("KOLD", 1)[entry].dropna()
trk = trk[trk.index >= IS0]


def rule_stats(tr, c):
    net = tr - c / 1e4
    if len(net) < 3:
        return f"n={len(net)}"
    eq = (1 + net).cumprod()
    mdd = (eq / eq.cummax() - 1).min()
    ys = net.groupby(net.index.year).sum()
    full = ys[[y for y in ys.index if y not in (2011,)]]
    return (f"n={len(net)} ort={net.mean()*1e4:6.1f} med={net.median()*1e4:6.1f} geo={(np.exp(np.log1p(net).mean())-1)*1e4:6.1f} t={stats.ttest_1samp(net,0).statistic:4.2f} isabet={(net>0).mean():.2f} yillik_toplam={full.mean()*100:6.1f}% "
            f"MDD={mdd*100:6.1f}% poz_yil={(full>0).mean():.2f}")


for c in [15, 30]:
    for lab, m in [("ALL", per(trk.index, "ALL")), ("IS", per(trk.index, "IS")), ("OOS", per(trk.index, "OOS")),
                   ("24-26", per(trk.index, "24-26"))]:
        P(f"c={c} {lab}: " + rule_stats(trk[m], c))
for lab, m in [("kis", trk.index.month.isin([11, 12, 1, 2, 3])), ("yaz", ~trk.index.month.isin([11, 12, 1, 2, 3])),
               ("contango", cont.reindex(trk.index).fillna(False).values),
               ("contango-degil", ~cont.reindex(trk.index).fillna(False).values)]:
    for pn in ["IS", "OOS"]:
        mm = m & per(trk.index, pn)
        P(f"c=15 {lab} {pn}: " + rule_stats(trk[mm], 15))
w5 = trk.sort_values().head(5)
P("en kotu 5 islem (giris tarihi, brut %): " + ", ".join(f"{d.date()} {v*100:.1f}" for d, v in w5.items()))
w5o = trk[trk.index >= OOS0].sort_values().head(5)
P("OOS en kotu 5: " + ", ".join(f"{d.date()} {v*100:.1f}" for d, v in w5o.items()))
# EIA'dan once giris yapilan ve EIA'nin kayma haftasi oldugu islemler haric
keep = ~shift_flag.shift(-1).fillna(False).astype(bool).reindex(trk.index).values
for pn in ["IS", "OOS"]:
    P(f"c=15 kayma haric {pn}: " + rule_stats(trk[keep & per(trk.index, pn)], 15))

# ================================================================= B2
P("## B2 yil yil KOLD/BOIL ortalama gunluk getiri bps (tum | kis | yaz)")
for y in range(2012, 2027):
    m = yrs == y
    s = f"{y}"
    for a in ["KOLD", "BOIL", "UNG"]:
        x = R[a][m]
        s += f" | {a} {x.mean()*1e4:6.1f} {x[win[m]].mean()*1e4:6.1f} {x[~win[m]].mean()*1e4:6.1f}"
    P(s)


def worst_nonoverlap(s, k, gap):
    s = s.dropna().sort_values()
    out = []
    for d, v in s.items():
        if all(abs(calS[d] - calS[o]) >= gap for o, _ in out):
            out.append((d, v))
        if len(out) == k:
            break
    return out


for a in ["KOLD", "BOIL"]:
    r1 = R[a][CAL >= IS0]
    r3 = (C[a] / C[a].shift(3) - 1)[CAL >= IS0]
    P(f"{a} en kotu 5 gun: " + ", ".join(f"{d.date()} {v*100:.1f}" for d, v in worst_nonoverlap(r1, 5, 1)))
    P(f"{a} en kotu 5 uc gun (bitis): " + ", ".join(f"{d.date()} {v*100:.1f}" for d, v in worst_nonoverlap(r3, 5, 3)))
    for pn in ["ALL", "OOS"]:
        x = r3[per(r3.index, pn)].dropna()
        ep = len(worst_nonoverlap(x[x <= -0.20], 10 ** 6, 3))
        P(f"{a} {pn} 3 gun <= -20%: gun orani={(x<=-0.20).mean()*100:.2f}% ayri olay={ep} yilda={ep/(len(x)/252):.2f}")

# ================================================================= B3
P("## B3 gece boslugu z>esik -> KOLD h=1; ertesi gun gece/gun ici parcasi; maliyet sonrasi")
nxt_gap = GAP["KOLD"].shift(-1)
nxt_in = INTRA["KOLD"].shift(-1)
for thr in [0.5, 1, 1.5, 2]:
    s = (ZGAP["UNG"] > thr)
    for pn in ["IS", "OOS", "24-26"]:
        r = event_test(s, "KOLD", 1, pn)
        mm = s & per(CAL, pn)
        P(f"esik {thr} {pn}: {fmt(r)} | gece {nxt_gap[mm].mean()*1e4:6.1f} gun_ici {nxt_in[mm].mean()*1e4:6.1f}")
s1 = ZGAP["UNG"] > 1
P("yil yil (esik 1): " + " ".join(
    f"{y}:{(fwd('KOLD',1)[s1 & (yrs==y)]).mean()*1e4:.0f}/{int((s1 & (yrs==y)).sum())}" for y in range(2012, 2027)))
s2 = Z["UNG"] > 2
both = (s1 & s2).sum()
P(f"ortusme: gap z>1 gunleri={int(s1[CAL>=IS0].sum())}, cc z>2 gunleri={int(s2[CAL>=IS0].sum())}, ikisi={int((s1&s2)[CAL>=IS0].sum())}")
only = s1 & ~s2 & ~(Z["UNG"] > 1)
for pn in ["IS", "OOS"]:
    P(f"gap z>1 ama cc z<=1 {pn}: " + fmt(event_test(only, "KOLD", 1, pn)))
    P(f"gap z>1 ve cc z>1 {pn}: " + fmt(event_test(s1 & (Z['UNG'] > 1), "KOLD", 1, pn)))

# ================================================================= B4
P("## B4 TTF z>+2 OOS olaylari: tarih TTF% UNG3g%")
ev = ttf_sig[ttf_sig & (CAL >= OOS0)].index
u3 = fwd("UNG", 3)
b3 = fwd("BOIL", 3)
ttf_us = tr_ttf.reindex(CAL)
P("; ".join(f"{d.date()} {ttf_us[d]*100:.0f} {u3[d]*100:.1f}" for d in ev))
for a in ["UNG", "BOIL"]:
    base_r = event_test(ttf_sig, a, 3, "OOS")
    P(f"{a} OOS tum: {fmt(base_r)}")
    tr = base_r["tr"]
    P(f"{a} bir yil disarida: " + " ".join(f"-{y}:{tr[tr.index.year!=y].mean()*1e4:.0f}(n{(tr.index.year!=y).sum()})"
                                          for y in sorted(set(tr.index.year))))
    P(f"{a} OOS medyan={tr.median()*1e4:.0f}, en buyuk olay cikinca ort={tr.sort_values().iloc[:-1].mean()*1e4:.0f}, en buyuk 2 cikinca={tr.sort_values().iloc[:-2].mean()*1e4:.0f}")
    ys = tr.groupby(tr.index.year).agg(["count", "sum"])
    P(f"{a} yil payi (n, toplam getiri payi): " + " ".join(
        f"{y}:{int(r['count'])},{r['sum']/tr.sum()*100:.0f}%" for y, r in ys.iterrows()))
for pn in ["IS", "OOS"]:
    sl = ttf_sig.shift(1).fillna(False).astype(bool)
    P(f"TTF 1 gun gecikmeli UNG h3 {pn}: " + fmt(event_test(sl, "UNG", 3, pn)))

# ================================================================= B5
P("## B5 UNG z>+2 -> ertesi gun UNG, yil yil (ort bps / n)")
nx = fwd("UNG", 1)
P(" ".join(f"{y}:{nx[s2 & (yrs==y)].mean()*1e4:.0f}/{int((s2&(yrs==y)).sum())}" for y in range(2007, 2027)))
x_is = nx[s2 & per(CAL, "IS")].dropna()
x_oos = nx[s2 & per(CAL, "OOS")].dropna()
x_pre = nx[s2 & (CAL < IS0)].dropna()
P(f"2007-2011.09: n={len(x_pre)} ort={x_pre.mean()*1e4:.1f}; IS n={len(x_is)} ort={x_is.mean()*1e4:.1f}; OOS n={len(x_oos)} ort={x_oos.mean()*1e4:.1f}")
P(f"IS-OOS farki Welch t={stats.ttest_ind(x_is,x_oos,equal_var=False).statistic:.2f}; OOS en kotu/iyi 3 cikarilinca ort: "
  f"{x_oos.sort_values().iloc[3:-3].mean()*1e4:.1f}; OOS medyan {x_oos.median()*1e4:.1f}")
for pn in ["IS", "OOS"]:
    m = per(CAL, pn)
    P(f"{pn}: z>2 gun orani={s2[m].mean()*100:.1f}%  UNG sigma60 medyan={sig60(R['UNG'])[m].median()*1e4:.0f} bps; "
      f"kosulsuz ertesi gun ort={nx[m].mean()*1e4:.1f}")
for lo, hi in [(1, 2), (2, 3), (3, 99)]:
    s = (Z["UNG"] > lo) & (Z["UNG"] <= hi)
    P(f"z in ({lo},{hi}] IS/OOS: " + fmt(event_test(s, "UNG", 1, "IS")) + " || " + fmt(event_test(s, "UNG", 1, "OOS")))

# ================================================================= B6
P("## B6 risk tablosu 2022+ (%): 1g sd p5 p1 min | 3g sd p5 p1 min")
for t in ["UNG", "BOIL", "KOLD", "EQT", "CRK", "AR", "EXE"]:
    r1 = R[t][CAL >= OOS0].dropna()
    r3 = (C[t] / C[t].shift(3) - 1)[CAL >= OOS0].dropna()
    q = lambda x: f"{x.std()*100:5.2f} {x.quantile(.05)*100:6.2f} {x.quantile(.01)*100:6.2f} {x.min()*100:6.2f}"
    P(f"{t}: {q(r1)} | {q(r3)}")
P("gece payi 2022+: var(gece)/var(kapanis-kapanis) ve var(gece)/(var(gece)+var(gun ici))")
for t in ["UNG", "BOIL", "KOLD"]:
    m = CAL >= OOS0
    g, i_, c_ = GAP[t][m].dropna(), INTRA[t][m].dropna(), R[t][m].dropna()
    lg, li = np.log1p(g), np.log1p(i_)
    P(f"{t}: {g.var()/c_.var()*100:.0f}% | {lg.var()/(lg.var()+li.var())*100:.0f}% | sd gece {g.std()*100:.2f}% gun ici {i_.std()*100:.2f}%")

if OUT:
    open(OUT, "w").write("\n".join(_lines) + "\n")
