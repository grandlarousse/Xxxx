"""Veri indirme betiği (Yahoo / yfinance).

Kullanım:
  python kod/indir.py                      # tüm listeler, günlük
  python kod/indir.py NVDA AMD             # yalnızca bu kodlar, günlük
  python kod/indir.py --saatlik            # hedef + ETF, 1 saatlik (730 gün)
  python kod/indir.py --saatlik NVDA       # yalnızca NVDA saatlik

Çıktı:
  veri/gunluk/<KOD>.csv  sütunlar: Open High Low Close AdjClose Volume
                         + carpan (=AdjClose/Close) + AOpen AHigh ALow AClose (düzeltilmiş)
  veri/saatlik/<KOD>.csv (America/New_York saat dilimi, bar başlangıç zamanı)
  veri/kapsam_gunluk.csv / veri/kapsam_saatlik.csv : kod başına ilk/son tarih, satır sayısı, sorun notu

İleri doldurma YAPILMAZ. Boş ya da son günü eksik kodlar kapsam dosyasında işaretlenir.
"""
import sys, time, argparse
from pathlib import Path
import pandas as pd
import yfinance as yf

KOK = Path(__file__).resolve().parents[1]
VERI = KOK / "veri"

HEDEF = ("NVDA AMD AVGO MRVL TSM ASML AMAT LRCX KLAC TER INTC ARM QCOM MPWR ONTO CAMT MU SNDK WDC STX "
         "P NTAP ANET CRDO ALAB COHR LITE CIEN AAOI FN CLS SMCI DELL HPE VRT ETN GEV BE VST CEG OKLO "
         "CRWV NBIS IREN CIFR WULF APLD CORZ ORCL PLTR APP MSFT GOOGL META AMZN AAPL TSLA SNOW NOW CRM ADBE SKHY ANT").split()
ETF = ("SMH SOXX XSD QQQ SPY IWM XLK VGT IGV AIQ BOTZ ARKK WGMI XLU HYG TLT GLD UUP SOXL SOXS TQQQ SQQQ "
       "USD TECL TECS NVDL NVDX NVDD NVDQ AMDL MUU TSLL PLTU SMCX DRAM").split()
ONCUL = ("^VIX ^VIX3M ^VIX9D ^VVIX ^SOX ^NDX ^GSPC ^TNX ^IRX DX-Y.NYB BTC-USD ETH-USD CL=F GC=F HG=F NQ=F ES=F "
         "JPY=X KRW=X TWD=X 2330.TW 2317.TW 2454.TW 3711.TW 2382.TW 000660.KS 005930.KS 8035.T 6857.T 6920.T "
         "6146.T 9984.T 285A.T ASML.AS ASM.AS BESI.AS IFX.DE STMPA.PA 0981.HK ^KS11 ^TWII ^N225 ^STOXX50E").split()
TUMU = HEDEF + ETF + ONCUL
# Kod değişiklikleri (veriyle doğrulandı, 2026-11-21):
#  PSTG -> P : Pure Storage adını Everpure, Inc. yaptı; Yahoo'da PSTG boş, NYSE kodu "P".
TAKMA_AD = {"PSTG": "P"}


def dosya_adi(kod):
    return kod.replace("^", "_").replace("=", "_").replace("/", "_")


def _tek_indir(kod, saatlik, deneme=5):
    son_hata = None
    for i in range(deneme):
        try:
            if saatlik:
                df = yf.download(kod, period="730d", interval="1h", auto_adjust=False,
                                 progress=False, threads=False, prepost=False)
                if df.empty:
                    # yfinance, 730 günden yeni halka arzlarda başlangıcı ilk işlem gününe çekip
                    # Yahoo sınırına takılıyor; açık başlangıç tarihiyle yeniden dene.
                    bas = (pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=729)).strftime("%Y-%m-%d")
                    df = yf.download(kod, start=bas, interval="1h", auto_adjust=False,
                                     progress=False, threads=False, prepost=False)
            else:
                df = yf.download(kod, start="2010-01-01", interval="1d", auto_adjust=False,
                                 progress=False, threads=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
        except Exception as e:  # ağ hatası
            son_hata = e
            time.sleep(2 * (i + 1))
    print(f"  {kod}: 5 denemede indirilemedi: {son_hata}")
    return pd.DataFrame()


def son_gun_yamasi(kod, df):
    """Son satırda Close=NaN ama Open/High/Low dolu ise (ör. SNDK 2026-11-20, 8:1 bölünme günü
    Yahoo kapanışı boş) kapanışı AYNI GÜNÜN 1 saatlik son barının kapanışından alır.
    Bu ileri doldurma değildir (önceki günün fiyatı taşınmaz); 'yama' sütununda işaretlenir.
    Saatlik son bar kapanışı resmi kapanış müzayedesinden birkaç sent farklı olabilir."""
    df["yama"] = ""
    son = df.index[-1]
    if pd.isna(df["Close"].iloc[-1]) and pd.notna(df["Open"].iloc[-1]):
        h = _tek_indir(kod, saatlik=True)
        if not h.empty:
            hi = pd.to_datetime(h.index)
            hi = hi.tz_convert("America/New_York") if hi.tz is not None else hi
            gun = h[hi.normalize().tz_localize(None) == pd.Timestamp(son).tz_localize(None).normalize()]
            if len(gun):
                df.loc[son, "Close"] = float(gun["Close"].iloc[-1])
                df.loc[son, "AdjClose"] = df.loc[son, "Close"]
                df.loc[son, "yama"] = "Close=saatlik_son_bar"
                print(f"  {kod}: {str(son)[:10]} Close boştu -> saatlik son bar {df.loc[son,'Close']:.2f}")
    return df


def gunluk_kaydet(kod, df):
    df = df.rename(columns={"Adj Close": "AdjClose"}).copy()
    df = son_gun_yamasi(kod, df)
    df = df.dropna(subset=["Close"])  # kalan boş satırlar atılır, doldurma yok
    df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
    df.index.name = "Date"
    if "AdjClose" not in df:
        df["AdjClose"] = df["Close"]
    df["carpan"] = df["AdjClose"] / df["Close"]
    for c in ["Open", "High", "Low", "Close"]:
        df["A" + c] = df[c] * df["carpan"]
    cols = ["Open", "High", "Low", "Close", "AdjClose", "Volume", "carpan", "AOpen", "AHigh", "ALow", "AClose", "yama"]
    df[cols].to_csv(VERI / "gunluk" / f"{dosya_adi(kod)}.csv")
    return df


def saatlik_kaydet(kod, df):
    df = df.rename(columns={"Adj Close": "AdjClose"}).dropna(subset=["Close"]).copy()
    idx = pd.to_datetime(df.index)
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    df.index = idx.tz_convert("America/New_York")
    df.index.name = "Datetime"
    df.to_csv(VERI / "saatlik" / f"{dosya_adi(kod)}.csv")
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kodlar", nargs="*")
    ap.add_argument("--saatlik", action="store_true")
    a = ap.parse_args()
    kodlar = [TAKMA_AD.get(k, k) for k in (a.kodlar or (HEDEF + ETF if a.saatlik else TUMU))]
    alt = "saatlik" if a.saatlik else "gunluk"
    (VERI / alt).mkdir(parents=True, exist_ok=True)
    kapsam_yol = VERI / f"kapsam_{alt}.csv"
    eski = pd.read_csv(kapsam_yol, index_col=0) if kapsam_yol.exists() else pd.DataFrame()
    satirlar = {}
    for k in kodlar:
        df = _tek_indir(k, a.saatlik)
        if df is None or df.empty or df["Close"].dropna().empty:
            satirlar[k] = dict(ilk=None, son=None, n=0, son_close_nan=None, not_="BOŞ")
            print(f"  {k}: BOŞ")
            continue
        ham_son = pd.to_datetime(df.index[-1])
        son_nan = bool(pd.isna(df["Close"].iloc[-1]))
        d = saatlik_kaydet(k, df) if a.saatlik else gunluk_kaydet(k, df)
        satirlar[k] = dict(ilk=str(d.index[0])[:19], son=str(d.index[-1])[:19], n=len(d),
                           son_close_nan=son_nan, not_="")
        if son_nan:
            satirlar[k]["not_"] = f"ham son satır ({str(ham_son)[:10]}) Close=NaN"
            if not a.saatlik and (d["yama"] != "").any():
                satirlar[k]["not_"] += "; kapanış saatlik son bardan yamandı"
    yeni = pd.DataFrame(satirlar).T
    kapsam = pd.concat([eski.drop(index=[i for i in yeni.index if i in eski.index], errors="ignore"), yeni])
    kapsam.to_csv(kapsam_yol)
    print(yeni.to_string())


if __name__ == "__main__":
    main()
