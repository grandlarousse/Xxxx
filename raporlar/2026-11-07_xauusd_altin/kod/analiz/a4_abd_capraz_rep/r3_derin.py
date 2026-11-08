"""r3: Derin kontroller — (1) Yahoo tarih/zaman hizası ampirik doğrulama (Dukascopy saatlik ile), (2) C1 duyarlılık: ABD takvimi getirisi, eşik, h, alt dönem,
ileri gün profili, piyasa-betası arındırılmış alfa, blok bootstrap OOS Sharpe GA, roll maliyeti, (3) D1 zaman çakışması, (4) kayıt FDR yeniden hesabı."""
import sys, json, glob, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
OUT = f"{S}/out/a4_abd_capraz_rep"; P = f"{S}/panel"
sys.path.insert(0, OUT)
from rep_util import *
d = pd.read_parquet(f"{OUT}/r1_viop.parquet"); idx = d.index; ISM = idx <= IS_END; OOSM = ~ISM
lg = open(f"{OUT}/r3_log.txt", "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s); lg.write(s + "\n")
def zsc(r, win=120, minp=60): return r / r.rolling(win, min_periods=minp).std().shift(1)
def beta(a, b, win, minp): return (a.rolling(win, min_periods=minp).cov(b) / b.rolling(win, min_periods=minp).var()).shift(1)

# ---------- (1) Yahoo kapanış anı ampirik ----------
def duka_hourly_close(sym):
    h = pd.read_parquet(f"{P}/duka/{sym}.parquet")
    c = pd.Series(h["c"].values, index=h.index.tz_convert("UTC").tz_localize(None) + pd.Timedelta(hours=1))
    return c
def yahoo(tk):
    y = pd.read_parquet(f"{P}/yahoo/{tk}.parquet"); y.index = pd.to_datetime(y.index); return y.adjclose
say("== (1) Yahoo günlük getirisinin Dukascopy saatlik getirisiyle korelasyonu (aynı gün D, HH:00 UTC → önceki işlem günü HH:00) ==")
for tk, sym in (("GLD", "XAUUSD"), ("GDXJ", "XAUUSD"), ("DX-Y.NYB", "DOLLARIDXUSD")):
    yr = np.log(yahoo(tk)).diff(); yr = yr[yr.index >= "2018-01-01"]
    c = duka_hourly_close(sym)
    row = {}
    for HH in (14, 16, 18, 19, 20, 21, 22, 23):
        p = c[c.index.hour == HH]; p.index = p.index.normalize(); p = p[~p.index.duplicated()]
        p = p.reindex(yr.index)
        rr = np.log(p).diff()
        row[HH] = round(float(yr.corr(rr)), 3)
    # bir gün kaydırılmış
    p = c[c.index.hour == 21]; p.index = p.index.normalize(); p = p[~p.index.duplicated()].reindex(yr.index)
    row["D+1_21"] = round(float(yr.corr(np.log(p).diff().shift(-1))), 3); row["D-1_21"] = round(float(yr.corr(np.log(p).diff().shift(1))), 3)
    say(f"  {tk} vs duka {sym}: {row}")
# DXY: yaz/kış ayrı (ET kapanış 17:00 → yaz 21:00, kış 22:00 UTC)
yr = np.log(yahoo("DX-Y.NYB")).diff(); yr = yr[yr.index >= "2018-01-01"]
c = duka_hourly_close("DOLLARIDXUSD")
dst = pd.Series(yr.index.tz_localize("America/New_York").map(lambda x: bool(x.dst())), index=yr.index)
for HH in (19, 20, 21, 22, 23):
    p = c[c.index.hour == HH]; p.index = p.index.normalize(); p = p[~p.index.duplicated()].reindex(yr.index); rr = np.log(p).diff()
    say(f"  DXY HH={HH}: yaz corr={yr[dst].corr(rr[dst]):.3f}  kış corr={yr[~dst].corr(rr[~dst]):.3f}")
for HH in (19, 20, 21, 22):
    p = duka_hourly_close("XAUUSD"); p = p[p.index.hour == HH]; p.index = p.index.normalize(); p = p[~p.index.duplicated()].reindex(yr.index)
    g = np.log(yahoo("GLD")).diff().reindex(yr.index); rr = np.log(p).diff()
    say(f"  GLD HH={HH}: yaz corr={g[dst].corr(rr[dst]):.3f}  kış corr={g[~dst].corr(rr[~dst]):.3f}")

# ---------- (2) C1 duyarlılık ----------
say("\n== (2) C1 duyarlılık ==")
rm = np.log(d.y_GDXJ).diff(); rg = np.log(d.y_GLD).diff()
z = zsc(rm - beta(rm, rg, 60, 40) * rg)
pos = np.sign(z).where(z.abs() > 0.43, 0.0).fillna(0)
# (a) ABD takvimi: getiriler Yahoo ABD günlerinde, sonra as-of VİOP gününe (tatil sonrası tekrar eden değer yerine son ABD günü değeri)
gj = np.log(yahoo("GDXJ")).diff(); gl = np.log(yahoo("GLD")).diff()
ee = gj - beta(gj, gl, 60, 40) * gl; zu = zsc(ee).rename("zu")
m = pd.merge_asof(pd.DataFrame({"t": idx}), zu.reset_index().rename(columns={"date": "D"}).assign(cl=lambda x: x.D + pd.Timedelta(hours=21)).sort_values("cl"),
                  left_on=pd.Series(idx + pd.Timedelta(hours=15)), right_on="cl", allow_exact_matches=False)
zU = pd.Series(m["zu"].values, index=idx)
# tekrar eden (bayat) değerler: ABD tatili → aynı D iki VİOP gününe düşer → ikinci kez sayma
Dm = pd.Series(m["D"].values, index=idx); zU_nodup = zU.where(Dm != Dm.shift(1))
for nm, x in (("VİOP-endeksi fark (analist)", z), ("ABD takvimi, tekrar dahil", zU), ("ABD takvimi, tekrar hariç", zU_nodup)):
    s = split(x, d.fwd3, 3); say(f"  {nm}: ic={s['ic']:.4f} t={s['t']:.2f} IS={s['t_is']:.2f} OOS={s['t_oos']:.2f} yıl={s['yrs']}")
say("  corr(z, zU)=", round(float(z.corr(zU)), 3), " VİOP günlerinin kaçında ABD getirisi >1 gün kapsıyor:", int((Dm.diff().dt.days > 4).sum()))
# (b) eşik ve h
say("  eşik duyarlılığı (h=3; IS/OOS Sharpe 5bps):")
for th in (0.0, 0.25, 0.43, 0.67, 1.0, 1.5):
    p = np.sign(z).where(z.abs() > th, 0.0).fillna(0)
    a = bt(p[ISM], d.v_ret[ISM], 3); b = bt(p[OOSM], d.v_ret[OOSM], 3)
    say(f"    |z|>{th}: IS {a['sharpe']:.2f}  OOS {b['sharpe']:.2f}  OOS_dm {bt(p[OOSM], d.v_ret[OOSM], 3, demean=True)['sharpe']:.2f}")
say("  h duyarlılığı (IC t full/IS/OOS; tercile BT OOS Sharpe):")
for h in (1, 2, 3, 4, 5, 10):
    y = sum(d.v_ret.shift(-k) for k in range(1, h + 1))
    s = split(z, y, h); b = bt(pos[OOSM], d.v_ret[OOSM], h); a = bt(pos[ISM], d.v_ret[ISM], h)
    say(f"    h={h}: t={s['t']:.2f} IS={s['t_is']:.2f} OOS={s['t_oos']:.2f}  BT IS {a['sharpe']:.2f} OOS {b['sharpe']:.2f}")
# (c) ileri gün profili IS/OOS
say("  ileri gün profili: IC(z_t, v_ret_{t+k})")
for k in range(1, 6):
    y = d.v_ret.shift(-k); s = split(z, y, 1)
    say(f"    k={k}: ic={s['ic']:.3f} t={s['t']:.2f} | IS ic={s['ic_is']:.3f} t={s['t_is']:.2f} | OOS ic={s['ic_oos']:.3f} t={s['t_oos']:.2f}")
# (d) alt dönem
say("  alt dönem IC (fwd3) ve BT Sharpe:")
for a_, b_ in (("2017", "2019"), ("2020", "2021"), ("2022", "2023"), ("2024", "2026")):
    mm = (idx >= a_) & (idx <= b_ + "-12-31")
    s = ic_t(z[mm], d.fwd3[mm], 5); bb = bt(pos[mm], d.v_ret[mm], 3)
    say(f"    {a_}-{b_}: ic={s['ic']:.3f} t={s['t']:.2f} n={s['n']}  BT Sharpe={bb['sharpe']:.2f}")
# (e) OOS: piyasa-betası arındırılmış alfa (pnl ~ a + b v_ret)
import statsmodels.api as sm
pn = bt(pos[OOSM], d.v_ret[OOSM], 3)["pnl"]; rr = d.v_ret.reindex(pn.index)
mm = sm.OLS(pn, sm.add_constant(rr)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
say(f"  OOS alfa (yıllık %)={mm.params['const']*252*100:.2f} t={mm.tvalues['const']:.2f}  beta={mm.params.iloc[1]:.3f}")
pn = bt(pos, d.v_ret, 3)["pnl"]; rr = d.v_ret.reindex(pn.index)
mm = sm.OLS(pn, sm.add_constant(rr)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
say(f"  TAM alfa (yıllık %)={mm.params['const']*252*100:.2f} t={mm.tvalues['const']:.2f}  beta={mm.params.iloc[1]:.3f}")
# (f) blok bootstrap OOS Sharpe %90 GA (blok 20 gün)
rng = np.random.default_rng(7); pn = bt(pos[OOSM], d.v_ret[OOSM], 3)["pnl"].values; n = len(pn); B = 20; sh = []
for _ in range(3000):
    st = rng.integers(0, n - B, size=n // B + 1); s = np.concatenate([pn[i:i + B] for i in st])[:n]
    sh.append(s.mean() / s.std() * np.sqrt(252))
say(f"  OOS Sharpe blok-bootstrap %90 GA: [{np.percentile(sh, 5):.2f}, {np.percentile(sh, 95):.2f}], P(Sharpe<=0)={np.mean(np.array(sh) <= 0):.3f}")
# (g) roll maliyeti: aktif kontrat değişince net pozisyon devri |eff| × 5 bps (kapat+aç)
p = pos.copy(); eff = p.rolling(3, min_periods=1).sum() / 3
rollday = (d.code != d.code.shift(-1))   # t'de tutulan kontrat t+1'de değişiyor
extra = (eff.abs() * 5 / 1e4).where(rollday, 0.0)
base = bt(pos, d.v_ret, 3)["pnl"]; adj = base - extra.shift(1).reindex(base.index).fillna(0)
say(f"  roll devir maliyeti eklenince TAM Sharpe {base.mean()/base.std()*np.sqrt(252):.2f} → {adj.mean()/adj.std()*np.sqrt(252):.2f}; OOS: "
    f"{base[base.index>IS_END].mean()/base[base.index>IS_END].std()*np.sqrt(252):.2f} → {adj[adj.index>IS_END].mean()/adj[adj.index>IS_END].std()*np.sqrt(252):.2f}")
# (h) uç dönem hariç (Ocak–Şubat 2026) BT
ext = (idx >= "2026-01-01") & (idx <= "2026-02-28")
b1 = bt(pos[OOSM & ~ext], d.v_ret[OOSM & ~ext], 3)
say(f"  OOS Ocak–Şubat 2026 hariç Sharpe: {b1['sharpe']:.2f}")
# (i) Diğer eşlemelerin OOS sonucu (IS seçimine duyarlılık)
for nm, p in (("isaret", np.sign(z).fillna(0)), ("z_kirp", (z / 2).clip(-1, 1).fillna(0))):
    say(f"  eşleme {nm}: OOS Sharpe {bt(p[OOSM], d.v_ret[OOSM], 3)['sharpe']:.2f}, dm {bt(p[OOSM], d.v_ret[OOSM], 3, demean=True)['sharpe']:.2f}")
# (j) en iyi OOS'u veren madenci seçimi (seçim yanlılığı): GDX, RING
for c in ("y_GDX", "y_RING"):
    r_ = np.log(d[c]).diff(); zz = zsc(r_ - beta(r_, rg, 60, 40) * rg); pp = np.sign(zz).where(zz.abs() > 0.43, 0.0).fillna(0)
    s = split(zz, d.fwd3, 3)
    say(f"  {c}: t={s['t']:.2f} IS={s['t_is']:.2f} OOS={s['t_oos']:.2f}; tercile OOS Sharpe {bt(pp[OOSM], d.v_ret[OOSM], 3)['sharpe']:.2f}")

# ---------- (3) D1 zaman çakışması ----------
say("\n== (3) D1: DXY Yahoo kapanışı (17:00 ET) ile emilim penceresi [t-1 20:00 → t 15:00] çakışması ==")
zD = zsc(np.log(d.y_DX_Y_NYB).diff())
dstv = pd.Series((idx - pd.Timedelta(days=1)).tz_localize("America/New_York").map(lambda x: bool(x.dst())), index=idx)
for hs in (20, 21, 22):
    w = np.log(d.XAUUSD_p15 / d[f"XAUUSD_p{hs}"].shift(1))
    for nm, mm in (("yaz", dstv), ("kış", ~dstv)):
        s = ic_t(zD[mm], w[mm], 5); say(f"  pencere t-1 {hs}:00→t 15:00, {nm}: ic={s['ic']:.3f} t={s['t']:.2f} n={s['n']}")
# DXY kapanışından sonra başlayan pencere: yaz 21:00, kış 22:00 (kapanış anı) → +1 saat güvenlik
w = np.log(d.XAUUSD_p15 / d.XAUUSD_p23.shift(1)); s = split(zD, w, 0)
say(f"  pencere t-1 23:00 → t 15:00 (Dukascopy günlük arasından sonra): ic={s['ic']:.3f} t={s['t']:.2f} IS={s['t_is']:.2f} OOS={s['t_oos']:.2f}")
w = np.log(d.XAUUSD_p23.shift(1) / d.XAUUSD_p20.shift(1)); s = ic_t(zD, w, 5)
say(f"  yalnız t-1 20:00 → 23:00: ic={s['ic']:.3f} t={s['t']:.2f}")
# DXY'nin ampirik kapanışı ~19:00 UTC (yaz) / 20:00 UTC (kış) → pencere başlangıcı 20:00 UTC'den önce; çakışma yok, README'nin 17:00 ET varsayımı muhafazakâr.
w = np.log(d.XAUUSD_p15 / d.XAUUSD_p00); s = split(zD, w, 0)
say(f"  pencere t 00:00 → t 15:00: ic={s['ic']:.3f} t={s['t']:.2f} IS={s['t_is']:.2f} OOS={s['t_oos']:.2f}")
w = np.log(d.XAUUSD_p00 / d.XAUUSD_p20.shift(1)); s = split(zD, w, 0)
say(f"  pencere t-1 20:00 → t 00:00: ic={s['ic']:.3f} t={s['t']:.2f}")
# GLD (16:00 ET) ile aynı: altın ETF kapanışı vs DXY — pencere başlangıcı 20:00 UTC'de ABD hisse kapanışı ile hizalı mı?

# ---------- (4) Kayıt FDR ----------
say("\n== (4) Kayıt BH-FDR yeniden hesap ==")
r = pd.read_csv(f"{S}/out/registry/a4_abd_capraz.csv")
say("  kayıt satırı:", len(r), " aileler:", r.family.value_counts().to_dict())
def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]; return np.clip(q, 0, 1)
from scipy.stats import norm
r["p2"] = 2 * (1 - norm.cdf(r.t.abs()))
ok = r.p2.notna()
r.loc[ok, "q_all"] = bh(r.loc[ok, "p2"])
prim_fam = [f for f in r.family.unique() if f.startswith(("s1_", "s2_", "s3_")) and "emilim" not in f and "oz" not in f]
pm = ok & r.family.isin(prim_fam)
r.loc[pm, "q_prim"] = bh(r.loc[pm, "p2"])
say("  birincil test sayısı (s1–s3, emilim/öz hariç):", int(pm.sum()), " en küçük q:", round(float(r.q_prim.min()), 3))
say("  en küçük p (birincil):", r.loc[pm].nsmallest(5, "p2")[["test_id", "h", "t", "p2", "q_prim"]].round(5).to_string())
say("  Bonferroni eşiği 0.05/n =", 0.05 / pm.sum(), " geçen:", int((r.loc[pm, "p2"] < 0.05 / pm.sum()).sum()))
lg.close()
