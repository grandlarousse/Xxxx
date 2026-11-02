"""cin - Adım 4: Roll düzeltmesinin kalitesi. Örtüşen dönemde sürekli (ham) seri vs roll-düzeltilmiş seri;
sezgisel roll filtresi; Yahoo/Sina çapraz kontrol (SSE Composite). Çıktı: code_cin/roll_check.csv"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_cin")
import cin_lib as C, numpy as np, pandas as pd
from c02_fetch_sina import COMS
rows = []
for code, (desc, ex, _) in COMS.items():
    c0 = C._load_json(code + "0"); r0 = np.log(c0["c"].where(c0["c"] > 0)).diff()
    ra, info = C.roll_adjusted(code)
    if ra is None: rows.append({"code": code, "desc": desc}); continue
    df = pd.concat([r0.rename("r0"), ra.rename("ra")], axis=1).dropna()
    d = (df.r0 - df.ra).abs()
    rf = C.fut_ret(code)
    # filtre performansı: örtüşmede filtre roll günlerini yakalıyor mu?
    f0 = C.fut_ret(code, hybrid=False).reindex(df.index)
    big = d > 0.005
    rows.append({"code": code, "desc": desc, "exch": ex, "cont_first": str(c0.index[0].date()), **info,
                 "n_overlap": len(df), "corr_r0_ra": df.r0.corr(df.ra), "n_rolldays(|diff|>0.5%)": int(big.sum()),
                 "mean_abs_rolljump_pct": 100 * d[big].mean() if big.any() else 0, "filter_caught": int((big & f0.isna()).sum()),
                 "filter_false_pos": int((~big & f0.isna()).sum()), "sd_daily_pct": 100 * df.ra.std(), "hybrid_n": int(rf.notna().sum())})
out = pd.DataFrame(rows); out.to_csv("/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_cin/roll_check.csv", index=False)
print(out[["code", "start", "n_switch", "corr_r0_ra", "n_rolldays(|diff|>0.5%)", "mean_abs_rolljump_pct", "filter_caught", "filter_false_pos", "sd_daily_pct"]].round(3).to_string())
# çapraz kontrol
a = C.ret_local("SIDX:sh000001"); b = C.ret_local("000001.SS")
x = pd.concat([a, b], axis=1, join="inner").dropna(); print("SSE Sina vs Yahoo corr", round(x.corr().iloc[0, 1], 4), len(x))
