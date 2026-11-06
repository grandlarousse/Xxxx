"""Hizli bakis olay listeleri (yalniz metadata; detay sayfasi cekilmedi):
 (a) BEDELLI (ruchan hakli) sermaye artirimi: Is Yatirim 'Bedelli Sermaye Artırımı' hak gunu (ruchan baslangici) + KAP ilk 'bedelli/rüçhan/nakden' YK bildirimi
 (b) NAKIT TEMETTU: Is Yatirim 'Nakit Temettü' hak gunu + brut oran (nominale %) ; ilk KAP 'Kar Payi Dagitimi' bildirimi (hak gunu oncesi 200 gun)
Cikti: <CACHE>/olaylar_bedelli.pkl, olaylar_temettu.pkl"""
import numpy as np, pandas as pd
import f07_olaylar as O
CACHE = O.CACHE
def bedelli():
    isy = pd.read_csv(f"{CACHE}/isy_sermaye_all.csv", parse_dates=["tarih"])
    b = isy[isy.SHT_TANIMI.isin(["Bedelli Sermaye Artırımı", "Bedelli ve Bedelsiz Sermaye Artırımı"]) & (isy.tarih >= "2014-06-01") & (isy.tarih <= "2026-11-05")]
    b = b.groupby(["HISSE_KODU", "tarih"]).agg(oran=("SHHE_BDLI_ORAN", "sum"), bdsz=("SHHE_BDSZ_IK_ORAN", "sum"), tip=("SHT_TANIMI", "first")).reset_index()
    K = O.kap_meta(); out = []
    allx = isy[isy.SHT_TANIMI.str.contains("Bedelli")][["HISSE_KODU", "tarih"]]
    for _, e in b.iterrows():
        prev = allx[(allx.HISSE_KODU == e.HISSE_KODU) & (allx.tarih < e.tarih)].tarih.max()
        lo = max(prev + pd.Timedelta(days=1) if pd.notna(prev) else pd.Timestamp("2000-01-01"), e.tarih - pd.Timedelta(days=400))
        m = K[(K.codes == e.HISSE_KODU) & (K.pt > lo) & (K.pt < e.tarih)].sort_values("pt")
        s = m.summary.fillna("").str.lower()
        c = m[s.str.contains("bedelli|rüçhan|ruchan|nakden|nakit") & ~s.str.contains("tahsis|tescil|tamamlan|kullanılmayan|sonuç|satış sonu|ilan") ]
        out.append(dict(kod=e.HISSE_KODU, hak=e.tarih, oran=e.oran, bdsz=e.bdsz, tip=e.tip, p1=c.pt.min() if len(c) else pd.NaT))
    ev = pd.DataFrame(out); ev.to_pickle(f"{CACHE}/olaylar_bedelli.pkl"); return ev
def temettu():
    isy = pd.read_csv(f"{CACHE}/isy_sermaye_all.csv", parse_dates=["tarih"])
    b = isy[isy.SHT_TANIMI.isin(["Nakit Temettü", "Bedelsiz ve Nakit Temettü"]) & (isy.tarih >= "2014-06-01") & (isy.tarih <= "2026-11-05")]
    b = b.groupby(["HISSE_KODU", "tarih"]).agg(brut=("SHHE_NAKIT_TM_ORAN", "sum"), net=("SHHE_NAKIT_TM_ORAN_NET", "sum"), ayar=("SHHE_FIYAT_AYAR_OR", "min")).reset_index()
    KP = O.kpd_meta(); out = []
    allx = b[["HISSE_KODU", "tarih"]]
    for _, e in b.iterrows():
        prev = allx[(allx.HISSE_KODU == e.HISSE_KODU) & (allx.tarih < e.tarih)].tarih.max()
        lo = max(prev + pd.Timedelta(days=1) if pd.notna(prev) else pd.Timestamp("2000-01-01"), e.tarih - pd.Timedelta(days=200))
        m = KP[(KP.codes == e.HISSE_KODU) & (KP.pt > lo) & (KP.pt < e.tarih)].sort_values("pt")
        out.append(dict(kod=e.HISSE_KODU, hak=e.tarih, brut=e.brut, net=e.net, ayar=e.ayar, p1=m.pt.min() if len(m) else pd.NaT))
    ev = pd.DataFrame(out); ev["verim"] = 1 - ev.ayar   # Is Yatirim fiyat ayarlama orani = 1 - temettu/onceki kapanis
    ev.to_pickle(f"{CACHE}/olaylar_temettu.pkl"); return ev
if __name__ == "__main__":
    a = bedelli(); print("bedelli", len(a), a.p1.notna().sum())
    t = temettu(); print("temettu", len(t), t.p1.notna().sum()); print(t.verim.describe())
