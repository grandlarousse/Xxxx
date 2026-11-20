"""VİOP süzülmüş bültenlerinden viop_daily.parquet ve viop_front.parquet (D2).
Girdi : $S/data/viop_filt/viop_YYYYMMDD.txt  (01_viop_indir.py çıktısı)
Çıktı : $S/data/panel_full/viop_daily.parquet, viop_front.parquet
Kullanım: python3 -I 06_viop_build.py
Notlar:
- Bülten fiyatlarında 0 = o gün işlem yok -> açılış/düşük/yüksek/kapanış/aof NaN yapılır; uzlaşma korunur.
- Kapanış (kapanis) sütunu bülten 'KAPANIS FIYATI' = o günün son işlem fiyatı (kapanışta son eşleşme); 'son' takma adı.
- Yakın vade = o gün işlem hacmi (TL) en yüksek, vadesi bitmemiş kontrat. Hacim hepsi 0 ise açık pozisyon, o da yoksa en yakın vade.
- ret_settle  : aynı kontratın uzlaşmadan uzlaşmaya getirisi = uzlasma / onceki_uzlasma - 1 (bülten kendi önceki uzlaşmasını verir; kontrat içinde, vade geçişinde sıçrama yok)
- ret_last    : aynı kontratın son fiyattan son fiyata getirisi = kapanis(t)/kapanis(önceki bülten günü, aynı kontrat) - 1 (iki gün de işlem varsa)
- ret_last_prevset: kapanis(t)/onceki_uzlasma(t) - 1
- fwd_settle_h (h=1,2,3): t günü seçilen kontratın t+1..t+h bülten günlerindeki ret_settle'lerinin bileşkesi (kontrat bu günlerde listeliyse; değilse NaN). Elde tutma getirisi.
"""
import os, glob, re
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el/data"
FILT = f"{S}/viop_filt"; OUT = f"{S}/panel_full"; os.makedirs(OUT, exist_ok=True)
COLS = {"TARIH": "date", "SOZLESME KODU": "kod", "PAZAR SEGMENTI": "seg", "SOZLESME SINIFI": "sinif", "DAYANAK VARLIK": "und_raw",
        "VADE TARIHI": "vade", "UZLASMA FIYATI": "uzlasma", "ONCEKI UZLASMA FIYATI": "onceki_uzlasma", "ACILIS FIYATI": "acilis",
        "EN DUSUK FIYAT": "dusuk", "EN YUKSEK FIYAT": "yuksek", "KAPANIS FIYATI": "kapanis", "AGIRLIKLI ORTALAMA FIYAT": "aof",
        "ISLEM HACMI": "hacim_tl", "ISLEM MIKTARI": "miktar", "ISLEM SAYISI": "islem_sayisi", "ACIK POZISYON": "acik_poz",
        "ACIK POZISYON DEGISIMI": "acik_poz_deg", "ACILIS SEANSI FIYATI": "os_fiyat", "ACILIS SEANSI ISLEM HACMI": "os_hacim_tl",
        "ACILIS SEANSI ISLEM MIKTARI": "os_miktar"}
NUM = ["uzlasma", "onceki_uzlasma", "acilis", "dusuk", "yuksek", "kapanis", "aof", "hacim_tl", "miktar", "islem_sayisi", "acik_poz",
       "acik_poz_deg", "os_fiyat", "os_hacim_tl", "os_miktar"]
PX = ["acilis", "dusuk", "yuksek", "kapanis", "aof", "os_fiyat"]

def fnum(x):
    if not isinstance(x, str): return np.nan
    x = x.strip()
    if x == "": return np.nan
    try: return float(x)
    except ValueError:
        try: return float(x.replace(",", "."))
        except ValueError: return np.nan

def parse(fn):
    with open(fn, encoding="utf-8") as fh: lines = fh.read().splitlines()
    hdr = [h.strip() for h in lines[0].split(";")]
    idx = {COLS[h]: i for i, h in enumerate(hdr) if h in COLS}
    recs = []
    for ln in lines[1:]:
        f = ln.split(";")
        recs.append({k: (f[i] if i < len(f) else "") for k, i in idx.items()})
    return recs

def und_of(r):
    u = r["und_raw"].strip()
    if u == "D_XU030D" or r["sinif"].strip() == "DE_BIST30_FUT": return "XU030"
    if r["seg"].strip() == "ENF" and r["kod"].startswith("F_ELCBAS"): return "ELCBAS"
    return u[:-2] if u.endswith(".E") else u

def main():
    files = sorted(glob.glob(f"{FILT}/viop_????????.txt"))
    recs = []
    for fn in files: recs += parse(fn)
    D = pd.DataFrame(recs)
    for c in NUM:
        if c not in D: D[c] = np.nan
        else: D[c] = D[c].map(fnum)
    D["date"] = pd.to_datetime(D["date"]); D["vade"] = pd.to_datetime(D["vade"], errors="coerce")
    D["und"] = [und_of(r) for r in D[["und_raw", "sinif", "seg", "kod"]].to_dict("records")]
    for c in PX: D.loc[D[c] <= 0, c] = np.nan
    D["carpan"] = D["hacim_tl"] / (D["miktar"] * D["aof"])  # TL hacim / (adet x aof) = sözleşme çarpanı (pay 100)
    D = D.sort_values(["und", "date", "vade", "kod"]).reset_index(drop=True)
    keep = ["date", "und", "kod", "vade", "uzlasma", "onceki_uzlasma", "acilis", "dusuk", "yuksek", "kapanis", "aof", "hacim_tl", "miktar",
            "islem_sayisi", "acik_poz", "acik_poz_deg", "os_fiyat", "os_hacim_tl", "os_miktar", "carpan"]
    D = D[keep]
    D = D.drop_duplicates(["date", "kod"], keep="last").reset_index(drop=True)
    D.to_parquet(f"{OUT}/viop_daily.parquet", index=False)
    print("viop_daily", D.shape, D["date"].min().date(), D["date"].max().date())

    # --- yakın vade sürekli seri ---
    bdays = np.sort(D["date"].unique()); bi = {d: i for i, d in enumerate(bdays)}  # bülten günü sırası (tüm dayanaklar için ortak)
    D["bi"] = D["date"].map(bi)
    D["ret_settle"] = np.where(D["onceki_uzlasma"] > 0, D["uzlasma"] / D["onceki_uzlasma"] - 1, np.nan)
    D = D.sort_values(["kod", "date"])
    g = D.groupby("kod")
    pk = g["kapanis"].shift(1); pbi = g["bi"].shift(1)
    D["ret_last"] = np.where((pbi == D["bi"] - 1) & (pk > 0), D["kapanis"] / pk - 1, np.nan)
    D["ret_last_prevset"] = np.where(D["onceki_uzlasma"] > 0, D["kapanis"] / D["onceki_uzlasma"] - 1, np.nan)
    # önceki uzlaşma tutarlılığı (aynı kontrat, ardışık bülten günü)
    pu = g["uzlasma"].shift(1)
    D["onceki_tutarsiz"] = ((pbi == D["bi"] - 1) & ((D["onceki_uzlasma"] / pu - 1).abs() > 1e-6)).astype(int)
    # seçim
    E = D[D["vade"] >= D["date"]].copy()
    E["hv"] = E["hacim_tl"].fillna(0); E["oi"] = E["acik_poz"].fillna(0)
    E = E.sort_values(["und", "date", "hv", "oi", "vade"], ascending=[True, True, False, False, True])
    F = E.groupby(["und", "date"]).head(1).copy()
    F = F.sort_values(["und", "date"]).reset_index(drop=True)
    F["vade_kalan_gun"] = (F["vade"] - F["date"]).dt.days
    F["secim"] = np.where(F["hv"] > 0, "hacim", np.where(F["oi"] > 0, "acik_poz", "yakin_vade"))
    # kontrat değişimi (önceki bülten gününde farklı kontrat seçilmişse)
    F["onceki_kod"] = F.groupby("und")["kod"].shift(1)
    F["roll"] = ((F["onceki_kod"].notna()) & (F["onceki_kod"] != F["kod"])).astype(int)
    # ileri bileşik getiri (t'de seçilen kontrat; t+1..t+h aynı kontratın ret_settle'i)
    lk = D.set_index(["kod", "bi"])["ret_settle"]
    for h in (1, 2, 3):
        acc = np.ones(len(F)); ok = np.ones(len(F), bool)
        for k in range(1, h + 1):
            r = lk.reindex(pd.MultiIndex.from_arrays([F["kod"], F["bi"] + k])).values
            ok &= ~np.isnan(r); acc *= np.where(np.isnan(r), 1.0, 1 + r)
        F[f"fwd_settle_{h}"] = np.where(ok, acc - 1, np.nan)
    F = F[["date", "und", "kod", "vade", "vade_kalan_gun", "secim", "roll", "uzlasma", "onceki_uzlasma", "acilis", "dusuk", "yuksek", "kapanis",
           "aof", "hacim_tl", "miktar", "islem_sayisi", "acik_poz", "ret_settle", "ret_last", "ret_last_prevset", "onceki_tutarsiz",
           "fwd_settle_1", "fwd_settle_2", "fwd_settle_3"]]
    F.to_parquet(f"{OUT}/viop_front.parquet", index=False)
    print("viop_front", F.shape)
    # doğrulama özeti
    rows = []
    for u, g2 in F.groupby("und"):
        rows.append(dict(und=u, ilk=g2["date"].min().date(), son=g2["date"].max().date(), gun=len(g2),
                         hacim0_oran=round((g2["hacim_tl"].fillna(0) == 0).mean(), 3), ret_settle_na=round(g2["ret_settle"].isna().mean(), 3),
                         ret_last_na=round(g2["ret_last"].isna().mean(), 3), max_abs_ret_settle=round(g2["ret_settle"].abs().max(), 3),
                         roll_sayisi=int(g2["roll"].sum()), onceki_tutarsiz=int(g2["onceki_tutarsiz"].sum()), med_hacim_mTL=round(g2["hacim_tl"].median() / 1e6, 2)))
    print(pd.DataFrame(rows).to_string(index=False))
    print("bülten günü sayısı", len(bdays))

if __name__ == "__main__": main()
