"""DENETİM: tuprs.pine algoritmasının Python benzetimi (derleyici yok -> mantık doğrulaması).
Grafik = BIST günlük barları (VİOP takvimi, 2017-03-06'dan). Her bar için request.security(lookahead_on) eşlemesi iki olası
kuralla denenir: (a) açılış zamanı <= BIST bar açılışı olan son ABD barı (gerçek TV davranışı beklenen), (b) aynı TARİHLİ ABD barı
(en kötü durum: aynı gün barı eşlenirse sızıntı olur mu?). Sonra Pine'daki time_close<=kesim ve >lastTc süzgeci, 8 gecikme,
kayan toplamlı beta/std ve durum makinesi birebir uygulanır. Sonuç bağımsız z ile karşılaştırılır."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/rehber/tuprs/denetim/kod")
import z_bagimsiz as zb

Z, R = zb.build()
cal = Z.index[Z.index >= "2017-03-06"]
spx = zb.adj("^GSPC"); us = spx.index
ret = {"S": np.log(spx).diff()}
for m in zb.MEM: ret[m] = np.log(zb.adj(m)).diff().reindex(us)
ny = "America/New_York"
us_open = pd.DatetimeIndex([pd.Timestamp(d.year, d.month, d.day, 9, 30, tz=ny).tz_convert("UTC") for d in us])
us_close = pd.DatetimeIndex([pd.Timestamp(d.year, d.month, d.day, 16, 0, tz=ny).tz_convert("UTC") for d in us])

def run(mapping):
    W, MB, WS, MS = 250, 100, 250, 100
    pair = {m: dict(y=[], x=[], st=np.zeros(5)) for m in zb.MEM}
    hpb = []; stpb = np.zeros(3); lastTc = None; zs = []; evs = []
    pos = 0; left = 0
    for D in cal:
        bopen = pd.Timestamp(D.year, D.month, D.day, 9, 30, tz="Europe/Istanbul").tz_convert("UTC")
        cutoff = pd.Timestamp(D.year, D.month, D.day, 18, 10, tz="Europe/Istanbul").tz_convert("UTC")
        if mapping == "a": j0 = np.searchsorted(us_open.values, bopen.to_datetime64(), side="right") - 1
        else: j0 = np.searchsorted(us.values, D.to_datetime64(), side="right") - 1   # aynı tarihli ABD barı
        lags = [j0 - k for k in range(8) if j0 - k >= 1]
        pbsum = 0.0; pbany = False
        if lastTc is None:
            for j in reversed(lags):
                if us_close[j] <= cutoff: lastTc = us_close[j]
        else:
            for j in reversed(lags):   # en eski -> en yeni
                tk = us_close[j]
                if tk > lastTc and tk <= cutoff:
                    rs = ret["S"].iloc[j]; es = []
                    for m in zb.MEM:
                        st = pair[m]["st"]; b = np.nan
                        if st[4] >= MB:
                            mx, my = st[0] / st[4], st[1] / st[4]; vx = st[3] / st[4] - mx * mx
                            if vx > 0: b = (st[2] / st[4] - mx * my) / vx
                        rm_ = ret[m].iloc[j]
                        es.append(rm_ - b * rs if np.isfinite(rm_) and np.isfinite(b) and np.isfinite(rs) else np.nan)
                        # push
                        P = pair[m]; P["y"].append(rm_); P["x"].append(rs)
                        if np.isfinite(rm_) and np.isfinite(rs): st += [rs, rm_, rs * rm_, rs * rs, 1]
                        if len(P["y"]) > W:
                            yo = P["y"].pop(0); xo = P["x"].pop(0)
                            if np.isfinite(yo) and np.isfinite(xo): st -= [xo, yo, xo * yo, xo * xo, 1]
                    es = np.array(es); c = np.isfinite(es).sum()
                    if c >= 3: pbsum += np.nanmean(es); pbany = True
                    lastTc = tk
        Pb = pbsum if pbany else np.nan
        n = stpb[2]; sd = np.nan
        if n >= MS and n > 1:
            mm = stpb[0] / n; vv = (stpb[1] - n * mm * mm) / (n - 1); sd = np.sqrt(vv) if vv > 0 else np.nan
        z = Pb / sd if np.isfinite(Pb) and np.isfinite(sd) else np.nan
        hpb.append(Pb)
        if np.isfinite(Pb): stpb += [Pb, Pb * Pb, 1]
        if len(hpb) > WS:
            o = hpb.pop(0)
            if np.isfinite(o): stpb -= [o, o * o, 1]
        zs.append(z)
        sig = np.isfinite(z) and abs(z) > 1; ev = ""
        if pos != 0:
            left -= 1
            if left == 0:
                if sig and np.sign(z) == pos: left = 2; ev = "UZAT"
                elif sig: pos = int(np.sign(z)); left = 2; ev = "CEVIR"
                else: pos = 0; ev = "KAPAT"
        elif sig: pos = int(np.sign(z)); left = 2; ev = "AC"
        evs.append((ev, pos))
    return pd.Series(zs, index=cal), evs

for mp in ("a", "b"):
    zp, evs = run(mp)
    ref = Z["z"].reindex(zp.index)
    for start in ("2019-01-01", "2024-01-01"):
        m = (zp.index >= start) & zp.notna() & ref.notna()
        both_na = ((zp.isna() != ref.isna()) & (zp.index >= start)).sum()
        s1 = np.sign(zp[m]) * (zp[m].abs() > 1); s2 = np.sign(ref[m]) * (ref[m].abs() > 1)
        print(f"eşleme {mp} | {start}+ : ortak {int(m.sum())}, maks|Δz| {np.abs(zp[m] - ref[m]).max():.2e}, yalnız birinde boş {int(both_na)}, sinyal eşleşme {(s1 == s2).mean() * 100:.2f}%")
    print("   son 5 z:", zp.tail(5).round(3).to_dict(), "| son olaylar:", [(str(d.date()), e) for d, e in zip(zp.index[-12:], evs[-12:]) if e[0]])
