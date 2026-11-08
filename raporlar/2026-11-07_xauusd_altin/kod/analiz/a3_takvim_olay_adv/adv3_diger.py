"""Hakem: OG vade günü, bayram sonrası, Ocak etkisi + çoklu test. python3 -W ignore adv3_diger.py"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
O = f"{S}/out/a3_takvim_olay"
sys.path.insert(0, f"{S}/code")
from lib_altin import *
from scipy import stats as sst
d = load_viop(); s = load_spot(); V = d.index; r = d.v_ret; SPA = s.index
def tsimple(z): z = pd.Series(z).dropna(); return z.mean() / z.std() * np.sqrt(len(z))
def first_ge(idx, dates, strict=False):
    a = idx.values; q = pd.DatetimeIndex(pd.to_datetime(pd.Series(dates)).dropna()).values
    p = np.searchsorted(a, q, side="right" if strict else "left"); return np.unique(p[p < len(idx)])
def dummy(idx, p, shift=0):
    p = np.asarray(p, int) + shift; p = p[(p >= 0) & (p < len(idx))]; D = pd.Series(0.0, index=idx); D.iloc[np.unique(p)] = 1.0; return D
def blocks(y, D, lab, periods=((2017, 2019), (2020, 2021), (2022, 2023), (2024, 2026))):
    ev = y[D == 1]; ne = y[D == 0]
    for lo, hi in periods:
        m = (ev.index.year >= lo) & (ev.index.year <= hi); mn = (ne.index.year >= lo) & (ne.index.year <= hi)
        xx = ev[m] - ne[mn].mean()
        print(f"  {lab} {lo}-{hi}: n={m.sum()} diff={xx.mean()*1e4:7.1f} t_basit={tsimple(xx):5.2f} isabet(<0)={(ev[m]<0).mean():.2f}")

print("=" * 20, "OG vade günü (OE-1 uzlaşmasında kısa, OE uzlaşmasında çık)", "=" * 20)
cx = pd.read_csv(f"{O}/events_comex.csv", parse_dates=["og_expiry", "og_alt"])
# kural doğrulama: bildiğim vadeler (CME: 'ayın sondan 4. iş günü; Cuma/tatil arifesiyse bir önceki iş günü')
known = {"2024-03": "2024-03-25", "2024-11": "2024-11-25", "2025-01": "2025-01-28", "2025-11": "2025-11-24", "2026-01": "2026-01-27"}
for k, v in known.items():
    row = cx[cx.og_expiry.dt.strftime("%Y-%m") == k]
    print("  ", k, "kural:", row.og_expiry.dt.strftime("%Y-%m-%d").tolist(), " beklenen:", v)
OE = first_ge(V, cx.og_expiry); exact = np.isin(V[OE], cx.og_expiry.values)
print("  OE günü VİOP'ta açık:", exact.sum(), "/", len(OE), " (kapalıysa sonraki VİOP günü sayılıyor -> kayma)")
D = dummy(V, OE, -1); y = d.fwd1
ev = y[D == 1]; ne = y[D == 0]; print(f"  n={len(ev)} diff={(ev.mean()-ne.mean())*1e4:.1f} t_NW={ic(D, y, 5, 'pearson')['t']:.2f} t_basit={tsimple(ev-ne.mean()):.2f}")
blocks(y, D, "OG")
# yalnız VİOP'un tam OE günü açık olduğu olaylar
D2 = dummy(V, OE[exact], -1); e2 = y[D2 == 1]; print(f"  tam-gün eşleşen: n={len(e2)} diff={(e2.mean()-y[D2==0].mean())*1e4:.1f} t={tsimple(e2-y[D2==0].mean()):.2f}")
srt = (ev - ne.mean()).sort_values()
for kk in (1, 3, 5): print(f"  en kötü (en kârlı kısa) {kk} hariç: diff={srt.iloc[kk:].mean()*1e4:.1f} t={tsimple(srt.iloc[kk:]):.2f}")
print("  en büyük katkılar:", (srt.head(6) * 1e4).round(0).to_dict())
# komşu günler: OE-2, OE-1(=kendisi), OE, OE+1 getirileri
for sh in (-3, -2, -1, 0, 1):
    Dk = dummy(V, OE, sh); e = y[Dk == 1]; print(f"   giriş OE{sh:+d}: diff={(e.mean()-y[Dk==0].mean())*1e4:6.1f} t={ic(Dk, y, 5, 'pearson')['t']:.2f}")
# spot uzun örneklem
OEs = first_ge(SPA, cx.og_expiry); Ds = dummy(SPA, OEs, -1)
blocks(s.sfwd1, Ds, "OG spot", ((2010, 2013), (2014, 2016), (2017, 2019), (2020, 2021), (2022, 2023), (2024, 2026)))
es = s.sfwd1[Ds == 1]; print(f"  spot 2010-2026: diff={(es.mean()-s.sfwd1[Ds==0].mean())*1e4:.1f} t={tsimple(es - s.sfwd1[Ds==0].mean()):.2f} n={len(es)}")
oos = V > IS_END
for c in (5, 10):
    b = backtest(-D[oos], r[oos], 1, c); bi = backtest(-D[~oos], r[~oos], 1, c); print(f"  kısa kural maliyet {c}: IS sh {bi['sharpe']:.2f} OOS sh {b['sharpe']:.2f}")

print("\n" + "=" * 20, "Bayram sonrası (ilk VİOP günü kısa, 5 gün)", "=" * 20)
bay = pd.read_csv(f"{O}/events_tr_bayram.csv", parse_dates=["start", "arife"])
post_raw = np.searchsorted(V.values, bay.start.values)
print("  analist kodu post_b (filtresiz): 0 konumuna düşen bayram sayısı =", (post_raw == 0).sum(), "-> sahte olay", V[0].date())
Dan = dummy(V, post_raw); y5 = d.fwd5
e = y5[Dan == 1]; print(f"  analist tanımı: n={len(e)} diff={(e.mean()-y5[Dan==0].mean())*1e4:.1f} t_NW={ic(Dan, y5, 5, 'pearson')['t']:.2f}")
post_ok = post_raw[(post_raw > 0) & (post_raw < len(V))]
Dfix = dummy(V, post_ok); e = y5[Dfix == 1]; ne = y5[Dfix == 0]
o = ic(Dfix, y5, 5, "pearson"); m = V <= IS_END
print(f"  DÜZELTİLMİŞ (2017-03-06 sahte olay çıkarıldı): n={len(e)} diff={(e.mean()-ne.mean())*1e4:.1f} t_NW={o['t']:.2f} t_basit={tsimple(e-ne.mean()):.2f} IS t={ic(Dfix[m], y5[m], 5, 'pearson')['t']:.2f} OOS t={ic(Dfix[~m], y5[~m], 5, 'pearson')['t']:.2f}")
blocks(y5, Dfix, "BAY")
srt = (e - ne.mean()).sort_values()
for kk in (1, 3): print(f"  en kârlı (en negatif) {kk} hariç: diff={srt.iloc[kk:].mean()*1e4:.1f} t={tsimple(srt.iloc[kk:]):.2f}")
# yerel drift: ±63 gün merkezli
pos = np.where(Dfix.values == 1)[0]; cen = []
for p in pos:
    w = list(range(max(0, p-63), max(0, p-5))) + list(range(min(len(V), p+6), min(len(V)-5, p+69))); cen.append(y5.iloc[w].mean())
xx = e.values - np.array(cen); print(f"  yerel drift düzeltilmiş: {np.nanmean(xx)*1e4:.1f} t={tsimple(xx):.2f}")
# Ramazan vs Kurban
for nm in ["Ramazan Bayramı", "Kurban Bayramı"]:
    pp = np.searchsorted(V.values, bay[bay.bayram == nm].start.values); pp = pp[(pp > 0) & (pp < len(V))]
    ee = y5.iloc[pp]; print(f"  {nm}: n={len(ee)} ort={ee.mean()*1e4:.1f} (koşulsuz {y5.mean()*1e4:.1f}) t={tsimple(ee - y5.mean()):.2f}")
# komşu h ve giriş kaydırma
for sh in (-1, 0, 1, 2):
    for h in (3, 5, 10):
        Dk = dummy(V, post_ok, sh); yy = d[f"fwd{h}"]; ee = yy[Dk == 1]
        print(f"   giriş post{sh:+d} h{h}: diff={(ee.mean()-yy[Dk==0].mean())*1e4:7.1f} t={ic(Dk, yy, max(h,5), 'pearson')['t']:.2f}")
# spot 2010-2016: bayram sonrası ilk spot günü (bayram bitişi sonrası)
ends = [b.start + pd.Timedelta(days=int(b.days)) for _, b in bay.iterrows()]
Ps = first_ge(SPA, ends); Dsp = dummy(SPA, Ps)
blocks(s.sfwd5, Dsp, "BAY spot", ((2010, 2013), (2014, 2016), (2017, 2021), (2022, 2026)))

print("\n" + "=" * 20, "Ocak etkisi (getiri günü Ocak, h=1)", "=" * 20)
nm_ = pd.Series(np.r_[V.month[1:], [np.nan]], index=V); Dj = (nm_ == 1).astype(float); y1 = d.fwd1
ev = y1[Dj == 1]; ne = y1[Dj == 0]
print(f"  diff={(ev.mean()-ne.mean())*1e4:.1f} bps/gün t_NW={ic(Dj, y1, 5, 'pearson')['t']:.2f}")
jy = ev.groupby(ev.index.year).sum() * 1e4; ny = ne.groupby(ne.index.year).mean() * 1e4
print("  yıllık Ocak toplam getiri (bps):", jy.round(0).to_dict())
# yıl bazında Ocak ortalaması - diğer aylar ortalaması: 10 bağımsız gözlem
ym = (ev.groupby(ev.index.year).mean() - ne.groupby(ne.index.year).mean()).dropna() * 1e4
print("  yıl bazında fark (bps/gün):", ym.round(1).to_dict(), f" -> t(yıllık, n={len(ym)})={tsimple(ym):.2f}; 2026 hariç t={tsimple(ym.drop(2026, errors='ignore')):.2f}")
blocks(y1, Dj, "OCA")
for ex in [2026, 2017]:
    m = V.year != ex; o = ic(Dj[m], y1[m], 5, "pearson"); print(f"  {ex} hariç t_NW={o['t']:.2f}")
m = (V.year != 2026) & (V.year != 2017); print(f"  2017+2026 hariç t_NW={ic(Dj[m], y1[m], 5, 'pearson')['t']:.2f}")
nms = pd.Series(np.r_[SPA.month[1:], [np.nan]], index=SPA); Djs = (nms == 1).astype(float)
ysp = s.sfwd1; es_ = ysp[Djs == 1]; ns_ = ysp[Djs == 0]
ym_s = (es_.groupby(es_.index.year).mean() - ns_.groupby(ns_.index.year).mean()).dropna() * 1e4
print("  spot yıl bazında fark:", ym_s.round(1).to_dict())
for lo, hi in [(2010, 2016), (2010, 2026)]:
    z = ym_s[(ym_s.index >= lo) & (ym_s.index <= hi)]; print(f"  spot {lo}-{hi} yıllık t={tsimple(z):.2f} pozitif {int((z>0).sum())}/{len(z)}")
# 12 ay seçiminde en iyi ay olmanın şansı
print("  12 ay h1 t'leri (analist):  Oca 2.03, Haz -2.20, Eyl -1.75, Ara 1.69 ... max|t| 12 testte beklenen ~1.7-2.0")

print("\n" + "=" * 20, "Çoklu test: analist ailesi ve global kayıt", "=" * 20)
reg = pd.read_csv(f"{O}/registry_with_q.csv")
print("  a3 kayıt satırı:", len(reg))
import glob
G = pd.concat([pd.read_csv(f) for f in glob.glob(f"{S}/out/registry/*.csv")], ignore_index=True)
G = G[G.t.notna()].copy(); G["p"] = 2 * (1 - sst.norm.cdf(G.t.abs())); G["q_global"] = bh_fdr(G.p.values)
print("  global kayıt (t'si olan) satır:", len(G), " ajan:", G.agent.nunique())
for tid in ["QEND_TDE1_h3", "NFP_cond_spot12to15_h1", "NFP_cond_spot12to15_h3", "OG_OEday_h1", "BAYRAM_post_h5", "MONTH_Oca_h1"]:
    g = G[(G.agent == "a3_takvim_olay") & (G.test_id == tid)]
    rr = reg[reg.test_id == tid]
    if len(g):
        t = g.t.iloc[0]; p = g.p.iloc[0]
        print(f"  {tid}: t={t:.2f} p={p:.4f} Bonferroni(182)={min(1,p*182):.3f} q_a3={rr.q.iloc[0] if len(rr) else np.nan:.3f} q_global={g.q_global.iloc[0]:.3f} Bonf(global)={min(1, p*len(G)):.2f}")
# işaret kuralı t'leri ile (NFP için analistin raporladığı 2.42/2.51)
for lab, t in [("NFP h1 işaret t=2.42", 2.42), ("NFP h3 işaret t=2.51", 2.51), ("NFP h1 basit işaret t=2.05", 2.05)]:
    p = 2 * (1 - sst.norm.cdf(t)); rank_q = bh_fdr(np.r_[reg.p.fillna(1).values, p])[-1]
    print(f"  {lab}: p={p:.4f} Bonf(182)={min(1, p*182):.2f} BH-q(a3 ailesine eklenince)≈{rank_q:.2f}")
