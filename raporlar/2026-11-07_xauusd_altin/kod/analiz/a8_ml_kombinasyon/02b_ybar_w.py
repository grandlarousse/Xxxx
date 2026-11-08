"""Yama/yeniden üretim: mevcut preds_<V>.parquet dosyalarına ybar_w (winsorize eğitim ortalaması) sütununu, 02_walkforward.py ile
AYNI eğitim penceresi ve ambargo mantığıyla yeniden hesaplayıp ekler (model yeniden eğitilmez). 02 yeniden çalıştırılırsa bu sütun zaten yazılır;
bu betik o zaman aynı değerleri yeniden yazar (zararsız)."""
import sys
from common import *
from features import build, feature_sets
Xs, XV, info, s, d = build(); A, B = feature_sets(info)
cfg = {"V1": (XV[B], d, "fwd{h}", XV[B], "2017-03-01", ("2020-01-01", "2026-12-31")),
       "V2": (Xs[A], s, "sfwd{h}", XV[A], "2011-01-01", ("2020-01-01", "2026-12-31")),
       "V3": (Xs[A], s, "sfwd{h}", Xs[A], "2011-01-01", ("2013-01-01", "2016-12-31"))}
for V, (Xtr_all, ysrc_df, ycol, Xte_all, tstart, test) in cfg.items():
    P_ = pd.read_parquet(f"{OUT}/preds_{V}.parquet"); P_["date"] = pd.to_datetime(P_["date"])
    rows = []
    for h in (1, 3, 5):
        ysrc = ysrc_df[ycol.format(h=h)]; tr_idx = Xtr_all.index; te_idx = Xte_all.index
        tdays = te_idx[(te_idx >= test[0]) & (te_idx <= test[1])]
        for M in tdays.to_period("M").unique():
            td = tdays[tdays.to_period("M") == M]; p0 = tr_idx.searchsorted(td[0]); last_ok = p0 - 1 - h
            if last_ok < 100: continue
            tr = tr_idx[(tr_idx >= tstart) & (tr_idx <= tr_idx[last_ok])]
            ytr = ysrc.reindex(tr).dropna(); lo, hi = ytr.quantile([0.01, 0.99])
            rows.append(pd.DataFrame({"date": td, "h": h, "ybar_w2": float(ytr.clip(lo, hi).mean()), "ybar2": float(ytr.mean())}))
    W = pd.concat(rows)
    P_ = P_.drop(columns=[c for c in ("ybar_w",) if c in P_]).merge(W, on=["date", "h"], how="left")
    assert np.allclose(P_.ybar, P_.ybar2), "ybar uyuşmuyor — eğitim penceresi farklı"
    P_["ybar_w"] = P_.ybar_w2; P_ = P_.drop(columns=["ybar_w2", "ybar2"])
    P_.to_parquet(f"{OUT}/preds_{V}.parquet"); print(V, "ybar_w eklendi; ybar kontrolü geçti", P_.shape, (P_.ybar_w - P_.ybar).describe()[["mean", "min", "max"]].round(6).to_dict())
