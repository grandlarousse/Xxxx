"""Uzlaşma zamanını ham veriden yıl yıl doğrula: std(v_ret - spot_ret_H) hangi H'de minimum? (H = HH:00 UTC görüntüsü)"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
va = pd.read_parquet(f"{OUT}/viop_rep.parquet")
Hs = range(12, 19)
snaps = pd.DataFrame({H: snap("XAUUSD", H) for H in Hs})
# yarım saatlik çözünürlük: barın açılışı = önceki barın kapanışı; ayrıca dakika verisi örnek günler için
sn = snaps.reindex(va.index)
te = {}
for H in Hs:
    lp = np.log(sn[H])
    # aynı kontrat içi: settle_t / settle_{t-1} vs spot_H,t / spot_H,t-1 (VİOP takvimi)
    d = va.ret - (lp - lp.shift(1))
    d = d[~va.roll]
    te[H] = d.groupby(d.index.year).std() * 1e4
T = pd.DataFrame(te).round(1)
print("std(v_ret - spot ret @HH:00) bps, yıl × HH"); print(T.to_string())
# dakika verisi örnek günler
m = pd.read_parquet(f"{P}/duka_min_XAUUSD.parquet")
print(m.index[:2], m.shape, sorted(set(pd.to_datetime(m.index).year)))
