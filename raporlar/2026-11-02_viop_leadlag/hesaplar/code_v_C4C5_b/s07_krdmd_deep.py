"""s07: (b) SHFE HRC -> KRDMD gün-içi: çürütme testleri (kendi roll serim, günlük 2018-05+).
 1) Bayat açılış (KRDMD o == önceki c; 2014-20'de günlerin %15-46'sı) ayrımı ve tik büyüklüğü etkisi.
 2) Ortak Asya faktörü: HSI, Şanghay, 0700.HK, FMG.AX, Baosteel, Sinopec... kontrol edilince HC kalıyor mu? HC'ye özgü mü?
 3) Plasebo hedefler: HC D_t -> 47 hissenin gün-içi (çelik dışı da tahmin ediliyor mu?).
 4) Alt dönemler, gapD/ocD alt dönemlerde, uç değer, dairesel null."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
from scipy.stats import spearmanr
kr = bist_dec("KRDMD.IS"); y = kr.intra
R = sina_roll("HC")
HC = to_bist(R["cc"], "zero").reindex(y.index); gD = to_bist(R["gapD"], "zero").reindex(y.index); oD = to_bist(R["ocD"], "zero").reindex(y.index)
ST = "2018-06-01"
d = daily_local("KRDMD.IS")
stale = (np.abs(np.log(d.o / d.c.shift(1))) < 1e-6).reindex(y.index).fillna(False).astype(bool)
print("== 1) Bayat açılış ayrımı (2018-06+) ==")
for lab, m in [("tümü", pd.Series(True, index=y.index)), ("bayat açılış", stale), ("normal açılış", ~stale)]:
    mm = m & (y.index >= ST)
    b, t, n = nw_t(y[mm], HC[mm]); print(f"  {lab:14s} r={b:+.3f} t={t:+.2f} n={n}")
px = d["c"].reindex(y.index); tick_rel = (0.01 / px)
print("  KRDMD fiyatı (yıl medyanı):", px.groupby(px.index.year).median().round(2).loc[2014:].to_dict())
for lab, m in [("göreli tik >0,5%", tick_rel > 0.005), ("göreli tik <=0,5%", tick_rel <= 0.005)]:
    mm = m & (y.index >= ST); b, t, n = nw_t(y[mm], HC[mm]); print(f"  {lab:18s} r={b:+.3f} t={t:+.2f} n={n}")
print("\n== 2) Ortak Asya faktörü kontrolü (2018-06+) ==")
A = {}
for s in ["^HSI", "000001.SS", "0700.HK", "FMG.AX", "600019.SS", "600028.SS", "601088.SS", "603993.SS", "0347.HK", "^AXJO", "^N225", "^KS11"]:
    A[s] = to_bist(loc_ret(s, "adj"), "zero").reindex(y.index)
Xa = pd.DataFrame({"HC": HC, **A, "kr_gap": kr.gap, "kr_intra_l1": y.shift(1)})
Xa = Xa[Xa.index >= ST]
for s in A:
    b, t, n = nw_t(y[y.index >= ST], A[s][A[s].index >= ST]); print(f"  {s:10s} -> KRDMD intra: r={b:+.3f} t={t:+.2f}")
for cols in [["HC", "000001.SS", "600019.SS"], ["HC", "FMG.AX"], ["HC", "600028.SS", "601088.SS"], ["HC", "kr_gap", "kr_intra_l1"], ["HC", "FMG.AX", "600019.SS", "601088.SS", "603993.SS", "000001.SS", "kr_gap", "kr_intra_l1"]]:
    r, n = ols_nw(y, Xa[cols]); print(f"  n={n} " + " | ".join(f"{i}: {v.b:+.3f} (t {v.t:+.2f})" for i, v in r.iterrows()))
# HC'nin Asya 'çelik dışı' faktöründen arındırılmış kısmı
print("\n== 3) Plasebo hedefler: HC D_t -> gün-içi (2018-06+) ==")
VIOP = "AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK XU100".split()
res = {}
for s in VIOP:
    yy = bist_dec(s + ".IS").intra; yy = yy[yy.index >= ST]
    res[s] = nw_t(yy, to_bist(R["cc"], "zero").reindex(yy.index))[1]
res = pd.Series(res).sort_values(ascending=False)
print("  en yüksek 10:", res.head(10).round(2).to_dict()); print("  medyan t (KRDMD hariç):", round(res.drop("KRDMD").median(), 2), " #t>2:", int((res.drop('KRDMD') > 2).sum()), "/", len(res) - 1)
# aynı hedef plasebosu: rastgele Asya sinyallerinin KRDMD gün-içi t dağılımı (s03'ten)
P = pd.read_csv(sys.path[0] + "/s03_placebo_matrix.csv")
kk = P[(P.tgt == "KRDMD")]; print("  s03: KRDMD hedefinde 27 Asya sinyali t dağılımı (2014+):", kk.t.describe().round(2).to_dict())
print("\n== 4) Alt dönemler: cc / gapD / ocD -> KRDMD intra ==")
for a, b_ in [("2018-06-01", "2021-01-01"), ("2021-01-01", "2024-01-01"), ("2024-01-01", "2027-01-01"), ("2023-08-01", "2027-01-01")]:
    m = (y.index >= a) & (y.index < b_)
    o = []
    for nm, s in [("cc", HC), ("gapD", gD), ("ocD", oD)]:
        bb, t, n = nw_t(y[m], s[m]); o.append(f"{nm} r={bb:+.3f} t={t:+.2f}")
    print(f"  {a[:7]}..{b_[:7]} " + " | ".join(o) + f" n={n}")
print("\n== 5) Uç değer ==")
df = pd.concat([HC.rename("s"), y.rename("y")], axis=1).dropna(); df = df[(df.index >= ST) & (df.s != 0)]
print("  Pearson", round(df.s.corr(df.y), 4), "Spearman", round(spearmanr(df.s, df.y)[0], 4), "n", len(df))
w = df.clip(df.quantile(.01), df.quantile(.99), axis=1); print("  winsor %1 t", round(nw_t(w.y, w.s)[1], 2))
# en büyük |y| 1% günleri atılınca (her iki yön)
thr = df.y.abs().quantile(.99); m = df.y.abs() < thr; print(f"  en büyük %1 |KRDMD gün-içi| günleri atılınca t={nw_t(df.y[m], df.s[m])[1]:+.2f}")
r, pnl, pos = bt(HC, y, 10, start=ST); print("  BT 10bps:", fmt(r))
r15, _, _ = bt(HC, y, 15, start=ST); print("  BT 15bps:", fmt(r15))
a = pnl[pos != 0]; srt = a.sort_values(ascending=False)
for k in [5, 10, 20]:
    rest = a.drop(srt.index[:k]); print(f"  en iyi {k} işlem atılınca ort {1e4*rest.mean():+.2f} bps")
# dairesel null
rng = np.random.default_rng(11); base = nw_t(df.y, df.s)[1]; sv = HC.reindex(y.index).values; null = []
yy = y.copy(); yy[yy.index < ST] = np.nan
for k in rng.integers(60, len(sv) - 60, 500):
    null.append(nw_t(yy, pd.Series(np.roll(sv, k), index=y.index))[1])
null = np.abs(np.array(null)); print(f"  dairesel null: gerçek t={base:.2f}; %95={np.nanquantile(null,.95):.2f} %99={np.nanquantile(null,.99):.2f} p={np.mean(null>=abs(base)):.3f}")
