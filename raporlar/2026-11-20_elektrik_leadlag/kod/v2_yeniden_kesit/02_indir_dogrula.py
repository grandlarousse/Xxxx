"""V2: en az 6 hisseyi Is Yatirim'dan (HisseTekil) yeniden indir, ham dosyalarla ve ondan kurulan getirilerle karsilastir.
Kullanim: python3 -I 02_indir_dogrula.py <RAW_D1> <YENI_DIR> [KOD ...]"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402

RAW, NEW = sys.argv[1], sys.argv[2]
SYMS = sys.argv[3:] or ['AKSEN', 'ENJSA', 'ODAS', 'BIGEN', 'LYDYE', 'MAGEN', 'ZOREN', 'AYEN']
URL = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil'
os.makedirs(os.path.join(NEW, 'isy_hisse'), exist_ok=True)
rows = []
for s in SYMS:
    out = os.path.join(NEW, 'isy_hisse', s + '.json')
    if not os.path.exists(out):
        q = urllib.parse.urlencode({'hisse': s, 'startdate': '01-01-2000', 'enddate': '20-11-2026'})
        txt = None
        for a in range(4):
            try:
                req = urllib.request.Request(URL + '?' + q, headers={'User-Agent': 'Mozilla/5.0'})
                txt = urllib.request.urlopen(req, timeout=90).read().decode('utf-8')
                if len(json.loads(txt)['value']) > 0:
                    break
            except Exception as e:  # noqa: BLE001
                err = repr(e)[:200]
                txt = None
                time.sleep(1.5 * (a + 1))
        if txt is None:
            rows.append(dict(sym=s, durum='INDIRILEMEDI: ' + err))
            continue
        open(out, 'w').write(txt)
    a = L.read_stock(RAW, s)
    b = L.read_stock(NEW, s)
    a = a[a.index >= L.START]
    b = b[(b.index >= L.START) & (b.index <= a.index.max())]
    idx = a.index.intersection(b.index)
    d = (a.loc[idx] - b.loc[idx]).abs()
    ra = (a.c / L.adj_factor(a)).pct_change()
    rb = (b.c / L.adj_factor(b)).pct_change()
    rows.append(dict(sym=s, durum='ok', n_eski=len(a), n_yeni=len(b), ortak=len(idx), ham_kapanis_maks_fark=float(d.c.max()),
                     yuksek_dusuk_maks_fark=float(max(d.h.max(), d.l.max())), hacim_maks_goreli_fark=float((d.v / a.loc[idx].v.replace(0, np.nan)).max()),
                     duz_kapanis_maks_goreli_fark=float((d.ca / a.loc[idx].ca).max()),
                     duz_getiri_maks_fark_bps=float(1e4 * (ra.loc[idx] - rb.loc[idx]).abs().max())))
r = pd.DataFrame(rows)
pd.set_option('display.width', 250)
print(r.to_string(index=False))
r.to_csv(os.path.join(NEW, 'yeniden_indirme_karsilastirma.csv'), index=False)
