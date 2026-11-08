#!/usr/bin/env python3
"""Bağımsız yeniden üretim, adım 1: ham tablolardan VİOP aktif kontrat getirisi ve spot 15:00 UTC serisi.
lib_altin / analist kodu KULLANILMAZ. Çıktı: base.parquet (VİOP günleri), spot.parquet (spot takvimi).
"""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
OUT = f"{S}/out/a1_zaman_serisi_rep"

# ---------- VİOP: ham bülten satırları ----------
L = pd.read_parquet(f"{S}/panel/viop_long.parquet")
X = L[(L.root == "XAUUSD") & L.code.str.startswith("F_XAUUSD")].copy()
X["date"] = pd.to_datetime(X.date)
X = X.sort_values(["date", "code"])
dates = pd.DatetimeIndex(sorted(X.date.unique()))
settle = X.pivot_table(index="date", columns="code", values="settle", aggfunc="last").reindex(dates)
prevs = X.pivot_table(index="date", columns="code", values="prev_settle", aggfunc="last").reindex(dates)
oi = X.pivot_table(index="date", columns="code", values="oi", aggfunc="last").reindex(dates)
expiry = X.groupby("code").expiry.last()

# aktif kontrat gün t = gün t-1'de açık pozisyonu en büyük olan (ve gün t'de hâlâ listelenen) kontrat
act = []
for i, t in enumerate(dates):
    if i == 0:
        act.append(np.nan); continue
    o = oi.iloc[i - 1].dropna()
    o = o[o.index.isin(settle.columns[settle.iloc[i].notna()])]
    act.append(o.idxmax() if len(o) else np.nan)
act = pd.Series(act, index=dates)
st = pd.Series([settle.at[t, c] if isinstance(c, str) else np.nan for t, c in act.items()], index=dates)
ps = pd.Series([prevs.at[t, c] if isinstance(c, str) else np.nan for t, c in act.items()], index=dates)
# önceki uzlaşmayı kendim de bul (aynı kontratın t-1 settle'ı)
ps_own = pd.Series([settle.iloc[i - 1][c] if (i > 0 and isinstance(c, str)) else np.nan for i, (t, c) in enumerate(act.items())], index=dates)
v_ret = np.log(st / ps)
B = pd.DataFrame(dict(code=act, settle=st, prev_settle=ps, prev_settle_own=ps_own, v_ret=v_ret,
                      expiry=act.map(expiry)), index=dates)
B["v_ret_own"] = np.log(B.settle / B.prev_settle_own)
for h in [1, 3, 5]:
    B[f"fwd{h}"] = sum(B.v_ret.shift(-k) for k in range(1, h + 1))
B["roll"] = B.code != B.code.shift(1)

# ---------- spot: Dukascopy saatlik, fiyat anı = bar başlangıcı + 1 saat ----------
H = pd.read_parquet(f"{S}/panel/duka/XAUUSD.parquet")
H.index = pd.DatetimeIndex(H.index).tz_convert("UTC").tz_localize(None)
H = H[~H.index.duplicated(keep="last")]
def at_hour(hh):  # gün D'nin hh:00 UTC fiyatı = (hh-1):00 başlangıçlı barın kapanışı
    b = H[H.index.hour == hh - 1].c
    b.index = b.index.normalize(); return b
p15 = at_hour(15)
p15 = p15[p15.index.dayofweek < 5]
# Dukascopy saatlik dosyası 2026-10-30'da bitiyor -> sonrası dakikalık veriden (14:59 başlangıçlı dakika barının kapanışı)
M = pd.read_parquet(f"{S}/panel/duka_min_XAUUSD.parquet")
M.index = pd.DatetimeIndex(M.index)
mm = M[(M.index.hour == 14) & (M.index.minute == 59)].c; mm.index = mm.index.normalize()
extra = mm[(mm.index > p15.index.max()) & (mm.index.dayofweek < 5)]
p15 = pd.concat([p15, extra]).sort_index()
# saatlik diğer saatler (zaman kalibrasyonu için)
HR = pd.DataFrame({hh: at_hour(hh) for hh in range(8, 22)})
SP = pd.DataFrame(dict(p15=p15))
SP = SP[SP.index >= "2010-01-01"]
SP.to_parquet(f"{OUT}/spot.parquet"); HR.to_parquet(f"{OUT}/spot_hours.parquet")
B.to_parquet(f"{OUT}/base.parquet")

# ---------- panel ile karşılaştırma ----------
pv = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index)
psn = pd.read_parquet(f"{S}/panel/panel_spot.parquet"); psn.index = pd.to_datetime(psn.index)
c = B.join(pv[["v_code", "v_ret", "fwd1", "fwd3", "fwd5", "xau_p15"]], rsuffix="_pan", how="outer")
print("VİOP gün sayısı: mine", len(B), "panel", len(pv), "ortak", len(B.index.intersection(pv.index)))
print("kod uyuşmazlığı:", int((c.code != c.v_code).sum()), " v_ret maks fark:", float((c.v_ret - c.v_ret_pan).abs().max()))
for h in [1, 3, 5]: print(f"fwd{h} maks fark:", float((c[f'fwd{h}'] - c[f'fwd{h}_pan']).abs().max()))
print("prev_settle bülten vs kendi t-1 settle farklı gün:", int(((B.prev_settle - B.prev_settle_own).abs() > 1e-9).sum()),
      "| roll günü:", int(B.roll.sum()))
bad = B[((B.prev_settle - B.prev_settle_own).abs() > 1e-9)]
print(bad.head(10))
print("spot gün sayısı mine", len(SP), "panel", len(psn), "sadece mine", len(SP.index.difference(psn.index)), "sadece panel", len(psn.index.difference(SP.index)))
print(" sadece mine örnek:", list(SP.index.difference(psn.index)[:20]))
print(" sadece panel örnek:", list(psn.index.difference(SP.index)[:20]))
j = SP.join(psn.s_p15, how="inner"); print("s_p15 maks göreli fark:", float((j.p15 / j.s_p15 - 1).abs().max()))
jj = pv.xau_p15.to_frame().join(SP.p15, how="left"); print("panel_viop xau_p15 vs mine maks göreli fark:", float((jj.xau_p15 / jj.p15 - 1).abs().max()),
      "| panel VİOP gününde benim spotum yok:", int(jj.p15.isna().sum()), list(jj.index[jj.p15.isna()][:15]))
