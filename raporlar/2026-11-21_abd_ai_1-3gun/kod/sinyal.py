"""Gunluk sinyal araci (bagimsiz; yalniz pandas, numpy, yfinance).

Tanimlar kod/PROTOKOL.md ve kod/yeniden_kodlama.py ile ayni (ortak.py kullanilmaz):
  IBS = (C-L)/(H-L)                      F1a: IBS < 0,2 -> kapanista al, ertesi kapanista sat
  dusuk kapanis serisi (C_t < C_t-1 ...)  F3 : seri >= 3 -> al, 1 gun
  r / sigma60 (sigma: t-1'e kadar 60 gun)  F4b: r > +2 sigma -> UZAK DUR
  ^SOX gunluk degisim                     F11a: <= -%3 -> SMH al; F11b: >= +%3 -> SMH UZAK DUR
Sinyal kosulu: fiyat >= 3 $, 20 gunluk medyan ciro >= 20 milyon $, >= 250 gun gecmis, bozuk bar yok;
hisselerde bilanco tepki gunu [t, t+1] icindeyse F1a/F3 islemi atlanir (protokol 2.4).

Kullanim:
  python kod/sinyal.py                       # Yahoo'dan son islem gunu kapanisi
  python kod/sinyal.py --tarih 2026-11-20    # belirli bir gunun kapanisi
  python kod/sinyal.py --saat 1530           # 15:30 fiyatiyla (kapanistan once karar), saatlik veri
  python kod/sinyal.py --yerel veri/gunluk   # Yahoo yerine yerel CSV (sagleme icin)
"""
import argparse
import os
import sys
import numpy as np
import pandas as pd

T_EVREN = ["SMH", "SOXX", "QQQ", "XLK", "SPY", "IWM"]
KALDIRACLI = ["SOXL", "TQQQ", "USD", "TECL", "NVDL", "AMDL", "MUU", "DRAM"]
HISSE = ["NVDA", "AMD", "AVGO", "TSM", "MU"]
REJIM = ["^VIX", "^VIX3M", "^SOX"]
HEPSI = T_EVREN + KALDIRACLI + HISSE + REJIM
BURADA = os.path.dirname(os.path.abspath(__file__))
BILANCO_DIZIN = os.path.join(os.path.dirname(BURADA), "veri", "bilanco")

# Gecmis test ozeti (yeniden_kodlama.py ile bagimsiz olarak dogrulandi; 2010-2026, h=1)
TEST_NOTU = {
    "F1a": "T havuzu: alfa +17 bps/islem, net +7 (t 3,08). Kaldiracli/hisse: yalniz betimsel tasima.",
    "F3": "T havuzu: alfa +19 bps (t 2,61), ADAY.",
    "F11a": "SMH: alfa +43 bps (t 2,13, n 226), ADAY.",
    "F4b": "T havuzu: alfa -41 bps (t -2,28) -> o gun ALMA.",
    "F11b": "SMH: alfa -42 bps (t -2,44) -> o gun SMH ALMA.",
}


# ---------------- veri ----------------
def yahoo_gunluk(kodlar, bitis):
    import yfinance as yf
    bas = (pd.Timestamp(bitis) - pd.Timedelta(days=800)).strftime("%Y-%m-%d")
    son = (pd.Timestamp(bitis) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    ham = yf.download(kodlar, start=bas, end=son, auto_adjust=False, group_by="ticker",
                      progress=False, threads=True, actions=False)
    out = {}
    for k in kodlar:
        try:
            d = ham[k].copy()
        except KeyError:
            continue
        d = d.rename(columns={"Adj Close": "AdjClose"}).dropna(subset=["Close"])
        if len(d):
            d.index = pd.to_datetime(d.index).tz_localize(None)
            out[k] = d[["Open", "High", "Low", "Close", "AdjClose", "Volume"]]
    return out


def yerel_gunluk(dizin, kodlar, bitis):
    out = {}
    for k in kodlar:
        yol = os.path.join(dizin, k.replace("^", "_").replace("=", "_") + ".csv")
        if os.path.exists(yol):
            d = pd.read_csv(yol, parse_dates=["Date"]).set_index("Date").sort_index()
            out[k] = d.loc[: pd.Timestamp(bitis), ["Open", "High", "Low", "Close", "AdjClose", "Volume"]]
    return out


def yahoo_1530(kodlar, tarih):
    """Her kod icin {acilis, H(09:30-14:30), L(09:30-14:30), P1530}. Yarim gun / eksikse yok."""
    # 60m barlar 09:30, 10:30 ... 15:30'da baslar (protokol 7.1). ^VIX saatlik barlari tam saatte (03:00...)
    # basladigi icin 15:30 bari yoktur; o zaman 30m barlarla ayni an (15:30 acilisi, H/L 09:30-15:30 arasi) kullanilir.
    # 30m veri Yahoo'da yalniz ~60 gun geriye gider.
    import yfinance as yf
    t = pd.Timestamp(tarih)
    out = {}
    for aralik, ust in (("60m", "14:30"), ("30m", "15:00")):
        eksik = [k for k in kodlar if k not in out]
        if not eksik:
            break
        try:
            ham = yf.download(eksik, start=t.strftime("%Y-%m-%d"), end=(t + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
                              interval=aralik, auto_adjust=False, group_by="ticker", progress=False, prepost=False)
        except Exception:
            continue
        for k in eksik:
            try:
                d = ham[k].dropna(subset=["Open"])
            except KeyError:
                continue
            if not len(d):
                continue
            idx = d.index.tz_convert("America/New_York") if d.index.tz is not None else d.index
            d = d.set_axis(idx.strftime("%H:%M"))
            if "15:30" not in d.index:
                continue
            on = d.loc[[s for s in d.index if "09:30" <= s <= ust]]
            if not len(on):
                continue
            out[k] = dict(Open=float(on["Open"].iloc[0]), High=float(on["High"].max()), Low=float(on["Low"].min()),
                          Close=float(d.loc["15:30", "Open"]), aralik=aralik)
    return out


def sentetik_ekle(d, bar, tarih):
    """t gununu 15:30 bariyla degistir/ekle (duzeltme carpani 1)."""
    t = pd.Timestamp(tarih)
    d = d.loc[d.index < t].copy()
    vol_tah = d["Volume"].iloc[-20:].median()  # hacim bilinmiyor: ciro filtresi icin 20 gunluk medyan
    yeni = pd.DataFrame([dict(Open=bar["Open"], High=max(bar["High"], bar["Close"]), Low=min(bar["Low"], bar["Close"]),
                              Close=bar["Close"], AdjClose=bar["Close"], Volume=vol_tah)], index=[t])
    return pd.concat([d, yeni])


# ---------------- hesap ----------------
def gostergeler(d):
    """Vektorel gostergeler (her gun icin)."""
    carp = d["AdjClose"] / d["Close"]
    ah, al, ac = d["High"] * carp, d["Low"] * carp, d["AdjClose"]
    o, h, l, c = d["Open"], d["High"], d["Low"], d["Close"]
    g = pd.DataFrame(index=d.index)
    g["kapanis"] = c
    g["r"] = ac.pct_change()
    g["ibs"] = (ac - al) / (ah - al)
    dn = (ac < ac.shift(1)).astype(int)
    g["seri"] = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
    g["sigma60"] = g["r"].shift(1).rolling(60).std()
    g["z"] = g["r"] / g["sigma60"]
    bozuk = (h < np.maximum(o, c)) | (l > np.minimum(o, c)) | (h == l)
    ciro = c * d["Volume"]
    g["ciro_med20"] = ciro.rolling(20).median()
    g["gecmis"] = np.arange(len(d)) >= 250
    g["uygun"] = (~bozuk) & (c >= 3) & (g["ciro_med20"] >= 20e6) & g["gecmis"]
    g["zirve250"] = ac.rolling(250, min_periods=120).max()
    g["zirveden"] = ac / g["zirve250"] - 1
    return g


def bilanco_yakin(kod, tarih, sonraki):
    """Tepki gunu [t, t+1] icinde mi? (protokol 2.4; yerel bilanco dosyasindan, yoksa yfinance takvimi)."""
    t, t1 = pd.Timestamp(tarih), pd.Timestamp(sonraki)
    tarihler = []
    yol = os.path.join(BILANCO_DIZIN, kod + ".csv")
    if os.path.exists(yol):
        b = pd.read_csv(yol, parse_dates=["tarih"])
        for _, s in b.iterrows():
            d = s.tarih.normalize()
            if s.zaman == "sonra":
                r = d + pd.offsets.BDay(1)
            else:
                r = d if d.weekday() < 5 else d + pd.offsets.BDay(1)
            tarihler.append(r)
    else:
        try:
            import yfinance as yf
            ed = yf.Ticker(kod).get_earnings_dates(limit=8)
            for ts in ed.index:
                ts = ts.tz_convert("America/New_York")
                d = pd.Timestamp(ts.date())
                tarihler.append(d + pd.offsets.BDay(1) if ts.hour >= 16 else d)
        except Exception:
            return None
    return any(t <= r <= t1 for r in tarihler)


def ana():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tarih", default=None, help="YYYY-AA-GG (varsayilan: son islem gunu)")
    ap.add_argument("--saat", default=None, choices=["1530"], help="15:30 fiyatiyla hesapla")
    ap.add_argument("--yerel", default=None, help="Yahoo yerine yerel gunluk CSV dizini")
    ap.add_argument("--cikti", default=None)
    a = ap.parse_args()

    bitis = pd.Timestamp(a.tarih) if a.tarih else pd.Timestamp.today().normalize()
    veri = yerel_gunluk(a.yerel, HEPSI, bitis) if a.yerel else yahoo_gunluk(HEPSI, bitis)
    if "SMH" not in veri:
        sys.exit("SMH verisi alinamadi.")
    t = veri["SMH"].index[-1] if not a.tarih else pd.Timestamp(a.tarih)
    if t not in veri["SMH"].index and not a.saat:
        sys.exit(f"{t.date()} islem gunu degil ya da veri yok.")
    notlar = []
    if a.saat:
        if a.yerel:
            sys.exit("--saat yalniz Yahoo ile calisir.")
        barlar = yahoo_1530(list(veri), t)
        if "SMH" not in barlar:
            sys.exit(f"{t.date()} icin 15:30 bari yok (yarim gun ya da 730 gunden eski).")
        for k in list(veri):
            if k in barlar:
                veri[k] = sentetik_ekle(veri[k], barlar[k], t)
            else:
                notlar.append(f"{k}: 15:30 bari yok, satir atlandi.")
                veri.pop(k)
        notlar.append("15:30 modu: 'kapanis' = 15:30 barinin acilisi; H/L 09:30-14:30 barlari; "
                      "ciro filtresi icin t hacmi = 20 gunluk medyan. Giris yine kapanista (B senaryosu).")

    G = {k: gostergeler(d) for k, d in veri.items() if len(d)}
    sonraki = t + pd.offsets.BDay(1)

    def deger(k, s):
        g = G.get(k)
        if g is None or t not in g.index:
            return np.nan
        return g.at[t, s]

    vix, vix3m = deger("^VIX", "kapanis"), deger("^VIX3M", "kapanis")
    sox = deger("^SOX", "r")
    smh_z = deger("SMH", "zirveden")
    stres = bool(vix >= 30) if pd.notna(vix) else None
    bugun = bool(stres and smh_z <= -0.25) if stres is not None else None
    evet = lambda b: "BILINMIYOR (VIX yok)" if b is None else ("EVET" if b else "hayir")
    sat = []
    baslik = f"SINYAL RAPORU - {t.date()} {'15:30 fiyati' if a.saat else 'kapanis'}"
    sat.append(baslik)
    sat.append("=" * len(baslik))
    sat.append("")
    sat.append("REJIM")
    if pd.notna(vix) and pd.notna(vix3m):
        sat.append(f"  VIX {vix:.2f} | VIX/VIX3M {vix / vix3m:.3f} "
                   f"({'ters egri: VIX > VIX3M' if vix > vix3m else 'normal egri'})")
    else:
        sat.append(f"  VIX {vix:.2f} | VIX3M {vix3m:.2f} (eksik veri)")
    sat.append(f"  ^SOX gunluk {sox * 100:+.2f}% | SMH 250 gunluk zirveden {smh_z * 100:+.1f}%")
    sat.append(f"  STRES (VIX >= 30): {evet(stres)} | BUGUN (STRES ve SMH zirveden >= %25 asagi): {evet(bugun)}")
    sat.append("")
    sat.append("ARAC TABLOSU (r/sigma = gunluk getiri / onceki 60 gunun sigmasi)")
    sat.append(f"  {'Arac':<6} {'Grup':<10} {'Fiyat':>9} {'Gunluk':>8} {'r/sigma':>8} {'IBS':>5} {'Dusuk':>5} {'Uygun':>5}  Sinyal")
    acik = {"F1a": [], "F3": [], "F4b": []}
    for k in T_EVREN + KALDIRACLI + HISSE:
        g = G.get(k)
        if g is None or t not in g.index:
            sat.append(f"  {k:<6} veri yok")
            continue
        x = g.loc[t]
        grup = "T" if k in T_EVREN else ("kaldiracli" if k in KALDIRACLI else "hisse")
        uyg = bool(x.uygun)
        bil = bilanco_yakin(k, t, sonraki) if k in HISSE else False
        sin = []
        if uyg and x.ibs < 0.2:
            sin.append("F1a AL" if not bil else "F1a (bilanco: atla)")
        if uyg and x.seri >= 3:
            sin.append("F3 AL" if not bil else "F3 (bilanco: atla)")
        if uyg and x.z > 2:
            sin.append("F4b UZAK DUR")
        if not uyg:
            neden = []
            if not x.gecmis:
                neden.append(f"gecmis {int(g.index.get_loc(t)) + 1} gun < 250")
            if x.kapanis < 3:
                neden.append("fiyat < 3 $")
            if not (x.ciro_med20 >= 20e6):
                neden.append(f"medyan ciro {x.ciro_med20 / 1e6:.0f} mn $ < 20")
            sin.append("sinyal sayilmaz: " + (", ".join(neden) or "bozuk bar"))
        if bil is None:
            sin.append("bilanco tarihi bilinmiyor")
        elif bil:
            sin.append("bilanco [t,t+1]")
        for s in ("F1a", "F3", "F4b"):
            if any(z.startswith(s + " ") and ("AL" in z or "UZAK" in z) for z in sin):
                acik[s].append(k)
        sat.append(f"  {k:<6} {grup:<10} {x.kapanis:>9.2f} {x.r * 100:>+7.2f}% {x.z:>+8.2f} {x.ibs:>5.2f} "
                   f"{int(x.seri):>5d} {'evet' if uyg else 'HAYIR':>5}  {', '.join(sin) if sin else '-'}")
    sat.append("")
    sat.append("ACIK KURALLAR")
    sat.append(f"  F1a (IBS < 0,2) AL          : {', '.join(acik['F1a']) or 'yok'}   [{TEST_NOTU['F1a']}]")
    sat.append(f"  F3  (>= 3 dusuk kapanis) AL : {', '.join(acik['F3']) or 'yok'}   [{TEST_NOTU['F3']}]")
    smh_uyg = bool(deger("SMH", "uygun")) if "SMH" in G else False
    f11a = pd.notna(sox) and sox <= -0.03 and smh_uyg
    f11b = pd.notna(sox) and sox >= 0.03
    sat.append(f"  F11a (^SOX <= -%3) SMH AL   : {'EVET' if f11a else 'hayir'}   [{TEST_NOTU['F11a']}]")
    sat.append(f"  KACINMA F4b (> +2 sigma)    : {', '.join(acik['F4b']) or 'yok'}   [{TEST_NOTU['F4b']}]")
    sat.append(f"  KACINMA F11b (^SOX >= +%3)  : {'EVET - SMH alma' if f11b else 'hayir'}   [{TEST_NOTU['F11b']}]")
    sat.append("")
    sat.append("NOTLAR")
    sat.append("  - Giris: sinyal gunu kapanisi (15:55-15:59 emri), cikis: ertesi islem gunu kapanisi. Maliyet T: 10 bps gidis-donus.")
    sat.append("  - Testler yalniz T ETF havuzunda (ve F11 icin SMH) yapildi; kaldiracli ETF ve tek hisse satirlari betimseldir.")
    sat.append("  - 'Uygun = HAYIR': fiyat < 3 $, medyan ciro < 20 milyon $, < 250 gun gecmis ya da bozuk bar -> sinyal yok sayilir.")
    for n in notlar:
        sat.append("  - " + n)
    metin = "\n".join(sat)
    print(metin)
    if a.cikti:
        open(a.cikti, "w").write(metin + "\n")


if __name__ == "__main__":
    ana()
