"""Beş iddianın bağımsız yeniden hesabı. Fiyatlar: kendi saatlik serim (rep_common.price_at / price_asof).
VİOP hedefi: viop_long'dan kendi aktif kontrat kurulumum (r01'de panel ile birebir doğrulandı)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a2_seans_gunici_rep")
from rep_common import *
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)

vp = pd.read_parquet(f"{P}/panel_viop.parquet"); vp.index = pd.to_datetime(vp.index)
sp = pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index = pd.to_datetime(sp.index)
A = pd.read_parquet(f"{OUT}/viop_active_mine.parquet")
vdays = A.index
vret = A.ret
F = {h: fwd(vret, h) for h in (1, 3, 5)}

def px(days, H, off=0, asof=False):
    t = day_times(days, H, off)
    s = price_asof(t, 3) if asof else price_at(t)
    return pd.Series(s.values, index=days)

def fmt(d):
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items()}

res = {}
# ======================================================================= C1: S2 gece mevsimselliği
print("=" * 30, "C1 S2_late", "=" * 30)
sdays = sp.index  # Dukascopy 15:00 fiyatı olan iş günleri
p15s = px(sdays, 15); p00s = px(sdays, 0); p07s = px(sdays, 7); p12s = px(sdays, 12)
for asof in (False, True):
    p20s = px(sdays, 20, asof=asof)
    S1 = np.log(p20s.shift(1) / p15s.shift(1))
    S2 = np.log(p00s / p20s.shift(1))
    S3 = np.log(p07s / p00s)
    S4 = np.log(p12s / p07s); S5 = np.log(p15s / p12s)
    day = np.log(p15s / p15s.shift(1))
    tag = "asof" if asof else "exact"
    print(f"-- p20 {tag}: n S2 = {S2.notna().sum()}")
    per = {"2010-16": S2.index < "2017-01-01", "IS17-21": (S2.index >= "2017-03-01") & (S2.index <= IS_END), "OOS22-26": S2.index > IS_END, "full": np.ones(len(S2), bool),
           "IS_all<=2021": S2.index <= IS_END}
    for nm, m in per.items():
        mu, t, n = nw_t_mean(S2[m], 5)
        print(f"   S2 {nm}: {mu*1e4:.2f} bps t {t:.2f} n {n}")
    ym = S2.groupby(S2.index.year).mean()
    print("   yıl pozitif:", f"{(ym > 0).sum()}/{ym.notna().sum()}")
    # drift-düzeltilmiş fazla (analistin tanımı: yıllık varyans payı x yıllık gün ortalaması)
    seg = pd.concat([S1, S2, S3, S4, S5], axis=1, keys=["S1", "S2", "S3", "S4", "S5"]).dropna()
    dd = seg.sum(axis=1); yr = seg.index.year
    share = seg.S2.groupby(yr).transform("var") / dd.groupby(yr).transform("var")
    exc = seg.S2 - share * dd.groupby(yr).transform("mean")
    mu, t, n = nw_t_mean(exc, 5); print(f"   S2 fazla (varyans payı): {mu*1e4:.2f} bps t {t:.2f} n {n}")
    # basit alternatif drift: zaman payı (4 saat/24) x gün ortalaması, tam dönem sabit
    mu2, t2, _ = nw_t_mean(seg.S2 - dd.mean() * 4 / 24, 5); print(f"   S2 - (4/24)*ort gün getirisi: {mu2*1e4:.2f} bps t {t2:.2f}")
    if asof:
        res["c1_S2_full"] = nw_t_mean(S2, 5)
        S2_keep, S3_keep, seg_keep, dd_keep = S2, S3, seg, dd

# strateji: t-1 20:00 al -> t 07:00 sat (S2+S3), her gün 1 gidiş-dönüş
S2, S3, seg, dd = S2_keep, S3_keep, seg_keep, dd_keep
night = (seg.S2 + seg.S3)
yr = seg.index.year
share_n = night.groupby(yr).transform("var") / dd.groupby(yr).transform("var")
night_exc = night - share_n * dd.groupby(yr).transform("mean")
print("\n-- Gece-uzun kuralı (S2+S3), Sharpe:")
rows = []
for cost in (0, 5, 10):
    for nm, m in {"2010-16": night.index < "2017-01-01", "IS17-21": (night.index >= "2017-03-01") & (night.index <= IS_END), "OOS22-26": night.index > IS_END,
                  "VIOPeve2020-09-18+": night.index >= "2020-09-18"}.items():
        x = night[m] - cost / 1e4; xe = night_exc[m] - cost / 1e4
        rows.append(dict(cost=cost, per=nm, sharpe=round(sharpe(x), 2), sharpe_excess=round(sharpe(xe), 2), ann_pct=round(x.mean() * 252 * 100, 2), n=len(x)))
NT = pd.DataFrame(rows); print(NT.pivot_table(index="cost", columns="per", values=["sharpe", "sharpe_excess"]).to_string())
bh = dd
for nm, m in {"IS17-21": (bh.index >= "2017-03-01") & (bh.index <= IS_END), "OOS22-26": bh.index > IS_END, "VIOPeve2020-09-18+": bh.index >= "2020-09-18"}.items():
    print(f"   BH 15->15 spot {nm}: Sharpe {sharpe(bh[m]):.2f}")
# Gece kuralı: brüt getiri / maliyet oranı
print(f"   gece brüt ort OOS: {night[night.index > IS_END].mean()*1e4:.2f} bps/gün; maliyet 5 bps/gün; std {night[night.index > IS_END].std()*1e4:.1f} bps")
NT.to_csv(f"{OUT}/c1_night_rule.csv", index=False)

# GC=F saatlik (işlem fiyatı) 2024-06+ ile S2 kontrolü
g = pd.read_parquet(f"{P}/yahoo_h/GC_F.parquet")
gc = g["close"].copy(); gc.index = g.index + pd.Timedelta(hours=1)  # Yahoo saatlik: index = bar başlangıcı -> kapanış anı +1h
def gpx(days, H, off=0):
    t = day_times(days, H, off); return pd.Series(gc.reindex(t).values, index=days)
dd2 = sdays[sdays >= "2024-06-18"]
g00 = gpx(dd2, 0); g20 = gpx(dd2, 20).shift(1)
S2g = np.log(g00 / g20)
S2d = S2.reindex(dd2)
both = pd.concat([S2g.rename("gc"), S2d.rename("dk")], axis=1).dropna()
print(f"\n-- GC=F (Yahoo saatlik, 2024-06+): S2 GC {both.gc.mean()*1e4:.2f} bps (t {nw_t_mean(both.gc)[1]:.2f}), Dukascopy {both.dk.mean()*1e4:.2f} bps, corr {both.gc.corr(both.dk):.3f}, n {len(both)}")
# hafta içi saat dilimleri 20->22, 22->00
m4 = sdays[sdays.dayofweek < 4]
p20 = px(m4, 20); p22 = px(m4, 22); p00n = px(m4, 0, 1)
a = np.log(p22 / p20); b = np.log(p00n / p22)
print(f"   Pzt-Per t-1 akşamları: 20->22 {nw_t_mean(a)[0]*1e4:.2f} (t {nw_t_mean(a)[1]:.2f}), 22->00 {nw_t_mean(b)[0]*1e4:.2f} (t {nw_t_mean(b)[1]:.2f})")

# ======================================================================= ortak VİOP günlük öngörücüleri
p00 = px(vdays, 0); p12 = px(vdays, 12); p14 = px(vdays, 14); p15 = px(vdays, 15)

# ======================================================================= C2: baz
print("\n" + "=" * 30, "C2 baz", "=" * 30)
dte = (pd.to_datetime(A.expiry) - A.index).dt.days
r3m = vp.ust_nom3m.reindex(vdays)
eb = np.log(A.settle / p15) - r3m / 100 * dte / 365
p15prev = p15.shift(1)  # önceki VİOP günü 15:00 (spot yoksa NaN)
# panel xau_p15_prev: önceki mevcut 15:00 fiyatı (as-of). Aynısını kendi serimden kur:
p15_last = p15.ffill().shift(1)
s15 = np.log(p15 / p15_last)
relret = vret - s15
rel = {h: fwd(relret, h) for h in (1, 3, 5)}
isd = pd.concat([eb.rename("eb"), dte.rename("dte")], axis=1).dropna(); isd = isd[isd.index <= IS_END]
bb = np.polyfit(isd.dte, isd.eb, 1)
ebr = eb - (bb[0] * dte + bb[1])
print(f"eb ort {eb.mean()*1e4:.1f} bps, medyan {eb.median()*1e4:.1f}, AC1 {eb.autocorr(1):.3f}; IS eğim {bb[0]*1e4:.3f} bps/gün")
for h in (1, 3, 5):
    for nm, x in [("eb_t-1", eb.shift(1)), ("ebres_t-1", ebr.shift(1))]:
        st = split_ic(x, rel[h], h); print(f"  {nm} -> rel h{h}:", fmt(st))
        st2 = split_ic(x, F[h], h); print(f"  {nm} -> VİOP fwd h{h}:", fmt(st2))
res["c2"] = split_ic(ebr.shift(1), rel[5], 5)
# eb_t (kapanışta, mekanik) referans
print("  eb_t -> rel h5 (mekanik):", fmt(split_ic(eb, rel[5], 5)))
# relret ortalaması
print(f"  relret ort: tam {relret.mean()*1e4:.2f} IS {relret[relret.index<=IS_END].mean()*1e4:.2f} OOS {relret[relret.index>IS_END].mean()*1e4:.2f} bps/gün")
# Göreli değer kuralı
q = eb[eb.index <= IS_END].quantile([1 / 3, 2 / 3]).values
pos = pd.Series(np.where(eb.shift(1) > q[1], -1.0, np.where(eb.shift(1) < q[0], 1.0, 0.0)), index=vdays)
pos[eb.shift(1).isna()] = 0
qr = ebr[ebr.index <= IS_END].quantile([1 / 3, 2 / 3]).values
posr = pd.Series(np.where(ebr.shift(1) > qr[1], -1.0, np.where(ebr.shift(1) < qr[0], 1.0, 0.0)), index=vdays); posr[ebr.shift(1).isna()] = 0
rr = relret.dropna()
print("  RV kuralı (eb tercil), hedef relret:")
for h in (3, 5):
    for cost in (0, 10, 20):
        o = {p: bt(pos, rr, h, cost, p) for p in (None, "is", "oos")}
        print(f"   h{h} cost{cost}: full {o[None]['sharpe']:.2f} IS {o['is']['sharpe']:.2f} OOS {o['oos']['sharpe']:.2f} | OOS dm {o['oos']['sharpe_dm']:.2f} full dm {o[None]['sharpe_dm']:.2f} | turn/yıl {o[None]['turn']:.1f} | OOS ann% {o['oos']['ann']:.2f}")
    o = {p: bt(posr, rr, h, 10, p) for p in (None, "is", "oos")}
    print(f"   [ebres tercil] h{h} cost10: full {o[None]['sharpe']:.2f} IS {o['is']['sharpe']:.2f} OOS {o['oos']['sharpe']:.2f} | OOS dm {o['oos']['sharpe_dm']:.2f}")
# net pozisyon ortalaması (OOS) -> drift'e maruziyet
eff5 = pos.rolling(5, min_periods=1).sum() / 5
print(f"   ort. pozisyon (eff, h5): IS {eff5[eff5.index<=IS_END].mean():.3f} OOS {eff5[eff5.index>IS_END].mean():.3f}  (negatif = net VİOP kısa/spot uzun)")
# çıplak VİOP: pahalıyken kısa
for h in (3, 5):
    o = {p: bt(pos, vret, h, 5, p) for p in (None, "oos")}
    print(f"   çıplak VİOP (eb yüksek->kısa) h{h} 5bps: full {o[None]['sharpe']:.2f} OOS {o['oos']['sharpe']:.2f} dm {o['oos']['sharpe_dm']:.2f}")
res["c2_bt"] = {p: bt(pos, rr, 5, 10, p) for p in (None, "is", "oos")}

# ======================================================================= C3: kış fiks öncesi saat
print("\n" + "=" * 30, "C3 kış 14->15", "=" * 30)
def is_gmt(days):
    return pd.Series([pd.Timestamp(d.date()).tz_localize("Europe/London").utcoffset() == pd.Timedelta(0) for d in days], index=days)
win = is_gmt(vdays)
rpre = np.log(p15 / p14).where(win)
st = split_ic(rpre, F[1], 1); print("  kış rpre -> fwd1:", fmt(st)); res["c3"] = st
st_s = split_ic(np.log(p15 / p14).where(~win), F[1], 1); print("  yaz aynı saat -> fwd1:", fmt(st_s))
pos3 = np.sign(rpre).fillna(0)
for cost in (5, 10):
    o = {p: bt(pos3, vret, 1, cost, p) for p in (None, "is", "oos")}
    print(f"  işaret kuralı cost{cost}: full {o[None]['sharpe']:.2f} IS {o['is']['sharpe']:.2f} OOS {o['oos']['sharpe']:.2f} OOS dm {o['oos']['sharpe_dm']:.2f} turn/yıl {o[None]['turn']:.1f} BH OOS {o['oos']['bh']:.2f}")
    if cost == 5: res["c3_bt"] = o
for leg, pp in [("uzun", pos3.clip(lower=0)), ("kısa", pos3.clip(upper=0))]:
    o = bt(pp, vret, 1, 5, "oos"); print(f"   {leg} bacak OOS: {o['sharpe']:.2f} dm {o['sharpe_dm']:.2f}")
# işlem sayısı (pozisyon açılan gün sayısı / yıl)
print(f"  sinyal günü/yıl: {(pos3 != 0).sum() / (len(vdays) / 252):.1f}")
# erken dönem (spot 15->15 hedef)
sret = np.log(p15s / p15s.ffill().shift(1))
sf1 = fwd(sret, 1)
win_s = is_gmt(sdays)
p14s = px(sdays, 14)
rpre_s = np.log(p15s / p14s).where(win_s)
m = sdays < "2017-01-01"
c, t, n = ic_nw(rpre_s[m], sf1[m], 5)
d = pd.concat([rpre_s[m].rename("x"), sf1[m].rename("y")], axis=1).dropna(); yy = d.groupby(d.index.year).apply(lambda g: g.x.rank().corr(g.y.rank()))
print(f"  ERKEN 2010-16 kış: IC {c:.4f} t {t:.2f} n {n} yıllar {(np.sign(yy) == np.sign(c)).sum()}/{len(yy)}")
# sfwd1 panel ile aynı mı
print("  panel sfwd1 ile eşleşme:", np.nanmean(np.isclose(sf1, sp.sfwd1)))
# placebo: shift
for sh in (-1, 0, 1, 2):
    print(f"   placebo shift {sh}: IC {ic_nw(rpre.shift(sh), F[1], 5)[0]:.4f}")

# ======================================================================= C4: C_pre h3
print("\n" + "=" * 30, "C4 C_pre", "=" * 30)
cpre = np.log(p15 / p00)
st = split_ic(cpre, F[3], 3); print("  C_pre -> fwd3:", fmt(st)); res["c4"] = st
pos4 = np.sign(cpre).fillna(0)
o = {p: bt(pos4, vret, 3, 5, p) for p in (None, "is", "oos")}
print(f"  işaret h3 5bps: full {o[None]['sharpe']:.2f} (dm {o[None]['sharpe_dm']:.2f}) IS {o['is']['sharpe']:.2f} OOS {o['oos']['sharpe']:.2f} OOS dm {o['oos']['sharpe_dm']:.2f} turn/yıl {o[None]['turn']:.1f} BH OOS {o['oos']['bh']:.2f}")
res["c4_bt"] = o
for leg, pp in [("uzun", pos4.clip(lower=0)), ("kısa", pos4.clip(upper=0))]:
    oo = bt(pp, vret, 3, 5, "oos"); of = bt(pp, vret, 3, 5, None); print(f"   {leg} bacak: full {of['sharpe']:.2f} dm {of['sharpe_dm']:.2f} | OOS {oo['sharpe']:.2f} dm {oo['sharpe_dm']:.2f}")
cpre_s = np.log(p15s / p00s); sf3 = fwd(sret, 3)
c, t, n = ic_nw(cpre_s[m], sf3[m], 5); print(f"  ERKEN 2010-16: IC {c:.4f} t {t:.2f} n {n}")
for hh in (1, 5):
    print(f"  C_pre -> fwd{hh}:", fmt(split_ic(cpre, F[hh], hh)))

# ======================================================================= C5: büyük NY sabahı
print("\n" + "=" * 30, "C5 |S5|>q90", "=" * 30)
s5 = np.log(p15 / p12)
thr = s5[s5.index <= IS_END].abs().quantile(0.9)
big = s5.where(s5.abs() > thr)
print(f"  eşik {thr*1e4:.1f} bps, sinyal günleri {big.notna().sum()} ({big.notna().sum()/(len(vdays)/252):.1f}/yıl)")
for hh in (1, 3, 5):
    st = split_ic(big, F[hh], hh); print(f"  big -> fwd{hh}:", fmt(st))
    if hh == 5: res["c5"] = st
pos5 = np.sign(big).fillna(0)
o = {p: bt(pos5, vret, 5, 5, p) for p in (None, "is", "oos")}
print(f"  işaret h5 5bps: full {o[None]['sharpe']:.2f} IS {o['is']['sharpe']:.2f} OOS {o['oos']['sharpe']:.2f} OOS dm {o['oos']['sharpe_dm']:.2f} turn/yıl {o[None]['turn']:.1f}")
res["c5_bt"] = o
for leg, pp in [("uzun", pos5.clip(lower=0)), ("kısa", pos5.clip(upper=0))]:
    oo = bt(pp, vret, 5, 5, "oos"); print(f"   {leg} bacak OOS: {oo['sharpe']:.2f} dm {oo['sharpe_dm']:.2f}")
s5s = np.log(p15s / p12s); sf5 = fwd(sret, 5)
thr_e = s5s[m].abs().quantile(0.9)
c, t, n = ic_nw(s5s.where(s5s.abs() > thr_e)[m], sf5[m], 5); print(f"  ERKEN 2010-16 (kendi q90): IC {c:.4f} t {t:.2f} n {n}")
c, t, n = ic_nw(s5s.where(s5s.abs() > thr)[m], sf5[m], 5); print(f"  ERKEN 2010-16 (VİOP IS eşiği): IC {c:.4f} t {t:.2f} n {n}")
# NW lag duyarlılığı (h=5 seyrek örneklem: ardışık sinyaller nadir)
for L in (5, 10, 20):
    d = pd.concat([big.rename("x"), F[5].rename("y")], axis=1).dropna()
    rx = d.x.rank(); ry = d.y.rank()
    _, t = nw_t_ols(((ry - ry.mean()) / ry.std()).values, ((rx - rx.mean()) / rx.std()).values, L)
    print(f"   NW lag {L}: t {t:.2f}")

pd.to_pickle(dict(eb=eb, ebr=ebr, relret=relret, rpre=rpre, cpre=cpre, big=big, S2=S2), f"{OUT}/series_mine.pkl")
