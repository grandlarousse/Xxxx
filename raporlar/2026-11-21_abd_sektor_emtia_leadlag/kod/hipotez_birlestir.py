"""ek/hipotez/*.json dosyalarını tek tabloya birleştirir, sembolleri evrene karşı doğrular, aileye atar.

Çıktı: ek/hipotez/birlesik.csv (satır = öncü x hedef çifti) ve ek/hipotez/eksik_semboller.csv
Aile ataması (YONTEM.md bölüm 4): öncü emtia ise F1; faiz/kredi/kur/volatilite/kripto/ülke/yabancı endeks ise F3;
'KENDI' ise F4/F5/F6 (tanıma göre); diğer (hisse, sektör ETF'i, yabancı hisse) F2.
"""
import glob, json, os, re, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o

m = o.meta()
EMTIA = {"emtia_etf", "vadeli_emtia"}
CAPRAZ = {"faiz_vol", "tahvil_kredi", "kur", "kur_etf", "kripto", "ulke_etf", "endeks_dis", "vadeli_finans", "genis_etf", "endeks_abd"}

def aile(oncu, tanim):
    if oncu.upper() in ("KENDI", "KENDİ"):
        t = (tanim or "").lower()
        if re.search(r"bilanço|earnings|pead|kazanç", t): return "F6"
        if re.search(r"ay dön|takvim|fomc|tatil|opsiyon|haftanın|çeyrek|ay sonu|turn", t): return "F5"
        return "F4"
    if oncu not in m.index: return "?"
    g = set(str(m.loc[oncu, "gruplar"]).split(";"))
    if g & EMTIA: return "F1"
    if g & CAPRAZ: return "F3"
    return "F2"

def liste(x):
    if x is None: return []
    if isinstance(x, str): return [s for s in re.split(r"[,\s;]+", x) if s]
    return [str(s).strip() for s in x if str(s).strip()]

sat, eksik, hata = [], [], []
for yol in sorted(glob.glob(os.path.join(o.KOK, "ek", "hipotez", "*.json"))):
    ajan = os.path.basename(yol)[:-5]
    try:
        d = json.load(open(yol))
    except Exception as e:  # noqa: BLE001
        hata.append((ajan, str(e)[:100])); continue
    for e in d.get("ek_semboller", []) or []:
        if isinstance(e, dict): eksik.append((ajan, e.get("sembol"), e.get("neden")))
        else: eksik.append((ajan, str(e), ""))
    for i, h in enumerate(d.get("hipotezler", []) or []):
        for oc in liste(h.get("oncu")):
            for hd in liste(h.get("hedef")) or ["?"]:
                sat.append(dict(ajan=ajan, hip_no=i, aile=aile(oc, h.get("oncu_tanim")), oncu=oc, hedef=hd, yon=str(h.get("yon", "?")).strip(),
                                oncelik=h.get("oncelik", 3), oncu_evrende=int(oc in m.index or oc.upper().startswith("KEND")), hedef_evrende=int(hd in m.index),
                                oncu_tanim=h.get("oncu_tanim", ""), mekanizma=h.get("mekanizma", ""), zamanlama=h.get("zamanlama", ""), kanit=h.get("kanit", "")))
df = pd.DataFrame(sat)
df.to_csv(os.path.join(o.KOK, "ek", "hipotez", "birlesik.csv"), index=False)
ek = pd.DataFrame(eksik, columns=["ajan", "sembol", "neden"])
ek2 = set(df.loc[df.oncu_evrende == 0, "oncu"]) | set(df.loc[df.hedef_evrende == 0, "hedef"])
ek.to_csv(os.path.join(o.KOK, "ek", "hipotez", "eksik_semboller.csv"), index=False)
print(len(glob.glob(os.path.join(o.KOK, "ek", "hipotez", "*.json"))), "dosya;", len(df), "çift;", "json hatası:", hata)
if len(df):
    print(df.groupby(["ajan"]).agg(cift=("oncu", "size"), hip=("hip_no", "nunique")).to_string())
    print(df.aile.value_counts().to_dict())
    test = df[(df.oncu_evrende == 1) & (df.hedef_evrende == 1)].drop_duplicates(["oncu", "hedef"])
    print("test edilebilir tekil çift:", len(test), test.aile.value_counts().to_dict())
print("ajanların istediği ek semboller:", sorted(set(ek.sembol.dropna())))
print("hipotezlerde geçen ama evrende olmayan:", sorted(ek2))
