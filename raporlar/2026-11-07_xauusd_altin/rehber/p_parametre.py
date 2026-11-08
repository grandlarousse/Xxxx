# Görev P: elle hesaplayıcı sabit parametreleri (2026-11-06 Cuma kapanışı itibarıyla), sinyal_altin.py tanımlarıyla.
import sys, os, json, math, datetime as dt
import numpy as np, pandas as pd

S_ = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S_}/out/sentez")
import sinyal_altin as SA

OUT = f"{S_}/out/rehber"
K = SA.PanelKaynak(f"{S_}/panel", log=lambda *a: None)
P = SA.P
D = dt.date
T_PAZ = D(2026, 11, 9)       # betiğin hesapladığı ilk gün (Pazartesi)
T_SAL = D(2026, 11, 10)      # Cuma getirisini pencereye katan ilk gün
CUMA = D(2026, 11, 6)
YIL_ONCE = D(2025, 11, 6)
res = {}

# ------------------------------------------------------------------ E2 betaları
kar = SA.etf_karar(T_PAZ)
gunler = K.veri_gunleri_etf(T_PAZ)
i_t = gunler.index(T_PAZ)
gg = gunler[:i_t]                     # ... 2026-11-06
kk = {x: K.kapanis(x, kar) for x in ("GLD", "GDX", "GDXJ", "SPY")}
R = pd.DataFrame({x: SA._getiri(kk[x], gg) for x in kk}, index=gg)
n = len(R)
X = R[["GLD", "SPY"]].values

def beta_tam(Y, X, i, win=250, minp=60):  # sabit + iki eğim
    lo = max(0, i - win); yy, xx = Y[lo:i], X[lo:i]
    m = np.isfinite(yy) & np.all(np.isfinite(xx), axis=1)
    A = np.column_stack([np.ones(m.sum()), xx[m]])
    b = np.linalg.lstsq(A, yy[m], rcond=None)[0]
    r = yy[m] - A @ b
    return b, int(m.sum()), float(np.std(r, ddof=3))

e2 = {}
bet_ser = {}
for y in ("GDXJ", "GDX"):
    Y = R[y].values
    b_son, nn, sres = beta_tam(Y, X, n)          # pencere: son 250 getiri, 2026-11-06 dahil -> e(2026-11-09) için
    b_paz, _, _ = beta_tam(Y, X, n - 1)          # pencere 2026-11-05'te biter -> e(2026-11-06), Pazartesi sinyali
    # 12 aylık seri (her gün için o gün kullanılan beta: pencere bir önceki satırda biter)
    rows = [i for i in range(1, n + 1) if (gg[i] if i < n else T_PAZ) > YIL_ONCE]
    ser = pd.DataFrame([dict(gun=(gg[i] if i < n else T_PAZ), a=beta_tam(Y, X, i)[0][0], b_GLD=beta_tam(Y, X, i)[0][1], b_SPY=beta_tam(Y, X, i)[0][2]) for i in rows]).set_index("gun")
    bet_ser[y] = ser
    e2[y] = dict(b_GLD=float(b_son[1]), b_SPY=float(b_son[2]), sabit_gunluk=float(b_son[0]), n=nn, artik_std_gunluk=sres,
                 pencere=f"{gg[n-250]} → {gg[n-1]} (250 işlem günü getirisi, Cuma dahil)",
                 b_GLD_pazartesi=float(b_paz[1]), b_SPY_pazartesi=float(b_paz[2]),
                 aralik_12ay=dict(b_GLD=[float(ser.b_GLD.min()), float(ser.b_GLD.max())], b_SPY=[float(ser.b_SPY.min()), float(ser.b_SPY.max())]),
                 aylik_mutlak_degisim_medyan=dict(b_GLD=float(ser.b_GLD.diff(21).abs().median()), b_SPY=float(ser.b_SPY.diff(21).abs().median())))

# Betiğin x değerleri ve sabit beta ile elle hesap
art = {y: SA.madenci_artik(R, y, range(max(1, n - 40), n)) for y in ("GDXJ", "GDX")}
x_betik, x_elle, x_elle_paz = {}, {}, {}
c = {x: kk[x]["close"].reindex(gg).astype(float) for x in kk}
for sid, cc in SA.E2.items():
    y, k = cc["y"], cc["k"]
    x_betik[sid] = float(art[y].iloc[-k:].sum())
    lr = {z: math.log(c[z].iloc[-1] / c[z].iloc[-1 - k]) for z in (y, "GLD", "SPY")}
    for dst, bb in ((x_elle, (e2[y]["b_GLD"], e2[y]["b_SPY"])), (x_elle_paz, (e2[y]["b_GLD_pazartesi"], e2[y]["b_SPY_pazartesi"]))):
        dst[sid] = lr[y] - bb[0] * lr["GLD"] - bb[1] * lr["SPY"]
res["E2"] = dict(GDXJ=e2["GDXJ"], GDX=e2["GDX"],
                 esik=dict(C2j_ust=SA.E2["E2-C2j_GDXJ_artik_h3"]["hi"], C2_ust=SA.E2["E2-C2_GDX_artik_h3"]["hi"],
                           C1_ust=SA.E2["E2-C1_madenci_oncu_GLD_h5"]["hi"], C1_kaplama_alt=SA.E2["E2-C1_madenci_oncu_GLD_h5"]["lo"]),
                 dogrulama_pazartesi=dict(x_betik=x_betik, x_elle_sabit_beta_son=x_elle, x_elle_sabit_beta_pazartesi=x_elle_paz))

# ------------------------------------------------------------------ Donmuş beta / basit getiri / temettüsüz kapanış hata analizi (E2)
def x_karsilastir(bas=D(2023, 11, 1)):
    """E2 sinyal (x>eşik) tutarlılığı: betik (günlük beta, satır satır artık) vs elle (k günlük log getiri, sabit beta)."""
    Yh = {y: pd.read_parquet(f"{S_}/panel/yahoo/{y}.parquet") for y in ("GLD", "GDX", "GDXJ", "SPY")}
    cl_adj = pd.DataFrame({y: Yh[y]["adjclose"] for y in Yh}); cl_raw = pd.DataFrame({y: Yh[y]["close"] for y in Yh})
    cl_adj.index = [pd.Timestamp(d).date() for d in cl_adj.index]; cl_raw.index = cl_adj.index
    cl_adj = cl_adj.reindex(gg); cl_raw = cl_raw.reindex(gg)
    Rl = np.log(cl_adj).diff()
    gun = [d for d in gg if d >= bas]
    sonuc = {}
    for sid, cc in SA.E2.items():
        y, k, hi, lo = cc["y"], cc["k"], cc["hi"], cc["lo"]
        Y = Rl[y].values; Xm = Rl[["GLD", "SPY"]].values
        pos = {g: gg.index(g) for g in gun}
        # betik: e_i = Y_i - b_{i}·X_i (b: [i-250,i-1]); x(d) = sum e_{j}, j = i_d-k .. i_d-1
        bcache = {}
        def b_at(i):
            if i not in bcache: bcache[i] = SA._beta2(Y, Xm, i, 250, 60)
            return bcache[i]
        e = {}
        for g in gun:
            i = pos[g]
            for j in range(i - k, i):
                if j not in e:
                    b = b_at(j); e[j] = Y[j] - b[0] * Xm[j, 0] - b[1] * Xm[j, 1]
        x_true = pd.Series({g: sum(e[j] for j in range(pos[g] - k, pos[g])) for g in gun})
        sig_true = x_true > hi
        kf = dict(haftalik=lambda d: tuple(d.isocalendar()[:2]), aylik=lambda d: (d.year, d.month), ceyrek=lambda d: (d.year, (d.month - 1) // 3))
        ilk = {a: {} for a in kf}
        for j, d in enumerate(gg):
            for a in kf: ilk[a].setdefault(kf[a](d), j)
        def x_manual(cl, guncel, basit=False):
            v = {}
            for g in gun:
                i = pos[g]            # g günü; veri i-1'de biter
                # donmuş beta: son güncelleme günü u (<= g), beta = b_at(index(u)) (u'dan önceki 250 getiri)
                if guncel == "gunluk": u = i
                else: u = ilk[guncel][kf[guncel](g)]
                b = b_at(u)
                if basit:
                    f = lambda z: cl[z].iloc[i - 1] / cl[z].iloc[i - 1 - k] - 1
                else:
                    f = lambda z: math.log(cl[z].iloc[i - 1] / cl[z].iloc[i - 1 - k])
                v[g] = f(y) - b[0] * f("GLD") - b[1] * f("SPY")
            return pd.Series(v)
        r = {}
        for ad, cl, gu, basit in (("log_adj_gunluk_beta", cl_adj, "gunluk", False), ("log_adj_haftalik_beta", cl_adj, "haftalik", False),
                                  ("log_adj_aylik_beta", cl_adj, "aylik", False), ("log_adj_ceyreklik_beta", cl_adj, "ceyrek", False),
                                  ("log_temettusuz_aylik_beta", cl_raw, "aylik", False), ("basit_adj_aylik_beta", cl_adj, "aylik", True)):
            xm = x_manual(cl, gu, basit)
            sg = xm > hi
            r[ad] = dict(farkli_gun=int((sg != sig_true).sum()), gun=len(gun), oran=float((sg != sig_true).mean()),
                         max_abs_x_fark_bps=float((xm - x_true).abs().max() * 1e4), medyan_abs_x_fark_bps=float((xm - x_true).abs().median() * 1e4))
            if sid == "E2-C1_madenci_oncu_GLD_h5":
                r[ad]["kaplama_farkli_gun"] = int(((xm < lo) != (x_true < lo)).sum())
        sonuc[sid] = r
    return sonuc

res["E2_elle_hata"] = x_karsilastir()

# ------------------------------------------------------------------ A4-C1: β60 ve σ_e
def a4_seri(t_son):
    kar = SA.viop_karar(t_son)
    gun = SA.viop_gunleri(t_son - dt.timedelta(days=1100), t_son)
    gg4 = gun[-P["A4_GECMIS"]:]
    kg = K.kapanis("GDXJ", kar); kl = K.kapanis("GLD", kar)
    kes = [SA.utc(d, 15) for d in gg4]; kes[-1] = min(kes[-1], kar)
    vj, gj, _ = SA.asof_once(kg, kes); vl, gl, _ = SA.asof_once(kl, kes)
    y_j = pd.Series(vj, index=gg4); y_l = pd.Series(vl, index=gg4)
    rm = np.log(y_j).diff(); rg = np.log(y_l).diff()
    W, MP = P["A4_BETA"], P["A4_BETA_MINP"]
    b_raw = rm.rolling(W, min_periods=MP).cov(rg) / rg.rolling(W, min_periods=MP).var()   # satır d dahil
    e = rm - b_raw.shift(1) * rg
    sd_raw = e.rolling(P["A4_STD"], min_periods=P["A4_STD_MINP"]).std()
    z = e / sd_raw.shift(1)
    return pd.DataFrame(dict(y_j=y_j, y_l=y_l, rm=rm, rg=rg, b_raw=b_raw, b=b_raw.shift(1), e=e, sd_raw=sd_raw, sd=sd_raw.shift(1), z=z,
                             abd_gun_j=pd.Series(gj, index=gg4)))

A = a4_seri(T_PAZ)
rp = A.loc[T_PAZ]
a4 = dict(beta60_pazartesi=float(rp.b), sigma_e_pazartesi=float(rp.sd), z_pazartesi=float(rp.z), e_pazartesi=float(rp.e),
          r_GDXJ_cuma=float(rp.rm), r_GLD_cuma=float(rp.rg),
          beta60_son=float(rp.b_raw), sigma_e_son=float(rp.sd_raw),                 # VİOP satırı 09.11 (Cuma getirisi) dahil -> Salı 10.11'den itibaren
          esik_son=float(P["A4_ESIK"] * rp.sd_raw), esik_pazartesi=float(P["A4_ESIK"] * rp.sd))
a4["elle_z_pazartesi"] = (math.log(1 + (math.exp(rp.rm) - 1)) - rp.b * rp.rg) / rp.sd
yb = A[A.index > YIL_ONCE]
a4["aralik_12ay"] = dict(beta60=[float(yb.b.min()), float(yb.b.max())], sigma_e=[float(yb.sd.min()), float(yb.sd.max())],
                         esik=[float(P["A4_ESIK"] * yb.sd.min()), float(P["A4_ESIK"] * yb.sd.max())])
a4["aylik_mutlak_degisim_medyan"] = dict(beta60=float(yb.b.diff(21).abs().median()), sigma_e=float(yb.sd.diff(21).abs().median()))
# donmuş parametre hata analizi (son 3 yıl)
A3 = a4_seri(T_PAZ)
A3 = A3[A3.index >= D(2024, 6, 1)].copy()   # A4_GECMIS=600 VİOP günü ≈ 2,4 yıl; ısınma sonrası
def pz(zv): return np.sign(zv).where(zv.abs() > P["A4_ESIK"], 0.0)
true_sig = pz(A3.z)
hata = {}
for ad, key in (("haftalik", lambda d: d.isocalendar()[:2]), ("aylik", lambda d: (d.year, d.month)), ("ceyreklik", lambda d: (d.year, (d.month - 1) // 3))):
    grp = pd.Series([key(d) for d in A3.index], index=A3.index)
    bf = A3.b.groupby(grp).transform("first"); sf = A3.sd.groupby(grp).transform("first")
    zf = (A3.rm - bf * A3.rg) / sf
    sg = pz(zf)
    hata[ad] = dict(farkli_gun=int((sg != true_sig).sum()), gun=int(len(A3)), oran=float((sg != true_sig).mean()))
# temettüsüz kapanış (TradingView varsayılanı) ve basit getiri etkisi, aylık donmuş
Yh = {y: pd.read_parquet(f"{S_}/panel/yahoo/{y}.parquet") for y in ("GLD", "GDXJ")}
rawc = {y: pd.Series(Yh[y]["close"].values, index=[pd.Timestamp(d).date() for d in Yh[y].index]) for y in Yh}
adjc = {y: pd.Series(Yh[y]["adjclose"].values, index=[pd.Timestamp(d).date() for d in Yh[y].index]) for y in Yh}
rm_raw = np.log(rawc["GDXJ"].reindex(A3.abd_gun_j.values).values) - np.log(rawc["GDXJ"].reindex(A.abd_gun_j.shift(1).reindex(A3.index).values).values)
grp = pd.Series([(d.year, d.month) for d in A3.index], index=A3.index)
bf = A3.b.groupby(grp).transform("first"); sf = A3.sd.groupby(grp).transform("first")
zraw = (pd.Series(rm_raw, index=A3.index) - bf * A3.rg) / sf
hata["aylik_temettusuz_GDXJ"] = dict(farkli_gun=int((pz(zraw) != true_sig).sum()), gun=int(len(A3)))
rs = np.exp(A3.rm) - 1; gs = np.exp(A3.rg) - 1
zs = (rs - bf * gs) / sf
hata["aylik_basit_getiri"] = dict(farkli_gun=int((pz(zs) != true_sig).sum()), gun=int(len(A3)))
a4["elle_hata_2024_06_sonrasi"] = hata
res["A4"] = a4

# ------------------------------------------------------------------ LOWMOM: rv20 eşiği (15:00 UTC) ve TradingView HV(20) eşdeğeri
kv = SA.viop_karar(T_PAZ)
p15 = K.p15_seri(CUMA, kv).astype(float)
p15.index = pd.DatetimeIndex(pd.to_datetime(p15.index))
lp = np.log(p15); r15 = lp.diff()
rv = r15.rolling(20).std()
rvA = rv * math.sqrt(252)
fin = rvA.dropna()
esik_cuma = float(np.quantile(fin.values, 1 / 3))
# 12 ay boyunca genişleyen eşik
es_ser = pd.Series({d: float(np.quantile(fin[fin.index <= d].values, 1 / 3)) for d in fin.index[fin.index > pd.Timestamp(YIL_ONCE)][::5]})
lowmom = dict(rv20_esik_yillik_252=esik_cuma, rv20_cuma=float(rvA.iloc[-1]), yuzdelik_cuma=float((fin.values <= rvA.iloc[-1]).mean()),
              esik_aralik_12ay=[float(es_ser.min()), float(es_ser.max())], rv20_aralik_12ay=[float(rvA[rvA.index > pd.Timestamp(YIL_ONCE)].min()), float(rvA[rvA.index > pd.Timestamp(YIL_ONCE)].max())],
              x5_cuma=float(lp.iloc[-1] - lp.iloc[-6]), p15_cuma=float(p15.iloc[-1]), p15_5gun_once=float(p15.iloc[-6]), p15_5gun_once_gun=str(p15.index[-6].date()),
              not_="rv20 = 15:00 UTC spot (Dukascopy BID) günlük log getirilerinin 20 günlük örneklem std'si (ddof=1) × √252; eşik = 2010-01-04'ten bu yana bütün rv20 değerlerinin 1/3 kantili (genişleyen, bugün dahil).")

# Dukascopy saatlik + Kasım dakika -> günlük kapanışlar
H = pd.read_parquet(f"{S_}/panel/duka/XAUUSD.parquet")
H.index = pd.DatetimeIndex(H.index).tz_convert("UTC")
an = pd.Series(H["c"].values, index=H.index + pd.Timedelta(hours=1))   # fiyat anı = bar başı + 1 saat
M = pd.read_parquet(f"{S_}/panel/duka_min_XAUUSD.parquet")
mi = pd.DatetimeIndex(M.index).tz_localize("UTC")
mser = pd.Series(M["c"].values, index=mi + pd.Timedelta(minutes=1))
mser = mser[mser.index > an.index.max()]
an = pd.concat([an, mser]).sort_index()
an = an[~an.index.duplicated()]
def fiyat_an(ts_list, bayat=pd.Timedelta(hours=3)):
    ts = pd.DatetimeIndex(ts_list)
    j = an.index.searchsorted(ts, side="right") - 1
    v = np.where(j >= 0, an.values[np.clip(j, 0, None)], np.nan)
    t0 = np.where(j >= 0, an.index.values[np.clip(j, 0, None)], np.datetime64("NaT"))
    ok = (ts.values - t0) <= bayat.to_timedelta64()
    return pd.Series(np.where(ok, v, np.nan), index=ts)
gunler_hf = pd.bdate_range("2009-10-01", "2026-11-06")
def gunluk(tur):
    if tur == "17ET":
        ts = [pd.Timestamp(dt.datetime(d.year, d.month, d.day, 17, 0), tz="America/New_York").tz_convert("UTC") for d in gunler_hf]
    elif tur == "21UTC":
        ts = [pd.Timestamp(d.date()).tz_localize("UTC") + pd.Timedelta(hours=21) for d in gunler_hf]
    else:  # 00UTC: gün D'nin kapanışı = D+1 00:00 UTC
        ts = [pd.Timestamp(d.date()).tz_localize("UTC") + pd.Timedelta(hours=24) for d in gunler_hf]
    s = fiyat_an(ts); s.index = gunler_hf
    return s
# hızlı açık-gün denetimi: saatlik barların UTC günü (bar sayısı)
hb = pd.Series(1, index=H.index).groupby(H.index.date).sum()
hb.index = pd.DatetimeIndex(hb.index)
mb = pd.Series(1, index=mi).groupby(mi.date).sum() / 60
mb.index = pd.DatetimeIndex(mb.index)
hb = pd.concat([hb, mb[mb.index > hb.index.max()]])
acik = hb.reindex(gunler_hf).fillna(0) >= 8
def hv(s, n=20, ann=365, ddof=0):
    r = np.log(s).diff()
    return r.rolling(n).std(ddof=ddof) * math.sqrt(ann) * 100
hvres = {}
rv_al = rvA.copy()
for tur in ("17ET", "21UTC", "00UTC"):
    s = gunluk(tur)
    s = s[acik.values & s.notna().values]
    h365 = hv(s, ann=365, ddof=0)        # TradingView yerleşik HV: 100·stdev(log(c/c[1]),n)·√365 (Pine ta.stdev yanlı = ddof 0)
    h252 = hv(s, ann=252, ddof=0)
    df = pd.DataFrame(dict(hv365=h365, hv252=h252)).join(rv_al.rename("rv") * 100, how="inner").dropna()
    df = df[df.index >= pd.Timestamp("2010-02-01")]
    q365 = float(np.quantile(df.hv365, 1 / 3)); q252 = float(np.quantile(df.hv252, 1 / 3))
    oran = float((df.hv365 / df.rv).median())
    lab = df.rv < esik_cuma * 100
    # uyum: kantil eşiği ve en iyi eşik
    uy_q = float(((df.hv365 < q365) == lab).mean())
    grid = np.arange(10, 18.01, 0.05)
    acc = [((df.hv365 < g) == lab).mean() for g in grid]
    gbest = float(grid[int(np.argmax(acc))])
    # tek-yönlü hatalar
    fp = int(((df.hv365 < q365) & ~lab).sum()); fn = int(((df.hv365 >= q365) & lab).sum())
    hvres[tur] = dict(hv365_esik_kantil=q365, hv252_esik_kantil=q252, hv365_rv_oran_medyan=oran, hv365_esik_oran=oran * esik_cuma * 100,
                      uyum_kantil=uy_q, en_iyi_esik=gbest, en_iyi_uyum=float(max(acc)), yanlis_aktif=fp, yanlis_pasif=fn, gun=int(len(df)),
                      hv365_cuma=float(h365.dropna().iloc[-1]), hv365_cuma_gun=str(h365.dropna().index[-1].date()),
                      hv365_12ay=[float(h365[h365.index > pd.Timestamp(YIL_ONCE)].min()), float(h365[h365.index > pd.Timestamp(YIL_ONCE)].max())],
                      son_yil_uyum=float(((df.hv365 < q365) == lab)[df.index > pd.Timestamp("2021-01-01")].mean()))
    if tur == "17ET": df17 = df
lowmom["hv"] = hvres
lowmom["teorik_carpan_365_ddof0"] = math.sqrt(365 / 252) * math.sqrt(19 / 20)
lowmom["teorik_hv365_esik"] = lowmom["teorik_carpan_365_ddof0"] * esik_cuma * 100
# LOWMOM'un aktif olduğu günlerin oranı (2010+) ve son aktif gün
act = rvA.dropna()
q_exp = act.expanding().apply(lambda v: (v <= v[-1]).mean(), raw=True)
lowmom["son_aktif_gun"] = str(q_exp[q_exp < 1 / 3].index.max().date())
res["LOWMOM"] = lowmom

with open(f"{S_}/rehber_kod/p_ham.json", "w") as f: json.dump(res, f, indent=1, default=str)
for y in bet_ser: bet_ser[y].to_csv(f"{S_}/rehber_kod/beta_{y}_12ay.csv")
A[A.index > YIL_ONCE].to_csv(f"{S_}/rehber_kod/a4_12ay.csv")
print(json.dumps(res, indent=1, default=str))

# ------------------------------------------------------------------ HV bantları (17:00 ET kapanışlı HV365): LOWMOM aktif olasılığı
bands = [0, 10, 11, 12, 12.5, 13, 13.5, 14, 14.5, 15, 16, 17, 18, 20, 100]
dd = df17.copy(); dd["akt"] = dd.rv < esik_cuma * 100
tab = dd.groupby(pd.cut(dd.hv365, bands))["akt"].agg(["mean", "size"])
print(tab)
# gerçek yüzdelik kuralıyla (genişleyen) aktiflik
qx = q_exp.reindex(dd.index)
dd["akt_gercek"] = qx < 1 / 3
tab2 = dd.groupby(pd.cut(dd.hv365, bands))["akt_gercek"].agg(["mean", "size"])
print(tab2)
res["LOWMOM"]["hv_bant_aktif_olasiligi_bugunku_esikle"] = {str(k): dict(aktif_orani=round(float(v["mean"]), 3), gun=int(v["size"])) for k, v in tab.iterrows()}
res["LOWMOM"]["hv_bant_aktif_olasiligi_genisleyen_yuzdelikle"] = {str(k): dict(aktif_orani=round(float(v["mean"]), 3), gun=int(v["size"])) for k, v in tab2.iterrows()}
# en büyük HV365 değeri, ki rv20 eşiğin altında (aktif) idi; ve en küçük HV365 ki pasif
res["LOWMOM"]["hv_aktifken_max"] = float(dd[dd.akt_gercek].hv365.max()); res["LOWMOM"]["hv_aktifken_q99"] = float(dd[dd.akt_gercek].hv365.quantile(0.99))
res["LOWMOM"]["hv_pasifken_min"] = float(dd[~dd.akt_gercek].hv365.min()); res["LOWMOM"]["hv_pasifken_q01"] = float(dd[~dd.akt_gercek].hv365.quantile(0.01))
print({k: res["LOWMOM"][k] for k in ("hv_aktifken_max", "hv_aktifken_q99", "hv_pasifken_min", "hv_pasifken_q01")})
with open(f"{S_}/rehber_kod/p_ham.json", "w") as f: json.dump(res, f, indent=1, default=str)
