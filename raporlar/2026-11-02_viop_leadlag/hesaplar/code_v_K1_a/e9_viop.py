"""(e) VİOP pay vadelisi işlenebilirlik: günlük bültenlerden (data/viop, mevcut günler) 47 dayanağın ön-ay (en yüksek hacimli) kontratı.
Likidite (TL hacim, işlem sayısı), Abdi-Ranaldo (2017) spread tahmini (vadeli ve spot), vadelinin KENDİ açılış gap'i -> gün-içi fade (analoji testi)."""
import sys, glob, csv; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
files = sorted(glob.glob(S + "/data/viop/viop_*.csv"))
rec = []
U = set(VIOP)
def fl(x):
    try: return float(x)
    except: return np.nan
for f in files:
    with open(f, encoding="windows-1254", errors="replace") as fh:
        rd = csv.reader(fh, delimiter=";"); hdr = [h.strip() for h in next(rd)]; next(rd)
        ix = {h: i for i, h in enumerate(hdr)}
        for r in rd:
            if len(r) < 22 or not r[1].startswith("F_"): continue
            if r[ix["PAZAR SEGMENTI"]] != "SSF": continue
            und = r[ix["DAYANAK VARLIK"]].replace(".E", "")
            if und not in U: continue
            rec.append((r[0], und, r[1], fl(r[ix["ACILIS FIYATI"]]), fl(r[ix["EN DUSUK FIYAT"]]), fl(r[ix["EN YUKSEK FIYAT"]]), fl(r[ix["KAPANIS FIYATI"]]),
                        fl(r[ix["UZLASMA FIYATI"]]), fl(r[ix["ONCEKI UZLASMA FIYATI"]]), fl(r[ix["AGIRLIKLI ORTALAMA FIYAT"]]), fl(r[ix["ISLEM HACMI"]]), fl(r[ix["ISLEM SAYISI"]]), fl(r[ix["ACIK POZISYON"]])))
F = pd.DataFrame(rec, columns=["date", "und", "code", "o", "l", "h", "c", "settle", "prev_settle", "vwap", "tl", "ntr", "oi"])
F["date"] = pd.to_datetime(F.date)
F = F[(F.tl > 0) & (F.o > 0)]
F = F.sort_values("tl").groupby(["date", "und"]).tail(1).sort_values(["und", "date"])  # ön-ay = günün en yüksek hacimli kontratı
F.to_parquet(OUT + "/res_e9_viop_front.parquet")
print("bülten günü:", F.date.nunique(), "aralık", F.date.min().date(), F.date.max().date())
R4 = pd.read_csv(OUT + "/res_e4_all47.csv").set_index("sym")
def ar_spread(o, h, l, c):
    """Abdi-Ranaldo: s^2 = 4 E[(c_t - eta_t)(c_t - eta_{t+1})], eta = orta nokta log(h,l). Negatifleri 0 (gözlem düzeyinde 'two-day' sürümü)."""
    lc, eta = np.log(c), (np.log(h) + np.log(l)) / 2
    v = 4 * (lc - eta) * (lc - eta.shift(-1))
    v2 = v.clip(lower=0)
    return float(np.sqrt(v2.mean()) * 1e4)
rows = []
for s in VIOP:
    x = F[F.und == s].set_index("date")
    if len(x) < 50: continue
    d = decomp(s, start="2022-12-01").join(x.add_prefix("f_"), how="inner")
    r = dict(sym=s, n_days=len(x), f_tl_med_mn=x.tl.median() / 1e6, f_ntr_med=x.ntr.median(), spot_tl_med_mn=d.tlv.median() / 1e6,
             f_spread_AR_bps=ar_spread(x.o, x.h, x.l, x.c), spot_spread_AR_bps=ar_spread(d.o, d.h, d.l, d.c))
    # vadeli kendi gap'i (önceki uzlaşma -> açılış) ve gün-içi (açılış -> kapanış)
    fg = np.log(x.o / x.prev_settle); fi = np.log(x.c / x.o)
    ok = fg.notna() & fi.notna() & (fg.abs() < 0.105) & (fi.abs() < 0.22)
    fg, fi = fg[ok], fi[ok]
    r["f_corr_gap_intra"] = fg.corr(fi)
    m = fg.abs() > 0.01; p = -np.sign(fg[m]) * fi[m] - 0.001; mm, t, n = nw_mean_t(p.values); r.update(f_fade_bps=1e4 * mm, f_fade_t=t, f_fade_n=n)
    # spot fade aynı günlerde (karşılaştırma)
    dd = d.dropna(subset=["gap", "intra"]); m2 = dd.gap.abs() > 0.01; p2 = -np.sign(dd.gap[m2]) * dd.intra[m2] - 0.001; mm, t, n = nw_mean_t(p2.values)
    r.update(spot_fade_bps=1e4 * mm, spot_fade_t=t, spot_fade_n=n)
    # vadeli açılışı ile spot açılışı farkı (baz düzeltmesiz, medyan |.|)
    r["med_abs_fopen_vs_sopen_bps"] = float(1e4 * (np.log(d.f_o / d.o) - np.log(d.f_settle / d.c).shift(1)).abs().median())
    rows.append(r)
V = pd.DataFrame(rows).set_index("sym"); V["liq_grp"] = R4.liq_grp
V.to_csv(OUT + "/res_e9_viop.csv")
pd.set_option("display.width", 300); print(V.sort_values("f_tl_med_mn").round(2).to_string())
print(V.groupby("liq_grp")[["f_tl_med_mn", "f_ntr_med", "f_spread_AR_bps", "spot_spread_AR_bps", "f_corr_gap_intra", "f_fade_bps", "spot_fade_bps"]].median().round(2))
