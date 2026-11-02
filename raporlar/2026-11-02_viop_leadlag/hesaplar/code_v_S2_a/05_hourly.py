"""05: Saatlik (2023-12+) giriş zamanlaması ve saatlik iddia (TKC kapanış-sonrası -> TCELL 07:30->kapanış).
Saatlik bar zaman damgası = bar BAŞLANGICI (UTC). Fiyat 'an X' = X anında veya öncesinde KAPANMIŞ son barın kapanışı (kendi kodum).
BIST: 06:30 barı 07:30'da kapanır (açılış seansı + ilk 30 dk sürekli). Günlük 'o' = açılış seansı fiyatı (m5 06:55 barı ile doğrulandı)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_a")
from vs import *
pd.set_option("display.width", 250)
def px_at(sym, hhmm, kind="h1", maxage_h=3):
    d = rawd(sym, kind); d = d[~d.index.duplicated(keep="last")].sort_index()
    step = pd.Timedelta(minutes=60 if kind == "h1" else 5)
    end = d.index + step
    if sym.endswith(".IS") and kind == "h1":
        end = end.where(~((d.index.hour == 14) & (d.index.minute == 30)), d.index + pd.Timedelta(minutes=30))
        end = end.where(~((d.index.hour == 15) & (d.index.minute == 0)), d.index + pd.Timedelta(minutes=10))
    s = pd.Series(d["c"].values, index=end).sort_index()
    days = pd.DatetimeIndex(pd.DatetimeIndex(d["ldate"].values).unique()).sort_values()
    h, m = map(int, hhmm.split(":"))
    tg = (days + pd.Timedelta(hours=h, minutes=m)).tz_localize("UTC")
    pos = s.index.searchsorted(tg, side="right") - 1
    v = pd.Series(np.where(pos >= 0, s.values[np.clip(pos, 0, None)], np.nan), index=days)
    age = (tg - s.index[np.clip(pos, 0, None)]).total_seconds() / 3600
    v[(pos < 0) | (age > maxage_h)] = np.nan
    # aynı günün barı mı? (bar_end tarihi == gün)
    same = s.index[np.clip(pos, 0, None)].tz_convert(None).normalize() == days
    v[~same] = np.nan
    return v
df = pd.read_parquet(OUT + "/02_daily.parquet")
tc = bist_decomp("TCELL.IS")
p730 = px_at("TCELL.IS", "07:30"); p830 = px_at("TCELL.IS", "08:30")
tk1530 = px_at("TKC", "15:30"); fx1500 = px_at("TRY=X", "15:00"); fx2100 = px_at("TRY=X", "21:00"); fx0600 = px_at("TRY=X", "06:00")
H = df[df.index >= "2023-12-01"].copy()
H["p730_1"] = p730.reindex(tc.index).shift(-1).reindex(H.index)
H["p830_1"] = p830.reindex(tc.index).shift(-1).reindex(H.index)
H["fx21"] = fx2100.reindex(H.index); H["fx15"] = fx1500.reindex(H.index)
# Kendi FX'imle (saatlik 21:00 UTC) parite
H["P21"] = np.log(H.tkA * H.fx21 / (2.5 * H.tcA))
H["D21"] = H.P21 - H.P21.shift(1).rolling(20, min_periods=10).mean()
print("corr(D Yahoo-k1, D saatlik-21UTC) =", round(H[["D", "D21"]].corr().iloc[0, 1], 3), "n", H[["D", "D21"]].dropna().shape[0])
H["U_open"] = H.D - H.gap1
H["r_open_730"] = np.log(H.p730_1 / H.o1)
H["U_730"] = H.D - (np.log(H.p730_1 / H.c0) if "c0" in H else np.nan)
H["c0"] = tc.c.reindex(H.index)
H["U_730"] = H.D - np.log(H.p730_1 / H.c0) - (H.cc1 - np.log(H.c1 / H.c0)).fillna(0) * 0  # adj farkı (temettü günü) ihmal
H["U_830"] = H.D - np.log(H.p830_1 / H.c0)
H["y_open"] = H.intra1; H["y_730"] = np.log(H.c1 / H.p730_1); H["y_830"] = np.log(H.c1 / H.p830_1)
H = H[H.D.abs() < 0.15]
print("n gün (D, intra1, p730 mevcut):", H[["D", "intra1", "p730_1"]].dropna().shape[0], H.index.min().date(), "-", H.index.max().date())
print("\n=== Giriş zamanı karşılaştırması (aynı günler; 8 bps) ===")
z = H.dropna(subset=["D", "gap1", "intra1", "p730_1", "p830_1"])
for nm, sig, y in [("açılış, U_open", z.U_open, z.y_open), ("açılış, D (açılış bilgisi yok, MOO)", z.D, z.y_open),
                   ("07:30, U_730 (07:30'daki kalan sapma)", z.U_730, z.y_730), ("07:30, D", z.D, z.y_730),
                   ("07:30, U_open (açılışa göre sapma)", z.U_open, z.y_730), ("08:30, U_830", z.U_830, z.y_830)]:
    for thr in [0.0, 0.005]:
        r = bt(sig, y, 8, thr); r0 = bt(sig, y, 0, thr)
        print(f"{nm:42s} |>{thr*1e4:.0f}| n {r['n']:4d} brüt {r0['mean_bps']:6.1f} net {r['mean_bps']:6.1f} bps t {r['t']:5.2f} Sh {r['sharpe']:5.2f}")
# açılış->07:30 bacağının katkısı
pos = np.sign(z.U_open).where(z.U_open.abs() > 0.005, 0)
print(f"\n|U_open|>50 günlerinde: açılış->07:30 yön katkısı ort {1e4*(pos*z.r_open_730)[pos!=0].mean():.1f} bps; 07:30->kapanış {1e4*(pos*z.y_730)[pos!=0].mean():.1f} bps (brüt)")
for nm, X in [("U_open", "U_open"), ("U_730", "U_730")]:
    for y in ["y_open", "y_730"]:
        m, n = nw(z[y], z[[X]]); print(f"  {y} ~ {X}: b {m.params[X]:.3f} t {m.tvalues[X]:.2f} n {n}")
m, n = nw(z.y_730, z[["D", "gap1", "r_open_730"]]); print("  y_730 ~ D + gap1 + r(open->07:30):", m.params.round(3).to_dict(), "t", m.tvalues.round(2).to_dict())
m, n = nw(z.intra1, z[["D", "gap1"]]); print("  [aynı dönem] intra1 ~ D + gap1:", m.params.round(3).to_dict(), "t", m.tvalues.round(2).to_dict())
print("\n=== Saatlik iddia: tk_post = ln(TKC_kapanış / TKC_15:30) -> TCELL 07:30->kapanış (t+1) ===")
tkc = dser("TKC", "c")
H["tk_post"] = np.log(tkc.reindex(H.index) / tk1530.reindex(H.index))
H["fx_post"] = np.log(H.fx21 / H.fx15)
es = rawd("ES=F", "h1")
es15 = px_at("ES=F", "15:00"); es21 = px_at("ES=F", "20:00")
H["es_post"] = np.log(es21.reindex(H.index) / es15.reindex(H.index))
z = H.dropna(subset=["tk_post", "y_730"]); z = z[z.tk_post.abs() < 0.1]
for y in ["gap1", "y_730", "intra1"]:
    m, n = nw(z[y], z[["tk_post"]]); print(f"  {y} ~ tk_post: b {m.params['tk_post']:.3f} t {m.tvalues['tk_post']:.2f} n {n}")
m, n = nw(z.y_730, z[["tk_post", "gap1", "r_open_730"]]); print("  y_730 ~ tk_post + gap1 + r(open->07:30):", m.params.round(3).to_dict(), "t", m.tvalues.round(2).to_dict(), "n", n)
zz = z.dropna(subset=["es_post"]); m, n = nw(zz.y_730, zz[["tk_post", "es_post"]]); print("  y_730 ~ tk_post + es_post:", m.params.round(3).to_dict(), "t", m.tvalues.round(2).to_dict(), "n", n)
m, n = nw(z.y_730, z[["tk_post", "D"]]); print("  y_730 ~ tk_post + D:", m.params.round(3).to_dict(), "t", m.tvalues.round(2).to_dict(), "n", n)
for thr in [0, 0.005]:
    for c in [8, 15]:
        r = bt(z.tk_post, z.y_730, c, thr); print(f"  BT tk_post |>{thr*1e4:.0f}| -> 07:30->kapanış, {c} bps: n {r['n']} {r['mean_bps']:.1f} bps t {r['t']:.2f} Sh {r['sharpe']:.2f}")
# yıl/yarı kırılımı
for s, e in [("2023-12-01", "2024-12-31"), ("2025-01-01", "2025-12-31"), ("2026-01-01", "2026-12-31")]:
    zz = z[(z.index >= s) & (z.index <= e)]; m, n = nw(zz.y_730, zz[["tk_post"]]); r = bt(zz.tk_post, zz.y_730, 8, 0.005)
    print(f"  {s[:4]}: b {m.params['tk_post']:.3f} t {m.tvalues['tk_post']:.2f} n {n} | BT|>50| {r['n']} işlem {r['mean_bps']:.1f} bps Sh {r['sharpe']:.2f}")
H.to_parquet(OUT + "/05_hourly.parquet")
