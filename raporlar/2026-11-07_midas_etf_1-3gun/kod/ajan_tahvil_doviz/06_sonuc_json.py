"""6) FDR muhasebesi + makine okunur sonuç (sonuclar/aile_tahvil_doviz/sonuc.json).
Önce 00..04 ve strateji_S1/S2 betikleri çalışmış olmalı. Çalıştır: python3 -I kod/ajan_tahvil_doviz/06_sonuc_json.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import td, lib

O = td.OUT
R = lambda f: pd.read_csv(os.path.join(O, f))
# ---------------- FDR muhasebesi ----------------
g = R("genel_duzeltilmis.csv"); h = R("hipotez_testleri.csv")
parts = [g.assign(src="genel"), h.assign(src="hipotez")]
for f in ["S1_ana", "S1_aile", "S1_komsu", "S1_plasebo", "S1_A3_acilis", "S2_ana", "S2_aile", "S2_komsu", "leadlag_fx_kural"]:
    parts.append(R(f + ".csv").assign(src=f))
A = pd.concat(parts, ignore_index=True)
A = A[A.n >= 3].copy()
A["p"] = [lib.t_to_p(t, n) for t, n in zip(A.t, A.n)]
A["p1"] = np.where(A.t > 0, A.p / 2, 1 - A.p / 2)
A["fdr2"] = lib.bh_fdr(A.p.values, 0.10); A["fdr1"] = lib.bh_fdr(A.p1.values, 0.10)
n_strat = len(A); n_fdr2 = int(A.fdr2.sum()); n_fdr2_pos = int((A.fdr2 & (A.mean_net_bp > 0)).sum()); n_fdr1 = int(A.fdr1.sum())
k = n_fdr2; thr2 = float(np.sort(A.p.dropna().values)[k - 1]) if k else np.nan
pr = h[h.birincil].copy(); pr["p1"] = np.where(pr.t > 0, pr.p / 2, 1 - pr.p / 2); pr["f1"] = lib.bh_fdr(pr.p1.values, 0.10)
n_prim = len(pr); prim_pass = pr[pr.f1][["hyp", "sym", "t", "p1"]]
ll_n = sum(len(R(f)) for f in ["leadlag_fx_spy.csv", "leadlag_hy_spy.csv", "leadlag_catch_kontrollu.csv", "leadlag_izleme_oncu.csv"])
N_TOTAL = n_strat + ll_n
s1 = A[(A.src == "S1_ana")].set_index(["sym", "mode"])
fdr_txt = (f"Toplam {N_TOTAL} test (strateji {n_strat}: genel kütüphane dağıtım-düzeltmeli aile satırları 11880 + aileye özel hipotez {len(h)} + "
           f"S1/S2 sağlamlık ve döviz kuralları; lead-lag regresyonu {ll_n}). (1) İki yönlü BH-FDR q=0,10 (tüm strateji testleri): {n_fdr2} geçen "
           f"(eşik p≤{thr2:.4f}; çoğu maliyet yüzünden net negatif satır), net pozitif geçen {n_fdr2_pos}; S1-TMV C0 p={s1.loc[('TMV','C0'),'p']:.4f} GEÇTİ, "
           f"S1-TBT C0 p={s1.loc[('TBT','C0'),'p']:.4f} GEÇTİ. (2) Katı tek yönlü BH ('net>0', {n_strat} test): {n_fdr1} geçen — S1 de geçmiyor. "
           f"(3) Odaklı önceden kayıtlı birincil kurallar ({n_prim} test, notlar/hipotezler.csv TD01-TD09 + yönlendirme): tek yönlü BH'de geçen "
           f"{len(prim_pass)}: " + ", ".join(f"{r.hyp}/{r.sym} (p={r.p1:.4f})" for r in prim_pass.itertuples()) + ".")
print(fdr_txt)

# ---------------- izleme listesi ----------------
isl = R("islenebilirlik.csv").set_index("sym")
DEC = {
 "TMV": ("kabul", "S1'in ana aracı (−3x TLT). Medyan 35,8 mn $/gün, maliyet 20 bp (2.500 $), 1 günlük oynaklık 178 bp (maliyet/oynaklık 0,11). Direxion 1940 Yasası fonu (PTP/K-1 değil; ihraççı belgesiyle teyit önerilir). Midas'ta bulunurluğu resmî olarak doğrulanamadı: uygulamada sembol ve 'parçalı' etiketini kontrol et. Kaldıraçlı ters ETF: tek işlemde −%7,6'ya varan kayıp görüldü."),
 "TBT": ("yedek", "S1'in alternatif aracı (−2x TLT; TMV'ye göre daha düşük risk). Medyan 12,3 mn $/gün (tercih edilen eşiğin alt sınırı), maliyet 20 bp. ProShares Trust (1940 Yasası) fonu; PTP değil (teyit önerilir). Midas bulunurluğu doğrulanamadı."),
 "TLT": ("yedek", "S1'in dayanağı ve faiz izleme aracı; ailenin en likit/ucuz uzun vade ETF'i (2,6 mlr $/gün, 13 bp, maliyet/oynaklık 0,22). Long yönde eşiği geçen strateji YOK (ay sonu net 14 bp t=1,2; FOMC D-1 net 11 bp t=1,1; RSI2/IBS dönüşü net<0). Risk kuralı: 10Y ihale öncesi pencerede (A-3→A-1) TLT long taşımamak (brüt −41 bp, t=−3,7)."),
 "TMF": ("yedek", "TLT long sinyalleri için komisyon-verimli araç (3x; 159 mn $/gün; 16 bp maliyet ≈ TLT eşdeğerinde ~5 bp). Long sinyaller (FOMC D-1: net 53 bp t=1,91; ay sonu k4: net 52 bp t=1,51) brüt pozitif ama eşik altı; kabul edilmiş long strateji yok. Midas bulunurluğu doğrulanamadı."),
 "EDV": ("red", "TLT'nin daha uzun süreli kopyası (korelasyon 0,98, beta ~1,5); 73 mn $/gün ama TLT/TMF daha ucuz ve bağımsız kanıt değil; ayrı strateji yok."),
 "ZROZ": ("red", "EDV/TLT kopyası (corr 0,98-0,99); 37 mn $/gün, maliyet 20 bp; bağımsız strateji yok."),
 "TLH": ("red", "TLT kopyası (corr 0,98, daha kısa süre); TLT daha likit/ucuz."),
 "UBT": ("red", "2x TLT ama likidite 0,9 mn $/gün, maliyet 47 bp; TMF üstün."),
 "IEF": ("red", "Likit (759 mn $) ama 1g oynaklık 31 bp / maliyet 14 bp (0,45). İhale öncesi brüt −19 bp (t=−4,1) görülür fakat ailede 7-10 yıl için ters araç yok (TBX/PST veri dışı); long strateji yok."),
 "IEI": ("red", "Orta vade kopyası (IEF ile corr 0,97); maliyet/oynaklık 0,80."),
 "GOVT": ("red", "IEF benzeri; maliyet/oynaklık 0,66; 'yetişme' (IEF/SHY→GOVT) t≈2,4-3,0 ama 1 sd başına ~5 bp < 16 bp maliyet."),
 "SHY": ("red", "1g oynaklık 9 bp < 14 bp maliyet; ay sonu brüt etkisi istatistiksel (t=6) ama 7,7 bp."),
 "BIL": ("red", "Nakit benzeri (1g oynaklık 6,6 bp < 14 bp maliyet). leadlag_sweep'teki t≈7-11 'yetişme' sonuçları 0,4-1 bp/sd (ekonomik değil) ve eksik dağıtım verisinin testere dişi artefaktı: düzeltilmiş veride kayboluyor."),
 "SGOV": ("red", "BIL ile aynı (nakit benzeri; 'yetişme' 0,4-1 bp/sd, dağıtım artefaktı)."),
 "AGG": ("red", "Maliyet/oynaklık 0,52; ay sonu brüt 15 bp (t=3,6) maliyeti karşılamıyor. BND ile kopya (corr 0,97)."),
 "BND": ("red", "AGG kopyası."),
 "LQD": ("red", "Çok likit (3,3 mlr $) ama 1g oynaklık 37 bp / 13 bp; ay sonu/FOMC brüt pozitif ama net eşik altı."),
 "VCIT": ("red", "LQD kopyası (corr 0,96); maliyet/oynaklık 0,50."),
 "HYG": ("red", "Likit (3,1 mlr $) ama maliyet/oynaklık 0,49. SPY→HYG gecikmesi NEGATİF (t=−3,0; SPY yükselince ertesi gün HYG geri veriyor) ve 1 sd başına −11 bp < 13 bp; açığa satış yok. SPY sert düşüş sonrası HYG long: net −9 bp."),
 "JNK": ("red", "HYG kopyası (corr 0,98)."),
 "USHY": ("red", "HYG kopyası (corr 0,985); seri 2019-04'ten güvenilir."),
 "BKLN": ("red", "Maliyet/oynaklık 0,76; strateji yok."),
 "TIP": ("red", "Maliyet/oynaklık 0,55; strateji yok. SCHP kopyası."),
 "SCHP": ("red", "TIP kopyası."),
 "STIP": ("red", "1g oynaklık 16 bp ≈ maliyet."),
 "EMB": ("red", "Maliyet/oynaklık 0,37; genel kütüphanedeki net pozitif satırlar (ör. tatil öncesi C1 h3: net 16 bp, t=1,84; RSI2<10 üst200 O1 h2: net 9 bp, IS 4 bp) tek başına, aile tutarlılığı yok; strateji yok."),
 "MUB": ("red", "Maliyet/oynaklık 0,58; dönüş sinyalleri net negatif (FDR'de negatif)."),
 "UUP": ("red", "Ailenin en likit döviz ETF'i (44,6 mn $) ama 1g oynaklık 42 bp / 20 bp maliyet. Risk varlıkları (SPY/HYG/LQD) → ertesi gün USD düşüşü istatistiksel olarak gerçek (t≈−4, FDR, IS/OOS aynı işaret, gece+gün içi) ama 1 sd başına 8-9 bp; işlem kuralı net −14 bp. Invesco DB fonu (emtia havuzu, K-1/PTP riski: Midas'ta PTP ibaresi kontrol edilmeli)."),
 "UDN": ("red", "1,9 mn $/gün, 47 bp maliyet; DB fonu (K-1/PTP riski)."),
 "FXE": ("red", "9,8 mn $/gün, 27 bp maliyet / 34 bp oynaklık (0,79). SPY→FXE gecikmesi t=5 ama 6 bp/sd; kural net −20 bp."),
 "FXY": ("red", "9,6 mn $/gün, 27 bp / 51 bp. FXY←VIX/SPY şoku hipotezi ters çıktı (şok sonrası ertesi gün yen zayıflıyor, brüt −13 bp, t=−3,5) ve işlenebilir araç yok; FXY←DGS2 net negatif."),
 "FXF": ("red", "4,9 mn $/gün (likiditesiz). SPY→FXF gecikmesi (t=5,3) gece+gün içi parçalarında var; bayat kapanış tek açıklama değil (likit UUP'ta da var) ama 8 bp/sd < 27 bp."),
 "FXB": ("red", "1,5 mn $/gün, 47 bp maliyet."), "FXA": ("red", "0,7 mn $/gün, 47 bp maliyet."), "FXC": ("red", "1,5 mn $/gün, 47 bp; maliyet/oynaklık 1,64."),
 "CEW": ("red", "0,06 mn $/gün; neredeyse işlem görmüyor."),
 "YCS": ("red", "−2x yen; 0,9 mn $/gün, 47 bp; ProShares Trust II (K-1/PTP riski)."),
 "YCL": ("red", "2x yen; 0,5 mn $/gün; ProShares Trust II (K-1/PTP riski)."),
 "EUO": ("red", "−2x euro; 0,5 mn $/gün; ProShares Trust II (K-1/PTP riski)."),
 "ULE": ("red", "2x euro; 0,06 mn $/gün; ProShares Trust II (K-1/PTP riski)."),
}
izleme = []
order = ["TMV", "TBT", "TLT", "TMF"] + [s for s in td.FAM if s not in ("TMV", "TBT", "TLT", "TMF")]
for s in order:
    k_, gr = DEC[s]; r = isl.loc[s]
    izleme.append({"sym": s, "karar": k_, "gerekce": gr, "tv": r.tv, "likidite_mn_usd": round(float(r.med_dollar_vol_m), 2),
                   "maliyet_bp": round(float(r.cost_rt_bp), 1), "vol_1d_bp": round(float(r.vol_1d_bp), 1)})

# ---------------- S1 strateji kaydı ----------------
m = R("S1_ana.csv").set_index(["sym", "mode"]); fam = R("S1_aile.csv").set_index("sym"); a3 = R("S1_A3_acilis.csv").set_index("sym")
t0 = m.loc[("TMV", "C0")]
mod_txt = "; ".join(f"{md}: brüt {m.loc[('TMV', md), 'mean_gross_bp']:.0f} bp, net {m.loc[('TMV', md), 'mean_net_bp']:.0f} bp, t={m.loc[('TMV', md), 't']:.2f} "
                    f"(OOS {m.loc[('TMV', md), 'oos_net_bp']:.0f} bp)" for md in ("C0", "O1", "C1"))
mod_txt += (f"; ek: A-3 AÇILIŞINDA giriş (TR 17:30 kış) brüt {a3.loc['TMV', 'mean_gross_bp']:.0f} bp, net {a3.loc['TMV', 'mean_net_bp']:.0f} bp, "
            f"t={a3.loc['TMV', 't']:.2f}, IS {a3.loc['TMV', 'is_net_bp']:.0f} / OOS {a3.loc['TMV', 'oos_net_bp']:.0f} bp. O1 (=A-2 açılışı) zayıf çünkü "
            f"A-3 kapanışı→A-2 açılışı (çoğunlukla hafta sonu) boşluğu etkinin bir kısmını taşıyor: giriş A-3 seansı içinde yapılmalı.")
aile_txt = ("Aynı pencerede uzun ETF'ler brüt (C0): " + ", ".join(f"{s} {fam.loc[s, 'mean_gross_bp']:.0f} bp (t {fam.loc[s, 't_gross']:.1f})"
            for s in ["TLT", "EDV", "ZROZ", "TLH", "IEF", "IEI", "GOVT", "AGG", "LQD", "TIP", "EMB", "SHY", "MUB", "HYG", "TMF"])
            + f"; ters: TBT +{fam.loc['TBT', 'mean_gross_bp']:.0f} bp (net {m.loc[('TBT','C0'),'mean_net_bp']:.0f} bp, t={m.loc[('TBT','C0'),'t']:.2f}, "
            f"IS {m.loc[('TBT','C0'),'is_net_bp']:.0f} / OOS {m.loc[('TBT','C0'),'oos_net_bp']:.0f} bp), TMV +{fam.loc['TMV', 'mean_gross_bp']:.0f} bp. "
            "Hepsi aynı faiz faktörü: bağımsız kanıt değil, ama süreyle orantılı ölçekleniyor (beklenen işaret ve büyüklük).")
S1 = {
 "id": "tahvil_doviz_S1",
 "ad": "10 yıllık Hazine ihalesi öncesi uzun vade zayıflığı — TMV (−3x TLT) ile 2 gün",
 "kural": ("Takvim sinyali (fiyat göstergesi yok): A = ABD Hazinesi 10 yıllık tahvil (10-Year Note) ihale günü — TreasuryDirect 'Upcoming Auctions' / "
           "Hazine geçici ihale takvimi; TradingView Ekonomik Takvim'de '10-Year Note Auction' (sonuç 13:00 ET = TR 21:00 kış / 20:00 yaz). "
           "SİNYAL GÜNÜ = A'dan 3 işlem günü önceki gün (A-3; ihale Salı ise önceki Perşembe, Çarşamba ise önceki Cuma; NYSE tatilleri sayılmaz). "
           "İŞLEM: AMEX:TMV long (alternatif AMEX:TBT, −2x). A-3 günü al, A-1 günü (ihaleden bir önceki işlem günü) kapanışta sat; ihale günü tutulmaz. "
           "Stop yok, erken çıkış yok. 30 yıllık ihale (A30) penceresi KULLANILMAZ (zayıf). Dayanak kontrolü: NASDAQ:TLT aynı pencerede ortalama −41 bp."),
 "giris": ("A-3 günü kapanıştan 5-10 dk önce piyasa ya da agresif limit emriyle (kış saati TR ~23:50, yaz saati TR ~22:50; Midas'ta MOC/LOC yok). "
           "Sinyal takvimden bilindiği için aynı gün açılışta (TR 17:30 kış / 16:30 yaz) almak da test edildi ve benzer sonuç verdi. "
           "Sıradaki: 10 Kas 2026 (Sal) ihalesi -> A-3 = 5 Kas Per (geçti; açık pozisyon 9 Kas Pzt kapanışta kapanır); "
           "8 Ara 2026 (Sal, yeniden ihraç) -> giriş 3 Ara 2026 Per TR ~23:50."),
 "tutus": "2 işlem günü (A-2 ve A-1)",
 "cikis": ("A-1 günü kapanıştan 5-10 dk önce (kış TR ~23:50 / yaz ~22:50) sat; örn. 8 Ara 2026 ihalesi için 7 Ara 2026 Pzt. "
           "Uzatılmış saatlerde yalnız limit emir verilebildiği için normal seansta çık."),
 "islem_etf": ["TMV", "TBT"],
 "sinyal_etf": "takvim (10Y Hazine ihalesi); dayanak NASDAQ:TLT",
 "n": int(t0.n), "brut_bp": round(float(t0.mean_gross_bp), 1), "net_bp": round(float(t0.mean_net_bp), 1), "kazanma": round(float(t0.win), 3),
 "pf": round(float(t0.pf), 2), "t": round(float(t0.t), 2), "is_net_bp": round(float(t0.is_net_bp), 1), "oos_net_bp": round(float(t0.oos_net_bp), 1),
 "yil_pozitif": round(float(t0.years_pos_frac), 3), "maxdd": round(float(t0.maxdd), 3), "en_kotu_bp": round(float(t0.worst_bp), 0),
 "maliyet_duyarlilik": f"TMV net/işlem: 1.000$: {t0.net_bp_1000:.0f} bp | 2.500$: {t0.mean_net_bp:.0f} bp | 10.000$: {t0.net_bp_10000:.0f} bp (maliyet 2.500$'da 20 bp = 12 komisyon + 8 makas)",
 "mod_saglamlik": mod_txt,
 "aile_ici": aile_txt,
 "test_sayisi": int(N_TOTAL),
 "fdr": fdr_txt,
 "guven": "orta",
 "notlar": ("Literatür: Lou, Yan & Zhang (2013, RFS) ihale öncesi ikincil piyasa fiyat baskısı ve sonrası toparlanma; hipotez önceden kayıtlıydı "
            "(notlar/hipotezler.csv TD02 'Ek test: TLT C_A-3→C_A-1 <0'). IS t=" + f"{t0.is_t:.2f}, OOS t={t0.oos_t:.2f}; yılların 10/11'i pozitif (2017 hafif negatif). "
            "Plasebo (pencere ±5/±10 işlem günü kaydırılmış): etki yok (TLT −3..+17 bp, |t|<1,3). Haftanın günü eşlenik koşulsuz 2 günlük TLT ortalaması −2 bp. "
            "Pencerede CPI hiç yok, FOMC hiç yok; NFP içeren 26 pencerede etki daha büyük (TLT −66 bp) ama NFP'siz 93 pencerede de var (TLT −34 bp, TMV net +84 bp, t=2,18). "
            "2020 hariç TMV net 88 bp (t=2,57); 2022 hariç 101 bp (t=2,97). İhale SONRASI toparlanma (A→A+2) ETF verisinde YOK (TLT −9 bp). "
            "Riskler: −3x kaldıraçlı ters ETF (en kötü 2 günlük işlem −%7,6, 2019-08; maxDD −%13); TMV/TBT'nin Midas'ta bulunurluğu doğrulanamadı; "
            "Treasury piyasa yapısı (ihale büyüklüğü, birincil bayi kapasitesi) değişirse etki zayıflayabilir; 2026'da 10 işlemde ortalama +20 bp (zayıfladı mı izlenmeli). "
            "Veri: Yahoo dağıtım düzeltmeli (TMV/TBT dağıtımları Nasdaq verisinde yoktu)."),
 "betik": "kod/ajan_tahvil_doviz/strateji_S1_ihale_oncesi.py",
}

# ---------------- elenenler ----------------
hh = h.copy()
def best(hyp, sym=None, var=None, mode="C0", hh_=None):
    x = hh[(hh.hyp == hyp)]
    if sym: x = x[x.sym == sym]
    if var: x = x[x["var"] == var]
    if mode: x = x[x["mode"] == mode]
    if hh_: x = x[x.h == hh_]
    return x.iloc[0]
def fmt(r):
    return f"{r.sym} {r['mode']} h={int(r.h)}: n={int(r.n)}, brüt {r.mean_gross_bp:.0f} bp, net {r.mean_net_bp:.0f} bp, t={r.t:.2f}, IS {r.is_net_bp:.0f} / OOS {r.oos_net_bp:.0f} bp"
s2 = R("S2_ana.csv").set_index(["sym", "mode"])
elenen = [
 {"ad": "Genel kütüphane (31 sinyal × h × mod) aile içinde", "neden": "Dağıtım-düzeltmeli yeniden çalıştırmada (11880 satır) hiçbir kural temsilcilerin ≥%60'ında net pozitif değil; havuzlanmış sepetlerin hepsi net ≤ +2 bp. Tek tutarlı brüt etki ay sonu (CA_ay_sonu_3: 11/11 tahvil temsilcisinde brüt>0, sepet brüt 9-13 bp, t 2,5-3,5) ama 13-16 bp maliyetin altında. FDR'yi net pozitif geçen 9 satırın hepsi tek ETF/kaldıraçlı (TMF/TMV/TBT) ya da küçük n; aile tutarlılığı yok."},
 {"ad": "TD01 TLT ay sonu (sondan 4./3. gün → ay sonu/ilk gün)", "neden": fmt(best("TD01_ay_sonu", "TLT", "k4_h3_son_gun")) + "; TMF " + fmt(best("TD01_ay_sonu", "TMF", "k4_h3_son_gun")) + ". Brüt etki tüm tahvil ETF'lerinde pozitif (IEF/AGG/GOVT brüt t 3,6-3,9) ama OOS'ta TLT'de 2 bp'ye düşmüş (CXO bulgusuyla uyumlu); t<2."},
 {"ad": "TD02 ihale SONRASI toparlanma (A30/A10 → +2 gün TLT long)", "neden": fmt(best("TD02_ihale_sonrasi", "TLT", "A30_h2", hh_=2)) + ". ETF verisinde ihale sonrası toparlanma yok."},
 {"ad": "TD03 FOMC (D-2→D+1 ve D-1→D) — TLT/TMF long", "neden": f"D-1→D TMF C0: n={int(s2.loc[('TMF','C0'),'n'])}, net {s2.loc[('TMF','C0'),'mean_net_bp']:.0f} bp, t={s2.loc[('TMF','C0'),'t']:.2f} (IS t {s2.loc[('TMF','C0'),'is_t']:.2f}, OOS t {s2.loc[('TMF','C0'),'oos_t']:.2f}); O1 net {s2.loc[('TMF','O1'),'mean_net_bp']:.0f} bp, C1 {s2.loc[('TMF','C1'),'mean_net_bp']:.0f} bp (etki D-1 kapanışı→D açılışında). Isınma penceresi 60→0 gün değişince t 2,19→1,91 (kırılgan); 2025 ve 2026 negatif. TLT brüt 24 bp (t 2,5) gerçek ama küçük: eşik altı."},
 {"ad": "TD04 CPI/NFP öncesi TLT long", "neden": fmt(best("TD04_CPI_NFP", "TLT", "CPI_veya_NFP")) + " (beklenenin tersi)."},
 {"ad": "TD10 TLT RSI2/IBS iki yönlü dönüş (TLT/TMF long, TMV/TBT ters)", "neden": "TLT RSI2<10 → TLT: " + fmt(best("TD10_TLT_donus", "TLT", "RSI2<10_long", hh_=3)) + "; RSI2>90 → TMV: " + fmt(best("TD10_TLT_donus", "TMV", "RSI2>90_ters", hh_=3)) + "; IBS kuralları net negatif. Hiçbiri t≥2 değil."},
 {"ad": "TD11 10 yıllık getiri değişimi z-skoru (|z|≥2) sonrası dönüş", "neden": fmt(best("TD11_faiz_z", "TLT", "dDGS10_z>=2_TLTal(donus)", hh_=1)) + " — dönüş değil, ertesi gün devam (momentum) görülüyor ama C1'de kayboluyor ve sonradan seçilmiş yön olur; z≤−2 → TMV net 37 bp, t 0,55."},
 {"ad": "TD05 FOMC günü döviz (FXA/UDN/FXE long, UUP)", "neden": "Brüt 5-16 bp, maliyet 27-47 bp: tümü net −22..−41 bp (ör. " + fmt(best("TD05_FOMC_doviz", "FXA")) + ")."},
 {"ad": "TD06 ay sonu USD hedge dengelemesi", "neden": fmt(best("TD06_ay_sonu_USD", "FXE", "SPY_ay_ici>=+3%")) + "; UUP (SPY ≤ −%3) n=19 net −35 bp."},
 {"ad": "TD07 FXY güvenli liman (SPY ≤ −%2 veya VIX +%20)", "neden": fmt(best("TD07_FXY_guvenli_liman", "FXY", hh_=2)) + ". Ters yönde (şok sonrası yen/frank geri veriyor; FXF O1 brüt −16 bp, t −5,2) ama işlenebilir ucuz araç yok (YCS 47 bp) ve sonradan bulunan yön."},
 {"ad": "TD08 döviz gün saati (gece vs gün içi)", "neden": "UUP/FXE/FXY/FXF/FXB'de gece ve gün içi ortalamalar |≤2,3| bp/gün; maliyet 20-47 bp. Ekonomik değil."},
 {"ad": "TD09 bakır/altın oranı → TBT/TMV", "neden": fmt(best("TD09_bakir_altin", "TBT")) + " (IS negatif)."},
 {"ad": "TD12 USDJPY ← DGS2 değişimi (YCS/FXY)", "neden": fmt(best("TD12_JPY_DGS2", "YCS")) + "; " + fmt(best("TD12_JPY_DGS2", "FXY", "dDGS2_z<=-1.5_FXY")) + "."},
 {"ad": "TD13 HYG/JNK ← SPY", "neden": "Kendi gecikmesi kontrollü SPY→HYG t=−2,96 (IS −2,5 / OOS −1,5), −11 bp/sd < 13 bp; SPY z≤−1,5 sonrası HYG long " + fmt(best("TD13_HY_SPY", "HYG", "SPY_z1<=-1.5", hh_=1)) + "."},
 {"ad": "TD14 döviz 5 günlük momentum/dönüş", "neden": "7 döviz ETF'inde 14 kural: en iyisi " + fmt(hh[hh.hyp == "TD14_doviz_5g"].sort_values("t").iloc[-1]) + "."},
 {"ad": "Döviz ETF'leri ← ABD hisseleri (SPY/HYG/LQD) gecikmesi", "neden": "İstatistiksel olarak gerçek (FDR; IS/OOS aynı işaret; gece ve gün içi parçalarında; likit UUP'ta da var → yalnız bayat kapanış artefaktı değil) ama 1 sd başına 5-9 bp. İşlem kuralı (SPY z≥1 → FXE/FXF/FXY/FXB, SPY z≤−1 → UUP): brüt +2..+8 bp, net −14..−44 bp; z≥2 eşiğinde bile net < 0 (10.000 $ pozisyonda en iyi +3 bp, t<1)."},
 {"ad": "BIL/SGOV 'yetişme' (catch-up) sonuçları", "neden": "leadlag_sweep'te t≈7-11 ama 1 sd başına 0,4-1 bp (maliyet 13-14 bp). Ayrıca eksik dağıtım verisinin testere dişi deseninden kaynaklanıyor: dağıtım-düzeltmeli veride kendi gecikmesi kontrol edilince işaret dönüyor/kayboluyor. Ekonomik değil."},
 {"ad": "GOVT/TBT/TIP/SCHP 'yetişme' satırları", "neden": "Kendi gecikmesi kontrollü t 1,8-3,0 ama 1 sd başına 4-16 bp < 14-20 bp maliyet (TBT←IEF h3 kontrollü t=1,83)."},
 {"ad": "VERİ UYARISI (genel_tum.csv ve leadlag_sweep.csv)", "neden": "Nasdaq API NYSE Arca/Cboe listeli ETF'lerin dağıtımlarını vermiyor: ailenin 33/40 ETF'inde (HYG, AGG, LQD, TIP, MUB, BIL, SGOV, JNK, EDV, ZROZ, GOVT, TLH, SCHP, USHY, BKLN, STIP, TMF/TMV/TBT/UBT, döviz ETF'leri) toplam getiri eksik; ex-date (ayın ilk işlem günü) getirileri −16..−42 bp aşağı yanlı ve CA_ay_sonu sinyali sahte negatif çıkıyordu (HYG brüt −34 bp, t_edge −7). Bu aile Yahoo dağıtım olaylarıyla (td.load) yeniden hesaplandı; diğer aileler (ör. SPY dahil NYSE Arca listeli hisse ETF'leri) için de aynı sorun olabilir."},
]

# ---------------- lead-lag ----------------
llo = R("leadlag_izleme_oncu.csv"); sv = R("leadlag_suruculer.csv")
TVMAP = {"TLT": "NASDAQ:TLT", "IEF": "NASDAQ:IEF", "LQD": "AMEX:LQD", "TIP": "AMEX:TIP", "DGS30_d": "TVC:US30Y", "DGS10_d": "TVC:US10Y",
         "DFII10_d": "FRED:DFII10", "DGS2_d": "TVC:US02Y", "T10YIE_d": "FRED:T10YIE", "FXY": "AMEX:FXY", "GLD": "AMEX:GLD", "HYG": "AMEX:HYG", "SPY": "AMEX:SPY"}
NAMES = {"DGS30_d": "ABD 30 yıllık getiri değişimi (yüzde puan; beta = getiri/1 puan)", "DGS10_d": "ABD 10 yıllık getiri değişimi (yüzde puan)",
         "DFII10_d": "10 yıllık reel getiri (TIPS) değişimi (yüzde puan; FRED günlük, gecikmeli yayımlanır)", "TLT": "TLT", "IEF": "IEF (7-10 yıl)", "LQD": "LQD (yatırım yapılabilir kredi)", "TIP": "TIP"}
RT = [
 {"ad": "Ultra T-Bond vadeli (CBOT)", "tv": "CBOT:UB1!", "neden": "TLT'nin süresine en yakın vadeli; CME Globex Pazar-Cuma neredeyse 23 saat (kış TR 02:00 → ertesi gün 01:00, 01:00-02:00 ara; yaz saatinde bir saat erken). TR 12:00-17:30 arasında TLT/TMV açılış boşluğunu önceden gösterir — öncü değil, izleme aracı."},
 {"ad": "30 yıllık T-Bond vadeli (CBOT)", "tv": "CBOT:ZB1!", "neden": "UB1! ile aynı saatler; daha likit."},
 {"ad": "10 yıllık T-Note vadeli (CBOT)", "tv": "CBOT:ZN1!", "neden": "Faiz piyasasının en likit vadelisi; ABD veri açıklamaları (TR 16:30) anında tepki."},
 {"ad": "ABD 30 yıllık getiri", "tv": "TVC:US30Y", "neden": "TLT ile eşzamanlı korelasyon −0,97; Asya/Avrupa saatlerinde de kotasyon."},
 {"ad": "ABD 10 yıllık getiri", "tv": "TVC:US10Y", "neden": "Genel faiz yönü; CPI/NFP (TR 16:30) tepkisi açılıştan önce görülür."},
 {"ad": "Almanya 10 yıllık getiri", "tv": "TVC:DE10Y", "neden": "Avrupa seansında (TR ~10:00-19:00) küresel faiz hareketi; ABD açılışından önce."},
 {"ad": "Japonya 10 yıllık getiri", "tv": "TVC:JP10Y", "neden": "Asya seansında (TR ~03:00-09:00) küresel uzun vade baskısı (BoJ)."},
]
def ll_entry(sym, sign):
    sur = []
    for r in sv[sv.target == sym].head(5).itertuples():
        if r.driver in TVMAP:
            sur.append({"ad": NAMES.get(r.driver, r.driver) + " — eşzamanlı, öncü değil", "tv": TVMAP[r.driver], "corr_1y": round(r.corr_1y, 3), "beta_1y": round(r.beta_1y, 3)})
    s = m.loc[("TMV", "C0")] if sym == "TMV" else None
    tr = {"TMV": (fam.loc["TMV"], m.loc[("TMV", "C0")]), "TBT": (fam.loc["TBT"], m.loc[("TBT", "C0")]), "TLT": (fam.loc["TLT"], None), "TMF": (fam.loc["TMF"], None)}[sym]
    fr, mm = tr
    on = {"ad": "10Y Hazine ihale takvimi: A-3 kapanışı → A-1 kapanışı penceresi", "tv": "yok (takvim: TreasuryDirect 'Upcoming Auctions' / TradingView Ekonomik Takvim '10-Year Note Auction')",
          "tip": "takvim olayı (önceden bilinir; gecikmeli öngörü)", "ufuk": "t+1..t+2 (A-2, A-1)",
          "etki": f"{sym} brüt {fr.mean_gross_bp:+.0f} bp / pencere (t {fr.t_gross:.2f}); TLT −41 bp", "t": round(float(fr.t_gross), 2),
          "fdr": True}
    if mm is not None:
        on.update({"is_t": round(float(mm.is_t), 2), "oos_t": round(float(mm.oos_t), 2),
                   "maliyet_sonrasi": f"net {mm.mean_net_bp:+.0f} bp/işlem (2.500 $; t={mm.t:.2f}) — strateji S1"})
    else:
        on.update({"is_t": None, "oos_t": None, "maliyet_sonrasi": "long yönde işlenmez (açığa satış yok): risk kuralı = pencerede long taşıma; kısa yön TMV/TBT ile (S1)"})
    on = {k: v for k, v in on.items() if v is not None}
    oth = llo[(llo.target == sym)].sort_values("p").head(1).iloc[0]
    note = (f"Fiyat/faiz/kredi/risk öncüleri arasında doğrulanmış gecikmeli öncü YOK: {sym} için 18-19 aday × h∈{{1,3}} (kendi gecikmesi kontrollü, NW) içinde "
            f"BH-FDR (224 testlik izleme seti) geçen 0; en güçlüsü {oth.leader} (h{int(oth.h)}) t={oth.t:.2f}, {oth.bp_per_sd:+.0f} bp/sd. leadlag_sweep'te de bu hedef için FDR'li öncü yok. "
            "Tek gecikmeli öngörücü TAKVİM: 10Y ihale öncesi pencere (S1). Eşzamanlı sürücüler (30Y/10Y getiri, IEF, LQD) öncü değildir.")
    return {"sym": sym, "suruculer": sur, "onculer": [on], "gercek_zamanli": RT + ([{"ad": "S&P 500 E-mini vadeli", "tv": "CME_MINI:ES1!", "neden": "Risk iştahı; hisse-tahvil korelasyonu rejime göre değişiyor (2022'de pozitif)."}] if sym in ("TLT", "TMF") else []),
            "not": note,
            "takvim_riskleri": ("10 Kas 2026 Sal: 10Y ihale (13:00 ET=TR 21:00) + CPI (TR 16:30) aynı gün; 11 Kas Çar Veterans Day (tahvil nakit piyasası kapalı, NYSE açık: ince işlem); "
                                "12 Kas Per 30Y ihale; 26 Kas NYSE kapalı, 27 Kas erken kapanış 13:00 ET (TR 21:00); 4 Ara Cum NFP (8 Ara ihale penceresinin içinde: tarihsel olarak etki daha büyük ama oynak); "
                                "8 Ara Sal 10Y yeniden ihraç; 9 Ara Çar FOMC (SEP; TR 22:00); 10 Ara Per 30Y + CPI; 24 Ara erken kapanış, 25 Ara kapalı. "
                                "TMV/TBT çeyreklik dağıtım ex-date'leri ~Mar/Haz/Eyl/Ara 20-25'i (S1 penceresine denk gelmez).")}
leadlag = [ll_entry(s, 0) for s in ["TMV", "TBT", "TLT", "TMF"]]

ozet = ("Tahvil-döviz ailesinde (40 ETF) eşiği geçen TEK strateji: S1 — 10 yıllık Hazine ihalesinden 3 işlem günü önce (A-3) TMV (−3x TLT) al, "
        f"ihaleden bir gün önce (A-1) kapanışta sat. TMV C0: n={int(t0.n)}, brüt {t0.mean_gross_bp:.0f} bp, net {t0.mean_net_bp:.0f} bp (2.500 $), t={t0.t:.2f}, "
        f"IS {t0.is_net_bp:.0f} / OOS {t0.oos_net_bp:.0f} bp, yılların %{100*t0.years_pos_frac:.0f}'i pozitif, maxDD {100*t0.maxdd:.0f}%. Dayanakta TLT bu pencerede ortalama −41 bp "
        "(t −3,7; plasebo pencerelerde yok; tüm süre-duyarlı tahvil ETF'lerinde aynı işaret). Önceden kayıtlı hipotez; odaklı birincil sette tek yönlü FDR'yi geçen iki satırdan biri. "
        "Güven 'orta': kaldıraçlı ters ETF gerektiriyor, Midas'ta TMV/TBT bulunurluğu doğrulanamadı, A-2 açılışında girişte OOS zayıf (A-3 seansında girilmeli). "
        "Diğer her şey (ay sonu, FOMC, CPI/NFP, IBS/RSI2, faiz z-skoru, bakır/altın, HYG←SPY, tüm döviz kuralları) maliyet sonrası eşik altında: tahvil ETF'lerinin 1 günlük hareketi "
        "(25-60 bp) 13-16 bp maliyeti zor karşılıyor; döviz ETF'leri hem likiditesiz hem 20-47 bp maliyetli. Döviz ETF'lerindeki 'ABD hisseleri dün yükseldi → döviz bugün yükselir' "
        "gecikmesi gerçek (likit UUP'ta da, gün içi parçada da) ama 1 sd başına 5-9 bp: işlenemez. ÖNEMLİ VERİ BULGUSU: Nasdaq verisinde NYSE Arca listeli ETF'lerin dağıtımları eksik; "
        "aile Yahoo dağıtımlarıyla yeniden hesaplandı (genel_tum.csv'nin bu ailedeki ay sonu/ex-date sonuçları yanlı).")
out = {"family": "tahvil_doviz", "ozet": ozet, "izleme": izleme, "stratejiler": [S1], "elenen": elenen, "leadlag": leadlag,
       "tv_dogrulanacak": ["AMEX:TBF (ProShares Short 20+ Year Treasury, −1x; kaldıraçsız ters alternatif — veri ve TV kodu doğrulanmadı)",
                           "TradingView Ekonomik Takvim '10-Year Note Auction' girdisi (kod değil; takvim kontrolü TreasuryDirect ile yapılmalı)"],
       "dosyalar": [os.path.join(td.ROOT, p) for p in [
           "notlar/aile_tahvil_doviz.md", "sonuclar/aile_tahvil_doviz/sonuc.json",
           "kod/ajan_tahvil_doviz/strateji_S1_ihale_oncesi.py", "kod/ajan_tahvil_doviz/td.py", "kod/ajan_tahvil_doviz/00_temettu_indir.py",
           "kod/ajan_tahvil_doviz/01_islenebilirlik.py", "kod/ajan_tahvil_doviz/02a_genel_duzeltilmis.py", "kod/ajan_tahvil_doviz/02_genel_aile.py",
           "kod/ajan_tahvil_doviz/03_hipotezler.py", "kod/ajan_tahvil_doviz/04_leadlag.py", "kod/ajan_tahvil_doviz/strateji_S2_fomc.py",
           "kod/ajan_tahvil_doviz/06_sonuc_json.py",
           "sonuclar/aile_tahvil_doviz/S1_ana.csv", "sonuclar/aile_tahvil_doviz/S1_aile.csv", "sonuclar/aile_tahvil_doviz/S1_komsu.csv",
           "sonuclar/aile_tahvil_doviz/S1_plasebo.csv", "sonuclar/aile_tahvil_doviz/S1_yillar.csv", "sonuclar/aile_tahvil_doviz/S1_islemler_TMV_C0.csv",
           "sonuclar/aile_tahvil_doviz/hipotez_testleri.csv", "sonuclar/aile_tahvil_doviz/genel_duzeltilmis.csv",
           "sonuclar/aile_tahvil_doviz/genel_aile_tutarlilik_tahvil.csv", "sonuclar/aile_tahvil_doviz/genel_aile_havuz.csv",
           "sonuclar/aile_tahvil_doviz/islenebilirlik.csv", "sonuclar/aile_tahvil_doviz/kopya_gruplari.csv",
           "sonuclar/aile_tahvil_doviz/leadlag_izleme_oncu.csv", "sonuclar/aile_tahvil_doviz/leadlag_fx_spy.csv", "sonuclar/aile_tahvil_doviz/leadlag_fx_kural.csv",
           "sonuclar/aile_tahvil_doviz/leadlag_catch_kontrollu.csv", "sonuclar/aile_tahvil_doviz/temettu_yahoo.csv"]]}
json.dump(out, open(os.path.join(O, "sonuc.json"), "w"), ensure_ascii=False, indent=1)
print("yazıldı", os.path.join(O, "sonuc.json"))
print(json.dumps(out["stratejiler"][0], ensure_ascii=False, indent=1)[:3000])
