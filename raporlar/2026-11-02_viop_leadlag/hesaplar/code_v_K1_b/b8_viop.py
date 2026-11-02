"""VİOP pay vadelisi CIMSA/OYAKC: ilk listelenme (bülten verisi içinde), yıllara göre ön-ay likiditesi, işlem olmayan gün oranı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
V = pd.read_parquet(S + "/data/viop_panel.parquet")
V = V[V.segment == "SSF"]
print("bülten tarih aralığı:", V.date.min().date(), V.date.max().date(), "gün sayısı", V.date.nunique())
alld = pd.Series(pd.to_datetime(sorted(V.date.unique())))
for s in ["CIMSA", "OYAKC", "AKBNK", "THYAO"]:
    z = V[V.root == s].copy()
    if z.empty: print(s, "yok"); continue
    z = z.sort_values(["date", "expiry"])
    front = z.groupby("date").head(1)
    firsts = z.date.min().date()
    agg = front.assign(y=front.date.dt.year).groupby("y").agg(gun=("date", "nunique"), med_deger_mnTL=("value_tl", lambda x: round(x.median() / 1e6, 1)),
                                                               med_islem=("trades", "median"), sifir_islem=("trades", lambda x: round((x.fillna(0) == 0).mean(), 3)))
    tot = z.groupby("date").value_tl.sum()
    print(f"\n{s}: bültende ilk görülme {firsts}; bülten günlerinin %{100*len(set(z.date))/len(alld):.0f}'inde var")
    print(agg.to_string())
# bülten kapsamı yıllara göre
print("\nbülten gün sayısı/yıl:", alld.dt.year.value_counts().sort_index().to_dict())
