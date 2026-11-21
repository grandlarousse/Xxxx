"""federalreserve.gov FOMC takvimlerinden 2005-2026 toplanti tablosu. Kullanim: python3 -I fomc_kur.py <html_dizin>
html_dizin: cal.htm (fomccalendars.htm) ve h<yil>.htm (fomchistorical<yil>.htm, 2005-2020)."""
import sys, os, re
import pandas as pd
from bs4 import BeautifulSoup as B
D = sys.argv[1]
KOD = os.path.dirname(os.path.abspath(__file__)); VERI = os.path.join(os.path.dirname(KOD), "veri")
AY = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                  "September", "October", "November", "December"], 1)}
KISA = {m[:3]: i for m, i in AY.items()}
def tur_bul(t):
    t = t.lower()
    if "cancel" in t: return "iptal"
    if "notation" in t: return "notation_vote"
    if "conference call" in t: return "konferans_gorusmesi"
    if "unscheduled" in t: return "olaganustu_toplanti"
    return "planli"
rows = []
# 2005-2020 tarihsel sayfalar: "July 31-August 1  Meeting - 2012", "March 2 (unscheduled) Meeting - 2020"
for y in range(2005, 2021):
    s = B(open(os.path.join(D, f"h{y}.htm")).read(), "lxml")
    for h in s.find_all("h5"):
        bas = re.sub(r"\s+", " ", h.get_text(" ", strip=True))
        par = h.find_parent("div", class_="panel"); t = par.get_text(" ", strip=True) if par else ""
        ms = re.match(r"([A-Z][a-z]+)/([A-Z][a-z]+) (\d+)-(\d+)", bas)      # "Jan/Feb 31-1", "April/May 30-1"
        if ms:
            a1, g1, a2, gun2 = KISA[ms.group(1)[:3]], int(ms.group(3)), KISA[ms.group(2)[:3]], int(ms.group(4))
        else:
            m = re.match(r"([A-Z][a-z]+) (\d+)(?:-([A-Z][a-z]+)? ?(\d+))?", bas)
            if not m: print("ESLESMEDI", bas); continue
            a1, g1 = AY[m.group(1)], int(m.group(2))
            a2 = AY[m.group(3)] if m.group(3) else a1
            gun2 = int(m.group(4) or m.group(2))
        rows.append(dict(baslik=bas, karar_gunu=pd.Timestamp(y, a2, gun2), ilk_gun=pd.Timestamp(y, a1, g1),
                         tur=tur_bul(bas), basin_toplantisi="Press Conference" in t, aciklama_var="Statement" in t,
                         kaynak=f"https://www.federalreserve.gov/monetarypolicy/fomchistorical{y}.htm"))
# 2021-2027 guncel takvim
s = B(open(os.path.join(D, "cal.htm")).read(), "lxml")
for p in s.select("div.panel"):
    hd = p.select_one("div.panel-heading")
    my = re.match(r"(\d{4}) FOMC Meetings", hd.get_text(" ", strip=True)) if hd else None
    if not my: continue
    y = int(my.group(1))
    for mt in p.select("div.fomc-meeting"):
        ay = mt.select_one(".fomc-meeting__month").get_text(strip=True); tar = mt.select_one(".fomc-meeting__date").get_text(" ", strip=True)
        t = mt.get_text(" ", strip=True)
        ays = ay.split("/"); a1 = AY.get(ays[0]) or KISA[ays[0][:3]]; a2 = AY.get(ays[-1]) or KISA[ays[-1][:3]]
        g = re.match(r"(\d+)(?:-(\d+))?", tar)
        g1, g2 = int(g.group(1)), int(g.group(2) or g.group(1))
        if len(ays) == 1: a2 = a1
        y2 = y + 1 if a2 < a1 else y
        karar = pd.Timestamp(y2, a2, g2)
        rows.append(dict(baslik=f"{ay} {tar} - {y}", karar_gunu=karar, ilk_gun=pd.Timestamp(y, a1, g1), tur=tur_bul(tar),
                         basin_toplantisi=("Press Conference" in t) or (karar > pd.Timestamp("2026-11-21") and tur_bul(tar) == "planli"),
                         aciklama_var=("Statement" in t) or karar > pd.Timestamp("2026-11-21"), sep="*" in tar,
                         kaynak="https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"))
F = pd.DataFrame(rows)
F = F[(F.karar_gunu >= "2005-01-01") & (F.karar_gunu <= "2026-12-31")].sort_values("karar_gunu").drop_duplicates(["karar_gunu", "tur"])
F["gelecek"] = F.karar_gunu > pd.Timestamp("2026-11-21")
F["iki_gunluk"] = F.karar_gunu != F.ilk_gun
F["not"] = ""
F.loc[F.gelecek & F.tur.eq("planli"), "not"] = "gelecek toplanti; 2019'dan beri her planli toplantida basin toplantisi var (varsayim)"
F = F[["karar_gunu", "ilk_gun", "tur", "iki_gunluk", "basin_toplantisi", "aciklama_var", "gelecek", "baslik", "kaynak", "not"]]
F.to_csv(os.path.join(VERI, "fomc_tarihleri.csv"), index=False, date_format="%Y-%m-%d")
print(F.tur.value_counts().to_dict()); print(F[F.tur == "planli"].groupby(F.karar_gunu.dt.year).size().to_dict())
print("basin (planli):", F[F.tur == "planli"].groupby(F.karar_gunu.dt.year).basin_toplantisi.sum().to_dict())
print(F[F.tur != "planli"][["karar_gunu", "tur", "aciklama_var", "basin_toplantisi"]].to_string(index=False))
