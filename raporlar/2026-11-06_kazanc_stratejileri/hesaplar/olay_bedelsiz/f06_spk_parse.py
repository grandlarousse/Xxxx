"""SPK bulten metinlerinden (pdftotext -layout) iki bolum cikarir ve normalize eder:
  'onay'  : 'ONAYLANAN' baslikli bolum (izahname/ihrac belgesi onaylanan paylar), borclanma araci alt bolumu haric
  'basvuru': 'YENI BASVURULAR' bolumu (2014-20xx bultenlerinde var)
Cikti: <CACHE>/spk/bulten_bolum.pkl  (no, tarih, yayim_tsi [biliniyorsa], onay_txt, basvuru_txt)"""
import os, re, glob, pandas as pd, numpy as np
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bedelsiz/spk"
TR = str.maketrans({"İ": "i", "I": "i", "ı": "i", "Ş": "s", "ş": "s", "Ğ": "g", "ğ": "g", "Ü": "u", "ü": "u", "Ö": "o", "ö": "o", "Ç": "c", "ç": "c", "Â": "a", "â": "a", "Î": "i", "î": "i", "Û": "u", "û": "u"})
def norm(s): return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s.translate(TR).lower())).strip()
SEC = re.compile(r"^\s{0,20}[A-ZÇĞİÖŞÜ]{1,2}\.\s+[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ /\-,]{3,}")
SUBSTOP = re.compile(r"^\s{0,20}\d{1,2}\.\s+.*(Borçlanma|Kira Sertifika|Varant|Varlığa Dayalı|İpoteğe|Yatırım Fon|Fon Kurulu|Kurul Kayd|Sertifika)", re.I)
def bolumler(txt):
    L = txt.splitlines(); onay = []; bas = []; mode = None
    for l in L:
        if SEC.match(l):
            u = l.upper()
            mode = "onay" if "ONAYLANAN" in u else ("bas" if "YENİ BAŞVURU" in u or "YENI BASVURU" in u else None)
            continue
        if mode and SUBSTOP.match(l): mode = mode + "_x"
        if mode == "onay": onay.append(l)
        elif mode == "bas": bas.append(l)
    return norm(" ".join(onay)), norm(" ".join(bas))
if __name__ == "__main__":
    lst = pd.read_csv(f"{CACHE}/bulten_liste.csv", parse_dates=["tarih", "yukleme_utc"])
    rows = []
    for _, r in lst.iterrows():
        k = os.path.basename(r.url)[:-4].replace(" ", "_"); f = f"{CACHE}/txt/{k}.txt"
        if not os.path.exists(f): continue
        o, b = bolumler(open(f, errors="ignore").read())
        yt = r.yukleme_utc + pd.Timedelta(hours=3) if pd.notna(r.yukleme_utc) else pd.NaT
        if pd.notna(yt) and yt.normalize() != r.tarih: yt = pd.NaT   # yeniden yukleme: yayim zamani degil
        rows.append(dict(no=r.no.replace(" ", ""), tarih=r.tarih, yayim_tsi=yt, onay=o, basvuru=b, dosya=k))
    df = pd.DataFrame(rows).sort_values("tarih"); df.to_pickle(f"{CACHE}/bulten_bolum.pkl")
    print(len(df), "bulten; onay bolumu bos:", (df.onay.str.len() < 30).sum(), "basvuru bos:", (df.basvuru.str.len() < 30).sum())
    print(df.groupby(df.tarih.dt.year).agg(n=("no", "size"), onay_bos=("onay", lambda s: (s.str.len() < 30).sum()), bas_bos=("basvuru", lambda s: (s.str.len() < 30).sum())))
