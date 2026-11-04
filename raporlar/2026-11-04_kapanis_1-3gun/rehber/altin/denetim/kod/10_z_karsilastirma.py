"""(1) Son 300 BIST günü: z ve sinyal serisi — bağımsız kod vs günlük betik (sinyal_altin.py fonksiyonları) vs araştırma kodu (cl/ev).
Üç ayrı süreç parçası: (a) bağımsız (dlib), (b) betiğin kendi fonksiyonlarıyla aynı akış, (c) araştırma kodu genişletilmiş panelle."""
import sys, importlib.util, json
import numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/rehber/altin/denetim/kod")
import dlib
OUT = dlib.D + "/sonuc"; import os; os.makedirs(OUT, exist_ok=True)
c = dlib.cal(); print("takvim son günü", c[-1].date(), "gün", len(c))
# ---------------- (a) bağımsız
gV, sdV, zV = dlib.viop_gold_z()
p18 = dlib.snap("GC=F", "h1", 15, 0); r18 = dlib.chg(p18)
sd18 = r18.rolling(250, min_periods=100).std().shift(1)            # betik tanımı: ham GC=F 18:00 değişimleri
z18_own_sd = r18 / sd18; z18_viop_sd = r18 / sdV
p1755 = dlib.snap("GCZ26.CMX", "m5", 14, 55, max_age_min=30); r1755 = dlib.chg(p1755)
p1745 = dlib.snap("GCZ26.CMX", "m5", 14, 45, max_age_min=30); r1745 = dlib.chg(p1745)
z1755 = r1755 / sd18
# ---------------- (b) betik fonksiyonlarıyla (betik main() ile aynı akış, son kapanışa kadar)
spec = importlib.util.spec_from_file_location("sa", dlib.S + "/out/rehber/altin/sinyal_altin.py"); sa = importlib.util.module_from_spec(spec); spec.loader.exec_module(sa)
x30, _ = sa.daily_bist("XU030.IS"); bcal = x30.index
g60, _ = sa.yahoo("GC=F", "60m", rng="730d"); g60 = g60[(g60.index.second == 0) & (g60.index.minute == 0)]
ac, nm = sa.active_contract(); b5, _ = sa.yahoo(ac, "5m", rng="60d"); b5 = b5[(b5.index.second == 0) & (b5.index.minute % 5 == 0)]
s60 = sa.snap_series(g60, 60, bcal, 15, 0, max_age_h=30)["px"]; r60 = np.log(s60 / s60.shift(1)); sigB = r60.rolling(250, min_periods=100).std().shift(1)
sn = sa.snap_series(b5, 5, bcal, 14, 55)["px"]; gB = np.log(sn / sn.shift(1)); zB = gB / sigB
print("betik takvimi son", bcal[-1].date(), "| bağımsız takvim (VİOP) son", c[-1].date(), "| takvim farkı (son 300):",
      sorted(set(bcal[bcal >= c[-300]]).symmetric_difference(set(c[-300:]))))
# ---------------- (c) araştırma kodu (cl/ev) — panel 03.11'e genişletilmiş (bizim bültenlerimizle)
sys.path.insert(0, dlib.S + "/out/code_k_dis-suruculer_curut")
import cl, ev
P0 = pd.read_parquet(dlib.S + "/data/viop_panel.parquet", columns=["date", "code", "und", "expiry", "settle", "prev_settle", "close", "vwap", "value_tl", "trades", "oi"])
P0["code"] = P0["code"].astype(str); P0["und"] = P0["und"].astype(str); P0["date"] = pd.DatetimeIndex(P0["date"]).normalize(); P0["expiry"] = pd.DatetimeIndex(P0["expiry"]).normalize()
NP = dlib.panel(); NP = NP[NP["date"] > P0["date"].max()].copy()
NP["vwap"] = np.nan; NP["trades"] = np.nan; NP["oi"] = np.nan
P1 = pd.concat([P0, NP[P0.columns]], ignore_index=True)
cl._P = P1; cl._CAL = None; cl._FR.clear(); ev._R.clear()
gR = ev.R("XAUUSD"); zR = cl.zscale(gR, 250, 100)
# ---------------- karşılaştırma
L = c[-300:]
def sig(z, t=1.0): return np.sign(z).where(z.abs() > t, 0.0)
def cmp(a, b, lab, idx):
    A = a.reindex(idx); B = b.reindex(idx); m = A.notna() & B.notna()
    sa_, sb_ = sig(A[m]), sig(B[m])
    o = dict(karsilastirma=lab, n=int(m.sum()), corr=round(float(np.corrcoef(A[m], B[m])[0, 1]), 4), max_abs_fark=round(float((A[m] - B[m]).abs().max()), 4),
             sinyal_esleme=round(float((sa_ == sb_).mean()), 4), sinyal_A=int((sa_ != 0).sum()), sinyal_B=int((sb_ != 0).sum()),
             ters_isaret=int(((sa_ * sb_) < 0).sum()), ilk=str(A[m].index.min().date()), son=str(A[m].index.max().date()))
    print(o); return o
R = []
R.append(cmp(zV, zR, "VİOP z: bağımsız vs araştırma kodu", L))
R.append(cmp(sdV, cl.zscale(gR, 250, 100) * 0 + gR.rolling(250, min_periods=100).std().shift(1), "σ VİOP: bağımsız vs araştırma", L))
R.append(cmp(z1755, zB, "17:55 z: bağımsız (GCZ26 5dk, σ ham GC=F 18:00) vs betik", L))
R.append(cmp(sd18, sigB, "σ betik tanımı: bağımsız vs betik", L))
R.append(cmp(z18_own_sd, zV, "18:00 z (σ ham GC=F) vs VİOP uzlaşma z", L))
R.append(cmp(zB, zV, "betik 17:55 z vs VİOP uzlaşma z", L))
R.append(cmp(zB, zR, "betik 17:55 z vs araştırma kodu z", L))
R.append(cmp(r1745 / sd18, zV, "17:45 z vs VİOP uzlaşma z", L))
R.append(cmp(z1755, zV, "17:55 z (bağımsız) vs VİOP uzlaşma z", L))
pd.DataFrame(R).to_csv(OUT + "/z_karsilastirma.csv", index=False)
# σ karşılaştırması
both = pd.concat([sdV.rename("sd_viop"), sd18.rename("sd_ham18"), sigB.rename("sd_betik")], axis=1).reindex(L)
print("σ oranı ham GC=F 18:00 / VİOP (son 300 gün):", (both.sd_ham18 / both.sd_viop).describe()[["mean", "min", "max"]].round(3).to_dict())
F = pd.concat([gV.rename("g_viop"), sdV.rename("sd_viop"), zV.rename("z_viop_bagimsiz"), zR.rename("z_arastirma_kodu"),
               r18.rename("g_1800"), sd18.rename("sd_ham1800"), z18_own_sd.rename("z_1800"), r1755.rename("g_1755"), z1755.rename("z_1755_bagimsiz"),
               gB.rename("g_betik"), sigB.rename("sd_betik"), zB.rename("z_betik")], axis=1).reindex(L)
F.to_csv(OUT + "/z_son300.csv")
print(F.tail(12).round(4).to_string())
# farklı sinyal günleri (VİOP vs betik/17:55)
dd = F[(np.sign(F.z_betik).where(F.z_betik.abs() > 1, 0) != np.sign(F.z_viop_bagimsiz).where(F.z_viop_bagimsiz.abs() > 1, 0)) & F.z_betik.notna()]
print("betik vs VİOP farklı sinyal günleri:\n", dd[["z_viop_bagimsiz", "z_betik", "z_1755_bagimsiz"]].round(2).to_string())
dd2 = F[(np.sign(F.z_1800).where(F.z_1800.abs() > 1, 0) != np.sign(F.z_viop_bagimsiz).where(F.z_viop_bagimsiz.abs() > 1, 0)) & F.z_1800.notna()]
print("18:00 vs VİOP farklı sinyal günü sayısı", len(dd2), "| son 300 günde VİOP sinyal", int((F.z_viop_bagimsiz.abs() > 1).sum()), "18:00 sinyal", int((F.z_1800.abs() > 1).sum()))
print(dd2[["z_viop_bagimsiz", "z_1800"]].round(2).to_string())
