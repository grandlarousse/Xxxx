"""Hisse gunluk veri: Is Yatirim HisseTekil (VARSAYILAN requests basliklari, sirali, 0.7 sn bekleme).
Evren: KAP XUTUM guncel uyeleri (580) - yani SADECE BUGUN ISLEM GOREN hisseler (survivorship bias!).
Kardes ajanin onbellegi (scratchpad/veri/<KOD>.json) varsa once oradan okunur (sunucuya tekrar istek atmamak icin).
Cikti: scratchpad/data/bist_test/hisse/<KOD>.parquet  sutunlar: adj (temettu+bedelsiz duzeltmeli kapanis), raw, hi, lo, vol_tl, usdtry, mcap, float_mcap"""
import os, sys, json, time, requests, pandas as pd
SP = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad"
OUT = SP + "/data/bist_test/hisse"; SIB = SP + "/veri"
U = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil"
C = {"HGDG_KAPANIS": "adj", "HG_KAPANIS": "raw", "HGDG_MAX": "hi", "HGDG_MIN": "lo", "HGDG_HACIM": "vol_tl", "DD_DEGER": "usdtry", "PD": "mcap", "HAO_PD": "float_mcap"}
S = requests.Session()
def parse(v):
    df = pd.DataFrame(v)
    df["d"] = pd.to_datetime(df["HGDG_TARIH"], format="%d-%m-%Y")
    df = df.drop_duplicates("d").set_index("d").sort_index()
    return pd.DataFrame({n: pd.to_numeric(df[c], errors="coerce") for c, n in C.items() if c in df})
def one(code):
    p = f"{OUT}/{code}.parquet"
    if os.path.exists(p): return "cached"
    sp = f"{SIB}/{code}.json"
    if os.path.exists(sp) and os.path.getsize(sp) > 200:
        try:
            v = json.load(open(sp)).get("value") or []
            if v: parse(v).loc["2009-01-01":].to_parquet(p); return "sib"
        except Exception: pass
    for k in range(3):
        try:
            r = S.get(U, params={"hisse": code, "startdate": "01-01-2009", "enddate": "06-11-2026"}, timeout=120)
            if r.status_code == 200:
                v = r.json().get("value") or []
                if not v: return "empty"
                parse(v).to_parquet(p); return f"ok {len(v)}"
            if r.status_code == 429: time.sleep(15)
        except Exception as e:
            err = str(e)[:60]
        time.sleep(2)
    return "fail"
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    mem = json.load(open(SP + "/data/bist_test/kap_endeks_uyeleri.json"))
    codes = list(dict.fromkeys(mem["XUTUM"] + sum([mem[k] for k in mem if k.startswith("X")], [])))
    # kardes ajanin listesindekileri sona birak (onlar zaten indiriyor)
    sib_list = set(x[:-5] for x in os.listdir(SIB) if x.endswith(".json"))
    codes = [c for c in codes if c not in sib_list] + [c for c in codes if c in sib_list]
    print("toplam", len(codes), flush=True)
    for c in codes:
        st = one(c); print(c, st, flush=True)
        if st not in ("cached", "sib"): time.sleep(0.7)
