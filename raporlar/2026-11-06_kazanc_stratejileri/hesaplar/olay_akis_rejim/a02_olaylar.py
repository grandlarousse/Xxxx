"""(A) Olay listeleri: KAP 'Paylarin Geri Alinmasina Iliskin Bildirim' (GA) ve 'Pay Alim Satim Bildirimi' (PAS) metadatasindan.
GA siniflari (ozet metni, onceden belirlenmis kurallar):
  PROG = program/karar/baslatma/yetki ifadesi ve islem ifadesi yok;  BITIS = sonlandirma/tamamlanma;  ISLEM = digerleri (gerceklesen alim bildirimi agirlikli)
Olay tanimlari (hepsi hisse bazinda, ortusmeyi azaltmak icin 'sessizlik' kosullu):
  GA_YENI   : herhangi bir GA bildirimi, ayni hissede onceki 60 islem gunu GA bildirimi yok (yeni geri alim dalgasi baslangici)
  GA_PROG   : PROG sinifi, ayni hissede onceki 60 islem gunu PROG yok
  GA_ISLEM  : ISLEM sinifi, ayni hissede onceki 20 islem gunu ISLEM yok (alim kosusu baslangici)
PAS yonu: sadece ozetinde acikca 'alim' (satim/satis yok) -> ALIS; 'satim/satis' (alim yok) -> SATIS. Genel 'alim satim bildirimi' (%84) yon bilinmez
  -> PAS_HEPSI olarak ayrica (yonsuz kontrol). Ayrintili yon icin KAP eki PDF gerekiyor; olcekte cekilemedi (KAP 429 sinirlari).
  PAS_ALIS : ALIS, onceki 20 islem gunu ALIS yok;  PAS_ALIS_KUME: 20 islem gunu icinde >=3 ALIS bildirimi (3.'sunun giris gunu), onceki 60 gunde kume yok
  PAS_SATIS: SATIS, onceki 20 gunde SATIS yok;  PAS_HEPSI: herhangi PAS (genel), onceki 20 gunde PAS yok
Giris: yayin saati 17:00'den once ve islem gunu ise ayni gun kapanis, degilse sonraki islem gunu kapanis."""
import re, numpy as np, pandas as pd
import ortak as O
TK = O.islem_gunleri()
def kodlar(s):
    return [x.strip() for x in str(s).split(",") if x.strip()]
def ana_kod(lst):
    """Birden cok kod (orn. 'ISATR, ISBTR, ISCTR, ISKUR, TIB') -> fiyat verisi olan ilk tercih: tabloda en likit (vol) olan."""
    best, bv = None, -1
    for k in lst:
        d = O.hisse(k, fetch=False)
        if d is None: continue
        v = d.vol_tl.tail(500).median() if "vol_tl" in d else 0
        if v > bv: best, bv = k, v
    return best
def ga_sinif(s):
    s = s.lower()
    if re.search(r"sonland|tamamlan|bitiril|sona er", s): return "BITIS"
    if re.search(r"program|karar|başlat|baslat|yetki", s) and not re.search(r"işlem|islem|gerçekleş|gerceklest|tarihli|çerçevesinde (pay|hisse)|kapsamında (pay|hisse) al|alımı\.?$", s):
        return "PROG"
    return "ISLEM"
def pas_yon(s):
    s = s.lower()
    if re.search(r"geri al", s): return "GA"
    al = bool(re.search(r"al[ıi]m|al[ıi][şs]\b|satın al", s)); st = bool(re.search(r"sat[ıi]m|sat[ıi][şs]", s))
    if al and not st: return "A"
    if st and not al: return "S"
    return "?"
def sessiz(df, gun, key="kod"):
    """df: kod, gi (giris gunu indeksi). Ayni kodda onceki 'gun' islem gunu icinde olay yoksa tut."""
    out = []
    for k, g in df.sort_values("gi").groupby(key):
        last = -10 ** 9
        for _, r in g.iterrows():
            if r.gi - last > gun: out.append(r)
            last = r.gi
    return pd.DataFrame(out)
def hazirla(path, tur):
    df = pd.read_pickle(path)
    df["t"] = pd.to_datetime(df.publishDate, format="%d.%m.%Y %H:%M:%S")
    df["kods"] = df.stockCodes.fillna(df.relatedStocks).apply(kodlar)
    df = df[df.kods.str.len() > 0].copy()
    df["kod"] = df.kods.apply(lambda l: l[0] if len(l) == 1 else ana_kod(l))
    df = df[df.kod.notna()].copy()
    df["t0"] = df.t.apply(lambda x: O.giris_gunu(x, TK)); df = df[df.t0.notna()].copy()
    df["gi"] = TK.get_indexer(pd.DatetimeIndex(df.t0))
    df["sinif"] = df.summary.fillna("").apply(ga_sinif if tur == "GA" else pas_yon)
    df["duzeltme"] = df.summary.fillna("").str.lower().str.contains("düzeltme|duzeltme")
    return df[~df.duzeltme]
if __name__ == "__main__":
    ga = hazirla(O.MY + "/kap_GA_all.pkl", "GA"); pas = hazirla(O.MY + "/kap_PAS_all.pkl", "PAS")
    # PAS icindeki geri alim bildirimleri GA'ya eklenir (ayni bildirim degil; bazi sirketler yanlis konu secmis)
    ga = pd.concat([ga, pas[pas.sinif == "GA"].assign(sinif="ISLEM")], ignore_index=True)
    print("GA bildirim", len(ga), ga.sinif.value_counts().to_dict(), "hisse", ga.kod.nunique())
    print("PAS bildirim", len(pas), pas.sinif.value_counts().to_dict(), "hisse", pas.kod.nunique())
    ev = []
    e = sessiz(ga, 60); ev.append(e.assign(olay="GA_YENI"))
    e = sessiz(ga[ga.sinif == "PROG"], 60); ev.append(e.assign(olay="GA_PROG"))
    e = sessiz(ga[ga.sinif == "ISLEM"], 20); ev.append(e.assign(olay="GA_ISLEM"))
    a = pas[pas.sinif == "A"]
    ev.append(sessiz(a, 20).assign(olay="PAS_ALIS"))
    ev.append(sessiz(pas[pas.sinif == "S"], 20).assign(olay="PAS_SATIS"))
    ev.append(sessiz(pas[pas.sinif != "GA"], 20).assign(olay="PAS_HEPSI"))
    # kume alis: 20 islem gunu icinde >=3 ALIS bildirimi
    rows = []
    for k, g in a.sort_values("gi").groupby("kod"):
        gi = g.gi.values; lastc = -10 ** 9
        for j in range(2, len(gi)):
            if gi[j] - gi[j - 2] <= 20 and gi[j] - lastc > 60:
                rows.append(g.iloc[j]); lastc = gi[j]
    ev.append(pd.DataFrame(rows).assign(olay="PAS_ALIS_KUME"))
    E = pd.concat(ev, ignore_index=True)[["olay", "kod", "t", "t0", "gi", "sinif", "summary", "disclosureIndex"]]
    E["viop"] = E.kod.isin(O.VIOP)
    E.to_pickle(O.MY + "/olaylar_A.pkl")
    print(E.groupby("olay").agg(n=("kod", "size"), hisse=("kod", "nunique"), viop=("viop", "sum")).to_string())
    # fiyat verisi olmayan hisseler
    miss = sorted(set(k for k in E.kod.unique() if O.hisse(k, fetch=False) is None))
    open(O.MY + "/eksik_hisse.txt", "w").write("\n".join(miss)); print("fiyat yok:", len(miss))
