"""ETF'lerin TradingView kodlarını bulur: Nasdaq 'exchange' alanından aday önekler, sayfa okunarak doğrulanır.
PSE (NYSE Arca) -> AMEX ; NASDAQ-* -> NASDAQ ; BATS (Cboe BZX) -> CBOE, BATS ; NYSE -> AMEX, NYSE
Çıktı: sonuclar/tv_etf.csv (sym, exchange_nasdaq, tv, durum, baslik)"""
import os, sys, json, time, random, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import requests
import lib
from tv_verify import check

CAND = {"PSE": ["AMEX", "NYSE"], "BATS": ["CBOE", "BATS", "AMEX"], "NYSE": ["AMEX", "NYSE"], "AMEX": ["AMEX"]}

def cands(ex):
    if not ex: return ["AMEX", "NASDAQ", "CBOE", "NYSE"]
    if ex.startswith("NASDAQ"): return ["NASDAQ", "AMEX"]
    return CAND.get(ex, ["AMEX", "NASDAQ", "CBOE", "NYSE"])

if __name__ == "__main__":
    mt = lib.meta()
    out = os.path.join(lib.ROOT, "sonuclar", "tv_etf.csv")
    done = {}
    if os.path.exists(out):
        for r in csv.DictReader(open(out)): done[r["sym"]] = r
    s = requests.Session(); s.headers["User-Agent"] = "etf-research-script/1.0"
    syms = sys.argv[1:] or sorted(mt)
    for sym in syms:
        if sym in done and done[sym]["durum"] == "dogrulandi": continue
        ex = (mt.get(sym) or {}).get("exchange")
        rec = {"sym": sym, "exchange_nasdaq": ex, "tv": "", "durum": "bulunamadi", "baslik": ""}
        for pre in cands(ex):
            st, title, final = check(s, f"{pre}:{sym}")
            time.sleep(0.5 + random.random() * 0.5)
            if st == "dogrulandi":
                rec.update({"tv": f"{pre}:{sym}", "durum": st, "baslik": title[:150]}); break
        done[sym] = rec
        print(sym, rec["tv"], rec["durum"], flush=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sym", "exchange_nasdaq", "tv", "durum", "baslik"]); w.writeheader()
        for v in done.values(): w.writerow(v)
