"""v_YG2_a — BAĞIMSIZ veri katmanı (ll.py import edilmez).
Ham parquet'lerden (data/daily, data/h1) hisse-gün paneli kurar.

Kurallar (görev metni):
- Günlük index = ldate (BIST işlem günü). Bayat gün = hacim 0 VE h==l -> gün NaN.
- Kurumsal işlem eşiği rejime bağlı: 2020-03-13 öncesi fiyat bazında ±%20,5, sonrası ±%10,5 (h1 dönemi 2023-11+ -> ±%10,5).
  Her getiri parçası (C_t->O_{t+1}, C_t->P0730_{t+1}, ...) önceki kapanışa göre bu eşiği aşarsa NaN.
- h1: bar etiketi = başlangıç (UTC). 06:30 barı c = 07:30 fiyatı (10:30 TSİ); 13:30 barı c = P1430 (17:30 TSİ);
  14:30 barı c = P1500 = sürekli işlemin son fiyatı (18:00 TSİ) — YALNIZ 14:30 barı olan (AB yaz saati) günlerde.
- Yarım gün (h1 bar sayısı <=6) -> o günün CA'sı NaN.
Çıktı: res/panel.parquet (uzun format: date, stock, O,H,L,C,V, P0730,P0830,P1430,P1500, fb_h, fb_l (06:30 barı h/l), summer, half)
"""
import numpy as np, pandas as pd, os, sys
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = SCR + "/data"; RES = SCR + "/out/code_v_YG2_a/res"; os.makedirs(RES, exist_ok=True)
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
SYMS = VIOP + ["XU030", "XU100"]


def daily(sym):
    d = pd.read_parquet(f"{D}/daily/{sym}.IS.parquet")
    d.index = pd.DatetimeIndex(d["ldate"].values).normalize()
    d = d[~d.index.duplicated(keep="last")].sort_index()
    d = d[["o", "h", "l", "c", "v"]].astype(float)
    stale = (d["v"].fillna(0) == 0) & (d["h"] == d["l"])
    if sym.startswith("X"):  # endekslerde hacim yok/anlamsız olabilir
        stale = d["h"] == d["l"]
    d.loc[stale, :] = np.nan
    return d.rename(columns={"o": "O", "h": "H", "l": "L", "c": "C", "v": "V"})


def h1(sym):
    h = pd.read_parquet(f"{D}/h1/{sym}.IS.parquet")
    h = h[~h.index.duplicated(keep="last")].sort_index()
    t = h.index.tz_convert("UTC")
    day = pd.DatetimeIndex(t.tz_localize(None).normalize())
    hm = t.hour * 100 + t.minute
    df = pd.DataFrame({"day": day, "hm": hm, "o": h["o"].values, "h": h["h"].values, "l": h["l"].values, "c": h["c"].values, "v": h["v"].values})
    piv = df.pivot_table(index="day", columns="hm", values="c", aggfunc="last")
    nb = df.groupby("day").size()
    out = pd.DataFrame(index=piv.index)
    for k, nm in [(630, "P0730"), (730, "P0830"), (830, "P0930"), (1230, "P1330"), (1330, "P1430"), (1430, "P1500")]:
        out[nm] = piv[k] if k in piv.columns else np.nan
    fb = df[df.hm == 630].set_index("day")
    out["fb_h"] = fb["h"]; out["fb_l"] = fb["l"]; out["fb_o"] = fb["o"]
    out["nb"] = nb
    return out


def build():
    # takvim: XU030 h1 günleri; summer = XU030'da 14:30 barı var
    X = h1("XU030")
    days = X.index
    summer = X["P1500"].notna()
    half = X["nb"] <= 6
    rows = []
    for s in SYMS:
        d = daily(s).reindex(days)
        try:
            hh = h1(s).reindex(days)
        except FileNotFoundError:
            print("h1 yok", s); continue
        p = pd.concat([d, hh.drop(columns=["nb"])], axis=1)
        p["summer"] = summer.values; p["half"] = half.values
        p["stock"] = s; p["date"] = days
        rows.append(p.reset_index(drop=True))
    P = pd.concat(rows, ignore_index=True)
    P.to_parquet(RES + "/panel.parquet")
    print(P.shape, P.date.min(), P.date.max(), "yaz günü:", int(summer.sum()), "yarım gün:", int(half.sum()))
    return P


if __name__ == "__main__":
    build()
