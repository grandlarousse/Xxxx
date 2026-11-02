"""Saatlik (h1) analiz, ~2024-06'dan beri (BZ=F h1 başlangıcı).
Pencereler (UTC): BIST kapanış 15:00(t) -> ABD kapanış 21:00(t) -> BIST açılış 07:00(t+1) -> BIST kapanış 15:00(t+1).
Sorular: (a) BIST kapanışı sonrası Brent/HO/RB/ABD rafineri hareketi ertesi gün gap'te mi, gün-içinde mi fiyatlanıyor?
(b) Seans içi saatlik öncülük: sürücü saat h-1 -> hisse saat h."""
import pandas as pd, numpy as np, statsmodels.api as sm, elib
from elib import ll, DEC
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)
def snap(sym, hhmm): return ll.snap_daily(sym, hhmm)
def win(sym):
    a = snap(sym, "15:00"); b = snap(sym, "21:00"); c = snap(sym, "07:00")
    df = pd.DataFrame({"c15": a, "c21": b, "o07": c})
    # post-close: 15:00(t) -> 07:00(t+1, bir sonraki BIST günü)  ; hizalama: BIST günü t+1 indeksine yaz
    return df
cal = ll.bist_cal(); cal = cal[cal >= "2024-06-15"]
def drv_moves(sym):
    w = win(sym).reindex(cal)
    # BIST günü t için: önceki BIST günü 15:00 -> t 07:00 (gece), t 07:00 -> t 15:00 (seans), önceki 15:00 -> önceki gün 21:00 (ABD akşamı)
    prev15 = w.c15.shift(1); prev21 = w.c21.shift(1)
    return pd.DataFrame({"night": np.log(w.o07 / prev15), "eve": np.log(prev21 / prev15), "asia": np.log(w.o07 / prev21), "sess": np.log(w.c15 / w.o07)})
STK = ["TUPRS", "PETKM", "SASA", "AKSEN", "ENJSA", "ODAS"]
DRV = ["BZ=F", "HO=F", "RB=F", "CL=F", "NG=F", "TTF=F", "VLO", "GC=F", "ES=F"]
mv = {d: drv_moves(d) for d in DRV}
xud = DEC("XU100")
rows = []
for s in STK:
    dd = DEC(s).reindex(cal)
    for d in DRV:
        m = mv[d]
        for tgt_lab, tgt in [("gap", dd.gap), ("intra", dd.intra), ("gap_h", dd.gap - xud.gap.reindex(cal)), ("intra_h", dd.intra - xud.intra.reindex(cal))]:
            for w_ in ["night", "eve", "asia", "sess"]:
                if w_ == "sess" and tgt_lab.startswith("gap"): continue
                x = pd.concat([tgt.rename("y"), m[w_].rename("x")], axis=1).dropna()
                if len(x) < 100: continue
                z = lambda v: (v - v.mean()) / v.std()
                b, t, n = ll.nw_t(z(x.y), z(x.x))
                rows.append({"stock": s, "drv": d, "target": tgt_lab, "window": w_, "corr": b, "t": t, "n": n})
H = pd.DataFrame(rows); H.to_csv(elib.RES + "/hourly_windows.csv", index=False)
P("== Saatlik pencere testleri: corr(hedef, sürücü penceresi). night=BIST kapanış(t-1)->BIST açılış(t); sess=eşzamanlı seans")
piv = H[H.target.isin(["gap", "intra", "intra_h"])].pivot_table(index=["stock", "drv"], columns=["target", "window"], values="t").round(1)
piv.to_csv(elib.RES + "/hourly_windows_t_pivot.csv")
P(piv[[("gap", "night"), ("gap", "eve"), ("gap", "asia"), ("intra", "night"), ("intra_h", "night"), ("intra", "sess"), ("intra_h", "sess")]].loc[["TUPRS", "PETKM", "AKSEN", "ODAS"]].to_string())
# corr büyüklükleri TUPRS
P(H[(H.stock == "TUPRS") & (H.drv.isin(["BZ=F", "HO=F", "VLO"]))].pivot_table(index="drv", columns=["target", "window"], values="corr").round(2).to_string())

# (b) seans içi saatlik öncülük
def hourly_ret(sym):
    d = ll.intraday(sym)["c"]; d = d[~d.index.duplicated()]
    return np.log(d).diff()
def bist_hours(sym):
    d = ll.intraday(sym); c = d["c"][~d.index.duplicated()]
    idx = c.index; keep = (idx.minute == 30) & (idx.hour >= 7) & (idx.hour <= 14)  # 07:30..14:30 barları (06:30 açılış barını dışla)
    r = np.log(c).diff()[keep]
    r.index = r.index + pd.Timedelta(minutes=30)  # barın bitişi :30 -> saat başı hizalama için bitişi kullan: 08:30 bar biter 09:30
    return r
P("== Seans içi saatlik lead: corr(hisse saat-bar_h, sürücü bar_{h-1}) ve senkron; hisse barı 07:30-14:30 başlangıçlı")
rows = []
for s in ["TUPRS", "PETKM", "AKSEN", "ODAS"]:
    hs = ll.intraday(s)["c"]; hs = hs[~hs.index.duplicated()]
    rs = np.log(hs).diff(); rs = rs[(rs.index.minute == 30) & (rs.index.hour >= 7) & (rs.index.hour <= 13)]
    for d in ["BZ=F", "HO=F", "ES=F", "VLO"]:
        hd = ll.intraday(d)["c"]; hd = hd[~hd.index.duplicated()]
        # sürücü fiyatı hisse bar sınırlarında: bar [t, t+1h) için sürücüyü t ve t+1h anlarında (asof)
        def at(ts):
            pos = hd.index.searchsorted(ts, side="right") - 1
            return pd.Series(np.where(pos >= 0, hd.values[np.clip(pos, 0, None)], np.nan), index=ts)
        st = rs.index; p0 = at(st - pd.Timedelta(minutes=1)); p1 = at(st + pd.Timedelta(minutes=59)); pm1 = at(st - pd.Timedelta(minutes=61))
        rsync = np.log(p1.values / p0.values); rlag = np.log(p0.values / pm1.values)
        x = pd.DataFrame({"y": rs.values, "sync": rsync, "lag": rlag}, index=st).replace([np.inf, -np.inf], np.nan).dropna()
        x = x[(x.sync != 0) | (x.lag != 0)]
        for k in ["sync", "lag"]:
            z = lambda v: (v - v.mean()) / v.std(); b, t, n = ll.nw_t(z(x.y), z(x[k]))
            rows.append({"stock": s, "drv": d, "rel": k, "corr": b, "t": t, "n": n})
Hh = pd.DataFrame(rows); Hh.to_csv(elib.RES + "/hourly_intrasession_lead.csv", index=False)
P(Hh.round(3).to_string(index=False))
open(elib.RES + "/04_hourly.txt", "w").write("\n".join(out))
