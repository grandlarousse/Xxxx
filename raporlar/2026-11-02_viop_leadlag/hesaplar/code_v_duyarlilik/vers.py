"""v_duyarlilik: ll.py sürümlerini (v1..v4) ayrı modül olarak yükler + bağımsız (kendi yazdığım) v3/v4 temizlik uygulaması.
Kullanım: import vers; L = vers.L  -> {'v1': mod, 'v2': mod, 'v3': mod, 'v4': mod}
"""
import sys, os, importlib.util, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
CODE = SCR + "/code"; OUT = SCR + "/out"; DATA = SCR + "/data"
HERE = OUT + "/code_v_duyarlilik"; RES = HERE + "/res"; os.makedirs(RES, exist_ok=True)
sys.path.insert(0, CODE)
FILES = {"v1": "ll_v1_backup.py", "v2": "ll_v2_backup.py", "v3": "ll_v3_backup.py", "v4": "ll.py"}
L = {}
for k, f in FILES.items():
    spec = importlib.util.spec_from_file_location(f"ll_{k}", os.path.join(CODE, f))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); L[k] = m
# ortak ham veri önbelleği (aynı parquet'i 4 kez okumamak için) — raw() salt okunur kullanılıyor (decomp .copy() yapıyor)
_shared = {}
for m in L.values(): m._cache = _shared
from universe import VIOP

# ---------------- bağımsız uygulama (ll'ye dayanmadan) ----------------
REG = pd.Timestamp("2020-03-13")
def _raw(sym):
    d = pd.read_parquet(os.path.join(DATA, "daily", sym + ".parquet")).copy()
    d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")].sort_index()
    return d
def my_bad(r, ver):
    if ver == "v3":
        return (r > np.log(1.105)) | (r < np.log(0.895))
    pre = r.index < REG
    up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
    return (r > up) | (r < dn)
def my_keepmask(d, ver):
    """True = günü tut. Hacim çoğunlukla varsa (>%50) v3: v>0; v4: değil(v<=0 ve h==l)."""
    v = d["v"].fillna(0)
    if not (v.gt(0).mean() > 0.5): return pd.Series(True, index=d.index)
    if ver == "v3": return v > 0
    return ~((v <= 0) & (d["h"] == d["l"]))
_CAL = None
def my_cal():
    global _CAL
    if _CAL is None:
        d = _raw("XU100.IS"); d = d[d["v"].fillna(0) > 0] if d["v"].fillna(0).gt(0).mean() > 0.5 else d
        _CAL = d.index.unique().sort_values()
    return _CAL
def my_ret(sym, ver):
    d = _raw(sym); s = d["adj"].astype(float); s = s[s > 0].dropna()
    s = s[my_keepmask(d, ver).reindex(s.index).fillna(False)]
    cal = my_cal(); cal = cal[cal >= s.index[0]]
    s = s.reindex(s.index.union(cal)).ffill().reindex(cal)
    r = np.log(s).diff(); r[my_bad(r, ver)] = np.nan
    return r
