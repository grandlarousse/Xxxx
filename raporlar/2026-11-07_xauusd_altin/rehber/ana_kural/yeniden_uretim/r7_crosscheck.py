"""r7: islem simulasyonunun ikinci, vektorel bir uygulamayla capraz kontrolu + panel fwd sutunlariyla hedef kontrolu."""
import json
from rep_lib import *
D = pd.read_parquet(f"{OUT}/rep_signal_viop.parquet"); r = D.ret
thr = json.load(open(f"{OUT}/rep_esik.json"))
pv = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index).astype("datetime64[ns]")
for h in (1, 3, 5):
    print(f"fwd{h}: benim hedefim ile panel fwd{h} maks |fark| =", float((fwd_sum(r, h) - pv[f"fwd{h}"]).abs().max()))
for tn, th in (("A", thr["A_2008_2017_w250"]), ("C", thr["C_tum_<=2017_min60 (ana ajan)"])):
    sig = (D.x > th).astype(float)
    for H in (3, 5):
        pos = sig.rolling(H, min_periods=1).max()                       # son H gunde (bugun dahil) sinyal var mi
        simple = np.exp(r) - 1
        gross = (pos.shift(1) * simple).fillna(0)
        cost = pos.diff().abs().fillna(pos) * 5 / 2e4
        net = gross - cost
        T, net2, pos2 = run_trades(r, sig, H, 5)
        # islem bazinda: giris gunleri
        ent = (pos > 0) & (pos.shift(1).fillna(0) == 0); ex = (pos == 0) & (pos.shift(1).fillna(0) > 0)
        logeq = (pos.shift(1).fillna(0) * r.fillna(0)).cumsum()
        ei = np.where(ent)[0]; xi = np.where(ex)[0]
        tr = [np.exp(logeq.iloc[x] - logeq.iloc[e]) - 1 for e, x in zip(ei, xi)]
        tr = np.array(tr)
        print(f"esik {tn} H={H}: vektorel Sharpe {sharpe(net):.3f} vs dongu {sharpe(net2):.3f} | pos ayni: {bool((pos == pos2).all())} | islem {len(tr)} vs {int(T.closed.sum())} | brut ort %{tr.mean()*100:.3f} vs %{T[T.closed].gross.mean()*100:.3f} | medyan %{np.median(tr)*100:.2f} | kazanan(brut) %{(tr>0).mean()*100:.1f} | net(5bps) kazanan %{((tr-0.0005)>0).mean()*100:.1f}")
