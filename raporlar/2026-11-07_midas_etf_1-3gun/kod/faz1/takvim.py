"""Faz 1 — Olay takvimleri üretici (2016-01-01 .. 2026-12-31; NYSE tatilleri 2016-2027).

Kullanım:
    python3 -I kod/faz1/takvim.py <proje_kök_klasörü>

Girdi: <kök>/ham_sayfalar/takvim/ altındaki ham sayfalar (fetch_pages.py ile indirilmiş
       resmî sayfalar, Cboe JSON, fiscaldata JSON, EIA vadeli fiyat tabloları ve WebFetch
       çıktılarının kaydedildiği webfetch/*.txt dosyaları). Bu betik internete ÇIKMAZ;
       sadece yerel ham dosyaları okur, kurala dayalı tarihleri hesaplar ve doğrular.
Çıktı: <kök>/data/events/*.csv  (sütunlar: date, event, detail, source)
       <kök>/data/events/_dogrulama.json (doğrulama özetleri; not dosyası bundan yazılır)
"""
import csv
import datetime as dt
import html as htmlmod
import json
import os
import re
import sys
from collections import Counter, defaultdict

D = dt.date
START, END = D(2016, 1, 1), D(2026, 12, 31)
MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
MCODE = "FGHJKMNQUVXZ"  # vadeli ay kodları
TR_AY = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos",
         "Eylül", "Ekim", "Kasım", "Aralık"]
GUN = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
HAM = os.path.join(ROOT, "ham_sayfalar", "takvim")
OUT = os.path.join(ROOT, "data", "events")
VERIFY = {}


def rd(name, enc="utf-8"):
    with open(os.path.join(HAM, name), encoding=enc, errors="replace") as f:
        return f.read()


def in_range(d):
    return START <= d <= END


def write_csv(name, rows, src_note):
    rows = sorted(rows, key=lambda r: (r[0], r[1]))
    path = os.path.join(OUT, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "event", "detail", "source"])
        for r in rows:
            w.writerow([r[0].isoformat(), r[1], r[2], r[3]])
    VERIFY.setdefault("satir_sayilari", {})[name] = len(rows)
    VERIFY.setdefault("kaynak_notlari", {})[name] = src_note
    print(f"{name}: {len(rows)} satır")


# ----------------------------------------------------------------------------------------
# 1) Tatil takvimleri
# ----------------------------------------------------------------------------------------
def easter(y):
    a = y % 19; b = y // 100; c = y % 100; d = b // 4; e = b % 4; f = (b + 8) // 25
    g = (b - f + 1) // 3; h = (19 * a + b - d - g + 15) % 30; i = c // 4; k = c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7; m = (a + 11 * h + 22 * l_) // 451
    mo = (h + l_ - 7 * m + 114) // 31; da = ((h + l_ - 7 * m + 114) % 31) + 1
    return D(y, mo, da)


def nth_wd(y, m, wd, n):
    d = D(y, m, 1)
    d += dt.timedelta(days=(wd - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def last_wd(y, m, wd):
    d = D(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() - wd) % 7)


def observed(d, sat_to_fri=True):
    if d.weekday() == 5:
        return d - dt.timedelta(days=1) if sat_to_fri else None
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


NYSE_SPECIAL = {D(2018, 12, 5): "Ulusal yas günü (George H.W. Bush) — özel kapanış",
                D(2025, 1, 9): "Ulusal yas günü (Jimmy Carter) — özel kapanış"}


def nyse_regular_holidays(y):
    h = {}
    nyd = D(y, 1, 1)
    if nyd.weekday() == 6:
        h[D(y, 1, 2)] = "New Year's Day (gözlenen)"
    elif nyd.weekday() != 5:  # Cumartesi ise NYSE gözlemez (önceki Cuma açık)
        h[nyd] = "New Year's Day"
    h[nth_wd(y, 1, 0, 3)] = "Martin Luther King, Jr. Day"
    h[nth_wd(y, 2, 0, 3)] = "Washington's Birthday"
    h[easter(y) - dt.timedelta(days=2)] = "Good Friday"
    h[last_wd(y, 5, 0)] = "Memorial Day"
    if y >= 2022:
        jt = observed(D(y, 6, 19))
        h[jt] = "Juneteenth" + (" (gözlenen)" if jt != D(y, 6, 19) else "")
    ind = observed(D(y, 7, 4))
    h[ind] = "Independence Day" + (" (gözlenen)" if ind != D(y, 7, 4) else "")
    h[nth_wd(y, 9, 0, 1)] = "Labor Day"
    h[nth_wd(y, 11, 3, 4)] = "Thanksgiving Day"
    xm = observed(D(y, 12, 25))
    h[xm] = "Christmas Day" + (" (gözlenen)" if xm != D(y, 12, 25) else "")
    return h


def nyse_early_closes(y):
    e = {}
    jul3 = D(y, 7, 3)
    if jul3.weekday() <= 3:  # Pzt-Per (4 Temmuz Sal-Cum)
        e[jul3] = "Independence Day öncesi erken kapanış 13:00 ET"
    e[nth_wd(y, 11, 3, 4) + dt.timedelta(days=1)] = "Thanksgiving ertesi erken kapanış 13:00 ET"
    xe = D(y, 12, 24)
    if xe.weekday() <= 3:
        e[xe] = "Noel arifesi erken kapanış 13:00 ET"
    return e


NYSE_HOL = {}
for _y in range(2015, 2036):
    NYSE_HOL.update(nyse_regular_holidays(_y))
NYSE_HOL.update(NYSE_SPECIAL)
CME_HOL = {d: n for d, n in NYSE_HOL.items() if d not in NYSE_SPECIAL}  # yaklaşık CME tatili


def is_bd(d, hol=NYSE_HOL):
    return d.weekday() < 5 and d not in hol


def add_bd(d, n, hol=NYSE_HOL):
    step = 1 if n >= 0 else -1
    k = 0
    while k != n:
        d += dt.timedelta(days=step)
        if is_bd(d, hol):
            k += step
    return d


def prev_or_same_bd(d, hol=NYSE_HOL):
    while not is_bd(d, hol):
        d -= dt.timedelta(days=1)
    return d


def bdays_of_month(y, m, hol=NYSE_HOL):
    d = D(y, m, 1); out = []
    while d.month == m:
        if is_bd(d, hol):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


# Federal (OPM) tatilleri + başkanlık kararnamesiyle kapanışlar — EIA kuralı için
FED_EO = {D(2018, 12, 5): "Ulusal yas günü (Bush)", D(2018, 12, 24): "Noel arifesi (EO)",
          D(2019, 12, 24): "Noel arifesi (EO)", D(2020, 12, 24): "Noel arifesi (EO)",
          D(2024, 12, 24): "Noel arifesi (EO)", D(2025, 1, 9): "Ulusal yas günü (Carter)",
          D(2025, 12, 24): "Noel arifesi (EO)", D(2025, 12, 26): "Noel ertesi (EO)"}


def federal_holidays(y):
    h = {}
    for d0, n in [(D(y, 1, 1), "New Year's Day"), (D(y, 7, 4), "Independence Day"),
                  (D(y, 11, 11), "Veterans Day"), (D(y, 12, 25), "Christmas Day")]:
        h[observed(d0)] = n
    if D(y + 1, 1, 1).weekday() == 5:
        h[D(y, 12, 31)] = "New Year's Day (gözlenen)"
    if y >= 2021:
        h[observed(D(y, 6, 19))] = "Juneteenth"
    h[nth_wd(y, 1, 0, 3)] = "MLK Day"; h[nth_wd(y, 2, 0, 3)] = "Washington's Birthday"
    h[last_wd(y, 5, 0)] = "Memorial Day"; h[nth_wd(y, 9, 0, 1)] = "Labor Day"
    h[nth_wd(y, 10, 0, 2)] = "Columbus Day"; h[nth_wd(y, 11, 3, 4)] = "Thanksgiving Day"
    return h


FED_CLOSED = {}
for _y in range(2015, 2028):
    FED_CLOSED.update(federal_holidays(_y))
FED_CLOSED.update(FED_EO)


def build_nyse():
    rows = []
    src = "https://www.nyse.com/markets/hours-calendars"
    # Resmî 2026-2027 listesi (NYSE sayfası)
    txt = rd("www.nyse.com_markets_hours-calendars.txt")
    lines = [l.strip() for l in txt.splitlines()]
    i = lines.index("2028") + 1
    official = {}
    while i + 3 < len(lines) and not lines[i].startswith("*"):
        name, c26, c27 = lines[i], lines[i + 1], lines[i + 2]
        for yy, cell in ((2026, c26), (2027, c27)):
            m = re.match(r"\w+day, (\w+) (\d+)", cell)
            if m:
                official[D(yy, MONTHS[m.group(1)[:3].lower()], int(m.group(2)))] = name
        i += 4
    off_early = set()
    for l in lines:
        for m in re.finditer(r"(?:Monday|Tuesday|Wednesday|Thursday|Friday), (\w+) (\d+), (\d{4})", l):
            if "close early" in l:
                off_early.add(D(int(m.group(3)), MONTHS[m.group(1)[:3].lower()], int(m.group(2))))
    comp = {d: n for d, n in NYSE_HOL.items() if d.year in (2026, 2027)}
    comp_e = {d for y in (2026, 2027) for d in nyse_early_closes(y)}
    off_e_2627 = {d for d in off_early if d.year in (2026, 2027)}
    VERIFY["nyse_resmi_2026_2027"] = {
        "resmi_tatil_sayisi": len(official), "hesap_tatil_sayisi": len(comp),
        "fark_tatil": sorted(str(d) for d in set(official) ^ set(comp)),
        "fark_erken_kapanis": sorted(str(d) for d in off_e_2627 ^ comp_e)}
    # Fiyat verisinden doğrulama: işlem görmeyen hafta içi günler
    try:
        import pandas as pd
        spy = pd.read_parquet(os.path.join(ROOT, "data", "etf", "SPY.parquet")).index
        vix = pd.read_parquet(os.path.join(ROOT, "data", "vol", "VIX.parquet")).index
        spy0 = min(x.date() for x in spy)
        # VIX verisi 2022 sonrası bazı tatillerde (Cboe GTH seansı) satır içeriyor -> VIX yalnız SPY öncesi
        traded = {x.date() for x in spy} | {x.date() for x in vix if D(2016, 1, 1) <= x.date() < spy0}
        lo, hi = D(2016, 1, 1), max(x.date() for x in spy)
        d = lo; missing = set()
        while d <= hi:
            if d.weekday() < 5 and d not in traded:
                missing.add(d)
            d += dt.timedelta(days=1)
        hol_in = {d for d in NYSE_HOL if lo <= d <= hi and d.weekday() < 5}
        VERIFY["nyse_fiyat_verisi"] = {
            "aralik": f"{lo}..{hi} (VIX 2016-01..; SPY 2016-11-07..)",
            "islem_yok_haftaici": len(missing), "hesap_tatil": len(hol_in),
            "veride_islem_var_ama_tatil_dedik": sorted(str(x) for x in hol_in - missing),
            "veride_islem_yok_ama_tatil_degil": sorted(str(x) for x in missing - hol_in)}
    except Exception as e:  # noqa: BLE001
        VERIFY["nyse_fiyat_verisi"] = f"hata: {e}"
    for d, n in NYSE_HOL.items():
        if 2016 <= d.year <= 2027:
            kind = "resmî liste (nyse.com)" if d.year >= 2026 else "kural"
            if d in NYSE_SPECIAL:
                kind = "özel kapanış (bilinen istisna)"
            rows.append((d, "NYSE_tatil", f"{n}; {GUN[d.weekday()]}; tam gün kapalı; {kind}",
                         src if d.year >= 2026 else "kural (NYSE kuralı) + SPY/VIX işlem günleriyle doğrulama"))
    for y in range(2016, 2028):
        for d, n in nyse_early_closes(y).items():
            kind = "resmî liste (nyse.com)" if y >= 2026 else "kural"
            rows.append((d, "NYSE_erken_kapanis", f"{n} (opsiyon 13:15); {GUN[d.weekday()]}; {kind}",
                         src if y >= 2026 else "kural (NYSE erken kapanış kuralı)"))
    write_csv("nyse_tatil.csv", rows,
              "2026-2027 resmî NYSE listesi; 2016-2025 kuraldan (özel kapanışlar 2018-12-05, 2025-01-09) "
              "+ SPY/VIX günlük veride işlem olmayan günlerle karşılaştırma")


# ----------------------------------------------------------------------------------------
# 2) FOMC
# ----------------------------------------------------------------------------------------
MONTH_LABEL = re.compile(r"^(January|February|March|April|May|June|July|August|September|October|"
                         r"November|December|Jan/Feb|Feb/Mar|Mar/Apr|Apr/May|April/May|May/Jun|"
                         r"Jun/Jul|Jul/Aug|Aug/Sep|Sep/Oct|Oct/Nov|Nov/Dec|Dec/Jan)$")


def two_month(label):
    parts = label.split("/")
    m1 = MONTHS[parts[0][:3].lower()]
    m2 = MONTHS[parts[-1][:3].lower()]
    return m1, m2


def build_fomc():
    rows = []
    cal_src = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
    # 2021-2027 (güncel sayfa)
    lines = [l.strip() for l in rd("www.federalreserve.gov_monetarypolicy_fomccalendars.htm.txt").splitlines()]
    year = None; cur = None; meetings = []
    for i, l in enumerate(lines):
        m = re.match(r"^(\d{4}) FOMC Meetings$", l)
        if m:
            year = int(m.group(1)); continue
        if year and MONTH_LABEL.match(l) and i + 1 < len(lines):
            dm = re.match(r"^(\d{1,2})(?:-(\d{1,2}))?(\*)?\s*(?:\((.+)\))?$", lines[i + 1])
            if dm:
                m1, m2 = two_month(l)
                d1 = int(dm.group(1)); d2 = int(dm.group(2)) if dm.group(2) else d1
                end_m = m2 if dm.group(2) else m1
                if dm.group(2) and d2 < d1 and m1 == m2:
                    end_m = m1 + 1
                cur = {"year": year, "label": l, "days": lines[i + 1], "end": D(year, end_m, d2),
                       "start": D(year, m1, d1), "sep": bool(dm.group(3)), "note": dm.group(4) or "",
                       "pc": False, "src": cal_src}
                meetings.append(cur)
                continue
        if cur and l == "Press Conference":
            cur["pc"] = True
    # 2016-2020 (tarihsel sayfalar)
    for y in range(2016, 2021):
        src = f"https://www.federalreserve.gov/monetarypolicy/fomchistorical{y}.htm"
        lines = [l.strip() for l in rd(f"www.federalreserve.gov_monetarypolicy_fomchistorical{y}.htm.txt").splitlines()]
        cur = None
        for l in lines:
            m = re.match(r"^(\w+(?:/\w+)?) (\d{1,2})(?:-(\d{1,2}))? ?(?:\((unscheduled|cancelled|notation vote)\))?"
                         r"(?: Meeting)? - (\d{4})$", l)
            if m and int(m.group(5)) == y:
                m1, m2 = two_month(m.group(1))
                d1 = int(m.group(2)); d2 = int(m.group(3)) if m.group(3) else d1
                end_m = m2 if m.group(3) else m1
                cur = {"year": y, "label": m.group(1), "days": l, "start": D(y, m1, d1),
                       "end": D(y, end_m, d2), "sep": False, "note": m.group(4) or "", "pc": False,
                       "src": src, "stmt": None}
                meetings.append(cur); continue
            if cur is None:
                continue
            if l.startswith("SEP:") or l.startswith("Projection Materials"):
                cur["sep"] = True
            if l == "Press Conference":
                cur["pc"] = True
            ms = re.match(r"^Statement \(Released (\w+) (\d+), (\d{4})\)", l)
            if ms:
                cur["stmt"] = D(int(ms.group(3)), MONTHS[ms.group(1)[:3].lower()], int(ms.group(2)))
    # Fed basın bültenlerinden açıklama saatleri (ham sayfalardan)
    pr_times = {}
    for f in os.listdir(HAM):
        m = re.match(r"www\.federalreserve\.gov_newsevents_pressreleases_monetary(\d{8})[ab]\.htm\.txt$", f)
        if m:
            t = re.search(r"For release at ([0-9:]+ [ap]\.m\. E[DS]T)", rd(f))
            dd = dt.datetime.strptime(m.group(1), "%Y%m%d").date()
            pr_times[dd] = (t.group(1) if t else "saat bulunamadı",
                            "https://www.federalreserve.gov/newsevents/pressreleases/" + f.split("_")[-1][:-4])
    special = {
        D(2019, 10, 11): ("FOMC_plansiz", "Plansız toplantı (4 Eki 2019 konferans görüşmesi); açıklama 11 Eki; "
                          "faiz değişmedi (1.75-2.00%), T-bill alımları/rezerv yönetimi"),
        D(2020, 3, 3): ("FOMC_plansiz", "Plansız toplantı (2 Mar 2020); açıklama 3 Mar; faiz -50bp -> 1.00-1.25%"),
        D(2020, 3, 15): ("FOMC_plansiz", "Plansız toplantı (Pazar 15 Mar 2020); faiz -> 0-0.25%; piyasa tepkisi "
                         "16 Mar Pazartesi; basın toplantısı (telekonferans) yapıldı; SEP yayımlanmadı"),
        D(2020, 3, 18): ("FOMC_iptal", "Planlı 17-18 Mar 2020 toplantısı İPTAL (15 Mar'a öne alındı); bu tarihte açıklama yok"),
        D(2020, 3, 19): ("FOMC_diger", "Notation vote: merkez bankalarıyla geçici USD swap hatları (faiz kararı değil)"),
        D(2020, 3, 23): ("FOMC_plansiz", "Notation vote: Hazine/MBS alımları 'in the amounts needed' (sınırsız QE); faiz 0-0.25% sabit"),
        D(2020, 3, 31): ("FOMC_diger", "Notation vote: geçici FIMA Repo Facility (faiz kararı değil)"),
        D(2020, 8, 27): ("FOMC_diger", "Notation vote: Uzun Vadeli Hedefler ve Strateji Bildirgesi güncellemesi (Jackson Hole)"),
        D(2025, 8, 22): ("FOMC_diger", "Notation vote: Uzun Vadeli Hedefler ve Strateji Bildirgesi güncellemesi"),
    }
    seen = set()
    for mt in meetings:
        note = mt["note"]
        if note in ("unscheduled", "notation vote") or "notation" in note:
            ann = mt.get("stmt") or mt["end"]
            if note == "unscheduled" and mt["start"] == D(2020, 3, 2):
                ann = D(2020, 3, 3)
            if ann not in special:
                continue  # ör. açıklamasız konferans görüşmeleri
            ev, det = special[ann]
            t, prsrc = pr_times.get(ann, ("saat bulunamadı", mt["src"]))
            rows.append((ann, ev, f"{det}; açıklama saati {t}", f"{mt['src']} ; {prsrc}"))
            seen.add(ann); continue
        if note == "cancelled":
            ev, det = special[mt["end"]]
            rows.append((mt["end"], ev, det, mt["src"])); seen.add(mt["end"]); continue
        d = mt["end"]
        if not in_range(d):
            continue
        y = d.year
        pc = "var" if mt["pc"] else ("2019'dan beri her toplantıda planlı" if d > D(2026, 11, 7) else "yok")
        det = (f"Planlı toplantı {mt['start'].isoformat()}..{d.isoformat()} ({mt['label']} {mt['days'].split(' Meeting')[0].split()[-1] if y <= 2020 else mt['days']}); "
               f"karar açıklaması 2. gün 14:00 ET (TR {'21:00' if is_dst(d) else '22:00'}); "
               f"SEP/projeksiyon: {'EVET' if mt['sep'] else 'hayır'}; basın toplantısı 14:30 ET: {pc}")
        if d > D(2026, 11, 7):
            det += "; GELECEK (Fed sayfasında 'tentative until confirmed')"
        rows.append((d, "FOMC_karar", det, mt["src"]))
    for d, (ev, det) in special.items():
        if d not in seen:
            VERIFY.setdefault("fomc_uyari", []).append(f"özel satır eşleşmedi: {d}")
    fk = [r for r in rows if r[1] == "FOMC_karar"]
    VERIFY["fomc"] = {"planli_karar": len(fk), "yillara_gore": dict(sorted(Counter(r[0].year for r in fk).items())),
                      "SEP_sayisi": sum("SEP/projeksiyon: EVET" in r[2] for r in fk),
                      "carsamba_olmayan_planli": [str(r[0]) for r in fk if r[0].weekday() != 2],
                      "plansiz_diger_iptal": [(str(r[0]), r[1]) for r in rows if r[1] != "FOMC_karar"]}
    write_csv("fomc.csv", rows, "federalreserve.gov fomccalendars.htm (2021-2026) + fomchistorical2016-2020.htm + "
              "plansız/notation vote basın bültenleri (saatler bültenlerden)")


def is_dst(d):
    """ABD yaz saati: Mart 2. Pazar .. Kasım 1. Pazar."""
    s = nth_wd(d.year, 3, 6, 2); e = nth_wd(d.year, 11, 6, 1)
    return s <= d < e


# ----------------------------------------------------------------------------------------
# 3) CPI ve NFP (BLS)
# ----------------------------------------------------------------------------------------
def parse_bls(archive_file, sched_file, prefix):
    out = {}
    for l in rd(os.path.join("webfetch", archive_file)).splitlines():
        if l.startswith("#") or "|" not in l:
            continue
        ref, url = [x.strip() for x in l.split("|", 1)]
        ref = ref.replace(" Consumer Price Index", "")
        m = re.search(prefix + r"_(\d{2})(\d{2})(\d{4})\.htm", url)
        if not m:
            continue
        d = D(int(m.group(3)), int(m.group(1)), int(m.group(2)))
        out[d] = (ref, "arşiv", "https://www.bls.gov" + url if url.startswith("/") else url)
    for l in rd(os.path.join("webfetch", sched_file)).splitlines():
        if l.startswith("#") or "|" not in l:
            continue
        ref, ds, tm = [x.strip() for x in l.split("|")]
        d = dt.datetime.strptime(ds.replace(".", "").replace("Sept", "Sep"), "%b %d, %Y").date()
        if d not in out:
            out[d] = (ref, "resmî takvim; GELECEK" if d > D(2026, 11, 7) else "resmî takvim", None)
    return out


def build_bls():
    lapse = {}
    for l in rd(os.path.join("webfetch", "bls_2025_lapse.txt")).splitlines():
        if l.startswith("#") or "|" not in l:
            continue
        rel, ref, prev, rev = [x.strip() for x in l.split("|")]
        lapse[(rel, ref)] = (prev, rev)
    lapse_src = "https://www.bls.gov/bls/2025-lapse-revised-release-dates.htm"
    for kind, arch, sched, prefix, ev, relname, arch_url, sched_url in [
        ("cpi", "bls_cpi_archive_links.txt", "bls_cpi_schedule.txt", "cpi", "CPI", "Consumer Price Index",
         "https://www.bls.gov/bls/news-release/cpi.htm", "https://www.bls.gov/schedule/news_release/cpi.htm"),
        ("nfp", "bls_empsit_archive_links.txt", "bls_empsit_schedule.txt", "empsit", "NFP", "Employment Situation",
         "https://www.bls.gov/bls/news-release/empsit.htm", "https://www.bls.gov/schedule/news_release/empsit.htm")]:
        data = parse_bls(arch, sched, prefix)
        rows = []
        for d, (ref, typ, url) in data.items():
            if not in_range(d):
                continue
            det = f"Referans ayı: {ref}; 08:30 ET (TR {'15:30' if is_dst(d) else '16:30'}); {GUN[d.weekday()]}; kaynak tipi: {typ}"
            if d in NYSE_HOL:
                det += f"; NYSE KAPALI ({NYSE_HOL[d]}) — vadeli piyasalar kısa seans; ETF tepkisi ertesi işlem günü"
            key = (relname, ref)
            if key in lapse and lapse[key][1] not in ("NO CHANGE",):
                det += f"; 2025-26 bütçe kesintisi nedeniyle KAYDI (önceki plan {lapse[key][0]})"
            if kind == "cpi" and ref == "September 2025":
                det += "; 2025 kapanması nedeniyle gecikmeli yayım (orijinal plan haberlere göre 2025-10-15, resmî sayfada doğrulanamadı)"
            if kind == "nfp" and ref == "November 2025":
                det += "; Ekim 2025 kurum anketi (payroll) verisi de bu raporla yayımlandı"
            rows.append((d, ev, det, (url or sched_url) + f" ; liste: {arch_url if typ == 'arşiv' else sched_url}"))
        for (rel, ref), (prev, rev) in lapse.items():
            if rel == relname and rev.startswith("CANCELED"):
                d = D(*map(int, prev.split("-")))
                rows.append((d, ev + "_iptal", f"Referans ayı: {ref}; YAYIMLANMADI (planlanan tarih {prev}); {rev}", lapse_src))
        dts = sorted(r[0] for r in rows if r[1] == ev)
        VERIFY[kind] = {"yayim_sayisi": len(dts), "yillara_gore": dict(sorted(Counter(d.year for d in dts).items())),
                        "gun_dagilimi": dict(Counter(GUN[d.weekday()] for d in dts)),
                        "nfp_cuma_disi" if kind == "nfp" else "cpi_ornek_son5": (
                            [f"{d} {GUN[d.weekday()]}" for d in dts if d.weekday() != 4] if kind == "nfp" else [str(x) for x in dts[-5:]]),
                        "tatil_cakisma": [str(d) for d in dts if d in NYSE_HOL]}
        write_csv(f"{kind}.csv", rows, f"BLS arşiv sayfası {arch_url} (URL'deki yayım tarihleri) + BLS takvimi {sched_url} "
                  f"+ {lapse_src}; requests 403 verdiği için WebFetch ile okundu")


# ----------------------------------------------------------------------------------------
# 4) EIA haftalık doğalgaz depolama
# ----------------------------------------------------------------------------------------
def ng_storage_rule(thu):
    """Kural (2025-2026 resmî takvim + teyitli örneklerden türetildi)."""
    wk = {thu + dt.timedelta(days=k): (thu + dt.timedelta(days=k)) in FED_CLOSED for k in range(-3, 2)}
    mon, tue, wed, t, fri = (wk[thu + dt.timedelta(days=k)] for k in range(-3, 2))
    if t:
        if not wed:
            return thu - dt.timedelta(days=1), "12:00 ET", "Perşembe kapalı -> Çarşamba 12:00"
        return None, None, "Çarşamba+Perşembe kapalı: kural tanımsız"
    if tue or wed:
        if fri:
            return None, None, "Sal/Çar ve Cuma kapalı: kural tanımsız"
        return thu + dt.timedelta(days=1), "10:30 ET", "Salı/Çarşamba kapalı -> Cuma 10:30"
    return thu, "10:30 ET", "normal"


def build_ng_storage():
    src_sched = "https://ir.eia.gov/ngs/schedule.html"
    txt = rd("ir.eia.gov_ngs_schedule.html.txt")
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    off = {}
    for i, l in enumerate(lines):
        m = re.match(r"^(\w+) (\d{1,2}), (\d{4})( - \(Updated\))?$", l)
        if m and m.group(1)[:3].lower() in MONTHS:
            d = D(int(m.group(3)), MONTHS[m.group(1)[:3].lower()], int(m.group(2)))
            off[d] = (lines[i + 1], lines[i + 2], lines[i + 3].replace("â\x80\x99", "'").replace("â", "'"),
                      bool(m.group(4)))
    # resmî istisnaları ait oldukları Perşembe'ye eşle
    off_by_thu = {}
    shift = {0: -4, 1: 2, 2: 1, 3: 0, 4: -1}  # Pzt->önceki Per (gecikme), Sal/Çar->sonraki Per, Cum->önceki Per
    en_tr = {"Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba", "Thursday": "Perşembe", "Friday": "Cuma"}
    for d, v in off.items():
        thu = d + dt.timedelta(days=shift[d.weekday()])
        assert thu.weekday() == 3 and thu not in off_by_thu, (d, thu)
        off_by_thu[thu] = (d, (en_tr.get(v[0], v[0]),) + v[1:])
    confirmed = {}
    for l in rd(os.path.join("webfetch", "websearch_teyitler.txt")).splitlines():
        m = re.match(r"^(\d{4}-\d{2}-\d{2}) \| ([^|]+)\|([^|]+)\| (.+)$", l)
        if m:
            confirmed[D(*map(int, m.group(1).split("-")))] = (m.group(2).strip(), m.group(4).strip())
    rows = []; cmp_rows = []
    thu = D(2016, 1, 7)
    while thu <= END:
        rd_, tm, why = ng_storage_rule(thu)
        if thu >= D(2025, 1, 2):
            # resmî takvim dönemi (sayfa 2025 başından itibaren istisnaları listeliyor)
            if thu in off_by_thu:
                d, (day, t, hol, upd) = off_by_thu[thu]
                det = f"{day} {t}; {hol}{' (güncellendi)' if upd else ''}; resmî istisna"
            else:
                d, det = thu, "Perşembe 10:30 ET; resmî takvimde istisna yok"
            if rd_ != d:
                cmp_rows.append((str(thu), "kural=" + (str(rd_) if rd_ else "tanımsız"), "resmî=" + str(d)))
            if d > D(2026, 11, 7):
                det += "; GELECEK"
            if d == D(2026, 12, 24):
                det += "; Noel arifesi federal kapanış kararnamesi çıkarsa değişebilir"
            if in_range(d):
                rows.append((d, "EIA_NG_depolama", det + f"; TR {tr_time(d, t if 'p.m.' in det or 'a.m.' in det else '10:30 a.m.')}", src_sched))
        else:
            if rd_ is None:
                rd_, tm = thu, "10:30 ET"; why += " (Perşembe varsayıldı)"
            det = f"{GUN[rd_.weekday()]} {tm}; {why}; kural"
            if rd_ in confirmed:
                det += f"; TEYİT: {confirmed[rd_][0]}"
                srcx = "kural ; teyit: " + confirmed[rd_][1]
            else:
                srcx = "kural (EIA standart Perşembe 10:30 ET + federal tatil kaydırma kuralı; bkz. notlar/takvim_notlari.md)"
            if rd_ in (D(2018, 12, 7),):
                det += "; BELİRSİZ: 5 Ara 2018 yas günü kısa sürede ilan edildi, rapor Perşembe 6 Ara'da da çıkmış olabilir"
            if rd_.year <= 2024 and why != "normal" and rd_ not in confirmed:
                det += "; doğrulanmadı"
            rows.append((rd_, "EIA_NG_depolama", det, srcx))
        thu += dt.timedelta(days=7)
    VERIFY["ng_depolama"] = {
        "resmi_istisnalar": {str(k): v[0] + " " + v[1] for k, v in off.items()},
        "kural_vs_resmi_2025_2026_farklar": cmp_rows,
        "kural_istisnalari_2016_2024": [f"{r[0]} {r[2].split(';')[0]} | {r[2].split(';')[1].strip()}" for r in rows
                                         if r[0].year <= 2024 and "normal" not in r[2]],
        "teyitli_kural_tarihleri": [str(d) for d in confirmed]}
    write_csv("eia_ng_storage.csv", rows, "2025-2026: resmî EIA takvimi (ir.eia.gov/ngs/schedule.html); 2016-2024: kural "
              "(resmî arşiv takvimi erişilemedi; web.archive.org engelli) + 6 tarihlik teyit")


def tr_time(d, et):
    m = re.match(r"(\d{1,2}):(\d{2}) ?([ap])\.?m", et)
    if not m:
        m2 = re.match(r"(\d{1,2}):(\d{2}) ET", et)
        if not m2:
            return "?"
        h, mi = int(m2.group(1)), int(m2.group(2))
    else:
        h, mi = int(m.group(1)) % 12 + (12 if m.group(3) == "p" else 0), int(m.group(2))
    h += 7 if is_dst(d) else 8
    return f"{h:02d}:{mi:02d}"


# ----------------------------------------------------------------------------------------
# 5) EIA WPSR
# ----------------------------------------------------------------------------------------
def build_wpsr():
    t = rd("www.eia.gov_petroleum_supply_weekly_archive.html")
    arch = sorted({D(int(y), int(m), int(d)) for y, m, d in
                   re.findall(r"archive/\d{4}/(\d{4})_(\d{2})_(\d{2})/", t)})
    sched_txt = [l.strip() for l in rd("www.eia.gov_petroleum_supply_weekly_schedule.php.txt").splitlines() if l.strip()]
    exc = {}
    for i, l in enumerate(sched_txt):
        m = re.match(r"^(\w+) (\d{1,2}), (\d{4})$", l)
        if m and m.group(1)[:3].lower() in MONTHS and i + 4 < len(sched_txt):
            m2 = re.match(r"^(\w+) (\d{1,2}), (\d{4})$", sched_txt[i + 1])
            if m2:
                wk = D(int(m.group(3)), MONTHS[m.group(1)[:3].lower()], int(m.group(2)))
                rel = D(int(m2.group(3)), MONTHS[m2.group(1)[:3].lower()], int(m2.group(2)))
                exc[rel] = (wk, sched_txt[i + 2], sched_txt[i + 3], sched_txt[i + 4])
    rows = []
    src_a = "https://www.eia.gov/petroleum/supply/weekly/archive/"
    src_s = "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    last = max(arch)
    for d in arch:
        if not in_range(d):
            continue
        det = f"{GUN[d.weekday()]}; arşivde yayım"
        if d in exc:
            det += f"; resmî istisna: {exc[d][1]} {exc[d][2]} ({exc[d][3]})"
        elif d.weekday() != 2:
            det += "; tatil kayması (arşivden)"
        tm = exc[d][2] if d in exc else ("10:30 a.m." if d.weekday() == 2 else "saat arşivde yok")
        det += f"; saat {tm}"
        rows.append((d, "EIA_WPSR", det, src_a + f"{d.year}/{d:%Y_%m_%d}/wpsr_{d:%Y_%m_%d}.php"))
    # gelecek: standart Çarşamba + takvim istisnaları
    d = last + dt.timedelta(days=1)
    while d <= END:
        if d.weekday() == 2:
            rel = d
            for r_, v in exc.items():
                if r_ > last and abs((r_ - d).days) <= 3:
                    rel = r_
            det = f"{GUN[rel.weekday()]}; GELECEK; " + (f"resmî istisna: {exc[rel][1]} {exc[rel][2]} ({exc[rel][3]})"
                                                     if rel in exc else "Çarşamba 10:30 ET; takvimde istisna yok")
            rows.append((rel, "EIA_WPSR", det, src_s))
        d += dt.timedelta(days=1)
    gaps = [(str(a), str(b)) for a, b in zip(arch, arch[1:]) if (b - a).days > 9 and a.year >= 2016]
    miss_exc = [str(r) for r in exc if r <= last and r not in arch]
    VERIFY["wpsr"] = {"arsiv_yayim_2016+": sum(1 for x in arch if x.year >= 2016), "son_arsiv": str(last),
                      "carsamba_disi": sum(1 for r in rows if r[0].weekday() != 2),
                      "atlanan_haftalar(>9 gun bosluk)": gaps, "takvim_istisnasi_arsivde_yok": miss_exc,
                      "ornek_istisnalar": [f"{r} {v[1]} {v[3]}" for r, v in list(exc.items())[:6]]}
    write_csv("eia_petroleum.csv", rows, "EIA WPSR arşiv sayfası (gerçekleşen yayım tarihleri, 2016-01..2026-11-04) + "
              "WPSR takvim sayfası (2026 kalan haftalar)")


# ----------------------------------------------------------------------------------------
# 6) Opsiyon vadesi
# ----------------------------------------------------------------------------------------
def build_opex():
    rows = []
    for y in range(2016, 2027):
        for m in range(1, 13):
            f3 = nth_wd(y, m, 4, 3)
            d = f3
            note = "3. Cuma"
            if not is_bd(d):
                d = prev_or_same_bd(d - dt.timedelta(days=1))
                note = f"3. Cuma ({f3}) borsa tatili ({NYSE_HOL.get(f3)}) -> {GUN[d.weekday()]}"
            q = m in (3, 6, 9, 12)
            ev = "OPEX_ceyrek_triple_witching" if q else "OPEX_aylik"
            det = f"{note}; {'çeyrek sonu (hisse/endeks opsiyon + vadeli, triple witching)' if q else 'aylık standart vade'}; "
            det += "SPX AM-uzlaşmalı seri bir önceki işlem gününde son işlem görür; kural"
            if y == 2026 and d > D(2026, 11, 7):
                det += "; GELECEK"
            rows.append((d, ev, det, "kural (OCC/Cboe: ayın 3. Cuması, tatilse önceki iş günü) ; tatiller: "
                         "https://www.cboe.com/about/hours/us-options/ (2026-2027), öncesi NYSE kuralı"))
    thu = [str(r[0]) for r in rows if r[0].weekday() != 4]
    VERIFY["opex"] = {"satir": len(rows), "cuma_disi": thu}
    write_csv("opex.csv", rows, "Kuraldan hesaplandı (3. Cuma; tatilse Perşembe). Cboe 2026 tatil listesi (19 Haz 2026 Juneteenth) ile tutarlı")


# ----------------------------------------------------------------------------------------
# 7) Vadeler: NG, CL (kural) + VIX (Cboe resmî liste)
# ----------------------------------------------------------------------------------------
def ng_expiry(cy, cm):
    """NG teslim ayı (cy,cm) son işlem: teslim ayının 1. gününden önceki 3. iş günü."""
    return add_bd(D(cy, cm, 1), -3, CME_HOL)


def cl_expiry(cy, cm):
    py, pm = (cy - 1, 12) if cm == 1 else (cy, cm - 1)
    d25 = D(py, pm, 25)
    if is_bd(d25, CME_HOL):
        return add_bd(d25, -3, CME_HOL), "25'i iş günü -> 3 iş günü önce"
    return add_bd(d25, -4, CME_HOL), "25'i iş günü değil -> 4 iş günü önce"


def parse_eia_fut(fn):
    t = rd(os.path.join("eia_futures", fn))
    out = {}
    for m in re.finditer(r"<td class='B6'>(?:&nbsp;)*(\d{4}) (\w{3})-\s?(\d{1,2}) to \w{3}-\s?\d{1,2}</td>((?:\s*<td class='B3'>[^<]*</td>){5})", t):
        y, mon, day = int(m.group(1)), MONTHS[m.group(2).lower()], int(m.group(3))
        start = D(y, mon, day)
        vals = re.findall(r"<td class='B3'>([^<]*)</td>", m.group(4))
        for k, v in enumerate(vals):
            v = v.strip().replace(",", "")
            if v:
                out[start + dt.timedelta(days=k)] = float(v)
    return out


def switch_check(e, cs):
    """EIA Contract 1..4 günlük fiyatlarıyla vade (kontrat geçişi) günü kontrolü.
    Geçiş olmayan günde Ck(n)/Ck(t) getirileri birbirine yakın; geçiş gününde (t=son işlem
    günü, n=ertesi gün) Ck(n)/Ck+1(t) getirileri yakın olur. Pencere: E-3..E+3 iş günü."""
    c1 = cs[0]
    days = sorted(d for d in c1 if all(d in c for c in cs[:3]))
    if not days or e < days[0] or e >= days[-1]:
        return "veri yok"
    if e not in days:
        return "veri yok (gün yok)"
    i0 = days.index(e)
    sc = {}
    for i in range(max(0, i0 - 3), min(len(days) - 1, i0 + 4)):
        t, n = days[i], days[i + 1]
        av = [c for c in cs if t in c and n in c]
        ns = [c[n] / c[t] for c in av]
        sw = [av[k][n] / av[k + 1][t] for k in range(len(av) - 1)]
        sc[t] = (max(sw) - min(sw)) - (max(ns) - min(ns))
    best = min(sc, key=sc.get)
    vals = sorted(sc.values())
    margin = vals[1] - vals[0] if len(vals) > 1 else 0
    if best == e and sc[e] < 0:
        return "uyumlu" if margin > 0.003 else "uyumlu (zayıf)"
    if sc[best] > -0.003 or margin < 0.003:
        return f"belirsiz (en iyi aday {best})"
    return f"UYUMSUZ (veri {best} gösteriyor)"


def build_vadeler():
    rows = []
    ngs = [parse_eia_fut(f"rngc{k}d.htm") for k in range(1, 5)]
    cls = [parse_eia_fut(f"RCLC{k}D.htm") for k in range(1, 5)]
    res = {"NG": Counter(), "CL": Counter()}; bad = []
    for cy in range(2016, 2028):
        for cm in range(1, 13):
            code = f"{MCODE[cm - 1]}{cy % 100:02d}"
            e = ng_expiry(cy, cm)
            if in_range(e):
                chk = switch_check(e, ngs)
                res["NG"][chk.split(" (")[0]] += 1
                if chk.startswith(("UYUMSUZ", "belirsiz")):
                    bad.append(("NG" + code, str(e), chk))
                rows.append((e, "NG_vade", f"NG{code} ({TR_AY[cm]} {cy} teslim) son işlem; kural: teslim ayının 1. gününden "
                             f"önceki 3. iş günü; EIA C1-C4 geçiş kontrolü: {chk}",
                             "kural (CME NG şartnamesi; EIA tanımı https://www.eia.gov/dnav/ng/TblDefs/ng_pri_fut_tbldef2.asp) ; "
                             "kontrol: https://www.eia.gov/dnav/ng/hist/rngc1d.htm (..rngc4d)"))
            e, why = cl_expiry(cy, cm)
            if in_range(e):
                chk = switch_check(e, cls)
                res["CL"][chk.split(" (")[0]] += 1
                if chk.startswith(("UYUMSUZ", "belirsiz")):
                    bad.append(("CL" + code, str(e), chk))
                rows.append((e, "CL_vade", f"CL{code} ({TR_AY[cm]} {cy} teslim) son işlem; kural: {why}; EIA C1-C4 geçiş kontrolü: {chk}",
                             "kural (CME CL şartnamesi; EIA tanımı https://www.eia.gov/dnav/pet/TblDefs/pet_pri_fut_tbldef2.asp) ; "
                             "kontrol: https://www.eia.gov/dnav/pet/hist/RCLC1D.htm (..RCLC4D)"))
    # İkincil kaynak çapraz kontrolü (TradingView kontrat listesi; 2026-11..2029 vadeleri)
    tvc = {"eslesen": 0, "farkli": []}; tv_ok = set()
    for l in rd(os.path.join("webfetch", "tradingview_ng_cl_contracts.txt")).splitlines():
        m = re.match(r"^(NG|CL)([FGHJKMNQUVXZ])(\d{4}) (\d{4}-\d{2}-\d{2})$", l.strip())
        if not m:
            continue
        cy, cm = int(m.group(3)), MCODE.index(m.group(2)) + 1
        mine = ng_expiry(cy, cm) if m.group(1) == "NG" else cl_expiry(cy, cm)[0]
        tv = D(*map(int, m.group(4).split("-")))
        if mine == tv:
            tvc["eslesen"] += 1
            tv_ok.add(f"{m.group(1)}{m.group(2)}{cy % 100:02d}")
        else:
            tvc["farkli"].append(f"{l.strip()} kural={mine}")
    VERIFY["vadeler_tradingview_capraz"] = tvc
    manual = {
        "NGH16": "elle inceleme: 25 Şub 2016'da C1 diğer vadelerden ayrışarak -%3.8 (vade günü yakınsaması); eğri düz olduğundan otomatik test yanılıyor; kural esas",
        "CLN18": "elle inceleme: eğri çok düz (C1-C4 farkı <%2), test ayırt edemiyor; kural esas",
        "CLK20": "20 Nis 2020 negatif fiyat günü (C1 -37$) testi bozuyor; CLK20 son işlem 21 Nis 2020 (kural)",
        "NGH24": "elle inceleme: 27 Şub 2024 C1=1.615 (vade günü), 28 Şub C1=1.885 ≈ 27 Şub C2 x1.04 ve C2..C4 aynı yönde +%4 -> geçiş 27->28, kural doğru; otomatik test vade günü sapması yüzünden yanıldı",
    }
    for i, r in enumerate(rows):
        code = r[2].split(" ")[0]
        if code in manual:
            rows[i] = (r[0], r[1], r[2] + "; " + manual[code], r[3])
        if code in tv_ok:
            rows[i] = (rows[i][0], rows[i][1], rows[i][2] + "; TradingView kontrat listesiyle AYNI (ikincil kaynak)",
                       rows[i][3] + " ; https://www.tradingview.com/symbols/NYMEX-" + code[:2] + "1%21/contracts")
    # VIX
    js = json.loads(rd(os.path.join("cboe", "vx_product_list.json")))
    vx = []
    for yr, lst in js.items():
        for it in lst:
            if it.get("duration_type") == "M":
                vx.append((D(*map(int, it["expire_date"].split("-"))), it["product_display"]))
    vx = sorted(set(vx))
    vmis = []
    for d, disp in vx:
        if not in_range(d):
            continue
        # kural: sonraki ayın 3. Cuması - 30 gün (Cuma tatilse önceki iş günü - 30; Çarşamba tatilse önceki iş günü)
        y2, m2 = (d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1)
        # kontrat ayı = uzlaşma ayı (VIX vadelileri ay içi uzlaşır)
        f3 = nth_wd(y2, m2, 4, 3)
        base = f3 if is_bd(f3) else prev_or_same_bd(f3 - dt.timedelta(days=1))
        rule = base - dt.timedelta(days=30)
        if not is_bd(rule):
            rule = prev_or_same_bd(rule - dt.timedelta(days=1))
        ok = "kural ile uyumlu" if rule == d else f"KURAL FARKLI ({rule})"
        if rule != d:
            vmis.append((str(d), str(rule)))
        rows.append((d, "VIX_vade", f"{disp.split('/')[-1]} aylık VX kontratı nihai uzlaşma günü ({GUN[d.weekday()]}); "
                     f"vadesi gelen kontratta işlem bu sabah 08:00 CT'de biter (SOQ açılış uzlaşması); {ok}",
                     "Cboe resmî liste: https://www.cboe.com/us/futures/market_statistics/historical_data/product/list/VX/ ; "
                     "kural: Cboe VX şartnamesi / 2026 opsiyon takvimi notu"))
    VERIFY["vadeler"] = {"NG_kontrol": dict(res["NG"]), "CL_kontrol": dict(res["CL"]), "sorunlu": bad,
                         "VIX_resmi_sayi": sum(1 for d, _ in vx if in_range(d)), "VIX_kural_farki": vmis,
                         "EIA_veri_son_gun": {"NG": str(max(ngs[0])), "CL": str(max(cls[0]))}}
    write_csv("vadeler.csv", rows, "NG/CL: kuraldan (CME tatili ~ NYSE düzenli tatilleri) + EIA günlük C1/C2 fiyat geçişiyle "
              "2016-2024 kontrol; VIX: Cboe resmî ürün listesi + kural karşılaştırması")
    return {(r[1], r[0]) for r in rows}


# ----------------------------------------------------------------------------------------
# 8) UNG / USO / BOIL-KOLD roll pencereleri
# ----------------------------------------------------------------------------------------
def build_rolls():
    rows = []
    q = "ham_sayfalar/takvim/webfetch/sec_uscf_roll_alintilar.txt"
    # UNG
    for cy in range(2016, 2028):
        for cm in range(1, 13):
            e = ng_expiry(cy, cm)
            if not (D(2016, 1, 1) <= e <= D(2027, 1, 20)):
                continue
            s0 = e - dt.timedelta(days=14)
            s = prev_or_same_bd(s0)
            win = [s] + [add_bd(s, k) for k in range(1, 4)]
            nxt = (cy + (cm == 12), cm % 12 + 1)
            c_from = f"NG{MCODE[cm - 1]}{cy % 100:02d}"; c_to = f"NG{MCODE[nxt[1] - 1]}{nxt[0] % 100:02d}"
            for k, d in enumerate(win, 1):
                if in_range(d):
                    rows.append((d, "UNG_roll", f"gün {k}/4 (benchmark %{25 * k} yeni kontrat, gün sonu); {c_from}->{c_to}; "
                                 f"pencere {win[0]}..{win[-1]}; ön ay vadesi {e}; başlangıç = vade-14 takvim günü"
                                 f"{' (tatil/hafta sonu -> önceki iş günü, VARSAYIM)' if s != s0 else ''}; kural"
                                 f"{'; GELECEK' if d > D(2026, 11, 7) else ''}",
                                 "UNG 10-K FY2025 https://www.sec.gov/Archives/edgar/data/1376227/000110465926021507/ung-20251231x10k.htm ; " + q))
    # USO
    for cy in range(2016, 2028):
        for cm in range(1, 13):
            e, _ = cl_expiry(cy, cm)
            if not (D(2016, 1, 1) <= e <= D(2020, 4, 30)):
                continue
            s0 = e - dt.timedelta(days=14); s = prev_or_same_bd(s0)
            win = [s] + [add_bd(s, k) for k in range(1, 4)]
            nxt = (cy + (cm == 12), cm % 12 + 1)
            c_from = f"CL{MCODE[cm - 1]}{cy % 100:02d}"; c_to = f"CL{MCODE[nxt[1] - 1]}{nxt[0] % 100:02d}"
            for k, d in enumerate(win, 1):
                if in_range(d):
                    det = (f"gün {k}/4; {c_from}->{c_to}; pencere {win[0]}..{win[-1]}; ön ay vadesi {e}; "
                           f"2020 öncesi kural (UNG ile aynı: vadeden 2 hafta önce başlayan 4 gün)")
                    if d.year == 2020 and d.month == 4:
                        det += "; NİSAN 2020: olağan roll + 16-28 Nisan arası portföyün çok vadeye yayılması (ayrıntılı tarih bulunamadı)"
                    rows.append((d, "USO_roll", det, "USO 10-K FY2016/FY2019 (sec.gov) ; " + q))
    for y in range(2020, 2027):
        for m in range(1, 13):
            if (y, m) < (2020, 5):
                continue
            n = 5 if y >= 2026 else 10
            bds = bdays_of_month(y, m)[:n]
            if (y, m) <= (2023, 8):
                ph = "2020-05..2023-08: çok vadeli portföy (yalnız ön ay değil) aylık yeniden dengeleme"
            elif (y, m) <= (2024, 1):
                ph = "2023-09..2024-01 ön aya geri geçiş dönemi"
            else:
                ph = "ön ay -> sonraki ay (benchmark)"
            near = (y + (m == 12), m % 12 + 1); nxt = (near[0] + (near[1] == 12), near[1] % 12 + 1)
            cc = f"CL{MCODE[near[1] - 1]}{near[0] % 100:02d}->CL{MCODE[nxt[1] - 1]}{nxt[0] % 100:02d}"
            for k, d in enumerate(bds, 1):
                rows.append((d, "USO_roll", f"gün {k}/{n}; ayın ilk {n} iş günü; {cc if not ph.startswith('2020-05') else 'çok vadeli'}; {ph}; "
                             f"{'2026-01den itibaren 5 gün' if n == 5 else '2020-05..2025-12 10 gün'}; kural"
                             f"{'; GELECEK' if d > D(2026, 11, 7) else ''}",
                             "USO 10-K FY2025 https://www.sec.gov/Archives/edgar/data/1327068/000110465926021501/uso-20251231x10k.htm ; "
                             "USO 424B3 2025-11 https://www.sec.gov/Archives/edgar/data/1327068/000207187625000081/i25397_uso-424b3.htm ; " + q))
    # BOIL/KOLD (Bloomberg Natural Gas Subindex): Şub/Nis/Haz/Ağu/Eki/Ara, 6.-10. iş günü
    lead = {1: 3, 2: 3, 3: 5, 4: 5, 5: 7, 6: 7, 7: 9, 8: 9, 9: 11, 10: 11, 11: 1, 12: 1}
    for y in range(2016, 2027):
        for m in range(1, 13):
            l1, l2 = lead[m], lead[m % 12 + 1]
            if l1 == l2:
                continue
            y1 = y + (l1 < m)
            nm, ny = m % 12 + 1, y + (m == 12)
            y2 = ny + (l2 < nm)
            c_from = f"NG{MCODE[l1 - 1]}{y1 % 100:02d}"; c_to = f"NG{MCODE[l2 - 1]}{y2 % 100:02d}"
            bds = bdays_of_month(y, m)[5:10]
            for k, d in enumerate(bds, 1):
                rows.append((d, "BOIL_KOLD_roll", f"gün {k}/5 (%20/gün); {c_from}->{c_to}; ayın 6.-10. iş günü; BCOM NG takvimi "
                             f"(yalnız Şub/Nis/Haz/Ağu/Eki/Ara roll var); iş günü ~NYSE; kural{'; GELECEK' if d > D(2026, 11, 7) else ''}",
                             "ProShares BOIL sayfası https://www.proshares.com/our-etfs/leveraged-and-inverse/boil ; "
                             "BCOM metodoloji Table 9 https://assets.bbhub.io/professional/sites/10/BCOM-Methodology.pdf"))
    cnt = Counter(r[1] for r in rows)
    VERIFY["roll"] = {"satir": dict(cnt),
                      "ornek_UNG_2026_11": [f"{r[0]} {r[2][:60]}" for r in rows if r[1] == "UNG_roll" and r[0].year == 2026 and r[0].month in (11, 12)],
                      "ornek_BOIL_2026_12": [f"{r[0]} {r[2][:40]}" for r in rows if r[1] == "BOIL_KOLD_roll" and r[0] >= D(2026, 12, 1)],
                      "ornek_USO_2026_11": [f"{r[0]} {r[2][:40]}" for r in rows if r[1] == "USO_roll" and r[0].year == 2026 and r[0].month == 11]}
    write_csv("ung_uso_roll.csv", rows, "Tamamı kuraldan hesaplandı (USCF/ProShares/Bloomberg belgelerindeki kurallar); "
              "USCF'nin yayımladığı roll CSV'sine erişilemedi")


# ----------------------------------------------------------------------------------------
# 9) Hazine 10Y/30Y ihaleleri
# ----------------------------------------------------------------------------------------
def build_treasury():
    rows = []
    js = json.loads(rd(os.path.join("treasury", "auctions_10y30y.json")))
    src = ("https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query"
           "?filter=original_security_term:in:(10-Year,30-Year)")
    seen = set()
    months = set(); dropped = []
    for r in sorted(js["data"], key=lambda x: x["auction_date"]):
        d = D(*map(int, r["auction_date"].split("-")))
        if not in_range(d):
            continue
        if r.get("inflation_index_security") != "No" or r["security_term"].split("-")[0] not in ("10", "9", "30", "29"):
            continue  # TIPS ve eski kağıt yeniden ihraçları (ör. 3-Year) hariç
        ev = "UST10Y_ihale" if r["original_security_term"] == "10-Year" else "UST30Y_ihale"
        key = (d, ev)
        if key in seen:
            continue
        if (d.year, d.month, ev) in months:
            dropped.append(f"{d} {ev} {r['security_term']} {r['cusip']}")
            continue
        months.add((d.year, d.month, ev))
        seen.add(key)
        rows.append((d, ev, f"{r['security_type']} {r['security_term']}; {'reopening' if r['reopening'] == 'Yes' else 'yeni ihraç'}; "
                     f"CUSIP {r['cusip']}; rekabetçi teklif kapanışı {r['closing_time_comp']} ET (TR {tr_time(d, r['closing_time_comp'].lower().replace(' pm', ' p.m.').replace(' am', ' a.m.'))}); gerçekleşen",
                     src))
    tent = rd(os.path.join("treasury", "tentative.txt"))
    for m in re.finditer(r"^(10-Year NOTE|30-Year BOND)\s+(R?)\s+\w{3}, (\w{3}) (\d{2}), (\d{4})\s+\w{3}, (\w{3}) (\d{2}), (\d{4})", tent, re.M):
        d = D(int(m.group(8)), MONTHS[m.group(6).lower()], int(m.group(7)))
        ev = "UST10Y_ihale" if m.group(1).startswith("10") else "UST30Y_ihale"
        if in_range(d) and (d, ev) not in seen:
            seen.add((d, ev))
            rows.append((d, ev, f"{m.group(1)}; {'reopening' if m.group(2) else 'yeni ihraç'}; duyuru {m.group(5)}-{m.group(3)}-{m.group(4)}; "
                         f"13:00 ET (TR {tr_time(d, '1:00 p.m.')}); GELECEK (geçici takvim)",
                         "https://home.treasury.gov/system/files/221/Tentative-Auction-Schedule.pdf ; "
                         "https://www.treasurydirect.gov/TA_WS/securities/upcoming?format=json"))
    c = Counter((r[0].year, r[1]) for r in rows)
    VERIFY["hazine_ayni_ay_ikinci_kayit_cikarildi"] = dropped
    VERIFY["hazine"] = {"yil_ihale": {f"{y}": f"10Y={c[(y, 'UST10Y_ihale')]}, 30Y={c[(y, 'UST30Y_ihale')]}" for y in range(2016, 2027)}}
    write_csv("hazine_ihale_10y30y.csv", rows, "fiscaldata.treasury.gov auctions_query (gerçekleşen, 2016-01..2026-10) + "
              "Hazine geçici ihale takvimi PDF (Kasım-Aralık 2026)")


def main():
    os.makedirs(OUT, exist_ok=True)
    build_nyse()
    build_fomc()
    build_bls()
    build_ng_storage()
    build_wpsr()
    build_opex()
    build_vadeler()
    build_rolls()
    build_treasury()
    with open(os.path.join(OUT, "_dogrulama.json"), "w", encoding="utf-8") as f:
        json.dump(VERIFY, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: v for k, v in VERIFY.items() if k != "kaynak_notlari"}, ensure_ascii=False, indent=1, default=str)[:20000])


if __name__ == "__main__":
    main()
