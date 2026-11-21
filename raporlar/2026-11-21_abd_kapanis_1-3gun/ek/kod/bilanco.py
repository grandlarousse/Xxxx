"""SEC EDGAR'dan 8-K Item 2.02 (bilanco aciklamasi) tarihleri.
Kullanim: python3 -I bilanco.py <ham_dizin> <cikti_csv>
 - <ham_dizin>/sec/ altina company_tickers.json ve CIK*.json (ek dosyalar dahil) indirir (varsa yeniden indirmez).
 - Islem takvimi: <ham_dizin>/SPY.json (Yahoo) gun listesi.
"""
import sys, os, json, time, datetime as dt, requests
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evren_tanim import KODLAR

ham, cikti = sys.argv[1], sys.argv[2]
sec = os.path.join(ham, "sec"); os.makedirs(sec, exist_ok=True)
H = {"User-Agent": "research-script/1.0 (generic research client)", "Accept-Encoding": "gzip, deflate"}
ET, UTC = ZoneInfo("America/New_York"), dt.timezone.utc
_son = [0.0]

def getj(url, yol):
    if os.path.exists(yol):
        return json.load(open(yol))
    for i in range(5):
        bekle = 0.22 - (time.time() - _son[0])     # <= 5 istek/sn
        if bekle > 0: time.sleep(bekle)
        _son[0] = time.time()
        try:
            r = requests.get(url, headers=H, timeout=30)
            if r.status_code == 200:
                j = r.json(); json.dump(j, open(yol, "w")); return j
            if r.status_code == 404: return None
        except Exception:
            pass
        time.sleep(1 + i)
    return None

# islem takvimi (SPY gunleri, NY yerel tarih)
spy = json.load(open(os.path.join(ham, "SPY.json")))["chart"]["result"][0]
gunler = sorted({dt.datetime.fromtimestamp(t, ET).date() for t in spy["timestamp"]})
gunset = set(gunler)
import bisect
def sonraki_gun(d, dahil):
    i = bisect.bisect_left(gunler, d) if dahil else bisect.bisect_right(gunler, d)
    return gunler[i] if i < len(gunler) else None

def kapanis_saati(d):
    """Yarim gunler (13:00 ET): Sukran Gunu sonrasi Cuma, 24 Aralik, 3 Temmuz (islem gunuyse)."""
    if d.month == 12 and d.day == 24: return dt.time(13, 0)
    if d.month == 7 and d.day == 3: return dt.time(13, 0)
    if d.month == 11 and d.weekday() == 4 and 23 <= d.day <= 29: return dt.time(13, 0)
    return dt.time(16, 0)

# www.sec.gov/files/company_tickers.json bu ortamda 403 ("Request Rate Threshold Exceeded") donduruyor;
# yedek: EDGAR tam metin arama varlik endeksi (efts.sec.gov), tickers alaninda birebir eslesme.
tick = getj("https://www.sec.gov/files/company_tickers.json", os.path.join(sec, "company_tickers.json")) if not os.path.exists(os.path.join(sec, "_efts_yok")) else None
cikmap = {v["ticker"].upper(): v["cik_str"] for v in tick.values()} if tick else {}
def efts_cik(k):
    j = getj(f"https://efts.sec.gov/LATEST/search-index?keysTyped={k}", os.path.join(sec, f"efts_{k}.json"))
    if not j: return None
    for h in j.get("hits", {}).get("hits", []):
        tk = [t.strip().upper() for t in (h["_source"].get("tickers") or "").split(",")]
        if k.upper() in tk or k.replace("-", ".").upper() in tk or k.replace("-", "").upper() in tk:
            return int(h["_id"])
    return None

satirlar, notlar = [], {}
hisseler = [k for k, g in KODLAR if g.startswith("h_")]
for k in hisseler:
    cik = cikmap.get(k) or cikmap.get(k.replace("-", ".")) or efts_cik(k)
    if cik is None:
        notlar[k] = "CIK bulunamadi"; continue
    c10 = f"{int(cik):010d}"
    sub = getj(f"https://data.sec.gov/submissions/CIK{c10}.json", os.path.join(sec, f"CIK{c10}.json"))
    if sub is None:
        notlar[k] = "submissions indirilemedi"; continue
    if k.upper() not in [t.upper() for t in sub.get("tickers", [])] and k.replace("-", ".").upper() not in [t.upper() for t in sub.get("tickers", [])]:
        notlar[k] = f"uyari: CIK {cik} tickers={sub.get('tickers')}"
    bloklar = [sub["filings"]["recent"]]
    for f in sub["filings"].get("files", []):
        e = getj("https://data.sec.gov/submissions/" + f["name"], os.path.join(sec, f["name"]))
        if e: bloklar.append(e)
    n = 0; formlar = set()
    for b in bloklar:
        for form, items, fd, acc in zip(b["form"], b.get("items", [""] * len(b["form"])), b["filingDate"], b["acceptanceDateTime"]):
            formlar.add(form)
            if form != "8-K" or "2.02" not in (items or "").split(","):
                continue
            if fd < "2004-12-01": continue
            # acceptanceDateTime 'Z' ekli ama ET degil UTC mi? -> asagida NVDA kontroluyle dogrulandi: gercek UTC.
            a = dt.datetime.fromisoformat(acc.replace("Z", "+00:00")).astimezone(UTC)
            ae = a.astimezone(ET); d = ae.date(); t = ae.time()
            if d in gunset:
                if t < dt.time(9, 30): seans = "ACILIS_ONCESI"; tep = d
                elif t < kapanis_saati(d): seans = "SEANS_ICI"; tep = d
                else: seans = "KAPANIS_SONRASI"; tep = sonraki_gun(d, False)
                nt = "" if kapanis_saati(d) == dt.time(16, 0) else "yarim_gun_13:00"
            else:
                seans = "KAPANIS_SONRASI" if t >= dt.time(9, 30) else "ACILIS_ONCESI"
                tep = sonraki_gun(d, True); nt = "islem_gunu_degil"
            satirlar.append((k, fd, a.strftime("%Y-%m-%d %H:%M:%S"), ae.strftime("%Y-%m-%d %H:%M:%S"), seans,
                             tep.isoformat() if tep else "", nt))
            n += 1
    if n == 0:
        yab = {"6-K", "20-F", "40-F"} & formlar
        notlar[k] = ("yabanci ihracci (" + "/".join(sorted(yab)) + "), 8-K 2.02 yok") if yab else "8-K 2.02 bulunamadi"
    elif {"6-K", "20-F", "40-F"} & formlar:
        notlar[k] = f"{n} adet 8-K 2.02; gecmiste 6-K/20-F/40-F de var (bir donem yabanci ihracci)"

import csv
satirlar.sort()
with open(cikti, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["kod", "filing_date", "acceptance_utc", "acceptance_et", "seans", "ilk_tepki_gunu", "not"])
    w.writerows(satirlar)
    for k in hisseler:
        if k in notlar and not any(s[0] == k for s in satirlar):
            w.writerow([k, "", "", "", "", "", notlar[k]])
json.dump(notlar, open(os.path.join(sec, "_notlar.json"), "w"), indent=1, ensure_ascii=False)
print(len(satirlar), "satir;", json.dumps(notlar, ensure_ascii=False))
