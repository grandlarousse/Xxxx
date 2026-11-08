"""s3: Dukascopy saatlik — x'in belirli UTC pencerelerindeki hareketi ve altının aynı penceredeki hareketinden sapması → VİOP fwd1/3/5.
Pencereler (gün t satırı; t-1 = panelin bir önceki VİOP günü):
  A: [t-1 15:00, t-1 20:00]  ABD öğleden sonrası (VİOP t-1 uzlaşmasından sonra, ABD kapanışına kadar)
  B: [t-1 15:00, t 15:00]    tam 24 saat (karar anında biter)
  C: [t-1 20:00, t 15:00]    ABD kapanışı sonrası → karar anı (gece + Asya + Avrupa)
Ölçüler: raw = z(x penceresi); gap = β·x − altın (β: altın~x pencere regresyonu, önceki 250 gün, geçmiş-yalnız) → 'altın x'e göre geride kaldı' → +.
Tanı: gap_A → altın C penceresi (karar anından önce 'kapanma' oluyor mu; işlem yapılamaz).
Fiyat anı: Dukascopy bar başlangıcı + 1 saat. 15:00 fiyatı ≤ karar anı (15:00 dahil)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz")
from a4_common import *

reg_reset("s3_")
d = load_viop()
idx = d.index
prev = pd.Series(idx, index=idx).shift(1)

def win_ret(sym):
    p15 = px_at(sym, 15); p20 = px_at(sym, 20)
    a15 = p15.reindex(idx).values; a20 = p20.reindex(idx).values
    pv15 = p15.reindex(prev.values).values; pv20 = p20.reindex(prev.values).values
    A = pd.Series(np.log(pv20 / pv15), index=idx)
    B = pd.Series(np.log(a15 / pv15), index=idx)
    C = pd.Series(np.log(a15 / pv20), index=idx)
    return dict(A=A, B=B, C=C)

G = win_ret("XAUUSD")
# kontrol: 15:00 Dukascopy saatlik ≈ panel xau_p15
chk = pd.concat([px_at("XAUUSD", 15).reindex(idx), d.xau_p15], axis=1).dropna()
print("duka15 vs xau_p15 max |log fark|:", float(np.abs(np.log(chk.iloc[:, 0] / chk.iloc[:, 1])).max()))
SYMS = ["DOLLARIDXUSD", "USTBONDTRUSD", "USA500IDXUSD", "XAGUSD", "BRENTCMDUSD", "COPPERCMDUSD", "VOLIDXUSD", "EURUSD", "USDJPY", "USDCNH", "BTCUSD"]
rows = []
for sym in SYMS:
    X = win_ret(sym)
    for w in ("A", "B", "C"):
        x = X[w].replace([np.inf, -np.inf], np.nan); g = G[w]
        b = (x.rolling(250, min_periods=150).cov(g) / x.rolling(250, min_periods=150).var()).shift(1)
        gap = b * x - g
        cand = {"raw": zscale(x), "gap": zscale(gap)}
        for m, sig in cand.items():
            for h in (1, 3, 5):
                s = split_stats(sig, d[f"fwd{h}"], h)
                reg("s3_pencere", f"s3_{sym}_{w}_{m}_h{h}", f"{m}[{sym}] pencere {w}", h, s, note="duka saatlik")
                rows.append(dict(sym=sym, win=w, m=m, h=h, ic=s["ic"], t=s["t"], t_is=s["t_is"], t_oos=s["t_oos"], yrs=f"{s['yrs_same_sign']}/{s['yrs']}", n=s["n"]))
            if w == "A":
                s = split_stats(sig, G["C"], 1)
                reg("s3_emilim", f"s3_emilim_{sym}_{m}", f"{m}[{sym}] A -> altin C", 0, s, note="tani; islem yapilamaz")
                rows.append(dict(sym=sym, win="A->C", m=m, h=0, ic=s["ic"], t=s["t"], t_is=s["t_is"], t_oos=s["t_oos"], yrs=f"{s['yrs_same_sign']}/{s['yrs']}", n=s["n"]))
# altının kendi pencere getirileri (referans)
for w in ("A", "B", "C"):
    for h in (1, 3, 5):
        s = split_stats(zscale(G[w]), d[f"fwd{h}"], h)
        reg("s3_oz", f"s3_XAU_{w}_raw_h{h}", f"raw[XAUUSD] pencere {w}", h, s, note="oz gecikme referansi")
        rows.append(dict(sym="XAUUSD", win=w, m="raw", h=h, ic=s["ic"], t=s["t"], t_is=s["t_is"], t_oos=s["t_oos"], yrs=f"{s['yrs_same_sign']}/{s['yrs']}", n=s["n"]))
res = pd.DataFrame(rows); res.to_csv(f"{OUT}/s3_saatlik_pencere.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
print("test sayısı:", len(res))
print(res[(res.t.abs() >= 2) | (res.t_is.abs() >= 2)].round(3).to_string())
print("\nEmilim tanısı:"); print(res[res.h == 0].round(3).to_string())
print("\nAltın öz:"); print(res[res.sym == "XAUUSD"].round(3).to_string())
