"""KAP 'Endeksler' sayfasindan (https://www.kap.org.tr/tr/Endeksler, kardes ajanin indirdigi HTML) guncel endeks uyeliklerini cikarir.
Cikti: data/bist_test/kap_endeks_uyeleri.json  {endeks_kodu: [hisse,...]}"""
import re, json, sys
SP = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad"
h = open(SP + "/dl/kap_endeksler.html", encoding="utf-8", errors="ignore").read().replace('\\"', '"')
out = {}
for m in re.finditer(r'\{"code":"(X[A-Z0-9]+)","content":\[(.*?)\]', h):
    code, body = m.group(1), m.group(2)
    mem = re.findall(r'"stockCode":"([A-Z0-9]+)"', body)
    if mem and code not in out: out[code] = list(dict.fromkeys(mem))
json.dump(out, open(SP + "/data/bist_test/kap_endeks_uyeleri.json", "w"))
print(len(out), {k: len(v) for k, v in out.items() if k in ("XUTUM", "XU100", "XU030", "XBANK", "XUSIN", "XUMAL", "XUHIZ", "XUTEK", "XKTUM", "XTUMY", "XYLDZ")})
print(sorted(out.keys()))
