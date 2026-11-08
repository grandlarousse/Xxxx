"""Akşam kontrol betiği: denetimden sağ çıkan kuralları (A1, A2, B1-B10) en son günlük veriyle değerlendirir,
açık/bekleyen pozisyonların giriş-çıkış günlerini TR saatiyle verir. Yatırım tavsiyesi değildir.

KURULUM (bir kez):
  Python 3.10+ kurun. Klasörde:  python3 -m venv .venv  ve  .venv/bin/pip install requests numpy pandas tzdata
  (Windows: py -m venv .venv  ve  .venv\\Scripts\\pip install requests numpy pandas tzdata)
KULLANIM:
  .venv/bin/python kod/sinyal.py            # ABD kapanışından SONRA (kış TR 00:00+, yaz 23:00+): son tamamlanmış mum
  .venv/bin/python kod/sinyal.py --canli    # kapanıştan ~10-15 dk ÖNCE: bugünün mumu anlık fiyatla kurulur (IBS/RSI tahmini)
  (Windows: .venv\\Scripts\\python kod\\sinyal.py)
Veri: Nasdaq API ve (10Y ihaleleri için) ABD Hazinesi fiscaldata API'si; dürüst istemci adı. İnternet gerekir.
Takvimler: data/events/*.csv (NYSE tatil + yarım gün, EIA doğalgaz, 10Y ihale). Takvim bitince betik uyarır."""
import sys, os, time, datetime as dt
from zoneinfo import ZoneInfo
import requests, numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
EV = os.path.join(ROOT, "data", "events")
UA = "etf-research-script/1.0"
NY, TR = ZoneInfo("America/New_York"), ZoneInfo("Europe/Istanbul")
S = requests.Session(); S.headers["User-Agent"] = UA
CANLI = "--canli" in sys.argv

ETFS = ["QQQ", "SPY", "SMH", "GDXJ", "GDX", "GLD", "EWY", "EWJ", "EWT", "FXI", "EWA", "EWH", "SVXY", "USO", "TMV", "KOLD"]
STOCKS = {"NVDA": "NVDL", "TSLA": "TSLL", "AMZN": "AMZU", "MSFT": "MSFU", "GOOGL": "GGLL", "AAPL": "AAPU", "META": "METU"}
ASIA = ["EWJ", "EWY", "EWT", "FXI", "EWA", "EWH"]

def num(x):
    return float(str(x).replace("$", "").replace(",", "")) if x not in (None, "", "N/A") else np.nan

def hist(sym, ac):
    frm = (dt.date.today() - dt.timedelta(days=420)).isoformat()
    for a in range(4):
        try:
            r = S.get(f"https://api.nasdaq.com/api/quote/{sym}/historical", params={"assetclass": ac, "fromdate": frm, "todate": dt.date.today().isoformat(), "limit": "9999"}, timeout=40)
            rows = r.json()["data"]["tradesTable"]["rows"]; break
        except Exception:
            time.sleep(2 ** a)
    else:
        raise RuntimeError(f"{sym}: veri alınamadı")
    df = pd.DataFrame(rows); df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    df = df.set_index("date").sort_index()
    df = pd.DataFrame({k: df[v].map(num) for k, v in (("o", "open"), ("h", "high"), ("l", "low"), ("c", "close"))})
    if CANLI:
        try:
            info = S.get(f"https://api.nasdaq.com/api/quote/{sym}/info", params={"assetclass": ac}, timeout=30).json()["data"]
            summ = S.get(f"https://api.nasdaq.com/api/quote/{sym}/summary", params={"assetclass": ac}, timeout=30).json()["data"]["summaryData"]
            last = num(info["primaryData"]["lastSalePrice"])
            hi, lo = [num(x) for x in summ["TodayHighLow"]["value"].split("/")]
            today = pd.Timestamp(dt.datetime.now(NY).date())
            if today not in df.index and np.isfinite(last):
                df.loc[today] = {"o": np.nan, "h": max(hi, last), "l": min(lo, last), "c": last}
        except Exception as e:
            print(f"  ! {sym}: canlı fiyat alınamadı ({e})")
    return df

def ibs(d): return ((d["c"] - d["l"]) / (d["h"] - d["l"]).replace(0, np.nan))
def rsi(c, n=2):
    dd = c.diff(); up = dd.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean(); dn = (-dd).clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))

def calendar():
    p = os.path.join(EV, "nyse_tatil.csv")
    if not os.path.exists(p): return set(), set(), None
    h = pd.read_csv(p); d = pd.to_datetime(h["date"]).dt.date
    hol = set(d[h["event"] == "NYSE_tatil"]); early = set(d[h["event"] == "NYSE_erken_kapanis"])
    return hol, early, max(d)
HOL, EARLY, CAL_END = calendar()

def next_bdays(d, k):
    out = []; x = d
    while len(out) < k:
        x = x + dt.timedelta(days=1)
        if x.weekday() < 5 and x not in HOL: out.append(x)
    return out

def prev_bday(d):
    x = d
    while True:
        x = x - dt.timedelta(days=1)
        if x.weekday() < 5 and x not in HOL: return x

def tr_close(d):
    """d günü ABD kapanışının TR saati; NYSE yarım günlerinde 13:00 ET."""
    hh = 13 if d in EARLY else 16
    t = dt.datetime(d.year, d.month, d.day, hh, 0, tzinfo=NY).astimezone(TR)
    return t.strftime("%d.%m %H:%M") + (" — YARIM GÜN, erken kapanış!" if d in EARLY else "")

def tr_open(d):
    return dt.datetime(d.year, d.month, d.day, 9, 30, tzinfo=NY).astimezone(TR).strftime("%d.%m %H:%M")

def positions(sig, mode, h, last, exit_sig=None, lookback=25):
    """Son sinyallerden çakışmasız kuralla (lib.trades ile aynı) açık/bekleyen pozisyonlar.
    exit_sig: (opsiyonel) t kapanışında True ise erken çık (C0'da giriş gününden sonra)."""
    sig = sig.dropna().iloc[-lookback:]
    days = [d.date() for d in sig.index]
    cal = days + next_bdays(days[-1], 8)
    ex = None if exit_sig is None else exit_sig.reindex(sig.index).fillna(False).values
    busy = -1; out = []
    for i, d in enumerate(sig.index):
        if not sig.loc[d] or i < busy: continue
        e = i if mode == "C0" else i + 1
        x = (i + h) if mode in ("C0", "O1") else (i + 1 + h)
        x_known = None
        if ex is not None:
            for j in range(e + 1 if mode != "O1" else e, min(x, len(days) - 1) + 1):
                if ex[j]: x_known = j; break
        if x_known is not None: x = x_known
        busy = max(x, i + 1)
        if cal[x] >= last:
            ne = "açılış" if mode == "O1" else "kapanış"
            st = "BEKLEYEN" if cal[e] > last else ("SON KAPANIŞTA KAPANDI" if cal[x] == last else "AÇIK")
            extra = " (en geç; erken çıkış koşulunu her akşam kontrol et)" if ex is not None and x_known is None and cal[x] > last else ""
            out.append(f"{st}: sinyal {d.date()} -> giriş {cal[e]} {ne} (TR {tr_open(cal[e]) if mode == 'O1' else tr_close(cal[e])}), çıkış {cal[x]} kapanış (TR {tr_close(cal[x])}){extra}")
    return "; ".join(out) if out else "açık/bekleyen pozisyon yok"

def line(kad, ad, durum, eylem, poz=None):
    print(f"[{kad}] {ad}\n     durum: {durum}\n     eylem: {eylem}")
    if poz:
        for p in poz: print(f"     {p}")

def upcoming_10y(last):
    """CSV + Hazine 'upcoming auctions' API'si (yaklaşık 1 hafta önceden duyurulur)."""
    dates, src = set(), {}
    p = os.path.join(EV, "hazine_ihale_10y30y.csv")
    if os.path.exists(p):
        a = pd.read_csv(p); a = a[a["event"].str.contains("10Y")]
        for x in pd.to_datetime(a["date"]).dt.date: dates.add(x); src[x] = "takvim dosyası"
    try:
        r = S.get("https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/upcoming_auctions",
                  params={"filter": f"auction_date:gte:{last.isoformat()}", "sort": "auction_date", "page[size]": "100"}, timeout=30)
        for x in r.json().get("data", []):
            if x.get("security_type") == "Note" and (x.get("security_term") or "") in ("10-Year", "9-Year 10-Month", "9-Year 11-Month"):
                d = dt.date.fromisoformat(x["auction_date"]); dates.add(d); src[d] = "Hazine API"
    except Exception:
        pass
    return sorted(dates), src

def main():
    now = dt.datetime.now(TR)
    print(f"Çalışma zamanı: {now:%d.%m.%Y %H:%M} TR  ({'CANLI: bugünün mumu anlık fiyatla (kesin değil)' if CANLI else 'son tamamlanmış günlük mum'})\n")
    D = {s: hist(s, "etf") for s in ETFS}
    ST = {s: hist(s, "stocks") for s in STOCKS}
    last = max(d.index[-1] for d in D.values()).date()
    nb = next_bdays(last, 5)
    print(f"Son mum: {last}  · sonraki işlem günleri: {', '.join(str(x) for x in nb)}")
    soon_early = [x for x in nb if x in EARLY]
    if soon_early: print(f"  ⚠ YARIM GÜN(LER): {', '.join(str(x) for x in soon_early)} — kapanış 13:00 ET (TR 21:00 kış / 20:00 yaz)")
    if CAL_END and (CAL_END - last).days < 45: print(f"  ⚠ NYSE tatil takvimi {CAL_END} tarihinde bitiyor: data/events/nyse_tatil.csv'yi güncelleyin")
    print()

    # A1 — QQQ IBS<0,10 & düşüş -> 3 gün (C1 ana)
    q = D["QQQ"]; sq = (ibs(q) < 0.10) & (q["c"] < q["c"].shift(1))
    durum = f"IBS={ibs(q).iloc[-1]:.2f}, günlük {100*(q['c'].iloc[-1]/q['c'].iloc[-2]-1):+.2f}% -> {'SİNYAL' if sq.iloc[-1] else 'sinyal yok'}"
    ey = "sinyal yok" if not sq.iloc[-1] else (
        f"C1 (ana): bu gece bir şey yapma; {nb[0]} kapanıştan ~10 dk önce (TR {tr_close(nb[0])}) QQQ al, {next_bdays(nb[0], 3)[-1]} kapanışında sat. "
        "C0 kullanıyorsan (ikisini birden YAPMA): bugünün kapanışında/after-hours limitle al, 3 gün sonra sat.")
    line("A1", "QQQ IBS<0,10 + düşüş günü -> 3 gün (araç QQQ; 2x QLD / 3x TQQQ yalnız küçük payla)", durum, ey,
         [f"pozisyon (C1 ana): {positions(sq, 'C1', 3, last)}", f"pozisyon (C0 kullanıyorsan): {positions(sq, 'C0', 3, last)}"])

    # A2 — SMH IBS<0,20 -> 1 gün (C0)
    m = D["SMH"]; sm = ibs(m) < 0.20
    durum = f"IBS={ibs(m).iloc[-1]:.2f} -> {'SİNYAL' if sm.iloc[-1] else 'sinyal yok'}"
    ey = "sinyal yok" if not sm.iloc[-1] else (
        f"C0: resmî kapanıştan sonra after-hours'ta (TR 00:00-01:00 tercih) kapanış fiyatı + 2-5 sent LİMİT emirle SMH al (tam adet); "
        f"{nb[0]} kapanışından önce sat — o gün de IBS<0,20 olacaksa satma, bir gün daha tut. Ertesi açılışta girme (kenar kaybolur).")
    line("A2", "SMH IBS<0,20 -> 1 gün (araç SMH ya da SOXX; SOXL yalnız koşullu)", durum, ey, [f"pozisyon (C0): {positions(sm, 'C0', 1, last)}"])

    # B1 — SPY
    p = D["SPY"]; sp = (ibs(p) < 0.10) & (p["c"] < p["c"].shift(1))
    line("B1", "SPY IBS<0,10 + düşüş -> 3 gün (zayıf; QQQ ile sinyallerin ~%73'ü ortak — ikisini birden alma)",
         f"IBS={ibs(p).iloc[-1]:.2f} -> {'SİNYAL' if sp.iloc[-1] else 'sinyal yok'}", "QQQ sinyali de varsa yalnız A1'i kullan" if sp.iloc[-1] else "-",
         [f"pozisyon (C1): {positions(sp, 'C1', 3, last)}"])

    # B2 — GDXJ (C0, 3 gün)
    g = D["GDXJ"]; sg = (ibs(g) < 0.10) & (g["c"] < g["c"].shift(1))
    line("B2", "GDXJ IBS<0,10 + düşüş -> 3 gün (kapanışa bağımlı; ertesi açılışta girme)", f"IBS={ibs(g).iloc[-1]:.2f} -> {'SİNYAL' if sg.iloc[-1] else 'sinyal yok'}",
         f"C0: bugün kapanışta/after-hours limitle al, {next_bdays(last, 3)[-1]} kapanışında sat" if sg.iloc[-1] else "-", [f"pozisyon (C0): {positions(sg, 'C0', 3, last)}"])

    # B4 — Asya sepeti (C0, 1 gün)
    spy_r = p["c"].pct_change()
    poz = []
    for s in ASIA:
        r_ = D[s]["c"].pct_change(); sig = (spy_r.reindex(r_.index) <= -0.015) & (r_ <= spy_r.reindex(r_.index))
        pp = positions(sig, "C0", 1, last)
        if "yok" not in pp: poz.append(f"{s}: {pp}")
    hits = [s for s in ASIA if spy_r.iloc[-1] <= -0.015 and D[s]["c"].pct_change().iloc[-1] <= spy_r.iloc[-1]]
    line("B4", "SPY ≤ -%1,5 gününde SPY'dan çok düşen Asya ETF'leri -> 1 gün (gün kümeli t 1,9: eşik altı)", f"SPY {100*spy_r.iloc[-1]:+.2f}% -> {'SİNYAL: ' + ', '.join(hits) if hits else 'sinyal yok'}",
         f"C0: bugün kapanışta eşit tutarla al, {nb[0]} kapanışında sat" if hits else "-", poz or ["pozisyon: açık/bekleyen pozisyon yok"])

    # B5 — EWY (C0, 1 gün)
    k = D["EWY"]; sk = (ibs(k) < 0.10) & (k["c"] < k["c"].shift(1))
    line("B5", "EWY IBS<0,10 + düşüş -> 1 gün (2026 oynaklık rejimine bağlı)", f"IBS={ibs(k).iloc[-1]:.2f} -> {'SİNYAL' if sk.iloc[-1] else 'sinyal yok'}",
         f"C0: bugün kapanışta al, {nb[0]} kapanışında sat" if sk.iloc[-1] else "-", [f"pozisyon (C0): {positions(sk, 'C0', 1, last)}"])

    # B8 — USO alt Bollinger -> C1 2 gün (PTP)
    u = D["USO"]["c"]; bb = u < (u.rolling(20).mean() - 2 * u.rolling(20).std())
    line("B8", "USO alt Bollinger(20,2) kırılımı -> ertesi gün kapanışta al, 2 gün tut (⚠ PTP)", f"{'SİNYAL' if bb.iloc[-1] else 'sinyal yok'}",
         f"C1: {nb[0]} kapanışında al, {next_bdays(nb[0], 2)[-1]} kapanışında sat" if bb.iloc[-1] else "-", [f"pozisyon (C1): {positions(bb, 'C1', 2, last)}"])

    # B9 — SVXY RSI(2)<10 & >SMA200 -> 2 gün (PTP)
    v = D["SVXY"]["c"]; sv = (rsi(v) < 10) & (v > v.rolling(200).mean())
    line("B9", "SVXY RSI(2)<10 ve SMA200 üstü -> 2 gün (⚠ PTP; teyit yoksa aynı sinyalle QQQ)",
         f"RSI2={rsi(v).iloc[-1]:.1f}, SMA200 üstü={bool(v.iloc[-1] > v.rolling(200).mean().iloc[-1])} -> {'SİNYAL' if sv.iloc[-1] else 'sinyal yok'}",
         f"C0: bugün kapanışta al, {next_bdays(last, 2)[-1]} kapanışında sat" if sv.iloc[-1] else "-", [f"pozisyon (C0): {positions(sv, 'C0', 2, last)}"])

    # B10 — mega-cap RSI(2) -> 2x ETF, SMA5'te çık (≤3 gün)
    poz, summ = [], []
    for stk, etf in STOCKS.items():
        c = ST[stk]["c"]; sig = (rsi(c) < 10) & (c > c.rolling(200).mean()); ex = c > c.rolling(5).mean()
        summ.append(f"{stk}:RSI2={rsi(c).iloc[-1]:.0f}{'' if c.iloc[-1] > c.rolling(200).mean().iloc[-1] else '(SMA200 altı)'}{' SİNYAL' if sig.iloc[-1] else ''}")
        pp = positions(sig, "C0", 3, last, exit_sig=ex)
        if "yok" not in pp: poz.append(f"{stk}->{etf}: {pp}")
    line("B10", "Mega-cap hisse RSI(2)<10 ve SMA200 üstü -> 2x ETF (ya da hissenin kendisi); hisse > SMA5 kapanınca, en geç 3 gün sonra sat",
         " · ".join(summ), "aynı anda en çok 2 hisse; sinyal varsa bugün kapanışta al", poz or ["pozisyon: açık/bekleyen pozisyon yok"])

    # Takvim kuralları
    print("\nTakvim kuralları:")
    month_last = next(x for x in [last] + next_bdays(last, 30) if next_bdays(x, 1)[0].month != x.month)
    if month_last == last:
        print(f"  [B3] Ay sonu GDX (ya da GLD): BUGÜN ayın son işlem günü -> kapanışta al, {next_bdays(last, 3)[-1]} kapanışında sat")
    else:
        print(f"  [B3] Ay sonu GDX (ya da GLD): sonraki giriş {month_last} kapanış (TR {tr_close(month_last)}), çıkış {next_bdays(month_last, 3)[-1]} kapanış (TR {tr_close(next_bdays(month_last, 3)[-1])}). GDX ve GLD aynı bahis: birini seç.")
    prev_ml = [x for x in [prev_bday(last), prev_bday(prev_bday(last)), prev_bday(prev_bday(prev_bday(last)))] if next_bdays(x, 1)[0].month != x.month]
    if prev_ml:
        ml = prev_ml[0]; x3 = next_bdays(ml, 3)[-1]
        if x3 >= last: print(f"       AÇIK: {ml} ay sonu girişi -> çıkış {x3} kapanış (TR {tr_close(x3)})")
    ad, src = upcoming_10y(last)
    fut = [x for x in ad if x > last]
    if fut:
        A = fut[0]; c3 = [prev_bday(A)]; c3.append(prev_bday(c3[-1])); c3.append(prev_bday(c3[-1]))
        st = "GİRİŞ GÜNÜ GEÇTİ" if c3[2] < last else ("BUGÜN GİRİŞ" if c3[2] == last else "bekleniyor")
        acik = c3[2] <= last <= c3[0]
        print(f"  [B6] 10Y Hazine ihalesi {A} ({src.get(A)}): TBT (ya da TMV) giriş {c3[2]} kapanış (A-3) [{st}], çıkış {c3[0]} kapanış (A-1, TR {tr_close(c3[0])})"
              + (" -> pozisyon AÇIK" if acik and c3[2] < last else ""))
    if not fut or (fut and (fut[-1] - last).days < 35):
        print(f"  ⚠ [B6] 10Y ihale takvimi {ad[-1] if ad else '-'} tarihinde bitiyor: TreasuryDirect 'Tentative Auction Schedule' ile data/events/hazine_ihale_10y30y.csv'yi güncelleyin.")
    p_ = os.path.join(EV, "eia_ng_storage.csv")
    if os.path.exists(p_):
        e = sorted(pd.to_datetime(pd.read_csv(p_)["date"]).dt.date)
        fut = [x for x in e if x > last and x.month in (11, 12, 1, 2, 3)][:3]
        if not fut and last.month in (10, 11, 12, 1, 2, 3):
            # takvim bittiyse kuraldan üret (Perşembe; tatilse bir önceki iş günü) — EIA takviminden teyit edin
            x = last; gen = []
            while len(gen) < 3:
                x += dt.timedelta(days=1)
                if x.weekday() == 3 and x.month in (11, 12, 1, 2, 3):
                    gen.append(x if x not in HOL else prev_bday(x))
            fut = gen
            print(f"  ⚠ [B7] EIA takvimi {e[-1]} tarihinde bitiyor; aşağıdaki tarihler kuraldan (Perşembe) üretildi — ir.eia.gov/ngs/schedule.html ile teyit edin.")
        for R in fut:
            x = prev_bday(R)
            print(f"  [B7] EIA doğalgaz raporu {R}: KOLD giriş {x} kapanış (TR {tr_close(x)}), çıkış {R} kapanış (zayıf; ⚠ PTP; tek işlemde -%16)")
        if e and (e[-1] - last).days < 45: print(f"  ⚠ [B7] EIA takvim dosyası {e[-1]} tarihinde bitiyor; güncelleyin.")
    print("\nNotlar: Midas'ta MOC/LOC yok. 'Kapanışta al' = kapanıştan ~5-10 dk önce piyasa/agresif limit emir YA DA kapanıştan sonra after-hours'ta"
          " (yalnız limit emir; kesirli emir kabul edilmeyebilir -> tam adet) kapanış fiyatına yakın limit. Aynı gece sat-al yaparken takas (T+1) ve kullanılabilir bakiye kontrolü.")
    print("A1, A2, B1 ve B10 aynı risk faktörü (ABD teknoloji): aynı anda en fazla birini tam boyutla taşı. Yatırım tavsiyesi değildir; ayrıntı: RAPOR.md, kartlar/<SYM>.md")

if __name__ == "__main__":
    main()
