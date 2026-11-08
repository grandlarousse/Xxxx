"""Adım 2: genişleyen pencere, ayda bir yeniden eğitim. Kullanım: python3 02_walkforward.py V1|V2|V3
 V1: VİOP paneli, set B (tüm öznitelikler), hedef VİOP fwd_h, eğitim 2017-03 başlangıç, test 2020-01..2026-11.
 V2: spot paneli, set A (2010+ mevcut öznitelikler), hedef spot sfwd_h (15:00→15:00), eğitim 2011-01 başlangıç; tahmin VİOP günlerinde, test 2020-01..
 V3: erken dönem tekrarı — spot paneli, set A, eğitim 2011-01..2012-12 ilk pencere, test 2013-01..2016-12 (hedef sfwd_h).
Ambargo: test ayının ilk günü T0 için eğitim etiketleri yalnız t + h <= T0-1 olan satırlar (etiket örtüşmesi sızıntısı yok).
Standardizasyon, winsorize ve ceza seçimi yalnız eğitim penceresinde.
ybar = ham eğitim ortalaması (CT tarihsel ortalama kıyası); ybar_w = winsorize eğitim ortalaması (modelin kendi taban tahmini; zamanlama sinyali yhat - ybar_w)."""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
from common import *
from features import build, feature_sets
from models import fit_predict, MODELS

V = sys.argv[1]
Xs, XV, info, s, d = build()
A, B = feature_sets(info)
cfg = {
    "V1": dict(Xtr_all=XV[B], ytr_src=d, ycol="fwd{h}", Xte_all=XV[B], train_start="2017-03-01", test=("2020-01-01", "2026-12-31")),
    "V2": dict(Xtr_all=Xs[A], ytr_src=s, ycol="sfwd{h}", Xte_all=XV[A], train_start="2011-01-01", test=("2020-01-01", "2026-12-31")),
    "V3": dict(Xtr_all=Xs[A], ytr_src=s, ycol="sfwd{h}", Xte_all=Xs[A], train_start="2011-01-01", test=("2013-01-01", "2016-12-31")),
}[V]
rows, diags = [], []
t0 = time.time()
for h in (1, 3, 5):
    Xtr_all = cfg["Xtr_all"]; ysrc = cfg["ytr_src"][cfg["ycol"].format(h=h)]
    tr_idx = Xtr_all.index
    Xte_all = cfg["Xte_all"]; te_idx = Xte_all.index
    test_days = te_idx[(te_idx >= cfg["test"][0]) & (te_idx <= cfg["test"][1])]
    for M in test_days.to_period("M").unique():
        td = test_days[test_days.to_period("M") == M]
        T0 = td[0]
        p0 = tr_idx.searchsorted(T0)          # eğitim endeksinde T0'ın konumu (T0 dahil değil)
        last_ok = p0 - 1 - h                  # etiket t+h <= T0-1
        if last_ok < 100: continue
        tr = tr_idx[(tr_idx >= cfg["train_start"]) & (tr_idx <= tr_idx[last_ok])]
        ytr = ysrc.reindex(tr); m = ytr.notna()
        Xtr = Xtr_all.loc[tr][m.values]; ytr = ytr[m]
        out, dg, ybar, ybar_w = fit_predict(Xtr, ytr, Xte_all.loc[td], h)
        for k, v in out.items():
            rows.append(pd.DataFrame({"date": td, "h": h, "model": k, "yhat": v, "ybar": ybar, "ybar_w": ybar_w}))
        diags.append(dict(h=h, month=str(M), train_end=str(tr[-1].date()), test_start=str(T0.date()), **dg))
    print(V, "h", h, "bitti", round(time.time() - t0), "s", flush=True)
P_ = pd.concat(rows, ignore_index=True)
P_.to_parquet(f"{OUT}/preds_{V}.parquet")
pd.DataFrame(diags).to_csv(f"{OUT}/diag_{V}.csv", index=False)
print("kaydedildi", P_.shape)
