"""Denetim: C0 girişinin gerçekçiliği (Midas'ta MOC/LOC yok). Yahoo saatlik barları (2023-12..2026-11, ~730 gün)
ile IBS kapanıştan 30 dk önce (15:30 ET) hesaplanır ve 15:30 fiyatından girilir.
Ham veri: scratchpad/yahoo_raw/*.json (indirilen veri; yalnız sayısal alanlar okunur).
python3 -I kod/denetim_sektor_tematik/d2_gun_ici.py <yahoo_raw_dizini>"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_ortak import *

RAW = sys.argv[1]


def yahoo(sym, iv):
    j = json.load(open(os.path.join(RAW, f"{sym}_{iv}.json")))["chart"]["result"][0]
    ts = pd.to_datetime(j["timestamp"], unit="s", utc=True).tz_convert("America/New_York")
    q = j["indicators"]["quote"][0]
    df = pd.DataFrame({k: pd.to_numeric(pd.Series(q[k]), errors="coerce").values for k in ("open", "high", "low", "close", "volume")}, index=ts)
    return df.dropna(subset=["open", "high", "low", "close"])


def daily_from_intraday(df, cut):
    """Her gün için: cut saatinden ÖNCE başlayan barların H/L'i, cut barının açılışı (=karar/giriş fiyatı)."""
    df = df[df.index.time < pd.Timestamp("16:00").time()]
    day = df.index.tz_localize(None).normalize()
    tm = pd.Series(df.index.time, index=df.index)
    rows = {}
    for d, g in df.groupby(day):
        t = pd.Series(g.index.time, index=g.index)
        pre = g[t < cut]; at = g[t == cut]
        if len(pre) < 3 or len(at) != 1: continue
        P = float(at["open"].iloc[0])
        H = max(float(pre["high"].max()), P); L = min(float(pre["low"].min()), P)
        rows[d] = {"H_pre": H, "L_pre": L, "P": P}
    return pd.DataFrame(rows).T


out = {}
for sym, trade in (("SMH", "SMH"), ("SMH", "SOXL")):
    hr = yahoo(sym, "60m")
    dd = daily_from_intraday(hr, pd.Timestamp("15:30").time())
    dl = D(sym)  # günlük resmî veri
    dd = dd[dd.index.isin(dl.index)]
    # sağlık kontrolü: Yahoo saatlik gün H/L ile Nasdaq günlük H/L
    hh = hr[hr.index.time < pd.Timestamp("16:00").time()]
    hday = hh.groupby(hh.index.tz_localize(None).normalize()).agg(h=("high", "max"), l=("low", "min"))
    rw = raw(sym).reindex(hday.index)
    print(sym, "Yahoo vs Nasdaq günlük: H medyan fark bp", round(float(((hday.h / rw.h - 1).abs()).median() * 1e4), 2),
          " L medyan fark bp", round(float(((hday.l / rw.l - 1).abs()).median() * 1e4), 2), " gün", len(hday))
    ibs_1530 = ((dd["P"] - dd["L_pre"]) / (dd["H_pre"] - dd["L_pre"]).where(lambda x: x > 0)).clip(0, 1)
    rc = raw(sym)["c"].reindex(dd.index)
    ibs_off = my_ibs(raw(sym)).reindex(dd.index)
    tdf = D(trade); traw = raw(trade)
    th = yahoo(trade, "60m"); tP = daily_from_intraday(th, pd.Timestamp("15:30").time())["P"].reindex(dd.index)
    tc = traw["c"].reindex(dd.index)
    idx = dd.index
    # ileri getiriler (ham fiyat; 1 günlük tutuşta temettü etkisi ihmal edilebilir)
    nxt_c = tc.shift(-1); nxt_P = tP.shift(-1)
    cst = cost(trade)
    variants = {
        "A resmi IBS, resmi kapanışta giriş (backtest C0)": ((ibs_off < 0.2), tc, nxt_c),
        "B 15:30 IBS, 15:30 fiyatında giriş, ertesi resmi kapanışta çıkış": ((ibs_1530 < 0.2), tP, nxt_c),
        "C 15:30 IBS, 15:30 giriş, ertesi gün 15:30 çıkış": ((ibs_1530 < 0.2), tP, nxt_P),
        "D 15:30 IBS, resmi kapanışta giriş (yalnız sınıflama hatası)": ((ibs_1530 < 0.2), tc, nxt_c),
        "E resmi IBS ama 15:30 girişi (ayrıştırma; gerçekte uygulanamaz)": ((ibs_off < 0.2), tP, nxt_c),
    }
    res = []
    for nm, (sg, ep, xp) in variants.items():
        sg = sg.fillna(False)
        g = (xp / ep - 1)[sg].dropna()
        # çakışma: h=1 C0 benzeri; ardışık sinyaller ayrı işlem sayılır (backtest ile aynı)
        res.append({"varyant": nm, "n": len(g), "brut_bp": g.mean() * 1e4, "net_bp": g.mean() * 1e4 - cst, "t_net": tt(g.values - cst / 1e4)})
    r = pd.DataFrame(res); print(f"\nSinyal {sym} -> işlem {trade}, dönem {idx[0].date()}..{idx[-1].date()}, maliyet {cst:.1f} bp")
    print(r.round(2).to_string())
    # sınıflama uyumu
    a = (ibs_off < 0.2); b = (ibs_1530 < 0.2)
    print("  resmi sinyal günü:", int(a.sum()), " 15:30 sinyal günü:", int(b.sum()), " ikisi:", int((a & b).sum()),
          " son 30 dk getirisi (resmi sinyal günleri) ort bp:", round(float(((rc / dd['P'] - 1)[a]).mean() * 1e4), 1) if trade == sym else "")
    out[f"{sym}->{trade}"] = r.round(3).to_dict("records")
    # 5 dakikalık (son ~60 gün): 15:50 kararı
    try:
        m5 = yahoo(sym, "5m"); d5 = daily_from_intraday(m5, pd.Timestamp("15:50").time())
        d5 = d5[d5.index.isin(dl.index)]
        i5 = ((d5["P"] - d5["L_pre"]) / (d5["H_pre"] - d5["L_pre"])).clip(0, 1)
        io = my_ibs(raw(sym)).reindex(d5.index)
        print(f"  5dk (son {len(d5)} gün): 15:50 IBS<0.2 gün {int((i5<0.2).sum())}, resmi {int((io<0.2).sum())}, ortak {int(((i5<0.2)&(io<0.2)).sum())}; "
              f"15:50 fiyatı / resmi kapanış (resmi sinyal günleri) ort bp {float(((d5['P']/raw(sym)['c'].reindex(d5.index)-1)[io<0.2]).mean()*1e4):.1f}")
    except Exception as e:
        print("5dk hata", e)

json.dump(out, open(os.path.join(OUT, "d2_gun_ici.json"), "w"), ensure_ascii=False, indent=1)
