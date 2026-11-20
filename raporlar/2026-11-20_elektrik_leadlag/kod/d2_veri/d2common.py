"""D2 ortak sabitler (VİOP bülteni + gün içi veri). Betikler veri klasörünün DIŞINDA durur; python3 -I ile çalıştırılır."""
import os
S = "/tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el"
DATA = S + "/data"
RAW = DATA + "/raw/d2"            # ham/ara dosyalar (2. dalga ajanları bakmaz)
FULL = DATA + "/panel_full"
DEV = DATA + "/panel_dev"
CUT = "2025-06-30"               # panel_dev son günü (dahil)
START, END = "2017-03-01", "2026-11-19"   # VİOP bülten aralığı
XELKT = ("A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN CONSE CWENE CANTE CATES ARASE ECOGR "
         "ENDAE ENJSA ENERY ESEN GWIND HUNER ENTRA IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ NATEN ODAS PAMEL SMRTG "
         "TATEN VEYAS ZEDUR ZOREN").split()
NEIGH = "ASTOR ALARK EUPWR GESAN".split()
STOCKS = XELKT + NEIGH
YIDX = ["XU030", "XU100"]        # Yahoo gün içi endeksler
ISY_IDX = ["XELKT", "XU030", "XU100"]
VIOP_UND = ["AKSEN", "ENJSA", "ODAS", "ASTOR", "ALARK"]
UA = "Mozilla/5.0"
for d in (RAW, FULL, DEV): os.makedirs(d, exist_ok=True)
