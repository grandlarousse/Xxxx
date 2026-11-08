"""Akşam kontrol betiği: denetimden sağ çıkan kuralları en son günlük veriyle değerlendirir.
Kullanım:
  python3 -I kod/sinyal.py            # son TAMAMLANMIŞ günlük mum (ABD kapanışından sonra; TR kış 00:00+, yaz 23:00+)
  python3 -I kod/sinyal.py --canli    # seans içinde (kapanıştan ~10-15 dk önce): bugünün mumunu anlık fiyatla kurar
Veri: Nasdaq API (dürüst istemci adı). İnternet gerekir. Yatırım tavsiyesi değildir.
Kademe A = denetimden geçmiş kural; B = zayıf kanıt (küçük boyut ya da kağıt üstünde izle)."""
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

def holidays():
    p = os.path.join(EV, "nyse_tatil.csv")
    if not os.path.exists(p): return set()
    h = pd.read_csv(p); h = h[h["event"] == "NYSE_tatil"]
    return set(pd.to_datetime(h["date"]).dt.date)
HOL = holidays()

def next_bdays(d, k):
    out = []; x = d
    while len(out) < k:
        x = x + dt.timedelta(days=1)
        if x.weekday() < 5 and x not in HOL: out.append(x)
    return out

def tr_close(d):
    """d günü ABD kapanışının TR saati (yarım günler hariç 16:00 ET)."""
    t = dt.datetime(d.year, d.month, d.day, 16, 0, tzinfo=NY).astimezone(TR)
    return t.strftime("%d.%m %H:%M")

def tr_open(d):
    t = dt.datetime(d.year, d.month, d.day, 9, 30, tzinfo=NY).astimezone(TR)
    return t.strftime("%d.%m %H:%M")

def positions(sig, mode, h, last, lookback=25):
    """Son sinyallerden, çakışmasız kuralla açık/bekleyen pozisyonları çıkarır. Dönüş: metin."""
    sig = sig.dropna().iloc[-lookback:]
    cal = [d.date() for d in sig.index] + next_bdays(sig.index[-1].date(), 8)
    busy = -1; out = []
    for i, d in enumerate(sig.index):
        if not sig.loc[d] or i < busy: continue
        e = i if mode == "C0" else i + 1
        x = (i + h) if mode in ("C0", "O1") else (i + 1 + h)
        busy = max(x, i + 1)
        if cal[x] >= last:
            ne = "açılış" if mode == "O1" else "kapanış"
            st = "BEKLEYEN" if cal[e] > last else ("SON KAPANIŞTA KAPANDI" if cal[x] == last else "AÇIK")
            out.append(f"{st}: sinyal {d.date()} -> giriş {cal[e]} {ne} (TR {tr_open(cal[e]) if mode == 'O1' else tr_close(cal[e])}), çıkış {cal[x]} kapanış (TR {tr_close(cal[x])})")
    return "; ".join(out) if out else "açık/bekleyen pozisyon yok"

def line(kad, ad, durum, eylem):
    print(f"[{kad}] {ad}\n     durum: {durum}\n     eylem: {eylem}")

def main():
    now = dt.datetime.now(TR)
    print(f"Çalışma zamanı: {now:%d.%m.%Y %H:%M} TR  ({'CANLI: bugünün mumu anlık fiyatla' if CANLI else 'son tamamlanmış günlük mum'})\n")
    D = {s: hist(s, "etf") for s in ETFS}
    ST = {s: hist(s, "stocks") for s in STOCKS}
    last = max(d.index[-1] for d in D.values()).date()
    nb = next_bdays(last, 4)
    print(f"Son mum: {last}  · sonraki işlem günleri: {', '.join(str(x) for x in nb)}\n")

    def recent_signals(sig, n=6):
        s = sig.dropna(); return ", ".join(str(d.date()) for d in s.index[-n:] if s.loc[d]) or "-"

    # A1 — QQQ IBS<0,10 & düşüş -> 3 gün (C1 ana; C0 da geçerli)
    q = D["QQQ"]; sq = (ibs(q) < 0.10) & (q["c"] < q["c"].shift(1))
    rec = recent_signals(sq)
    durum = f"bugün IBS={ibs(q).iloc[-1]:.2f}, günlük {100*(q['c'].iloc[-1]/q['c'].iloc[-2]-1):+.2f}% -> {'SİNYAL' if sq.iloc[-1] else 'sinyal yok'}; son 6 gündeki sinyaller: {rec or '-'}"
    if sq.iloc[-1]:
        e = nb[0]; x = next_bdays(e, 3)[-1]
        ey = f"C1: {e} kapanıştan ~10 dk önce (TR {tr_close(e)}) QQQ al, {x} kapanışında (TR {tr_close(x)}) sat. C0 tercih edilirse bugün kapanışta/after-hours limit."
    else:
        ey = "yeni giriş yok"
    ey += f"\n     pozisyon (C1 ana): {positions(sq, 'C1', 3, last)}\n     pozisyon (C0 alternatif): {positions(sq, 'C0', 3, last)}"
    line("A", "QQQ IBS<0,10 + düşüş günü -> 3 gün (araç: QQQ; 2x QLD / 3x TQQQ küçük payla)", durum, ey)

    # A2 — SMH IBS<0,20 -> 1 gün (C0: kapanış/after-hours)
    m = D["SMH"]; sm = ibs(m) < 0.20
    durum = f"bugün IBS={ibs(m).iloc[-1]:.2f} -> {'SİNYAL' if sm.iloc[-1] else 'sinyal yok'}"
    ey = (f"C0: bugün kapanışta ya da kapanıştan sonra after-hours'ta kapanış fiyatına yakın LİMİT emirle SMH al; {nb[0]} kapanışında (TR {tr_close(nb[0])}) sat. "
          "Ertesi açılışta girmek kenarın çoğunu kaybettirir (O1 ~17 bp, C1 ~0).") if sm.iloc[-1] else "yeni giriş yok"
    ey += f"\n     pozisyon (C0): {positions(sm, 'C0', 1, last)}"
    line("A", "SMH IBS<0,20 -> 1 gün (araç: SMH/SOXX; SOXL yalnız koşullu)", durum, ey)

    # B — SPY IBS
    p = D["SPY"]; sp = (ibs(p) < 0.10) & (p["c"] < p["c"].shift(1))
    line("B", "SPY IBS<0,10 + düşüş -> 3 gün (zayıf; QQQ ile sinyallerin ~%73'ü ortak — ikisini birden alma)",
         f"IBS={ibs(p).iloc[-1]:.2f} -> {'SİNYAL' if sp.iloc[-1] else 'sinyal yok'}", ("QQQ sinyali de varsa yalnız QQQ'yu kullan" if sp.iloc[-1] else "-") + f" · pozisyon (C1): {positions(sp, 'C1', 3, last)}")

    # B — GDXJ IBS<0,10 & düşüş -> 3 gün (C0)
    g = D["GDXJ"]; sg = (ibs(g) < 0.10) & (g["c"] < g["c"].shift(1))
    line("B", "GDXJ IBS<0,10 + düşüş -> 3 gün (kapanışa bağımlı)", f"IBS={ibs(g).iloc[-1]:.2f} -> {'SİNYAL' if sg.iloc[-1] else 'sinyal yok'}",
         (f"C0: bugün kapanışta al, {next_bdays(last, 3)[-1]} kapanışında sat" if sg.iloc[-1] else "-") + f" · pozisyon (C0): {positions(sg, 'C0', 3, last)}")

    # B — EWY IBS -> 1 gün
    k = D["EWY"]; sk = (ibs(k) < 0.10) & (k["c"] < k["c"].shift(1))
    line("B", "EWY IBS<0,10 + düşüş -> 1 gün (2026 oynaklık rejimine bağlı)", f"IBS={ibs(k).iloc[-1]:.2f} -> {'SİNYAL' if sk.iloc[-1] else 'sinyal yok'}",
         f"C0: bugün kapanışta al, {nb[0]} kapanışında sat" if sk.iloc[-1] else "-")

    # B — Asya sepeti
    spy_r = p["c"].pct_change().iloc[-1]
    hits = [s for s in ["EWJ", "EWY", "EWT", "FXI", "EWA", "EWH"] if D[s]["c"].pct_change().iloc[-1] <= spy_r] if spy_r <= -0.015 else []
    line("B", "SPY ≤ -%1,5 gününde SPY'dan çok düşen Asya ETF'leri -> 1 gün", f"SPY {100*spy_r:+.2f}% -> {'SİNYAL: ' + ', '.join(hits) if hits else 'sinyal yok'}",
         f"C0: bugün kapanışta eşit tutarla al, {nb[0]} kapanışında sat" if hits else "-")

    # B — SVXY RSI(2)<10 & >SMA200 -> 2 gün (PTP)
    v = D["SVXY"]; r2 = rsi(v["c"]).iloc[-1]; above = v["c"].iloc[-1] > v["c"].rolling(200).mean().iloc[-1]
    sv = (r2 < 10) and above
    line("B", "SVXY RSI(2)<10 ve SMA200 üstü -> 2 gün (PTP %10 kesinti riski; Midas'ta teyit et)",
         f"RSI2={r2:.1f}, SMA200 üstü={above} -> {'SİNYAL' if sv else 'sinyal yok'}", f"C0: bugün kapanışta al, {next_bdays(last, 2)[-1]} kapanışında sat" if sv else "-")

    # B — mega-cap RSI(2) -> 2x ETF
    for stk, etf in STOCKS.items():
        c = ST[stk]["c"]; r = rsi(c).iloc[-1]; a = c.iloc[-1] > c.rolling(200).mean().iloc[-1]
        if r < 10 and a:
            line("B", f"{stk} RSI(2)<10 ve SMA200 üstü -> {etf} (2x) al, hisse SMA5 üstünde kapanınca ya da en geç 3 gün sonra sat",
                 f"RSI2={r:.1f}", f"C0: bugün kapanışta {etf} al; her akşam {stk} kapanışı > SMA5 mi kontrol et (en geç {next_bdays(last, 3)[-1]})")
    up = [f"{s}:RSI2={rsi(ST[s]['c']).iloc[-1]:.0f}{'' if ST[s]['c'].iloc[-1] > ST[s]['c'].rolling(200).mean().iloc[-1] else '(SMA200 altı)'}" for s in STOCKS]
    print(f"[B] Mega-cap RSI(2) özet: {' · '.join(up)}")

    # B — USO alt Bollinger -> C1 2 gün (PTP)
    u = D["USO"]["c"]; bb = u.iloc[-1] < (u.rolling(20).mean() - 2 * u.rolling(20).std()).iloc[-1]
    line("B", "USO alt Bollinger(20,2) kırılımı -> ertesi gün kapanışta al, 2 gün tut (PTP riski)", f"{'SİNYAL' if bb else 'sinyal yok'}",
         f"C1: {nb[0]} kapanışında al, {next_bdays(nb[0], 2)[-1]} kapanışında sat" if bb else "-")

    # Takvim kuralları
    print("\nTakvim kuralları (B):")
    # ay sonu GDX/GLD
    d = last; month_last = None
    for x in [last] + next_bdays(last, 30):
        nxt = next_bdays(x, 1)[0]
        if nxt.month != x.month and x >= last:
            month_last = x; break
    if month_last:
        ex = next_bdays(month_last, 3)[-1]
        print(f"  - Ay sonu GDX/GLD: sonraki giriş {month_last} kapanış (TR {tr_close(month_last)}), çıkış {ex} kapanış (TR {tr_close(ex)}). GDX ve GLD aynı bahis: birini seç.")
    # 10Y ihale
    p_ = os.path.join(EV, "hazine_ihale_10y30y.csv")
    if os.path.exists(p_):
        a = pd.read_csv(p_); a = a[a["event"].str.contains("10Y")]; ad = sorted(pd.to_datetime(a["date"]).dt.date)
        fut = [x for x in ad if x > last]
        if fut:
            A = fut[0]; cal = []; x = A
            while len(cal) < 3:
                x = x - dt.timedelta(days=1)
                if x.weekday() < 5 and x not in HOL: cal.append(x)
            print(f"  - 10Y Hazine ihalesi {A}: TMV/TBT giriş {cal[2]} kapanış (A-3), çıkış {cal[0]} kapanış (A-1). (TBT daha düşük kuyruk riski)")
    # EIA kış KOLD
    p_ = os.path.join(EV, "eia_ng_storage.csv")
    if os.path.exists(p_):
        e = sorted(pd.to_datetime(pd.read_csv(p_)["date"]).dt.date); fut = [x for x in e if x > last and x.month in (11, 12, 1, 2, 3)][:3]
        for R in fut:
            x = R
            while True:
                x = x - dt.timedelta(days=1)
                if x.weekday() < 5 and x not in HOL: break
            print(f"  - EIA doğalgaz raporu {R}: KOLD giriş {x} kapanış, çıkış {R} kapanış (zayıf; PTP; tek işlemde -%16 görüldü)")
    print("\nNot: Midas'ta MOC/LOC yok. 'Kapanışta al' = kapanıştan ~5-10 dk önce piyasa/agresif limit emir ya da kapanıştan sonra after-hours'ta kapanış fiyatına yakın LİMİT emir.")
    print("Yatırım tavsiyesi değildir; ayrıntı: RAPOR.md ve kartlar/<SYM>.md")

if __name__ == "__main__":
    main()
