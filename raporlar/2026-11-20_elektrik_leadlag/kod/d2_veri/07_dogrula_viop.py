"""VİOP panel doğrulaması. Spot ham kapanış: D1'in panel_full/close_raw.parquet (hisse) ve idx.parquet (XU030) dosyaları.
Çıktı: RAW/dogrulama_viop.txt (ekrana da yazar).  Kullanım: python3 -I 07_dogrula_viop.py"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2common import RAW, FULL
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)
d = pd.read_parquet(f"{FULL}/viop_daily.parquet"); f = pd.read_parquet(f"{FULL}/viop_front.parquet")
cr = pd.read_parquet(f"{FULL}/close_raw.parquet"); ix = pd.read_parquet(f"{FULL}/idx.parquet")
spot = cr.join(ix[["XU030"]], how="outer")
P("== 1. Takvim: bülten günleri ile spot işlem günleri (XU030 endeksi dolu günler)")
bd = pd.DatetimeIndex(sorted(d["date"].unique())); sd = spot.index[spot["XU030"].notna() & (spot.index >= bd.min()) & (spot.index <= bd.max())]
P("bülten günü", len(bd), "spot günü", len(sd), "| spotta var bültende yok:", [str(x.date()) for x in sd.difference(bd)][:20],
  "| bültende var spotta yok:", [str(x.date()) for x in bd.difference(sd)][:20])
P("== 2. Dayanak özeti (viop_front)")
rows = []
for u, g in f.groupby("und"):
    g = g.set_index("date"); last = g.loc[g.index >= "2025-11-20"]
    s = spot[u].reindex(g.index) if u in spot else pd.Series(np.nan, index=g.index)
    ratio = (g["uzlasma"] * g["fiyat_carpani"] / s).dropna()
    ann = ((ratio - 1) * 365 / g["vkg"].reindex(ratio.index).clip(lower=5))
    rs = g["ret_settle"]; sr = s.pct_change(fill_method=None)
    rows.append(dict(und=u, ilk=str(g.index.min().date()), gun=len(g), sifir_hacim_oran=round((g["hacim_tl"] <= 0).mean(), 4),
                     medyan_hacim_mnTL_son1y=round(last["hacim_tl"].median() / 1e6, 1), gecis=int(g["vade_degisti"].sum()),
                     yakin_vade_oran=round(g["yakin_mi"].mean(), 3), oran_p1=round(ratio.quantile(.01), 4) if len(ratio) else np.nan,
                     oran_medyan=round(ratio.median(), 4) if len(ratio) else np.nan, oran_p99=round(ratio.quantile(.99), 4) if len(ratio) else np.nan,
                     oran_min=round(ratio.min(), 4) if len(ratio) else np.nan, oran_max=round(ratio.max(), 4) if len(ratio) else np.nan,
                     n_oran_disi=int(((ratio < 0.93) | (ratio > 1.12)).sum()), yillik_baz_medyan=round(ann.median(), 3) if len(ann) else np.nan,
                     korr_spot=round(rs.corr(sr), 4) if len(ratio) else np.nan, max_abs_ret_settle=round(rs.abs().max(), 4),
                     ret_last_nan=round(g["ret_last"].isna().mean(), 4)))
P(pd.DataFrame(rows).to_string(index=False))
P("== 3. Uzlaşma/spot oranı sınır dışı günler (oran<0,93 ya da >1,12)")
for u in ["AKSEN", "ENJSA", "ODAS", "ASTOR", "ALARK", "XU030"]:
    g = f[f["und"] == u].set_index("date"); ratio = (g["uzlasma"] * g["fiyat_carpani"] / spot[u].reindex(g.index)).dropna()
    b = ratio[(ratio < 0.93) | (ratio > 1.12)]
    if len(b): P(u, len(b), [(str(k.date()), round(v, 3), int(g.loc[k, "vkg"])) for k, v in b.items()][:12])
P("== 4. Vade geçişi: sürekli seride sıçrama var mı? (geçiş günlerinde |ret_settle| ile aynı gün spot getirisi farkı; 'naif' = sözleşmeler arası oran)")
for u in ["AKSEN", "ENJSA", "ODAS", "ASTOR", "ALARK", "XU030"]:
    g = f[f["und"] == u].set_index("date"); sr = spot[u].pct_change(fill_method=None).reindex(g.index)
    naive = (g["uzlasma"] * g["fiyat_carpani"]).pct_change(fill_method=None); roll = g["vade_degisti"]
    dif = (g["ret_settle"] - sr).abs(); difn = (naive - sr).abs()
    P(u, "geçiş", int(roll.sum()), "| |vadeli-spot| medyan bps: geçiş günü", round(1e4 * dif[roll].median(), 1), "diğer", round(1e4 * dif[~roll].median(), 1),
      "| naif seride geçiş günü", round(1e4 * difn[roll].median(), 1))
P("== 5. viop_daily: sözleşme sayısı ve tutarlılık")
P("satır", len(d), "| uzlasma<=0:", int((d["uzlasma"] <= 0).sum()), "| vade<date:", int((d["vkg"] < 0).sum()), "| duz_carpan!=1:", int(((d["duz_carpan"] - 1).abs() > 1e-4).sum()),
  d.loc[(d["duz_carpan"] - 1).abs() > 1e-4, ["date", "kod", "duz_carpan"]].astype(str).values.tolist()[:5])
P("aynı (date,kod) yinelenen:", int(d.duplicated(["date", "kod"]).sum()), "| front (date,und) yinelenen:", int(f.duplicated(["date", "und"]).sum()))
chk = d.sort_values(["kod", "date"]); lag = chk.groupby("kod")["uzlasma"].shift(1)
mm = ((chk["onceki_uzlasma"] - lag).abs() / lag > 1e-6) & lag.notna() & (chk["onceki_uzlasma"] > 0)
P("bültendeki ONCEKI UZLASMA != dünkü uzlasma (aynı sözleşme):", int(mm.sum()), chk.loc[mm, "und"].value_counts().to_dict())
e = f[f["und"] == "ELCBAS"]
P("== 6. Baz yük elektrik (ELCBAS yakın vade): yıllara göre işlem olan gün sayısı", e.groupby(e["date"].dt.year)["hacim_tl"].apply(lambda s: int((s > 0).sum())).to_dict())
open(f"{RAW}/dogrulama_viop.txt", "w").write("\n".join(out) + "\n")
