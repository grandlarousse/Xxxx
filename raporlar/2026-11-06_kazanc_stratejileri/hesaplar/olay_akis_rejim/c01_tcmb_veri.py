"""TCMB EVDS3 web arayuzunun kendi veri ucu (https://evds3.tcmb.gov.tr/igmevdsms-dis/fe, giris/anahtar gerektirmeyen herkese acik sorgu),
varsayilan basliklar, tek tek, 1.5 sn bekleme. Captcha sadece uyelik/giris icin; veri sorgusu acik.
Cekilenler:
  (1) Haftalik yurt disi yerlesik menkul kiymet portfoyu: TP.MKNETHAR.M7 (hisse net alim, mn USD, 2020-09->), M1 (hisse stok), M8 (DIBS net)
      + arsiv TP.PYUK3 / PYUK1 / PYUK4 (2005-01 -> 2021-08). Cuma biten hafta; yayin: izleyen Persembe 14:30.
  (2) TCMB AOFM (TP.APIFON4), gunluk.
  (3) DIBS gosterge nitelikli gunluk degerler (bie_pydibs + bie_pydibsarsiv): sabit kuponlu (..T2) ve kuponsuz (..T) TRT tahvilleri,
      'Deger' = KIRLI fiyat (kupon gununde kupon kadar dusuyor, dogrulandi) ve '.ORAN' = donemlik kupon (%).
Cikti: <CACHE>/tcmb/*.parquet"""
import os, sys, json, time, requests, pandas as pd
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/akis_rejim"
RAW = CACHE + "/tcmb_raw"; OUT = CACHE + "/tcmb"; os.makedirs(OUT, exist_ok=True)
U = "https://evds3.tcmb.gov.tr/igmevdsms-dis/fe"
S = requests.Session()
def q(series, agg, start, end, freq="1", dec="4"):
    body = {"type": "json", "series": "-".join(series), "aggregationTypes": "-".join(agg), "formulas": "-".join(["0"] * len(series)),
            "startDate": start, "endDate": end, "frequency": freq, "decimalSeperator": ".", "decimal": dec, "dateFormat": "0", "lang": "tr",
            "yon": "", "sira": "", "ozelFormuller": [], "groupSeperator": False, "isRaporSayfasi": False}
    for k in range(3):
        try:
            r = S.post(U, json=body, timeout=180)
            if r.status_code == 200:
                d = pd.DataFrame(r.json()["items"]); d["Tarih"] = pd.to_datetime(d["Tarih"], format="%d-%m-%Y")
                d = d.set_index("Tarih").drop(columns=["UNIXTIME", "YEARWEEK"], errors="ignore")
                return d.apply(pd.to_numeric, errors="coerce")
            print("status", r.status_code, flush=True)
        except Exception as e: print("err", e, flush=True)
        time.sleep(10 * (k + 1))
    return None
def akim():
    a = q(["TP.MKNETHAR.M7", "TP.MKNETHAR.M1", "TP.MKNETHAR.M8"], ["sum", "last", "sum"], "01-01-2005", "06-11-2026", "3", "2"); time.sleep(1.5)
    b = q(["TP.PYUK3", "TP.PYUK1", "TP.PYUK4"], ["sum", "last", "sum"], "01-01-2005", "06-11-2026", "3", "2"); time.sleep(1.5)
    a.to_parquet(OUT + "/akim_yeni.parquet"); b.to_parquet(OUT + "/akim_arsiv.parquet")
    c = q(["TP.APIFON4"], ["last"], "01-01-2009", "06-11-2026", "1", "2"); c.to_parquet(OUT + "/aofm.parquet"); time.sleep(1.5)
def tahvil():
    v = pd.read_csv(RAW + "/bond_sel.csv", parse_dates=["iss", "mat"])
    done = set(os.path.basename(f)[:-8] for f in os.listdir(OUT) if f.startswith("TP.TR"))
    v = v[~v.code.isin(done)]
    # ayni donemde yasayan tahvilleri 8'erli grupla (her biri Deger + ORAN; kuponsuzda ORAN yok)
    v = v.sort_values("iss"); rows = v.to_dict("records")
    for i in range(0, len(rows), 8):
        grp = rows[i:i + 8]; ser = []
        for x in grp:
            ser.append(x["code"])
            if x["fix"]: ser.append(x["code"] + ".ORAN")
        s0 = min(x["iss"] for x in grp).strftime("%d-%m-%Y"); s1 = min(max(x["mat"] for x in grp), pd.Timestamp("2026-11-06")).strftime("%d-%m-%Y")
        d = q(ser, ["last"] * len(ser), s0, s1)
        if d is None: print("FAIL", i, flush=True); time.sleep(5); continue
        for x in grp:
            c = x["code"].replace(".", "_"); cols = [c] + ([c + "_ORAN"] if x["fix"] else [])
            cols = [z for z in cols if z in d.columns]
            d[cols].dropna(how="all").to_parquet(f"{OUT}/{x['code']}.parquet")
        print(i, len(grp), d.shape, flush=True); time.sleep(1.5)
if __name__ == "__main__":
    if "akim" in sys.argv: akim()
    if "tahvil" in sys.argv: tahvil()
