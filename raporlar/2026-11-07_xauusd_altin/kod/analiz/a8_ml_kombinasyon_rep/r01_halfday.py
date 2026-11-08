"""Adım 1: uzlaşma saatinin gün gün doğrulanması (yarım gün / arife seansları).
Her VİOP günü için log(settle) − log(spot_H) farkını, komşu günlerin 15:00 bazına göre normalize edip hangi saatin uzlaşmaya
en yakın olduğunu bul. 15:00'ten belirgin önce uzlaşan günler (arife yarım günleri) → o günlerde 15:00 UTC öznitelikleri
giriş fiyatından SONRA bilinir (ileriye bakma)."""
import numpy as np, pandas as pd
OUT0=None
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
v = pd.read_parquet(f"{OUT}/base_viop.parquet")
h = pd.read_parquet(f"{S}/panel/duka/XAUUSD.parquet").c; h.index = h.index + pd.Timedelta(hours=1)  # Ekim-Kasım 2026 yaması burada yok (yalnız 15:00 kontrolü için önemsiz)
def at(dts, H):
    t = pd.DatetimeIndex(dts).tz_localize("UTC") + pd.Timedelta(hours=H)
    i = h.index.searchsorted(t, side="right") - 1
    ok = (i >= 0); age = (t.values - h.index.values[np.clip(i, 0, None)]) / np.timedelta64(1, "h")
    return pd.Series(np.where(ok & (age <= 1), h.values[np.clip(i, 0, None)], np.nan), index=pd.DatetimeIndex(dts))
D = pd.DataFrame({f"d{H}": np.log(v.settle) - np.log(at(v.index, H)) for H in range(7, 19)})
# referans baz: önceki ve sonraki 5 günün 15:00 bazının medyanı (aynı kontrat varsayımı yaklaşık; roll günlerinde gürültü)
ref = pd.concat([D.d15.shift(k) for k in (-5, -4, -3, -2, -1, 1, 2, 3, 4, 5)], axis=1).median(axis=1)
E = D.sub(ref, axis=0).abs() * 1e4
best = E.fillna(1e9).idxmin(axis=1).where(E.notna().any(axis=1), "none")
flag = (best.isin(["d8", "d9", "d10", "d11", "d12"])) & (E.d15 > 3 * E.min(axis=1)) & (E.d15 > 15)
hd = E[flag].copy(); hd["best"] = best[flag]
pd.set_option("display.width", 250)
print("15:00'ten belirgin önce uzlaşan gün sayısı:", int(flag.sum()))
print(hd[["d9", "d10", "d11", "d12", "d14", "d15", "d16", "best"]].round(1).to_string())
print("tarih (ay-gün) dağılımı:", pd.Series(hd.index.strftime("%m-%d")).value_counts().head(10).to_dict())
hd.to_csv(f"{OUT}/halfday_candidates.csv")
pd.Series(flag, name="halfday").to_frame().to_parquet(f"{OUT}/halfday_flag.parquet")
