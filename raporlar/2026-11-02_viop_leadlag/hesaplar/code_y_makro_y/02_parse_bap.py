"""BAP kesin alım-satım bülteni (ttb*.zip) -> res/bap_bonds.parquet (ISIN bazında günlük kapanış/ağ.ort. bileşik getiri, VKG, hacim).
Sadece TL Hazine (Devlet tahvili / Hazine bonosu) ISIN'leri: ^TR[TBD]\\d{6}T\\d{2}$ . Çalıştırma: python3 -I 02_parse_bap.py"""
import os, sys, re, glob, io, zipfile, csv
import pandas as pd, numpy as np
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
OUT = S + "/out/code_y_makro_y/res/bap_bonds.parquet"
GOV = re.compile(r"^TR[TBD]\d{6}T\d{2}$")
def fnum(x):
    try:
        return float(str(x).replace(",", "")) if str(x).strip() not in ("", "-") else np.nan
    except Exception: return np.nan
def parse_csv(raw, date):
    txt = raw.decode("windows-1254", errors="replace").splitlines()
    rd = csv.reader(txt, delimiter=";"); hdr = [h.strip() for h in next(rd)]; next(rd); ix = {h: i for i, h in enumerate(hdr)}
    out = []
    for r in rd:
        if len(r) < 10 or "KES NORMAL" not in r[ix["PAZAR ISMI"]]: continue
        isin = r[ix["ISIN/KOD"]].strip()
        if not GOV.match(isin): continue
        code = r[ix["ISLEM KODU"]]
        same = 1 if code.endswith("_T0") else 0
        g = lambda k: fnum(r[ix[k]]) if k in ix and ix[k] < len(r) else np.nan
        out.append(dict(date=date, isin=isin, same=same, dtm=g("VKG/REPO SURESI"), yc=g("KAPANIS BILESIK GETIRI"), ya=g("AG. ORT. BILESIK GETIRI"),
                        ys=g("KAPANIS FIYAT/GETIRI"), px=g("KAPANIS"), vol=g("ISLEM HACMI")))
    return out
def parse_xls(raw, date):
    import xlrd
    b = xlrd.open_workbook(file_contents=raw)
    # 2018 sonrası bazı bültenlerde ilk sayfa 'PARA PIYASASI'; kesin alım-satım sayfasını adından seç
    cand = [x for x in b.sheets() if ("KAS" in x.name.upper() or "KES" in x.name.upper())]
    sh = cand[0] if cand else b.sheet_by_index(0)
    # başlık satırlarını bul
    hrow = None
    for i in range(min(15, sh.nrows)):
        if str(sh.cell_value(i, 0)).strip().upper().startswith("MENKUL"): hrow = i; break
    if hrow is None: return []
    top = [str(sh.cell_value(hrow - 1, j)) for j in range(sh.ncols)]
    h1 = [str(sh.cell_value(hrow, j)) for j in range(sh.ncols)]; h2 = [str(sh.cell_value(hrow + 1, j)) for j in range(sh.ncols)]
    jb = next((j for j, v in enumerate(top) if "BİLEŞİK" in v.upper() or "BILESIK" in v.upper()), None)
    jvol = next((j for j in range(sh.ncols) if "HACM" in h2[j].upper() and "İŞLEM" in h1[j].upper()), None)
    jval = next((j for j in range(sh.ncols) if "VAL" in h1[j].upper()), 2)
    jvkg = next((j for j in range(sh.ncols) if h1[j].strip().upper() == "VKG"), 3)
    jpx = next((j for j in range(sh.ncols) if h1[j].strip().upper().startswith("KAPANI")), 9)
    jbs = next((j for j, v in enumerate(top) if "BAS" in v.upper() and "GET" in v.upper()), None)
    if jb is None: return []
    out = []; dnum = (pd.Timestamp(date) - pd.Timestamp("1899-12-30")).days
    for i in range(hrow + 2, sh.nrows):
        isin = str(sh.cell_value(i, 0)).strip()
        if not GOV.match(isin): continue
        if str(sh.cell_value(i, 1)).strip() not in ("TLR", "TRY", "TL"): continue
        val = fnum(sh.cell_value(i, jval))
        out.append(dict(date=date, isin=isin, same=1 if val == dnum else 0, dtm=fnum(sh.cell_value(i, jvkg)), yc=fnum(sh.cell_value(i, jb)), ya=fnum(sh.cell_value(i, jb + 1)),
                        ys=fnum(sh.cell_value(i, jbs + 3)) if jbs is not None else np.nan, px=fnum(sh.cell_value(i, jpx)), vol=fnum(sh.cell_value(i, jvol)) if jvol is not None else np.nan))
    return out
def main():
    old = pd.read_parquet(OUT) if os.path.exists(OUT) else None
    if old is not None:  # boş ayrıştırılmış dosyaları yeniden dene
        empty = set(old.groupby("file")["isin"].apply(lambda x: (x != "").sum() == 0).loc[lambda z: z].index)
        old = old[~old["file"].isin(empty)]
    done = set(old["file"].unique()) if old is not None else set()
    rows = []; bad = 0
    for fn in sorted(glob.glob(S + "/data/bap/ttb*.zip")):
        b = os.path.basename(fn)
        if b in done: continue
        ds = b[3:11]; date = pd.Timestamp(ds)
        try:
            z = zipfile.ZipFile(fn); nm = z.namelist()[0]; raw = z.read(nm)
            rr = parse_csv(raw, date) if nm.lower().endswith(".csv") else parse_xls(raw, date)
            for r in rr: r["file"] = b
            rows += rr
            if not rr: rows.append(dict(date=date, isin="", file=b))
        except Exception as e:
            bad += 1; print("ERR", b, e)
    new = pd.DataFrame(rows)
    df = pd.concat([old, new]) if old is not None else new
    df.to_parquet(OUT); print(df.shape, df["date"].min(), df["date"].max(), df["file"].nunique(), "bad", bad)
if __name__ == "__main__": main()
