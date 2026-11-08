"""1) Takvim ve bilgi zamanı doğrulaması (ham zaman damgaları)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_rep")
from rep_lib import *
pd.set_option("display.width", 220)

print("XNYS seans:", len(SESS), SESS.min().date(), SESS.max().date())
# Yahoo SPY/GLD tarihleri ile XNYS uyumu
for t in ["SPY", "GLD", "GDX", "GDXJ", "NUGT", "JNUG"]:
    y = yahoo(t); yi = y.index[(y.index >= START) & (y.index <= END)]
    st = max(pd.Timestamp(START), y.index.min())
    sess_t = SESS[SESS >= st]
    extra = yi.difference(SESS); miss = sess_t.difference(yi)
    print(f"{t}: yahoo gün {len(yi)}  XNYS'de olmayan {len(extra)} {list(extra.date)[:5]}  eksik seans {len(miss)} {list(miss.date)[:8]}")

# Panel endeksi ile karşılaştır
P = pd.read_parquet(f"{S}/panel/panel_etf.parquet"); PI = pd.to_datetime(P.index)
print("panel endeks:", len(PI), " XNYS-panel:", list(SESS.difference(PI).date)[:10], " panel-XNYS:", list(PI.difference(SESS).date)[:10])

# Tatiller
H = regular_holidays(); AD = adhoc_closures(); EC = early_closes()
H = H[(H.index >= "2008-01-01") & (H.index <= "2026-12-31")]
print("düzenli tatil (2008-2026):", len(H), " ad hoc kapanış:", [d.date() for d in AD if pd.Timestamp(START) <= d <= pd.Timestamp(END)])
print("erken kapanış günü sayısı:", len(EC))

# bd - seans farkı (analistin 'tatil' tanımı) vs XNYS
bd = pd.bdate_range(START, END); closed = bd.difference(SESS)
print("hafta içi kapalı gün:", len(closed), " bunlardan düzenli tatil olmayan:", [d.date() for d in closed.difference(H.index)])

# Öngörücü bilgi zamanları: ham ts_utc (bar başlangıcı) -> kapanış anı
y = yahoo("GDXJ")
ts = y.ts_utc
et = ts.dt.tz_convert("America/New_York")
print("GDXJ günlük bar başlangıcı ET saat dağılımı:", et.dt.strftime("%H:%M").value_counts().to_dict())
print("index tarihi == ET tarih:", bool((et.dt.tz_localize(None).dt.normalize() == y.index).all()))
# Kapanış anı (16:00 ET; erken kapanışta 13:00) ve karar anı (15:00 ET)
sess = SESS
close_utc = pd.Series([CAL.session_close(d) for d in sess], index=sess)
open_utc = pd.Series([CAL.session_open(d) for d in sess], index=sess)
cut_utc = pd.Series([(pd.Timestamp(d.date()).tz_localize("America/New_York") + pd.Timedelta(hours=15)).tz_convert("UTC") for d in sess], index=sess)
pc = pd.Series(pd.to_datetime(P["cut_utc"]).values, index=PI)
print("panel cut_utc == bağımsız 15:00 ET:", bool((pc.reindex(sess).dt.tz_localize("UTC") if pc.dt.tz is None else pc.reindex(sess)).eq(cut_utc).all()))
T = pd.DataFrame({"open_utc": open_utc, "close_utc": close_utc, "cut_utc": cut_utc})
T["close_prev_utc"] = T.close_utc.shift(1)
T["prev_close_before_cut"] = T.close_prev_utc < T.cut_utc
T["early_close"] = T.close_utc < T.cut_utc
print("t-1 kapanışı her zaman t 15:00 ET'den önce:", bool(T.prev_close_before_cut.iloc[1:].all()))
print("erken kapanış günleri (kapanış < 15:00 ET):", int(T.early_close.sum()))
print(T.close_utc.dt.strftime("%H:%M").value_counts().to_dict())
T.to_csv(f"{OUT}/r01_seans_zamanlari.csv")

# Yahoo günlük bar kapanış fiyatının o günün kapanışı olduğunu saatlik veriyle kontrol (son 730 gün)
hh = pd.read_parquet(f"{S}/panel/yahoo_h/GDXJ.parquet"); hh.index = pd.to_datetime(hh.index)
e = hh.index.tz_convert("America/New_York"); hh["d"] = e.normalize().tz_localize(None); hh["hm"] = e.strftime("%H:%M")
reg_h = hh[(hh.hm >= "09:30") & (hh.hm < "16:00")]
lastc = reg_h.groupby("d").close.last()
cmp = pd.DataFrame({"daily_close": y.close, "hourly_last": lastc}).dropna()
print("GDXJ günlük close vs saatlik son bar close: medyan |fark| bps", round((np.log(cmp.daily_close / cmp.hourly_last)).abs().median() * 1e4, 2), "n", len(cmp))
