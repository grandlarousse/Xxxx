"""DENETİM tahvil_doviz — S1 sağlamlık: permütasyon (rastgele gün; ay+haftanın günü eşlenik), göreli gün profili,
NFP/haftanın günü karışıklığı, 10Y/30Y, yeni ihraç/yeniden ihraç, ve 1990-2016 uzun dönem Hazine getirisi testi
(fiscaldata ihale tarihleri + FRED DGS10/DGS30; ham veri sonuclar/aile_tahvil_doviz/denetim_ham/).
Çalıştır: python3 -I kod/denetim_tahvil_doviz/d02_s1_saglamlik.py
"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd
import lib
from d01_s1_yeniden import IDX, A10, A30, ROOT, OUT, sim, tstat, cost, apos

HAM = os.path.join(ROOT, "sonuclar", "aile_tahvil_doviz", "denetim_ham")
rng = np.random.default_rng(20261107)
NREP = 20000

tmv = lib.load("TMV").reindex(IDX); tlt = lib.load("TLT").reindex(IDX)
c = tmv["c"].values; cl = tlt["c"].values
r2 = c[2:] / c[:-2] - 1                      # C0 h=2 getirisi, sinyal günü i -> i+2
r2 = np.r_[r2, [np.nan, np.nan]]
r2l = np.r_[cl[2:] / cl[:-2] - 1, [np.nan, np.nan]]
t = sim("TMV", A10, 3, 1, "C0")
sig_pos = IDX.get_indexer(t.sig_date)
obs = np.nanmean(r2[sig_pos]); obs_l = np.nanmean(r2l[sig_pos])
print(f"Gözlenen TMV brüt {obs*1e4:.1f} bp, TLT {obs_l*1e4:.1f} bp, n={len(sig_pos)}")

valid = np.where(np.isfinite(r2) & (np.arange(len(IDX)) >= 0))[0]
# (a) rastgele gün permütasyonu (aynı n, aynı 2 gün tutuş)
sims = np.array([np.nanmean(r2[rng.choice(valid, len(sig_pos), replace=False)]) for _ in range(NREP)])
p_a = (np.sum(sims >= obs) + 1) / (NREP + 1)
simsl = np.array([np.nanmean(r2l[rng.choice(valid, len(sig_pos), replace=False)]) for _ in range(NREP)])
p_al = (np.sum(simsl <= obs_l) + 1) / (NREP + 1)
print(f"(a) rastgele gün: TMV p={p_a:.5f} (sim ort {sims.mean()*1e4:.1f} bp, %95 {np.quantile(sims,0.95)*1e4:.1f}); TLT p={p_al:.5f}")
# (b) aynı ay + aynı haftanın günü eşlenik (gerçek pencere hariç)
ym = IDX.year * 100 + IDX.month; dow = IDX.dayofweek
pools = []
for sp in sig_pos:
    cand = np.where((ym == ym[sp]) & (dow == dow[sp]) & (np.abs(np.arange(len(IDX)) - sp) > 2) & np.isfinite(r2))[0]
    if len(cand) == 0:
        cand = np.where((dow == dow[sp]) & (np.abs(np.arange(len(IDX)) - sp) > 2) & (np.abs(np.arange(len(IDX)) - sp) < 30) & np.isfinite(r2))[0]
    pools.append(cand)
simb = np.empty(NREP); simbl = np.empty(NREP)
for k in range(NREP):
    pick = np.array([rng.choice(pl) for pl in pools])
    simb[k] = np.nanmean(r2[pick]); simbl[k] = np.nanmean(r2l[pick])
p_b = (np.sum(simb >= obs) + 1) / (NREP + 1); p_bl = (np.sum(simbl <= obs_l) + 1) / (NREP + 1)
print(f"(b) ay+gün eşlenik: TMV p={p_b:.5f} (sim ort {simb.mean()*1e4:.1f} bp, %95 {np.quantile(simb,0.95)*1e4:.1f}); TLT p={p_bl:.5f} (sim ort {simbl.mean()*1e4:.1f})")
# (c) tüm takvimi kaydırma profili
shifts = []
for sh in list(range(-20, -4)) + list(range(5, 21)):
    pos = sig_pos + sh; pos = pos[(pos >= 0) & (pos < len(IDX) - 2)]
    shifts.append((sh, np.nanmean(r2l[pos]) * 1e4, tstat(r2l[pos])))
sh = pd.DataFrame(shifts, columns=["kaydirma", "TLT_bp", "t"])
print(f"(c) takvim kaydırma ±5..20 gün (32 kaydırma): TLT ort {sh.TLT_bp.mean():.1f} bp, en düşük {sh.TLT_bp.min():.1f} bp; "
      f"gözlenenden (≤{obs_l*1e4:.1f}) düşük kaydırma sayısı: {(sh.TLT_bp <= obs_l*1e4).sum()}")

# göreli gün profili: A-6 .. A+3 tek günlük TLT getirisi ve haftanın günü kontrolü
P, _ = apos(A10); P = P[P >= 7]
r1 = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
dow_mean = pd.Series(r1).groupby(dow).mean()
prof = []
for k in range(-6, 4):
    pos = P + k; pos = pos[pos < len(IDX)]
    x = r1[pos]; dm = np.array([dow_mean[dow[q]] for q in pos])
    prof.append((f"A{k:+d}", np.nanmean(x) * 1e4, tstat(x), np.nanmean(x - dm) * 1e4, tstat(x - dm),
                 pd.Series(dow[pos]).map({0: "Pzt", 1: "Sal", 2: "Çar", 3: "Per", 4: "Cum"}).value_counts().idxmax()))
prof = pd.DataFrame(prof, columns=["gun", "TLT_1g_bp", "t", "gun_eslenik_fark_bp", "t_fark", "en_sik_gun"])
print("\nGöreli gün profili (TLT 1 günlük; A-2 getirisi = A-3 kapanış -> A-2 kapanış):")
print(prof.round(2).to_string(index=False))
print("TLT haftanın günü ortalaması (bp, 2016-2026):", (dow_mean * 1e4).round(2).to_dict())

# NFP karışıklığı
nfp = pd.read_csv(os.path.join(ROOT, "data", "events", "nfp.csv"), parse_dates=["date"])
nfp_d = pd.DatetimeIndex(sorted(nfp[nfp.event == "NFP"].date.unique())) if "event" in nfp else pd.DatetimeIndex(sorted(nfp.date.unique()))
nfp_pos = IDX.get_indexer(nfp_d); nfp_pos = nfp_pos[nfp_pos >= 0]
is_nfp_sig = np.isin(sig_pos, nfp_pos)
win_has_nfp = np.array([np.any((nfp_pos > s) & (nfp_pos <= s + 2)) for s in sig_pos])
cst = cost("TMV") / 1e4
for lab, m in [("A-3 = NFP günü", is_nfp_sig), ("A-3 ≠ NFP günü", ~is_nfp_sig), ("pencerede NFP (A-2/A-1)", win_has_nfp),
               ("NFP ne A-3 ne pencerede", ~is_nfp_sig & ~win_has_nfp)]:
    x = r2[sig_pos[m]]; xl = r2l[sig_pos[m]]
    print(f"{lab:26s}: n={m.sum():3d} TMV net {np.nanmean(x-cst)*1e4:6.1f} bp (t {tstat(x-cst):5.2f}) | TLT {np.nanmean(xl)*1e4:6.1f} bp (t {tstat(xl):5.2f})")
# genel NFP sonrası (ihale penceresi olmayan NFP günleri): NFP kapanışı -> +2 gün
oth = np.setdiff1d(nfp_pos, sig_pos); oth = oth[oth < len(IDX) - 2]
print(f"İhale penceresi DIŞINDAKİ NFP günü kapanışı -> +2 gün: n={len(oth)} TLT {np.nanmean(r2l[oth])*1e4:.1f} bp (t {tstat(r2l[oth]):.2f}); TMV brüt {np.nanmean(r2[oth])*1e4:.1f} bp")

# 10Y yeni ihraç vs yeniden ihraç
ev = pd.read_csv(os.path.join(ROOT, "data", "events", "hazine_ihale_10y30y.csv"), parse_dates=["date"])
e10 = ev[ev.event == "UST10Y_ihale"].set_index("date")
reo = t.auction.map(lambda d: "reopening" in str(e10.loc[d, "detail"]))
for lab, m in (("yeni ihraç (Şub/May/Ağu/Kas)", ~reo.values), ("yeniden ihraç", reo.values)):
    x = r2[sig_pos[m]]; xl = r2l[sig_pos[m]]
    print(f"{lab:30s}: n={m.sum():3d} TMV net {np.nanmean(x-cst)*1e4:6.1f} bp (t {tstat(x-cst):5.2f}) | TLT {np.nanmean(xl)*1e4:6.1f}")
# A-3 haftanın günü
for d_, nm in ((2, "Çar"), (3, "Per"), (4, "Cum")):
    m = dow[sig_pos] == d_
    x = r2[sig_pos[m]]; xl = r2l[sig_pos[m]]
    print(f"A-3 = {nm}: n={m.sum():3d} TMV net {np.nanmean(x-cst)*1e4:6.1f} bp (t {tstat(x-cst):5.2f}) | TLT {np.nanmean(xl)*1e4:6.1f} (t {tstat(xl):.2f})")

# Hazine getirisiyle (ETF değil) 30Y ve birleşik pencere
y10 = lib.fred("DGS10").reindex(IDX).values; y30 = lib.fred("DGS30").reindex(IDX).values
def dy(y, P, k1, k2):
    a = P - k1; b = P - k2; m = (a >= 0) & (b < len(IDX)); return (y[b[m]] - y[a[m]]) * 100
P30, _ = apos(A30)
for lab, PP in (("10Y ihale", P), ("30Y ihale", P30[P30 >= 7])):
    for k1, k2 in ((3, 1), (3, 0), (1, 0), (0, -2)):
        x = dy(y30, PP, k1, k2); z = dy(y10, PP, k1, k2)
        print(f"{lab} A-{k1}->A{-k2:+d}: ΔDGS30 {np.nanmean(x):5.2f} bp (t {tstat(x):5.2f}) ΔDGS10 {np.nanmean(z):5.2f} bp (t {tstat(z):5.2f})")

# ---------------- uzun dönem (1990-2016) Hazine getirisi testi ----------------
def fred_csv(s):
    d = pd.read_csv(os.path.join(HAM, s + ".csv"), parse_dates=["observation_date"]).set_index("observation_date")[s]
    return pd.to_numeric(d, errors="coerce").dropna()
g10 = fred_csv("DGS10"); g30 = fred_csv("DGS30"); g20 = fred_csv("DGS20")
J = json.load(open(os.path.join(HAM, "auc10.json")))["data"]
au = pd.DataFrame(J)
au = au[(au.inflation_index_security == "No") & (au.original_security_term == "10-Year") & (au.security_type == "Note")]
ad = pd.DatetimeIndex(sorted(pd.to_datetime(au.auction_date).unique()))
# proje csv'si ile çakışan dönemde eşleşme
proj = A10[(A10 >= "2016-01-01") & (A10 <= "2026-10-31")]; api = ad[(ad >= "2016-01-01") & (ad <= "2026-10-31")]
print(f"\nfiscaldata 10Y nominal ihale: {len(ad)} ({ad.min().date()}..{ad.max().date()}); 2016-2026 proje csv {len(proj)} / api {len(api)}; "
      f"fark: proje-api {sorted(set(proj.date) - set(api.date))[:5]}, api-proje {sorted(set(api.date) - set(proj.date))[:5]}")
cal = g10.index  # tahvil piyasası günleri (FRED)
long = []
for per, lo, hi in (("1990-2007", "1990-01-01", "2007-12-31"), ("2008-2016-10", "2008-01-01", "2016-10-31"),
                    ("1990-2016-10 (tümü)", "1990-01-01", "2016-10-31"), ("2016-11-2026 (örneklem)", "2016-11-01", "2026-11-06")):
    dd = ad[(ad >= lo) & (ad <= hi)]
    pp = cal.searchsorted(dd); pp = pp[(pp >= 3) & (pp < len(cal))]
    for nm, ser in (("DGS10", g10), ("DGS30", g30.reindex(cal)), ("DGS20", g20.reindex(cal))):
        v = ser.reindex(cal).values
        x = (v[pp - 1] - v[pp - 3]) * 100
        # aynı dönemde koşulsuz 2 günlük değişim
        allx = (v[2:] - v[:-2]) * 100
        sel = (cal[2:] >= lo) & (cal[2:] <= hi)
        u = np.nanmean(allx[sel])
        long.append((per, nm, int(np.isfinite(x).sum()), np.nanmean(x), tstat(x), u, np.nanmean(x) - u))
L = pd.DataFrame(long, columns=["donem", "seri", "n", "dY_A3_A1_bp", "t", "kosulsuz_2g_bp", "fark_bp"])
print("Uzun dönem: 10Y ihale A-3 -> A-1 Hazine getiri değişimi (yükseliş = TLT düşüşü = TMV kazancı):")
print(L.round(3).to_string(index=False))
# TLT eşdeğeri (süre ~17) ve TMV eşdeğeri (≈ -3 x) kaba ölçek
x = L[(L.donem == "1990-2016-10 (tümü)") & (L.seri == "DGS20")].iloc[0]
print(f"1990-2016 DGS20 farkı {x.fark_bp:.2f} bp -> TLT ~ {-17*x.fark_bp:.1f} bp, TMV(-3x) brüt ~ {51*x.fark_bp:.1f} bp (kaba)")
# yıllara göre 1990-2016 (DGS10)
pp_all = cal.searchsorted(ad[(ad >= "1990-01-01") & (ad <= "2016-10-31")]); pp_all = pp_all[pp_all >= 3]
v = g10.values
xx = pd.Series((v[pp_all - 1] - v[pp_all - 3]) * 100, index=cal[pp_all])
yy = xx.groupby(xx.index.year).mean()
print("1990-2016 yıllara göre ort ΔDGS10 (bp) pozitif yıl oranı:", round((yy > 0).mean(), 3), "| yıl sayısı", len(yy))
print("yıllık:", yy.round(1).to_dict())

pd.DataFrame({"sims_random": sims[:2000], "sims_matched": simb[:2000]}).to_csv(os.path.join(OUT, "d02_perm_ornek.csv"), index=False)
prof.to_csv(os.path.join(OUT, "d02_goreli_gun.csv"), index=False); L.to_csv(os.path.join(OUT, "d02_uzun_donem.csv"), index=False)
sh.to_csv(os.path.join(OUT, "d02_kaydirma.csv"), index=False)
json.dump({"p_random_tmv": p_a, "p_random_tlt": p_al, "p_matched_tmv": p_b, "p_matched_tlt": p_bl}, open(os.path.join(OUT, "d02_perm.json"), "w"), indent=1)
