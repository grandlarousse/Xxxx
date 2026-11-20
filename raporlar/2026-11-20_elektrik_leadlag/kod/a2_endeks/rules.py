"""rules.py — A2 (endeks <-> hisse) ailesinin DONDURULMUŞ kuralları (YONTEM_EK E1 sözleşmesi).
Eşikler IS'te (<= 2022-12-30) seçildi ve sayı olarak yazıldı; P'den hiçbir şey yeniden kestirilmez.
Bütün girdiler yalnız t kapanışına kadarki bilgiyle kurulur (a2lib.context: rolling + shift).
Hisse listesi koda gömülü değildir: hedef evreni elib.sector_cols(P), komşular elib.KOMSU, VİOP'lular elib.VIOP."""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_HERE, '..', 'ortak'), _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import a2lib
from a2lib import elib


def build(P):
    C = a2lib.context(P)
    x1_all = a2lib.make_sig(C, 'XELKT', 1.0, 'all')       # XELKT(t) / std60(t-1) >= 1; hedef: bütün sektör hisseleri
    x1_lag = a2lib.make_sig(C, 'XELKT', 1.0, 'lag')       # aynı gün, yalnız "geciken" hisseler
    m1_all = a2lib.make_sig(C, 'XU100', 1.0, 'all')
    spec2 = a2lib.make_sig(C, 'SPEC', 2.0, 'all')
    kom15 = a2lib.make_sig(C, 'KOMSU', 1.5, 'all')
    viop = [c for c in elib.VIOP if c in C['sc']]
    ew_dn = a2lib.make_sig(C, 'EWx', -1.5, 'lag')[viop]
    rules = [
        {"ad": "A2_xelkt_z1_tum_h3", "sig": x1_all, "h": 3, "yon": "long", "olcu": "own", "arac": "spot", "birincil": True,
         "aciklama": "XELKT günlük getirisi / 60 günlük gecikmeli std >= 1 ise o gün dolabilir bütün XELKT hisseleri AL, 3 gün tut"},
        {"ad": "A2_xelkt_z1_geciken_h3", "sig": x1_lag, "h": 3, "yon": "long", "olcu": "own", "arac": "spot", "birincil": False,
         "aciklama": "XELKT z >= 1 günü, |r_i| < 0,5*|XELKT| ya da ters işaretli (geciken) hisseler AL, 3 gün tut"},
        {"ad": "A2_spec_z2_tum_h3", "sig": spec2, "h": 3, "yon": "long", "olcu": "own", "arac": "spot", "birincil": False,
         "aciklama": "SPEC = XELKT - beta250*XU030; z >= 2 ise dolabilir bütün XELKT hisseleri AL, 3 gün tut"},
        {"ad": "A2_xelkt_z1_xu100alt_tum_h3", "sig": x1_all & ~m1_all, "h": 3, "yon": "long", "olcu": "own", "arac": "spot",
         "birincil": False,
         "aciklama": "KEŞİF (ızgara dışı): XELKT z >= 1 ve XU100 z < 1 (sektöre özgü yükseliş) ise bütün XELKT hisseleri AL, 3 gün tut"},
        {"ad": "A2_komsu_z15_tum_h2", "sig": kom15, "h": 2, "yon": "long", "olcu": "own", "arac": "spot", "birincil": False,
         "aciklama": "KOMSU (ASTOR, ALARK, EUPWR, GESAN eşit ağırlıklı) z >= 1,5 ise dolabilir bütün XELKT hisseleri AL, 2 gün tut"},
        {"ad": "A2_ewx_zm15_geciken_viop_sat_h1", "sig": ew_dn, "h": 1, "yon": "short", "olcu": "own", "arac": "viop",
         "birincil": False,
         "aciklama": "KEŞİF (ızgara dışı): hisse hariç EW sektör sepeti z <= -1,5 ve AKSEN/ENJSA/ODAS o gün gecikmiş (düşmemiş) ise vadelide SAT, 1 gün"},
    ]
    if 'AKSEN' in C['sc']:
        rules.insert(5, {"ad": "A2_komsu_z2_aksen_h1", "sig": a2lib.make_sig(C, 'KOMSU', 2.0, 'AKSEN'), "h": 1, "yon": "long",
                         "olcu": "own", "arac": "spot", "birincil": False,
                         "aciklama": "KOMSU sepeti z >= 2 ise AKSEN AL (spot), 1 gün tut"})
    return rules
