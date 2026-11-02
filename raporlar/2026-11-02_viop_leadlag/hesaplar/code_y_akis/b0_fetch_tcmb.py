"""TCMB haftalık yabancı hisse akışı ve stoku (EVDS3 halka açık web arayüzü veri uç noktası; anahtar gerekmez) -> data/akis/tcmb_foreign_equity_weekly.csv
Seriler: TP.PYUK3/TP.PYUK1 (arşiv 2005-2021), TP.MKNETHAR.M7/M1 (2020-09+), TP.PYUK4/TP.MKNETHAR.M8 (DİBS). groupSeperator=False ŞART (yoksa '31,569.27')."""
import requests, pandas as pd, alib, os
body = {"type": "json", "series": "TP.PYUK3-TP.PYUK1-TP.MKNETHAR.M7-TP.MKNETHAR.M1-TP.PYUK4-TP.MKNETHAR.M8", "aggregationTypes": "last-last-last-last-last-last",
        "formulas": "0-0-0-0-0-0", "startDate": "01-01-2005", "endDate": pd.Timestamp.today().strftime('%d-%m-%Y'), "frequency": "3", "decimalSeperator": ".", "decimal": "4",
        "dateFormat": "0", "lang": "tr", "yon": "1", "sira": "1", "ozelFormuller": [], "groupSeperator": False, "isRaporSayfasi": False}
r = requests.post("https://evds3.tcmb.gov.tr/igmevdsms-dis/fe", json=body, timeout=60); r.raise_for_status()
d = pd.DataFrame(r.json()['items']); d['date'] = pd.to_datetime(d['Tarih'], format='%d-%m-%Y'); d = d.set_index('date')
cols = [c for c in d if c.startswith('TP_')]
for c in cols: d[c] = pd.to_numeric(d[c].astype(str).str.replace(',', ''), errors='coerce')
out = pd.DataFrame({'flow_eq_musd': d['TP_MKNETHAR_M7'].combine_first(d['TP_PYUK3']), 'stock_eq_musd': d['TP_MKNETHAR_M1'].combine_first(d['TP_PYUK1']),
                    'flow_gdds_musd': d['TP_MKNETHAR_M8'].combine_first(d['TP_PYUK4'])}).dropna(how='all')
os.makedirs(alib.SCR + '/data/akis', exist_ok=True); out.to_csv(alib.SCR + '/data/akis/tcmb_foreign_equity_weekly.csv'); print(out.tail(), len(out))
