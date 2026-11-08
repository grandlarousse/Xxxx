"""6) Birleşik test sayısı / BH-FDR ve sonuc.json üretimi. Önce 01-05 çalışmış olmalı. Çalıştır:
   python3 -I kod/ajan_abd_endeks/06_sonuc_json.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ae, lib
from scipy import stats as st

O = ae.OUT; R = ae.ROOT
def rd(n): return pd.read_csv(os.path.join(O, n))

# ---------------- birleşik test kümesi ----------------
g = pd.read_csv(os.path.join(R, "sonuclar", "genel_tum.csv")); g = g[g.sym.isin(ae.FAM)]
P = [("genel_aile", g["p"].values)]
h03 = rd("hipotez_testleri.csv"); P.append(("hipotez_03", h03["p"].values))
for f in ("leadlag_catch_backtest.csv", "leadlag_reel_faiz_backtest.csv", "leadlag_tip_backtest.csv"):
    P.append((f, rd(f)["p"].values))
cr = rd("leadlag_catch_kontrollu.csv")
P.append(("catch_kontrollu", np.r_[2 * st.norm.sf(cr["catch_t_kontrollu_h1"].abs()), 2 * st.norm.sf(cr["catch_t_kontrollu_h3"].abs())]))
allp = np.concatenate([p for _, p in P]); mask = lib.bh_fdr(allp, 0.10)
n_tot = int(np.isfinite(allp).sum())
# BH eşiği: geçen en büyük p
thr = float(np.nanmax(allp[mask])) if mask.any() else np.nan
nb = len(rd("aday_S1_komsu_parametre.csv")); nlev = len(rd("aday_S1_kaldiracli.csv"))
print("Birleşik test sayısı:", n_tot, " (", {k: int(np.isfinite(v).sum()) for k, v in P}, ")")
print("Ek sağlamlık yeniden-değerlendirmeleri (komşu parametre + kaldıraçlı araç):", nb + nlev)
print(f"Birleşik BH-FDR q=0.10: {int(mask.sum())} geçti; geçiş için p eşiği ≈ {thr:.5f}")

# Tek yönlü (yalnız "net>0") BH: maliyet nedeniyle anlamlı NEGATİF çıkan binlerce satır iki yönlü BH eşiğini gevşetir; katı kontrol için.
def one_sided(t, n): return np.where(np.isfinite(t), st.t.sf(t, np.maximum(np.asarray(n) - 1, 1)), np.nan)
p1_all = np.r_[one_sided(g.t.values, g.n.values), one_sided(h03.t.values, h03.n.values)]
m1_all = lib.bh_fdr(p1_all, 0.10)
p1_03 = one_sided(h03.t.values, h03.n.values); m1_03 = lib.bh_fdr(p1_03, 0.10)
ONE_TXT = (f"Katı kontrol (tek yönlü 'net>0' BH): genel+hipotez {int(np.isfinite(p1_all).sum())} testte geçen {int(m1_all.sum())}; "
           f"yalnız odaklı hipotez setimde (03, {len(p1_03)} test) geçen {int(m1_03.sum())} — hepsi QQQ IBS<0,10 satırları. ")
print(ONE_TXT)
a = rd("aday_ozet.csv")
def pick(aday, sym, mode):
    r = a[(a.aday == aday) & (a.sym == sym) & (a["mode"] == mode)].iloc[0]
    return r
def fdr_ok(p): return bool(np.isfinite(p) and p <= thr)

S1 = {m: pick("S1", "SPY", m) for m in ("C0", "O1", "C1")}
S2 = {m: pick("S1", "QQQ", m) for m in ("C0", "O1", "C1")}
S3 = {m: pick("S2", "SPY", m) for m in ("C0", "O1", "C1")}
S3q = {m: pick("S2", "QQQ", m) for m in ("C0", "O1", "C1")}
for nm, d, m in (("S1 SPY", S1, "C1"), ("S2 QQQ", S2, "C1"), ("S3 SPY", S3, "C0"), ("S3 QQQ", S3q, "C0")):
    r = d[m]
    print(f"{nm} {m}: n={r.n:.0f} brüt={r.mean_gross_bp:.1f} net={r.mean_net_bp:.1f} t={r.t:.2f} p={r.p:.4f} birleşik FDR={'GEÇTİ' if fdr_ok(r.p) else 'geçmedi'}")
lv = rd("aday_S1_kaldiracli.csv")

def mstr(d):
    return "; ".join(f"{m}: brüt {d[m].mean_gross_bp:.0f} bp, net {d[m].mean_net_bp:.0f} bp, t={d[m].t:.2f}" for m in ("C0", "O1", "C1"))
def cstr(r):
    return f"1.000$: {r.net_bp_1000:.0f} bp | 2.500$: {r.mean_net_bp:.0f} bp | 10.000$: {r.net_bp_10000:.0f} bp (net, işlem başı)"
def fam(aday, mode):
    x = a[(a.aday.isin([aday, aday + "_faktor"])) & (a["mode"] == mode)]
    return ", ".join(f"{s} {n:.0f}bp/t{t:.1f}" for s, n, t in zip(x.sym, x.mean_net_bp, x.t))
def lvs(base, mode):
    x = lv[(lv.dayanak == base) & (lv["mode"] == mode)]
    return "; ".join(f"{s} ({k}x): net {n:.0f} bp, t={t:.2f}, maxDD {dd*100:.0f}%, en kötü işlem {w/100:.1f}%, en kötü gün {wd/100:.1f}%"
                     for s, k, n, t, dd, w, wd in zip(x.sym, x.kaldirac, x.mean_net_bp, x.t, x.maxdd, x.worst_bp, x.en_kotu_gun_bp))

TEST_SAYISI = n_tot
FDR_TXT = (f"Birleşik iki yönlü BH-FDR (q=0,10; {n_tot} test: genel kütüphane aile satırları + kendi testlerim) eşiği p≤{thr:.4f}. " + ONE_TXT)

def strat(id_, ad, kural, giris, tutus, cikis, islem, sinyal, d, mode, guven, notlar, aile_ici, extra_fdr=""):
    r = d[mode]
    return {"id": id_, "ad": ad, "kural": kural, "giris": giris, "tutus": tutus, "cikis": cikis, "islem_etf": islem,
            "sinyal_etf": sinyal, "n": int(r.n), "brut_bp": round(float(r.mean_gross_bp), 1), "net_bp": round(float(r.mean_net_bp), 1),
            "kazanma": round(float(r.win), 3), "pf": round(float(r.pf), 2), "t": round(float(r.t), 2),
            "is_net_bp": round(float(r.is_net_bp), 1), "oos_net_bp": round(float(r.oos_net_bp), 1),
            "yil_pozitif": round(float(r.years_pos_frac), 2), "maxdd": round(float(r.maxdd), 3), "en_kotu_bp": round(float(r.worst_bp), 0),
            "maliyet_duyarlilik": cstr(r), "mod_saglamlik": mstr(d), "aile_ici": aile_ici,
            "test_sayisi": TEST_SAYISI, "fdr": FDR_TXT + ("Bu satır GEÇTİ (p=%.4f). " % r.p if fdr_ok(r.p) else "Bu satır GEÇMEDİ (p=%.4f). " % r.p) + extra_fdr,
            "guven": guven, "notlar": notlar + f" IS t={r.is_t:.2f}, OOS t={r.oos_t:.2f}.",
            "betik": "python3 -I kod/ajan_abd_endeks/05_adaylar.py (sayıları basar; önce 01-04 gerekmez)"}

TV_PINE = "Pine: ibs=(close-low)/(high-low); sinyal = ibs<0.10 and close<close[1]"
k1 = ("TradingView günlük grafik AMEX:SPY (ayarlarda temettü düzeltmesi 'ADJ' açık). IBS=(kapanış−düşük)/(yüksek−düşük). "
      "SİNYAL (t günü kapanışı): IBS<0,10 VE kapanış<önceki günün kapanışı (gün düşüşle ve günün dibine çok yakın kapandı). "
      "İŞLEM: AMEX:SPY long (alternatif araç: AMEX:SSO 2x / AMEX:SPXL 3x — sinyal yine SPY verisinden). "
      "Ana mod C1: t+1 kapanışında al, 3 işlem günü sonra (t+4) kapanışta sat. Pozisyondayken gelen yeni sinyal yok sayılır. Stop yok. " + TV_PINE)
k2 = k1.replace("AMEX:SPY long (alternatif araç: AMEX:SSO 2x / AMEX:SPXL 3x — sinyal yine SPY verisinden)",
                "NASDAQ:QQQ long (alternatif araç: AMEX:QLD 2x / NASDAQ:TQQQ 3x — sinyal yine QQQ verisinden)").replace("grafik AMEX:SPY", "grafik NASDAQ:QQQ")
g_c1 = ("Sinyali t akşamı ABD kapanışından sonra (kış TR 00:00 / yaz 23:00) gör; ertesi işlem günü (t+1) kapanıştan 5-10 dk önce "
        "(kış TR ~23:50, yaz ~22:50) piyasa ya da agresif limit emriyle al (Midas'ta MOC/LOC yok). Alternatif C0: t günü TR ~23:50'de "
        "anlık fiyatla IBS<0,10 ve düşüş koşulu sağlanıyorsa aynı kapanışta al (hafif iyimser). O1 (t+1 açılışı TR 17:30 kış/16:30 yaz) daha zayıf.")
c_txt = ("Girişten 3 işlem günü sonra kapanıştan 5-10 dk önce sat (kış TR ~23:50, yaz ~22:50). Erken kapanış günlerinde (27 Kas 2026, 24 Ara 2026) "
         "kapanış 13:00 ET = TR 21:00. Erken çıkış kuralı yok.")
r1 = S1["C1"]; r2 = S2["C1"]
spy_vix = "VIX≥20 iken SPY C1 net 93 bp (t=2,75, n=83), VIX<20 iken 13 bp (t=0,75, n=72) — 7 filtre denendiği için yalnız bilgi, kurala eklenmedi."
STRATS = [
    strat("abd_endeks_S1", "Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) — S&P 500 / SPY, 3 gün", k1, g_c1, "3 işlem günü", c_txt,
          ["SPY", "SSO", "SPXL"], "SPY", S1, "C1", "orta",
          ("Aile genelinde en tutarlı sonuç: 19 grup temsilcisinin 19'unda C1 h=3 net>0, 18'inde IS ve OOS>0; 6 çekirdek endeks ETF'si sepeti t=2,44 (C1), "
           "SPY+QQQ+IWM sepeti t=2,77. Komşu eşikler (IBS 0,05-0,30, düşüş şartlı/şartsız) IS ve OOS'ta hep pozitif. Sinyal sonrası 1-4. günler ortalamanın üstünde, 5. gün negatif. Koşulsuz 3 günlük getiri 16 bp, kenar (edge) 53 bp (t=2,64). 2020 hariç C1 net 47 bp (t=2,79); 2024+ net 51 bp (t=1,54). "
           "Yılda ~16 işlem. "
           "ÖNEMLİ: etki piyasa geneli zayıf kapanışlarda — 19 temsilcinin ≥10'unun aynı gün sinyal verdiği 99 günde gün-ortalaması net 94 bp (t=3,55), 1-10 ETF'in sinyal verdiği günlerde ≈0; "
           "sinyal SPY'dan alınmalı (19 temsilci gün-sepeti t=1,23 bu yüzden düşük). "
           "SPY sinyaliyle başka ETF'de işlem (C1): QQQ 74 bp t=3,34; IWM 59 bp t=2,40; MDY 56 t=2,34; RSP 50 t=2,34; DIA 45 t=2,20 (sonradan bakıldı, bilgi). " + spy_vix +
           " Kaldıraçlı araç (C1): " + lvs("SPY", "C1") + ". Sabit komisyonda kaldıraç yalnız sermaye verimliliği sağlar (2.500$ SPXL ≈ 7.500$ SPY, aynı 3$), kuyruk riski 3 kat. Literatürle uyumlu: h=1'de net ~0 (Pandey & Joshi 2023), etki 2-4 günde. SPY-QQQ sinyallerinin %73'ü aynı gün."),
          fam("S1", "C1")),
    strat("abd_endeks_S2", "Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) — Nasdaq-100 / QQQ, 3 gün", k2, g_c1, "3 işlem günü", c_txt,
          ["QQQ", "QLD", "TQQQ"], "QQQ", S2, "C1", "orta",
          ("S1 ile aynı kural, Nasdaq-100 dayanağı; tüm modlarda t>2,9 (C0 3,68 / O1 2,94 / C1 3,46), IS ve OOS t>2. Kenar 60 bp (t=2,95), koşulsuz 3 günlük 23 bp. "
           "2020 hariç net 62 bp (t=3,03); 2024+ 70 bp (t=1,62). QQQ'nun 2016-2026 güçlü teknoloji trendi sonucu şişirmiş olabilir (aynı kural her endekste pozitif ama en güçlü QQQ'da: seçim yanlılığı riski). "
           "S1 ile sinyallerin %73'ü aynı gün: ikisini birlikte almak çeşitlendirme değil, riski ikiye katlar; birini seç ya da pozisyonu böl. "
           "QQQ'nun SPY'ın sinyal vermediği (yalnız teknoloji) günlerdeki sinyalleri C1'de zayıf (n=50, net 42 bp, t=1,49), C0'da güçlü (n=54, 95 bp, t=3,03). "
           "Kaldıraçlı araç (C1): " + lvs("QQQ", "C1") + ". TQQQ'da tek işlemde −%31 kayıp yaşandı (Mart 2020); kaldıraçlı kullanım yalnız küçük sermaye payıyla."),
          fam("S1", "C1")),
    strat("abd_endeks_S3", "3 ardışık düşüş sonrası al, ilk yükselen kapanışta sat (en çok 3 gün) — SPY",
          ("TradingView günlük AMEX:SPY (ADJ açık). SİNYAL (t kapanışı): close<close[1] VE close[1]<close[2] VE close[2]<close[3] (3 ardışık düşen kapanış; trend filtresi yok). "
           "İŞLEM: AMEX:SPY long, C0: t kapanışında al. ÇIKIŞ: sonraki ilk close>close[1] olan günün kapanışında, en geç 3. işlem günü kapanışında sat. "
           "Pine: sig = close<close[1] and close[1]<close[2] and close[2]<close[3]; cikis = close>close[1]"),
          ("t günü kapanıştan 5-10 dk önce (kış TR ~23:50, yaz ~22:50) anlık fiyatla 3. düşüş günü teyit edilirse al (C0 — kapanışa bağımlı). "
           "C1 (t+1 kapanışı) ve O1 (t+1 açılışı TR 17:30) brüt pozitif ama anlamsız."),
          "1-3 işlem günü (ilk yükselen kapanışa kadar)", "İlk yükselen kapanışta ya da en geç 3. gün kapanışında, kapanıştan 5-10 dk önce (TR ~23:50 kış / ~22:50 yaz).",
          ["SPY"], "SPY", S3, "C0", "dusuk",
          ("KAPANIŞA BAĞIMLI: C0'da t=2,32 ama O1 t=1,21, C1 t=1,52 (brüt pozitif). IS döneminde zayıf (IS net 14 bp, t=0,48), sonuç OOS'tan geliyor. "
           "Aile içinde tutarlı değil: 6 çekirdek ETF sepeti C0 t=1,95, O1 t=0,29, C1 t=−0,14; yalnız SPY ve QQQ (C0 52 bp, t=3,21) eşiği geçiyor, IWM/DIA/RSP/MDY t<1,3. "
           "S1 ile sinyal günlerinin yalnız ~%26'sı ortak (kısmen farklı fırsat). Hipotez AE05'teki SMA200 filtreli sürüm (3 düşüş & C>SMA200) eşiği GEÇMEDİ (medyan net 2 bp). "
           "Bu nedenle 'düşük güven' — ancak S1'i tamamlayıcı küçük pozisyon için."),
          fam("S2", "C0")),
]

# ---------------- izleme listesi ----------------
isl = rd("islenebilirlik.csv").set_index("sym")
def iz(sym, karar, gerekce):
    r = isl.loc[sym]
    return {"sym": sym, "karar": karar, "gerekce": gerekce, "tv": r.tv, "likidite_mn_usd": round(float(r.med_dollar_vol_m), 1),
            "maliyet_bp": round(float(r.cost_rt_bp), 1), "vol_1d_bp": round(float(r.vol_1d_bp), 1)}
s1f = a[(a.aday.isin(["S1", "S1_faktor"])) & (a["mode"] == "C1")].set_index("sym")
def s1txt(s):
    if s in s1f.index:
        r = s1f.loc[s]; return f"S1 kuralı bu ETF'de C1 h=3 net {r.mean_net_bp:.0f} bp (t={r.t:.1f})"
    return ""
INV_TXT = "Ters ETF: kısa yön sinyali yok (RSI2>90, 3 gün yükseliş, IBS>0,8 -> ters ETF testleri net negatif); 3 günde ≈{d:.0f} bp sıfırlama kaybı. Yalnız koruma amaçlı."
IZ = [
    iz("SPY", "kabul", "S&P 500 ana aracı: en likit (41,6 mlr$/gün), makas ~1 bp, maliyet/1g oynaklık 0,15. S1 (t=2,79) ve S3 burada. Sürücü/izleme: CME_MINI:ES1!."),
    iz("QQQ", "kabul", "Nasdaq-100 ana aracı: 30 mlr$/gün, maliyet/oynaklık 0,10 (ailede en iyi oranlardan). S2 (t=3,46). İzleme: CME_MINI:NQ1!."),
    iz("IWM", "yedek", "Russell 2000: likit (7,8 mlr$), maliyet/oynaklık 0,11. " + s1txt("IWM") + " — kendi sinyaliyle eşik altı (C0 t=0,8); SPY sinyaliyle IWM'de işlem C1 net 59 bp (t=2,40, sonradan bakıldı). Bağımsız küçük ölçek dayanağı. İzleme: CME_MINI:RTY1!."),
    iz("RSP", "yedek", "Eşit ağırlıklı S&P 500: " + s1txt("RSP") + ", IS/OOS pozitif; ancak SPY ile korelasyon yüksek ve günlük hareket dar (maliyet/oynaklık 0,17). S1 için SPY'a alternatif."),
    iz("DIA", "yedek", "Dow 30: " + s1txt("DIA") + "; SPY ile yüksek korelasyon, ayrı kanıt sayılmaz. SPY'a alternatif. İzleme: CBOT_MINI:YM1!."),
    iz("MDY", "yedek", "S&P 400 orta ölçek: " + s1txt("MDY") + "; makas 2 bp, 476 mn$/gün. IWM ile 0,92 korelasyon."),
    iz("SPXL", "yedek", "SPY 3x aracı (S1 sinyali SPY'dan): 526 mn$/gün, 3x maruziyet aynı 3$ komisyonla (sermaye verimliliği). Kuyruk: tek günde −%29, S1 işlemlerinde en kötü −%22,8, maxDD −%35. UPRO'dan daha likit."),
    iz("SSO", "yedek", "SPY 2x aracı: daha ılımlı kaldıraç (S1 C1 net 121 bp, t=3,0; en kötü işlem −%13,8). 3 günlük kaldıraç kaybı ≈2 bp."),
    iz("TQQQ", "yedek", "QQQ 3x aracı (S2 sinyali QQQ'dan): 4,7 mlr$/gün, maliyet/oynaklık 0,035. S2 C1 net 220 bp (t=3,5) ama en kötü işlem −%31, maxDD −%32. Midas bulunurluğu 'muhtemel' (resmî doğrulama yok)."),
    iz("QLD", "yedek", "QQQ 2x aracı: S2 C1 net 145 bp (t=3,5), en kötü işlem −%19,6. Midas bulunurluğu doğrulanmadı."),
    iz("VOO", "red", "SPY kopyası (korelasyon 0,997); 1-3 günlük işlemde SPY daha likit. Uzun vadeli tutuş için düşük gider oranı avantajı burada önemsiz."),
    iz("IVV", "red", "SPY kopyası (0,997); SPY tercih."),
    iz("VTI", "red", "Toplam piyasa ≈ S&P 500 (0,995); SPY tercih."),
    iz("QQQM", "red", "QQQ kopyası (0,9997); QQQ daha likit."),
    iz("UPRO", "red", "SPXL kopyası (0,9996); SPXL daha likit (aynı makas)."),
    iz("TNA", "red", "IWM 3x: IWM sinyali zayıf (S1 C0 t=0,8); TNA'da S1 C1 en kötü işlem −%35, maxDD −%40. Kuyruk riski kazancı haklı çıkarmıyor."),
    iz("URTY", "red", "TNA kopyası ve daha az likit (56 mn$)."),
    iz("UDOW", "red", "DIA 3x; DIA'nın kendisi yedek, S&P 3x (SPXL) daha likit."),
    iz("SH", "red", INV_TXT.format(d=2)), iz("SDS", "red", INV_TXT.format(d=7)), iz("SPXU", "red", INV_TXT.format(d=13)),
    iz("SPXS", "red", INV_TXT.format(d=13) + " SPXU kopyası."), iz("PSQ", "red", INV_TXT.format(d=5)), iz("QID", "red", INV_TXT.format(d=16) + " Makas 6 bp."),
    iz("SQQQ", "red", INV_TXT.format(d=33)), iz("TZA", "red", INV_TXT.format(d=25)), iz("SRTY", "red", INV_TXT.format(d=25) + " TZA kopyası, düşük likidite."),
    iz("SDOW", "red", INV_TXT.format(d=13)),
    iz("IWF", "red", "Büyük büyüme ≈ QQQ (0,98); " + s1txt("IWF") + " ama QQQ daha likit/ucuz — bağımsız kanıt değil."),
    iz("VUG", "red", "IWF/QQQ benzeri büyüme fonu (0,99); QQQ tercih."), iz("SCHG", "red", "Büyüme fonu kopyası (VUG 0,994); QQQ tercih."),
    iz("MGK", "red", "Mega büyüme ≈ VUG (0,997); makas 4 bp."),
    iz("IWD", "red", "Büyük değer: " + s1txt("IWD") + " ama günlük hareket dar (maliyet/oynaklık 0,19) ve SPY ile yüksek korelasyon; ayrı araç gerekmiyor."),
    iz("VTV", "red", "IWD kopyası (0,976); dar hareket (68 bp/gün)."), iz("VYM", "red", "Değer/temettü ≈ VTV (0,974); makas 4 bp, dar hareket."),
    iz("SCHD", "red", "Temettü: dar hareket (75 bp/gün, maliyet/oynaklık 0,20); " + s1txt("SCHD") + " (eşik altı)."),
    iz("DGRO", "red", "Temettü büyüme: dar hareket (65 bp), makas 4 bp."), iz("VIG", "red", "Temettü büyüme: dar hareket (68 bp)."),
    iz("DVY", "red", "Yüksek temettü: 58 mn$/gün, makas 4 bp, dar hareket; strateji yok."), iz("NOBL", "red", "Temettü aristokratları: düşük likidite (63 mn$), dar hareket."),
    iz("SPYD", "red", "Yüksek temettü: düşük likidite (57 mn$), makas 4 bp."),
    iz("SPLV", "red", "Düşük oynaklık: S1 çalışmıyor (C1 net 4 bp, OOS negatif); maliyet/oynaklık 0,20."),
    iz("USMV", "red", "Düşük oynaklık: 58 bp/gün, maliyet/oynaklık 0,28 — 1-3 gün için çok dar."),
    iz("SPHB", "red", "Yüksek beta: " + s1txt("SPHB") + " ama C0/O1 t≈1,4-1,5, makas 8 bp, 43 mn$/gün; aynı işlevi QQQ/SPXL daha ucuza görür. SPHB/SPLV göreli dönüşü eşiği geçmedi."),
    iz("MTUM", "red", "Momentum faktörü: " + s1txt("MTUM") + "; QQQ ile örtüşen maruziyet, gap payı yüksek (0,51)."),
    iz("QUAL", "red", "Kalite ≈ S&P 500 (0,97); SPY tercih."), iz("VLUE", "red", "Değer faktörü: makas 4 bp, 114 mn$/gün; S1 C0/O1'de zayıf."),
    iz("IWO", "red", "Küçük büyüme ≈ IWM (0,98); IWM daha likit."), iz("IWN", "red", "Küçük değer ≈ IWM (0,975); makas 4 bp."),
    iz("AVUV", "red", "Küçük değer (2019+), makas 4 bp; IWM/IWN ile örtüşür."), iz("COWZ", "red", "Nakit akışı faktörü: 74 mn$/gün, makas 4 bp, strateji yok."),
    iz("JEPI", "red", "Kapalı alım (covered call) fonu: yukarı hareket sınırlı, dar hareket (58 bp/gün, maliyet/oynaklık 0,24); S1 OOS'ta zayıf."),
    iz("JEPQ", "red", "Kapalı alım (NDX), 2022+ kısa geçmiş; QQQ dönüşünü kısmen keser."),
    iz("QYLD", "red", "Kapalı alım (NDX): makas ~6 bp, aylık dağıtım sıçramaları; lead-lag 'yetişme' FDR bulguları QYLD'nin kendi getirisindeki dönüşten (artefakt)."),
    iz("XYLD", "red", "Kapalı alım (S&P): 27 mn$/gün, makas 8 bp, 54 bp/gün — maliyet/oynaklık 0,37 (ailede en kötü)."),
]
assert len(IZ) == 55, len(IZ)
assert set(x["sym"] for x in IZ) == set(ae.FAM)

# ---------------- lead-lag ----------------
lo = rd("leadlag_aile_ozet.csv")
def surucu(T, n=4):
    e = lo[(lo.target == T) & (lo.tip == "eszamanli_surucu")].head(n)
    return [{"ad": l.replace("_dlog", " (log değişim)").replace("VIXTS_d", "VIX/VIX3M oranı değişimi"), "tv": tv, "corr_1y": round(c, 2), "beta_1y": round(b, 2)}
            for l, tv, c, b in zip(e.leader, e.tv, e.corr_1y, e.beta_1y)]
def best_lag(T):
    d = lo[(lo.target == T) & lo.tip.str.startswith("gecikmeli")]
    d = d.reindex(d.t.abs().sort_values(ascending=False).index).head(2)
    return "; ".join(f"{l} ({tp.split('_')[1]}): t={t:.2f}, IS {a_:.1f}/OOS {b_:.1f}, {bp:.0f} bp/sd" for l, tp, t, a_, b_, bp in zip(d.leader, d.tip, d.t, d.t_is, d.t_oos, d.bp_per_sd))
RT = {"SPY": [("S&P 500 E-mini vadeli", "CME_MINI:ES1!", "CME Globex'te Pazar-Cuma ~23 saat işler (ABD kış saatinde TR 02:00'den ertesi gün 01:00'e; 01:00-02:00 bakım arası, yaz saatinde 00:00-01:00); TR 12:00-17:30 arasında SPY açılış boşluğunu önceden gösterir (SPY varyansının ~%40'ı gece)."),
                ("VIX vadeli (ön ay)", "CBOE:VX1!", "Neredeyse 24 saat işler; gece risk iştahı/stres göstergesi."),
                ("Nikkei 225 vadeli (OSE)", "OSE:NK2251!", "OSE gündüz seansı TR 02:45-09:15, gece seansı TR 10:30-00:00: ABD kapalıyken küresel risk duyarlılığı."),
                ("DAX vadeli", "EUREX:FDAX1!", "Xetra nakit seansı TR 11:00-19:30 (Avrupa kış saati; yaz saatinde 10:00-18:30), FDAX vadelisi ~TR 03:10-00:00: ABD açılışından önce risk iştahı; Bondarenko & Muravyev gece getirisinin Avrupa açılışı civarında yoğunlaştığını bulmuş."),
                ("USD/JPY", "FX_IDC:USDJPY", "Gece risk-off (yen güçlenmesi) göstergesi; 5 Ağu 2024 tipi taşıma ticareti çözülmeleri."),
                ("ABD 10 yıllık getiri", "TVC:US10Y", "Faiz şoku (CPI/NFP TR 16:30) açılıştan önce görülür.")],
      "QQQ": [("Nasdaq-100 E-mini vadeli", "CME_MINI:NQ1!", "CME Globex ~23 saat (ES1! ile aynı saatler); QQQ açılış boşluğunu önceden gösterir (QQQ varyansının ~%42'si gece)."),
              ("VIX vadeli (ön ay)", "CBOE:VX1!", "Gece stres göstergesi."),
              ("NVIDIA (hisse, pre-market)", "NASDAQ:NVDA", "Pre-market (TR 12:00-17:30) ve kazanç sonrası after-hours hareketi QQQ'nun en büyük tekil sürücüsü; 'öncü' değil, gerçek zamanlı izleme."),
              ("USD/JPY", "FX_IDC:USDJPY", "Risk-off göstergesi."),
              ("ABD 10 yıllık getiri", "TVC:US10Y", "Büyüme hisseleri faize duyarlı; CPI/NFP (TR 16:30) tepkisi açılıştan önce.")],
      "IWM": [("Russell 2000 E-mini vadeli", "CME_MINI:RTY1!", "CME Globex ~23 saat; IWM açılış boşluğunu önceden gösterir (IWM varyansının ~%40'ı gece)."),
              ("S&P 500 E-mini vadeli", "CME_MINI:ES1!", "Genel piyasa yönü (IWM betası SPY'a 1,14)."),
              ("ABD 2 yıllık getiri", "TVC:US02Y", "Küçük ölçek finansman/faiz duyarlılığı; veri günlerinde açılış öncesi.")],
      "DIA": [("Dow E-mini vadeli", "CBOT_MINI:YM1!", "CBOT Globex ~23 saat; DIA açılış boşluğunu önceden gösterir."), ("S&P 500 E-mini vadeli", "CME_MINI:ES1!", "Genel piyasa.")],
      "RSP": [("S&P 500 E-mini vadeli", "CME_MINI:ES1!", "RSP'nin eşit ağırlıklı vadelisi yok; ES1! ve RTY1! birlikte izlenir."), ("Russell 2000 E-mini", "CME_MINI:RTY1!", "Orta/küçük ağırlık eğilimi.")],
      "MDY": [("Russell 2000 E-mini", "CME_MINI:RTY1!", "MDY'nin likit vadelisi TradingView doğrulama listesinde yok; RTY1! (0,92 korelasyonlu IWM) ve ES1! izlenir."), ("S&P 500 E-mini", "CME_MINI:ES1!", "Genel piyasa.")]}
NO_LAG = ("Doğrulanmış gecikmeli öncü YOK: leadlag_sweep'te bu hedef için hiçbir öncü (48 aday) BH-FDR'yi geçmedi (aile alt kümesi 2.636 hedef×öncü satırında da h1 ve h3 için 0). "
          "'Yetişme' testi kendi getirisi kontrol edilince yalnız T10YIE (başabaş enflasyon) h3'te FDR geçti; ancak etki tamamen 2020'den (2020 hariç t=0,75; OOS t≈0,4) -> öncü değil. "
          "Faiz kanalı adayları (DFII10 reel faiz ↓, TIP ↑, LQD ↑ -> 3 günde endeks ↑) IS ve OOS'ta aynı işaretli ama FDR yok; işlem kuralına çevrilince (z>1) "
          "SPY'da net 4-30 bp, t<1,6 (yalnız QQQ C1 t≈2,0-2,5) -> izleme bilgisi, sinyal değil. IWM'in SPY'ı 'yetişmesi' (AE13) TERS işaretli: SPY'ın IWM'den 1 puan iyi olduğu günün ertesi IWM long net −28 bp; "
          "z>1 yetişme kuralı net −21 bp (t=−2,1). En güçlü (FDR'siz) gecikmeli satırlar: ")
LL = []
TAKVIM = ("Önümüzdeki olaylar (TR saati): CPI 10 Kas 2026 Sal 16:30; OPEX 20 Kas 2026 Cum; Şükran Günü 26 Kas kapalı, 27 Kas erken kapanış 21:00; NFP 4 Ara 16:30; "
          "FOMC 9 Ara 22:00 (SEP); CPI 10 Ara 16:30; OPEX/triple witching 18 Ara; 24 Ara erken kapanış 21:00, 25 Ara ve 1 Oca kapalı. Testlerde pre-FOMC (AE08), CPI/NFP günü (AE09), "
          "OPEX haftası (AE10) için pozitif kenar YOK (çoğu net negatif) -> bu günler sinyal değil; S1/S2 işlemleri bu günlere denk gelirse açılış boşluğu riski büyür.")
for T, kind in (("SPY", "SPY"), ("QQQ", "QQQ"), ("IWM", "IWM"), ("RSP", "RSP"), ("DIA", "DIA"), ("MDY", "MDY"),
                ("SPXL", "SPY"), ("SSO", "SPY"), ("TQQQ", "QQQ"), ("QLD", "QQQ")):
    rt = [{"ad": a_, "tv": tv_, "neden": n_} for a_, tv_, n_ in RT[kind]]
    if T in ("SPXL", "SSO", "TQQQ", "QLD"):
        rt = [{"ad": rt[0]["ad"], "tv": rt[0]["tv"], "neden": f"Dayanak {kind} ile aynı izleme seti ({kind} satırına bakın); vadeli hareketi x kaldıraç = beklenen açılış boşluğu."}]
    if T == "SPY":
        note = NO_LAG + best_lag(T) + "."
    else:
        note = ("Doğrulanmış gecikmeli öncü YOK (aile alt kümesi BH-FDR 0/2.636; yetişme, faiz kanalı ve IWM-SPY ayrıntısı SPY satırında). "
                "En güçlü (FDR'siz) gecikmeli satırlar: " + best_lag(T) + ".")
    if T in ("SPXL", "SSO", "TQQQ", "QLD"):
        note = f"Kaldıraçlı araç: sinyal ve öncü analizi dayanak {kind} üzerinden yapılır (korelasyon ≈1,00). " + note
    if T in ("SPY", "QQQ", "SPXL", "SSO", "TQQQ", "QLD"):
        note += " Bu ETF için işlem sinyali öncüden değil kendi fiyat deseninden gelir (S1/S2: IBS<0,10 + düşüş)."
    LL.append({"sym": T, "suruculer": surucu(T), "onculer": [], "gercek_zamanli": rt, "not": note,
               "takvim_riskleri": TAKVIM if T == "SPY" else "SPY satırındaki takvimle aynı (CPI 10 Kas, OPEX 20 Kas, 26-27 Kas tatil/erken kapanış, NFP 4 Ara, FOMC 9 Ara, CPI 10 Ara, OPEX 18 Ara, 24-25 Ara)."})

# ---------------- elenenler ----------------
hs = rd("hipotez_ozet.csv")
def hsum(hyp, var, mode, h):
    x = hs[(hs.hyp == hyp) & (hs["var"] == var) & (hs["mode"] == mode) & (hs.h == h)]
    if not len(x): return ""
    r = x.iloc[0]; return f"{mode} h={h}: medyan net {r.med_net:.0f} bp, medyan t {r.med_t:.1f}, {int(r.pos_net)}/{int(r.n_etf)} ETF net>0, {int(r.t_ge2)} ETF t≥2"
EL = [
    {"ad": "AE01 IBS<0,20, 1 gün", "neden": "Maliyet sonrası yok: " + hsum("AE01_IBS_dusuk", "ibs<0.2", "C0", 1) + "; O1 negatif. Literatürle uyumlu (IVV'de zayıf)."},
    {"ad": "AE02 IBS>0,80 -> ters ETF ile kısa", "neden": "Long ertesi gün brüt ~0 (negatif değil, maliyetle −12 bp); ters ETF ile tüm varyantlar net −17/−23 bp, t<−2 (SH/PSQ). Kısa yön kârsız."},
    {"ad": "AE03 RSI2<10 & C>SMA200, C>SMA5'te çık (≤3 gün)", "neden": hsum("AE03_RSI2", "rsi2<10 & c>sma200, cikis c>sma5 max3", "C0", 3) + ". Filtresiz RSI2<10 C0 h1 SPY 24 bp/t=2,0, QQQ t=2,1 ama O1/C1'de ~0 ve IWM/DIA/RSP/MDY'de yok (kapanışa bağımlı, aile tutarsız)."},
    {"ad": "AE04 RSI4<25 & C>SMA200 (Connors RSI 25)", "neden": hsum("AE04_RSI4_25", "rsi4<25 & c>sma200, cikis rsi4>55 max3", "C0", 3) + "; C1 negatif."},
    {"ad": "AE05 3 düşüş & C>SMA200, ilk yükselişte çık", "neden": hsum("AE05_3gun_dusus", "3 dusus & c>sma200, cikis ilk yukselis max3", "C0", 3) + ". Filtresiz sürüm S3 olarak düşük güvenle tutuldu."},
    {"ad": "AE06 Turnaround Tuesday (Pzt ≤ −%1,5 -> Salı)", "neden": "6/6 ETF pozitif (C0 medyan net 90 bp) ama n≈31 (<40), medyan t 1,7, yalnız QQQ t≥2; O1 zayıf, C1 negatif. Örneklem yetersiz."},
    {"ad": "AE07 Ay dönümü", "neden": "Son gün -> ilk 3 gün: " + hsum("AE07_ay_donumu", "t=son gun, yeni ayin ilk 3 gunu", "O1", 3) + "; sondan 2. gün sürümü daha zayıf. Pozitif ama t<1; eşik altı."},
    {"ad": "AE08 Pre-FOMC (D-1 kapanış -> D kapanış)", "neden": hsum("AE08_pre_FOMC", "t=FOMC-1 (C0: D-1 kapanis->D kapanis)", "C0", 1) + ". Kurov ve diğ. (2021) ile uyumlu: 2015 sonrası drift yok."},
    {"ad": "AE09 CPI / NFP / FOMC günü (önceki kapanışta gir)", "neden": "CPI: " + hsum("AE09_makro_duyuru_gunu", "t+1=CPI", "C0", 1) + "; NFP: " + hsum("AE09_makro_duyuru_gunu", "t+1=NFP", "C0", 1) + ". Duyuru primi bu dönemde yok."},
    {"ad": "AE10 OPEX haftası (öncesi Cuma -> Çarşamba)", "neden": hsum("AE10_opex_haftasi", "t=OPEX haftasi oncesi son gun, 3 gun tut", "C0", 3) + "."},
    {"ad": "AE11 Tatil öncesi gün (C0 t -> t+1)", "neden": hsum("AE11_tatil_oncesi", "t+1=tatil oncesi gun, C0 h1", "C0", 1) + "; maliyet sonrası ~0 (Ko & Yang 2021: büyüklerde etki yok)."},
    {"ad": "Genel CA_tatil_oncesi C1 h=3 (tatil sonrası 2.-4. gün)", "neden": "SPY 39 bp/t=2,2, QQQ t=2,3 ama C0/O1 ~0; tatil türüne göre çok dağınık (Good Friday +147 bp, Yılbaşı +75, Noel −46, Juneteenth −26; her tür ≤10 gözlem). Mekanizma ve literatür yok -> veri madenciliği."},
    {"ad": "AE12 VIX ≥ 1,2×SMA10 & SPY>SMA200 -> 3 gün", "neden": hsum("AE12_VIX_sicrama", "vix>=1.2*sma10 & SPY>sma200", "C0", 3) + "; O1/C1 negatif; filtresiz sürüm negatif."},
    {"ad": "AE13 SPY−IWM ≥ +1 puan -> IWM long (yetişme)", "neden": "Ters işaret: C0 h1 IWM net −28 bp, h3 −89 bp; TNA ile de negatif. Lead-lag 'yetişme' kuralı (z>1) net −21 bp, t=−2,1."},
    {"ad": "AE14 Gece/gün içi ayrışması", "neden": "Gece > gün içi (SPY 3,7 vs 1,9 bp/gün; IWM gün içi negatif) ama OOS'ta gece getirisi yarıya indi (SPY 2,2 bp, t=1,2). Kapanışta al-açılışta sat net −9 bp (2.500$). Uygulama çıkarımı: giriş/çıkışı kapanışta yap (S1'de C0/C1 > O1 ile uyumlu)."},
    {"ad": "AE15 Büyük düşüş günü (≤ −2σ20) -> 2 gün long", "neden": hsum("AE15_buyuk_gun_donusu", "r<=-2*sd20 -> long h2", "C0", 2) + "; O1/C1 daha kötü."},
    {"ad": "200 günlük ortalama / VIX rejimi filtreleri (S1 üzerinde)", "neden": "7 filtre denendi; hiçbiri S1'i tüm modlarda iyileştirmedi. C>SMA200: C1 medyan net 36 bp (filtresiz 52). VIX≥20 C1 medyan 80 bp ama n≈85; VIX/VIX3M≥1 n≈25. Filtre seçimi aşırı uyum riski -> ana kurala eklenmedi, bilgi olarak raporlandı."},
    {"ad": "VIX backwardation -> kontango dönüşü (VIX/VIX3M 1'in altına)", "neden": "C1 h=3 6/6 ETF pozitif (medyan net 55 bp) ama n≈45 ve medyan t=1,3; C0/O1 zayıf. Eşik altı."},
    {"ad": "VIX backwardation (VIX/VIX3M>1) genel sinyali", "neden": "19/19 temsilcide C1 h=2 pozitif ama medyan t≈1,0, hiçbir ETF t≥2 değil."},
    {"ad": "Faktör çiftleri göreli dönüş (SPHB/SPLV, IWF/IWD, IWO/IWN, QQQ/IWM)", "neden": "16 varyantın yalnız 'z1(QQQ/IWM)<−2 -> QQQ' C1 h3 (n=52, t=3,2) FDR geçti; aynı fikir C0/O1 h1'de negatif, ters yönü (IWM long) negatif, diğer çiftlerde yok -> tek satır, aile tutarsız. SPHB/SPLV'de 'kaybedeni al' negatif."},
    {"ad": "Aşırı alım sonrası ters ETF (RSI2>90, 3 gün yükseliş; SH/SDS/SPXU/SPXS/PSQ/QID/SQQQ/TZA/SRTY/SDOW)", "neden": "180 testin neredeyse tamamı net negatif (SPY RSI2>90 -> SH C0 h1 −20 bp, t=−6). Tek pozitif köşe 'QQQ RSI2>90 & C<SMA200 -> SQQQ C1 h3' (n küçük, C0/O1 negatif). Kısa yön için geçerli kural yok."},
    {"ad": "Genel kütüphane: haftanın günü (CA_cum O1 h3, CA_per C1 h3)", "neden": "Yalnız NDX/büyüme kümesinde (QQQ/QLD/TQQQ/IWF) eşik geçiyor; SPY/IWM/DIA/RSP/MDY'de yok -> tek bağımsız küme, teknoloji trendinin yan ürünü olabilir."},
    {"ad": "Genel kütüphane: 20 gün zirve kırılımı, momentum sinyalleri", "neden": "Aile genelinde net negatif ya da ~0 (yönlendirmeyle uyumlu)."},
    {"ad": "Lead-lag: T10YIE (başabaş enflasyon) 'yetişme' (h3, FDR geçti)", "neden": "Etki tamamen 2020 krizinden: 2020 hariç t=0,75, OOS t≈0,4. Öncü değil."},
    {"ad": "Lead-lag: DFII10 reel faiz / TIP öncüsü (3 gün)", "neden": "IS/OOS aynı işaret ama FDR yok; işlem kuralı (z>1) SPY'da net 4-30 bp, t<1,6; QQQ C1 t≈2,0-2,5; IWM/DIA zayıf. İzleme bilgisi."},
]

ozet = (f"abd_endeks (55 ETF, 27 bağımsız grup). Toplam {n_tot} test (genel kütüphane aile satırları 16.335 + kendi hipotez/lead-lag testlerim), birleşik BH-FDR q=0,10. "
        f"Eşiği geçen ve aile genelinde tutarlı TEK etki: 'zayıf kapanış dönüşü' — IBS<0,10 ve düşüş günü sonrası 3 gün long (S1 SPY: C1 net {r1.mean_net_bp:.0f} bp, t={r1.t:.2f}, "
        f"IS {r1.is_net_bp:.0f}/OOS {r1.oos_net_bp:.0f} bp, yılların %100'ü pozitif; S2 QQQ: net {r2.mean_net_bp:.0f} bp, t={r2.t:.2f}). 19 grup temsilcisinin 19'unda pozitif, "
        "üç giriş modunda da brüt pozitif, komşu eşiklerde IS ve OOS pozitif; etki piyasa geneli zayıf kapanışlarda yoğun (sinyal SPY'dan alınmalı). SPY ile QQQ sinyalleri %73 aynı gün (tek bağımsız fırsat kümesi). "
        "İki yönlü birleşik FDR'yi geçer; ancak katı tek yönlü BH'de (17.391 test) hiçbir satır geçmez, odaklı hipotez setimde yalnız QQQ satırları geçer -> güven 'orta', kanıt tek test değil aile tutarlılığı. "
        "S3 (3 ardışık düşüş, ilk yükselişte çık) yalnız SPY/QQQ'da ve C0'da geçiyor: düşük güven, kapanışa bağımlı. "
        "Takvim etkileri (pre-FOMC, CPI/NFP, OPEX, ay dönümü, tatil öncesi), VIX sıçraması, IWM'in SPY'ı yetişmesi, faktör çifti dönüşü ve ters ETF ile kısa yön: eşik altı ya da negatif. "
        "Doğrulanmış gecikmeli öncü yok; ES1!/NQ1!/RTY1! açılış boşluğunu önceden gösteren gerçek zamanlı izleme araçlarıdır. "
        "Kaldıraçlı ETF'ler (SPXL/SSO, TQQQ/QLD) aynı sinyalle çalışır, sabit komisyonda yalnız sermaye verimliliği sağlar; S1/S2 işlemlerinde tek işlemde −%23/−%31 kayıp yaşandı. "
        "Ters ETF'ler yalnız koruma amaçlı (kalıcı negatif net). Bu bir backtest; geçmiş sonuç garanti değildir.")

DOSYALAR = [os.path.join(R, p) for p in [
    "notlar/aile_abd_endeks.md", "kod/ajan_abd_endeks/ae.py", "kod/ajan_abd_endeks/01_islenebilirlik.py", "kod/ajan_abd_endeks/02_genel_aile.py",
    "kod/ajan_abd_endeks/03_hipotezler.py", "kod/ajan_abd_endeks/04_leadlag.py", "kod/ajan_abd_endeks/05_adaylar.py", "kod/ajan_abd_endeks/06_sonuc_json.py",
    "sonuclar/aile_abd_endeks/sonuc.json", "sonuclar/aile_abd_endeks/islenebilirlik.csv", "sonuclar/aile_abd_endeks/kopya_ciftleri.csv",
    "sonuclar/aile_abd_endeks/genel_aile_tutarlilik.csv", "sonuclar/aile_abd_endeks/genel_aile_fdr_pozitif.csv", "sonuclar/aile_abd_endeks/hipotez_testleri.csv",
    "sonuclar/aile_abd_endeks/hipotez_ozet.csv", "sonuclar/aile_abd_endeks/gece_gunici.csv", "sonuclar/aile_abd_endeks/leadlag_aile_ozet.csv",
    "sonuclar/aile_abd_endeks/leadlag_catch_kontrollu.csv", "sonuclar/aile_abd_endeks/leadlag_catch_backtest.csv", "sonuclar/aile_abd_endeks/leadlag_reel_faiz_backtest.csv",
    "sonuclar/aile_abd_endeks/leadlag_tip_backtest.csv", "sonuclar/aile_abd_endeks/aday_ozet.csv", "sonuclar/aile_abd_endeks/aday_S1_komsu_parametre.csv",
    "sonuclar/aile_abd_endeks/aday_S1_kaldiracli.csv", "sonuclar/aile_abd_endeks/aday_S1_spy_sinyali.csv"]]
OUTJ = {"family": "abd_endeks", "ozet": ozet, "izleme": IZ, "stratejiler": STRATS, "elenen": EL, "leadlag": LL, "dosyalar": DOSYALAR,
        "tv_dogrulanacak": ["CBOE:VIX/CBOE:VIX3M (TradingView oran ifadesi; bileşen kodları doğrulandı, ifadenin kendisi sayfa olarak doğrulanmadı)"]}
def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list): return [clean(v) for v in o]
    if isinstance(o, (np.floating,)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, float) and not np.isfinite(o): return None
    return o
OUTJ = clean(OUTJ)
fn = os.path.join(O, "sonuc.json")
json.dump(OUTJ, open(fn, "w"), ensure_ascii=False, indent=1)
print("yazıldı:", fn, " strateji:", len(STRATS), " izleme:", len(IZ), " leadlag:", len(LL), " elenen:", len(EL))
