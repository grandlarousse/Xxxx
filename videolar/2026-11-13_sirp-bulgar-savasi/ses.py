#!/usr/bin/env python3
"""560 Yıl Rumeli — Sırp-Bulgar Savaşı Reel'i için özgün ses bandı (tamamı sentez, telifsiz).
Kullanım: python3 ses.py cikti.wav   — zamanlar film.js ile eşlidir."""
import sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000; DUR = 30.0; N = int(SR * DUR)
rng = np.random.default_rng(1885)
dry = np.zeros((2, N)); send = np.zeros((2, N))
t = np.arange(N) / SR

def filt(x, kind, fc, order=2):
    wn = np.asarray(fc, dtype=float) / (SR / 2)
    return sosfilt(butter(order, wn, kind, output='sos'), x)

def put(sig, t0, gain=1.0, pan=0.0, rev=0.25):
    i = int(round(t0 * SR))
    if i >= N: return
    n = min(len(sig), N - i)
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    for ch, g in ((0, l), (1, r)):
        dry[ch, i:i + n] += sig[:n] * gain * g
        send[ch, i:i + n] += sig[:n] * gain * g * rev

def boom(f0=46.0, dur=2.6, drop=2.6, decay=2.6, noise=0.45, click=0.5):
    n = int(SR * dur); tt = np.arange(n) / SR
    f = f0 * (1 + (drop - 1) * np.exp(-tt * 20))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-tt * decay)
    x += 0.45 * np.sin(2 * ph) * np.exp(-tt * decay * 1.8)
    x += 0.25 * np.sin(3 * ph) * np.exp(-tt * decay * 2.6)
    nz = filt(rng.standard_normal(n), 'low', 2200) * np.exp(-tt * 22)
    ck = filt(rng.standard_normal(n), 'band', [90, 480]) * np.exp(-tt * 7)
    x = (x + noise * nz + click * ck) * np.minimum(1, tt / 0.003)
    return np.tanh(x * 1.5) / 1.3

def tom(f0=82.0):
    return boom(f0=f0, dur=0.9, drop=1.7, decay=7.5, noise=0.3, click=0.35)

def snare(dur=0.22):
    n = int(SR * dur); tt = np.arange(n) / SR
    x = filt(rng.standard_normal(n), 'band', [900, 7000]) * np.exp(-tt * 34) + 0.5 * np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 40)
    return x * np.minimum(1, tt / 0.001)

def whoosh(dur, rise=0.75, lo=300, hi=5000):
    n = int(SR * dur); u = np.arange(n) / n
    nz = rng.standard_normal(n)
    x = filt(nz, 'band', [lo, lo * 4]) * (1 - u) + filt(nz, 'band', [hi / 3, hi]) * u
    env = np.where(u < rise, (u / rise) ** 2.2, ((1 - u) / (1 - rise)) ** 1.5)
    return x * env

def riser(dur, f0=90.0, f1=520.0):
    n = int(SR * dur); u = np.arange(n) / n
    x = np.zeros(n)
    for k, d in ((1, 0), (1.5, 0.003), (2.01, -0.004), (3.02, 0.002)):
        f = f0 * k * (f1 / f0) ** (u ** 1.6) * (1 + d)
        x += np.sin(2 * np.pi * np.cumsum(f) / SR) / k
    return x * u ** 2.5 * 0.5 + whoosh(dur, rise=0.97, lo=400, hi=7000) * 0.9

def tick(f):
    n = int(SR * 0.09); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 95) + 0.7 * filt(rng.standard_normal(n), 'band', [2500, 8000]) * np.exp(-tt * 260)) * np.minimum(1, tt / 0.0005)

def pad(freqs, t0, t1, gain, att=1.0, rel=1.6, cutoff=1100, trem=0.0):
    n = int(SR * (t1 - t0 + rel)); tt = np.arange(n) / SR
    env = (np.minimum(1, tt / att) * np.clip((t1 - t0 + rel - tt) / rel, 0, 1)) ** 1.5
    for ch, sgn in ((0, -1), (1, 1)):
        x = np.zeros(n)
        for f in freqs:
            for det in (-0.0045, 0.0, 0.0052):
                ff = f * (1 + det + sgn * 0.0011); phs = rng.uniform(0, 2 * np.pi)
                for k in range(1, 9):
                    if ff * k > cutoff * 2.2: break
                    x += np.sin(2 * np.pi * ff * k * tt + phs * k) / (k ** 1.25) / len(freqs)
        x = filt(x, 'low', cutoff)
        if trem: x *= 1 - trem * 0.5 * (1 + np.sin(2 * np.pi * 5.2 * tt))
        x *= env * (0.88 + 0.12 * np.sin(2 * np.pi * 0.13 * tt + ch))
        i = int(t0 * SR); m = min(n, N - i)
        dry[ch, i:i + m] += x[:m] * gain; send[ch, i:i + m] += x[:m] * gain * 0.5

def voice(f, t0, dur, gain, pan=0.0):
    n = int(SR * (dur + 1.2)); tt = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.1 * tt) * np.minimum(1, tt / 0.6)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    x = np.sin(ph) + 0.42 * np.sin(2 * ph) + 0.22 * np.sin(3 * ph) + 0.1 * np.sin(4 * ph)
    env = np.minimum(1, tt / 0.35) * np.clip((dur + 1.2 - tt) / 1.2, 0, 1)
    put(x * env, t0, gain, pan, rev=0.7)

D1, G1, A1, Bb1 = 36.71, 49.0, 55.0, 58.27
D2, E2, F2, G2, A2, Bb2 = 73.42, 82.41, 87.31, 98.0, 110.0, 116.54
Cs3, D3, E3, F3, A3 = 138.59, 146.83, 164.81, 174.61, 220.0
D4, E4, F4, A4 = 293.66, 329.63, 349.23, 440.0

# pes zemin
dr = 0.9 * np.sin(2 * np.pi * D1 * t) + 0.6 * np.sin(2 * np.pi * D2 * t + 0.3) + 0.25 * np.sin(2 * np.pi * A2 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t))
dry += dr * np.interp(t, [0, 0.3, 3, 9.4, 10.4, 13.0, 13.2, 23.8, 27, 29.2, 30], [0, 0.25, 0.5, 0.55, 0.22, 0.3, 0.7, 0.75, 0.5, 0.25, 0]) * 0.16
# akorlar: Re minör → askıda → Si bemol → Sol minör → La → Re minör
pad([D2, A2, D3, F3], 1.6, 9.4, 0.085, att=2.0)
pad([D2, A3, E4], 9.4, 13.1, 0.045, att=1.2, cutoff=1500, trem=0.35)
pad([Bb1, F2, Bb2, D3, F3], 13.2, 19.3, 0.11, att=0.25)
pad([G1, D2, G2, Bb2, D3], 19.3, 22.0, 0.12, att=0.2)
pad([A1, E2, A2, Cs3, E3], 22.0, 23.8, 0.125, att=0.15, rel=0.8)
pad([D1, D2, A2, D3, F3, A3], 23.8, 29.0, 0.12, att=0.3, rel=1.8)
# vuruşlar (yazıların çarptığı anlar)
for t0, g in ((0.30, 0.95), (0.52, 0.55), (1.55, 1.0), (1.80, 0.6), (3.2, 0.5), (7.0, 0.75), (7.2, 0.45), (9.9, 0.6), (13.2, 1.0), (13.55, 0.9),
              (14.5, 0.8), (14.8, 0.5), (15.1, 0.5), (17.5, 0.7), (19.6, 0.8), (22.0, 0.95), (23.8, 0.7), (24.3, 0.55), (24.9, 0.85), (25.3, 1.0), (27.2, 0.5)):
    put(boom(), t0, g * 0.8, 0, rev=0.45)
# Slivnitsa topları
for t0, g, pan in ((19.9, 0.9, -0.3), (20.5, 0.75, 0.35), (20.8, 0.85, -0.1), (21.4, 0.6, 0.25)):
    put(boom(f0=58, dur=1.8, drop=3.2, decay=3.6, noise=0.9, click=0.8), t0, g * 0.7, pan, rev=0.6)
# savaş davulları ve trampet (100 vuruş/dk, sekizlik = 0,3 sn)
pat = [1.0, 0, 0.45, 0.7, 0, 0.5, 0.8, 0.45]
t0, k = 14.5, 0
while t0 < 23.6:
    b = (t0 - 14.5) / 9.1
    if pat[k % 8] > 0:
        put(tom((84, 74, 92)[k % 3]), t0, pat[k % 8] * (0.30 + 0.22 * b), (-0.25, 0.25, 0)[k % 3], rev=0.35)
    sg = (0.05 if k % 2 else 0.085) * (0.8 + 0.5 * b)
    put(snare(), t0, sg, 0.15, rev=0.3)
    if k % 4 == 3: put(snare(), t0 + 0.15, sg * 0.7, 0.15, rev=0.3)
    t0 += 0.3; k += 1
def roll(a, b, g0, g1):
    x = a
    while x < b - 1e-6:
        put(snare(0.12), x, g0 + (g1 - g0) * (x - a) / (b - a), 0.1, rev=0.3); x += 0.0625
roll(12.7, 13.2, 0.02, 0.2); roll(17.0, 17.5, 0.04, 0.2); roll(19.15, 19.6, 0.04, 0.22); roll(21.55, 22.0, 0.05, 0.26)
# geçiş sesleri
put(whoosh(0.55), 2.7, 0.22); put(whoosh(1.4, rise=0.6), 6.65, 0.28); put(whoosh(0.9, rise=0.9), 9.0, 0.2)
put(riser(1.2), 12.0, 0.30); put(whoosh(0.7), 18.9, 0.22); put(riser(0.6, 140, 500), 23.2, 0.2)
put(whoosh(1.2, rise=0.15), 23.8, 0.25); put(whoosh(0.6), 26.6, 0.15)
# İstanbul'un sessizliği: saat
for j in range(6):
    put(tick(2100 if j % 2 == 0 else 1680), 10.3 + 0.5 * j, 0.22, 0.15 if j % 2 else -0.15, rev=0.5)
# ezgi
voice(A3, 3.6, 1.4, 0.035); voice(D4, 5.1, 1.6, 0.035); voice(A4, 10.0, 2.6, 0.016)
voice(D4, 24.3, 1.0, 0.05); voice(F4, 25.3, 1.2, 0.055); voice(E4, 26.6, 0.9, 0.05); voice(D4, 27.6, 2.0, 0.055)
# rüzgâr
w = filt(rng.standard_normal((2, N)), 'band', [180, 900])
dry += w * np.interp(t, [0, 2, 9.4, 10.5, 13, 13.2, 24, 27, 30], [0.4, 0.5, 0.6, 1.0, 1.0, 0.3, 0.4, 0.8, 0.0]) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.21 * t + 1)) * 0.035
# yankı ve son işlem
irn = int(SR * 2.6); ti = np.arange(irn) / SR
wet = np.zeros((2, N))
for ch in range(2):
    ir = filt(filt(rng.standard_normal(irn) * np.exp(-ti * 2.5), 'low', 5200), 'high', 180)
    wet[ch] = fftconvolve(send[ch], ir / np.sqrt(np.sum(ir ** 2)))[:N]
mix = filt(dry + wet * 0.55, 'high', 24)
mix = np.tanh(mix / np.percentile(np.abs(mix), 99.9) * 1.1)
mix *= 0.9 / np.max(np.abs(mix))
mix *= np.minimum(1, t / 0.02) * np.clip((DUR - t) / 1.0, 0, 1)
with wave.open(sys.argv[1], 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes((mix.T * 32767).astype('<i2').tobytes())
print('ses yazıldı', sys.argv[1])
