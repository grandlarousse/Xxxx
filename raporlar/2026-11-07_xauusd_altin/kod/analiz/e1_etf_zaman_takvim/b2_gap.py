"""(b2) Madenci açılış boşluğu dönüşü: gece_t (gün t 09:30 ET açılışı / t-1 kapanışı; 09:30 ET = 13:30/14:30 UTC'de bilinir, karar anı 15:00 ET'den önce).
Ayrışım: gece_t -> gece_{t+1} mi gün içi_{t+1} mi? Strateji: boşluk z-skoru eşikleri (IS'te seçim), yalnız uzun / ters ETF / kaldıraçlı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("b2_")
pd.set_option("display.width", 250)
rows = []; tabs = []; dec = []
for t in ["GDX", "GDXJ", "GLD", "SLV"]:
    n, d, tot = night_day(t)
    sig = R[t].rolling(60).std().shift(1)          # t-1'e kadar bilinen oynaklık
    z = n / sig
    for comp, y in [("gece_t+1", n.shift(-1)), ("gun_ici_t+1", d.shift(-1)), ("toplam_t+1", R[t].shift(-1))]:
        st = rstats(z, y, 1, method="spearman"); reg("b2_decomp", f"b2_decomp|{t}|{comp}", f"gap z_t -> {comp}", 1, st)
        dec.append(dict(etf=t, hedef=comp, ic=round(st["ic"], 3), t=round(st["t"], 2), t_is=round(st["t_is"], 2), t_oos=round(st["t_oos"], 2), t_22=round(st["t_22"], 2), yrs=f"{st['yrs_same_sign']}/{st['yrs']}"))
    if t in ("GDX", "GDXJ"):
        # placebo: gelecek boşluk (t+1) ve daha eski boşluk
        pl = placebo_lead(z, R[t], 1); print(t, "placebo_lead (shift<0 = gelecek):", pl)
        for thr in [0.0, 0.5, 1.0, 1.5]:
            x = pd.Series(np.where(z < -thr, 1.0, np.where(z > thr, -1.0, 0.0)), index=IDX).where(z.notna())
            for h in [1, 3]:
                st = rstats(x, fwd(R[t], h), h); reg("b2_rule", f"b2_rule|{t}|thr{thr}|h{h}", f"-sign(gap z) |z|>{thr}", h, st)
                rows.append(dict(etf=t, thr=thr, h=h, t=round(st["t"], 2), t_is=round(st["t_is"], 2), t_oos=round(st["t_oos"], 2), t_22=round(st["t_22"], 2), yrs=f"{st['yrs_same_sign']}/{st['yrs']}", n_sig=int((x != 0).sum())))
                for leg, m in [("uzun", x > 0), ("kisa", x < 0)]:
                    s = m.astype(float).where(x.notna()); st2 = rstats(s, fwd(R[t], h), h)
                    reg("b2_leg", f"b2_leg|{t}|thr{thr}|h{h}|{leg}", f"gap leg {leg}", h, st2)
                    rows[-1][f"t_{leg}"] = round(st2["t"], 2); rows[-1][f"t_oos_{leg}"] = round(st2["t_oos"], 2)
DEC = pd.DataFrame(dec); DEC.to_csv(f"{O}/b2_gap_ayrisim.csv", index=False); print(DEC.to_string())
RU = pd.DataFrame(rows); RU.to_csv(f"{O}/b2_gap_kurallar.csv", index=False); print(RU.to_string())
# IS'te seç (h=1; |t_is| en büyük eşik) -> strateji tabloları
for t in ["GDX", "GDXJ"]:
    q = RU[(RU.etf == t) & (RU.h == 1)]; b = q.iloc[q.t_is.abs().argmax()]
    n, d, tot = night_day(t); z = n / R[t].rolling(60).std().shift(1); thr = b.thr
    x = pd.Series(np.where(z < -thr, 1.0, np.where(z > thr, -1.0, 0.0)), index=IDX).where(z.notna()).fillna(0)
    print(t, "IS-seçilen eşik", thr)
    tabs.append(strat_table(x, 1, t, f"{t}_gaprev_thr{thr}"))
T = pd.concat(tabs); T.to_csv(f"{O}/b2_gap_strateji.csv", index=False)
print(pivot_short(T).to_string())
print(T[(T.period == "oos") & (T.version.isin(["long_only", "inv_DUST", "inv_JDST", "lev_NUGT", "lev_JNUG"]))][["strategy", "version", "cost", "sh", "ann", "rt_yr", "bh_sh"]].to_string())
