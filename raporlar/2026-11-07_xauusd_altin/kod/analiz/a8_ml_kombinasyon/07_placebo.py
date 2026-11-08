"""Adım 7: ileriye bakma tanısı — model tahminleri için placebo_lead (tahmin serisini ±gün kaydır, IC'ye bak).
Kaydırma -1/-2 = geleceğin tahmini (yasak bilgi; IC'nin artması beklenir çünkü özellikler hedef penceresiyle örtüşür),
0 = gerçek, +1..+3 = daha eski tahmin. Gerçek (0) IC'nin -1'den belirgin küçük olması ve 0 ile +1'in benzer büyüklükte olması
'öznitelik hedefi zaten içeriyor' şüphesini dışlar. Ayrıca ham öznitelikler için hedefle aynı gün (v_ret_t, 15:10'da biten) korelasyonu."""
from common import *
from features import build

d = load_viop()
ML = ["ridge", "lasso", "enet", "hgb", "rf"]
rows = []
for V in ("V1", "V2"):
    P_ = pd.read_parquet(f"{OUT}/preds_{V}.parquet"); P_["date"] = pd.to_datetime(P_["date"])
    ens = P_[P_.model.isin(ML)].groupby(["date", "h"]).agg(yhat=("yhat", "mean"), ybar=("ybar", "first"), ybar_w=("ybar_w", "first")).reset_index(); ens["model"] = "ens_ml"
    P_ = pd.concat([P_, ens], ignore_index=True)
    for h in (1, 3, 5):
        for m in ("ens_ml", "ridge", "rf", "hgb", "c1_apriori_score"):
            q = P_[(P_.model == m) & (P_.h == h)].set_index("date")
            x = q.yhat - q.ybar_w if not m.endswith("_score") else q.yhat
            x = x.where(x.abs() > 1e-9, 0.0).reindex(d.index)
            rows.append(dict(V=V, model=m, h=h, **{f"shift{k}": v for k, v in placebo_lead(x, d.v_ret, h).items()}))
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/placebo_preds.csv", index=False)
pd.set_option("display.width", 200)
print(R.to_string(index=False))
