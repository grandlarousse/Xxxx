"""s07: HAKEM_sablon.md içindeki {{...}} yer tutucularını CSV/JSON çıktılarından üretilen Markdown tablolarıyla doldurup HAKEM.md yazar."""
import json, re, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/sentez"


def fmt(v):
    if v is None or (isinstance(v, float) and np.isnan(v)): return "—"
    if isinstance(v, (float, np.floating)):
        s = f"{v:.2f}" if abs(v) < 100 else f"{v:.0f}"
        return s.replace(".", ",")
    if isinstance(v, (int, np.integer)): return f"{v:,}".replace(",", ".")
    return str(v).replace("|", "/").replace("\n", " ")


def md(df, cols=None, rename=None):
    df = df.copy()
    if cols: df = df[cols]
    if rename: df = df.rename(columns=rename)
    h = "| " + " | ".join(map(str, df.columns)) + " |\n|" + "---|" * len(df.columns) + "\n"
    return h + "\n".join("| " + " | ".join(fmt(v) for v in r) + " |" for r in df.itertuples(index=False))


T = {}
# --- FDR
d = pd.read_csv(f"{OUT}/fdr_siniflandirma.csv", low_memory=False)
cls = d.groupby(["sinif", "alan"]).size().unstack(fill_value=0).reset_index()
cls["toplam"] = cls.ETF + cls.VIOP
lab = {"X1_KAPANIS": "X1 kapanışta/cutoff sonrası", "X2_MEKANIK": "X2 mekanik", "X3_TANI": "X3 tanı/kontrol/betimsel", "X4_KAPKAP_DEGIL": "X4 kapanıştan kapanışa değil",
       "X5_GORELI_CEPHE": "X5 göreli/spread ya da cephe dışı", "X6_KOPYA": "X6 birebir kopya", "R1_SAGLAMLIK": "R1 sağlamlık/varyant (işlenebilir, birincil değil)",
       "R2_ERKEN": "R2 erken dönem tekrarı (işlenebilir, birincil değil)", "BIRINCIL": "Birincil işlenebilir öngörü"}
cls["sinif"] = cls.sinif.map(lab)
T["FDR_SINIF"] = md(cls[["sinif", "VIOP", "ETF", "toplam"]], rename={"sinif": "Sınıf"})
F = pd.read_csv(f"{OUT}/fdr_ozet.csv")
F["kume"] = F.kume.map({"islenebilir_genis": "işlenebilir (geniş)", "birincil": "birincil"})
F["min_q"] = F.min_q.map(lambda v: f"{v:.4f}".replace(".", ",")); F["beklenen_p005"] = F.beklenen_p005.map(lambda v: f"{v:.1f}".replace(".", ","))
T["FDR_OZET"] = md(F, ["kume", "alan", "n_test", "p_lt_005", "beklenen_p005", "abs_t_ge3", "q_lt_005", "q_lt_010", "bonf_lt_005", "bonf_esik_t", "min_q"],
                   {"kume": "Küme", "alan": "Alan", "n_test": "Test", "p_lt_005": "p<0,05", "beklenen_p005": "Şansla beklenen", "abs_t_ge3": "mutlak t≥3", "q_lt_005": "BH q<0,05",
                    "q_lt_010": "BH q<0,10", "bonf_lt_005": "Bonferroni<0,05", "bonf_esik_t": "Bonf. t eşiği", "min_q": "En küçük q"})
P = pd.read_csv(f"{OUT}/fdr_gecenler.csv")
P = P[(P.kume == "birincil") & (P.q_bh < 0.05)].copy()
def fen(r):
    t = r.test_id
    if "zm" in t or "zA_" in t or "zB_" in t or "xau_intraday" in t: return "altın gün içi hareketi → madenci ertesi gün ters"
    if "PLATIN" in t or "1328" in t: return "metal 1-5 g hareketi → GDX ters"
    if "GDX~GLD+SPY_k10" in t: return "madenci artığı → GLD"
    return "?"
P["fenomen"] = P.apply(fen, axis=1)
P["q_bh"] = P.q_bh.map(lambda v: f"{v:.4f}".replace(".", ",")); P["p_bonf"] = P.p_bonf.map(lambda v: f"{v:.4f}".replace(".", ","))
T["FDR_GECEN"] = md(P, ["agent", "test_id", "h", "t", "t_is", "t_oos", "q_bh", "p_bonf", "fenomen"],
                    {"agent": "Aile", "test_id": "Test", "t_is": "t IS", "t_oos": "t OOS", "q_bh": "q (BH, alan içi)", "p_bonf": "Bonferroni p", "fenomen": "Fenomen"})
# --- sinyal tablosu
S2 = pd.read_csv(f"{OUT}/sinyal_tablosu.csv")
ay = S2[S2.ayakta != "HAYIR"].copy()
T["AYAKTA"] = md(ay, ["id", "cephe", "son_guven", "kural", "bilgi_zamani", "h", "etki_bps_islem", "etki_yillik", "t_IS", "t_OOS", "oos_sharpe_net", "oos_bh_sharpe",
                      "hakem_OOS_sharpe", "hakem_OOS_sharpe_stres", "hakem_OOS_BH", "hakem_2022p_sharpe", "hakem_2022p_BH", "hakem_2026_sharpe", "hakem_gidis_donus_yil", "ana_zayiflik", "islenebilirlik"],
                 {"id": "İddia", "cephe": "Cephe", "son_guven": "SON güven", "kural": "Kural", "bilgi_zamani": "Bilgi zamanı", "etki_bps_islem": "Etki (işlem başı, brüt)",
                  "etki_yillik": "Etki (yıllık, net)", "t_IS": "t IS", "t_OOS": "t OOS", "oos_sharpe_net": "OOS net Sharpe (analist)", "oos_bh_sharpe": "OOS B&H (analist)",
                  "hakem_OOS_sharpe": "Hakem OOS Sharpe", "hakem_OOS_sharpe_stres": "Hakem OOS stres", "hakem_OOS_BH": "Hakem OOS B&H", "hakem_2022p_sharpe": "Hakem 2022+",
                  "hakem_2022p_BH": "B&H 2022+", "hakem_2026_sharpe": "Hakem 2026", "hakem_gidis_donus_yil": "Gidiş-dönüş/yıl", "ana_zayiflik": "Ana zayıflık", "islenebilirlik": "İşlenebilirlik"})
T["TUM_IDDIA"] = md(S2, ["id", "cephe", "h", "bilgi_zamani", "etki_bps_islem", "t_IS", "t_OOS", "oos_sharpe_net", "oos_bh_sharpe", "yilda_islem", "analist", "rep", "adv", "son_guven", "ayakta", "ana_zayiflik", "islenebilirlik"],
                    {"id": "İddia", "cephe": "Cephe", "bilgi_zamani": "Bilgi zamanı", "etki_bps_islem": "Etki", "t_IS": "t IS", "t_OOS": "t OOS", "oos_sharpe_net": "OOS net Sharpe",
                     "oos_bh_sharpe": "OOS B&H", "yilda_islem": "İşlem/yıl", "analist": "Analist", "rep": "REP", "adv": "ADV", "son_guven": "SON", "ayakta": "Ayakta",
                     "ana_zayiflik": "Ana zayıflık", "islenebilirlik": "İşlenebilirlik"})
# --- doğrulama
D = pd.read_csv(f"{OUT}/dogrulama.csv")
dv = D[D.donem.isin(["tam", "IS", "OOS"])].pivot_table(index=["sinyal"], columns=["getiri", "donem"], values="sharpe").round(2)
dv.columns = [f"{a} {b}" for a, b in dv.columns]
dv = dv.reset_index()
bh = D[(D.donem == "OOS")].pivot_table(index="sinyal", columns="getiri", values="bh_sharpe").round(2).reset_index().rename(columns={"basit": "B&H OOS basit", "log": "B&H OOS log"})
dv = dv.merge(bh, on="sinyal")
T["DOGRULAMA"] = md(dv, ["sinyal", "log tam", "log IS", "log OOS", "B&H OOS log", "basit tam", "basit IS", "basit OOS", "B&H OOS basit"], {"sinyal": "Sinyal (hakem kodu)"})
# --- korelasyonlar
for nm, f in [("KOR_VIOP_POZ", "korelasyon_viop_poz.csv"), ("KOR_VIOP_PNL", "korelasyon_viop_pnl.csv"), ("KOR_ETF_POZ", "korelasyon_etf_poz.csv"), ("KOR_ETF_PNL", "korelasyon_etf_pnl.csv")]:
    c = pd.read_csv(f"{OUT}/{f}").rename(columns={"Unnamed: 0": " "})
    T[nm] = md(c)
# --- birleşim
CB = pd.read_csv(f"{OUT}/birlesim.csv")
T["BIRLESIM"] = md(CB, ["cephe", "donem", "maliyet", "sharpe", "t", "yillik_pct", "vol_pct", "maxDD_pct", "maruziyet", "bh_sharpe", "bh_yillik_pct", "alfa_yillik_pct", "alfa_t", "beklenen_yariya_sharpe", "beklenen_yariya_yillik_pct"],
                   {"cephe": "Cephe", "donem": "Dönem", "maliyet": "Maliyet", "sharpe": "Net Sharpe", "yillik_pct": "Yıllık %", "vol_pct": "Vol %", "maxDD_pct": "Maks. düşüş %", "maruziyet": "Ort. mutlak poz.",
                    "bh_sharpe": "B&H Sharpe", "bh_yillik_pct": "B&H yıllık %", "alfa_yillik_pct": "Alfa % (sepete göre)", "alfa_t": "Alfa t", "beklenen_yariya_sharpe": "Yarıya: Sharpe", "beklenen_yariya_yillik_pct": "Yarıya: yıllık %"})
YR = pd.read_csv(f"{OUT}/birlesim_yillik.csv")
T["BIRLESIM_YIL"] = md(YR.rename(columns={"date": "Yıl"}))
# --- rejim ve 2026
RG = pd.read_csv(f"{OUT}/rejim_iki_dilim.csv")
rp = RG.pivot(index="sinyal", columns="rejim", values="sharpe").reset_index()
ra = RG.pivot(index="sinyal", columns="rejim", values="aktif_gun").reset_index().rename(columns={"rv<%18": "aktif gün rv<%18", "rv>=%18": "aktif gün rv≥%18"})
A = pd.read_csv(f"{OUT}/etkinlik_2026.csv")
rr = rp.merge(ra, on="sinyal").merge(A, on="sinyal")
T["REJIM"] = md(rr, ["sinyal", "rv<%18", "rv>=%18", "aktif gün rv<%18", "aktif gün rv≥%18", "aktif_gun_pay_tum", "aktif_gun_pay_2026", "net_2026_pct"],
                {"sinyal": "Sinyal", "rv<%18": "Sharpe rv20<%18", "rv>=%18": "Sharpe rv20≥%18", "aktif_gun_pay_tum": "Aktif gün payı (tüm)", "aktif_gun_pay_2026": "Aktif gün payı 2026", "net_2026_pct": "2026 net % (1x)"})
# --- risk
V = pd.read_csv(f"{OUT}/risk_var.csv")
V = V[V.arac.isin(["VIOP_F_XAUUSD", "GLD", "GDX", "GDXJ", "NUGT"]) & V.donem.isin(["2026", "2017-2026"])]
T["VAR"] = md(V, ["arac", "donem", "h", "vol_yillik_pct", "VaR95_tarihsel_pct", "VaR99_tarihsel_pct", "ES975_pct", "VaR99_normal_pct", "en_kotu_pct"],
              {"arac": "Araç", "donem": "Dönem", "vol_yillik_pct": "Yıllık vol %", "VaR95_tarihsel_pct": "VaR95 %", "VaR99_tarihsel_pct": "VaR99 %", "ES975_pct": "ES97,5 %",
               "VaR99_normal_pct": "VaR99 normal %", "en_kotu_pct": "En kötü %"})
TM = pd.read_csv(f"{OUT}/risk_teminat.csv")
T["TEMINAT"] = md(TM, None, {"kaldirac": "Nominal/özsermaye", "ozsermaye_pay_teminat_pct": "Teminatın özsermayeye oranı %", "kayip99_1g_2026_pct": "1g VaR99 kayıp % (2026)",
                             "kayip99_5g_2026_pct": "5g VaR99 kayıp % (2026)", "enkotu5g_2026_pct": "En kötü 5g % (2026)", "kayip99_5g_2017_pct": "5g VaR99 % (2017-26)"})
SO = pd.read_csv(f"{OUT}/risk_stop.csv")
SO = SO[SO.esik_sigma == 2.0]
T["STOP"] = md(SO, ["arac", "nakit_gun", "stop_sharpe", "bh_sharpe", "stop_yillik", "bh_yillik", "fark_yillik_pct", "nakit_gun_pay"],
               {"arac": "Araç", "nakit_gun": "2σ düşüşten sonra nakit gün", "stop_sharpe": "Stoplu Sharpe", "bh_sharpe": "B&H Sharpe", "stop_yillik": "Stoplu yıllık %", "bh_yillik": "B&H yıllık %",
                "fark_yillik_pct": "Fark (yüzde puan)", "nakit_gun_pay": "Nakitte gün payı"})
SS = pd.read_csv(f"{OUT}/risk_stop_sinyal.csv")
T["STOP_SINYAL"] = md(SS, None, {"sinyal": "Sinyal", "stopsuz_sharpe": "Stopsuz Sharpe", "stoplu_sharpe": "Stoplu Sharpe", "stopsuz_yillik": "Stopsuz yıllık %", "stoplu_yillik": "Stoplu yıllık %", "stop_gun": "Stop günü"})
R = json.load(open(f"{OUT}/risk_ozet.json"))
k = R["kosullu"]
rows = []
for nm in ["VIOP_2017_2026", "spot_2010_2026", "spot_2010_2016", "GLD_2008_2026", "GDX_2008_2026", "GDXJ_2010_2026"]:
    x = k[nm]; rows.append(dict(seri=nm, asagi_h1=x["asagi_2s_h1_bps"], asagi_h1_t=x["asagi_2s_h1_t"], asagi_h5=x["asagi_2s_h5_bps"], yukari_h1=x["yukari_2s_h1_bps"], yukari_h5=x["yukari_2s_h5_bps"],
                                 kos_h1=x["kosulsuz_h1_bps"], kos_h5=x["kosulsuz_h5_bps"], n=x["asagi_2s_h1_n"]))
T["KOSULLU"] = md(pd.DataFrame(rows), None, {"seri": "Seri", "asagi_h1": "2σ düşüş sonrası 1g (bps)", "asagi_h1_t": "t", "asagi_h5": "2σ düşüş sonrası 5g", "yukari_h1": "2σ yükseliş sonrası 1g",
                                              "yukari_h5": "2σ yükseliş sonrası 5g", "kos_h1": "Koşulsuz 1g", "kos_h5": "Koşulsuz 5g", "n": "2σ düşüş sayısı"})
txt = open(f"{OUT}/HAKEM_sablon.md").read()
for kk, v in T.items(): txt = txt.replace("{{" + kk + "}}", v)
left = re.findall(r"\{\{[A-Z_]+\}\}", txt)
open(f"{OUT}/HAKEM.md", "w").write(txt)
print("yazıldı; doldurulmamış:", left, "| uzunluk", len(txt))
