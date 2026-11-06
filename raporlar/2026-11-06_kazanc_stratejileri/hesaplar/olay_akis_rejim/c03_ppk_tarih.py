"""TCMB PPK karar tarihleri (2010-2026): https://www.tcmb.gov.tr/.../Para+Politikasi/PPK/<yil> tablosunun ilk sutunu.
Varsayilan basliklar, tek tek, 1.5 sn. Cikti: tcmb/ppk_tarihleri.csv (karar_tarihi). Politika faizi seviyesi: TCMB '1 Hafta Repo' tablosu
(kardes ajanin indirdigi sayfa) yururluk tarihleri -> karar tarihi = yururlukten onceki islem gunu."""
import os, re, time, requests, pandas as pd
import ortak as O
RAW = O.MY + "/tcmb_raw/ppk"; os.makedirs(RAW, exist_ok=True)
AY = {"Ocak": 1, "Şubat": 2, "Mart": 3, "Nisan": 4, "Mayıs": 5, "Haziran": 6, "Temmuz": 7, "Ağustos": 8, "Eylül": 9, "Ekim": 10, "Kasım": 11, "Aralık": 12}
S = requests.Session(); rows = []
for y in range(2010, 2027):
    f = f"{RAW}/{y}.html"
    if not os.path.exists(f):
        u = f"https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/PPK/{y}"
        r = S.get(u, timeout=60); open(f, "w").write(r.text); time.sleep(1.5)
    t = open(f, encoding="utf8", errors="ignore").read().replace("&nbsp;", " ")
    if y <= 2014:
        for m in re.finditer(r"(\d{1,2}) (Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık) (20\d\d)", t):
            if int(m.group(3)) == y: rows.append(pd.Timestamp(y, AY[m.group(2)], int(m.group(1))))
        continue
    for tr in re.findall(r"<tr>(.*?)</tr>", t, flags=re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)
        if not tds: continue
        txt = re.sub(r"<[^>]+>", " ", tds[0]); txt = re.sub(r"\s+", " ", txt).strip()
        m = re.search(r"(\d{1,2}) ([A-Za-zÇŞĞÜÖİçşğüöı]+) (20\d\d)", txt)
        if m and m.group(2) in AY: rows.append(pd.Timestamp(int(m.group(3)), AY[m.group(2)], int(m.group(1))))
P = pd.Series(sorted(set(rows)), name="karar").to_frame()
P = P[(P.karar >= "2010-01-01") & (P.karar <= "2026-11-06")]
P.to_csv(O.MY + "/tcmb/ppk_tarihleri.csv", index=False)
print(len(P)); print(P.groupby(P.karar.dt.year).size().to_dict()); print(P.tail(8).to_string())
