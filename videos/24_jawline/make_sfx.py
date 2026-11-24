#!/usr/bin/env python3
"""assets/sfx_bed.wav – Format D: keine Musik, nur sehr dezente Effekte."""
import json, wave, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "assets/cues.json")))
SR = 44100; T = C["TOTAL"]; n = int(SR*T); rng = np.random.default_rng(3); out = np.zeros(n)
def add(t0, s):
    i0 = int(t0*SR); i1 = min(n, i0+len(s))
    if 0 <= i0 < n: out[i0:i1] += s[:i1-i0]
def lp(x, k): return np.convolve(x, np.ones(k)/k, mode="same")
def env(L, a, d): x = np.arange(L)/SR; return np.minimum(1, x/max(a, 1e-4))*np.exp(-x/d)
def tone(t0, f0, f1, dur, g, dec=.1):
    L = int(dur*SR); f = np.linspace(f0, f1, L); add(t0, g*np.sin(2*np.pi*np.cumsum(f)/SR)*env(L, .003, dec))
def noise(t0, dur, dec, k, g): L = int(dur*SR); add(t0, g*env(L, .002, dec)*lp(rng.standard_normal(L), k))
def pop(t0, f=900, g=.08): tone(t0, f, f*1.4, .08, g, .03)
def whoosh(t0, dur=.35, g=.18): L = int(dur*SR); x = np.arange(L)/L; add(t0, g*np.sin(np.pi*x)**2*lp(rng.standard_normal(L), 10))
def splash(t0):
    noise(t0, .5, .18, 3, .5); tone(t0, 600, 200, .25, .15, .08)
    for k in range(5): tone(t0+.05+k*.05, 1400-k*150, 900, .06, .06, .03)
def tap(t0): noise(t0, .05, .01, 2, .35); tone(t0, 220, 160, .08, .2, .03)
whoosh(C["t_gag"], .35, .22)
for k in ("t_knochen1", "t_fett1", "t_fertig", "t_kaust2", "t_kaumuskel", "t_breiter", "t_schaerfer", "t_bizeps", "t_bauch", "t_elf", "t_k2", "t_f2", "t_kinn2", "t_kiefer", "t_abfuehrend", "t_kfett", "t_gerade", "t_kopf", "t_brei"):
    pop(C[k], 880)
for k in range(6): tap(C["t_und_das"] + k*.3)
tone(C["t_kuh"], 180, 140, .9, .12, .5)
out = out/max(1e-6, np.max(np.abs(out)))*.5
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
