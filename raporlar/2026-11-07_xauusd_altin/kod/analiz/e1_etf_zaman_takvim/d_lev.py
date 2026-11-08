"""(d) Kaldıraçlı/ters ETF'ler: 1/3/5/20 günlük gerçekleşen kaldıraç, iz sürme hatası, oynaklık aşınması (gerçek vs teori), yıl yıl.
Teori (günlük yeniden dengeleme): E[log(1+L r)] - L·E[log(1+r)] ≈ -(L²-L)/2·σ² (günlük) -> yıllık aşınma ≈ (L²-L)/2·σ²_yıllık (+ ücret/finansman)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("d_")
pd.set_option("display.width", 250)
PAIRS = [("UGL", "GLD"), ("GLL", "GLD"), ("NUGT", "GDX"), ("DUST", "GDX"), ("JNUG", "GDXJ"), ("JDST", "GDXJ"), ("AGQ", "SLV"), ("ZSL", "SLV")]
lev_rows = []; drag_rows = []; yr_rows = []
for le, un in PAIRS:
    Ls = lev_sched(le)
    df = pd.DataFrame({"l": R[le], "u": R[un], "L": Ls}).dropna()
    for regime, msk in [("tum", slice(None)), ("3x_donemi(<2020-04)", df.index < SW), ("2x_donemi(>=2020-04)", df.index >= SW)]:
        q = df[msk] if not isinstance(msk, slice) else df
        if len(q) < 200 or (le in ("UGL", "GLL", "AGQ", "ZSL") and regime != "tum"): continue
        Lnom = q.L.iloc[-1] if regime != "tum" else q.L.iloc[-1]
        for h in [1, 3, 5, 20]:
            # örtüşmeyen h günlük basit getiriler
            g = (q.index.to_series().reset_index(drop=True).index // h)
            lh = np.expm1(q.l.groupby(g.values).sum()); uh = np.expm1(q.u.groupby(g.values).sum())
            b = np.polyfit(uh, lh, 1)[0]
            te = (lh - Lnom * uh).std()
            lev_rows.append(dict(letf=le, alt=un, rejim=regime, L_nominal=Lnom, h=h, n=len(lh), gerceklesen_kaldirac=round(b, 3),
                                 sapma_std_bps=round(te * 1e4, 1), ort_sapma_bps=round((lh - Lnom * uh).mean() * 1e4, 1),
                                 kor=round(np.corrcoef(uh, lh)[0, 1], 4)))
        # aşınma: yıllık log fark ve teori
        dd = q.l - q.L * q.u
        sig2 = q.u.var() * 252
        th = -(Lnom ** 2 - Lnom) / 2 * sig2
        drag_rows.append(dict(letf=le, alt=un, rejim=regime, L=Lnom, yillik_log_fark_pct=round(dd.mean() * 252 * 100, 1), teori_asinma_pct=round(th * 100, 1),
                              ucret_finansman_vb_pct=round((dd.mean() * 252 - th) * 100, 1), alt_vol_pct=round(np.sqrt(sig2) * 100, 1), n=len(q),
                              h1_asinma_bps=round(dd.mean() * 1e4, 1), h5_asinma_bps=round(dd.mean() * 5 * 1e4, 1)))
    # yıl yıl gerçek vs L×alt (toplam getiri, %)
    for y, q in df.groupby(df.index.year):
        Ly = q.L.iloc[-1]
        yr_rows.append(dict(letf=le, alt=un, yil=y, L=Ly, letf_getiri_pct=round(np.expm1(q.l.sum()) * 100, 1), alt_getiri_pct=round(np.expm1(q.u.sum()) * 100, 1),
                            L_kere_alt_pct=round(Ly * np.expm1(q.u.sum()) * 100, 1), log_fark_pct=round((q.l - Ly * q.u).sum() * 100, 1), alt_vol=round(q.u.std() * np.sqrt(252) * 100, 1)))
    st = dict(ic=float((df.l - df.L * df.u).mean()), t=float(nw_ols(df.l - df.L * df.u, pd.Series(1.0, index=df.index), 5, add_const=False)["t"]), n=len(df))
    reg("d_drag", f"d_drag|{le}", f"{le} - L·{un} günlük log fark (aşınma)", 1, st, "aşınma testi")
LV = pd.DataFrame(lev_rows); DR = pd.DataFrame(drag_rows); YR = pd.DataFrame(yr_rows)
LV.to_csv(f"{O}/d_gerceklesen_kaldirac.csv", index=False); DR.to_csv(f"{O}/d_asinma.csv", index=False); YR.to_csv(f"{O}/d_yillik_kaldirac.csv", index=False)
print(LV.to_string()); print(DR.to_string())
print(YR[YR.letf.isin(["UGL", "NUGT", "GLL", "DUST"])].pivot_table(index="yil", columns="letf", values=["letf_getiri_pct", "L_kere_alt_pct"]).to_string())

# Oynaklık rejimine göre 5 günlük aşınma (NUGT, UGL): σ yüksekken aşınma artar mı (bilinen σ_{t-1})
vr = []
for le, un in [("UGL", "GLD"), ("NUGT", "GDX"), ("GLL", "GLD"), ("DUST", "GDX")]:
    L = lev_sched(le); d5 = fwd(R[le] - L * R[un], 5)
    sv = R[un].rolling(20).std().shift(1) * np.sqrt(252)
    q = pd.DataFrame({"d5": d5, "sv": sv}).dropna(); q["terc"] = pd.qcut(q.sv, 3, labels=["dusuk", "orta", "yuksek"])
    g = q.groupby("terc").d5.mean() * 1e4
    st = rstats(sv, d5, 5); reg("d_volregime", f"d_volregime|{le}", f"σ20 -> 5g aşınma {le}", 5, st)
    vr.append(dict(letf=le, **{f"asinma_5g_bps_{k}": round(v, 1) for k, v in g.items()}, t=round(st["t"], 2)))
VR = pd.DataFrame(vr); VR.to_csv(f"{O}/d_asinma_vol_rejimi.csv", index=False); print(VR.to_string())
