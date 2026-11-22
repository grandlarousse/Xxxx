"""Planlı FOMC karar günleri 2010-2026 -> veri/fomc.csv (karar_gunu = toplantının son günü).

Kaynak: federalreserve.gov/monetarypolicy/fomchistorical<YIL>.htm (2010-2020) ve fomccalendars.htm
(2021-2026). Yalnız "Meeting" satırları alınır; "Conference Call", "(unscheduled)" ve "notation vote"
olağanüstü sayılıp atılır. 2020 Mart: planlı 17-18 Mart toplantısı yapılmadı (15 Mart olağanüstü) -> 7 karar.
Kullanım: python kod/fomc_indir.py [html_klasoru]   (klasör verilirse indirilmiş sayfalar kullanılır)
"""
import re, sys
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "veri" / "fomc.csv"
AY = "January|February|March|April|May|June|July|August|September|October|November|December"
KISA = {a[:3]: a for a in AY.split("|")}
URL_H = "https://www.federalreserve.gov/monetarypolicy/fomchistorical{}.htm"
URL_C = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"


def oku(ad, url, klasor):
    if klasor and (Path(klasor) / ad).exists():
        return (Path(klasor) / ad).read_text(errors="ignore")
    import requests
    return requests.get(url, timeout=60).text


def ay_adi(s):
    s = s.split("/")[-1].strip()
    return KISA.get(s[:3], s)


def main():
    klasor = sys.argv[1] if len(sys.argv) > 1 else None
    rows = []
    for y in range(2010, 2021):
        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", oku(f"h{y}.htm", URL_H.format(y), klasor)))
        desen = rf"((?:{AY}|[A-Z][a-z]{{2}}/[A-Z][a-z]{{2}}))\s+(\d{{1,2}})(?:-(?:({AY})\s+)?(\d{{1,2}}))?\s+(Meeting|Conference Call)"
        for m in re.finditer(desen, t):
            if m.group(5) != "Meeting":
                continue
            ay = ay_adi(m.group(3) or m.group(1))
            rows.append((y, pd.Timestamp(f"{ay} {m.group(4) or m.group(2)} {y}"), m.group(0)))
    s = oku("cal.htm", URL_C, klasor)
    for y in range(2021, 2027):
        i = s.find(f"{y} FOMC Meetings")
        j = s.find("FOMC Meetings", i + 20)
        seg = s[i:j if j > 0 else None]
        for m in re.finditer(r"fomc-meeting__month[^>]*>\s*<strong>([^<]+)</strong>.*?fomc-meeting__date[^>]*>([^<]+)<", seg, re.S):
            ay, d = m.group(1).strip(), m.group(2).strip()
            if "unscheduled" in d.lower() or "notation" in d.lower():
                continue
            rows.append((y, pd.Timestamp(f"{ay_adi(ay)} {re.findall(r'[0-9]+', d)[-1]} {y}"), f"{ay} {d}"))
    df = pd.DataFrame(rows, columns=["yil", "karar_gunu", "kaynak_metin"])
    df = df.drop_duplicates("karar_gunu").sort_values("karar_gunu").reset_index(drop=True)
    df.to_csv(OUT, index=False)
    print(df.groupby("yil").size().to_dict(), len(df))


if __name__ == "__main__":
    main()
