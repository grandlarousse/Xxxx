# parametreler.json: hesaplayıcı sabitleri + doğrulama + güncelleme önerisi
import json
S_ = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
r = json.load(open(f"{S_}/rehber_kod/p_ham.json"))
bug = json.load(open(f"{S_}/out/sentez/bugun_2026_11_09.json"))["bugun"]
E2, A4, L = r["E2"], r["A4"], r["LOWMOM"]
h17 = L["hv"]["17ET"]
R4 = lambda x, n=4: round(float(x), n)

out = {
 "tarih": "2026-11-06 Cuma kapanışı itibarıyla (ABD kapanışı 16:00 ET; spot 15:00 UTC). Hesap: 2026-11-08.",
 "kaynak": "out/sentez/sinyal_altin.py tanımları (P, E2 sözlükleri, madenci_artik, A4 ve lowmom_tablo), panel_etf/panel_viop/panel_spot parquet; betik: rehber_kod/p_parametre.py",
 "birim": "Getiriler log getiri. Hesaplayıcı TradingView kapanışlarından ln(C_son/C_önce) ile hesaplar; yüzde girilirse r = ln(1 + yüzde/100). Eşikler yüzde (log) cinsinden.",
 "E2": {
   "formul": "x_k = ln(Y_{t-1}/Y_{t-1-k}) − b_GLD·ln(GLD_{t-1}/GLD_{t-1-k}) − b_SPY·ln(SPY_{t-1}/SPY_{t-1-k}); t-1 = son ABD seansı, k ABD işlem günü (bar) sayılır. OLS sabiti ÇIKARILMAZ (betik de çıkarmıyor).",
   "GDXJ": {"b_GLD": R4(E2["GDXJ"]["b_GLD"]), "b_SPY": R4(E2["GDXJ"]["b_SPY"]), "pencere": E2["GDXJ"]["pencere"],
            "pazartesi_09_11_betik_betasi": {"b_GLD": R4(E2["GDXJ"]["b_GLD_pazartesi"]), "b_SPY": R4(E2["GDXJ"]["b_SPY_pazartesi"])},
            "aralik_12ay": {k: [R4(v[0], 3), R4(v[1], 3)] for k, v in E2["GDXJ"]["aralik_12ay"].items()}},
   "GDX": {"b_GLD": R4(E2["GDX"]["b_GLD"]), "b_SPY": R4(E2["GDX"]["b_SPY"]), "pencere": E2["GDX"]["pencere"],
           "pazartesi_09_11_betik_betasi": {"b_GLD": R4(E2["GDX"]["b_GLD_pazartesi"]), "b_SPY": R4(E2["GDX"]["b_SPY_pazartesi"])},
           "aralik_12ay": {k: [R4(v[0], 3), R4(v[1], 3)] for k, v in E2["GDX"]["aralik_12ay"].items()}},
   "kurallar": {
     "E2-C2j": {"y": "GDXJ", "k": 1, "esik_ust_pct": R4(E2["esik"]["C2j_ust"] * 100), "islem": "x > eşik ise GDXJ al, 3 gün kademeli (her gün sermayenin 1/3'ü; 3 ABD işlem günü sonra o dilimi sat)"},
     "E2-C2": {"y": "GDX", "k": 3, "esik_ust_pct": R4(E2["esik"]["C2_ust"] * 100), "islem": "x > eşik ise GDX al, 3 gün kademeli"},
     "E2-C1": {"y": "GDX", "k": 10, "esik_ust_pct": R4(E2["esik"]["C1_ust"] * 100), "kaplama_alt_pct": R4(E2["esik"]["C1_kaplama_alt"] * 100),
               "islem": "x > eşik ise GLD al, 5 gün kademeli; kaplama sürümü: GLD tut, x < alt eşik olan günün 1/5 dilimi nakit"}},
   "dogrulama_pazartesi_09_11_x_pct": {
     sid.split("_")[0]: {"betik": R4(E2["dogrulama_pazartesi"]["x_betik"][sid] * 100, 3),
                         "elle_pazartesi_betasiyla": R4(E2["dogrulama_pazartesi"]["x_elle_sabit_beta_pazartesi"][sid] * 100, 3),
                         "elle_son_betayla": R4(E2["dogrulama_pazartesi"]["x_elle_sabit_beta_son"][sid] * 100, 3)}
     for sid in E2["dogrulama_pazartesi"]["x_betik"]},
   "dogrulama_notu": "C2j (k=1) elle hesap betikle aynı (%3,674). k=3 ve k=10'da betik her günün artığını o günün betasıyla toplar; 05.11 SPY −%4,5 günü pencereye girince GDX b_SPY 0,88 → 0,76 sıçradı, bu yüzden sabit betalı elle hesap ≈45–55 bps düşük. Üçü de eşiğin çok üstünde, sinyal aynı.",
   "elle_hata_son_3_yil": {sid.split("_")[0]: {k: {"farkli_gun": v["farkli_gun"], "gun": v["gun"]} for k, v in d.items()} for sid, d in r["E2_elle_hata"].items()},
 },
 "A4_C1": {
   "formul": "e = r_GDXJ − β60·r_GLD (r = son ABD kapanışının bir önceki VİOP gününde bilinen son ABD kapanışına göre log değişimi); |e| > 0,43·σ_e ise yön sign(e); 3 gün kademeli (VİOP günü).",
   "beta60": R4(A4["beta60_son"]), "sigma_e_pct": R4(A4["sigma_e_son"] * 100), "esik_pct": R4(A4["esik_son"] * 100), "z_esik": 0.43,
   "pencere_notu": "β60 = son 60 VİOP satırının cov(r_GDXJ, r_GLD)/var(r_GLD); σ_e = son 120 VİOP satırının e std'si (örneklem). İkisi de 09.11 VİOP satırını (Cuma 06.11 ABD getirisi) içerir → Salı 10.11 ve sonrası için.",
   "pazartesi_09_11_betik": {"beta60": R4(A4["beta60_pazartesi"]), "sigma_e_pct": R4(A4["sigma_e_pazartesi"] * 100), "esik_pct": R4(A4["esik_pazartesi"] * 100),
                             "r_GDXJ_pct_log": R4(A4["r_GDXJ_cuma"] * 100), "r_GLD_pct_log": R4(A4["r_GLD_cuma"] * 100), "e_pct": R4(A4["e_pazartesi"] * 100), "z": R4(A4["z_pazartesi"], 3)},
   "aralik_12ay": {"beta60": [R4(A4["aralik_12ay"]["beta60"][0], 3), R4(A4["aralik_12ay"]["beta60"][1], 3)],
                   "sigma_e_pct": [R4(A4["aralik_12ay"]["sigma_e"][0] * 100, 3), R4(A4["aralik_12ay"]["sigma_e"][1] * 100, 3)],
                   "esik_pct": [R4(A4["aralik_12ay"]["esik"][0] * 100, 3), R4(A4["aralik_12ay"]["esik"][1] * 100, 3)]},
   "elle_hata_2024_06_2026_11": A4["elle_hata_2024_06_sonrasi"],
 },
 "LOWMOM": {
   "rv20_esik_yillik_pct": R4(L["rv20_esik_yillik_252"] * 100, 3),
   "tanim": L["not_"],
   "rv20_cuma_pct": R4(L["rv20_cuma"] * 100, 2), "yuzdelik_cuma": R4(L["yuzdelik_cuma"], 3),
   "esik_aralik_12ay_pct": [R4(L["esik_aralik_12ay"][0] * 100, 3), R4(L["esik_aralik_12ay"][1] * 100, 3)],
   "rv20_aralik_12ay_pct": [R4(L["rv20_aralik_12ay"][0] * 100, 2), R4(L["rv20_aralik_12ay"][1] * 100, 2)],
   "son_aktif_gun": L["son_aktif_gun"],
   "x5_cuma_pct": R4(L["x5_cuma"] * 100, 3),
   "TradingView_HV20": {
     "tanim": "TradingView yerleşik HV = 100 · stdev(ln(C/C[1]), 20) · √365; Pine ta.stdev yanlı (n'ye bölünür). Günlük mum OANDA:XAUUSD (kapanış 17:00 New York).",
     "esik_HV365": round(h17["hv365_esik_kantil"], 2),
     "esik_HV365_00UTC_kapanisla": round(L["hv"]["00UTC"]["hv365_esik_kantil"], 2),
     "esik_HV365_21UTC_kapanisla": round(L["hv"]["21UTC"]["hv365_esik_kantil"], 2),
     "esik_HV252_eger_gosterge_252_kullaniyorsa": round(h17["hv252_esik_kantil"], 2),
     "teorik_esik_HV365": round(L["teorik_hv365_esik"], 2),
     "teorik_carpan": round(L["teorik_carpan_365_ddof0"], 4),
     "uyum_orani_2010_2026": round(h17["uyum_kantil"], 3), "uyum_orani_2021_2026": round(h17["son_yil_uyum"], 3),
     "HV365_cuma_17ET": round(h17["hv365_cuma"], 2), "HV365_cuma_00UTC": round(L["hv"]["00UTC"]["hv365_cuma"], 2),
     "HV365_aralik_12ay": [round(h17["hv365_12ay"][0], 2), round(h17["hv365_12ay"][1], 2)],
     "bant_aktif_olasiligi": L["hv_bant_aktif_olasiligi_bugunku_esikle"],
     "kullanim": "HV(20) ≥ 17 → LOWMOM PASİF say (yanılma ≈%5; ≥20'de %0,6). 12–17 → sınır bölgesi, tam rv20 hesabı gerekir (Pine betiği ya da sinyal_altin.py). < 12 → büyük olasılıkla AKTİF (%79–97), yine tam hesapla teyit et.",
   },
 },
 "E3_1": {"pazartesi_09_11_esik_fiyat_usd": 4065.685, "not_": "Cuma 06.11 16:00 ET Dukascopy BID spot. TradingView'da kendi kaynağınızın (OANDA:XAUUSD) aynı anki fiyatını kullanın; iki fiyat aynı kaynaktan olmalı."},
 "A8_3": {"acik_dilimler_pazartesi": bug["V_LAST1H_h5"]["acik_dilimler"], "acik_dilim_toplami_bes_te": bug["V_LAST1H_h5"]["acik_dilim_toplami_bes_te"]},
 "guncelleme_onerisi": {
   "E2_betalari": "Haftada bir (Cuma kapanışından sonra, Pazartesi'den önce). Aylık da kabul edilebilir: son 3 yılda sinyalin farklı çıktığı gün oranı haftalıkta %0,1–0,8, aylıkta %0,9–1,3, çeyreklikte %2,4–2,9. |SPY| ya da |GLD| > %3 olan bir günden sonra hemen yenile (05.11.2026'da b_SPY tek günde 0,88 → 0,76).",
   "A4_beta60_sigma_e": "Haftada bir. Hata oranı haftalıkta %1,0, aylıkta %2,5, çeyreklikte %7,5 (2024-06 → 2026-11, 600 VİOP günü). 60 ve 120 günlük pencereler E2'nin 250 gününden hızlı değişir.",
   "LOWMOM_esik": "Yılda bir. Genişleyen 2010+ yüzdelik; son 12 ayda %11,45–11,67 arasında.",
   "HV_esdegeri": "Yılda bir (aynı yüzdelik mantığı).",
   "E2_esikleri": "Hiç değiştirme (IS 2008–2017'de donduruldu; yeniden kalibrasyon sinyal seçimini bozar).",
 },
}
json.dump(out, open(f"{S_}/out/rehber/parametreler.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1)[:6000])
