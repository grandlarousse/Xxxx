"""Bağımsız yeniden üretim — adım 0: ham tablolardan hedef ve spot fiyatlarını kur, panel ile karşılaştır.
Kaynak: viop_long.parquet (XAUUSD kontrat satırları), duka/XAUUSD.parquet (saatlik BID, index = bar başlangıcı UTC).
Çıktı: base.parquet (gün endeksi = VİOP XAUUSD işlem günleri) — v_ret, aktif kontrat, fwd1/3/5, spot p07/p10/p12/p15/p20 (kendi hesabım).
"""
import os, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
O = f"{S}/out/a3_takvim_olay_rep"

L = pd.read_parquet(f"{S}/panel/viop_long.parquet")
x = L[(L.root == "XAUUSD") & L.code.str.startswith("F_XAUUSD")].copy()
x["date"] = pd.to_datetime(x.date)
days = pd.DatetimeIndex(sorted(x.date.unique()))
print("VİOP XAUUSD günleri:", len(days), days[0].date(), days[-1].date())
oi = x.pivot_table(index="date", columns="code", values="oi", aggfunc="first").reindex(days)
st = x.pivot_table(index="date", columns="code", values="settle", aggfunc="first").reindex(days)
ps = x.pivot_table(index="date", columns="code", values="prev_settle", aggfunc="first").reindex(days)
# aktif kontrat gün t = gün t-1'de OI en büyük kontrat (ileriye bakmasız); ilk gün: kendi OI'si
oi_prev = oi.shift(1)
oi_prev.iloc[0] = oi.iloc[0]
act = oi_prev.fillna(-1).idxmax(axis=1)
# aynı kontrat içinde getiri: settle_t / settle_{t-1} (aynı kontrat); prev_settle sütunuyla da
s_t = np.array([st.loc[d, c] for d, c in act.items()])
s_tm1 = np.array([st.shift(1).loc[d, c] if i > 0 else np.nan for i, (d, c) in enumerate(act.items())])
p_t = np.array([ps.loc[d, c] for d, c in act.items()])
B = pd.DataFrame(index=days)
B["code"] = act.values
B["settle"] = s_t
B["ret_own"] = np.log(s_t / s_tm1)
B["ret_prev"] = np.log(s_t / p_t)
print("ret_own vs ret_prev (bulten prev_settle) max |fark|:", np.nanmax(np.abs(B.ret_own - B.ret_prev)))
B["ret"] = B.ret_own.fillna(B.ret_prev)
B["vol"] = [x.set_index(["date", "code"]).volume.get((d, c), np.nan) for d, c in act.items()]
for h in (1, 3, 5, 10):
    B[f"fwd{h}"] = sum(B.ret.shift(-k) for k in range(1, h + 1))

# spot: Dukascopy saatlik; fiyat anı HH:00 = index (HH-1):00 barının kapanışı
H = pd.read_parquet(f"{S}/panel/duka/XAUUSD.parquet")
H.index = H.index.tz_convert(None)
cl = H["c"].copy(); cl.index = cl.index + pd.Timedelta(hours=1)   # damga = fiyat anı
for hh in (7, 10, 12, 13, 14, 15, 16, 20):
    want = days + pd.Timedelta(hours=hh)
    B[f"p{hh:02d}"] = cl.reindex(want).values
# ertesi bar boşluğu: tam saat yoksa NaN kalır
print("spot NaN sayısı p12/p15:", B.p12.isna().sum(), B.p15.isna().sum())

# panel ile karşılaştır
P = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); P.index = pd.to_datetime(P.index)
cmp = pd.concat([B[["code", "ret", "fwd1", "fwd3", "fwd5", "p12", "p15", "p20"]],
                 P[["v_code", "v_ret", "fwd1", "fwd3", "fwd5", "xau_p12", "xau_p15", "xau_p20"]].add_prefix("P_")], axis=1)
print("gün sayısı: ben", len(B), "panel", len(P), "ortak", len(B.index.intersection(P.index)))
print("aktif kontrat farklı gün:", int((cmp.code != cmp.P_v_code).sum()))
for a, b in [("ret", "P_v_ret"), ("fwd1", "P_fwd1"), ("fwd3", "P_fwd3"), ("fwd5", "P_fwd5"), ("p12", "P_xau_p12"), ("p15", "P_xau_p15"), ("p20", "P_xau_p20")]:
    dd = (cmp[a] - cmp[b]).abs()
    print(f"  {a:5s} vs {b:10s}: max|fark|={dd.max():.3g}  >1e-9 olan={int((dd > 1e-9).sum())}  NaN(ben/panel)={cmp[a].isna().sum()}/{cmp[b].isna().sum()}")
diff_code = cmp[cmp.code != cmp.P_v_code]
if len(diff_code): print(diff_code[["code", "P_v_code", "ret", "P_v_ret"]].head(20))

# dakikalık veriyle saat damgası kalibrasyonu: p15 (bar 14:00 kapanışı) dakika 14:59 kapanışına mı eşit?
M = pd.read_parquet(f"{S}/panel/duka_min_XAUUSD.parquet")
mdays = pd.DatetimeIndex(sorted(set(M.index.normalize()))).intersection(days)
rows = []
for d0 in mdays:
    for lab, ts in [("m14:59", d0 + pd.Timedelta("14:59:00")), ("m15:00", d0 + pd.Timedelta("15:00:00")), ("m15:59", d0 + pd.Timedelta("15:59:00"))]:
        rows.append(dict(d=d0, lab=lab, v=M.c.get(ts, np.nan)))
mm = pd.DataFrame(rows).pivot(index="d", columns="lab", values="v")
mm["p15"] = B.p15.reindex(mm.index)
for c in ["m14:59", "m15:00", "m15:59"]:
    print(f"  dakika kalibrasyonu: |log(p15/{c})| medyan bps = {(np.log(mm.p15 / mm[c]).abs().median() * 1e4):.2f}  (n={mm[c].notna().sum()})")

# uzlaşma hangi saate yakın? (yarım gün tespiti için) — saatlik spot ile |log(settle/spot_HH)|
for hh in (10, 12, 15):
    print(f"  medyan |log(settle/p{hh})| bps: {(np.log(B.settle / B[f'p{hh:02d}'])).abs().median() * 1e4:.1f}")
B.to_parquet(f"{O}/base.parquet")
print("yazıldı:", f"{O}/base.parquet")
