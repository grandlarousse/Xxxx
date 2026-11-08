"""s2: Göreli değer öngörücüleri → VİOP fwd1/3/5.
 (A) Madenci/altın: oran değişimi Δw log(M/GLD) ve beta-artığı e = r_M − β60·r_GLD (β geçmiş-yalnız), w=1,5; büyük artık olayları.
 (B) Altın/gümüş oranı (15:00 UTC spot, xau_p15/dk_XAGUSD_p15) z-skoru (pencere 20/60/120/250) ve Δ1/Δ5.
 (C) Reel faiz + dolar seviye modelinden sapma: log altın ~ reel10 + log DXY, yuvarlanan W=120/250/500 (yalnız geçmiş + bugün bilinen).
     İki sürüm: (i) t-1 ABD kapanışı (y_GC_F, y_DX_Y_NYB, ust_real10); (ii) 15:00 UTC (xau_p15, dk_DOLLARIDXUSD_p15, ust_real10 t-1).
     Değişim modeli: r_altın − (b Δreal + c Δlog DXY), β120 geçmiş-yalnız; 1 ve 5 günlük toplam.
 (D) GLD hacim şoku: log hacim − önceki 20 gün ortalaması (GLD gün D kapanışı, D 20/21 UTC → t'de bilinir); işaretli (× sign r_GLD).
Bilgi zamanı: madenci/GLD/GC_F/DXY = t-1 ABD kapanışı (≤21:00 UTC t-1); reel10 = t-1 22:00 UTC; xau_p15, dk_*_p15 = t 15:00 UTC."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz")
from a4_common import *

reg_reset("s2_")
d = load_viop()
rows = []

def run(fam, tid, name, x, hs=(1, 3, 5), note=""):
    for h in hs:
        y = d[f"fwd{h}"]
        s = split_stats(x, y, h)
        reg(fam, f"{tid}_h{h}", name, h, s, note)
        rows.append(dict(fam=fam, test=tid, pred=name, h=h, ic=s["ic"], t=s["t"], t_is=s["t_is"], t_oos=s["t_oos"], ic_oos=s["ic_oos"], yrs=f"{s['yrs_same_sign']}/{s['yrs']}", n=s["n"]))

def run_ev(fam, tid, name, dm, hs=(1, 3, 5), note=""):
    for h in hs:
        e = event_stats(dm, d[f"fwd{h}"], h)
        reg(fam, f"{tid}_h{h}", name, h, e, note + "; ic=ortalama fark bps")
        rows.append(dict(fam=fam, test=tid, pred=name, h=h, ic=e["ic"], t=e["t"], t_is=e["t_is"], t_oos=e["t_oos"], ic_oos=e["ic_oos"], yrs=f"{e['yrs_same_sign']}/{e['yrs']}", n=e["n"]))

# ---------- (A) madenci / altın ----------
lg = np.log(d["y_GLD"]); rg = lg.diff()
basket_names = ["y_NEM", "y_AEM", "y_B", "y_KGC", "y_FNV", "y_WPM", "y_RGLD"]
rb = np.log(d[basket_names]).diff().mean(axis=1)
miners = {"y_GDX": np.log(d["y_GDX"]).diff(), "y_GDXJ": np.log(d["y_GDXJ"]).diff(), "y_RING": np.log(d["y_RING"]).diff(),
          "y_SIL": np.log(d["y_SIL"]).diff(), "sepet7": rb}
for m, rm in miners.items():
    for w in (1, 5):
        ratio = (rm - rg).rolling(w).sum()
        run("s2_madenci_oran", f"s2_oran_{m}_w{w}", f"z(d{w} log({m}/GLD))", zscale(ratio), note="t-1 ABD kapanisi")
    beta = rm.rolling(60, min_periods=40).cov(rg).shift(1) / rg.rolling(60, min_periods=40).var().shift(1)
    e = rm - beta * rg
    for w in (1, 5):
        ew = zscale(e.rolling(w).sum())
        run("s2_madenci_artik", f"s2_artik_{m}_w{w}", f"z(sum{w} e[{m}|GLD,b60])", ew, note="t-1 ABD kapanisi")
    ez = zscale(e)
    run_ev("s2_madenci_buyuk", f"s2_artikup_{m}", f"1[z(e {m})>1.5]", (ez > 1.5).astype(float).where(ez.notna()))
    run_ev("s2_madenci_buyuk", f"s2_artikdn_{m}", f"1[z(e {m})<-1.5]", (ez < -1.5).astype(float).where(ez.notna()))

# ---------- (B) altın / gümüş oranı ----------
gsr = np.log(d["xau_p15"] / d["dk_XAGUSD_p15"])
for W in (20, 60, 120, 250):
    z = (gsr - gsr.rolling(W, min_periods=int(W * 0.7)).mean()) / gsr.rolling(W, min_periods=int(W * 0.7)).std()
    run("s2_gsr_z", f"s2_gsrz_W{W}", f"z_{W}(log XAU/XAG, 15:00 UTC)", z, note="t 15:00 UTC")
for w in (1, 5):
    run("s2_gsr_d", f"s2_gsrd_w{w}", f"z(d{w} log XAU/XAG 15:00)", zscale(gsr.diff(w)), note="t 15:00 UTC")

# ---------- (C) reel faiz + dolar modeli ----------
def roll_resid(yv, X, W):
    """Katsayılar YALNIZ geçmişten: [t-W, t-1] penceresinde OLS; artık_t = y_t − X_t·b (pencere dışı), z = artık_t / pencere-içi artık std."""
    dd = pd.concat([yv.rename("y"), X], axis=1).dropna()
    Y = dd["y"].values; XX = np.column_stack([np.ones(len(dd)), dd.drop(columns="y").values])
    res = np.full(len(dd), np.nan); rz = np.full(len(dd), np.nan)
    for i in range(W, len(dd)):
        sl = slice(i - W, i)
        b, *_ = np.linalg.lstsq(XX[sl], Y[sl], rcond=None)
        e = Y[sl] - XX[sl] @ b
        res[i] = Y[i] - XX[i] @ b; rz[i] = res[i] / e.std()
    return pd.Series(res, index=dd.index), pd.Series(rz, index=dd.index)

lvl_us = dict(y=np.log(d["y_GC_F"]), X=pd.DataFrame({"r10": d["ust_real10"], "ldx": np.log(d["y_DX_Y_NYB"])}))
lvl_15 = dict(y=np.log(d["xau_p15"]), X=pd.DataFrame({"r10": d["ust_real10"], "ldx": np.log(d["dk_DOLLARIDXUSD_p15"])}))
for ver, L in (("abd", lvl_us), ("p15", lvl_15)):
    for W in (120, 250, 500):
        res, rz = roll_resid(L["y"], L["X"], W)
        res.to_frame("res").assign(rz=rz).to_parquet(f"{OUT}/s2_model_artik_{ver}_W{W}.parquet")
        run("s2_reelmodel_seviye", f"s2_lvl_{ver}_W{W}", f"artikz(log altin ~ reel10 + log DXY; {ver}, W{W})", rz.reindex(d.index), note=ver)

# değişim modeli (15:00 sürümü: altın 15:00->15:00, DXY 15:00->15:00, reel10 t-1 değişimi)
ra = np.log(d["xau_p15"]).diff(); dxr = np.log(d["dk_DOLLARIDXUSD_p15"]).diff(); drr = d["ust_real10"].diff()
Xc = pd.DataFrame({"dr": drr, "dx": dxr})
dd = pd.concat([ra.rename("y"), Xc], axis=1)
cov = lambda a, b: a.rolling(120, min_periods=80).cov(b).shift(1)
# çoklu beta: 2x2 sistem, geçmiş-yalnız
vr = drr.rolling(120, min_periods=80).var().shift(1); vx = dxr.rolling(120, min_periods=80).var().shift(1); cxr = cov(drr, dxr)
cyr = cov(ra, drr); cyx = cov(ra, dxr)
det = vr * vx - cxr ** 2
br = (cyr * vx - cyx * cxr) / det; bx = (cyx * vr - cyr * cxr) / det
ech = ra - br * drr - bx * dxr
for w in (1, 5):
    run("s2_reelmodel_degisim", f"s2_chg_w{w}", f"z(sum{w} [r_altin - b dreal - c dlogDXY], b120)", zscale(ech.rolling(w).sum()), note="15:00 UTC")

# ---------- (D) GLD hacim şoku ----------
g = pd.read_parquet(f"{P}/yahoo/GLD.parquet"); g.index = pd.to_datetime(g.index)
lv = np.log(g["volume"].where(g["volume"] > 0))
vs = lv - lv.rolling(20, min_periods=15).mean().shift(1)
vs_z = vs / vs.rolling(250, min_periods=120).std().shift(1)
gr = np.log(g["adjclose"]).diff()
avail_day = pd.to_datetime(d["y_GLD_avail"]).dt.normalize()   # GLD kapanış günü D (avail = D 20/21 UTC < t 15:00)
assert (pd.to_datetime(d["y_GLD_avail"]) < d.index + pd.Timedelta(hours=15)).all()
vsp = pd.Series(vs_z.reindex(avail_day).values, index=d.index)
sgn = pd.Series(np.sign(gr.reindex(avail_day).values), index=d.index)
# aynı kapanış tekrarlanan günlerde (tatil) şok yinelenir: yalnız yeni kapanış günlerinde kullan
newbar = avail_day != avail_day.shift(1)
vsp = vsp.where(newbar); sgn = sgn.where(newbar)
run("s2_gld_hacim", "s2_vol", "z(GLD log hacim - ort20)", vsp, note="t-1 ABD kapanisi")
run("s2_gld_hacim", "s2_volsgn", "z(GLD hacim sok) x sign(r_GLD)", vsp * sgn, note="t-1 ABD kapanisi")
run_ev("s2_gld_hacim_buyuk", "s2_volup", "1[hacim z>2 & r_GLD>0]", ((vsp > 2) & (sgn > 0)).astype(float).where(vsp.notna()))
run_ev("s2_gld_hacim_buyuk", "s2_voldn", "1[hacim z>2 & r_GLD<0]", ((vsp > 2) & (sgn < 0)).astype(float).where(vsp.notna()))

res = pd.DataFrame(rows); res.to_csv(f"{OUT}/s2_goreli_deger.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
print("test sayısı:", len(res))
print(res.round(3).to_string())
