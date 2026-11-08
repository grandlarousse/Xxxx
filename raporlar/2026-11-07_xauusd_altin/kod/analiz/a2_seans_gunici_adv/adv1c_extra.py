"""İddia 1 ek: 06:00 çıkış, Pazartesi hariç, akşam bülteni tarih eşleşmesi kontrolü."""
from adv_common import *
v = load_viop(); px = A2.price_series()
vd = v.index[v.index >= "2020-09-21"]
prev_cal = pd.DatetimeIndex([pd.Timestamp(d.date()) for d in v.index.to_series().shift(1).reindex(vd)]).tz_localize("UTC")
b0 = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") for d in vd])
e20 = snap(px, prev_cal + pd.Timedelta(hours=20))
def sh(x): x = pd.Series(x).dropna(); return round(x.mean() / x.std() * np.sqrt(252), 2)
for H in (6, 7):
    r = pd.Series(np.log(snap(px, b0 + pd.Timedelta(hours=H)) / e20), index=vd).dropna()
    for nm, m in [("hepsi", np.ones(len(r), bool)), ("Pzt hariç", r.index.dayofweek != 0), ("yalnız Pzt", r.index.dayofweek == 0)]:
        x = r[m]; oo = x.index >= "2022-01-01"
        print(f"çıkış {H:02d}:00 {nm:10s}: brüt {x.mean()*1e4:.2f} bps (t {mean_t(x)[1]:.2f}), Sharpe 0/5/10 bps: {sh(x)} / {sh(x-5e-4)} / {sh(x-1e-3)} | OOS 5bps {sh(x[oo]-5e-4)} n {len(x)}")
