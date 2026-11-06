"""Is Yatirim sirket karti 'Sermaye Artirimlari / Temettuler' tablosunun JSON kaynagi (tum hisseler, yil yil).
Kaynak: POST /_layouts/15/IsYatirim.Website/StockInfo/CompanyInfoAjax.aspx/GetSermayeArttirimlari (sitenin kendi AJAX cagrisi).
Varsayilan istek basliklari, istekler arasi 1 sn. Cikti: <CACHE>/isy_sermaye_<yil>.json ve isy_sermaye_all.csv"""
import os, json, time, requests, pandas as pd
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bedelsiz"
U = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/StockInfo/CompanyInfoAjax.aspx/GetSermayeArttirimlari"
S = requests.Session()
def yil(y):
    p = f"{CACHE}/isy_sermaye_{y}.json"
    if os.path.exists(p): return json.load(open(p))
    r = S.post(U, data=json.dumps({"hisseKodu": "", "hisseTanimKodu": "", "yil": y, "zaman": "HEPSI", "endeksKodu": "09", "sektorKodu": ""}),
               headers={"Content-Type": "application/json; charset=utf-8"}, timeout=120)
    d = json.loads(r.json()["d"]); json.dump(d, open(p, "w"), ensure_ascii=False); time.sleep(1.0); return d
if __name__ == "__main__":
    os.makedirs(CACHE, exist_ok=True); rows = []
    for y in range(2010, 2027):
        d = yil(y); print(y, len(d), flush=True); rows += d
    df = pd.DataFrame(rows)
    keep = ["HISSE_KODU","HisseTanim","SHT_TANIMI","SHHE_TIP_KODU","SHHE_TARIH","SHHE_BDLI_ORAN","SHHE_RHK_ORAN","SHHE_BDSZ_IK_ORAN","SHHE_BDSZ_TM_ORAN",
            "SHHE_BDSZ_BU_ORAN","SHHE_NAKIT_TM_ORAN","SHHE_NAKIT_TM_ORAN_NET","SHHE_FIYAT_AYAR_OR","HSP_BOLUNME_ONCESI_SERMAYE","HSP_BOLUNME_SONRASI_SERMAYE","SHHE_NM_SER_CARPANI"]
    df = df[keep].drop_duplicates()
    df["tarih"] = pd.to_datetime(df.SHHE_TARIH, unit="ms", errors="coerce") + pd.Timedelta(hours=3)
    df["tarih"] = df.tarih.dt.normalize()
    df.to_csv(f"{CACHE}/isy_sermaye_all.csv", index=False); print(df.SHT_TANIMI.value_counts())
