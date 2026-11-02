"""Hisse kartları + genel içerikten tek dosyalık HTML sayfa, izleme listeleri ve kart özetini üretir.
Kullanım: python3 -I build_site.py <SCRATCH> <ÇIKTI_DİZİNİ>
"""
import json, os, sys, glob, re
import pandas as pd

S, OUT = sys.argv[1], sys.argv[2]
SITE = os.path.join(S, "site")
os.makedirs(OUT, exist_ok=True)
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
SECTORS = [
    ["Bankalar", ["AKBNK","GARAN","YKBNK","ISCTR","HALKB","VAKBN","TSKB"]],
    ["Holding · inşaat · GYO", ["KCHOL","SAHOL","DOHOL","ALARK","ENKAI","TKFEN","EKGYO"]],
    ["Havacılık · turizm", ["THYAO","PGSUS","TAVHL"]],
    ["Savunma · telekom", ["ASELS","TCELL","TTKOM"]],
    ["Enerji · rafineri · kimya", ["TUPRS","PETKM","SASA","AKSEN","ENJSA","ODAS"]],
    ["Metal · madencilik", ["EREGL","KRDMD","TRALT","TRMET","BRSAN"]],
    ["Gübre · çimento · cam", ["GUBRF","HEKTS","SISE","CIMSA","OYAKC"]],
    ["Otomotiv · dayanıklı · ekipman", ["FROTO","TOASO","DOAS","ARCLK","VESTL","ASTOR"]],
    ["Perakende · gıda · içecek", ["BIMAS","MGROS","SOKM","ULKER","AEFES"]],
]
CONFS = {"YUKSEK", "ORTA", "DUSUK", "COK_DUSUK"}
CHINA_PREFIX = re.compile(r"\b(SSE|SZSE|SHFE|DCE|ZCE|CFFEX|INE|GFEX):[A-Z0-9!]+")

def norm_conf(c):
    c = str(c or "").upper().replace("Ü", "U").replace("Ş", "S").replace("Ç", "C").strip()
    lead = re.split(r"[\s(/,;]", c)[0] if c else ""
    for k in ["COK_DUSUK", "COK", "YUKSEK", "ORTA", "DUSUK"]:
        if lead.startswith(k): return "COK_DUSUK" if k.startswith("COK") else k
    if "COK" in c: return "COK_DUSUK"
    if "YUKSEK" in c: return "YUKSEK"
    if re.search(r"\bORTA\b", c): return "ORTA"
    return "DUSUK" if "DUSUK" in c else "COK_DUSUK"

# ---- varyans payları
V = pd.read_csv(os.path.join(S, "out", "y_varyans_ayristirma.csv"))
V = V[V["spec"] == "base"]
def vshare(stock, period):
    r = V[(V["stock"] == stock) & (V["period"] == period)]
    if r.empty: return None
    r = r.iloc[0]
    sh = {"global": r["sh_global"], "trmakro": r["sh_trmakro"], "piyasa": r["sh_piyasa"], "sektor": r["sh_sektor"]}
    sh = {k: max(0.0, float(v)) for k, v in sh.items()}
    tot = sum(sh.values()); idio = max(0.0, 1.0 - tot)
    sh["idio"] = idio
    return {k: round(v, 4) for k, v in sh.items()}

# ---- kartlar
cards, problems = [], []
for s in VIOP:
    p = os.path.join(S, "out", "kartlar", f"{s}.json")
    if not os.path.exists(p):
        problems.append(f"{s}: kart yok"); continue
    c = json.load(open(p))
    if isinstance(c, list): c = c[0]
    c["stock"] = s
    for d in c.get("drivers", []):
        d["confidence"] = norm_conf(d.get("confidence"))
        for k in ["tv", "tv_alt"]:
            if d.get(k) and CHINA_PREFIX.search(str(d[k])):
                problems.append(f"{s}: Çin kodu {d[k]} -> kaldırıldı"); d[k] = CHINA_PREFIX.sub("(Çin kodu — açılmıyor)", str(d[k]))
    wl = str(c.get("watchlist", ""))
    if CHINA_PREFIX.search(wl):
        problems.append(f"{s}: izleme listesinde Çin kodu temizlendi")
        wl = ",".join(x for x in re.split(r"\s*,\s*", wl) if x and not CHINA_PREFIX.search(x))
    # izleme listesi: tekrarları at, sırayı koru
    seen, items = set(), []
    for x in re.split(r"\s*,\s*", wl):
        x = x.strip()
        if x.startswith(("HKEX:", "HSI:")): continue  # HKEX kullanıcıda açılmayabilir; izleme listesine konmaz (tabloda notuyla durur)
        if x and x not in seen and ":" in x and " " not in x: seen.add(x); items.append(x)
    c["watchlist"] = ",".join(items)
    c["var_full"] = vshare(s, "tam"); c["var_recent"] = vshare(s, "2024-26")
    cards.append(c)

# ---- genel içerik
G = json.load(open(os.path.join(SITE, "genel.json")))

# ---- Çin alternatifleri
C = pd.read_csv(os.path.join(S, "out", "cin_alternatifler.csv"))
def f2(x):
    try: return f"{float(x):.2f}".replace(".", ",")
    except Exception: return "—"
cin = []
for _, r in C.iterrows():
    alt = str(r.get("alternatif_tv") or "")
    if CHINA_PREFIX.search(alt): continue
    cin.append({"o": str(r.get("orijinal") or ""), "od": str(r.get("orijinal_desc") or ""), "a": alt, "ad": str(r.get("alternatif_desc") or ""),
                "w": f2(r.get("corr_weekly")), "d": f2(r.get("corr_sync")), "n": str(r.get("not") or "")[:300], "g": norm_conf(r.get("guven"))})
cin.sort(key=lambda r: ({"YUKSEK": 0, "ORTA": 1, "DUSUK": 2, "COK_DUSUK": 3}[r["g"]], r["o"]))

# ---- TradingView kodları
T = pd.read_csv(os.path.join(S, "out", "tv_final.csv")).fillna("")
tv = [[str(r["yahoo"]), str(r["aciklama"])[:120], str(r["tv_kodu"]), str(r["tv_alternatif"]), str(r["durum"]), str(r["not"])[:200]] for _, r in T.iterrows()]

DATA = {"meta": G["meta"], "sectors": SECTORS, "cards": cards, "default_stock": "THYAO", "genel": G["genel_html"], "yontem": G["yontem_html"],
        "signals": G["signals"], "signals_note": G["signals_note"], "cin": cin, "cin_note": G["cin_note"], "tv": tv, "tv_note": G["tv_note"]}
tpl = open(os.path.join(SITE, "template.html")).read()
html = tpl.replace("/*__DATA__*/null", json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/"))
open(os.path.join(SITE, "viop_surucu_haritasi.html"), "w").write(html)

# ---- izleme listeleri (TradingView 'Listeyi içe aktar' biçimi)
WL = os.path.join(OUT, "izleme_listeleri"); os.makedirs(WL, exist_ok=True)
allsec = []
for c in cards:
    open(os.path.join(WL, f"{c['stock']}.txt"), "w").write(c["watchlist"] + "\n")
    allsec.append(f"###{c['stock']}," + c["watchlist"])
open(os.path.join(WL, "TUM_HISSELER_bolumlu.txt"), "w").write(",".join(allsec) + "\n")

# ---- kart özeti markdown
md = ["# Hisse kartları — 47 VİOP pay vadelisi dayanağı\n", "Her kartın ayrıntılı tablosu `hisse_kartlari/<KOD>.md` ve `.json` dosyalarında. Güven etiketleri doğrulama turundan sonraki hâlidir.\n"]
for sec, ks in SECTORS:
    md.append(f"\n## {sec}\n")
    for k in ks:
        c = next((x for x in cards if x["stock"] == k), None)
        if not c: md.append(f"- **{k}**: kart yok\n"); continue
        top = [d for d in c["drivers"] if d["confidence"] in ("YUKSEK", "ORTA")][:6]
        md.append(f"\n### {k} — {c.get('name','')}\n\n{c.get('summary','')}\n\n- Spot: `{c.get('tv_spot','')}` · VİOP: `{c.get('tv_viop','')}`\n- VİOP: {c.get('viop_liquidity','')}\n")
        if top:
            md.append("\n| Sürücü | TradingView | İlişki | Ölçüm | İşlenebilir | Güven |\n|---|---|---|---|---|---|\n")
            for d in top:
                md.append(f"| {d['driver']} | `{d.get('tv','')}` | {d.get('relation','')} | {str(d.get('metric','')).replace('|','/')} | {d.get('tradable','')} | {d['confidence']} |\n")
        md.append(f"\nİzleme listesi: `{c['watchlist']}`\n")
open(os.path.join(OUT, "HISSE_KARTLARI.md"), "w").write("".join(md))
print("kart", len(cards), "sorun", problems[:20], "html KB", round(len(html) / 1024))
