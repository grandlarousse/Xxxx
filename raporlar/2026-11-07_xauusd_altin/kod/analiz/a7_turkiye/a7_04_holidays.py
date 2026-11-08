"""Aile (c): Yurt içi tatiller (VİOP kapalı, dünya açık) ve yarım günler."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye")
from a7_common import *
from scipy import stats as st_
FAM = "c_holiday"
reset_family(FAM)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
p, f = build()
r = p.v_ret
spot_gap = np.log(p.xau_p15 / p.xau_p15_prev)   # önceki VİOP günü 15:00 -> bugün 15:00 spot (tatil boyunca dünya hareketi dahil)
gap = f.gap
post = gap > 0
pre = post.shift(-1, fill_value=False)          # tatilden önceki son VİOP günü (t). Tatil riski = fwd1(t) = v_ret(post)
hd = f.half_day
print("Tatil sonrası ilk gün sayısı:", int(post.sum()), " yarım gün:", int(hd.sum()))

# C1: tatil sonrası ilk gün getirisi spot hareketini ne kadar yansıtıyor?
rows = []
for nm, m in [("normal (gap=0, yarım gün değil)", (gap == 0) & ~hd & ~hd.shift(1, fill_value=False)), ("tatil sonrası (gap>=1)", post), ("gap=1", gap == 1), ("gap>=2", gap >= 2)]:
    d = pd.DataFrame({"v": r[m], "s": spot_gap[m]}).dropna()
    b = np.polyfit(d.s, d.v, 1)
    rows.append(dict(grup=nm, n=len(d), beta=b[0], R2=d.v.corr(d.s) ** 2, sd_v_bps=d.v.std() * 1e4, sd_fark_bps=(d.v - d.s).std() * 1e4,
                     ort_v_bps=d.v.mean() * 1e4, ort_s_bps=d.s.mean() * 1e4))
C1 = pd.DataFrame(rows); print("\nC1. VİOP getirisi vs spot (15:00->15:00) — tatil sonrası:"); print(C1.round(3).to_string(index=False))
C1.to_csv(f"{OUT}/c1_post_holiday_tracking.csv", index=False)

# C2: tatil boyunca pozisyon riski: varyans oranı ve ortalama (drift düzeltmeli)
mu = r[(gap == 0)].mean(); sd0 = r[(gap == 0)].std()
print("\nC2. Tatili kapsayan getiri (pozisyon tatil öncesi uzlaşmada açılır, tatil sonrası uzlaşmada kapanır)")
for k in sorted(gap[post].unique()):
    v = r[gap == k]
    print(f"  gap={k}: n={len(v)}, sd={v.std()*1e4:.0f} bps (normal {sd0*1e4:.0f}, beklenen √(k+1)×={sd0*np.sqrt(k+1)*1e4:.0f}), ort={v.mean()*1e4:+.1f} bps, |getiri|>2% oranı {(v.abs()>0.02).mean():.2f} (normal {(r[gap==0].abs()>0.02).mean():.2f})")
v = r[post]; ex = v - mu * (gap[post] + 1)
tt = ex.mean() / (ex.std() / np.sqrt(len(ex)))
print(f"  tüm tatiller: ort {v.mean()*1e4:+.1f} bps, drift-düzeltilmiş fazla {ex.mean()*1e4:+.1f} bps, t={tt:+.2f}, n={len(v)}, isabet(>0) {(v>0).mean():.2f}")
yr = ex.groupby(ex.index.year).mean()
print("  yıl yıl fazla getiri (bps):", (yr * 1e4).round(0).to_dict())
L.register(AG, FAM, "holiday_span_long", "tatil öncesi uzlaşmada uzun, tatil sonrası çık (takvim)", 1,
           dict(ic=np.nan, t=tt, n=len(v), t_is=(lambda e: e.mean() / (e.std() / np.sqrt(len(e))))(ex[ex.index <= L.IS_END]),
                t_oos=(lambda e: e.mean() / (e.std() / np.sqrt(len(e))))(ex[ex.index > L.IS_END]), yrs_same_sign=int((np.sign(yr) == np.sign(ex.mean())).sum()), yrs=len(yr)),
           "drift düzeltilmiş; bilgi = resmi tatil takvimi (önceden bilinir)")
# Fabozzi tipi tatil ÖNCESİ gün getirisi: tatil öncesi son günün kendi getirisi (t-1 uzlaşma -> pre günü uzlaşma)
vpre = r[pre]; expre = vpre - mu
tpre = expre.mean() / (expre.std() / np.sqrt(len(expre)))
print(f"  tatil öncesi son gün getirisi: ort {vpre.mean()*1e4:+.1f} bps, fazla {expre.mean()*1e4:+.1f}, t={tpre:+.2f}, n={len(vpre)}")
L.register(AG, FAM, "pre_holiday_day", "tatil öncesi günün getirisi (t-1 uzlaşmada gir)", 1, dict(ic=np.nan, t=tpre, n=len(vpre),
           t_is=(lambda e: e.mean() / (e.std() / np.sqrt(len(e))))(expre[expre.index <= L.IS_END]), t_oos=(lambda e: e.mean() / (e.std() / np.sqrt(len(e))))(expre[expre.index > L.IS_END])), "takvim")

# C3: tatilde birikmiş dünya hareketi sonrası (tatil sonrası günden itibaren) devam/dönüş
print("\nC3. Tatil boyunca spot hareketi (tatil sonrası ilk gün 15:00'te bilinir) -> sonraki fwd_h (tatil sonrası uzlaşmada gir)")
hol_move = spot_gap.where(post)
for h in (1, 3, 5):
    y = f[f"fwd{h}"]
    d = pd.DataFrame({"x": hol_move, "y": y}).dropna()
    b = nw_ols(d.y, d.x, lags=h)
    c = st_.spearmanr(d.x, d.y)
    print(f"  h={h}: n={len(d)}, spearman {c[0]:+.3f} (p {c[1]:.2f}), OLS b={b['b']:+.3f} t={b['t']:+.2f}")
    L.register(AG, FAM, "holiday_move_cont", "tatil boyunca spot hareketi -> fwd_h", h, dict(ic=c[0], t=b["t"], n=len(d)), "olay örneklemi küçük")
    # tatil sonrası günler ortalaması fwd_h (drift düzeltilmiş)
    e = y[post] - y.mean()
    print(f"        tatil sonrası günden fwd{h} fazla ort {e.mean()*1e4:+.1f} bps (t={e.mean()/(e.std()/np.sqrt(len(e)))*np.sqrt(1/max(1,1)):+.2f})")
    L.register(AG, FAM, "post_holiday_fwd", "tatil sonrası ilk günden fwd_h (drift düzeltilmiş)", h, dict(ic=np.nan, t=e.mean() / (e.std() / np.sqrt(len(e))), n=len(e)), "")

# C4: tatil sonrası ilk gün VİOP bazı (uzlaşma vs spot) anormal mi?
xb = f.xbasis_dev_K
print("\nC4. VİOP XAUUSD baz sapması (bps): normal vs tatil sonrası ilk gün vs yarım gün")
for nm, m in [("normal", gap == 0), ("tatil sonrası", post), ("yarım gün", hd)]:
    s = xb[m].dropna() * 1e4
    print(f"  {nm:14s} n={len(s)} ort {s.mean():+.1f} medyan {s.median():+.1f} |ort| {s.abs().mean():.1f} sd {s.std():.1f}")

# C5: yarım günler — zaman damgası kayması ve ileriye bakma uyarısı
print("\nC5. Yarım günler (uzlaşma ~09:40 UTC). 15:00 UTC bilgisiyle kurulan bir sinyal bu günlerde İLERİYE BAKAR.")
s15 = np.log(p.xau_p15).diff()
d = pd.DataFrame({"v": r, "s15": s15, "xau_intraday_after_settle": np.log(p.xau_p15 / p.xau_p12)}).loc[hd]
print(f"  n={hd.sum()}, corr(v_ret, spot15 getiri) yarım günde {d.v.corr(d.s15):.2f} (normal {r[~hd].corr(s15[~hd]):.2f})")
nxt = hd.shift(1, fill_value=False)
print(f"  yarım günden sonraki VİOP günü (tatil sonrası) getirisi sd {r[nxt].std()*1e4:.0f} bps, n={nxt.sum()}")
# Örnek: 15:00 spot momentumu (xau_p15/xau_p07) yarım günde fwd1 ile korelasyonu — sızıntı göstergesi
mom = np.log(p.xau_p15 / p.xau_p07)
for nm, m in [("yarım gün", hd), ("normal", ~hd)]:
    dd = pd.concat([mom[m], f.fwd1[m]], axis=1).dropna()
    print(f"  örnek sızıntı: corr(xau 07->15 UTC, fwd1) {nm}: {dd.corr().iloc[0,1]:+.3f} n={len(dd)}")
pd.DataFrame({"half_day": hd[hd].index.strftime("%Y-%m-%d")}).to_csv(f"{OUT}/c5_half_days.csv", index=False)
pd.DataFrame({"post_holiday": post[post].index.strftime("%Y-%m-%d"), "gap": gap[post].values}).to_csv(f"{OUT}/c_post_holiday_days.csv", index=False)
