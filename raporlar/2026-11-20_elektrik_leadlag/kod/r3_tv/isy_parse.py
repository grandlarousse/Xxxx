#!/usr/bin/env python3
"""Is Yatirim 'Temel Degerler ve Oranlar' sayfasindan XELKT uyelerinin
piyasa degeri (mn TL) ve halka aciklik oranini cikarir. python3 -I isy_parse.py <html> <json_cikti>"""
import html, json, re, sys
UYE = ("A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN CONSE CWENE CANTE CATES "
       "ARASE ECOGR ENDAE ENJSA ENERY ESEN GWIND HUNER ENTRA IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ "
       "NATEN ODAS PAMEL SMRTG TATEN VEYAS ZEDUR ZOREN ASTOR ALARK EUPWR GESAN").split()
def num(s):
    s = s.strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except ValueError: return None
src = open(sys.argv[1], encoding="utf-8", errors="replace").read()
pat = re.compile(r'hisse=([A-Z0-9]+)">\1</a></td><td>([^<]*)</td><td>([^<]*)</td>' + r'<td class="text-right">([^<]*)</td>' * 5)
out = {}
for m in pat.finditer(src):
    k = m.group(1)
    if k in UYE and k not in out:
        out[k] = dict(ad=html.unescape(m.group(2)), sektor=html.unescape(m.group(3)), kapanis=num(m.group(4)),
                      pd_mn_tl=num(m.group(5)), pd_mn_usd=num(m.group(6)), hao=num(m.group(7)), sermaye_mn_tl=num(m.group(8)))
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("bulunan", len(out), "eksik", [k for k in UYE if k not in out])
tot = sum(v["pd_mn_tl"] * v["hao"] / 100 for k, v in out.items() if k in UYE[:42] and v["pd_mn_tl"] and v["hao"])
print("toplam PD mn TL", round(sum(v["pd_mn_tl"] or 0 for k, v in out.items() if k in UYE[:42])), "halka acik PD", round(tot))
for k, v in sorted(out.items(), key=lambda kv: -((kv[1]["pd_mn_tl"] or 0) * (kv[1]["hao"] or 0))):
    w = (v["pd_mn_tl"] or 0) * (v["hao"] or 0) / 100 / tot * 100 if k in UYE[:42] else float("nan")
    print(k, v["ad"][:22], "|", v["sektor"][:22], "|", v["kapanis"], v["pd_mn_tl"], v["hao"], round(w, 2))
