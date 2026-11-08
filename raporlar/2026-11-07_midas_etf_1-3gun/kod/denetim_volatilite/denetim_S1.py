"""Denetim: volatilite_S1 (RSI2(SVXY)<10 & SVXY>SMA200 -> SVXY long, h=2) bağımsız yeniden üretim ve sağlamlık.
Çalıştırma: python3 -I kod/denetim_volatilite/denetim_S1.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import dlib, lib
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 400)
rng = np.random.default_rng(20261107)

sv = lib.load("SVXY"); C = sv["c"]
rsi = dlib.wilder_rsi(C, 2); ma = dlib.sma(C, 200)
SIG = ((rsi < 10) & (C > ma)).fillna(False)
COST = dlib.cost("SVXY")
print(f"SVXY maliyet 2.5k={COST:.1f} 1k={dlib.cost('SVXY',1000):.1f} 10k={dlib.cost('SVXY',10000):.1f} bp; sinyal gün sayısı={int(SIG.sum())}, ilk={SIG[SIG].index[0].date()}")

# --- 1) yeniden üretim C0/O1/C1 x h ---
rows = []; TR = {}
for mode in ("C0", "O1", "C1"):
    for h in (1, 2, 3):
        tr = dlib.sim(sv, SIG, h, mode, COST); TR[(mode, h)] = tr
        s = dlib.summ(tr, f"SVXY {mode} h{h}")
        s["net_1k"] = s["brut_bp"] - dlib.cost("SVXY", 1000); s["net_10k"] = s["brut_bp"] - dlib.cost("SVXY", 10000)
        rows.append(s)
R = pd.DataFrame(rows); print("\n=== 1) Yeniden üretim (kendi motorum) ==="); print(R.round(3).to_string())
R.to_csv(os.path.join(dlib.OUT, "S1_yeniden_uretim.csv"), index=False)

# ajanın işlem listesi ile karşılaştır
ag = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "aile_volatilite", "aday_rsi2_islemler_SVXY_C0h2.csv"), parse_dates=["sig_date", "entry_date", "exit_date"])
mine = TR[("C0", 2)]
print("\najan işlem sayısı", len(ag), "benim", len(mine), "| ortak sinyal günü:", len(set(ag.sig_date) & set(mine.sig)),
      "| max |brüt farkı| bp:", float((ag.set_index("sig_date").gross - mine.set_index("sig").gross).abs().max() * 1e4))

# lib.rsi (ewm, ilk değerden tohum) ile Wilder (SMA tohum) farkı
r_lib = lib.rsi(C, 2)
print("RSI farkı (lib vs Wilder) 30. günden sonra max:", float((r_lib - rsi).abs().iloc[30:].max()))

# --- 2) en iyi 5 / en kötü 5 işlem, veri kalitesi kontrolü ---
vk = pd.read_csv(os.path.join(lib.ROOT, "sonuclar", "veri_kalitesi.csv"), parse_dates=["date"])
vk = vk[vk.sym == "SVXY"]
tr = mine.copy()
tr["rsi"] = rsi.reindex(tr.sig).values; tr["sma_mesafe_%"] = ((C / ma - 1) * 100).reindex(tr.sig).values
vix = lib.vol_index("VIX").reindex(sv.index); tr["VIX"] = vix.reindex(tr.sig).values
tr["gece_bp"] = [(sv.o.iloc[sv.index.get_loc(g) + 1] / sv.c.loc[g] - 1) * 1e4 for g in tr.giris]
print("\n=== 2) En iyi 5 işlem ===")
best = tr.nlargest(5, "net"); print(best.assign(net_bp=best.net * 1e4).drop(columns=["gross", "net"]).round(2).to_string())
for r in best.itertuples():
    hit = vk[(vk.date > r.giris) & (vk.date <= r.cikis)]
    print("  ", r.sig.date(), "veri_kalitesi kaydı:", "YOK" if hit.empty else hit.to_dict("records"))
print("En kötü 5 işlem:"); w5 = tr.nsmallest(5, "net"); print(w5.assign(net_bp=w5.net * 1e4).drop(columns=["gross", "net"]).round(2).to_string())
tr.to_csv(os.path.join(dlib.OUT, "S1_islemler_C0h2_denetim.csv"), index=False)

# --- 3) yıl yıl; 2020/2022 hariç; en iyi 5 çıkarılınca ---
print("\n=== 3) Yıl yıl (C0 h2 ve O1 h2) ===")
for key in [("C0", 2), ("O1", 2)]:
    t_ = TR[key]; g = t_.groupby(t_.sig.dt.year).net
    print(key, pd.DataFrame({"n": g.count(), "ort_net_bp": (g.mean() * 1e4).round(0), "top_net_bp": (g.sum() * 1e4).round(0)}).T.to_string())
alt = []
for key in [("C0", 2), ("O1", 2), ("C0", 1)]:
    t_ = TR[key]
    for nm, m in [("tum", t_.sig.dt.year > 0), ("2020_haric", t_.sig.dt.year != 2020), ("2022_haric", t_.sig.dt.year != 2022),
                  ("2020_2022_haric", ~t_.sig.dt.year.isin([2020, 2022])), ("2021_haric", t_.sig.dt.year != 2021),
                  ("2019_2021", t_.sig.dt.year <= 2021), ("2022_2026", t_.sig.dt.year >= 2022)]:
        s = dlib.summ(t_[m.values], f"{key[0]} h{key[1]} {nm}"); alt.append(s)
    s5 = t_.drop(t_.nlargest(5, "net").index); alt.append(dlib.summ(s5, f"{key[0]} h{key[1]} en_iyi5_cikar"))
    s3 = t_.drop(t_.nlargest(3, "net").index); alt.append(dlib.summ(s3, f"{key[0]} h{key[1]} en_iyi3_cikar"))
A = pd.DataFrame(alt)[["tag", "n", "net_bp", "t", "p", "win", "is_net_bp", "oos_net_bp", "yil_pozitif"]]
print(A.round(3).to_string()); A.to_csv(os.path.join(dlib.OUT, "S1_alt_ornek.csv"), index=False)

# --- 4) maliyet duyarlılığı ---
print("\n=== 4) Maliyet (net bp, t) ===")
for key in [("C0", 2), ("O1", 2)]:
    t_ = TR[key]
    for pos in (1000, 2500, 10000):
        x = t_.gross - dlib.cost("SVXY", pos) / 1e4
        print(key, pos, round(x.mean() * 1e4, 1), round(dlib.tstat(x), 2))

# --- 5) rastgele giriş permütasyonu ---
def rand_test(pool_mask, n_tr, h, mode, reps=2000, tag=""):
    pool = np.where(pool_mask.reindex(sv.index).fillna(False).values)[0]
    pool = pool[(pool + h + 1) < len(sv)]
    c = sv.c.values; o = sv.o.values
    means = np.empty(reps)
    for k in range(reps):
        perm = rng.permutation(pool); acc = []; taken = np.zeros(len(sv) + 5, bool)
        for i in perm:
            if mode == "C0": a, b = i, i + h
            elif mode == "O1": a, b = i + 1, i + h
            else: a, b = i + 1, i + 1 + h
            if taken[a:b + 1].any() if mode != "C0" else taken[a + 1:b + 1].any(): continue
            if mode == "C0": taken[a + 1:b + 1] = True
            else: taken[a:b + 1] = True
            ep = c[a] if mode != "O1" else o[a]
            acc.append(c[b] / ep - 1)
            if len(acc) >= n_tr: break
        means[k] = np.mean(acc) * 1e4 - COST
    return means

print("\n=== 5) Rastgele giriş permütasyonu (2000 tekrar, aynı n, aynı tutuş, çakışmasız) ===")
start = SIG[SIG].index[0]
elig_all = pd.Series(sv.index >= start, index=sv.index) & ma.notna()
elig_trend = elig_all & (C > ma)
perm_rows = []
for key in [("C0", 2), ("O1", 2), ("C0", 1)]:
    obs = TR[key].net.mean() * 1e4; n_tr = len(TR[key])
    for nm, pm in [("tum_gunler", elig_all), ("SMA200_ustu_gunler", elig_trend)]:
        m = rand_test(pm, n_tr, key[1], key[0], 2000)
        p = (np.sum(m >= obs) + 1) / (len(m) + 1)
        perm_rows.append({"kural": f"{key[0]} h{key[1]}", "havuz": nm, "gozlenen_net_bp": obs, "rastgele_ort": m.mean(), "rastgele_p95": np.percentile(m, 95), "p_tek_yon": p})
P = pd.DataFrame(perm_rows); print(P.round(4).to_string()); P.to_csv(os.path.join(dlib.OUT, "S1_permutasyon.csv"), index=False)

# döngüsel kaydırma (sinyal kümelenmesini korur)
print("\nDöngüsel kaydırma testi (C0 h2, SMA200 filtresi sabit; RSI sinyali kaydırılır):")
rs_sig = (rsi < 10)
sh_means = []
valid = sv.index >= start
for k in range(1000):
    sh = int(rng.integers(20, valid.sum() - 20))
    arr = rs_sig.values[valid]; arr = np.roll(arr, sh)
    s2 = pd.Series(False, index=sv.index); s2.iloc[np.where(valid)[0]] = arr
    s2 = s2 & (C > ma)
    t2 = dlib.sim(sv, s2, 2, "C0", COST)
    sh_means.append(t2.net.mean() * 1e4 if len(t2) else np.nan)
sh_means = np.array(sh_means)
obs = TR[("C0", 2)].net.mean() * 1e4
print(f"  gözlenen {obs:.1f}; kaydırılmış ort {np.nanmean(sh_means):.1f}, p95 {np.nanpercentile(sh_means,95):.1f}, p={(np.sum(sh_means>=obs)+1)/(len(sh_means)+1):.4f}")

# --- 6) parametre komşuluğu (gerçek SVXY) ---
print("\n=== 6) Parametre komşuluğu (gerçek SVXY, h=2) ===")
nb = []
for L in (2, 3):
    rr = dlib.wilder_rsi(C, L)
    for thr in (5, 7.5, 10, 12.5, 15, 20, 25):
        for m_ in (0, 100, 150, 200, 250):
            filt = (C > dlib.sma(C, m_)) if m_ else pd.Series(True, index=C.index)
            s = ((rr < thr) & filt).fillna(False)
            s[sv.index < start] = False   # aynı başlangıç (adil karşılaştırma)
            for mode in ("C0", "O1", "C1"):
                for h in (1, 2, 3):
                    t_ = dlib.sim(sv, s, h, mode, COST); x = dlib.summ(t_)
                    nb.append({"rsi_len": L, "esik": thr, "sma": m_, "mode": mode, "h": h, "n": x["n"], "net_bp": x.get("net_bp"), "t": x.get("t"),
                               "is_net": x.get("is_net_bp"), "oos_net": x.get("oos_net_bp"), "yil_poz": x.get("yil_pozitif")})
NB = pd.DataFrame(nb); NB.to_csv(os.path.join(dlib.OUT, "S1_komsuluk.csv"), index=False)
for mode in ("C0", "O1", "C1"):
    pv = NB[(NB.rsi_len == 2) & (NB.h == 2) & (NB["mode"] == mode)].pivot(index="esik", columns="sma", values="net_bp").round(0)
    pt = NB[(NB.rsi_len == 2) & (NB.h == 2) & (NB["mode"] == mode)].pivot(index="esik", columns="sma", values="t").round(2)
    print(f"{mode} h2 RSI(2) net bp (satır=eşik, sütun=SMA; 0=filtresiz):\n{pv.to_string()}\n t:\n{pt.to_string()}")
pv = NB[(NB.rsi_len == 3) & (NB.h == 2) & (NB["mode"] == "C0")].pivot(index="esik", columns="sma", values="net_bp").round(0)
print("C0 h2 RSI(3) net bp:\n", pv.to_string())
sub = NB[(NB.rsi_len == 2) & (NB.esik.isin([5, 7.5, 10, 12.5, 15])) & (NB.sma.isin([100, 150, 200, 250])) & (NB.h == 2)]
print("\nKomşuluk (RSI2, eşik 5-15, SMA 100-250, h2) mod bazında medyan net bp ve pozitif oranı:")
print(sub.groupby("mode").agg(med_net=("net_bp", "median"), pos=("net_bp", lambda x: (x > 0).mean()), med_t=("t", "median"), n_comb=("n", "size")).round(2).to_string())

# --- 7) getirinin ayrışması: gece mi gün içi mi; koşulsuz kıyas ---
print("\n=== 7) Ayrışma (C0 h2): gece (t kapanış -> t+1 açılış) + t+1 gün içi + t+2 ===")
c = sv.c; o = sv.o
on = (o.shift(-1) / c - 1); d1 = (c.shift(-1) / o.shift(-1) - 1); d2 = (c.shift(-2) / c.shift(-1) - 1)
for nm, m in [("sinyal", SIG), ("SMA200_ustu_tum", (C > ma) & (sv.index >= start)), ("tum", pd.Series(sv.index >= start, index=sv.index))]:
    print(f"  {nm:<16} n={int(m.sum()):>5} gece={on[m].mean()*1e4:6.1f}  t+1 gün içi={d1[m].mean()*1e4:6.1f}  t+2={d2[m].mean()*1e4:6.1f}  "
          f"C0h2 brüt={(c.shift(-2)/c-1)[m].mean()*1e4:6.1f}")

# --- 8) C0 uygulanabilirlik: sinyal kapanıştan ~10-20 dk önceki fiyatla verilirse ---
print("\n=== 8) C0 kapanış öncesi fiyat duyarlılığı (simülasyon) ===")
lr = np.log(C).diff(); vol20 = lr.rolling(20).std().shift(0)
res = []
for k in range(500):
    eps = rng.normal(0, 1, len(C)) * vol20.fillna(0.02).values * np.sqrt(20 / 390) * 1.3   # son ~20 dk, kapanış yoğunluğu x1.3
    p_pre = C * np.exp(-eps)                     # 15:40 fiyatı = kapanış / exp(eps)
    cc = C.copy(); 
    # her gün t için: RSI t gününü p_pre ile hesapla (geçmiş günler gerçek kapanış)
    # yaklaşık: RSI2 Wilder tek adım güncellemesi
    rv = rsi.copy()
    d = C.diff()
    up = d.clip(lower=0); dn = (-d).clip(lower=0)
    # Wilder ortalamaları (t-1'e kadar)
    au = pd.Series(np.nan, index=C.index); ad = pd.Series(np.nan, index=C.index)
    a_u = up.values; a_d = dn.values
    AU = np.full(len(C), np.nan); AD = np.full(len(C), np.nan)
    AU[2] = a_u[1:3].mean(); AD[2] = a_d[1:3].mean()
    for i in range(3, len(C)):
        AU[i] = (AU[i - 1] + a_u[i]) / 2; AD[i] = (AD[i - 1] + a_d[i]) / 2
    dpre = p_pre.values - np.r_[np.nan, C.values[:-1]]
    upp = np.clip(dpre, 0, None); dnp = np.clip(-dpre, 0, None)
    AUp = (np.r_[np.nan, AU[:-1]] + upp) / 2; ADp = (np.r_[np.nan, AD[:-1]] + dnp) / 2
    rsip = 100 - 100 / (1 + AUp / ADp)
    map_ = (C.rolling(199).sum().shift(1) + p_pre) / 200
    sp = pd.Series((rsip < 10) & (p_pre.values > map_.values), index=C.index).fillna(False)
    df2 = sv.copy(); df2["c"] = C.where(~sp, p_pre)   # giriş fiyatı = kapanış öncesi fiyat (yalnız giriş günü)
    # çıkış fiyatı gerçek kapanış olmalı: sim giriş için df2.c, çıkış için sv.c kullanılsın
    s_arr = sp.values; rows_ = []; busy = -1
    for i in range(len(C) - 2):
        if not s_arr[i] or i < busy: continue
        g_ = C.values[i + 2] / p_pre.values[i] - 1; rows_.append(g_); busy = i + 2
    x = np.array(rows_) - COST / 1e4
    res.append((len(x), x.mean() * 1e4, dlib.tstat(x)))
res = np.array(res)
print(f"  n ort {res[:,0].mean():.1f} (min {res[:,0].min():.0f}, max {res[:,0].max():.0f}); net ort {res[:,1].mean():.1f} bp (p5 {np.percentile(res[:,1],5):.1f}, p95 {np.percentile(res[:,1],95):.1f}); t ort {res[:,2].mean():.2f} (p5 {np.percentile(res[:,2],5):.2f})")
near = tr[(tr.rsi > 7) & (tr.rsi < 10)]
print(f"  RSI 7-10 aralığındaki sinyaller: {len(near)}/{len(tr)} (eşiğe yakın, son dakika fiyatıyla dönebilir)")

# --- 9) Aynı kural diğer araçlarda ---
print("\n=== 9) Aynı SVXY sinyali diğer araçlarda (C0/O1/C1 h2) ===")
oth = []
for sym in ["SVIX", "VXX", "VIXY", "UVXY", "UVIX", "VIXM", "SPY", "QQQ", "SSO", "UPRO", "QLD", "TQQQ"]:
    d = lib.load(sym)
    s = SIG.reindex(d.index).fillna(False)
    for mode in ("C0", "O1", "C1"):
        t_ = dlib.sim(d, s, 2, mode, dlib.cost(sym)); x = dlib.summ(t_, f"{sym} {mode} h2")
        x["cost"] = dlib.cost(sym); oth.append(x)
O = pd.DataFrame(oth)[["tag", "n", "brut_bp", "net_bp", "t", "is_net_bp", "oos_net_bp", "win", "maxdd", "en_kotu_bp", "yil_pozitif", "cost"]]
print(O.round(2).to_string()); O.to_csv(os.path.join(dlib.OUT, "S1_diger_araclar.csv"), index=False)

# SVIX'in kendi RSI2 sinyali
sx = lib.load("SVIX"); rsx = dlib.wilder_rsi(sx.c, 2)
filt = (C > ma).reindex(sx.index).fillna(False)
for nm, s in [("SVIX kendi RSI2<10 & SVXY>SMA200", (rsx < 10) & filt), ("SVIX SVXY sinyali", SIG.reindex(sx.index).fillna(False))]:
    for mode in ("C0", "O1", "C1"):
        x = dlib.summ(dlib.sim(sx, s, 2, mode, dlib.cost("SVIX")), nm)
        print(f"  {nm} {mode} h2: n={x['n']} net={x['net_bp']:.1f} t={x['t']:.2f}")
# SVXY yalnız SVIX dönemi (2022-03+)
x = dlib.summ(TR[("C0", 2)][TR[("C0", 2)].sig >= sx.index[0]], "SVXY C0 h2 2022-03+")
print(f"  SVXY C0 h2 aynı dönem (2022-03+): n={x['n']} net={x['net_bp']:.1f} t={x['t']:.2f}")
print("\nSon gün:", sv.index[-1].date(), "SVXY", round(sv.raw_c.iloc[-1], 2), "RSI2", round(rsi.iloc[-1], 1), "SMA200", round(ma.iloc[-1], 2), "sinyal", bool(SIG.iloc[-1]))
