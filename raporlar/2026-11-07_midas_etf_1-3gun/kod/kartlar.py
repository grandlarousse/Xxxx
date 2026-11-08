"""Aile ajanı (sonuc.json) + denetçi (denetim.json) çıktılarından ETF kartlarını ve TradingView izleme listelerini üretir.
Kurallar:
  * Strateji: denetçi 'dogrulandi' -> 'Uygulanabilir'; 'zayif' -> 'İzlemede (zayıf kanıt)'; 'curutuldu' -> karta girmez (aile özetinde elenenler).
  * Öncü: aynı mantık (denetçi kararı yoksa 'denetlenmedi' işaretiyle ve yalnız FDR + IS/OOS tutarlıysa).
  * TradingView kodu yalnız sonuclar/tv_etf.csv ve sonuclar/tv_dogrulama.csv'de doğrulanmışsa düz yazılır; değilse '(doğrulanmadı)'.
Çıktı: kartlar/<SYM>.md, izleme_listeleri/<aile>.txt, izleme_listeleri/TUM_ETF_bolumlu.txt, sonuclar/tv_eksik.txt
Kullanım: python3 -I kod/kartlar.py"""
import os, sys, json, csv, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
import kurallar as KR
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

FAM_TR = {"abd_endeks": "ABD endeks ve faktör", "sektor_tematik": "Sektör ve tematik", "tek_hisse_kaldiracli": "Tek hisse kaldıraçlı",
          "enerji_tarim": "Enerji ve tarım emtiası", "metal_madenci": "Değerli/sanayi metalleri ve madenciler", "tahvil_doviz": "Tahvil ve döviz",
          "volatilite": "Volatilite (VIX)", "kripto": "Kripto", "uluslararasi": "Uluslararası / ülke"}
ORDER = ["abd_endeks", "sektor_tematik", "tek_hisse_kaldiracli", "enerji_tarim", "metal_madenci", "tahvil_doviz", "volatilite", "kripto", "uluslararasi"]

def tv_sets():
    ok = {}
    for r in csv.DictReader(open(os.path.join(ROOT, "sonuclar", "tv_etf.csv"))):
        if r["durum"] == "dogrulandi": ok[r["tv"].upper()] = r["tv"]
    p = os.path.join(ROOT, "sonuclar", "tv_dogrulama.csv")
    for r in csv.DictReader(open(p)):
        if r["durum"] in ("dogrulandi", "dogrulandi_kanonik"): ok[r["ticker"].upper()] = r["ticker"]
    etf = {r["sym"]: r["tv"] for r in csv.DictReader(open(os.path.join(ROOT, "sonuclar", "tv_etf.csv"))) if r["durum"] == "dogrulandi"}
    return ok, etf

TV_OK, TV_ETF = tv_sets()
MISSING = set()

def tvfmt(tv):
    """Bir veya birden çok kodu (virgül, '/', ' ve ' ile ayrılmış) doğrulayıp biçimler."""
    if not tv: return "—"
    parts = re.split(r"\s*(?:,|;| ve | veya )\s*", str(tv))
    out = []
    for p in parts:
        p = p.strip().strip("`")
        if not p: continue
        # oran/fark ifadeleri: CBOE:VIX/CBOE:VIX3M
        toks = re.findall(r"[A-Z_]+:[A-Z0-9!\.\-]+", p.upper())
        if not toks:
            out.append(p); continue
        bad = [t for t in toks if t not in TV_OK]
        if bad:
            MISSING.update(bad); out.append(f"`{p}` (doğrulanmadı)")
        else:
            out.append(f"`{p}`")
    return ", ".join(out) if out else "—"

def trnum(x, dec=1):
    """Türkçe sayı biçimi: binlik '.', ondalık ','."""
    try:
        if x is None or (isinstance(x, float) and np.isnan(x)): return "—"
        s_ = f"{float(x):,.{dec}f}"
        return s_.replace(",", "§").replace(".", ",").replace("§", ".")
    except Exception:
        return str(x)

def num(x, fmt="{:.1f}"):
    try:
        if x is None or (isinstance(x, float) and np.isnan(x)): return "—"
        return fmt.format(float(x))
    except Exception:
        return str(x)

def load_fam(fam):
    d = os.path.join(ROOT, "sonuclar", f"aile_{fam}")
    res = json.load(open(os.path.join(d, "sonuc.json"))) if os.path.exists(os.path.join(d, "sonuc.json")) else None
    den = json.load(open(os.path.join(d, "denetim.json"))) if os.path.exists(os.path.join(d, "denetim.json")) else None
    return res, den

def verdict_maps(den):
    sv, ov = {}, {}
    if not den: return sv, ov
    for s in den.get("stratejiler", []): sv[s["id"]] = s
    for o in den.get("onculer", []): ov[(o["sym"].upper(), o["oncu"].upper())] = o
    return sv, ov

def oncu_verdict(ov, sym, o):
    for key in [(sym, (o.get("tv") or "").upper()), (sym, (o.get("ad") or "").upper())]:
        if key in ov: return ov[key]
    # gevşek eşleşme
    for (s, name), v in ov.items():
        if s == sym and (name in (o.get("ad") or "").upper() or name in (o.get("tv") or "").upper() or (o.get("ad") or "").upper() in name):
            return v
    return None

def midas_info():
    j = json.load(open(os.path.join(ROOT, "notlar", "midas_kosullari.json")))
    det = j.get("sembol_detay", {}); sb = j.get("sembol_bazinda", {})
    return det, sb

MIDAS_DET, MIDAS_SB = midas_info()
PTP = {k for k, v in MIDAS_DET.items() if isinstance(v, dict) and v.get("ptp_k1")} | KR.PTP_EXTRA
TAR = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")
SON = pd.read_csv(os.path.join(ROOT, "sonuclar", "izleme_son.csv"))
SK = pd.read_csv(os.path.join(ROOT, "sonuclar", "son_kontrol.csv"))
KAD_TR = {"A": "A — denetimden geçmiş kural var", "B": "B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)", "C": "C — kural yok; sürücüleriyle takip"}

def sk_line(sid, sym, fallback=None):
    """Ana ajanın son kontrolü (Yahoo dağıtım düzeltmeli veri, ortak motor). Sepetlerde gün kümeli t de verilir."""
    v = SK[(SK["id"] == sid) & (SK["pos_usd"] == 2500) & ((SK["arac"] == sym) | SK["arac"].str.contains("sepet", na=False))]
    note = ""
    if v.empty and fallback:
        v = SK[(SK["id"] == sid) & (SK["pos_usd"] == 2500) & (SK["arac"] == fallback)]; note = f" [bu ETF için ayrı hesap yok; ana araç {fallback} rakamları]"
    if v.empty: return ""
    parts = []
    for m in ("C0", "O1", "C1"):
        r = v[v["mode"] == m]
        if len(r):
            r = r.iloc[0]
            tk = f", gün kümeli t {trnum(r['t_gun_kumeli'])}" if "sepet" in str(r["arac"]) and pd.notna(r.get("t_gun_kumeli")) else ""
            parts.append(f"{m}: net {trnum(r['mean_net_bp'],0)} bp (t {trnum(r['t'])}{tk}, n={int(r['n'])})")
    r1 = SK[(SK["id"] == sid) & (SK["pos_usd"] == 1000) & SK["ana_mod"] & ((SK["arac"] == sym) | SK["arac"].str.contains("sepet", na=False))]
    extra = f"; 1.000 $ pozisyonda ana mod net {trnum(r1.iloc[0]['mean_net_bp'],0)} bp (t {trnum(r1.iloc[0]['t'])})" if len(r1) else ""
    return "- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** " + " · ".join(parts) + extra + note

def midas_line(sym):
    d = MIDAS_DET.get(sym); s = MIDAS_SB.get(sym)
    txt = (d or {}).get("degerlendirme") or s or "doğrulanamadı (uygulamada sembolü arayarak kontrol edin)"
    if sym in PTP:
        txt += " · ⚠ PTP/K-1 yapısı: satışta %10 brüt kesinti (1446(f)) riski — uygulamada 'PTP' ibaresini ve kesintiyi teyit etmeden kısa vadeli işlem yapmayın"
    return txt

CUR_SYM = None

def patched(s):
    s = dict(s); pt = KR.STRAT_PATCH.get(s["id"], {})
    for k, v_ in pt.items():
        if k == "notlar_on": s["notlar"] = v_ + (s.get("notlar") or "")
        elif k == "ad_on": s["ad"] = v_ + s["ad"]
        else: s[k] = v_
    return s

def strat_block(s, v, code=None, role=None, fallback=None):
    s = patched(s)
    lines = []
    lab = {"dogrulandi": "Uygulanabilir (denetçi doğruladı)", "zayif": "İzlemede — zayıf kanıt", None: "Denetlenmedi"}[v["karar"] if v else None]
    if code == "F": lab = "Filtre — strateji değil"
    head = f"{code} — " if code else ""
    lines.append(f"#### {head}{s['ad']}  \n*{lab} · güven: {s.get('guven','—')} · aile kimliği: `{s['id']}`*" + (f"  \n*Bu ETF'nin rolü: {role}*" if role else "") + "\n")
    lines.append(f"- **Sinyal (t kapanışında):** {s['kural']}")
    lines.append(f"- **Giriş:** {s['giris']}")
    lines.append(f"- **Tutuş / çıkış:** {s['tutus']} — {s['cikis']}")
    lines.append(f"- **İşlem aracı:** {', '.join(s.get('islem_etf') or [])}" + (f" (sinyal: {s['sinyal_etf']})" if s.get("sinyal_etf") else ""))
    stats = (f"n={num(s.get('n'),'{:.0f}')}, net {num(s.get('net_bp'))} bp/işlem (brüt {num(s.get('brut_bp'))}), "
             f"kazanma %{num((s.get('kazanma') or 0)*100 if (s.get('kazanma') or 0) <= 1 else s.get('kazanma'),'{:.0f}')}, t={num(s.get('t'),'{:.2f}')}, "
             f"IS {num(s.get('is_net_bp'))} / OOS {num(s.get('oos_net_bp'))} bp, yılların %{num((s.get('yil_pozitif') or 0)*100 if (s.get('yil_pozitif') or 0) <= 1 else s.get('yil_pozitif'),'{:.0f}')}'i pozitif, "
             f"en kötü işlem {num(s.get('en_kotu_bp'),'{:.0f}')} bp")
    lines.append(f"- **Geçmiş (ajan):** {stats}")
    if v:
        if v.get("duzeltilmis_sayilar"): lines.append(f"- **Denetçi düzeltmesi:** {v['duzeltilmis_sayilar']}")
        if v.get("duzeltilmis_kural"): lines.append(f"- **Denetçi kural düzeltmesi:** {v['duzeltilmis_kural']}")
        lines.append(f"- **Denetim:** {v.get('yeniden_uretim','')} {('Sağlamlık: ' + v['saglamlik']) if v.get('saglamlik') else ''}".strip())
        if v.get("sorunlar"): lines.append(f"- **Denetçinin uyarıları:** {v['sorunlar']}")
    if s.get("mod_saglamlik"): lines.append(f"- **Giriş zamanı sağlamlığı:** {s['mod_saglamlik']}")
    if s.get("maliyet_duyarlilik"): lines.append(f"- **Maliyet duyarlılığı:** {s['maliyet_duyarlilik']}")
    if s.get("notlar"): lines.append(f"- **Not:** {s['notlar']}")
    lines.append(f"- Betik: `{s.get('betik','')}`")
    if CUR_SYM:
        sk = sk_line(s["id"], CUR_SYM, fallback)
        if sk: lines.insert(6, sk)
    return "\n".join(lines) + "\n"

def card(fam, sym, item, res, sv, ov, kademe="C", note=""):
    global CUR_SYM
    CUR_SYM = sym
    ll = next((x for x in res.get("leadlag", []) if x["sym"].upper() == sym), None)
    tr = TAR.loc[sym] if sym in TAR.index else None
    name = (tr["name"] if tr is not None and isinstance(tr["name"], str) else "")
    tv = TV_ETF.get(sym) or item.get("tv")
    L = [f"# {sym} — {name}", ""]
    L.append(f"**TradingView:** {tvfmt(tv)} · **Aile:** {FAM_TR.get(fam, fam)} · **İzleme kararı:** {item['karar']}  ")
    L.append(f"**Midas:** {midas_line(sym)}\n")
    if tr is not None:
        L.append("| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |")
        L.append("|---|---|---|---|---|---|")
        L.append(f"| {trnum(tr['med_dollar_vol_m'],0)} | {trnum(tr['cost_rt_bp'])} | {trnum(tr['vol_1d_bp'],0)} | %{trnum(tr['worst_1d_1y']*100)} | {trnum(tr['lev'],1)}x | {tr['first']} |\n")
    L.append(f"**Kademe:** {KAD_TR.get(kademe, kademe)}  ")
    L.append(f"**Neden izleme listesinde:** {KR.GEREKCE_PATCH.get(sym, item['gerekce'])}" + (f" **Ana ajan notu:** {note}" if note else "") + "\n")
    if sym in KR.UNDERLYING_CARD:
        u = KR.UNDERLYING_CARD[sym]
        L.append(f"*Dayanak / ana araç kartı: `kartlar/{u}.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*\n")
    # stratejiler
    byid = {s["id"]: s for s in res.get("stratejiler", [])}
    mine = []   # (strateji, kod, rol, yedek araç)
    for code, rule, role in KR.rules_for(sym):
        if rule["id"] in byid:
            main_tool = list(rule["araclar"])[0]
            mine.append((byid[rule["id"]], code, role, main_tool if main_tool != sym else None))
    seen = {m[0]["id"] for m in mine}
    for s_ in res.get("stratejiler", []):
        if s_["id"] in seen or sv.get(s_["id"], {}).get("karar") == "curutuldu": continue
        if sym in [x.split(" ")[0].upper() for x in (s_.get("islem_etf") or [])] or (s_.get("sinyal_etf") or "").upper() == sym:
            mine.append((s_, KR.ID2CODE.get(s_["id"]), None, None))
    ok = [m for m in mine if sv.get(m[0]["id"], {}).get("karar") == "dogrulandi" and m[1] != "F"]
    weak = [m for m in mine if sv.get(m[0]["id"], {}).get("karar") == "zayif" or m[1] == "F"]
    und = [m for m in mine if m[0]["id"] not in sv]
    L.append("## 1. Ne zaman girilir?\n")
    if ok:
        for s_, c_, r_, fb in ok: L.append(strat_block(s_, sv[s_["id"]], c_, r_, fb))
    else:
        L.append("Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.\n")
    if weak:
        L.append("### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)\n")
        for s_, c_, r_, fb in weak: L.append(strat_block(s_, sv.get(s_["id"]), c_, r_, fb))
    if und:
        L.append("### Denetlenmemiş adaylar\n")
        for s_, c_, r_, fb in und: L.append(strat_block(s_, None, c_, r_, fb))
    L.append("## 2. Lead-lag\n")
    if ll:
        L.append("### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)\n")
        if ll.get("suruculer"):
            L.append("| Sürücü | TradingView | corr (1y) | beta (1y) |\n|---|---|---|---|")
            for d in ll["suruculer"]:
                L.append(f"| {d['ad']} | {tvfmt(d.get('tv'))} | {num(d.get('corr_1y'),'{:.2f}')} | {num(d.get('beta_1y'),'{:.2f}')} |")
            L.append("")
        L.append("### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)\n")
        rows = []
        for o in ll.get("onculer", []):
            v = oncu_verdict(ov, sym, o)
            if v and v["karar"] == "curutuldu": continue
            lab = {"dogrulandi": "doğrulandı", "zayif": "zayıf"}.get(v["karar"]) if v else "denetlenmedi"
            rows.append(f"| {o['ad']} | {tvfmt(o.get('tv'))} | {o.get('tip','')} | {o.get('ufuk','')} | {o.get('etki','')} | {num(o.get('t'),'{:.1f}')} ({num(o.get('is_t'),'{:.1f}')}/{num(o.get('oos_t'),'{:.1f}')}) | {o.get('maliyet_sonrasi','—')} | {lab}{(' — ' + v['not']) if v and v.get('not') else ''} |")
        if rows:
            L.append("| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |\n|---|---|---|---|---|---|---|---|")
            L += rows; L.append("")
        else:
            L.append("Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.\n")
        if ll.get("gercek_zamanli"):
            L.append("### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)\n")
            L.append("| Gösterge | TradingView | Neden |\n|---|---|---|")
            for g in ll["gercek_zamanli"]:
                L.append(f"| {g['ad']} | {tvfmt(g.get('tv'))} | {g['neden']} |")
            L.append("")
        if ll.get("takvim_riskleri"): L.append(f"## 3. Takvim ve olay riskleri\n\n{ll['takvim_riskleri']}\n")
        if ll.get("not"): L.append(f"## 4. Notlar\n\n{ll['not']}\n")
    else:
        L.append("Aile ajanı bu ETF için lead-lag girdisi üretmedi.\n")
    L.append("---\n*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_%s.md`, `notlar/denetim_%s.md`.*\n" % (fam, fam))
    out = "\n".join(L)
    fm = KR.FAM_S.get(fam, {})
    if fm:
        out = re.sub(r"(?<![A-Za-z_0-9])S(\d)(?![0-9])", lambda m_: fm.get("S" + m_.group(1), m_.group(0)), out)
    for a, b in KR.TEXT_FIX: out = out.replace(a, b)
    # kod değişiminden sonra Türkçe ilgi eki uyumu (S1'in -> A2'nin vb.)
    GEN = {"A1": "'in", "A2": "'nin", "A2-3x": "'in", "B1": "'in", "B2": "'nin", "B3a": "'nın", "B3b": "'nin", "B4": "'ün", "B5": "'in", "B6": "'nın",
           "B7": "'nin", "B8": "'in", "B9": "'un", "B10": "'un"}
    out = re.sub(r"(?<![A-Za-z0-9_])(A2-3x|B3a|B3b|B10|A1|A2|B[1-9])'(?:in|nin|ün|ın|un|nın|nun|ün)(?![a-zçğıöşü])",
                 lambda m_: m_.group(1) + GEN.get(m_.group(1), "'in"), out)
    return out

def watch_txt(fam, res, sv):
    fin = SON[SON["aile"] == fam]
    acc = fin[fin["karar"] == "kabul"]["sym"].tolist()
    yed = fin[fin["karar"] == "yedek"]["sym"].tolist()
    def ok_tv(t):
        return [TV_OK[k] for k in re.findall(r"[A-Z_]+:[A-Z0-9!\.\-]+", (t or "").upper()) if k in TV_OK]
    etf = [TV_ETF[s] for s in acc + yed if s in TV_ETF]
    lead, rt = [], []
    for ll in res.get("leadlag", []):
        if ll["sym"].upper() not in acc + yed: continue
        for d in ll.get("suruculer", []) + ll.get("onculer", []): lead += ok_tv(d.get("tv"))
        for g in ll.get("gercek_zamanli", []): rt += ok_tv(g.get("tv"))
    uniq = lambda xs: list(dict.fromkeys(xs))
    lead = [x for x in uniq(lead) if x not in etf]; rt = [x for x in uniq(rt) if x not in etf and x not in lead]
    name = FAM_TR.get(fam, fam)
    parts = [f"###{name} ETF"] + uniq(etf) + [f"###{name} sürücüler (aynı gün)"] + lead + [f"###{name} gerçek zamanlı"] + rt
    return ",".join(parts), uniq(etf), lead, rt

COMBINED = []

def main():
    os.makedirs(os.path.join(ROOT, "kartlar"), exist_ok=True); os.makedirs(os.path.join(ROOT, "izleme_listeleri"), exist_ok=True)
    allparts = []; index = []
    for fam in ORDER:
        res, den = load_fam(fam)
        if not res: print("yok:", fam); continue
        sv, ov = verdict_maps(den)
        fin = SON[SON["aile"] == fam].set_index("sym")
        for item in res.get("izleme", []):
            sym = item["sym"].upper()
            if sym not in fin.index or fin.loc[sym, "karar"] not in ("kabul", "yedek"): continue
            item = dict(item); item["karar"] = fin.loc[sym, "karar"]
            note = fin.loc[sym, "not"] if isinstance(fin.loc[sym, "not"], str) else ""
            open(os.path.join(ROOT, "kartlar", f"{sym}.md"), "w").write(card(fam, sym, item, res, sv, ov, fin.loc[sym, "kademe"], note))
            nstr = sum(1 for s in res.get("stratejiler", []) if (sym in [x.upper() for x in (s.get("islem_etf") or [])] or (s.get("sinyal_etf") or "").upper() == sym) and sv.get(s["id"], {}).get("karar") == "dogrulandi")
            index.append((fam, sym, item["karar"], nstr, fin.loc[sym, "kademe"]))
        txt, etf, lead, rt = watch_txt(fam, res, sv)
        COMBINED.append((fam, etf, lead, rt))
        open(os.path.join(ROOT, "izleme_listeleri", f"{fam}.txt"), "w").write(txt + "\n")
        allparts.append(txt)
        print(fam, "kart:", sum(1 for i in index if i[0] == fam), "etf:", len(etf), "öncü:", len(lead), "gz:", len(rt))
    # birleşik dosya: önce tüm ailelerin ETF bölümleri, sonra ortak sürücü/öncü ve gerçek zamanlı bölümleri (tekrarsız)
    seen = set(); parts = []
    for fam_, etf_, lead_, rt_ in COMBINED:
        e2 = [x for x in etf_ if x not in seen]; seen.update(e2)
        if e2: parts += [f"###{FAM_TR[fam_]} ETF"] + e2
    L2 = [x for _, _, lead_, _ in COMBINED for x in lead_ if x not in seen]; L2 = list(dict.fromkeys(L2)); seen.update(L2)
    R2 = [x for _, _, _, rt_ in COMBINED for x in rt_ if x not in seen]; R2 = list(dict.fromkeys(R2))
    parts += ["###Ortak sürücüler (aynı gün)"] + L2 + ["###Gerçek zamanlı izleme (vadeli / kripto / döviz)"] + R2
    open(os.path.join(ROOT, "izleme_listeleri", "TUM_ETF_bolumlu.txt"), "w").write(",".join(parts) + "\n")
    pd.DataFrame(index, columns=["aile", "sym", "karar", "dogrulanmis_strateji", "kademe"]).to_csv(os.path.join(ROOT, "sonuclar", "kart_indeksi.csv"), index=False)
    open(os.path.join(ROOT, "sonuclar", "tv_eksik.txt"), "w").write("\n".join(sorted(MISSING)) + ("\n" if MISSING else ""))
    print("doğrulanmamış TV kodları:", len(MISSING))

if __name__ == "__main__":
    main()
