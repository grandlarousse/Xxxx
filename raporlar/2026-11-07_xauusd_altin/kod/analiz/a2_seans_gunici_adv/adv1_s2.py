"""İddia 1 (S2 gece mevsimselliği) saldırısı.
1) Panel xau_p00 / xau_p20_prev ile ham saatlik bardan bağımsız yeniden kurulum (hizalama).
2) Alt dönemler, haftanın günü, tatil sonrası (t-1 > 1 iş günü), uç dönemler, winsor.
3) Komşu pencereler (19->23, 20->01, 21->01, 20->23...) — tek tepe mi?
4) GC=F (COMEX işlem fiyatı) ile aynı pencere (2024-06+), BID yanılsaması.
5) Strateji: 20:00 al -> 06:30/07:00 sat; 5/10 bps, drift düzeltmesi, buy&hold; 2020-09-18+.
6) VİOP yerel: 2026 akşam bülteni kapanışı -> ertesi normal seans açılış (os_price) vs spot aynı pencere."""
from adv_common import *
import glob
s = load_spot(); v = load_viop()
px = A2.price_series()   # index = fiyat anı (bar başlangıcı + 1s)
days = s.index
D0 = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") for d in days])
prevD = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") for d in days.to_series().shift(1).fillna(days[0])])
p00 = snap(px, D0); p20p = snap(px, prevD + pd.Timedelta(hours=20)); p07 = snap(px, D0 + pd.Timedelta(hours=7))
print("Hizalama: panel xau_p00 vs bağımsız p00 |log fark| > 1e-6 oranı:", float((np.abs(np.log(s.xau_p00.values / p00)) > 1e-6)[np.isfinite(p00) & s.xau_p00.notna().values].mean()))
print("Hizalama: panel xau_p20_prev vs bağımsız:", float((np.abs(np.log(s.xau_p20_prev.values / p20p)) > 1e-6)[np.isfinite(p20p) & s.xau_p20_prev.notna().values].mean()))
S2 = pd.Series(np.log(p00 / p20p), index=days).iloc[1:]
print("\nS2 bağımsız: ort %.2f bps t %.2f n %d" % (mean_t(S2)[0] * 1e4, mean_t(S2)[1], mean_t(S2)[2]))
# boşluk: t-1 ile t arası takvim günü
gapd = (days.to_series().diff().dt.days).reindex(S2.index)
dow = S2.index.dayofweek
rows = []
def add(nm, x):
    m, t, n = mean_t(x); rows.append(dict(kosul=nm, bps=round(m * 1e4, 2), t=round(t, 2), n=n, medyan_bps=round(x.median() * 1e4, 2), poz=round((x > 0).mean(), 3)))
add("hepsi", S2)
for k, (a, b) in SUBP.items(): add(k, S2[(S2.index >= a) & (S2.index <= b)])
for i, nm in enumerate(["Pzt(t-1=Cuma, hafta sonu dahil)", "Sal", "Çar", "Per", "Cum"]): add(nm, S2[dow == i])
add("ardışık takvim günü (gap=1)", S2[gapd == 1])
add("tatil sonrası (Pzt dışı gap>1)", S2[(gapd > 1) & (dow != 0)])
ext = ((S2.index >= "2020-03-01") & (S2.index <= "2020-03-31")) | ((S2.index >= "2026-01-01") & (S2.index <= "2026-02-28"))
add("uç dönem hariç", S2[~ext])
add("winsor %1-99", S2.clip(S2.quantile(.01), S2.quantile(.99)))
add("|S2|<50bps (büyük gece hareketleri hariç)", S2[S2.abs() < 0.005])
# en büyük 20 gün katkısı
top = S2.sort_values(ascending=False)
add("en büyük 20 pozitif gün hariç", S2.drop(top.index[:20]))
add("en büyük 1% (|S2|) hariç", S2[S2.abs() < S2.abs().quantile(.99)])
R = pd.DataFrame(rows); print(R.to_string()); R.to_csv(f"{OUT}/adv1_s2_conditions.csv", index=False)
# yıllık
yy = S2.groupby(S2.index.year).agg(["mean", "count"]); yy["mean"] *= 1e4
print("\nYıl yıl S2 bps:\n", yy.round(2).T.to_string())
# drift: o yılın günlük ortalama 15->15 getirisinin "saat payı" (4/24) ve varyans payı
day = np.log(s.xau_p15 / s.xau_p15_prev).reindex(S2.index)
dd = pd.concat([S2.rename("s2"), day.rename("d")], axis=1).dropna()
yr = dd.index.year
exc_time = dd.s2 - dd.d.groupby(yr).transform("mean") * 4 / 24
print("\nZaman payı (4/24) drift düzeltilmiş S2: %.2f bps t %.2f" % (mean_t(exc_time)[0] * 1e4, mean_t(exc_time)[1]))
exc_all = dd.s2 - dd.d.groupby(yr).transform("mean")  # en sert: bütün günlük drift'i S2'ye yükle
print("En sert (bütün günlük drift S2'den çıkar): %.2f bps t %.2f" % (mean_t(exc_all)[0] * 1e4, mean_t(exc_all)[1]))
for k, (a, b) in SUBP.items():
    m = (exc_all.index >= a) & (exc_all.index <= b); print(f"   {k}: {mean_t(exc_all[m])[0]*1e4:.2f} bps t {mean_t(exc_all[m])[1]:.2f}")

# 3) komşu pencereler (Pzt-Per t-1 akşamları: hafta sonu karışmasın) — bütün yıllar
print("\nKomşu pencereler (t-1 Pzt-Per; saat a [t-1] -> b [t veya t-1]); bps, t:")
dmt = days[days.dayofweek < 4]
base = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") for d in dmt])
grid = []
for a in (18, 19, 20, 21, 22):
    for b in (22, 23, 24, 25, 26, 27):
        if b <= a: continue
        pa = snap(px, base + pd.Timedelta(hours=a)); pb = snap(px, base + pd.Timedelta(hours=b))
        r = pd.Series(np.log(pb / pa), index=dmt).dropna()
        m, t, n = mean_t(r)
        m2 = mean_t(r[r.index >= "2017-01-01"])
        grid.append(dict(a=a, b=b % 24 if b < 24 else f"{b-24}(t)", bps=round(m * 1e4, 2), t=round(t, 2), bps_2017p=round(m2[0] * 1e4, 2), t_2017p=round(m2[1], 2), n=n))
G = pd.DataFrame(grid); print(G.to_string()); G.to_csv(f"{OUT}/adv1_neighbor_windows.csv", index=False)

# 4) GC=F saatlik (bar başlangıcı = ts_utc; fiyat anı = +1s), 2024-06+
g = pd.read_parquet(f"{S}/panel/yahoo_h/GC_F.parquet"); gp = g["close"].copy(); gp.index = g.index + pd.Timedelta(hours=1)
dd2 = days[days >= "2024-06-20"]
b2 = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") for d in dd2]); pv2 = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") for d in dd2.to_series().shift(1).fillna(dd2[0])])
gc = pd.Series(np.log(snap(gp, b2) / snap(gp, pv2 + pd.Timedelta(hours=20))), index=dd2).iloc[1:]
dk = S2.reindex(gc.index)
both = pd.concat([gc.rename("gc"), dk.rename("dk")], axis=1).dropna()
print(f"\nGC=F vs Dukascopy S2 (2024-06+, n={len(both)}): GC {mean_t(both.gc)[0]*1e4:.2f} bps (t {mean_t(both.gc)[1]:.2f}), DK {mean_t(both.dk)[0]*1e4:.2f} bps (t {mean_t(both.dk)[1]:.2f}), corr {both.gc.corr(both.dk):.3f}")
# GC'de hafta içi her pencere (20->22, 22->00)
for a, b in [(20, 22), (22, 24), (20, 24)]:
    bb = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") for d in dd2[dd2.dayofweek < 4]])
    rg = pd.Series(np.log(snap(gp, bb + pd.Timedelta(hours=b)) / snap(gp, bb + pd.Timedelta(hours=a))), index=dd2[dd2.dayofweek < 4]).dropna()
    rd = pd.Series(np.log(snap(px, bb + pd.Timedelta(hours=b)) / snap(px, bb + pd.Timedelta(hours=a))), index=dd2[dd2.dayofweek < 4]).reindex(rg.index)
    print(f"   {a}->{b%24}: GC {rg.mean()*1e4:.2f} bps (t {mean_t(rg)[1]:.2f}) | DK {rd.mean()*1e4:.2f} bps (t {mean_t(rd)[1]:.2f}) n {len(rg)}")
