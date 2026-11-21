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
