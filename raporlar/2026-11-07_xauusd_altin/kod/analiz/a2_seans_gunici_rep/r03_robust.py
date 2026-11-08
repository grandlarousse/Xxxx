"""Ek sağlamlık: C1 çıkış saati aralığı, VİOP-yerel gece getirisi, akşam seansı fiyat kalibrasyonu;
C3 saat-ailesi (kışın her saatin getirisi -> fwd1), alt dönemler; C4/C5 alt dönem ve parametre duyarlılığı."""
import sys, glob, os; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a2_seans_gunici_rep")
from rep_common import *
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
vp = pd.read_parquet(f"{P}/panel_viop.parquet"); vp.index = pd.to_datetime(vp.index)
sp = pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index = pd.to_datetime(sp.index)
A = pd.read_parquet(f"{OUT}/viop_active_mine.parquet"); vdays = A.index; vret = A.ret
F = {h: fwd(vret, h) for h in (1, 3, 5, 10)}
def px(days, H, off=0, asof=False):
    t = day_times(days, H, off); s = price_asof(t, 3) if asof else price_at(t); return pd.Series(s.values, index=days)
sdays = sp.index

print("=" * 25, "C1 ek", "=" * 25)
p20 = px(sdays, 20, asof=True).shift(1)
for H in (6, 7):
    pe = px(sdays, H)
    night = np.log(pe / p20)
    for nm, m in {"IS17-21": (night.index >= "2017-03-01") & (night.index <= IS_END), "OOS22-26": night.index > IS_END, "2020-09-18+": night.index >= "2020-09-18"}.items():
        x = night[m].dropna()
        print(f"  20:00 al -> {H:02d}:00 sat {nm}: brüt {x.mean()*1e4:.2f} bps/gün, Sharpe brüt {sharpe(x):.2f}, 5bps {sharpe(x-5e-4):.2f}, 10bps {sharpe(x-1e-3):.2f}")
# yıl yıl 5 bps net (07:00 çıkış)
night = np.log(px(sdays, 7) / p20)
yy = ((night - 5e-4).groupby(night.index.year).mean() * 1e4).round(2)
print("  yıl yıl net (5bps) bps/gün:", yy.to_dict())
print("  net>0 yıl:", (yy > 0).sum(), "/", len(yy))
# VİOP-yerel: bülten AÇILIŞ (akşam seansı ilk işlemi ~16:00 UTC t-1) -> AÇILIŞ SEANSI (~06:30 UTC t)
nat = np.log(A.os_price / A.open)
p16prev = px(vdays, 16).shift(1); p07 = px(vdays, 7); p06 = px(vdays, 6)
spot_eq = np.log(p07 / p16prev)
m = (vdays >= "2020-09-21")
d = pd.concat([nat.rename("viop"), spot_eq.rename("spot")], axis=1)[m].replace([np.inf, -np.inf], np.nan).dropna()
d = d[(d.viop.abs() < 0.1)]
mu, t, n = nw_t_mean(d.viop); mu2, t2, _ = nw_t_mean(d.spot)
print(f"  VİOP-yerel açılış(akşam ilk işlem)->açılış seansı: {mu*1e4:.2f} bps (t {t:.2f}, n {n}); spot eşdeğeri 16->07: {mu2*1e4:.2f} (t {t2:.2f}); corr {d.viop.corr(d.spot):.3f}")
mu3, t3, n3 = nw_t_mean(np.log(A.os_price / A.prev_settle)[m].replace([np.inf, -np.inf], np.nan).dropna().loc[lambda x: x.abs() < 0.1])
print(f"  VİOP-yerel uzlaşma(t-1)->açılış seansı(t): {mu3*1e4:.2f} bps (t {t3:.2f}, n {n3})")
# akşam seansı kalibrasyonu (2026 akşam bültenleri)
ev = []
for f in sorted(glob.glob(f"{S}/dl4/as_*.csv")):
    t_ = pd.read_csv(f, sep=";", skiprows=[1])
    t_ = t_[t_["SOZLESME KODU"].astype(str).str.startswith("F_XAUUSD")]
    t_ = t_[pd.to_numeric(t_["ISLEM MIKTARI"], errors="coerce") > 0]
    if t_.empty: continue
    r = t_.sort_values("ISLEM MIKTARI", ascending=False).iloc[0]
    ev.append(dict(date=pd.Timestamp(os.path.basename(f)[3:11]), code=r["SOZLESME KODU"], ev_open=float(r["ACILIS FIYATI"]), ev_close=float(r["KAPANIS FIYATI"]), qty=float(r["ISLEM MIKTARI"])))
E = pd.DataFrame(ev).set_index("date")
E = E.join(A[["code", "settle"]].rename(columns={"code": "act"}), how="inner"); E = E[E.code == E.act]
E["p15"] = px(E.index, 15); E["p20"] = px(E.index, 20); E["p16"] = px(E.index, 16)
bas = np.log(E.settle / E.p15)
d20 = (np.log(E.ev_close / E.p20) - bas) * 1e4
print(f"  akşam kapanışı - (spot20 + baz_t): medyan {d20.median():.1f} bps, MAD {(d20-d20.median()).abs().median():.1f}, n {len(E)}; tarih günleri: {E.index.dayofweek.value_counts().to_dict()}")

print("\n" + "=" * 25, "C3 ek", "=" * 25)
win = pd.Series([pd.Timestamp(x.date()).tz_localize("Europe/London").utcoffset() == pd.Timedelta(0) for x in vdays], index=vdays)
usw = pd.Series([pd.Timestamp(x.date()).tz_localize("America/New_York").utcoffset() == pd.Timedelta(hours=-5) for x in vdays], index=vdays)
P = {H: px(vdays, H) for H in range(0, 16)}
rows = []
for H in range(1, 16):
    r = np.log(P[H] / P[H - 1])
    for nm, msk in [("kis", win), ("yaz", ~win)]:
        st = split_ic(r.where(msk), F[1], 1)
        rows.append(dict(hour=f"{H-1:02d}->{H:02d}", season=nm, ic=round(st["ic"], 4), t=round(st["t"], 2), t_is=round(st["t_is"], 2), t_oos=round(st["t_oos"], 2), yrs=st["yrs"]))
HR = pd.DataFrame(rows); print(HR.pivot_table(index="hour", columns="season", values=["t", "t_is", "t_oos"]).to_string())
HR.to_csv(f"{OUT}/c3_hour_family.csv", index=False)
k = HR[HR.season == "kis"]; print(f"  kış: 15 saat içinde |t|>=2 olan: {(k.t.abs() >= 2).sum()}, max |t| saat: {k.loc[k.t.abs().idxmax(), 'hour']}")
rpre = np.log(P[15] / P[14])
for nm, msk in [("Londra GMT", win), ("ABD EST", usw), ("Londra GMT & ABD EST", win & usw), ("Londra GMT, ABD EDT (uyumsuz haftalar)", win & ~usw)]:
    c, t, n = ic_nw(rpre.where(msk), F[1], 5); print(f"  {nm}: IC {c:.4f} t {t:.2f} n {n}")
for nm, a, b in [("2017-19", "2017", "2019"), ("2020-21", "2020", "2021"), ("2022-24", "2022", "2024"), ("2025-26", "2025", "2026")]:
    m = (vdays >= a) & (vdays <= f"{b}-12-31")
    c, t, n = ic_nw(rpre.where(win)[m], F[1][m], 5); print(f"  {nm}: IC {c:.4f} t {t:.2f} n {n}")
m = vdays < "2025-01-01"; c, t, n = ic_nw(rpre.where(win)[m], F[1][m], 5); print(f"  2025-26 hariç: IC {c:.4f} t {t:.2f}")
pos = np.sign(rpre.where(win)).fillna(0)
oo = bt(pos[vdays < "2025-01-01"], vret[(vdays > IS_END) & (vdays < "2025-01-01")], 1, 5)
print(f"  işaret kuralı OOS 2022-24 (5bps): Sharpe {oo['sharpe']:.2f} dm {oo['sharpe_dm']:.2f}")

print("\n" + "=" * 25, "C4 ek", "=" * 25)
cpre = np.log(P[15] / P[0])
for nm, a, b in [("2017-19", "2017", "2019"), ("2020-21", "2020", "2021"), ("2022-24", "2022", "2024"), ("2025-26", "2025", "2026")]:
    m = (vdays >= a) & (vdays <= f"{b}-12-31")
    c, t, n = ic_nw(cpre[m], F[3][m], 5); print(f"  {nm}: IC {c:.4f} t {t:.2f} n {n}")
m = vdays < "2025-01-01"; c, t, n = ic_nw(cpre[m], F[3][m], 5); print(f"  2025-26 hariç: IC {c:.4f} t {t:.2f}")
pos4 = np.sign(cpre).fillna(0)
oo = bt(pos4, vret[(vdays > IS_END) & (vdays < "2025-01-01")], 3, 5); print(f"  işaret h3 OOS 2022-24: Sharpe {oo['sharpe']:.2f} dm {oo['sharpe_dm']:.2f} BH {oo['bh']:.2f}")
oo = bt(pos4, vret[vdays >= "2025-01-01"], 3, 5); print(f"  işaret h3 2025-26: Sharpe {oo['sharpe']:.2f} dm {oo['sharpe_dm']:.2f} BH {oo['bh']:.2f}")

print("\n" + "=" * 25, "C5 ek", "=" * 25)
s5 = np.log(P[15] / P[12])
for q in (0.8, 0.85, 0.9, 0.95):
    thr = s5[s5.index <= IS_END].abs().quantile(q); big = s5.where(s5.abs() > thr)
    out = []
    for h in (3, 5, 10):
        st = split_ic(big, F[h], h); out.append(f"h{h}: t {st['t']:.2f} (IS {st['t_is']:.2f}, OOS {st['t_oos']:.2f})")
    pos = np.sign(big).fillna(0); o = bt(pos, vret, 5, 5, "oos"); oi = bt(pos, vret, 5, 5, "is")
    print(f"  q{int(q*100)} (n {big.notna().sum()}): " + " | ".join(out) + f" | h5 Sharpe IS {oi['sharpe']:.2f} OOS {o['sharpe']:.2f}")
thr = s5[s5.index <= IS_END].abs().quantile(0.9); big = s5.where(s5.abs() > thr)
for nm, a, b in [("2017-21", "2017", "2021"), ("2022-24", "2022", "2024"), ("2025-26", "2025", "2026")]:
    m = (vdays >= a) & (vdays <= f"{b}-12-31")
    c, t, n = ic_nw(big[m], F[5][m], 5); print(f"  {nm}: IC {c:.4f} t {t:.2f} n {n}")
pos5 = np.sign(big).fillna(0)
oo = bt(pos5, vret[(vdays > IS_END) & (vdays < "2025-01-01")], 5, 5); print(f"  h5 OOS 2022-24: Sharpe {oo['sharpe']:.2f} dm {oo['sharpe_dm']:.2f}")
oo = bt(pos5, vret[vdays >= "2025-01-01"], 5, 5); print(f"  h5 2025-26: Sharpe {oo['sharpe']:.2f} dm {oo['sharpe_dm']:.2f}")
# işaret yönü dağılımı OOS: büyük hareketlerin kaçı yukarı
bo = big[big.index > IS_END].dropna(); print(f"  OOS sinyal: {len(bo)}, yukarı oranı {(bo>0).mean():.2f}")

print("\n" + "=" * 25, "C2 ek", "=" * 25)
ser = pd.read_pickle(f"{OUT}/series_mine.pkl"); eb = ser["eb"]; relret = ser["relret"]
q = eb[eb.index <= IS_END].quantile([1 / 3, 2 / 3]).values
pos = pd.Series(np.where(eb.shift(1) > q[1], -1.0, np.where(eb.shift(1) < q[0], 1.0, 0.0)), index=vdays); pos[eb.shift(1).isna()] = 0
# spot bacağını fonlama maliyeti: uzun spot -> r/365 takvim günü; kısa spot -> +r (kabaca). relret'e -pos*(-r) ... VİOP kısa+spot uzun = -relret yönünde
r3m = vp.ust_nom3m.reindex(vdays) / 100
cal = pd.Series(vdays, index=vdays).diff().dt.days.fillna(1)
fin = r3m * cal / 365   # günlük fonlama (log yaklaşık)
# pos=+1: VİOP uzun + spot kısa -> spot kısadan faiz kazanılır (+fin); pos=-1: VİOP kısa + spot uzun -> fonlama öde (-fin)
# relret'e eklenecek düzeltme: hedef relret_adj = relret + fin (pos ile çarpılınca: +1 -> +fin, -1 -> -fin)
rr = (relret + fin).dropna()
for h in (5,):
    for cost in (0, 10):
        o = {p: bt(pos, rr, h, cost, p) for p in (None, "is", "oos")}
        print(f"  fonlama dahil RV h{h} cost{cost}: full {o[None]['sharpe']:.2f} IS {o['is']['sharpe']:.2f} OOS {o['oos']['sharpe']:.2f} (dm {o['oos']['sharpe_dm']:.2f})")
print(f"  fonlama dahil relret ort: OOS {rr[rr.index>IS_END].mean()*1e4:.2f} bps/gün (fonlamasız {relret[relret.index>IS_END].mean()*1e4:.2f})")
