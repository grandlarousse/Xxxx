"""TradingView kodlarını sembol sayfasını okuyarak doğrular (https://www.tradingview.com/symbols/EXCH-SYM/).
200 + başlıkta sembol -> 'dogrulandi'; 404 -> 'yok'. Dürüst istemci adı, istekler arasında bekleme.
Kullanım: python3 -I kod/tv_verify.py girdi.txt  (satır başına bir 'EXCH:SYM')  -> sonuclar/tv_dogrulama.csv (birikimli)"""
import os, sys, re, time, random, csv
import requests
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "sonuclar", "tv_dogrulama.csv")

def check(s, tk):
    ex, sym = tk.split(":", 1)
    url = f"https://www.tradingview.com/symbols/{ex}-{sym}/"
    for a in range(4):
        try:
            r = s.get(url, timeout=40, allow_redirects=True)
        except Exception:
            time.sleep(2 ** a); continue
        if r.status_code == 429: time.sleep(5 * 2 ** a); continue
        t = re.search(r"<title>(.*?)</title>", r.text, re.S)
        title = t.group(1).strip().replace("&amp;", "&") if t else ""
        final = r.url
        if r.status_code == 404: return "yok", title, final
        if r.status_code == 200:
            ok = (ex.upper() + "-" + sym.upper().replace("!", "%21") in final.upper()) or (ex.upper() + "-" + sym.upper() in final.upper())
            if ok: return "dogrulandi", title, final
            # kanonik sayfaya yönlendirme (FX, kripto, 2. vade vb.): istenen kod sayfa içinde geçiyorsa geçerli say
            if tk.upper() in r.text.upper() or ("contract=" + sym.replace("!", "%21")).upper() in final.upper():
                return "dogrulandi_kanonik", title, final
            return "yonlendirildi", title, final
        return f"HTTP{r.status_code}", title, final
    return "ag_hatasi", "", url

if __name__ == "__main__":
    tks = [l.strip() for l in open(sys.argv[1]) if l.strip() and ":" in l]
    done = {}
    if os.path.exists(OUT):
        for row in csv.DictReader(open(OUT)): done[row["ticker"]] = row
    s = requests.Session(); s.headers["User-Agent"] = "etf-research-script/1.0"
    for tk in tks:
        if tk in done and done[tk]["durum"] in ("dogrulandi", "dogrulandi_kanonik", "yok"): continue
        st, title, final = check(s, tk)
        done[tk] = {"ticker": tk, "durum": st, "baslik": title[:160], "url": final}
        print(tk, st, title[:80], flush=True)
        time.sleep(0.6 + random.random() * 0.6)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "durum", "baslik", "url"]); w.writeheader()
        for v in done.values(): w.writerow(v)
