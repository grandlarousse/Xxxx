"""(2) Pratik kuralın bağımsız backtest'i (dlib; cl/ev/pl kullanılmaz). VİOP uzlaşma fiyatları, örtüşmesiz, aynı kontrat, spot β,
tam sayı kontrat, vadeli kilit, maliyet 8+3 / 15+3 / tik. Parametre duyarlılığı (eşik 0,75/1/1,25 × tutma 1/2/3). Yarım gün etkisi."""
import sys, json
import numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/rehber/altin/denetim/kod")
import dlib
OUT = dlib.D + "/sonuc"
c = dlib.cal(); START = "2018-12-17"; B0 = pd.Timestamp("2024-07-01")
gV, sdV, zV = dlib.viop_gold_z()
# ---------------- araştırma benzeri (ön vade zinciri, vadeli β, günlük değişen hedge, tam sayı yok, kilit yok)
fT = dlib.front("TRALT"); fX = dlib.front("XU030")
rT = fT["r"].copy(); rX = fX["r"].copy()
sp = np.log(dlib.ydaily("TRALT.IS")["adj"]).diff().reindex(c)
lim = pd.Series(np.where(c < dlib.REG, np.log(1.22), np.log(1.115)), index=c)
rT[(rT.abs() > lim)] = np.nan; rT[((rT - sp).abs() > 0.08) & sp.notna()] = np.nan
sdx = rX.rolling(250, min_periods=60).std().shift(1); rX[(rX.abs() > 10 * sdx) & sdx.notna()] = np.nan
def rb(y, x, w=250, mp=100):
    m = y.notna() & x.notna(); y = y.where(m); x = x.where(m)
    return (y.rolling(w, min_periods=mp).cov(x) / x.rolling(w, min_periods=mp).var()).shift(1)
bF = rb(rT, rX); hed = rT - bF * rX
def research_trades(z, h=2, thr=1.0, start=START):
    y = sum(hed.shift(-i) for i in range(1, h + 1)); y = y[y.index >= start]
    zz = z.reindex(y.index).values; yy = y.values; rows = []; i = 0
    while i < len(yy):
        if np.isfinite(zz[i]) and np.isfinite(yy[i]) and abs(zz[i]) > thr:
            d = np.sign(zz[i]); rows.append((y.index[i], d, d * yy[i] * 1e4)); i += h
        else: i += 1
    T = pd.DataFrame(rows, columns=["date", "dir", "gross_bps"]).set_index("date"); T["hold"] = h; T["tick_bps"] = np.nan
    T["devam_ayni_kontrat"] = False
    return T
R = []
def rep(lab, T, costs=("8+3", "15+3", "tik", "8+3 devam0")):
    for cs in costs:
        if cs in ("tik", "8+3 devam0") and T["tick_bps"].isna().all(): continue
        s = dlib.stats(T, cs); s.update(var=lab, cost=cs); R.append(s)
        if cs == "8+3":
            print(f"{lab:70s} n {s['n']} /yıl {s['per_yr']:.1f} brüt {s['gross']:+.1f} net {s['net']:+.1f} (t {s['t']:.2f}) isabet {s['hit']:.3f} "
                  f"IS {s['IS']:+.1f} ({s['IS_t']:.2f}) OOS {s['OOS']:+.1f} ({s['OOS_t']:.2f}) 24-26 {s['y24']:+.1f} ({s['y24_t']:.2f}, n {s['y24_n']}) "
                  f"top10 hariç {s['drop10']:+.1f} ({s['drop10_t']:.2f})")
TR0 = research_trades(zV); TR0x = research_trades(zV, start=START); rep("R0 araştırma benzeri (bağımsız; 03.11'e kadar)", TR0)
TR0b = research_trades(zV[zV.index <= "2026-10-30"]); TR0b = TR0b[TR0b.index <= "2026-10-28"]; rep("R0' araştırma benzeri, panel sonu 30.10'a kadar", TR0b)
# ---------------- pratik sinyal
bS = dlib.spot_beta()
p18 = dlib.snap("GC=F", "h1", 15, 0); r18 = dlib.chg(p18)
d = r18 - gV
ym = pd.Series(c.year * 100 + c.month, index=c); win = pd.Series(False, index=c)
for key in ym.unique():
    if key % 100 in (1, 3, 5, 7, 11):
        dd = ym.index[ym == key]; nx = ym.index[ym > key][:2]; win[dd[-6:]] = True; win[nx] = True
roll = (d > 0.004) & win & (c >= B0)
print("bağımsız GC=F vade sıçrama günleri:", [(str(k.date()), round(v * 1e4)) for k, v in d[roll].items()])
r18f = r18.where(~roll, r18 - d)                 # sıçrama günü: VİOP değişimi (TVC:GOLD spotta sıçrama yok)
sd_raw = r18.rolling(250, min_periods=100).std().shift(1)       # betik σ'sı (ham GC=F)
sd_raw = sd_raw.where(sd_raw.notna(), sdV)                        # 100 gözlem dolana kadar VİOP σ (kurucuyla aynı)
sd_fix = r18f.rolling(250, min_periods=100).std().shift(1)      # TVC:GOLD benzeri σ (Pine)
sd_fix = sd_fix.where(sd_fix.notna(), sdV)
z_P = (r18f / sd_raw).where((c >= B0) & r18f.notna(), zV)        # kurucunun P tanımı (hibrit)
z_Pfix = (r18f / sd_fix).where((c >= B0) & r18f.notna() & sd_fix.notna(), z_P)
z_Praw = (r18 / sd_raw).where((c >= B0) & r18.notna(), zV)        # sıçrama düzeltmesiz
# yarım gün farkında: arife günü giriş yok; ertesi gün referans = arife 12:30 TSİ (09:00 ve 10:00 UTC bitişli barların ortalaması)
h1x = pd.read_parquet(dlib.S + "/data/h1/XU030.IS.parquet"); dday = h1x.index.tz_convert("Europe/Istanbul").tz_localize(None).normalize()
lastbar = pd.Series(h1x.index.tz_convert("Europe/Istanbul").hour, index=dday).groupby(level=0).max()
half = pd.DatetimeIndex(lastbar.index[lastbar <= 13]); print("yarım günler (XU030.IS 60dk):", [str(x.date()) for x in half])
p_half = (dlib.snap("GC=F", "h1", 9, 0) + dlib.snap("GC=F", "h1", 10, 0)) / 2
ref = p18.shift(1).copy(); prevday = pd.Series(c, index=c).shift(1)
for k in c[c >= B0]:
    if prevday[k] in half: ref[k] = p_half[prevday[k]]
r18h = np.log(p18 / ref); r18h = r18h.where(~roll, r18h - d)
z_Ph = (r18h / sd_raw).where((c >= B0) & r18h.notna(), zV); z_Ph[z_Ph.index.isin(half)] = np.nan
# ---------------- pratik kural simülasyonları
S1 = {}
for lab, z, kw in (("E1 VİOP sinyali + aynı kontrat + spot β + tam sayı + kilit", zV, {}),
                   ("E1n VİOP sinyali, kilit yok", zV, dict(lock=False)),
                   ("E1i VİOP sinyali, tam sayı yok, kilit yok", zV, dict(lock=False, integer=False)),
                   ("P PRATİK (kurucu tanımı: 2024-07+ 18:00 GC=F düzeltilmiş, betik σ)", z_P, {}),
                   ("P-ham (GC=F vade sıçraması düzeltilmeden)", z_Praw, {}),
                   ("P-σfix (σ da sıçramasız = TVC:GOLD/Pine σ)", z_Pfix, {}),
                   ("P-yarımgün (arife günü giriş yok, ertesi gün 12:30 referansı)", z_Ph, {})):
    T = dlib.simulate(z, beta=bS, start=START, **kw); S1[lab] = T
    rep(lab, T); print("      atlanan giriş (kilit)", T.attrs["skipped"], "uzatılan", int((T["hold"] > 2).sum()), "devam", int(T["devam"].sum()),
                       "aynı kontratla devam", int(T["devam_ayni_kontrat"].sum()))
TP = S1["P PRATİK (kurucu tanımı: 2024-07+ 18:00 GC=F düzeltilmiş, betik σ)"]
TP.to_csv(OUT + "/denetim_pratik_islemler.csv")
# kurucunun işlem listesiyle karşılaştırma
B = pd.read_csv(dlib.S + "/out/rehber/altin/sonuc/pratik_islemler.csv", parse_dates=["date"]).set_index("date")
j = TP.join(B[["dir", "gross", "N_TRALT"]].rename(columns={"dir": "dir_k", "gross": "gross_k"}), how="outer")
both = j.dropna(subset=["dir", "dir_k"])
print("işlem tarihi eşleşmesi: bizde", len(TP), "kurucuda", len(B), "ortak", len(both), "aynı yön", int((both.dir == both.dir_k).sum()),
      "| ortak işlemlerde brüt fark (bps) ort", round((both.gross_bps - both.gross_k * 1e4).mean(), 1), "medyan |fark|", round((both.gross_bps - both.gross_k * 1e4).abs().median(), 1),
      "| N farkı olan", int((both.N != both.N_TRALT).sum()))
only_me = j[j["dir_k"].isna()].index; only_k = j[j["dir"].isna()].index
print("yalnız bizde:", [str(x.date()) for x in only_me][:30]); print("yalnız kurucuda:", [str(x.date()) for x in only_k][:30])
# ---------------- duyarlılık
G = []
for zl, z in (("VİOP", zV), ("PRATİK", z_P)):
    for thr in (0.75, 1.0, 1.25):
        for h in (1, 2, 3):
            T = dlib.simulate(z, thr=thr, h=h, beta=bS, start=START)
            for cs in ("8+3", "15+3"):
                s = dlib.stats(T, cs)
                G.append(dict(sinyal=zl, esik=thr, tutma=h, maliyet=cs, n=s["n"], yilda=round(s["per_yr"], 1), net=round(s["net"], 1), t=round(s["t"], 2),
                              IS=round(s["IS"], 1), OOS=round(s["OOS"], 1), y24=round(s["y24"], 1), y24_t=round(s["y24_t"], 2), top10_haric=round(s["drop10"], 1), top10_t=round(s["drop10_t"], 2)))
G = pd.DataFrame(G); G.to_csv(OUT + "/denetim_duyarlilik.csv", index=False)
print(G[G.maliyet == "8+3"].to_string(index=False))
print(G[G.maliyet == "15+3"][["sinyal", "esik", "tutma", "net", "t"]].to_string(index=False))
# ince eşik taraması (pratik, h2)
print("eşik taraması (PRATİK, h2, 8+3):", {thr: (lambda s: (round(s['net'], 1), round(s['t'], 2), s['n']))(dlib.stats(dlib.simulate(z_P, thr=thr, beta=bS), "8+3")) for thr in (0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5)})
# ---------------- ayrıntı: pratik kural P
s = dlib.stats(TP, "8+3"); print("P yıllar:", s["by_year"], "| long", round(s["long"], 1), s["n_long"], "short", round(s["short"], 1), "| maxDD", round(s["maxdd"]), "en kötü", round(s["worst"]), s["worst_date"], "p5", round(s["p5"]), "sd", round(s["sd"]))
net = TP["gross_bps"] - 11; win_ = net[net > 0].mean(); los = net[net <= 0].mean()
ls = (net <= 0).astype(int); streak = ls.groupby((ls != ls.shift()).cumsum()).sum().max()
fk = TP[(TP.index >= "2026-09-01") & (TP.index <= "2026-10-31")]
print("ort kazanç", round(win_), "ort kayıp", round(los), "en uzun kayıp serisi", int(streak), "| fon krizi (Eyl–Eki 2026) n", len(fk), "ort net", round((fk.gross_bps - 11).mean(), 1))
# TL: 03.11 fiyatları
last = c[-1]; pT0 = fT.loc[last, "settle"]; pX0 = fX.loc[last, "settle"]; b0 = bS.dropna().iloc[-1]
N0 = int(round(10 * pX0 / (b0 * 100 * pT0))); nT0 = N0 * 100 * pT0
print(f"03.11: {fT.loc[last,'code']} {pT0} / {fX.loc[last,'code']} {pX0} β {b0:.3f} -> N {N0}, TRALT tutarı {nT0:,.0f} TL, XU030 tutarı {10*pX0:,.0f} TL; "
      f"teminat %15/%11 {0.15*nT0+0.11*10*pX0:,.0f} TL, %17/%11 {0.17*nT0+0.11*10*pX0:,.0f}")
for cs in ("8+3", "15+3", "tik"):
    s = dlib.stats(TP, cs); print(f"  {cs}: işlem başı {s['net']/1e4*nT0:,.0f} TL, yılda {s['net']/1e4*nT0*s['per_yr']:,.0f} TL; en kötü {s['worst']/1e4*nT0:,.0f}; maxDD {s['maxdd']/1e4*nT0:,.0f}; p5 {s['p5']/1e4*nT0:,.0f}; sd {s['sd']/1e4*nT0:,.0f}")
pd.DataFrame(R).drop(columns=["by_year"]).to_csv(OUT + "/denetim_backtest_ozet.csv", index=False)
json.dump({k: dlib.stats(v, "8+3")["by_year"] for k, v in S1.items()}, open(OUT + "/denetim_yillar.json", "w"), ensure_ascii=False, indent=1)
