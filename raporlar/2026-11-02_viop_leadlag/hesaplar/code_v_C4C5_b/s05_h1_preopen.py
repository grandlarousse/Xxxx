"""s05: Saatlik veriyle açılış ÖNCESİ bilinen sinyaller (kendi hizalamam).
Bar zaman damgası = bar başlangıcı (UTC). Anlık fiyat P(hh:mm) = o anda kapanan son barın kapanışı.
HK barları 01:30,02:30,03:30(->04:00),04:30(->05:30, 05:00'te başlar),05:30,06:30,07:30(->08:10). SSE: 01:30,02:30,(03:30),04:30,05:30,06:30(->07:00).
Önce h1 son bar kapanışı ile günlük kapanış tutarlılığı aylık kontrol edilir."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
tr = bist_dec("TRALT.IS"); y = tr.intra
def h1(sym):
    h = raw(sym, "h1").copy(); h["ld"] = pd.to_datetime(h["ldate"]); h["end"] = h.index + pd.Timedelta(minutes=60); return h
def snap(sym, hhmm):
    """her yerel gün için bitişi <= hhmm UTC olan son barın kapanışı"""
    h = h1(sym); hh, mm = map(int, hhmm.split(":"))
    lim = h.index.normalize() + pd.Timedelta(hours=hh, minutes=mm)
    # 06:30 HK barı 07:30'da biter vb. Bar bitişi <= lim olanlar
    ok = h[h["end"] <= lim]
    return ok.groupby("ld")["c"].last()
for sym in ["1787.HK", "600547.SS", "2899.HK"]:
    h = h1(sym); last = h.groupby("ld")["c"].last(); dc = daily_local(sym)["c"]
    j = pd.concat([last.rename("h"), dc.rename("d")], axis=1).dropna(); dev = 1e4 * np.log(j.h / j.d).abs()
    print(sym, "h1 son kapanış vs günlük kapanış |fark| bps, aylık medyan/%90:")
    print("   ", dev.groupby(dev.index.to_period("Q")).agg(lambda x: f"{x.median():.0f}/{x.quantile(.9):.0f}").to_dict())
print()
dclose = {s: daily_local(s)["c"] for s in ["1787.HK", "600547.SS", "2899.HK"]}
res = []
for sym, times in [("600547.SS", ["03:30", "05:30", "06:00", "06:30", "07:00"]), ("1787.HK", ["04:00", "05:30", "06:30", "07:30", "08:30"]), ("2899.HK", ["04:00", "06:30", "08:30"])]:
    pc = dclose[sym].shift(1)
    for st in ["2023-11-01", "2024-09-01"]:
        for hm in times:
            p = snap(sym, hm)
            sig_loc = np.log(p / pc.reindex(p.index))
            sig = to_bist(sig_loc, "zero").reindex(y.index)
            sig = sig[sig.index >= st]
            b, t, n = nw_t(y, sig)
            r10, _, _ = bt(sig, y, 10, start=st); r15, _, _ = bt(sig, y, 15, start=st)
            a = r10["ALL"]; a15 = r15["ALL"]
            res.append(dict(sym=sym, start=st, snap=hm, r=b, t=t, n=n, net10=a.get("bps"), t10=a.get("t"), sh10=a.get("sh"), net15=a15.get("bps")))
            print(f"{sym:10s} {st} P({hm}) / C(t-1) -> TRALT intra: r={b:+.3f} t={t:+.2f} n={n} | net10 {a.get('bps', np.nan):+.1f} (t {a.get('t', np.nan):+.2f}, Sh {a.get('sh', np.nan):.2f}) net15 {a15.get('bps', np.nan):+.1f}")
    # aynı dönemde günlük kapanış sinyali (karşılaştırma)
    for st in ["2023-11-01", "2024-09-01"]:
        sig = to_bist(np.log(dclose[sym] / dclose[sym].shift(1)), "zero").reindex(y.index); sig = sig[sig.index >= st]
        b, t, n = nw_t(y, sig); r10, _, _ = bt(sig, y, 10, start=st)
        print(f"{sym:10s} {st} GÜNLÜK KAPANIŞ (karşılaştırma): r={b:+.3f} t={t:+.2f} n={n} | net10 {r10['ALL'].get('bps', np.nan):+.1f}")
pd.DataFrame(res).to_csv(sys.path[0] + "/s05_h1_preopen.csv", index=False)
