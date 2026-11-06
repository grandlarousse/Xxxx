"""Bedelsiz olay listesi: Is Yatirim hak kullanim (bolunme) tarihi + oran  <->  KAP bildirimleri (yayim zamani) <-> SPK bulteni.
Asamalar (her biri icin kamuya acik olma ZAMANI):
  P1 'yk'      : ilk bedelsiz bildirimi (YK karari / genel kurul teklifi). Bedelsiz temettude KAP 'Kar Payi Dagitimi' ilk bildirimi de aday.
  P2 'basvuru' : SPK basvurusunun ilk duyurusu (KAP ozet/govde 'basvur' ; 2014-17 bultenlerinde 'Yeni Basvurular' tablosu).
  P3 'onay'    : SPK onayi: min(KAP onay bildirimi, SPK bulteni 'Onaylanan' tablosunda sirket unvani). Bulten saati bilinmiyorsa 18:30 varsayilir.
  P4 'hak'     : hak kullanim (bolunme) gunu (Is Yatirim).
Cikti: <CACHE>/olaylar_bedelsiz.pkl ve repo: olaylar_bedelsiz.csv (kaynak indeksleri ile; ham veri degil, turetilmis olay listesi)."""
import os, re, json, numpy as np, pandas as pd
import f06_spk_parse as SP
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bedelsiz"
HERE = os.path.dirname(os.path.abspath(__file__))
BON_T = ["Bedelsiz Sermaye Artırımı", "Bedelsiz Temettü", "Bedelli ve Bedelsiz Sermaye Artırımı", "Bedelsiz ve Nakit Temettü"]
RX_BON = r"bedelsiz|iç kaynak|ic kaynak|iç kaynaklardan|bölünme|bolunme"
RX_NEG = r"bedelli|tahsis|rüçhan|ruchan|nakit|azalt|halka arz|birleşme|kullanılmayan|kayıtlı sermaye tavan|şarta bağlı|sarta bagli"
RX_POST = r"tescil|tamamlan|ilan|dağıtım tarih|dağıtıl|hak kullanım|kullanım başlangıç|kayda alın|başlangıç tarih"   # onceki/ayni olayin kapanis bildirimleri
def detaylar():
    D = {}
    p = f"{CACHE}/kap_detay.jsonl"
    if not os.path.exists(p): return D
    for l in open(p):
        try: d = json.loads(l)
        except Exception: continue
        t = re.sub(r"[\r\t]", " ", d["txt"]); parts = [x.strip() for x in t.split("|") if x.strip() and x.strip() != "&nbsp;"]
        def val(lab_rx):
            for i, x in enumerate(parts[:-1]):
                if re.fullmatch(lab_rx, x): return parts[i + 1]
            return None
        def tarih(v):
            if not v: return pd.NaT
            m = re.search(r"(\d{2})[./](\d{2})[./](\d{4})", v)
            return pd.Timestamp(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else pd.NaT
        tl = t.lower()
        D[d["idx"]] = dict(
            yk=tarih(val(r"Yönetim Kurulu Karar Tarihi")),
            spk_bas=tarih(val(r"SPK Başvuru Tarihi") or val(r"Ana Sözleşmenin Sermaye Maddesinin Tadiline İlişkin SPK Başvuru Tarihi")),
            spk_onay=tarih(val(r"SPK Onay Tarihi") or val(r"Ana Sözleşmenin Sermaye Maddesinin Tadiline İlişkin SPK Onay Tarihi")),
            hak=tarih(val(r"Bedelsiz Pay Alma Hakkı Kullanım Başlangıç Tarihi") or val(r"Bedelsiz Sermaye Artırımı Hak Kullanım Başlangıç Tarihi")),
            ozet=val(r"Özet Bilgi") or "",
            bonus=("bedelsiz pay alma" in tl) or bool(re.search(r"bedelsiz", (val(r"Özet Bilgi") or "").lower())),
            ruchan=("rüçhan hakkı kullanım oranı" in tl) or ("bedelli" in (val(r"Özet Bilgi") or "").lower()),
            guncelleme=(val(r"Yapılan Açıklama Güncelleme mi ?") or val(r"Yapılan Açıklama Güncelleme mi\?") or "") == "Evet")
    return D
def kap_meta():
    k = pd.read_pickle(f"{CACHE}/kap_CA_all.pkl").copy()
    s = k.summary.fillna("").str.lower()
    s = s.str.replace(r"art[ıi]r[ıi]m[ıi]?\s*[-/]?\s*azalt[ıi]m[ıi]?", "artirim", regex=True)   # sablon adi 'Artirimi/Azaltimi' -> notr
    bon = s.str.contains(RX_BON); neg = s.str.contains(RX_NEG) & ~bon
    k["cls"] = np.where(bon, "bon", np.where(neg, "neg", "amb"))
    k["codes"] = k.stockCodes.fillna("").str.replace(" ", "").str.split(",")
    return k.explode("codes")
def kpd_meta():
    k = pd.read_pickle(f"{CACHE}/kap_KPD_all.pkl").copy()
    k["codes"] = k.stockCodes.fillna("").str.replace(" ", "").str.split(",")
    return k.explode("codes")
GENEL = {"turkiye", "anadolu", "dogan", "global", "is", "ak", "turk", "yeni", "park", "ege", "marmara", "akdeniz"}
def anahtar(unvan):
    w = [x for x in SP.norm(unvan).split() if x not in {"a", "s", "as", "t"}]
    return " ".join(w[:3] if (w and w[0] in GENEL) else w[:2])
def kur():
    isy = pd.read_csv(f"{CACHE}/isy_sermaye_all.csv", parse_dates=["tarih"])
    isy["bdsz"] = isy[["SHHE_BDSZ_IK_ORAN", "SHHE_BDSZ_TM_ORAN", "SHHE_BDSZ_BU_ORAN"]].fillna(0).sum(axis=1)
    b = isy[isy.SHT_TANIMI.isin(BON_T)].copy()
    b = (b.groupby(["HISSE_KODU", "tarih"]).agg(tip=("SHT_TANIMI", lambda x: "+".join(sorted(set(x)))), oran=("bdsz", "sum"),
          bedelli=("SHHE_BDLI_ORAN", "sum"), ik=("SHHE_BDSZ_IK_ORAN", "sum"), tm=("SHHE_BDSZ_TM_ORAN", "sum"),
          once=("HSP_BOLUNME_ONCESI_SERMAYE", "first"), sonra=("HSP_BOLUNME_SONRASI_SERMAYE", "last"), unvan=("HisseTanim", "first")).reset_index())
    b = b[(b.tarih >= "2014-06-01") & (b.tarih <= "2026-11-05")].sort_values(["HISSE_KODU", "tarih"]).reset_index(drop=True)
    allb = isy[isy.SHT_TANIMI.isin(BON_T)][["HISSE_KODU", "tarih"]]
    K = kap_meta(); KP = kpd_meta(); D = detaylar()
    BUL = pd.read_pickle(f"{CACHE}/spk/bulten_bolum.pkl")
    out = []
    for _, e in b.iterrows():
        T, X = e.HISSE_KODU, e.tarih
        prev = allb[(allb.HISSE_KODU == T) & (allb.tarih < X)].tarih.max()
        lo = max(prev + pd.Timedelta(days=1) if pd.notna(prev) else pd.Timestamp("2000-01-01"), X - pd.Timedelta(days=540))
        m = K[(K.codes == T) & (K.pt > lo) & (K.pt <= X + pd.Timedelta(hours=23))].sort_values("pt").copy()
        det = [D.get(i) for i in m.disclosureIndex]
        m["d_bonus"] = [x["bonus"] if x else None for x in det]; m["d_ruchan"] = [x["ruchan"] if x else None for x in det]
        m["d_yk"] = [x["yk"] if x else pd.NaT for x in det]; m["d_bas"] = [x["spk_bas"] if x else pd.NaT for x in det]
        m["d_onay"] = [x["spk_onay"] if x else pd.NaT for x in det]; m["d_hak"] = [x["hak"] if x else pd.NaT for x in det]
        sm = m.summary.fillna("").str.lower()
        post = sm.str.contains(RX_POST)
        has_d = m.d_bonus.notna()
        d_bon = m.d_bonus.fillna(False).astype(bool) & ~m.d_ruchan.fillna(False).astype(bool)
        # bedelsize ait: (ozet 'bedelsiz') ya da (detay bedelsiz gosteriyor); detaysiz 'amb' = belirsiz
        isb = (m.cls == "bon") | (has_d & d_bon)
        unk = (m.cls == "amb") & ~has_d
        mb_sure = m[isb].copy(); mb = m[isb | unk].copy()
        core_sure = m[isb & ~post]; core_unk = m[unk & ~post & sm.str.contains("karar|başvur|basvur|onay|sonuç|sonuc|izin")]
        r = dict(kod=T, hak=X, tip=e.tip, oran=e.oran, bedelli_oran=e.bedelli, ik=e.ik, tm=e.tm, once=e.once, sonra=e.sonra,
                 n_kap=len(m), n_kap_bon=len(mb_sure), n_detay=int(m.d_bonus.notna().sum()))
        unv = m.kapTitle.mode().iloc[0] if len(m) else e.unvan
        r["unvan"] = unv; r["anahtar"] = anahtar(unv)
        # --- P1: ilk bedelsiz bildirimi (kapanis/tescil turu bildirimler haric)
        p1 = core_sure.pt.min() if len(core_sure) else pd.NaT
        yk = mb_sure.d_yk.dropna()
        r["yk_tarih"] = yk.iloc[-1] if len(yk) else pd.NaT       # son bildirimdeki YK karar tarihi
        r["p1_kaynak"] = "KAP-CA"
        if "Temettü" in e.tip:
            kp = KP[(KP.codes == T) & (KP.pt > max(lo, X - pd.Timedelta(days=200))) & (KP.pt < X)]
            if len(kp) and (pd.isna(p1) or kp.pt.min() < p1): p1 = kp.pt.min(); r["p1_kaynak"] = "KAP-KPD"
        # detaysiz belirsiz bir YK/basvuru bildirimi P1'den once ise isaretle (detay gelince cozulur)
        u_before = core_unk[core_unk.pt < (p1 if pd.notna(p1) else X + pd.Timedelta(days=1))]
        r["p1_belirsiz"] = bool(len(u_before))
        r["p1_alt"] = u_before.pt.min() if len(u_before) else pd.NaT   # belirsiz aday dahil en erken zaman
        r["p1"] = p1
        if pd.notna(r["yk_tarih"]) and pd.notna(p1) and p1.normalize() < r["yk_tarih"] - pd.Timedelta(days=3):
            r["p1_not"] = "ilk bildirim YK tarihinden once (plan degisikligi?)"
        # --- P2: SPK basvurusu duyurusu
        after = mb[(mb.pt >= (p1 if pd.notna(p1) else lo)) & ~mb.summary.fillna("").str.lower().str.contains("şarta bağlı")]
        sa = after.summary.fillna("").str.lower()
        c_bas = after[(sa.str.contains("başvur|basvur|müracaat") & ~sa.str.contains("sonuc|sonuç|onay")) | after.d_bas.notna()]
        r["p2_kap"] = c_bas.pt.min() if len(c_bas) else pd.NaT
        r["spk_bas_tarih"] = after.d_bas.dropna().iloc[-1] if after.d_bas.notna().any() else pd.NaT
        # --- P3: SPK onayi (KAP)
        c_on = after[sa.str.contains("onay|sonuc|sonuç|izin") | after.d_onay.notna()]
        c_on = c_on[c_on.pt >= (r["p2_kap"] if pd.notna(r["p2_kap"]) else p1 if pd.notna(p1) else lo)]
        r["p3_kap"] = c_on.pt.min() if len(c_on) else pd.NaT
        r["spk_onay_tarih"] = after.d_onay.dropna().iloc[-1] if after.d_onay.notna().any() else pd.NaT
        # --- SPK bulteni: onay ve basvuru tablolarinda unvan anahtari
        key = r["anahtar"]; bl = BUL[(BUL.tarih >= (p1.normalize() - pd.Timedelta(days=3) if pd.notna(p1) else lo)) & (BUL.tarih <= X)]
        if len(key) >= 5:
            on = bl[bl.onay.str.contains(r"\b" + re.escape(key) + r"\b", regex=True)]
            ba = bl[bl.basvuru.str.contains(r"\b" + re.escape(key) + r"\b", regex=True)]
        else: on = ba = bl.iloc[0:0]
        if len(on):
            z = on.iloc[-1]; r["bulten_onay_no"] = z.no; r["bulten_onay_tarih"] = z.tarih
            r["bulten_onay_zaman"] = z.yayim_tsi if pd.notna(z.yayim_tsi) else z.tarih + pd.Timedelta(hours=18, minutes=30)
            r["bulten_onay_saat_bilinen"] = pd.notna(z.yayim_tsi)
        if len(ba):
            z = ba.iloc[0]; r["bulten_bas_no"] = z.no
            r["bulten_bas_zaman"] = z.yayim_tsi if pd.notna(z.yayim_tsi) else z.tarih + pd.Timedelta(hours=18, minutes=30)
        # P3: bulten esleşmisse bulten zamani; KAP onay bildirimi bultenden en fazla 3 gun once ise KAP (sirket erken duyurmus).
        # KAP 'onay' bildirimi bultenden >3 gun onceyse farkli bir onaydir (esas sozlesme uygun gorusu vb.) -> kullanilmaz.
        bz = r.get("bulten_onay_zaman", pd.NaT); kz = r["p3_kap"]
        if pd.notna(bz):
            if pd.notna(kz) and bz - pd.Timedelta(days=3) <= kz < bz: r["p3"], r["p3_kaynak"] = kz, "KAP (bultenden once)"
            else: r["p3"], r["p3_kaynak"] = bz, "bulten"
        elif pd.notna(kz): r["p3"], r["p3_kaynak"] = kz, "KAP"
        else: r["p3"], r["p3_kaynak"] = pd.NaT, None
        cands = [x for x in [r["p2_kap"], r.get("bulten_bas_zaman", pd.NaT)] if pd.notna(x)]
        r["p2"] = min(cands) if cands else pd.NaT
        r["idx_ilk"] = int(mb_sure.disclosureIndex.iloc[0]) if len(mb_sure) else None
        out.append(r)
    ev = pd.DataFrame(out)
    # tutarlilik: siralama P1 <= P2 <= P3 <= hak
    for a, c in [("p2", "p1"), ("p3", "p2"), ("p3", "p1")]:
        bad = ev[a].notna() & ev[c].notna() & (ev[a] < ev[c]); ev.loc[bad, a + "_sira_uyari"] = True
    ev.loc[ev.p3.notna() & (ev.p3 > ev.hak + pd.Timedelta(hours=23)), "p3"] = pd.NaT
    ev.to_pickle(f"{CACHE}/olaylar_bedelsiz.pkl")
    cols = ["kod", "unvan", "tip", "oran", "bedelli_oran", "yk_tarih", "p1", "p1_kaynak", "p2", "spk_bas_tarih", "p3", "p3_kaynak", "spk_onay_tarih",
            "bulten_onay_no", "hak", "n_kap", "n_kap_bon", "n_detay", "idx_ilk"]
    ev[[c for c in cols if c in ev.columns]].to_csv(f"{HERE}/olaylar_bedelsiz.csv", index=False)
    return ev
if __name__ == "__main__":
    ev = kur()
    print(len(ev), "olay")
    for c in ["p1", "p2", "p3", "yk_tarih", "spk_onay_tarih", "bulten_onay_no"]:
        print(c, ev[c].notna().sum())
    print(ev.p3_kaynak.value_counts(dropna=False))
    print(ev.groupby(ev.hak.dt.year).agg(n=("kod", "size"), p1=("p1", "count"), p2=("p2", "count"), p3=("p3", "count"), bul=("bulten_onay_no", "count")))
