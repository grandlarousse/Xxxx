"""A6: saatlik veriyle kesin hizalama (2023-11 -> 2026-10; TTF 2024-06+).
(1) 'Gerçek senkron': sürücünün 15:00 UTC (BIST kapanışı) anındaki fiyatı ile hesaplanan BIST-kapanış-kapanış getirisi vs hisse cc.
(2) 'Kapanış sonrası' parça: sürücü 15:00 UTC_t -> kendi kapanışı_t  vs hisse gap_{t+1} ve intra_{t+1}.
(3) ABD ilk saati (yaz: 13:30-14:30 UTC) -> hisse 14:30->kapanış (işlenebilir gün-içi öncülük).
Çıktı: res_intraday.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc import *
from kc import _corr
HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [("GUBRF", "CF"), ("GUBRF", "NTR"), ("GUBRF", "YAR.OL"), ("GUBRF", "TTF=F"), ("GUBRF", "NG=F"), ("TKFEN", "CF"), ("HEKTS", "CF"),
         ("SISE", "TTF=F"), ("SISE", "SGO.PA"), ("SISE", "NG=F"), ("SISE", "EURUSD=X"), ("SISE", "TRY=X"), ("CIMSA", "HEI.DE"), ("OYAKC", "HEI.DE"),
         ("CIMSA", "SGO.PA"), ("CIMSA", "TTF=F"), ("OYAKC", "TTF=F"), ("XU100", "ES=F"), ("SISE", "ES=F"), ("GUBRF", "ES=F"), ("CIMSA", "ES=F")]


def bist_bdays(stock):
    return DEC(stock).dropna().index


rows = []
for st, dv in PAIRS:
    try:
        snap = ll.snap_daily(dv, "15:00")
        full = ll.daily(dv, on_bist_cal=False)  # günlük kapanış (yerel tarih)
    except Exception as e:
        print("skip", st, dv, e); continue
    dd = DEC(st); idx = dd.index[dd.index >= snap.dropna().index.min()]
    sn = snap.reindex(idx).ffill(limit=1)
    r_sync = np.log(sn).diff()  # sürücünün BIST kapanışından BIST kapanışına getirisi
    # sürücünün kendi günlük kapanışı (aynı takvim günü)
    fc = full.reindex(idx)
    r_after = np.log(fc / sn)  # 15:00 UTC -> sürücü kapanışı (aynı gün)
    o = {"stock": st, "driver": dv, "start": str(idx[0].date())}
    o["c_sync_snap"], o["n"] = _corr(dd["cc"], r_sync)
    o["t_sync_snap"] = nwt_corr(dd["cc"], r_sync)
    o["pc_sync_snap"], _ = pc(dd["cc"], r_sync, [DEC("XU100")["cc"]]) if st != "XU100" else (np.nan, 0)
    rd = R(dv).reindex(idx)
    o["c_sync_daily"], _ = _corr(dd["cc"], rd)  # standart günlük (eşzamansız) lag0
    o["c_after_gap1"], _ = _corr(dd["gap"], r_after.shift(1))
    o["t_after_gap1"] = nwt_corr(dd["gap"], r_after.shift(1))
    o["c_after_intra1"], _ = _corr(dd["intra"], r_after.shift(1))
    o["t_after_intra1"] = nwt_corr(dd["intra"], r_after.shift(1))
    rows.append(o)
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in o.items()}, flush=True)

# (3) ABD ilk saat -> BIST son yarım saat + kapanış seansı
for st, dv in [("GUBRF", "CF"), ("GUBRF", "NTR"), ("HEKTS", "CF"), ("TKFEN", "CF"), ("CIMSA", "VMC"), ("XU100", "ES=F"), ("GUBRF", "ES=F"), ("SISE", "ES=F")]:
    try:
        h = ll.intraday(dv, "h1"); b = ll.intraday(ll.T(st), "h1")
    except Exception as e:
        print("skip3", st, dv, e); continue
    h = h.copy(); h["d"] = h.index.tz_convert(None).normalize()
    first = h.groupby("d").apply(lambda g: g.iloc[0])  # günün ilk ABD barı (13:30 yaz / 14:30 kış)
    first_start = h.groupby("d").apply(lambda g: g.index[0])
    summer = first_start.dt.hour == 13
    r_first = np.log(first["c"] / first["o"])
    b = b.copy(); b["d"] = b.index.tz_convert(None).normalize()
    bar1330 = b[(b.index.hour == 13) & (b.index.minute == 30)].set_index("d")["c"]
    dclose = ll.daily(ll.T(st), field="c", on_bist_cal=False)
    tgt = np.log(dclose.reindex(bar1330.index) / bar1330)  # 14:30 -> günlük kapanış
    df = pd.concat([r_first.rename("x"), tgt.rename("y"), summer.rename("summer")], axis=1).dropna()
    df = df[df.summer.astype(bool)]
    if len(df) < 60: print("az veri", st, dv, len(df)); continue
    c = df.x.corr(df.y); t = nwt_corr(df.y, df.x)
    res, pnl, pos = run_bt(df.x, df.y, 10, start="2023-01-01")
    rows.append({"stock": st, "driver": dv, "test": "US_first_hour_summer->BIST_1430_close", "c": c, "t": t, "n": len(df),
                 "bt10_mean_bps": res["ALL"].get("mean_bps"), "bt10_t": res["ALL"].get("t")})
    print(st, dv, "ABD ilk saat->BIST 14:30-kapanış (yaz)", round(c, 3), round(t, 2), len(df), "BT10:", {k: round(v, 2) for k, v in res["ALL"].items()}, flush=True)
pd.DataFrame(rows).to_csv(os.path.join(HERE, "res_intraday.csv"), index=False)
