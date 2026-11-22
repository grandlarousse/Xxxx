"""F5 Takvim etkileri: 1-3 günlük kapanış alımında takvim kuralları bugün işe yarıyor mu?

Kurallar (YONTEM.md bölüm 4 F5; önceden yazılı hipotezler ek/hipotez/birlesik.csv, ajan l4_takvim_olay + e1_enerji):
  Ay dönümü (T = ayın son işlem günü), tatil öncesi / yarım gün / Şükran Günü, FOMC (planlı karar günleri),
  opsiyon vadesi (aylık / üç aylık), haftanın günü (iki yönlü), çeyrek sonu / ayın ilk günü, TÜFE ve istihdam raporu.
Sinyal: giriş günü t kapanışında +1 (AL) ya da -1 (SAT, hipotez yönü '-'); çıkış t+h kapanışı. Takvim t kapanışında
tümüyle bilinir (ileri bakış yok). Tatiller NYSE takvimindeki boşluklardan çıkarılır.
İstatistik ortak.py'den: donemli_test, ek_olcutler, plasebo_dairesel, siniflandir, havuz_donemli, son_sinyal.

Girdi : veri/ (ortak.py), ek/backtest/f5_takvim/ham/ (federalreserve.gov ve bls.gov sayfalarının kaydı; web'e çıkmaz)
Çıktı : ek/backtest/f5_takvim/{sonuclar.csv, ayakta_kalanlar.csv, kural_ozet.csv, takvim_6hafta.csv, fomc_tarihleri.csv,
        makro_tarihleri.csv}
Kullanım: python3 kod/f5_takvim.py
"""
import os
import re
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

CIK = os.path.join(o.KOK, "ek", "backtest", "f5_takvim")
HAM = os.path.join(CIK, "ham")
os.makedirs(CIK, exist_ok=True)

HEDEF_HISSE = ["SPY", "QQQ", "IWM", "DIA", "XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLV", "XLY",
               "SMH", "XBI", "KRE", "XOP", "GDX", "ITB", "XRT", "IYT", "XME", "OIH"]
HEDEF_DIGER = ["GLD", "SLV", "USO", "UNG", "DBA", "CPER", "TLT", "HYG"]
HEDEFLER = HEDEF_HISSE + HEDEF_DIGER
SON_VERI = pd.Timestamp("2026-11-20")
T1_GECIS = "2024-05-28"  # T+1 takas
AYLAR = "January|February|March|April|May|June|July|August|September|October|November|December"
AY_NO = {a: i + 1 for i, a in enumerate(AYLAR.split("|"))}
AY_NO.update({a[:3]: i + 1 for i, a in enumerate(AYLAR.split("|"))})  # "Jan/Feb 31-1" biçimi
AYLAR_K = AYLAR + "|" + "|".join(a[:3] for a in AYLAR.split("|"))
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


# ---------------------------------------------------------------------------------------------------------------
# 1. Genişletilmiş NYSE takvimi (veri + bilinen gelecek günler; ay sonu konumu son ayda yanlış çıkmasın diye)
# ---------------------------------------------------------------------------------------------------------------
tam = o.oku("SPY").index
tam = tam[tam <= SON_VERI]
gelecek = pd.bdate_range("2026-11-23", "2027-02-26")
gelecek = gelecek[~gelecek.isin(pd.to_datetime(["2026-11-26", "2026-12-25", "2027-01-01", "2027-01-18", "2027-02-15"]))]
E = tam.append(gelecek)
E = E[E >= "2003-01-01"]
POS = pd.Series(np.arange(len(E)), index=E)
TK = o.takvim()

# Tatiller: hafta içi olup işlem olmayan günler (boşluklar). Sandy (2012-10-29/30) plansız kapanıştır, çıkarılır.
is_gunleri = pd.bdate_range(E[0], E[-1])
tatil = is_gunleri[~is_gunleri.isin(E)]
PLANSIZ = pd.to_datetime(["2012-10-29", "2012-10-30"])
tatil_plan = tatil[~tatil.isin(PLANSIZ)]
sonraki_is = E + pd.offsets.BDay(1)
pretatil_gun = E[np.asarray(sonraki_is.isin(tatil_plan))]


def sukran(y):
    k1 = pd.Timestamp(y, 11, 1)
    return k1 + pd.Timedelta(days=(3 - k1.weekday()) % 7 + 21)


YILLAR = range(2003, 2027)
SUKRAN = pd.DatetimeIndex([sukran(y) for y in YILLAR])
yarim = [s + pd.Timedelta(days=1) for s in SUKRAN] + [pd.Timestamp(y, 12, 24) for y in YILLAR] + \
        [pd.Timestamp(y, 7, 3) for y in YILLAR]
YARIM = pd.DatetimeIndex(sorted(d for d in yarim if d in POS.index))

# ---------------------------------------------------------------------------------------------------------------
# 2. FOMC planlı karar günleri: federalreserve.gov sayfaları (ham/) + sayfası çekilmeyen yıllar için bellek listesi
# ---------------------------------------------------------------------------------------------------------------
BELLEK = {  # karar (son) günü, planlı toplantılar
    2005: "02-02 03-22 05-03 06-30 08-09 09-20 11-01 12-13", 2006: "01-31 03-28 05-10 06-29 08-08 09-20 10-25 12-12",
    2007: "01-31 03-21 05-09 06-28 08-07 09-18 10-31 12-11", 2008: "01-30 03-18 04-30 06-25 08-05 09-16 10-29 12-16",
    2009: "01-28 03-18 04-29 06-24 08-12 09-23 11-04 12-16", 2010: "01-27 03-16 04-28 06-23 08-10 09-21 11-03 12-14",
    2011: "01-26 03-15 04-27 06-22 08-09 09-21 11-02 12-13", 2012: "01-25 03-13 04-25 06-20 08-01 09-13 10-24 12-12",
    2013: "01-30 03-20 05-01 06-19 07-31 09-18 10-30 12-18", 2014: "01-29 03-19 04-30 06-18 07-30 09-17 10-29 12-17",
    2015: "01-28 03-18 04-29 06-17 07-29 09-17 10-28 12-16", 2016: "01-27 03-16 04-27 06-15 07-27 09-21 11-02 12-14",
    2017: "02-01 03-15 05-03 06-14 07-26 09-20 11-01 12-13", 2018: "01-31 03-21 05-02 06-13 08-01 09-26 11-08 12-19",
    2019: "01-30 03-20 05-01 06-19 07-31 09-18 10-30 12-11", 2020: "01-29 04-29 06-10 07-29 09-16 11-05 12-16",
}


def _karar(m1, m2, d1, d2, y):
    ay = AY_NO[m2] if m2 else AY_NO[m1]
    return pd.Timestamp(y, ay, int(d2) if d2 else int(d1))


def fomc_tarihleri():
    satir = []
    yol = os.path.join(HAM, "fomccalendars.txt")
    t = open(yol).read()
    bloklar = re.split(r"(\d{4}) FOMC Meetings", t)
    for i in range(1, len(bloklar) - 1, 2):
        y = int(bloklar[i])
        if y > 2026:
            continue
        for m in re.finditer(rf"\b({AYLAR_K})(?:/({AYLAR_K}))? (\d{{1,2}})(?:-(\d{{1,2}}))?(\*)?\s+(?:Statement|\* Meeting|$)",
                             bloklar[i + 1]):
            satir.append((_karar(m.group(1), m.group(2), m.group(3), m.group(4), y), y, "fomccalendars.htm",
                          int(bool(m.group(5)))))
    sayfa_yil = set()
    for f in sorted(os.listdir(HAM)):
        mm = re.match(r"fomchistorical(\d{4})\.txt", f)
        if not mm:
            continue
        y = int(mm.group(1))
        sayfa_yil.add(y)
        t = open(os.path.join(HAM, f)).read()
        for m in re.finditer(rf"({AYLAR})(?:/({AYLAR}))? (\d{{1,2}})(?:-(?:({AYLAR}) )?(\d{{1,2}}))? (\((?:unscheduled|cancelled)\) )?Meeting - {y}", t):
            if m.group(6):
                continue
            m2 = m.group(4) or m.group(2)
            satir.append((_karar(m.group(1), m2, m.group(3), m.group(5), y), y, f"fomchistorical{y}.htm", np.nan))
    d = pd.DataFrame(satir, columns=["tarih", "yil", "kaynak", "sep"]).drop_duplicates("tarih")
    # bellek listesi: sayfası çekilmeyen yıllar + sayfada eksik çıkan toplantılar; çekilen yıllarda karşılaştırma
    kontrol = []
    for y, s in BELLEK.items():
        b = [pd.Timestamp(f"{y}-{x}") for x in s.split()]
        if y in sayfa_yil:
            sy = set(d.loc[d.yil == y, "tarih"])
            kontrol.append((y, len(b), len(sy), sorted(set(b) ^ sy)))
            for x in b:
                if x not in sy:
                    satir.append((x, y, "bellek (sayfada bulunamadı)", np.nan))
        else:
            for x in b:
                satir.append((x, y, "bellek", np.nan))
    d = pd.DataFrame(satir, columns=["tarih", "yil", "kaynak", "sep"]).drop_duplicates("tarih").sort_values("tarih")
    d["islem_gunu"] = d["tarih"].isin(POS.index)
    return d.reset_index(drop=True), kontrol


FOMC, fomc_kontrol = fomc_tarihleri()
FOMC.assign(tarih=FOMC.tarih.dt.date).to_csv(os.path.join(CIK, "fomc_tarihleri.csv"), index=False)
log("FOMC:", len(FOMC), "tarih; sayfa/bellek karşılaştırma (yıl, bellek n, sayfa n, fark):", fomc_kontrol)
FOMC_GUN = pd.DatetimeIndex(FOMC.loc[FOMC.islem_gunu & (FOMC.tarih >= "2005-01-01"), "tarih"])


# ---------------------------------------------------------------------------------------------------------------
# 3. TÜFE ve istihdam raporu günleri (bls.gov arşiv sayfalarının bağlantılarından; 08:30 ET açıklanır)
# ---------------------------------------------------------------------------------------------------------------
def bls(ad):
    h = open(os.path.join(HAM, f"bls_{ad}.html")).read()
    g = sorted(set(pd.Timestamp(f"{x[4:]}-{x[:2]}-{x[2:4]}") for x in re.findall(rf"archives/{ad}_(\d{{8}})\.(?:htm|pdf)", h)))
    return pd.DatetimeIndex(g)


MAKRO = {"nfp": bls("empsit"), "cpi": bls("cpi")}
pd.DataFrame([(k, d.date(), d in POS.index) for k, v in MAKRO.items() for d in v],
             columns=["rapor", "tarih", "islem_gunu"]).to_csv(os.path.join(CIK, "makro_tarihleri.csv"), index=False)
log("BLS:", {k: len(v) for k, v in MAKRO.items()}, "kapalı güne düşen:",
    {k: [str(d.date()) for d in v if d not in POS.index and d >= pd.Timestamp('2005-01-01')] for k, v in MAKRO.items()})

# ---------------------------------------------------------------------------------------------------------------
# 4. Kurallar: giriş günleri (E üzerinde konum), h, önceden yazılı yön
# ---------------------------------------------------------------------------------------------------------------
per = E.to_period("M")
T_POS = POS.groupby(per).max().values[1:]  # ilk ay (veri başlangıcı) tam olmayabilir
T_GUN = E[T_POS]
CEYREK = np.isin(T_GUN.month, [3, 6, 9, 12])
CUMA = T_GUN.weekday == 4


def kp(p):
    p = np.asarray(p, dtype=int)
    return p[(p >= 0) & (p < len(E))]


def poz(gunler):
    g = pd.DatetimeIndex(gunler)
    return POS.reindex(g).dropna().astype(int).values


KURAL = {}  # ad: dict(giris=konumlar, h, yon, grup, tanim)


def ekle(ad, giris, h, yon, grup, tanim):
    KURAL[ad] = dict(giris=kp(giris), h=h, yon=yon, grup=grup, tanim=tanim)


# Ay dönümü
ekle("tom_a", T_POS - 4, 3, "+", "ay_donumu", "T-4 -> T-1")
ekle("tom_b", T_POS - 3, 3, "+", "ay_donumu", "T-3 -> T")
ekle("tom_c", T_POS, 3, "+", "ay_donumu", "T -> T+3")
ekle("tom_d", T_POS - 1, 4, "+", "ay_donumu", "T-1 -> T+3 (4 gün)")
for k in range(-3, 4):
    ekle(f"gun_T{k:+d}", T_POS + k - 1, 1, "+", "ay_donumu", f"tek gün: T{k:+d} günü getirisi")
ekle("tom_a_cuma", T_POS[CUMA] - 4, 3, "+", "ay_donumu", "T-4 -> T-1, T cuma")
ekle("tom_a_cumadegil", T_POS[~CUMA] - 4, 3, "+", "ay_donumu", "T-4 -> T-1, T cuma değil")
ekle("tom_c_cuma", T_POS[CUMA], 3, "+", "ay_donumu", "T -> T+3, T cuma")
ekle("tom_c_cumadegil", T_POS[~CUMA], 3, "+", "ay_donumu", "T -> T+3, T cuma değil")
ekle("ceyrek_son_gun", T_POS[CEYREK] - 1, 1, "+", "ceyrek", "çeyrek sonu son gün (T, Mar/Haz/Eyl/Ara)")
ekle("ay_son_gun_ceyrekdisi", T_POS[~CEYREK] - 1, 1, "+", "ceyrek", "çeyrek dışı ay sonu son gün")
ekle("ceyrek_ilk_gun", T_POS[CEYREK], 1, "+", "ceyrek", "çeyreğin ilk işlem günü (T+1)")
ekle("ay_ilk_gun_ceyrekdisi", T_POS[~CEYREK], 1, "+", "ceyrek", "çeyrek dışı ayın ilk işlem günü")
# Tatil
P_PRE = poz(pretatil_gun)
ekle("pretatil", P_PRE - 1, 1, "+", "tatil", "tatil öncesi son işlem günü")
ekle("pretatil_tam", poz(pretatil_gun[~pretatil_gun.isin(YARIM)]) - 1, 1, "+", "tatil", "tatil öncesi gün, tam gün")
ekle("pretatil_yarim", poz(pretatil_gun[pretatil_gun.isin(YARIM)]) - 1, 1, "+", "tatil", "tatil öncesi gün, yarım gün (24 Ara, 3 Tem)")
ekle("yarim_gun", poz(YARIM) - 1, 1, "+", "tatil", "bütün yarım günler (Şükran sonrası cuma dahil)")
ekle("sukran_hafta", poz(SUKRAN - pd.Timedelta(days=2)), 2, "+", "tatil", "Şükran salı kapanışı -> cuma (yarım gün) kapanışı")
# FOMC
P_F = poz(FOMC_GUN)
vix = o.panel("adjclose", ["^VIX"])["^VIX"].reindex(E)
vix_gec = vix.shift(1)
ekle("fomc_once", P_F - 1, 1, "+", "fomc", "karar gününden önceki kapanış -> karar günü kapanışı")
for h in (1, 2, 3):
    ekle(f"fomc_sonra_h{h}", P_F, h, "+", "fomc", f"karar günü kapanışı -> {h} gün")
v20 = lambda p: p[(vix.iloc[p] > 20).values]  # noqa: E731  (VIX 16:15 ET: 15 dk ileri bakış riski işaretli)
ekle("fomc_once_vix20", v20(P_F - 1), 1, "+", "fomc", "fomc_once, giriş günü VIX > 20")
for h in (1, 2, 3):
    ekle(f"fomc_sonra_vix20_h{h}", v20(P_F), h, "+", "fomc", f"fomc_sonra_h{h}, giriş günü VIX > 20")
# Opsiyon vadesi (3. cuma; tatil ise önceki işlem günü). Haftalık kurallar yalnız 5 işlem günlük tam haftalarda.
ops = []
for y in range(2004, 2027):
    for m in range(1, 13):
        a1 = pd.Timestamp(y, m, 1)
        F = a1 + pd.Timedelta(days=(4 - a1.weekday()) % 7 + 14)
        if F > pd.Timestamp("2026-12-31"):
            continue
        e = POS[POS.index <= F]
        on = POS[POS.index <= F - pd.Timedelta(days=7)]
        so = POS[POS.index <= F + pd.Timedelta(days=7)]
        ops.append((F, int(e.iloc[-1]), int(on.iloc[-1]), int(so.iloc[-1]), m in (3, 6, 9, 12)))
OPS = pd.DataFrame(ops, columns=["F", "p_vade", "p_once", "p_sonra", "ceyrek"])
OPS["tam_once"] = (OPS.p_vade - OPS.p_once) == 5
OPS["tam_sonra"] = (OPS.p_sonra - OPS.p_vade) == 5
q = OPS.ceyrek.values
ekle("opex_hafta", OPS.p_once[OPS.tam_once], 5, "-", "opsiyon", "vade haftası: önceki cuma -> 3. cuma (SAT; hipotez 12)")
ekle("opex_hafta_ceyrek", OPS.p_once[OPS.tam_once & q], 5, "-", "opsiyon", "üç aylık vade haftası (SAT; hipotez 13)")
ekle("opex_hafta_aylik", OPS.p_once[OPS.tam_once & ~q], 5, "-", "opsiyon", "üç aylık olmayan vade haftası (SAT)")
ekle("opex_sonra_hafta", OPS.p_vade[OPS.tam_sonra], 5, "+", "opsiyon", "vadeden sonraki hafta: 3. cuma -> sonraki cuma (AL; hipotez 11)")
ekle("opex_sonra_hafta_ceyrek", OPS.p_vade[OPS.tam_sonra & q], 5, "-", "opsiyon", "üç aylık vadeden sonraki hafta (SAT; hipotez 13)")
ekle("opex_sonra_hafta_aylik", OPS.p_vade[OPS.tam_sonra & ~q], 5, "+", "opsiyon", "aylık vadeden sonraki hafta (AL)")
for h in (1, 2, 3):
    ekle(f"opex_sonra_h{h}", OPS.p_vade, h, "+", "opsiyon", f"vade günü kapanışı -> {h} gün (AL; hipotez 11)")
# Haftanın günü (giriş günü; ertesi işlem günü kapanışında çıkış). Önceden yazılı yön yok: iki yön ayrı test.
GUN_AD = ["pzt", "sal", "car", "per", "cum"]
for i, g in enumerate(GUN_AD):
    p = POS.values[E.weekday == i]
    ekle(f"al_{g}", p, 1, "+", "hafta_gunu", f"{g} kapanışında al, ertesi işlem günü kapanışında sat")
    ekle(f"sat_{g}", p, 1, "-", "hafta_gunu", f"{g} kapanışında sat, ertesi işlem günü kapanışında kapat")
# Makro raporlar (08:30 ET): önceki kapanışta al, rapor günü kapanışında sat
for k, v in MAKRO.items():
    v = v[(v >= "2005-01-01") & (v <= SON_VERI)]
    ekle(f"{k}_once", poz(v) - 1, 1, "+", "makro", f"{k.upper()} günü: önceki kapanış -> rapor günü kapanışı (hipotez 10)")

# Hipotez yönü özel durumlar (haftanın günü ızgarasının içinde): UNG çarşamba girişi '-', USO çarşamba girişi '+'
OZEL = {("sat_car", "UNG"): "hipotez e1#0: UNG perşembe (depolama raporu günü) SAT",
        ("al_car", "USO"): "hipotez e1#10: USO çarşamba (WPSR) sonrası perşembe AL",
        ("al_sal", "USO"): "USO rapor günü (çarşamba) getirisi",
        ("sat_sal", "USO"): "USO rapor günü (çarşamba) getirisi"}

TOM_KURAL = [k for k, v in KURAL.items() if v["grup"] in ("ay_donumu", "ceyrek")]
log("tatil öncesi gün/yıl:", pd.Series(pretatil_gun.year).value_counts().sort_index().to_dict())
log("yarım gün/yıl:", pd.Series(YARIM.year).value_counts().sort_index().to_dict())
log("kural sayısı:", len(KURAL), "hedef:", len(HEDEFLER))


def sinyal(ad):
    v = KURAL[ad]
    s = pd.Series(0.0, index=E)
    s.iloc[v["giris"]] = 1.0 if v["yon"] == "+" else -1.0
    return s


SIN_E = {k: sinyal(k) for k in KURAL}
SIN = {k: s.reindex(TK).fillna(0.0) for k, s in SIN_E.items()}

# ---------------------------------------------------------------------------------------------------------------
# 5. Testler
# ---------------------------------------------------------------------------------------------------------------
BAYAT = o.bayat_hedefler()
vix_tk, vixg_tk = vix.reindex(TK), vix_gec.reindex(TK)


def yan_bolum(s, hedef, h, giris, onek, maske):
    r = o.islem_testi(s.where(maske, 0.0), hedef, h, giris=giris)
    return {f"{onek}_n": r.get("n", 0), f"{onek}_anormal_bps": r.get("anormal_net_bps"), f"{onek}_t": r.get("t_anormal")}


satirlar = []
for ad, v in KURAL.items():
    s = SIN[ad]
    for hd in HEDEFLER:
        giris = "acilis" if hd in BAYAT else "kapanis"
        d = o.donemli_test(s, hd, v["h"], giris=giris)
        d.update(aile="F5", sinyal_id=f"{ad}|{hd}|h{v['h']}", oncu="TAKVIM", bicim=ad, yon=v["yon"], grup=v["grup"],
                 tanim=v["tanim"], havuz="tek hedef", bayat_isaret=int(hd in BAYAT), not_=OZEL.get((ad, hd), ""))
        d.update(o.son_sinyal(s))
        # rejim ayrımı (sınıflandırılmaz): giriş günü VIX > 20, 1 gün gecikmeli VIX ile
        d.update(yan_bolum(s, hd, v["h"], giris, "vixg20", vixg_tk > 20))
        if ad in TOM_KURAL:  # T+1 takas geçişi öncesi / sonrası
            d.update(yan_bolum(s, hd, v["h"], giris, "t1once", s.index < T1_GECIS))
            d.update(yan_bolum(s, hd, v["h"], giris, "t1sonra", s.index >= T1_GECIS))
        satirlar.append(d)
    log(ad, "bitti")
df = pd.DataFrame(satirlar).rename(columns={"not_": "not"})
df.to_parquet(os.path.join(CIK, "ara_sonuclar.parquet"))
log("ana testler:", len(df))

# Ön eleme -> pahalı ölçütler (yıl yıl, açılış/ertesi giriş, dairesel plasebo, 1-4 gün kaydırma, SPY'dan arındırma)
num = lambda c: pd.to_numeric(df[c], errors="coerce")  # noqa: E731
on = ((num("is_t_anormal") >= 2.0) & (num("oos_t_anormal") >= 1.5) & (num("is_anormal_net_bps") > 0)
      & (num("oos_anormal_net_bps") > 0)) | (num("is_t_anormal") >= 2.5)
log("ön elemeyi geçen:", int(on.sum()))
for i in df.index[on]:
    ad, hd, h = df.at[i, "bicim"], df.at[i, "hedef"], int(df.at[i, "h"])
    s = SIN[ad]
    e = o.ek_olcutler(s, hd, h)
    kay = [o.islem_testi(s.shift(k).fillna(0.0), hd, h).get("anormal_net_bps", np.nan) for k in (1, 2, 3, 4)]
    e["kaydirma_anormal_ort"] = round(float(np.nanmean(kay)), 1)
    e["kaydirma_anormal_max"] = round(float(np.nanmax(kay)), 1)
    e["kaydirma_ok"] = bool(df.at[i, "tum_anormal_net_bps"] > np.nanmean(kay))
    e["plasebo_p_dairesel"] = e.pop("plasebo_p")
    e["plasebo_p"] = e["plasebo_p_dairesel"] if e["kaydirma_ok"] else 1.0
    if hd != "SPY":
        hh = o.donemli_test(s, hd, h, hedge="SPY")
        e.update({"spyar_is_t": hh.get("is_t_anormal"), "spyar_oos_t": hh.get("oos_t_anormal"),
                  "spyar_tum_bps": hh.get("tum_anormal_net_bps")})
    for k, val in e.items():
        df.at[i, k] = val
log("ek ölçütler bitti")

# Sınıflandırma. SAT bacağında D koşuluna 'ham net >= 0' eklenir (YONTEM.md 6-D): geçici kopyada anormal kırpılır.
tmp = df.copy()
sat_kotu = (tmp["yon"] == "-") & (pd.to_numeric(tmp["tum_net_bps"], errors="coerce") < 0)
tmp.loc[sat_kotu, "tum_anormal_net_bps"] = np.minimum(pd.to_numeric(tmp.loc[sat_kotu, "tum_anormal_net_bps"]), 0)
tmp = o.siniflandir(tmp)
for c in ["k_A", "k_B", "k_B_zayif", "k_C", "k_D", "k_E", "k_F", "k_G", "k_H", "k_I", "p_oos", "bh_oos", "sinif"]:
    df[c] = tmp[c]
N_TEST = len(df)
df.to_csv(os.path.join(CIK, "sonuclar.csv"), index=False)
ayk = df[df["sinif"] != "ELENDI"].copy()
ayk = ayk.sort_values(["sinif", "oos_t_anormal"], key=lambda c: c.map({"SAGLAM": 0, "KOSULLU": 1, "IZLE": 2}) if c.name == "sinif" else -c)
kol = ["sinyal_id", "bicim", "tanim", "hedef", "yon", "h", "tum_n", "oos_n", "tum_anormal_net_bps", "tum_net_bps",
       "is_t_anormal", "oos_t_anormal", "son_n", "son_net_bps", "son_t_anormal", "vixg20_n", "vixg20_anormal_bps", "vixg20_t",
       "t1sonra_n", "t1sonra_anormal_bps", "t1sonra_t", "spyar_is_t", "spyar_oos_t", "plasebo_p_dairesel", "kaydirma_ok",
       "yil_pozitif_oran", "acilis_anormal_bps", "acilis_net_bps", "k_A", "k_B", "k_C", "k_D", "k_E", "k_F", "k_G",
       "k_H", "k_I", "bh_oos", "sinif", "son_gun", "son_sinyal", "not"]
def buyuk5(r):
    f = o.ileri_getiri([r.hedef], int(r.h), "acilis" if r.hedef in BAYAT else "kapanis")[r.hedef]
    x = (SIN[r.bicim] * f)[SIN[r.bicim] != 0].dropna().sort_values(ascending=False)
    return "; ".join(f"{d.date()} {v * 1e4:+.0f}" for d, v in x.head(5).items())


ayk["en_buyuk_5_islem_bps"] = [buyuk5(r) for r in ayk.itertuples()] if len(ayk) else []
kol.append("en_buyuk_5_islem_bps")
ayk[[c for c in kol if c in ayk.columns]].to_csv(os.path.join(CIK, "ayakta_kalanlar.csv"), index=False)
log("sınıflar:", df["sinif"].value_counts().to_dict())

# ---------------------------------------------------------------------------------------------------------------
# 6. Kural özeti: hisse ETF'i havuzu (25 hedef, gün bazlı eşit ağırlıklı portföy t'si; betimleyici, sınıflanmaz)
# ---------------------------------------------------------------------------------------------------------------
oz = []
for ad, v in KURAL.items():
    S = pd.DataFrame({hd: SIN[ad] for hd in HEDEF_HISSE})
    hv = o.havuz_donemli(S, v["h"])
    h0 = o.havuz_donemli(S, v["h"], maliyet_bps=0)  # filtre değerlendirmesi: maliyetsiz (başka sinyalin üstüne biner)
    hz = o.havuz_donemli(S.where(vixg_tk.reindex(S.index) > 20, 0.0), v["h"])  # bugünkü rejim: dünkü VIX > 20
    g = df[df.bicim == ad]
    nsg = int(g.sinif.isin(["SAGLAM", "KOSULLU"]).sum())
    i0, o0 = h0.get("is_t_anormal", np.nan), h0.get("oos_t_anormal", np.nan)
    if nsg:
        deg = "tek başına sinyal"
    elif np.sign(i0) == np.sign(o0) and min(abs(i0), abs(o0)) >= 1.5:
        deg = "filtre adayı: " + ("ekle" if i0 > 0 else "kaçın") + " (kural yönüne göre)"
    elif np.sign(i0) == np.sign(o0) and min(abs(i0), abs(o0)) >= 1.0:
        deg = "zayıf filtre (|t| 1-1,5): " + ("ekle" if i0 > 0 else "kaçın")
    else:
        deg = "işe yaramıyor"
    oz.append({"kural": ad, "grup": v["grup"], "tanim": v["tanim"], "yon": v["yon"], "h": v["h"],
               "havuz_tum_n_gun": hv.get("tum_n_gun"), "havuz_tum_anormal_bps": hv.get("tum_anormal_net_bps"),
               "havuz_tum_net_bps": hv.get("tum_net_bps"),
               "havuz_is_t": hv.get("is_t_anormal"), "havuz_oos_t": hv.get("oos_t_anormal"), "havuz_son_t": hv.get("son_t_anormal"),
               "havuz_son_anormal_bps": hv.get("son_anormal_net_bps"),
               "hedef_is_t_med": round(float(num("is_t_anormal")[g.index].median()), 2),
               "hedef_oos_t_med": round(float(num("oos_t_anormal")[g.index].median()), 2),
               "n_is2_oos15": int(((num("is_t_anormal") >= 2) & (num("oos_t_anormal") >= 1.5))[g.index].sum()),
               "n_oos_neg2": int((num("oos_t_anormal") <= -2)[g.index].sum()),
               "n_ayakta": int((g.sinif != "ELENDI").sum()), "son_sinyal_20kas": float(SIN[ad].iloc[-1]),
               "brut_havuz_tum_bps": h0.get("tum_anormal_net_bps"), "brut_havuz_is_t": i0, "brut_havuz_oos_t": o0,
               "brut_havuz_son_t": h0.get("son_t_anormal"),
               "vix20_havuz_n_gun": hz.get("tum_n_gun"), "vix20_havuz_anormal_bps": hz.get("tum_anormal_net_bps"),
               "vix20_havuz_is_t": hz.get("is_t_anormal"), "vix20_havuz_oos_t": hz.get("oos_t_anormal"),
               "degerlendirme": deg})
OZ = pd.DataFrame(oz)
OZ.to_csv(os.path.join(CIK, "kural_ozet.csv"), index=False)
log("kural özeti yazıldı")

# ---------------------------------------------------------------------------------------------------------------
# 7. Önümüzdeki 6 hafta: hangi gün hangi takvim kuralının girişi var (yön, h, çıkış günü)
# ---------------------------------------------------------------------------------------------------------------
gel_gun = E[(E >= SON_VERI) & (E <= "2026-12-31")]
fut_nfp = pd.to_datetime(["2026-12-04"])
fut_cpi = pd.to_datetime(["2026-12-10"])
ek_giris = {"nfp_once": poz(fut_nfp) - 1, "cpi_once": poz(fut_cpi) - 1}  # bls.gov/schedule sayfasından
ayakta_kural = set(ayk["bicim"])
tk6 = []
for d in gel_gun:
    p = POS[d]
    acik = []
    for ad, v in KURAL.items():
        gir = np.concatenate([v["giris"], ek_giris.get(ad, np.array([], dtype=int))])
        if p in set(gir.tolist()):
            if v["grup"] == "hafta_gunu" and v["yon"] == "-":
                continue
            cik = E[min(p + v["h"], len(E) - 1)].date()
            acik.append(f"{ad}({'SAT' if v['yon'] == '-' else 'AL'},h{v['h']},çıkış {cik}){'*' if ad in ayakta_kural else ''}")
    olay = []
    if d in T_GUN:
        olay.append("T (ay son günü)")
    if d in pretatil_gun:
        olay.append("tatil öncesi gün")
    if d in YARIM:
        olay.append("yarım gün 13:00")
    if d in FOMC.tarih.values:
        olay.append("FOMC karar")
    if d in E[OPS.p_vade.values]:
        olay.append("opsiyon vadesi" + (" (üç aylık)" if d.month in (3, 6, 9, 12) else ""))
    if d in fut_nfp:
        olay.append("istihdam raporu 08:30")
    if d in fut_cpi:
        olay.append("TÜFE 08:30")
    tk6.append({"tarih": d.date(), "gun": GUN_AD[d.weekday()], "olay": "; ".join(olay), "giris_acik": " | ".join(acik)})
pd.DataFrame(tk6).to_csv(os.path.join(CIK, "takvim_6hafta.csv"), index=False)
log("bitti. test sayısı:", N_TEST, "beklenen yanlış pozitif SAĞLAM/KOŞULLU:", round(N_TEST * o.P_SIFIR_SAGLAM, 2),
    round(N_TEST * o.P_SIFIR_KOSULLU, 2))
