"""Adım 1: sinyalleri kur (spot takvimi, 15:00 UTC görüntüleri). Çıktı: signals_spot.parquet, signals_meta.csv
Bilgi zamanları (hepsi gün t 15:00 UTC'de ya da önce bilinir):
  xau_p15, dk_<SYM>_p15 : 14:00 saatlik BID mumunun kapanışı = 14:59:59 UTC
  xau_p12, h<SYM>_p12    : 11:00 mumunun kapanışı = 11:59:59 UTC
  xau_p07, dk_<SYM>_p07  : 06:00 mumunun kapanışı = 06:59:59 UTC
  y_GC_F, y_SI_F, y_PL_F : Yahoo son bilinen kapanış, *_avail <= gün t 22:00 UTC'nin bir gün öncesi (panel kontrolü: max avail - t = -2 saat)
  Beta: yalnız t-W..t-1 satırları.
"""
from a5_lib import *

sp = load_spot()
sym = dict(XAG="XAGUSD", DXY="DOLLARIDXUSD", TBOND="USTBONDTRUSD", SPX="USA500IDXUSD", USDJPY="USDJPY", USDCNH="USDCNH",
           BTC="BTCUSD", EURUSD="EURUSD", COPPER="COPPERCMDUSD")
g = np.log(sp.xau_p15).diff()
# veri temizliği: tek günlük hatalı baskı (|Δ|>%5, ertesi gün ters yönde |Δ|>%5 ve fiyat t-1 seviyesine %2 içinde dönüyor; BTC hariç) -> NaN. Yalnız açık veri hatası içindir.
for v in sym.values():
    if v in ("BTCUSD", "XAGUSD", "COPPERCMDUSD"): continue  # metal/kripto sert dönüşleri gerçek olaylar (Şub 2021 gümüş sıkışması, Oca 2026 bakır)
    for suf in ("p15", "p07"):
        c = f"dk_{v}_{suf}"; lp = np.log(sp[c]); d1 = lp.diff(); d2 = lp.shift(-1) - lp
        bad = (d1.abs() > 0.05) & (d2.abs() > 0.05) & (np.sign(d1) != np.sign(d2)) & ((lp.shift(-1) - lp.shift(1)).abs() < 0.02)
        if bad.any(): print("hatalı baskı NaN:", c, list(sp.index[bad].date)); sp.loc[bad, c] = np.nan
X = pd.DataFrame({k: np.log(sp[f"dk_{v}_p15"]).diff() for k, v in sym.items()})
# veri hatası koruması: |getiri| > %25 (BTC hariç %15 üstü yoksay değil) -> sadece raporla
print("en büyük |x|:", X.abs().max().round(3).to_dict(), " g:", round(g.abs().max(), 3))

models = {"XAG": ["XAG"], "DXY": ["DXY"], "TBOND": ["TBOND"], "SPX": ["SPX"], "USDJPY": ["USDJPY"], "USDCNH": ["USDCNH"],
          "BTC": ["BTC"], "EURUSD": ["EURUSD"], "MACRO3": ["DXY", "TBOND", "SPX"], "FX3": ["EURUSD", "USDJPY", "USDCNH"],
          "ALL7": ["XAG", "DXY", "TBOND", "SPX", "USDJPY", "USDCNH", "COPPER"]}
sig = pd.DataFrame(index=sp.index)
sig["g"] = g
meta = []
for m, cols in models.items():
    for W in (60, 120, 250):
        rr = roll_resid(g, X[cols], W)
        for k in (1, 3, 5):
            c = f"R_{m}_W{W}_k{k}"; sig[c] = cum_z(rr.e, rr.sig, k)
            meta.append(dict(col=c, fam="A_resid", model=m, W=W, k=k, info="t 15:00 UTC (dk_*_p15, xau_p15)"))
        sig[f"F_{m}_W{W}"] = rr.fit / rr.sig  # faktörün ima ettiği altın hareketi (standart)
        sig[f"E_{m}_W{W}"] = rr.e
        sig[f"SIG_{m}_W{W}"] = rr.sig
        for b in [c for c in rr.columns if c.startswith("b_")]:
            sig[f"{b}_{m}_W{W}"] = rr[b]
        sig[f"R2_{m}_W{W}"] = np.nan
    print("model", m, "ok", sig[f"R_{m}_W250_k1"].notna().sum())

# --- B: oran z-skorları (aynı damga) ---
lr = np.log(sp.xau_p15 / sp.dk_XAGUSD_p15)
for L in (20, 60, 120):
    c = f"GSRZ_L{L}"; sig[c] = (lr - lr.rolling(L, min_periods=int(0.8 * L)).mean()) / lr.rolling(L, min_periods=int(0.8 * L)).std()
    meta.append(dict(col=c, fam="B_ratio", model="XAU/XAG dk15", W=L, k=np.nan, info="t 15:00 UTC"))
dlr = lr.diff(); sd = dlr.rolling(120, min_periods=96).std().shift(1)
for k in (1, 3, 5):
    c = f"GSRD_k{k}"; sig[c] = dlr.rolling(k).sum() / (sd * np.sqrt(k))
    meta.append(dict(col=c, fam="B_ratio", model="dlog(XAU/XAG) dk15 (beta=1)", W=120, k=k, info="t 15:00 UTC"))
# Yahoo t-1 sürümleri (platin; erken dönem için gümüş)
for nm, a, b in [("GPT", "y_GC_F", "y_PL_F"), ("GSY", "y_GC_F", "y_SI_F")]:
    yl = np.log(sp[a] / sp[b])
    yl = yl.where(sp[a].diff().ne(0) | sp[b].diff().ne(0))  # tekrar eden (yeni kapanış yok) günleri at
    yl = yl.ffill()
    for L in (20, 60, 120):
        c = f"{nm}Z_L{L}"; sig[c] = (yl - yl.rolling(L, min_periods=int(0.8 * L)).mean()) / yl.rolling(L, min_periods=int(0.8 * L)).std()
        meta.append(dict(col=c, fam="B_ratio", model=f"{a}/{b} Yahoo t-1", W=L, k=np.nan, info="t-1 ABD kapanışı (<= t 00:00 UTC)"))
    dy = yl.diff(); sdy = dy.rolling(120, min_periods=96).std().shift(1)
    for k in (1, 3, 5):
        c = f"{nm}D_k{k}"; sig[c] = dy.rolling(k).sum() / (sdy * np.sqrt(k))
        meta.append(dict(col=c, fam="B_ratio", model=f"dlog {a}/{b} Yahoo t-1", W=120, k=k, info="t-1 ABD kapanışı"))

# --- C: gün içi 12:00-15:00 ve 07:00-15:00 eksik tepki ---
def snap(symbol, hour_close):
    h = hourly(symbol); h.index = h.index.tz_convert(None) if h.index.tz is not None else h.index
    c = h["c"]
    s = c[c.index.hour == hour_close - 1]; s.index = s.index.normalize()
    return s.reindex(sp.index)
g12 = np.log(sp.xau_p15 / sp.xau_p12)
X12 = pd.DataFrame({k: np.log(sp[f"dk_{sym[k]}_p15"] / snap(sym[k], 12)) for k in ("DXY", "TBOND", "SPX", "XAG", "USDJPY")})
g07 = np.log(sp.xau_p15 / sp.xau_p07)
X07 = pd.DataFrame({k: np.log(sp[f"dk_{sym[k]}_p15"] / sp[f"dk_{sym[k]}_p07"]) for k in ("DXY", "TBOND", "SPX", "XAG", "USDJPY")})
sig["g12"] = g12; sig["g07"] = g07
for k in X12: sig[f"x12_{k}"] = X12[k]
imodels = {"DXY": ["DXY"], "TBOND": ["TBOND"], "SPX": ["SPX"], "MACRO3": ["DXY", "TBOND", "SPX"]}
for win, gg, XX in [("I12", g12, X12), ("I07", g07, X07)]:
    for m, cols in imodels.items():
        if win == "I07" and m != "MACRO3":
            continue
        for W in (60, 120, 250):
            rr = roll_resid(gg, XX[cols], W)
            c = f"{win}_{m}_W{W}"; sig[c] = rr.e / rr.sig
            sig[f"{win}F_{m}_W{W}"] = rr.fit / rr.sig
            meta.append(dict(col=c, fam="C_intraday", model=f"{win} {m}", W=W, k=1, info="t 15:00 UTC (12:00 ya da 07:00 -> 15:00)"))
    print(win, "ok", sig[f"{win}_MACRO3_W250"].notna().sum())

# hedefler
for h in (1, 3, 5):
    sig[f"sfwd{h}"] = sp[f"sfwd{h}"]
    sig[f"skip{h}"] = np.log(sp.xau_p15.shift(-h) / sp.xau_p16)  # 1 saat atlamalı spot hedef (15:00 görüntü gürültüsünden arındırılmış)
sig["xag_fwd1"] = np.log(sp.dk_XAGUSD_p15).diff().shift(-1)
for h in (3, 5):
    sig[f"xag_fwd{h}"] = fwd(np.log(sp.dk_XAGUSD_p15).diff(), h)
sig["xag_fwd1"] = fwd(np.log(sp.dk_XAGUSD_p15).diff(), 1)
sig.to_parquet(f"{OUT}/signals_spot.parquet")
pd.DataFrame(meta).to_csv(f"{OUT}/signals_meta.csv", index=False)
print(sig.shape, "yazıldı")
