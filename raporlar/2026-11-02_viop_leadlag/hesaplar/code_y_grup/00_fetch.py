# Eksik grup sembollerini indir (günlük + saatlik). Ortak dizine yazar; varsa atlar.
import sys, time
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
import ydl
D = "ISATR ISBTR ADEL KERVT AGESA CRFSA TKNSA ZRGYO HLGYO TERA TEHOL BORLS CONSE NATEN GLBMD INTEM AKENR AKMGY ISGSY ISYAT GOZDE VAKFN VKGYO AKFGY AKFYE".split()
H = "ISDMR VESBE KRDMA KRDMB TRENJ BRYAT AKGRT CANTE GWIND ALCAR ISGYO ISFIN ECILC ECZYT GLYHO ASUZU ALGYO".split()
for s in D:
    r = ydl.fetch(s + ".IS", "daily"); print("daily", s, r, flush=True); time.sleep(0.3)
for s in H:
    r = ydl.fetch(s + ".IS", "h1"); print("h1", s, r, flush=True); time.sleep(0.3)
