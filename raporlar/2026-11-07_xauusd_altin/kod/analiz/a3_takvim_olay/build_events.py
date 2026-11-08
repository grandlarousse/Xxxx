"""a3_takvim_olay — olay takvimlerini kurar ve out/a3_takvim_olay/events_*.csv olarak yazar.
Kaynaklar (yerel kopyalar dl/ altında; yeniden indirmek için --download):
  FOMC 2010-2020: federalreserve.gov/monetarypolicy/fomchistorical<YIL>.htm ; 2021-2027: data/misc/fomc_calendar.html
  CPI / NFP: bls.gov/bls/news-release/cpi.htm ve empsit.htm (arşiv bağlantılarındaki MMDDYYYY gerçek yayım tarihidir)
  Tatiller: python 'holidays' paketi (pylib/), NYSE, XLON (LSE), XSHG (Şanghay), Türkiye; VİOP kapanışları panelden.
  COMEX OG opsiyon vadesi: CME kuralı 'opsiyon ayından önceki ayın SONDAN 4. iş günü; Cuma ya da tatil arifesine denk gelirse bir önceki iş günü'
      (doğrulama: OGZ25=24.11.2025, OGG26=27.01.2026, OGJ25=26.03.2025, OGM25=27.05.2025, OGV25=25.09.2025 bu kuralla tutuyor).
      Görev metnindeki 'son iş gününden 4 iş günü önce' tanımı da duyarlılık için ayrı sütun (og_alt) olarak yazılır.
  GC ilk bildirim günü (FND) = teslim ayından önceki ayın son iş günü (G,J,M,Q,V,Z). BCOM roll = Ocak/Mart/Mayıs/Temmuz/Kasım 6.–10. iş günleri.
  Çin Yeni Yılı, Diwali (holidays.India), Dhanteras = Diwali-2 takvim günü, Akshaya Tritiya (2021-2026 drikpanchang ile doğrulandı; 2010-2020 bellekten),
  Türkiye bayramları (holidays.Turkey; arife = bayramdan önceki gün).
"""
import os, re, sys, html, glob, subprocess
import numpy as np, pandas as pd
O = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, f"{O}/pylib")
S = os.path.abspath(f"{O}/../..")
import holidays

DL = f"{O}/dl"
AB = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
MON = {m: i for i, m in enumerate(["january","february","march","april","may","june","july","august","september","october","november","december"], 1)}

def fomc():
    rows = []
    for y in range(2009, 2021):
        t = open(f"{DL}/fomc_{y}.htm", encoding="utf-8", errors="ignore").read()
        for h in re.findall(r"<h5[^>]*>(.*?)</h5>", t, flags=re.S):
            h = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()
            if "Meeting" not in h: continue
            unsched = "unscheduled" in h.lower(); canc = "cancel" in h.lower()
            if canc: continue
            m = re.match(r"([A-Za-z/]+)\s+(\d+)(?:-(\d+))?", h)
            if not m: continue
            mo2 = AB[m.group(1).split("/")[-1].lower()[:3]]; d2 = int(m.group(3) or m.group(2))
            rows.append(dict(date=pd.Timestamp(y, mo2, d2), scheduled=not unsched, label=h))
    t = open(f"{S}/data/misc/fomc_calendar.html", encoding="utf-8", errors="ignore").read()
    parts = re.split(r"(\d{4}) FOMC Meetings", t)
    for i in range(1, len(parts), 2):
        y = int(parts[i]); b = parts[i + 1]
        if y < 2021: continue
        mos = re.findall(r"fomc-meeting__month[^>]*>\s*<strong>(.*?)</strong>", b, flags=re.S)
        dys = re.findall(r"fomc-meeting__date[^>]*>(.*?)</div>", b, flags=re.S)
        for mo, dy in zip(mos, dys):
            mo = re.sub(r"\s+", " ", mo).strip(); dy = re.sub(r"<[^>]+>|\s+", " ", dy).strip()
            if "notation" in dy or "unscheduled" in dy.lower(): continue
            m2 = mo.split("/")[-1]; dd = int(re.findall(r"\d+", dy)[-1])
            mm = MON.get(m2.lower()) or {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}[m2.lower()[:3]]
            rows.append(dict(date=pd.Timestamp(y, mm, dd), scheduled=True, label=f"{mo} {dy} {y}"))
    f = pd.DataFrame(rows).drop_duplicates("date").sort_values("date")
    # açıklama saati: 2013+ 14:00 ET; 2011-2012 basın toplantılı 12:30 ET; diğer 14:15 ET. Hepsi VİOP uzlaşmasından (15:10 UTC) SONRA.
    def et_to_utc(d, hh, mm):
        return (pd.Timestamp(d.year, d.month, d.day, hh, mm).tz_localize("America/New_York").tz_convert("UTC")).strftime("%H:%M")
    f["announce_utc"] = [et_to_utc(d, 14, 0) if d.year >= 2013 else et_to_utc(d, 14, 15) for d in f.date]
    f.loc[f.label.str.contains("March 3|March 2 \\(unscheduled", regex=True) & (f.date.dt.year == 2020), "announce_utc"] = "15:00"
    f.loc[(f.date == "2020-03-15"), "announce_utc"] = "21:00 (Pazar)"
    f["note"] = np.where(f.scheduled, "", "plansız (sinyalde kullanılmaz)")
    return f

def bls(kind):
    t = open(f"{DL}/bls_{kind}.htm", encoding="utf-8", errors="ignore").read()
    ds = sorted(set(re.findall(rf"archives/{kind}_(\d{{8}})\.htm", t)))
    d = pd.to_datetime(ds, format="%m%d%Y"); d = d[(d.year >= 2009)]
    f = pd.DataFrame(dict(date=sorted(d)))
    f["release_utc"] = [(pd.Timestamp(x.year, x.month, x.day, 8, 30).tz_localize("America/New_York").tz_convert("UTC")).strftime("%H:%M") for x in f.date]
    return f

def bdays(cal_hol, start="2008-12-01", end="2027-12-31"):
    return pd.bdate_range(start, end, freq="C", holidays=sorted(cal_hol))

def comex():
    yrs = range(2008, 2028)
    cme_hol = set(pd.Timestamp(d) for d in holidays.financial_holidays("NYSE", years=yrs).keys())
    bd = bdays(cme_hol); bds = pd.Series(bd, index=bd)
    rows = []
    for y in range(2009, 2027):
        for m in range(1, 13):
            mb = bd[(bd.year == y) & (bd.month == m)]
            if len(mb) < 6: continue
            og = mb[-4]                                   # sondan 4. iş günü
            if og.dayofweek == 4 or (og + pd.Timedelta(days=1)) in cme_hol:   # Cuma ya da tatil arifesi -> bir önceki iş günü
                og = bd[bd < og][-1]
            alt = mb[-5]                                  # 'son iş gününden 4 iş günü önce'
            if alt.dayofweek == 4 or (alt + pd.Timedelta(days=1)) in cme_hol: alt = bd[bd < alt][-1]
            cm = m % 12 + 1; cy = y + (m == 12)          # opsiyon kontrat ayı (bir sonraki ay)
            fnd = mb[-1] if cm in (2, 4, 6, 8, 10, 12) else pd.NaT   # GC ilk bildirim günü (aktif ay öncesi ayın son iş günü)
            bcom = mb[5:10] if m in (1, 3, 5, 7, 11) else []
            rows.append(dict(month=f"{y}-{m:02d}", og_expiry=og, og_alt=alt, opt_contract=f"{cy}-{cm:02d}", gc_fnd=fnd,
                             bcom_roll_start=bcom[0] if len(bcom) else pd.NaT, bcom_roll_end=bcom[-1] if len(bcom) else pd.NaT))
    return pd.DataFrame(rows)

def hol():
    yrs = range(2009, 2028); out = []
    for mk, cal in [("NYSE", holidays.financial_holidays("NYSE", years=yrs)), ("LSE", holidays.financial_holidays("XLON", years=yrs)),
                    ("SSE", holidays.financial_holidays("XSHG", years=yrs)), ("TR", holidays.Turkey(years=yrs))]:
        for d, n in sorted(cal.items()):
            out.append(dict(market=mk, date=pd.Timestamp(d), name=n))
    return pd.DataFrame(out)

def asia():
    cny = ["2009-01-26","2010-02-14","2011-02-03","2012-01-23","2013-02-10","2014-01-31","2015-02-19","2016-02-08","2017-01-28","2018-02-16",
           "2019-02-05","2020-01-25","2021-02-12","2022-02-01","2023-01-22","2024-02-10","2025-01-29","2026-02-17"]
    ak = {2009:"2009-04-27",2010:"2010-05-16",2011:"2011-05-06",2012:"2012-04-24",2013:"2013-05-13",2014:"2014-05-02",2015:"2015-04-21",2016:"2016-05-09",
          2017:"2017-04-28",2018:"2018-04-18",2019:"2019-05-07",2020:"2020-04-26",2021:"2021-05-14",2022:"2022-05-03",2023:"2023-04-22",
          2024:"2024-05-10",2025:"2025-04-30",2026:"2026-04-19"}
    ind = holidays.India(years=range(2009, 2027))
    dw = sorted(pd.Timestamp(d) for d, n in ind.items() if n.startswith("Diwali"))
    rows = [dict(event="CNY", date=pd.Timestamp(x), src="ay takvimi") for x in cny]
    rows += [dict(event="GOLDEN_WEEK", date=pd.Timestamp(y, 10, 1), src="sabit 1 Ekim") for y in range(2009, 2027)]
    rows += [dict(event="DIWALI", date=d, src="holidays.India") for d in dw]
    rows += [dict(event="DHANTERAS", date=d - pd.Timedelta(days=2), src="Diwali-2 gün (yaklaşık)") for d in dw]
    rows += [dict(event="AKSHAYA", date=pd.Timestamp(v), src="drikpanchang" if y >= 2021 else "bellek") for y, v in ak.items()]
    return pd.DataFrame(rows).sort_values(["event", "date"])

def tr_bayram():
    tr = holidays.Turkey(years=range(2009, 2027)); rows = []
    for nm in ["Ramazan Bayramı", "Kurban Bayramı"]:
        ds = sorted(pd.Timestamp(d) for d, n in tr.items() if n == nm)
        starts = [d for i, d in enumerate(ds) if i == 0 or (d - ds[i - 1]).days > 1]
        for s in starts:
            ln = sum(1 for d in ds if 0 <= (d - s).days < 6)
            rows.append(dict(bayram=nm, start=s, arife=s - pd.Timedelta(days=1), days=ln))
    return pd.DataFrame(rows).sort_values("start")

if __name__ == "__main__":
    if "--download" in sys.argv:
        A = "Mozilla/5.0 (research)"
        for k in ["cpi", "empsit"]: subprocess.run(["curl", "-sS", "-A", A, "-o", f"{DL}/bls_{k}.htm", f"https://www.bls.gov/bls/news-release/{k}.htm"])
        for y in range(2009, 2021): subprocess.run(["curl", "-sS", "-A", A, "-o", f"{DL}/fomc_{y}.htm", f"https://www.federalreserve.gov/monetarypolicy/fomchistorical{y}.htm"])
    f = fomc(); f.to_csv(f"{O}/events_fomc.csv", index=False)
    c = bls("cpi"); c.to_csv(f"{O}/events_us_cpi.csv", index=False)
    n = bls("empsit"); n.to_csv(f"{O}/events_us_nfp.csv", index=False)
    cx = comex(); cx.to_csv(f"{O}/events_comex.csv", index=False)
    h = hol(); h.to_csv(f"{O}/events_tatiller.csv", index=False)
    a = asia(); a.to_csv(f"{O}/events_asya_festival.csv", index=False)
    b = tr_bayram(); b.to_csv(f"{O}/events_tr_bayram.csv", index=False)
    print("FOMC", len(f), f.scheduled.sum(), f.date.min().date(), f.date.max().date())
    print(f.groupby(f.date.dt.year).size().to_dict())
    print("CPI", len(c), c.groupby(c.date.dt.year).size().to_dict()); print("NFP", len(n), n.groupby(n.date.dt.year).size().to_dict())
    print(cx.tail(14)); print(b.tail(6)); print(a[a.event == "DIWALI"].tail(4))
