"""Süzülmüş VİOP bültenlerinden (RAW/viop_filt) panel kurar.
Çıktı: panel_full/viop_daily.parquet (gün x sözleşme) ve panel_full/viop_front.parquet (gün x dayanak, yakın vade sürekli seri).
viop_daily: date, und, kod, vade, uzlasma, onceki_uzlasma, acilis, dusuk, yuksek, kapanis (= son işlem fiyatı), aof, hacim_tl, miktar,
  islem_sayisi, acik_poz, acik_poz_deg, segment, vkg (vadeye kalan takvim günü), fiyat_carpani, duz_carpan, ret_settle, ret_last
  - fiyat_carpani: XU030 için 2020-07-27 öncesi 10 (bugünkü endeks ölçeğine çevirmek için uzlasma*fiyat_carpani), diğerleri 1.
  - İşlem olmayan günlerde acilis/dusuk/yuksek/kapanis/aof = NaN (bültende 0).
  - ret_settle = uzlasma(t) / [aynı sözleşmenin uzlasma(t-1)] - 1. duz_carpan = bültendeki ONCEKI UZLASMA / uzlasma(t-1); 1'den farklıysa
    (özsermaye hâli/bülten düzeltmesi) payda bültendeki ONCEKI UZLASMA'dır. Sözleşmenin paneldeki ilk günü NaN.
  - ret_last = kapanis(t) / [kapanis(t-1) * duz_carpan] - 1; iki günde de işlem varsa.
viop_front: her dayanak ve gün için O GÜN HACMİ EN YÜKSEK vade (eşitlik/hiç işlem yoksa en yakın vade). Getiriler seçilen sözleşmenin KENDİ
  dünkü fiyatına göredir -> vade geçişinde sıçrama yok. Ek: vade_degisti, yakin_mi, toplam_hacim_tl, toplam_acik_poz,
  ret_settle_f1..f3 (t'de seçilen sözleşmenin t+h uzlaşmasına kadar getirisi; vade dolduysa NaN).
Kullanım: python3 -I 02_viop_build.py"""
import os, sys, re, glob, csv
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2common import RAW, FULL
COLS = {"TARIH": "date", "SOZLESME KODU": "kod", "PAZAR SEGMENTI": "segment", "DAYANAK VARLIK": "und_raw", "VADE TARIHI": "vade",
        "UZLASMA FIYATI": "uzlasma", "ONCEKI UZLASMA FIYATI": "onceki_uzlasma", "ACILIS FIYATI": "acilis", "EN DUSUK FIYAT": "dusuk",
        "EN YUKSEK FIYAT": "yuksek", "KAPANIS FIYATI": "kapanis", "AGIRLIKLI ORTALAMA FIYAT": "aof", "ISLEM HACMI": "hacim_tl",
        "ISLEM MIKTARI": "miktar", "ISLEM SAYISI": "islem_sayisi", "ACIK POZISYON": "acik_poz", "ACIK POZISYON DEGISIMI": "acik_poz_deg"}
NUM = ["uzlasma", "onceki_uzlasma", "acilis", "dusuk", "yuksek", "kapanis", "aof", "hacim_tl", "miktar", "islem_sayisi", "acik_poz", "acik_poz_deg"]
PX = ["acilis", "dusuk", "yuksek", "kapanis", "aof"]

def fnum(x):
    x = x.strip()
    if x == "": return np.nan
    try: return float(x)
    except ValueError: return float(x.replace(".", "").replace(",", ".")) if "," in x else np.nan

def und_std(kod, und_raw):
    if und_raw.endswith(".E"): return und_raw[:-2]
    if und_raw == "D_XU030D": return "XU030"
    m = re.match(r"^F_ELCBAS(Q|Y)?", kod)
    if m: return "ELCBAS" + (m.group(1) or "")
    return und_raw

def read_all():
    rows = []; bad = []
    for fn in sorted(glob.glob(f"{RAW}/viop_filt/viop_????????.csv")):
        fdate = os.path.basename(fn)[5:13]
        with open(fn, encoding="utf-8") as f:
            rd = csv.reader(f, delimiter=";"); hdr = [h.strip() for h in next(rd)]
            idx = {COLS[h]: i for i, h in enumerate(hdr) if h in COLS}
            if len(idx) != len(COLS): bad.append((fdate, "eksik sutun", sorted(set(COLS.values()) - set(idx))))
            for r in rd:
                rec = {k: r[i].strip() for k, i in idx.items() if i < len(r)}
                if rec["date"].replace("-", "") != fdate: bad.append((fdate, "tarih uyusmuyor", rec["date"]))
                rows.append(rec)
    D = pd.DataFrame(rows)
    for c in NUM: D[c] = D[c].map(fnum)
    D["date"] = pd.to_datetime(D["date"]); D["vade"] = pd.to_datetime(D["vade"], errors="coerce")
    D["und"] = [und_std(k, u) for k, u in zip(D["kod"], D["und_raw"])]
    return D, bad

def build_daily(D):
    D = D.sort_values(["kod", "date"]).reset_index(drop=True)
    notrade = ~(D["islem_sayisi"] > 0)
    for c in PX: D[c] = D[c].where(~notrade & (D[c] > 0))
    D["vkg"] = (D["vade"] - D["date"]).dt.days
    # XU030 vadelisi 2020-07-27'de (endeksten iki sıfır atılınca) 10 kat ölçek değiştirdi; ham fiyat korunur, seviye karşılaştırması için çarpan verilir.
    D["fiyat_carpani"] = np.where((D["und"] == "XU030") & (D["date"] < "2020-07-27"), 10.0, 1.0)
    g = D.groupby("kod", sort=False)
    lag_s = g["uzlasma"].shift(1); lag_c = g["kapanis"].shift(1)
    okp = D["onceki_uzlasma"].where(D["onceki_uzlasma"] > 0)
    D["duz_carpan"] = (okp / lag_s).where(lag_s > 0)
    base = okp.where(okp.notna(), lag_s)
    D["ret_settle"] = (D["uzlasma"] / base - 1).where(lag_s.notna() & (D["uzlasma"] > 0))
    D["ret_last"] = D["kapanis"] / (lag_c * D["duz_carpan"].fillna(1.0)) - 1
    keep = ["date", "und", "kod", "vade", "uzlasma", "onceki_uzlasma", "acilis", "dusuk", "yuksek", "kapanis", "aof", "hacim_tl", "miktar",
            "islem_sayisi", "acik_poz", "acik_poz_deg", "segment", "vkg", "fiyat_carpani", "duz_carpan", "ret_settle", "ret_last"]
    return D[keep].sort_values(["date", "und", "vade", "kod"]).reset_index(drop=True)

def build_front(D):
    D = D[(D["vkg"] >= 0) & D["und"].isin(["AKSEN", "ENJSA", "ODAS", "ASTOR", "ALARK", "XU030", "ELCBAS"])].copy()
    D = D.sort_values(["kod", "date"])
    lr = np.log1p(D["ret_settle"].fillna(0.0)); D["_cum"] = lr.groupby(D["kod"]).cumsum()
    g = D.groupby("kod", sort=False)
    for h in (1, 2, 3):
        D[f"ret_settle_f{h}"] = np.expm1(g["_cum"].shift(-h) - D["_cum"])
        D.loc[g["ret_settle"].shift(-h).isna(), f"ret_settle_f{h}"] = np.nan
    tot = D.groupby(["und", "date"]).agg(toplam_hacim_tl=("hacim_tl", "sum"), toplam_acik_poz=("acik_poz", "sum"), n_vade=("kod", "count"),
                                         en_yakin_vade=("vade", "min"))
    F = D.sort_values(["und", "date", "hacim_tl", "vade"], ascending=[True, True, False, True]).groupby(["und", "date"], sort=False).head(1)
    F = F.merge(tot.reset_index(), on=["und", "date"]).sort_values(["und", "date"])
    F["yakin_mi"] = F["vade"] == F["en_yakin_vade"]
    F["vade_degisti"] = F["kod"] != F.groupby("und")["kod"].shift(1)
    F.loc[F.groupby("und").cumcount() == 0, "vade_degisti"] = False
    keep = ["date", "und", "kod", "vade", "vkg", "uzlasma", "onceki_uzlasma", "acilis", "dusuk", "yuksek", "kapanis", "aof", "ret_settle", "ret_last",
            "hacim_tl", "miktar", "islem_sayisi", "acik_poz", "toplam_hacim_tl", "toplam_acik_poz", "n_vade", "yakin_mi", "vade_degisti",
            "fiyat_carpani", "duz_carpan", "ret_settle_f1", "ret_settle_f2", "ret_settle_f3"]
    return F[keep].reset_index(drop=True)

if __name__ == "__main__":
    D, bad = read_all()
    print("satir", len(D), "gun", D["date"].nunique(), D["date"].min().date(), D["date"].max().date(), "sorun", bad[:5], len(bad))
    daily = build_daily(D); front = build_front(daily)
    daily.to_parquet(f"{FULL}/viop_daily.parquet", index=False); front.to_parquet(f"{FULL}/viop_front.parquet", index=False)
    print(daily.groupby("und").agg(ilk=("date", "min"), son=("date", "max"), gun=("date", "nunique"), n=("kod", "size"), kod=("kod", "nunique")).to_string())
    print(front.groupby("und").agg(ilk=("date", "min"), gun=("date", "size"), sifir_hacim=("hacim_tl", lambda x: (x <= 0).mean()),
                                   gecis=("vade_degisti", "sum"), yakin=("yakin_mi", "mean"), rs_max=("ret_settle", lambda x: x.abs().max())).to_string())
