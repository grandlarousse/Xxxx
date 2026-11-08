"""comp_t'nin hangi gelecekteki spot alt-penceresini öngördüğü (VİOP günleri takvimi): t+j günü 15(t+j-1)->07(t+j) ve 07(t+j)->15(t+j)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin_rep")
from r0_base import *
T = viop_target(); days = T.index; F = pd.read_parquet(f"{OUT}/r1_features_viop.parquet")
G15 = pd.Series(gold_at(days + pd.Timedelta(hours=15)), index=days); G07 = pd.Series(gold_at(days + pd.Timedelta(hours=7)), index=days)
night = np.log(G07 / G15.shift(1)); dayw = np.log(G15 / G07)
for k in ("comp",):
    x = F[k]
    for j in range(0, 4):
        a = ic_t(x, night.shift(-j), 5); b = ic_t(x, dayw.shift(-j), 5)
        ao = ic_t(x[x.index > IS_END], night.shift(-j)[x.index > IS_END], 5); bo = ic_t(x[x.index > IS_END], dayw.shift(-j)[x.index > IS_END], 5)
        print(f"{k} j={j}: gece 15(t+{j}-1)->07(t+{j}) IC {a['ic']:.3f} t {a['t']:.2f} (OOS t {ao['t']:.2f}) | gündüz 07->15(t+{j}) IC {b['ic']:.3f} t {b['t']:.2f} (OOS t {bo['t']:.2f})")
