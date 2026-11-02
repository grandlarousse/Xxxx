"""BT2b: Hisseye özgü gap fade. idio_gap = gap_i - gap_XU030 (β=1, look-ahead yok). |idio|>1% -> -sign(idio).
Hedef (a) ham gün-içi intra_i, (b) piyasa-nötr intra_i - intra_XU030 (XU030 vadelisiyle hedge vekili). Giriş E0 (açılış) ve h1 dönemi için E2 (ilk 30 dk VWAP vekili).
Ayrıca 'piyasa gap'i' günleri: |gap_XU030|>1% günlerinde ham gap fade vs diğer günler.
Çıktı: res/a9_idio.csv"""
import numpy as np, pandas as pd, c_common as c
ll = c.ll; TG = c.VIOP
DEC = {s: ll.decomp(s) for s in TG + ["XU030"]}
idx = DEC["XU030"].index[DEC["XU030"].index >= "2014-01-01"]
G = pd.DataFrame({s: DEC[s]["gap"] for s in TG}).reindex(idx); I = pd.DataFrame({s: DEC[s]["intra"] for s in TG}).reindex(idx)
gm = DEC["XU030"]["gap"].reindex(idx); im = DEC["XU030"]["intra"].reindex(idx)
H = {s: c.h1_panel(s) for s in TG}; days = H["AKBNK"].index; half = days[len(days) // 2]
TP = {}
for s in TG:
    raw = ll.raw(ll.T(s), "h1"); raw = raw[~raw.index.duplicated(keep="last")]
    fb = raw[(raw.index.hour == 6) & (raw.index.minute == 30)].copy(); fb.index = pd.DatetimeIndex(fb.index.tz_convert(None).normalize())
    TP[s] = ((fb["h"] + fb["l"] + fb["c"]) / 3).reindex(days)
xh = c.h1_panel("XU030"); rawx = ll.raw("XU030.IS", "h1"); rawx = rawx[~rawx.index.duplicated(keep="last")]
fbx = rawx[(rawx.index.hour == 6) & (rawx.index.minute == 30)].copy(); fbx.index = pd.DatetimeIndex(fbx.index.tz_convert(None).normalize())
tpx = ((fbx["h"] + fbx["l"] + fbx["c"]) / 3).reindex(days)
Y2 = pd.DataFrame({s: np.log(H[s]["C"] / TP[s]) for s in TG}).where(pd.DataFrame({s: H[s]["intra"].notna() for s in TG}))
y2m = np.log(xh["C"] / tpx)
rows = []
def ev(name, pos, y, per_masks):
    pp = (pos * y).where(pos != 0).mean(axis=1)
    for per, m in per_masks:
        x = pp[m].dropna(); ntr = int((pos[m] != 0).sum().sum())
        if len(x) < 30: continue
        mm, t, _ = ll.nw_t(x.reset_index(drop=True), None, 5)
        rows.append(dict(bt=name, period=per, n_days=len(x), n_trades=ntr, gross_bps=1e4 * mm, t=t, net8=1e4 * mm - 8, net15=1e4 * mm - 15))
PM = [("IS2014-20", idx < "2021-01-01"), ("OOS2021-26", idx >= "2021-01-01"), ("2024+", idx >= "2024-01-01")]
idio = G.sub(gm, axis=0)
for thr in [0.01, 0.02]:
    pos = -np.sign(idio).where(idio.abs() > thr, 0.0).fillna(0)
    ev(f"idio fade |idio|>{thr:.0%} E0 ham", pos, I, PM)
    ev(f"idio fade |idio|>{thr:.0%} E0 piyasa-nötr", pos, I.sub(im, axis=0), PM)
    posr = -np.sign(G).where(G.abs() > thr, 0.0).fillna(0)
    big = (gm.abs() > 0.01).values
    ev(f"ham fade |gap|>{thr:.0%} E0, piyasa gap'i |XU030 gap|>1% günleri", posr, I, [(p + " büyük-piyasa-gap", m & big) for p, m in PM])
    ev(f"ham fade |gap|>{thr:.0%} E0, diğer günler", posr, I, [(p + " diğer", m & ~big) for p, m in PM])
    # h1 E2
    ih = idio.reindex(days); posh = -np.sign(ih).where(ih.abs() > thr, 0.0).fillna(0)
    PH = [("IS(1.yarı)", days < half), ("OOS(2.yarı)", days >= half), ("2026-08..10", days >= "2026-08-01")]
    ev(f"idio fade |idio|>{thr:.0%} E2 ham (h1)", posh, Y2, PH)
    ev(f"idio fade |idio|>{thr:.0%} E2 piyasa-nötr (h1)", posh, Y2.sub(y2m, axis=0), PH)
R = pd.DataFrame(rows); R.to_csv(c.RES + "/a9_idio.csv", index=False)
pd.set_option("display.width", 220); print(R.round(2).to_string())
