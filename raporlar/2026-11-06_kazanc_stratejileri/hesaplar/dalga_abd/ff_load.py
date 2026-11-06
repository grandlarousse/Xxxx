"""Ken French veri kutuphanesi CSV ayristirici (49 sektor aylik/gunluk + FF faktorleri).
Ham veri: /tmp/.../scratchpad/data/dalga_abd/raw/ (repo disinda).
"""
import io, os
import numpy as np
import pandas as pd

RAW = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_abd/raw"
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_abd/parsed"
os.makedirs(CACHE, exist_ok=True)


def _sections(path):
    """Dosyayi bolumlere ayir: {baslik: DataFrame}"""
    with open(path, "r", encoding="latin-1") as f:
        lines = f.read().splitlines()
    out = {}
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        # baslik satirindan sonra ',' ile baslayan kolon satiri gelir
        hdr = None
        if i + 1 < n and lines[i + 1].startswith(",") and ln.strip() and not ln.startswith(","):
            title = ln.strip(); hdr = i + 1
        elif ln.startswith(",") and (i == 0 or not lines[i - 1].strip() or not lines[i - 1].startswith(",")) and i + 1 < n and lines[i + 1].split(",")[0].strip().isdigit():
            title = "main%d" % i; hdr = i
        if hdr is not None:
            cols = [c.strip() for c in lines[hdr].split(",")[1:]]
            j = hdr + 1
            rows = []
            while j < n and lines[j].strip() and lines[j].split(",")[0].strip().isdigit():
                rows.append(lines[j])
                j += 1
            if rows:
                df = pd.read_csv(io.StringIO("\n".join(rows)), header=None)
                df.columns = ["date"] + cols
                df = df.set_index("date")
                df = df.replace([-99.99, -999.0, -999], np.nan)
                out[title] = df
            i = j
        else:
            i += 1
    return out


def _to_month_index(idx):
    return pd.PeriodIndex([pd.Period(str(x)[:4] + "-" + str(x)[4:6], "M") for x in idx])


def load_monthly49():
    p = os.path.join(CACHE, "m49.pkl")
    if os.path.exists(p):
        return pd.read_pickle(p)
    s = _sections(os.path.join(RAW, "49_Industry_Portfolios.csv"))
    res = {}
    for key, name in [("Average Value Weighted Returns -- Monthly", "vw"),
                      ("Average Equal Weighted Returns -- Monthly", "ew"),
                      ("Number of Firms in Portfolios", "nfirms"),
                      ("Average Firm Size", "size")]:
        df = s[key].copy()
        df.index = _to_month_index(df.index)
        res[name] = df
    for key, name in [("Sum of BE / Sum of ME", "bm_y")]:
        if key in s:
            res[name] = s[key]
    pd.to_pickle(res, p)
    return res


def load_daily49():
    p = os.path.join(CACHE, "d49.pkl")
    if os.path.exists(p):
        return pd.read_pickle(p)
    s = _sections(os.path.join(RAW, "49_Industry_Portfolios_Daily.csv"))
    res = {}
    for key, name in [("Average Value Weighted Returns -- Daily", "vw"),
                      ("Average Equal Weighted Returns -- Daily", "ew")]:
        df = s[key].copy()
        df.index = pd.to_datetime(df.index.astype(str), format="%Y%m%d")
        res[name] = df
    pd.to_pickle(res, p)
    return res


def load_ff_monthly():
    p = os.path.join(CACHE, "ffm.pkl")
    if os.path.exists(p):
        return pd.read_pickle(p)
    s = _sections(os.path.join(RAW, "F-F_Research_Data_Factors.csv"))
    k = [k for k in s if "Annual" not in k][0] if len(s) > 1 else list(s)[0]
    # ilk bolum aylik
    df = list(s.values())[0].copy()
    df = df[df.index > 100000]
    df.index = _to_month_index(df.index)
    pd.to_pickle(df, p)
    return df


def load_ff_daily():
    p = os.path.join(CACHE, "ffd.pkl")
    if os.path.exists(p):
        return pd.read_pickle(p)
    s = _sections(os.path.join(RAW, "F-F_Research_Data_Factors_daily.csv"))
    df = list(s.values())[0].copy()
    df.index = pd.to_datetime(df.index.astype(str), format="%Y%m%d")
    pd.to_pickle(df, p)
    return df


if __name__ == "__main__":
    m = load_monthly49()
    for k, v in m.items():
        print(k, v.shape, v.index[0], v.index[-1])
    d = load_daily49()
    for k, v in d.items():
        print(k, v.shape, v.index[0], v.index[-1])
    f = load_ff_monthly(); print(f.tail(3)); print(f.shape)
    fd = load_ff_daily(); print(fd.tail(3)); print(fd.shape)
    print(list(m["vw"].columns))
