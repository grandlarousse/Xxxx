"""Ekonomik tanımlı kümeler (bugün işlem gören, görece likit hisseler; ESİT AĞIRLIK).
Hayatta kalan yanlılığı: üyeler 06.11.2026 itibarıyla listede olan hisselerden seçildi; birleşen/kotasyondan
çıkan (TRKCM, ANACM, SODA, eski ASYAB, vb.) yok. Üye halka arzdan sonra ilk 20 işlem günü küme getirisine girmez."""
KUMELER = {
    "BANKA":       ["AKBNK", "GARAN", "YKBNK", "ISCTR", "VAKBN", "HALKB", "TSKB", "ALBRK", "SKBNK"],
    "HOLDING":     ["KCHOL", "SAHOL", "DOHOL", "AGHOL", "ALARK", "TKFEN", "NTHOL", "GLYHO"],
    "HAVACILIK":   ["THYAO", "PGSUS", "TAVHL", "CLEBI"],
    "RAFINERI":    ["TUPRS", "PETKM", "AYGAZ", "TRCAS"],
    "CELIK":       ["EREGL", "KRDMD", "ISDMR", "BRSAN", "CEMTS", "KCAER", "IZMDC"],
    "KOZA_ALTIN":  ["TRALT", "TRMET", "TRENJ"],
    "SAVUNMA":     ["ASELS", "OTKAR", "SDTTR", "ALTNY", "ONRYT"],
    "CIMENTO":     ["CIMSA", "OYAKC", "AKCNS", "BTCIM", "NUHCM", "AFYON", "BSOKE", "GOLTS", "KONYA"],
    "ELK_EKIPMAN": ["ASTOR", "EUPWR", "GESAN", "KONTR", "PRKAB"],
    "PERAKENDE":   ["BIMAS", "MGROS", "SOKM", "MAVI", "CRFSA"],
    "OTOMOTIV":    ["FROTO", "TOASO", "DOAS", "TTRAK", "KARSN", "ASUZU"],
    "OTO_YAN":     ["EGEEN", "BRISA", "KORDS", "FMIZP", "JANTS"],
    "TELEKOM":     ["TCELL", "TTKOM"],
    "GYO":         ["EKGYO", "ISGYO", "TRGYO", "SNGYO", "HLGYO", "OZKGY", "RYGYO"],
    "KIMYA":       ["SASA", "AKSA", "ALKIM", "DYOBY", "KMPUR"],
    "GUBRE":       ["GUBRF", "HEKTS", "BAGFS"],
    "CAM_SERAMIK": ["SISE", "KUTPO", "EGSER", "USAK", "QUAGR"],
    "GIDA":        ["ULKER", "AEFES", "CCOLA", "TATGD", "TUKAS", "BANVT", "PNSUT"],
    "ELK_URETIM":  ["AKSEN", "ENJSA", "ZOREN", "ODAS", "AYDEM", "AKENR"],
    "YENILENEBILIR": ["GWIND", "NATEN", "CWENE", "ALFAS", "SMRTG", "YEOTK"],
    "TEKNOLOJI":   ["LOGO", "NETAS", "KAREL", "INDES", "LINK", "ARDYZ", "FONET", "ALCTL"],
    "BEYAZ_ESYA":  ["ARCLK", "VESTL", "VESBE"],
    "SIGORTA":     ["ANSGR", "AKGRT", "ANHYT", "TURSG", "AGESA", "RAYSG"],
    "SAGLIK":      ["SELEC", "DEVA", "ECILC", "LKMNH", "MPARK"],
}
ENDEKSLER = ["XU100", "XU030", "XU050", "XUTUM", "XBANK", "XHOLD", "XUTEK", "XELKT", "XGIDA", "XGMYO", "XKMYA",
             "XMADN", "XMANA", "XMESY", "XINSA", "XTAST", "XTEKS", "XTRZM", "XULAS", "XUMAL", "XUSIN", "XUHIZ",
             "XILTM", "XKAGT", "XSGRT", "XTCRT", "XFINK", "XBLSM", "XSPOR"]
DOVIZ = ["USDTRY"]
# VİOP pay vadelisi olan 47 hisse (2026-11-04_kapanis_1-3gun/risk_ve_boyut_tablosu.csv)
VIOP = set("AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN "
           "GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO "
           "TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split())
def tum_kodlar():
    s = []
    for v in KUMELER.values():
        for k in v:
            if k not in s: s.append(k)
    return s + ENDEKSLER + DOVIZ
