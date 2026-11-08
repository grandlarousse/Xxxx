"""Bağımsız denetim: sinyal_altin.py --panel çıktısını, betiğin kodunu kullanmadan panel parquet'lerinden kurulan
kendi hesabımla 40 rastgele (+ birkaç uç) günde karşılaştırır. Kurallar hakem tablosu (sinyal_tablosu.csv) metninden."""
import json, os, subprocess, sys, random
import numpy as np, pandas as pd
import exchange_calendars as xc

S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
SCRIPT = f"{S}/out/sentez/sinyal_altin.py"
TMP = f"{S}/denetim_sinyal/json"; os.makedirs(TMP, exist_ok=True)
V = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); V.index = pd.to_datetime(V.index).normalize()
SP = pd.read_parquet(f"{S}/panel/panel_spot.parquet"); SP.index = pd.to_datetime(SP.index).normalize()
E = pd.read_parquet(f"{S}/panel/panel_etf.parquet"); E.index = pd.to_datetime(E.index).normalize()

# --- Türkiye yarım günleri: bağımsız olarak, BIST'in bilinen arife kuralından değil, a1 rep dosyasından ve
#     veri notundan (arife + 28 Ekim). 28 Ekim hafta içi ise yarım gün.
half = set(pd.to_datetime(pd.read_csv(f"{S}/out/a1_zaman_serisi_rep/half_days.csv", header=None)[0].iloc[1:].values))
for y in range(2017, 2027):
    d = pd.Timestamp(y, 10, 28)
    if d.weekday() < 5 and d in V.index: half.add(d)
HALF_TR = pd.DatetimeIndex(sorted(half))

cal = xc.get_calendar("XNYS", start="2007-06-01", end="2027-12-31")
sch = cal.schedule
HALF_US = set(pd.DatetimeIndex(sch.index[sch["close"].dt.tz_convert("America/New_York").dt.hour < 16]).tz_localize(None))
SES = pd.DatetimeIndex(cal.sessions).tz_localize(None)

# ============================== VİOP ==============================
lp = np.log(SP.s_p15.astype(float))
rv = lp.diff().rolling(20).std()
vals = rv.values
q = np.full(len(vals), np.nan)
fin = []
for i, v in enumerate(vals):
    if np.isfinite(v):
        fin.append(v)
        if len(fin) >= 250:
            a = np.asarray(fin); q[i] = np.mean(a <= v)
q = pd.Series(q, index=SP.index)
x5 = lp - lp.shift(5)
low_spot = pd.Series(np.where(q < 1 / 3, np.sign(x5), 0.0), index=SP.index).where(q.notna() & x5.notna())


def to_v(s):
    out = []
    for d in V.index:
        j = s.index.searchsorted(d, side="right") - 1
        out.append(s.iloc[j] if j >= 0 else np.nan)
    return pd.Series(out, index=V.index)


low_pos = to_v(low_spot).fillna(0.0)
low_pos[low_pos.index.isin(HALF_TR)] = 0.0
low_q = to_v(q); low_x = to_v(x5)

# QEND
qend = pd.Series(0.0, index=V.index)
for (y, m), g in pd.Series(V.index, index=V.index).groupby([V.index.year, V.index.month]):
    if m in (3, 6, 9, 12) and len(g) >= 2: qend[g.index[-2]] = 1.0

# A4-C1 (VİOP satırlarında, karar anında bilinen son ABD kapanışı: panel y_*)
rm = np.log(V.y_GDXJ.astype(float)).diff(); rg = np.log(V.y_GLD.astype(float)).diff()
beta = (rm.rolling(60, min_periods=40).cov(rg) / rg.rolling(60, min_periods=40).var()).shift(1)
ea = rm - beta * rg
za = ea / ea.rolling(120, min_periods=60).std().shift(1)
a4_pos = pd.Series(np.where(za.abs() > 0.43, np.sign(za), 0.0), index=V.index).where(za.notna(), 0.0)

# A8-3
x8 = np.log(V.xau_p15.astype(float) / V.xau_p14.astype(float))
a8_pos = np.sign(x8).fillna(0.0)
a8_pos[a8_pos.index.isin(HALF_TR)] = 0.0


def eff(p, h):
    p = p.fillna(0.0)
    return sum(p.shift(k).fillna(0.0) for k in range(h)) / h


VIOP = dict(
    lowmom=dict(pos=low_pos, eff=eff(low_pos, 1), eff5=eff(low_pos, 5)),
    qend=dict(pos=qend, eff=eff(qend, 3)),
    a4=dict(pos=a4_pos, eff=eff(a4_pos, 3), z=za),
    a8=dict(pos=a8_pos, eff=eff(a8_pos, 5), x=x8),
)
V_COMB = (VIOP["lowmom"]["eff"] + VIOP["qend"]["eff"] + VIOP["a4"]["eff"] + VIOP["a8"]["eff"]) / 4

# ============================== ETF ==============================
def lret(t):
    c = E[f"c_{t}"].astype(float); r = np.log(c).diff(); r[c.isna() | c.shift(1).isna()] = np.nan; return r


R = {t: lret(t) for t in ("GLD", "GDX", "GDXJ", "SPY", "PHYS", "CEF", "SLV")}


def resid_all(y):
    Y = R[y].values; X = np.column_stack([R["GLD"].values, R["SPY"].values]); n = len(Y)
    e = np.full(n, np.nan)
    for i in range(1, n):
        lo = max(0, i - 250); yy = Y[lo:i]; xx = X[lo:i]
        m = np.isfinite(yy) & np.isfinite(xx).all(1)
        if m.sum() < 60 or not np.isfinite(Y[i]) or not np.isfinite(X[i]).all(): continue
        A = np.column_stack([np.ones(m.sum()), xx[m]]); b = np.linalg.lstsq(A, yy[m], rcond=None)[0]
        e[i] = Y[i] - b[1] * X[i, 0] - b[2] * X[i, 1]
    return pd.Series(e, index=E.index)


EP = {}
res = {y: resid_all(y) for y in ("GDXJ", "GDX")}
for nm, y, k, h, qq in (("c2j", "GDXJ", 1, 3, 0.7), ("c2", "GDX", 3, 3, 0.7), ("c1", "GDX", 10, 5, 0.8)):
    xk = res[y].rolling(k, min_periods=k).sum().shift(1)
    xi = xk[xk.index <= "2017-12-31"].dropna()
    hi, lo = xi.quantile(qq), xi.quantile(1 - qq)
    p = (xk > hi).astype(float).where(xk.notna(), 0.0)
    EP[nm] = dict(x=xk, hi=hi, lo=lo, pos=p, eff=eff(p, h), kap=pd.Series(np.where(xk < lo, 0.0, 1.0), index=E.index))
    print(f"eşik {nm}: hi {hi:.10f} lo {lo:.10f}")

# E1-C2 (NYSE düzenli tatilleri, hafta içi)
hol = pd.DatetimeIndex(cal.regular_holidays.holidays(start="2007-06-01", end="2027-12-31"))
e1 = pd.Series(0.0, index=SES)
for hd in hol:
    if hd.weekday() >= 5: continue
    prev = SES[SES < hd]
    if len(prev) < 2: continue
    e1[prev[-2]] = 1.0
EP["e1"] = dict(pos=e1, eff=e1)

# E3-1
mm = np.log(E.xau_cut.astype(float)) - np.log(E.xau_close.astype(float).shift(1))
p31 = (mm < 0).astype(float).where(mm.notna(), 0.0)
p31[p31.index.isin(HALF_US)] = 0.0
EP["e31"] = dict(pos=p31, eff=p31, m=mm)

# E3-3 / E3-4: karar günü t için z_{t-1}
lvl = np.log(E.c_PHYS.astype(float) / E.c_GLD.astype(float))
dev = lvl - lvl.rolling(60, min_periods=30).median()
z33 = (dev / dev.rolling(250, min_periods=120).std()).shift(1)
dd = pd.concat([R["CEF"].rename("y"), R["GLD"].rename("g"), R["SLV"].rename("s")], axis=1).dropna()
Yv = dd.y.values; XX = np.column_stack([np.ones(len(dd)), dd[["g", "s"]].values]); eC = np.full(len(dd), np.nan)
for i in range(250, len(dd)):
    b = np.linalg.lstsq(XX[i - 250:i], Yv[i - 250:i], rcond=None)[0]; eC[i] = Yv[i] - XX[i, 1:] @ b[1:]
eC = pd.Series(eC, index=dd.index).reindex(E.index)
lc = eC.fillna(0).cumsum().where(eC.notna())
devc = lc - lc.rolling(60, min_periods=30).median()
z34 = (devc / devc.rolling(250, min_periods=120).std()).shift(1)
E_W = {"E1-C2_GDX_tatil_oncesi": ("GDX", "e1"), "E2-C2j_GDXJ_artik_h3": ("GDXJ", "c2j"), "E2-C2_GDX_artik_h3": ("GDX", "c2"),
       "E2-C1_madenci_oncu_GLD_h5": ("GLD", "c1"), "E3-1_altin_gunici_GDXJ_donus": ("GDXJ", "e31")}

# ============================== gün seçimi ==============================
random.seed(20261108)
vd = [d for d in V.index if d >= pd.Timestamp("2018-01-01")]
ed = [d for d in E.index if d >= pd.Timestamp("2009-06-01")]
pick = set(random.sample(vd, 22)) | set(random.sample(ed, 18))
# uç günler: TR yarım günü, ABD yarım günü, QEND girişi, tatil öncesi giriş, spotun olmadığı gün, son gün
extra = [pd.Timestamp(x) for x in ("2025-10-28", "2024-04-09", "2025-11-28", "2024-12-24", "2025-12-29", "2026-09-28", "2025-12-23",
                                    "2024-12-25", "2026-04-03", "2026-11-06", "2023-07-03", "2026-03-19", "2026-05-26")]
days = sorted(pick | set(extra))
print("gün sayısı:", len(days))

rows = []


def add(d, sid, alan, betik, ben, tol=1e-9):
    ok = (betik is None and (ben is None or not np.isfinite(ben))) or (betik is not None and ben is not None and np.isfinite(ben) and abs(float(betik) - float(ben)) <= tol)
    rows.append(dict(gun=str(d.date()), sinyal=sid, alan=alan, betik=betik, bagimsiz=None if ben is None else float(ben), ok=bool(ok)))


for d in days:
    fn = f"{TMP}/{d.date()}.json"
    subprocess.run([sys.executable, "-W", "ignore", SCRIPT, "--panel", "--tarih", str(d.date()), "--json", fn, "--sessiz"], check=True, capture_output=True)
    J = json.load(open(fn))
    v = J["viop"]
    if not v.get("kapali") and pd.Timestamp(v["tarih"]) in V.index:
        tv = pd.Timestamp(v["tarih"])
        sg = {s["id"]: s for s in v["sinyaller"]}
        for sid, key in (("A1-LOWMOM-h1", "lowmom"), ("A3_QEND_h3", "qend"), ("A4-C1_GDXJ_artik_h3", "a4"), ("A8-3_seg_last1h_h5", "a8")):
            s = sg[sid]; T = VIOP[key]
            if tv not in V.index: continue
            i = V.index.get_loc(tv)
            add(tv, sid, "etkin", s["etkin"], T["eff"].iloc[i])
            add(tv, sid, "etkin_onceki", s["etkin_onceki"], T["eff"].iloc[i - 1] if i >= 1 else 0.0)
            if not str(s["durum"]).startswith("DEVRE"):
                add(tv, sid, "yeni_dilim", s["yeni_dilim"], T["pos"].iloc[i])
            if key == "lowmom" and s["ek"].get("q") is not None:
                add(tv, sid, "q", s["ek"]["q"], low_q.iloc[i], 1e-12); add(tv, sid, "x5", s["ek"]["x5"], low_x.iloc[i], 1e-12)
                add(tv, sid, "h5_etkin", s["ek"]["h5"]["etkin"], T["eff5"].iloc[i])
            if key == "a4" and s["deger"] is not None:
                add(tv, sid, "z", s["deger"], za.iloc[i], 1e-6)
            if key == "a8" and s["deger"] is not None:
                add(tv, sid, "x", s["deger"], x8.iloc[i], 1e-12)
        add(tv, "VIOP_birlesik", "etkin", v["birlesik"]["etkin"], V_COMB.loc[tv])
    e = J["etf"]
    if not e.get("kapali"):
        te = pd.Timestamp(e["tarih"])
        sg = {s["id"]: s for s in e["sinyaller"]}
        if te not in E.index: continue
        i = E.index.get_loc(te)
        agg = {}
        for sid, (arac, key) in E_W.items():
            s = sg[sid]; T = EP[key]
            ef = T["eff"].reindex(E.index).fillna(0.0) if key == "e1" else T["eff"]
            pz = T["pos"].reindex(E.index).fillna(0.0) if key == "e1" else T["pos"]
            add(te, sid, "etkin", s["etkin"], ef.iloc[i])
            add(te, sid, "etkin_onceki", s["etkin_onceki"], ef.iloc[i - 1])
            if not str(s["durum"]).startswith("DEVRE"): add(te, sid, "yeni_dilim", s["yeni_dilim"], pz.iloc[i])
            if key in ("c2j", "c2", "c1") and s["deger"] is not None: add(te, sid, "x", s["deger"], T["x"].iloc[i], 1e-9)
            if key == "c1" and s["ek"].get("kaplama_poz") is not None:
                add(te, sid, "kaplama", s["ek"]["kaplama_poz"], T["kap"].iloc[i])
                ke = eff(T["kap"].where(T["x"].notna(), 1.0), 5)
                if "kaplama_etkin" in s["ek"]:
                    add(te, sid, "kaplama_etkin", s["ek"]["kaplama_etkin"], ke.iloc[i]); add(te, sid, "kaplama_etkin_onceki", s["ek"]["kaplama_etkin_onceki"], ke.iloc[i - 1])
            if key == "e31" and s["deger"] is not None: add(te, sid, "m", s["deger"], mm.iloc[i], 1e-12)
            agg[arac] = agg.get(arac, 0.0) + ef.iloc[i] / 5
        for a, w in agg.items(): add(te, "ETF_birlesik", a, e["birlesik"]["agirlik"].get(a, 0.0), w)
        add(te, "E3-3_PHYS_GLD_iskonto", "z", sg["E3-3_PHYS_GLD_iskonto"]["deger"], z33.iloc[i], 1e-6)
        add(te, "E3-4_CEF_artik", "z", sg["E3-4_CEF_artik"]["deger"], z34.iloc[i], 1e-6)

D = pd.DataFrame(rows)
D.to_csv(f"{S}/denetim_sinyal/karsilastirma.csv", index=False)
print("toplam karşılaştırma:", len(D), "fark:", int((~D.ok).sum()))
print(D[~D.ok].to_string())
print("VİOP günleri:", D[D.sinyal.str.startswith(("A", "VIOP"))].gun.nunique(), "ETF günleri:", D[D.sinyal.str.startswith(("E", "ETF"))].gun.nunique())
