"""3. adım: yakalama kuralları ızgarası. Olay kuralları (slot=3) + rotasyon; sepet ve lider; XU100>200GHO filtresi.
Çıktı: cikti/izgara_olay.csv, izgara_rot.csv, islem_ozet.csv, yillik_*.csv"""
import os, sys, itertools, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import panel, kume_getiri, rf_gunluk
from kumeler import KUMELER
from dalga import dalgalar
import motor as M
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
SON = os.environ.get("SON")
COST = float(os.environ.get("COST", "0.0025")); LAG = int(os.environ.get("LAG", "1"))
SUF = os.environ.get("SUF", "")
P, R, sup = panel(SON)
C, NU = kume_getiri(R)
rf, _ = rf_gunluk(C.index)
V = M.Veri(P, R, C, NU, rf, KUMELER)
usd = P["USDTRY"].ffill()
BAS, BAS24 = "2012-01-02", "2024-01-02"
# dalgalar (taban tanım) -> yakalama
W = dalgalar(V.RelD.where(V.elig).loc["2011-06-01":], D=0.15, esik=0.30)
W["ia"] = [V.cal.get_loc(d) for d in W.dip]; W["ib"] = [V.cal.get_loc(d) for d in W.tepe]
W = W[W.dip >= pd.Timestamp(BAS)]
kidx = {c: i for i, c in enumerate(V.kumeler)}
lR = np.log(V.Rel)
def yakalama(S, L):
    """dalga başına: göreli log hareketin pozisyonda geçirilen payı (sinyal t, işlem t+1+L)."""
    sh = 1 + L; Se = np.zeros_like(S); Se[sh:] = S[:-sh]
    caps = []; tut = []
    dl = np.diff(lR, axis=0, prepend=np.nan)
    for _, w in W.iterrows():
        k = kidx[w.kume]; a, b = w.ia, w.ib
        tot = lR[b, k] - lR[a, k]
        got = np.nansum(Se[a + 1:b + 1, k] * dl[a + 1:b + 1, k])
        caps.append(got / tot); tut.append(Se[a + 1:b + 1, k].max() > 0)
    return np.array(caps), np.array(tut)
def yanlis_baslangic(tr):
    """işlem [giris, cikis] hiçbir dalganın [dip, tepe] aralığıyla çakışmıyorsa yanlış başlangıç."""
    fs = []
    for _, t in tr.iterrows():
        w = W[W.kume == t.kume]
        fs.append(not ((w.ia <= t.ib) & (w.ib >= t.ia)).any())
    return np.array(fs, bool)
rows = []; tr_all = {}; SER = {}
ENTRY_EXIT = [("rs63", "ma50"), ("rs63", "rstr10"), ("rs63", "tr15"), ("rs63", "ma50|tr15"),
              ("rs126", "ma50"), ("rs126", "rstr10"), ("rs126", "tr15"), ("rs126", "ma50|tr15"),
              ("rs63br", "ma50"), ("rs63br", "rstr10"), ("rs63br", "tr15"),
              ("br70", "br40"), ("br70", "ma50"), ("br70", "tr15"),
              ("dm6", "dm"), ("dm6", "tr15"), ("dm3", "dm"), ("dm3", "tr15")]
for (g, x), f in itertools.product(ENTRY_EXIT, [0, 1]):
    S = M.durum_makinesi(V, g, x, f)
    caps, tut = yakalama(S, LAG)
    for lid in (False, True):
        tr = M.islemler(V, S, L=LAG, c=COST, lider=lid)
        tr = tr[tr.giris >= pd.Timestamp(BAS)]
        fs = yanlis_baslangic(tr) if len(tr) else np.array([])
        r, inv, to, _ = M.slot_portfoy(V, S, nslot=3, L=LAG, c=COST, lider=lid)
        o = M.olcu(r, inv, to, V, BAS, usd=usd); o24 = M.olcu(r, inv, to, V, BAS24, usd=usd)
        y = M.yillik(r.loc[BAS:], V)
        key = f"{g}|{x}|f{f}|{'lider' if lid else 'sepet'}"
        SER['O:' + key] = r; SER['O:' + key + ':inv'] = inv
        rel = (1 + tr.getiri) / (1 + tr.xu100) - 1
        rows.append(dict(kural=key, giris=g, cikis=x, filtre=f, surum="lider" if lid else "sepet",
                         n_islem=len(tr), islem_yil=len(tr) / ((V.cal[-1] - pd.Timestamp(BAS)).days / 365.25),
                         ort_gun=tr.gun.mean(), isabet_xu=(rel > 0).mean(), isabet_abs=(tr.getiri > tr.rf).mean(),
                         ort_net=tr.getiri.mean(), med_net=tr.getiri.median(), ort_rel=rel.mean(),
                         yanlis_bas=fs.mean() if len(fs) else np.nan,
                         dalga_tutulan=tut.mean(), yakalama_ort=np.nanmean(caps), yakalama_med=np.nanmedian(caps),
                         **{k: v for k, v in o.items()}, **{k + "_24": v for k, v in o24.items()},
                         yil_xu_yenen=(y.strateji > y.xu100).mean(), yil_rf_yenen=(y.strateji > y.rf).mean()))
        tr_all[key] = tr.assign(yanlis=fs)
        y.to_csv(os.path.join(OUT, "yillik", f"olay_{key.replace('|', '_')}{SUF}.csv"), float_format="%.4f") if os.path.isdir(os.path.join(OUT, "yillik")) else None
    print(key, f"cagr={o['cagr']:.3f} a_rf={o['a_rf']:.3f} a_xu={o['a_xu']:.3f} yb={rows[-1]['yanlis_bas']:.2f} cap={np.nanmean(caps):.2f}", flush=True)
G = pd.DataFrame(rows); G.to_csv(os.path.join(OUT, f"izgara_olay{SUF}.csv"), index=False, float_format="%.4f")
pd.concat([t.assign(kural=k) for k, t in tr_all.items()]).drop(columns=["ia", "ib", "k"]).to_csv(
    f"/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_bist/islemler_olay{SUF}.csv", index=False)
# ---- rotasyon ----
rows = []
for skor, K, fr, absf, mktf, lid, buf in itertools.product(["r21", "r63", "r126", "komp"], [2, 3], ["W", "M"], [0, 1], [0, 1], [0, 1], [0, 2]):
    r, inv, to, We = M.rotasyon(V, skor, K, fr, bool(absf), bool(mktf), bool(lid), buf, L=LAG, c=COST)
    o = M.olcu(r, inv, to, V, BAS, usd=usd); o24 = M.olcu(r, inv, to, V, BAS24, usd=usd)
    y = M.yillik(r.loc[BAS:], V)
    key = f"{skor}|K{K}|{fr}|abs{absf}|mkt{mktf}|{'lider' if lid else 'sepet'}|buf{buf}"
    SER['R:' + key] = r; SER['R:' + key + ':inv'] = inv
    # dalga yakalama: ağırlık>0 durumunu pozisyon say (sinyal hizası: We zaten kaydırılmış -> L=-1 eşleniği)
    S = (We > 0).astype(np.int8); Sx = np.zeros_like(S); Sx[:-(1 + LAG)] = S[1 + LAG:]
    caps, tut = yakalama(Sx, LAG)
    rows.append(dict(kural=key, skor=skor, K=K, frekans=fr, absf=absf, mktf=mktf, surum="lider" if lid else "sepet", buf=buf,
                     dalga_tutulan=tut.mean(), yakalama_ort=np.nanmean(caps),
                     **o, **{k + "_24": v for k, v in o24.items()},
                     yil_xu_yenen=(y.strateji > y.xu100).mean(), yil_rf_yenen=(y.strateji > y.rf).mean()))
    print(key, f"cagr={o['cagr']:.3f} a_rf={o['a_rf']:.3f} a_xu={o['a_xu']:.3f} 24: {o24['cagr']:.3f}", flush=True)
G2 = pd.DataFrame(rows); G2.to_csv(os.path.join(OUT, f"izgara_rot{SUF}.csv"), index=False, float_format="%.4f")
# ---- kıyas: tüm kümeler eşit ağırlık (zamanlama yok), XU100, rf ----
Wb = np.where(V.elig & (V.yas >= 130), 1.0, 0.0); Wb = Wb / np.maximum(Wb.sum(1, keepdims=True), 1)
Wx = np.zeros_like(Wb); Wx[2:] = Wb[:-2]
rb = pd.Series((Wx * np.nan_to_num(V.C)).sum(1), index=V.cal)
xr = pd.Series(V.Rm, index=V.cal)
SER['EW_tum_kumeler'] = rb; SER['XU100'] = xr; SER['rf'] = pd.Series(V.rf, index=V.cal)
pd.DataFrame(SER).to_parquet(f"/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_bist/seriler{SUF}.parquet")
for ad, s in [("EW_tum_kumeler", rb), ("XU100", xr)]:
    o = M.olcu(s, pd.Series(1.0, index=V.cal), pd.Series(0.0, index=V.cal), V, BAS, usd=usd)
    o24 = M.olcu(s, pd.Series(1.0, index=V.cal), pd.Series(0.0, index=V.cal), V, BAS24, usd=usd)
    print(ad, {k: round(v, 3) for k, v in o.items()}, "| 2024+:", {k: round(v, 3) for k, v in o24.items()})
    M.yillik(s.loc[BAS:], V).to_csv(os.path.join(OUT, f"kiyas_yillik_{ad}{SUF}.csv"), float_format="%.4f")
