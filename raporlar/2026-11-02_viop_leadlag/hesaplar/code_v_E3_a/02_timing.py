"""(b) zamanlama/ileriye bakma denetimi + (c) alternatif giriş (saatlik ilk bar kapanışı, 5dk) + VİOP vadeli gün-içi.
"""
import numpy as np, pandas as pd, glob, os
import vlib as V

out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)

X = pd.read_parquet(V.RES + "/panel_E3.parquet")
cal = V.bist_cal()

# ---------- (b1) ABD günlük ldate = ABD işlem tarihi mi? (FX tipi kayma var mı?) ----------
P("== (b1) Günlük ABD kapanışı vs saatlik son bar (ldate kayması kontrolü)")
for s in ["VLO", "XLE", "ES=F", "BZ=F"]:
    h = V.raw(s, "h1").copy(); d = V.by_ldate(s)
    h["ld"] = pd.DatetimeIndex(h["ldate"].values)
    last = h.groupby("ld").apply(lambda x: pd.Series({"c": x.c.iloc[-1], "t_end": x.index[-1]}))
    j = pd.concat([d.c.rename("dc"), last], axis=1, join="inner").dropna()
    j["rel"] = (j.dc / j.c.astype(float) - 1).abs()
    # gece fiyatıyla eşleşme (bir sonraki gün) alternatifi
    nxt = (d.c.shift(-1).reindex(j.index) / j.c.astype(float) - 1).abs()
    tt = pd.DatetimeIndex(j.t_end).tz_convert("UTC")
    P(f"{s}: n={len(j)} | günlük c == saatlik son bar c (|fark|<5bp) oranı={float((j.rel<5e-4).mean()):.3f} | (bir sonraki günle eşleşme={float((nxt<5e-4).mean()):.3f}) | "
      f"son bar başlangıç saati UTC dağılımı={pd.Series(tt.strftime('%H:%M')).value_counts().head(4).to_dict()}")
P("Not: ABD hisse son bar 19:00/20:00 UTC başlangıçlı -> kapanış 20:00 (yaz)/21:00 (kış) UTC; BIST açılış müzayedesi 06:55-07:00 UTC (2016 sonrası). "
  "2014-2016 kış: BIST UTC+2 -> açılış 07:55 UTC. Her durumda t-1 ABD kapanışı ile t BIST açılışı arasında >= 10 saat.")

# hangi ABD tarihi kullanılıyor: sigA(t) penceresi
d = V.by_ldate("VLO"); usd = d.index
pos_hi = usd.searchsorted(cal, side="right") - 1
last_us_le = pd.Series(usd[np.clip(pos_hi, 0, None)], index=cal)
# sigA(t) = r_A(t-1): pencere (last_us<=t-2, last_us<=t-1]; bitiş tarihi = last_us<=t-1
endA = last_us_le.shift(1)
viol = (endA >= pd.Series(cal, index=cal)).sum()
P(f"(b1) sigA penceresinin bitişi (ABD tarihi) >= BIST t olan gün sayısı (ileriye bakma): {int(viol)} / {len(cal)}")
pos_lt = usd.searchsorted(cal, side="left") - 1
last_us_lt = pd.Series(usd[np.clip(pos_lt, 0, None)], index=cal)
P(f"(b1) sigA'nın açılışta bilinen en son ABD kapanışını KAÇIRDIĞI gün (BIST tatili sonrası, sigB farkı): {int((endA < last_us_lt)[cal >= '2014'].sum())}")
P(f"(b1) ABD tatili nedeniyle sigA=0 (ABD işlem yok) gün sayısı 2014+: {int((X.US.abs() < 1e-12).sum())}")

# ---------- (b2) Yahoo BIST açılışı = açılış müzayedesi fiyatı mı? ----------
P("\n== (b2) TUPRS günlük o vs saatlik 06:30 bar o (2023-11+) ve 5dk 06:55 müzayede barı (son ~60 gün)")
th = V.raw("TUPRS.IS", "h1").copy(); th["ld"] = pd.DatetimeIndex(th["ldate"].values)
dd = V.by_ldate("TUPRS.IS")
fb = th[(th.index.hour == 6) & (th.index.minute == 30)].set_index("ld")
j = pd.concat([dd.o.rename("do"), dd.c.shift(1).rename("pc"), fb.o.rename("h_o"), fb.c.rename("h_c"), fb.v.rename("h_v")], axis=1, join="inner").dropna()
P(f"n={len(j)} | günlük o == h1 ilk bar o: {float((j.do==j.h_o).mean()):.3f} | o == önceki kapanış: {float((j.do==j.pc).mean()):.3f} | h1 ilk bar hacmi 0 oranı: {float((j.h_v==0).mean()):.3f}")
tm = V.raw("TUPRS.IS", "m5").copy(); tm["ld"] = pd.DatetimeIndex(tm["ldate"].values)
m_auc = tm[(tm.index.hour == 6) & (tm.index.minute == 55)].set_index("ld")
j2 = pd.concat([dd.o.rename("do"), m_auc.o.rename("auc")], axis=1, join="inner").dropna()
P(f"5dk 06:55 (müzayede) barı: n={len(j2)} | günlük o == müzayede fiyatı: {float((j2.do==j2.auc).mean()):.3f}")

# ---------- (c) Alternatif girişler (saatlik, 2023-11-30+) ----------
P("\n== (c) Alternatif giriş: E0 = günlük o (açılış müzayedesi), E1 = 06:30 barı kapanışı (07:30 UTC = 10:30 TSİ), E2 = 07:30 barı kapanışı (11:30 TSİ); çıkış = günlük c (kapanış müzayedesi)")
def hourly_close_at(sym, hh, mm):
    h = V.raw(sym, "h1").copy(); h["ld"] = pd.DatetimeIndex(h["ldate"].values)
    b = h[(h.index.hour == hh) & (h.index.minute == mm)]
    b = b[~b.ld.duplicated(keep="last")].set_index("ld")
    return b.c
tuD = V.bist_decomp("TUPRS.IS"); x30D = V.bist_decomp("XU030.IS"); xuD = V.bist_decomp("XU100.IS")
E1 = hourly_close_at("TUPRS.IS", 6, 30); E2 = hourly_close_at("TUPRS.IS", 7, 30)
X1 = hourly_close_at("XU030.IS", 6, 30); X2 = hourly_close_at("XU030.IS", 7, 30)
H = pd.DataFrame({"o": tuD.o, "c": tuD.c, "E1": E1, "E2": E2, "xo": x30D.o, "xc": x30D.c, "X1": X1, "X2": X2}).dropna()
H = H[H.index >= "2023-11-30"]
H["r0"] = np.log(H.c / H.o); H["r1"] = np.log(H.c / H.E1); H["r2"] = np.log(H.c / H.E2); H["first"] = np.log(H.E1 / H.o)
H["h0"] = H.r0 - np.log(H.xc / H.xo); H["h1"] = H.r1 - np.log(H.xc / H.X1); H["h2"] = H.r2 - np.log(H.xc / H.X2)
H["first_h"] = H["first"] - np.log(H.X1 / H.xo)
# temizlik: günlük intra NaN olan günleri at
H = H[tuD.intra.reindex(H.index).notna()]
H = H.join(X[["US", "USB", "VLO", "ES", "BZ"]], how="left")
P(f"n gün={len(H)} ({H.index.min().date()}–{H.index.max().date()})")
for tgt in ["r0", "first", "r1", "r2", "h0", "first_h", "h1", "h2"]:
    r, ti, tn, n = V.corr_t(H[tgt], H.US)
    m = V.hac(H[tgt], H[["US", "ES", "BZ"]])
    P(f"  {tgt:8s}: corr(US_REF_t-1)={r:.3f} t_NW={tn:.2f} | reg +ES+BZ: b_US={m.params.US:.3f} t={m.tvalues.US:.2f} | n={n}")
# z-sinyali TÜM geçmişten (2014+) hesaplanır, sonra son döneme kısıtlanır
sig = X.US
_, posall = V.positions(sig, X.y)  # X.y hizalaması için; pos indeksi X.y ile ortak günler
pos = posall.reindex(H.index).fillna(0)
P("  Z1 backtest (aynı günler, brüt bps/işlem, NW t):")
for tgt, lab in [("r0", "E0 açılış müzayedesi"), ("r1", "E1 10:30 TSİ"), ("r2", "E2 11:30 TSİ"), ("first", "ilk saat (o->10:30)"),
                 ("h0", "E0 hedge XU030"), ("h1", "E1 hedge XU030"), ("h2", "E2 hedge XU030")]:
    g = (pos * H[tgt])[pos != 0]; m, t, n = V.nw_mean(g)
    P(f"    {lab:24s}: n={n} ort={1e4*m:.1f} bps t={t:.2f} | 8bps net={1e4*m-8*(2 if 'hedge' in lab else 1):.1f} | 15bps net={1e4*m-15*(2 if 'hedge' in lab else 1):.1f}")
H.to_parquet(V.RES + "/hourly_entries.parquet")

# 5dk: son ~60 gün, giriş 07:05 UTC (ilk sürekli işlem 5dk barı kapanışı) — küçük örnek, sadece bilgi
m5 = V.raw("TUPRS.IS", "m5").copy(); m5["ld"] = pd.DatetimeIndex(m5["ldate"].values)
b = m5[(m5.index.hour == 7) & (m5.index.minute == 0)].set_index("ld").c.rename("e5")
M = pd.concat([tuD.o, tuD.c, b], axis=1, join="inner").dropna().join(X[["US"]])
M = M.join(pos.rename("pos"), how="left"); M["pos"] = posall.reindex(M.index).fillna(0)
M["r0"] = np.log(M.c / M.o); M["r5"] = np.log(M.c / M.e5)
g0 = (M.pos * M.r0)[M.pos != 0]; g5 = (M.pos * M.r5)[M.pos != 0]
P(f"  5dk (n gün={len(M)}, işlem={len(g0)}): E0 ort={1e4*g0.mean():.1f} bps | 10:05 TSİ giriş ort={1e4*g5.mean():.1f} bps (örnek çok küçük, bilgi amaçlı)")

# ---------- (b3) Bilgi zamanı: VLO saatlik ile ABD getirisini BIST kapanışı öncesi/sonrası parçalara ayır ----------
P("\n== (b3) VLO_t-1 = [ABD kapanış t-2 -> 15:00 UTC t-1 (BIST seansı içinde biliniyor)] + [15:00 UTC t-1 -> ABD kapanış t-1 (BIST kapanışı sonrası)]")
vh = V.raw("VLO", "h1").copy(); vh["ld"] = pd.DatetimeIndex(vh["ldate"].values)
vend = vh.index + pd.Timedelta(minutes=60)
vend = vend.where(~((vh.index.hour.isin([19, 20])) & (vh.index.minute == 0) & (vh.v == 0)), vh.index)  # 0 hacimli kapanış barı = an
vs = pd.Series(vh.c.values, index=vend).sort_index(); vs = vs[~vs.index.duplicated(keep="last")]
vd = V.by_ldate("VLO").c
rows = []
cl = vd.index
for i in range(1, len(cl)):
    t1 = cl[i]; t2 = cl[i - 1]
    snap = pd.Timestamp(t1).tz_localize("UTC") + pd.Timedelta(hours=15)
    k = vs.index.searchsorted(snap, side="right") - 1
    if k < 0 or vs.index[k] < snap - pd.Timedelta(hours=2) or vs.index[k].date() != t1.date(): continue
    rows.append((t1, np.log(vs.iloc[k] / vd.loc[t2]), np.log(vd.loc[t1] / vs.iloc[k])))
S = pd.DataFrame(rows, columns=["usdate", "pre", "post"]).set_index("usdate")
# BIST günü t için: ABD tarihi = t-1 BIST günü ile aynı olmalı (tatil karmaşası olan günleri at)
calS = pd.Series(cal, index=cal); prevb = calS.shift(1)
Z = pd.DataFrame({"prev": prevb}).join(X[["y", "y_h", "gap", "US", "ES", "BZ", "VLO"]], how="inner")
Z = Z.join(S, on="prev", how="inner").dropna()
P(f"n={len(Z)} ({Z.index.min().date()}–{Z.index.max().date()}) | pre+post vs VLO_t-1 (günlük) corr={np.corrcoef(Z.pre+Z.post, Z.VLO)[0,1]:.3f}")
for tgt in ["gap", "y", "y_h"]:
    m = V.hac(Z[tgt], Z[["pre", "post"]]); P(f"  {tgt:4s} ~ pre + post: b_pre={m.params.pre:.3f} (t {m.tvalues.pre:.2f}) | b_post={m.params.post:.3f} (t {m.tvalues.post:.2f})")
    m = V.hac(Z[tgt], Z[["VLO"]]); P(f"  {tgt:4s} ~ VLO_t-1 (aynı alt örnek): b={m.params.VLO:.3f} t={m.tvalues.VLO:.2f}")

# ---------- (c2) VİOP TUPRS vadelisi gün-içi (bülten: açılış fiyatı -> kapanış/uzlaşma) ----------
P("\n== (c2) VİOP F_TUPRS ön vade (en yüksek işlem hacmi) gün-içi: açılış fiyatı -> uzlaşma ve kapanış (bülten günleri)")
rows = []
for f in sorted(glob.glob(V.DATA + "/viop/viop_*.csv")):
    try:
        df = pd.read_csv(f, sep=";", encoding="windows-1254", skiprows=[1], dtype=str)
    except Exception as e:
        continue
    df.columns = [c.strip() for c in df.columns]
    q = df[df["SOZLESME KODU"].str.startswith("F_TUPRS", na=False)]
    if q.empty: continue
    q = q.copy()
    for c in ["UZLASMA FIYATI", "ACILIS FIYATI", "KAPANIS FIYATI", "ISLEM HACMI", "ISLEM SAYISI", "ONCEKI UZLASMA FIYATI", "ACILIS SEANSI FIYATI"]:
        q[c] = pd.to_numeric(q[c].str.replace(",", "."), errors="coerce") if c in q else np.nan
    q = q.sort_values("ISLEM HACMI", ascending=False).iloc[0]
    rows.append((pd.Timestamp(q["TARIH"]), q["SOZLESME KODU"], q["ACILIS FIYATI"], q["KAPANIS FIYATI"], q["UZLASMA FIYATI"], q["ISLEM HACMI"], q["ISLEM SAYISI"], q["ACILIS SEANSI FIYATI"]))
F = pd.DataFrame(rows, columns=["date", "kod", "o", "c", "settle", "hacim_tl", "islem", "acs"]).set_index("date")
F = F[(F.o > 0) & (F.c > 0)]
F["r_fc"] = np.log(F.c / F.o); F["r_fs"] = np.log(F.settle / F.o)
F = F.join(X[["US", "y"]], how="inner")
F["pos"] = posall.reindex(F.index).fillna(0)
P(f"bülten günü={len(F)} | medyan ön vade işlem hacmi={F.hacim_tl.median()/1e6:.0f} mn TL, medyan işlem sayısı={F.islem.median():.0f}")
P(f"corr(vadeli o->c, spot intra)={F.r_fc.corr(F.y):.3f} | corr(US_REF_t-1, vadeli o->c)={F.r_fc.corr(F.US):.3f} vs spot aynı günler={F.y.corr(F.US):.3f}")
for tgt in ["r_fc", "r_fs", "y"]:
    g = (F.pos * F[tgt])[F.pos != 0]; m, t, n = V.nw_mean(g)
    P(f"  Z1 {tgt}: n={n} ort={1e4*m:.1f} bps t={t:.2f}")
F.to_csv(V.RES + "/viop_tuprs_front.csv")
open(V.RES + "/02_timing.txt", "w").write("\n".join(out))
