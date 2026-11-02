"""Repo paketini kurar: raporlar/2026-11-02_viop_leadlag/
Kullanım: python3 -I package.py <SCRATCH> <REPO_HEDEF_DİZİN>
"""
import os, sys, shutil, glob, json, re, html as H
S, D = sys.argv[1], sys.argv[2]
O = os.path.join(S, "out")
os.makedirs(D, exist_ok=True)

def html2md(h):
    h = re.sub(r"<h2>(.*?)</h2>", lambda m: "\n## " + m.group(1) + "\n", h)
    h = re.sub(r"<h3>(.*?)</h3>", lambda m: "\n### " + m.group(1) + "\n", h)
    h = re.sub(r"<li>(.*?)</li>", lambda m: "- " + m.group(1) + "\n", h, flags=re.S)
    h = re.sub(r"</?ul>", "\n", h)
    h = re.sub(r"<p[^>]*>(.*?)</p>", lambda m: m.group(1).strip() + "\n\n", h, flags=re.S)
    h = re.sub(r"</?b>", "**", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = H.unescape(h)
    return re.sub(r"\n{3,}", "\n\n", h).strip() + "\n"

G = json.load(open(os.path.join(S, "site", "genel.json")))
CONF = {"YUKSEK": "YÜKSEK", "ORTA": "ORTA", "DUSUK": "DÜŞÜK", "COK_DUSUK": "ÇOK DÜŞÜK"}
rap = ["# VİOP pay vadelisi olan 47 BIST hissesi: uluslararası ve yurt içi sürücüler, lead-lag ve backtest\n",
       f"\n_{G['meta']['asof']}_\n\n{G['meta']['lede']}\n\n> Bu çalışma yatırım tavsiyesi değildir. Kaldıraçlı türev ürünlerde sermayenin tamamı kaybedilebilir.\n",
       "\n## Dört hüküm\n\n" + "".join(f"- **{a}.** {b}\n" for a, b in G["meta"]["verdicts"]),
       "\n" + html2md(G["genel_html"]),
       "\n## İşlenebilir aday sinyaller (doğrulama sonrası)\n\n" + G["signals_note"] + "\n\n| Sinyal | Hedef | Sonuç | İstatistik | İşlem | TradingView |\n|---|---|---|---|---|---|\n" +
       "".join(f"| **{s['name']}** — {s['def']} | {s['target']} | {s['result']} | {CONF[s['stat']]} | {CONF[s['trade']]} | {s['tv']} |\n" for s in G["signals"]),
       "\n## Çin kaynaklı ticker'lar\n\n" + G["cin_note"] + "\n\nTam liste: `cin_alternatifleri.csv` ve etkileşimli sayfadaki 'Çin alternatifleri' sekmesi.\n",
       "\n" + html2md(G["yontem_html"]),
       "\n## Dosyalar\n\n- `HISSE_KARTLARI.md`: 47 hissenin özet kartları; ayrıntılar `hisse_kartlari/<KOD>.md` ve `.json`.\n- `izleme_listeleri/`: TradingView izleme listeleri (her hisse için `<KOD>.txt`; tümü bölümlü `TUM_HISSELER_bolumlu.txt`, TradingView 'Listeyi içe aktar' biçimi).\n- `viop_surucu_haritasi.html`: etkileşimli sayfa (tek dosya; tarayıcıda açılır).\n- `tradingview_kodlari.csv`: doğrulanmış Yahoo → TradingView eşlemesi.\n- `bulgular_tum_ajanlar.csv`: 22 analiz ajanının ~12.500 bulgu satırı (agent sütunu; ham, doğrulama öncesi etiketler; conf_norm sadeleştirilmiş etiket).\n- `dogrulama/`: bağımsız yeniden üretim ve çürütme notları, `hukumler.json`.\n- `ajanlar/`: ajan brifingleri ve raporları.\n- `veri_ozet/`: VİOP likidite tablosu, varyans ayrıştırması, ortaklık tablosu, olay tarihleri, Çin alternatifleri.\n- `hesaplar/`: ortak kütüphane ve ajan kodları (veri dosyaları hariç; veriler Yahoo, İş Yatırım, Borsa İstanbul, EPİAŞ ve Sina'dan yeniden indirilebilir).\n"]
open(os.path.join(D, "RAPOR.md"), "w").write("".join(rap))

# site çıktıları
SO = os.path.join(S, "site", "out_final")
for name in ["HISSE_KARTLARI.md"]:
    shutil.copy(os.path.join(SO, name), D)
shutil.copytree(os.path.join(SO, "izleme_listeleri"), os.path.join(D, "izleme_listeleri"), dirs_exist_ok=True)
shutil.copy(os.path.join(S, "site", "viop_surucu_haritasi.html"), D)
os.makedirs(os.path.join(D, "hisse_kartlari"), exist_ok=True)
for f in glob.glob(os.path.join(O, "kartlar", "*")): shutil.copy(f, os.path.join(D, "hisse_kartlari"))
shutil.copy(os.path.join(O, "tv_final.csv"), os.path.join(D, "tradingview_kodlari.csv"))
shutil.copy(os.path.join(O, "master_findings_r1.csv"), os.path.join(D, "bulgular_tum_ajanlar.csv"))
os.makedirs(os.path.join(D, "dogrulama"), exist_ok=True)
for f in glob.glob(os.path.join(O, "v_*.md")) + glob.glob(os.path.join(O, "v_*.csv")) + [os.path.join(O, "v_wf4_ozet.txt")]:
    shutil.copy(f, os.path.join(D, "dogrulama"))
shutil.copy(os.path.join(O, "v_verdicts_all.json"), os.path.join(D, "dogrulama", "hukumler.json"))
os.makedirs(os.path.join(D, "ajanlar"), exist_ok=True)
for f in glob.glob(os.path.join(O, "r1_*.md")) + glob.glob(os.path.join(O, "ry_*.md")) + [os.path.join(O, x) for x in ["BRIEF.md", "BRIEF_YURTICI.md", "KART_BRIEF.md"]]:
    shutil.copy(f, os.path.join(D, "ajanlar"))
os.makedirs(os.path.join(D, "veri_ozet"), exist_ok=True)
for x in ["y_viop_likidite.csv", "y_varyans_ayristirma.csv", "y_ortaklik.csv", "olay_tarihleri.csv", "cin_alternatifler.csv"]:
    p = os.path.join(O, x)
    if os.path.exists(p): shutil.copy(p, os.path.join(D, "veri_ozet"))
shutil.copy(os.path.join(O, "cin_alternatifler.csv"), os.path.join(D, "cin_alternatifleri.csv"))
# kod: yalnız .py/.sh/.md, 1 MB altı
H_D = os.path.join(D, "hesaplar"); os.makedirs(H_D, exist_ok=True)
for f in ["ll.py", "ydl.py", "universe.py", "build_panel.py", "bulk.py", "viop_list.py"]:
    p = os.path.join(S, "code", f)
    if os.path.exists(p): shutil.copy(p, os.path.join(H_D, f))
n = 0
for d in sorted(glob.glob(os.path.join(O, "code_*"))):
    for root, _, files in os.walk(d):
        if "cache" in root or "__pycache__" in root: continue
        for fn in files:
            if not fn.endswith((".py", ".sh")): continue
            p = os.path.join(root, fn)
            if os.path.getsize(p) > 1_000_000: continue
            rel = os.path.relpath(p, O); dst = os.path.join(H_D, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(p, dst); n += 1
for f in ["template.html", "build_site.py", "make_genel.py", "package.py", "dom_signals.json"]:
    shutil.copy(os.path.join(S, "site", f), os.path.join(H_D, "site_" + f))
tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(D) for f in fs)
print("kod dosyası", n, "toplam MB", round(tot / 1e6, 1))
