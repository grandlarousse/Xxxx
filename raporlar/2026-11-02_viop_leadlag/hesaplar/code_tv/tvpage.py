"""Halka açık TradingView sembol sayfasını (https://www.tradingview.com/symbols/EXCH-SYM/) düz GET ile okur.
Başlık sahteciliği YOK (Origin/Referer eklenmez); iç API çağrılmaz. Sayfadaki window.initData.symbolInfo JSON'unu çıkarır."""
import json, re, subprocess, sys, time, urllib.parse
UA = None  # curl varsayılan UA
def fetch(tvsym, timeout=30):
    exch, sym = tvsym.split(':', 1)
    path = urllib.parse.quote(f"{exch}-{sym}", safe="-._~!")
    url = f"https://www.tradingview.com/symbols/{path}/"
    p = subprocess.run(["curl", "-sS", "-L", "--max-redirs", "3", "--compressed", "-m", str(timeout), "-o", "-", "-w", "\n__HTTP__%{http_code} %{url_effective} %{num_redirects}", url],
                       capture_output=True)
    out = p.stdout.decode('utf8', 'replace')
    i = out.rfind("\n__HTTP__")
    code, eff = (out[i+9:].split(' ', 1) + [''])[:2] if i >= 0 else ('000', '')
    body = out[:i] if i >= 0 else out
    info = None
    m = re.search(r'window\.initData\.symbolInfo\s*=\s*(\{.*?\});\s*</script>', body, re.S)
    if m:
        try: info = json.loads(m.group(1))
        except Exception: info = None
    t = re.search(r'<title>([^<]*)</title>', body)
    keep = {}
    if info:
        for k in ['resolved_symbol','pro_symbol','description','local_description','short_description','currency','type','typespecs','exchange','provider_id','isin_displayed','country','root','root_description','underlying_symbol','timezone']:
            keep[k] = info.get(k)
        s2 = info.get('source2') or {}
        keep['source'] = s2.get('description') or s2.get('name')
    return {'tv': tvsym, 'url': url, 'http': code.strip(), 'eff': eff.strip(), 'title': t.group(1) if t else None, 'info': keep}
if __name__ == '__main__':
    for s in sys.argv[1:]:
        print(json.dumps(fetch(s), ensure_ascii=False)); time.sleep(1.0)
