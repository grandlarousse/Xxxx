"""E3-5: BIST altın BYF primi (bağımsız). Analist tanımının kopyası + temiz zamanlı sürümler + yaz/kış ayrımı."""
from rc import *
import warnings; warnings.filterwarnings("ignore")
def duka(sym):
    x = pd.read_parquet(f"{P}/duka/{sym}.parquet")["c"]; x.index = x.index + pd.Timedelta(hours=1); return x[~x.index.duplicated()]
xau = xau_hourly(); usd = duka("USDTRY")
yu = pd.read_parquet(f"{P}/yahoo_h/USDTRY_X.parquet")["close"]; yu.index = yu.index + pd.Timedelta(hours=1)
usd = usd.combine_first(yu[yu.index > usd.index.max()])
G = (xau * usd.reindex(xau.index) / 31.1035).dropna()          # gram altın TL, tam saatlerde (fiyat anı)
def g_at(ts, mode="interp"):
    ts = pd.DatetimeIndex(ts); fl = ts.floor("h"); ce = ts.ceil("h")
    a = G.reindex(fl).values; b = G.reindex(ce).values
    if mode == "interp": return np.where(fl == ce, a, np.sqrt(a * b))     # analist: komşu iki saatin geometrik ortalaması (ceil = SONRAKİ saat)
    if mode == "past": return a                                            # yalnız geçmiş: floor saati
rows = []
for t in ["GLDTR", "ZGOLD", "ISGLK"]:
    h = pd.read_parquet(f"{OUT}/bist_{t}_1h.parquet"); h["day"] = h.index.normalize().tz_localize(None); h["hm"] = h.index.strftime("%H:%M")
    h = h[h.hm != "15:00"]
    gb = h.groupby("day")
    last_lab = gb.apply(lambda g: g.index[-1])
    close = gb.close.last(); summer = gb.hm.apply(lambda s: (s == "14:30").any())
    keep = last_lab.dt.strftime("%H:%M") >= "13:30"; days = close.index[keep]
    close = close[days]; summer = summer[days]; last_end = pd.DatetimeIndex(last_lab[days]) + pd.Timedelta(hours=1)
    px = {lab: h[h.hm == lab].set_index("day").close.reindex(days) for lab in ["12:30", "13:30", "14:30"]}   # bar kapanışı = lab + 1h
    D = lambda hhmm: pd.DatetimeIndex([pd.Timestamp(f"{d.date()} {hhmm}", tz="UTC") for d in days])
    g15 = pd.Series(G.reindex(D("15:00")).values, index=days)
    g1430i = pd.Series(g_at(D("14:30")), index=days); g1430p = pd.Series(g_at(D("14:30"), "past"), index=days)
    g1330i = pd.Series(g_at(D("13:30")), index=days)
    glast_i = pd.Series(g_at(last_end), index=days)
    # --- analist tanımı: kesim = son bar (başı ≤13:30) = 13:30 barı (kapanış 14:30); gram kesim = interp(14:30) [15:00 kullanır]
    ratio = close / g15; rmed = ratio.rolling(20, min_periods=10).median().shift(1)
    prem_A = np.log(px["13:30"] / (rmed * g1430i))
    r = np.log(close).diff(); rel_A = r - np.log(g15).diff()
    # --- B: aynı, gram kesim yalnız geçmiş (14:00 UTC), bilgi <=14:30
    prem_B = np.log(px["13:30"] / (rmed * g1430p))
    # --- C: temiz boşluk: sinyal 12:30 barı (kapanış 13:30) + gram interp(13:30) [<=14:00]; giriş/çıkış 13:30 barı kapanışı (14:30) hem BYF hem gram aynı an (interp 14:30)
    ratioC = px["13:30"] / g1430i; rmedC = ratioC.rolling(20, min_periods=10).median().shift(1)
    prem_C = np.log(px["12:30"] / (rmedC * g1330i))
    relC = np.log(px["13:30"]).diff() - np.log(g1430i).diff()
    # --- D: sinyal 13:30 barı (14:30) + gram 14:00 (geçmiş); hedef BYF son bar kapanışı (yaz 15:00, kış 14:30) ve gram AYNI an (interp)
    relD = np.log(close).diff() - np.log(glast_i).diff()
    tests = {"A_analist(interp g@14:30, hedef g@15:00)": (prem_A, rel_A), "B_gram14:00(geçmiş), hedef g@15:00": (prem_B, rel_A),
             "C_sinyal13:30->giriş14:30 (aynı an hedef)": (prem_C, relC), "D_sinyal14:30(g14:00)->hedef son bar, gram aynı an": (prem_B, relD)}
    for nm, (x, y) in tests.items():
        for hh in (1, 5):
            yy = fwd(y, hh)
            for seas, msk in [("hepsi", slice(None)), ("yaz(14:30 barı var)", summer.values), ("kış(son bar 14:30'da biter)", ~summer.values)]:
                xx = x[msk] if not isinstance(msk, slice) else x; yv = yy[msk] if not isinstance(msk, slice) else yy
                q = ic(xx, yv, max(hh, 5))
                rows.append(dict(etf=t, test=nm, h=hh, seas=seas, n=q["n"], ic=round(q["ic"], 3), t=round(q["t"], 2)))
    # A için yarı örneklem ve dilim
    if t == "GLDTR":
        for a_, b_ in [("2023-12-01", "2025-05-31"), ("2025-06-01", "2026-12-31")]:
            print("GLDTR A yarı", a_, ic(prem_A[a_:b_], fwd(rel_A, 1)[a_:b_], 5))
        dd = pd.concat([prem_A.rename("p"), fwd(rel_A, 1).rename("y1"), fwd(rel_A, 5).rename("y5")], axis=1).dropna()
        q5 = pd.qcut(dd.p, 5, labels=False)
        print("GLDTR A beşte birlik (bps):\n", (dd.groupby(q5).mean() * 1e4).round(1).to_string())
        dd = pd.concat([prem_C.rename("p"), fwd(relC, 1).rename("y1"), fwd(relC, 5).rename("y5")], axis=1).dropna()
        print("GLDTR C beşte birlik (bps):\n", (dd.groupby(pd.qcut(dd.p, 5, labels=False)).mean() * 1e4).round(1).to_string())
        # kışın kapanış = kesim fiyatı mı?
        print("kış günlerinde close == 13:30 bar kapanışı oranı:", float((close[~summer] == px["13:30"][~summer]).mean()), "| yaz:", float((close[summer] == px["13:30"][summer]).mean()))
        # mekanik bileşen: kışın gram 14:30->15:00 hareketi
        dg = np.log(g15 / g1430i)
        print("corr(prem_A, gram 14:30->15:00 hareketi) kış/yaz:", round(prem_A[~summer].corr(dg[~summer]), 3), round(prem_A[summer].corr(dg[summer]), 3),
              "| corr(rel_A_{t+1}, aynı hareket) kış/yaz:", round(fwd(rel_A, 1)[~summer].corr(dg[~summer]), 3), round(fwd(rel_A, 1)[summer].corr(dg[summer]), 3))
out = pd.DataFrame(rows); out.to_csv(f"{OUT}/r5_bist.csv", index=False)
pd.set_option("display.width", 250); print(out.pivot_table(index=["etf", "test", "h"], columns="seas", values=["ic", "t", "n"], aggfunc="first").to_string())
