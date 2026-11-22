"""Panel yukleyici.
    import sys; sys.path.insert(0, "/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod")
    from yukle import panel
    P = panel()   # {'open','high','low','close','adjclose','adjopen','volume': DataFrame (tarih x kod), 'evren': DataFrame}
Satirlar = NYSE islem gunleri (SPY veri gunleri) 2005-01-03..2026-11-20. Ileri doldurma YOK.
close/open/high/low: bolunmeye gore duzeltilmis, temettuye gore duzeltilmemis (Yahoo). adjclose: ikisine gore.
adjopen = open * adjclose / close (temettu+bolunme duzeltilmis acilis).
"""
import os
import pandas as pd

KOD = os.path.dirname(os.path.abspath(__file__))
VERI = os.path.join(os.path.dirname(KOD), "veri")
PANEL = os.environ.get("PANEL_DIZIN",
                       "/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/panel")
ALAN = ["open", "high", "low", "close", "adjclose", "volume"]
_onbellek = {}


def panel(dizin=None):
    dizin = dizin or PANEL
    if dizin in _onbellek:
        return {k: v.copy() for k, v in _onbellek[dizin].items()}
    P = {a: pd.read_pickle(os.path.join(dizin, f"{a}.pkl")) for a in ALAN}
    P["adjopen"] = P["open"] * P["adjclose"] / P["close"]
    P["evren"] = pd.read_csv(os.path.join(VERI, "evren.csv"), dtype={"kod": str})
    _onbellek[dizin] = P
    return {k: v.copy() for k, v in P.items()}


def bilanco():
    """8-K 2.02 bilanco tarihleri (ilk_tepki_gunu = getirinin ilk etkilenen islem gunu)."""
    return pd.read_csv(os.path.join(VERI, "bilanco_tarihleri.csv"),
                       parse_dates=["filing_date", "ilk_tepki_gunu"])


def dix_gex():
    return pd.read_csv(os.path.join(VERI, "dix_gex.csv"), parse_dates=["date"], index_col="date")


def kalite():
    return pd.read_csv(os.path.join(VERI, "veri_kalite.csv"))


# ---- D2 ek veri (saatlik, kripto 16:00, temettu, olay takvimleri) ----
def saatlik(dizin=None):
    """Yahoo 60m'den (son 730 gun, 376 likit ABD16 ETF/hisse). Doner: dict
    'acilis_1530': son tam saatlik cubugun acilisi (normal gun 15:30 ET, yarim gun 12:30 ET), tarih x kod
    'kapanis'    : ayni gunun son cubugunun kapanisi (son islem; resmi kapanis acik artirmasindan birkac bps farkli olabilir)
    'yarim_gun'  : tarih -> bool (13:00 kapanisli gunler).
    Fiyatlar bolunmeye gore duzeltilmis, temettuye gore duzeltilmemis (gunluk 'close' ile ayni olcek)."""
    dizin = dizin or PANEL
    return {"acilis_1530": pd.read_pickle(os.path.join(dizin, "saatlik_1530.pkl")),
            "kapanis": pd.read_pickle(os.path.join(dizin, "saatlik_kapanis.pkl")),
            "yarim_gun": pd.read_pickle(os.path.join(dizin, "saatlik_yarim_gun.pkl"))}


def kripto_1600(dizin=None, ayrinti=False):
    """BTC-USD (2015-01-02~), ETH-USD (2016-05-19~), SOL-USD (2021-06-18~): her NYSE gununde 16:00 ET fiyati
    (15:00-16:00 ET saatlik mumunun kapanisi; Coinbase, BTC 2015-07-22 oncesi Bitstamp). Index = panel gunleri.
    ayrinti=True: (fiyat, kaynak, yedek_mum) -> yedek_mum True ise tam mum yoktu, 3 saat icindeki son mum kullanildi."""
    dizin = dizin or PANEL
    F = pd.read_pickle(os.path.join(dizin, "kripto_1600.pkl"))
    if not ayrinti:
        return F
    return F, pd.read_pickle(os.path.join(dizin, "kripto_1600_kaynak.pkl")), pd.read_pickle(os.path.join(dizin, "kripto_1600_yedek.pkl"))


def temettu(dizin=None):
    """tarih (ex-date, borsa yerel gunu) x kod: hisse basina nakit temettu (Yahoo events.dividends; bolunmeye gore duzeltilmis). Index = panel gunleri."""
    return pd.read_pickle(os.path.join(dizin or PANEL, "temettu.pkl"))


def kapanis_saatleri():
    """Kod basina borsa saat dilimi, yerel ve ET kapanis saati (Yahoo meta; ornek gun 2026-11-20, ABD kis saati)."""
    return pd.read_csv(os.path.join(VERI, "kapanis_saatleri.csv"), dtype={"kod": str})


def fomc():
    """2005-2026 FOMC: karar_gunu, tur (planli/olaganustu_toplanti/konferans_gorusmesi/notation_vote/iptal), basin_toplantisi, aciklama_var."""
    return pd.read_csv(os.path.join(VERI, "fomc_tarihleri.csv"), parse_dates=["karar_gunu", "ilk_gun"])


def makro():
    """CPI ve Istihdam Raporu yayin gunleri 2005-2026 (ALFRED). ayda_birden_fazla=True satirlarda ana yayin belirsiz."""
    return pd.read_csv(os.path.join(VERI, "makro_tarihleri.csv"), parse_dates=["tarih"])
