#!/usr/bin/env python3
"""assets/sfx_bed.wav: Drone + Soundeffekte an den Cues (assets/cues.json)."""
import json, wave, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "assets/cues.json")))
SR = 44100; T = C["TOTAL"]; n = int(SR*T); t = np.arange(n)/SR
rng = np.random.default_rng(10); out = np.zeros(n)
def add(t0, s):
    i0 = int(t0*SR); i1 = min(n, i0+len(s))
    if i0 < n: out[i0:i1] += s[:i1-i0]
def lp(x, k): return np.convolve(x, np.ones(k)/k, mode="same")
def env(L, a, d): x = np.arange(L)/SR; return np.minimum(1, x/max(a, 1e-4))*np.exp(-x/d)
def tone(t0, f0, f1, dur, g, dec=.4):
    L = int(dur*SR); f = np.linspace(f0, f1, L); add(t0, g*np.sin(2*np.pi*np.cumsum(f)/SR)*env(L, .005, dec))
def noise(t0, dur, dec, k, g): L = int(dur*SR); add(t0, g*env(L, .003, dec)*lp(rng.standard_normal(L), k))
def boom(t0, g=1.):
    L = int(2*SR); x = np.arange(L)/SR; f = 70*np.exp(-x*1.5)+30; add(t0, g*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*2.2))
def whoosh(t0, dur, g=.35): L = int(dur*SR); x = np.arange(L)/L; add(t0, g*(np.sin(np.pi*x)**2)*lp(rng.standard_normal(L), 14))
def click(t0, g=.5): noise(t0, .06, .01, 2, g); tone(t0, 2200, 1800, .05, g*.4, .01)
# warmer Klangteppich (Dur-Akkord, sanft schwebend) statt düsterer Drone
pad = sum(g*np.sin(2*np.pi*f*t + .3*np.sin(2*np.pi*.07*t)) for f, g in ((130.8, .05), (164.8, .04), (196.0, .035), (261.6, .02)))
night = (t > C["t_aber"]) & (t < C["t_also1"])
pad *= np.where(night, .6, 1.0)
pad *= np.clip(t/1.5, 0, 1)*np.clip((T-t)/1.5, 0, 1); out += pad
out += .012*lp(rng.standard_normal(n), 120)  # leiser Wind
for k in range(14): tone(.4+k*.45, 2800+(k%3)*350, 3500, .1, .06, .04)   # Vögel
for k in range(10): tone(C["t_ringsum"]+k*.35, 2600+(k%4)*200, 3300, .1, .05, .04)
for k in range(3): tone(C["t_see"]+.1+k*.25, 520, 480, .12, .12, .05)   # Enten

for k in ("t_matr", "t_lampe", "t_fenster1"): tone(C[k], 660, 880, .2, .15, .08)
for k in range(6): tone(C["t_aber"]+k*.5, 1200, 1200, .4, .03, .3)   # Grillen-artig
for k in range(6): tone(C["t_platz"]+k*.15, 700+k*60, 700+k*60, .15, .06, .1)
boom(C["t_regel"], .6); whoosh(C["t_laut"], .6, .3)
whoosh(C["t_komm1"]+.5, .6, .3); tone(C["t_komm1"]+1.1, 880, 1320, .25, .15, .1)
for k in ("t_baue1", "t_baue2", "t_baue3"): boom(C[k]-.1+.22, .6); tone(C[k]+.2, 523, 523, .5, .12, .3); tone(C[k]+.2, 659, 659, .5, .1, .3)
for k in range(11): click(C["t_jeder2"]+.1+k*.11, .3); tone(C["t_jeder2"]+.2+k*.11, 900+k*40, 900+k*40, .08, .08, .04)
whoosh(C["t_stock"]-.3, .8, .35); boom(C["t_stock"]+.6, 1.0)
for k in range(5): click(C["t_morgen"]+k*.3, .3)
for k in range(12): tone(C["t_morgen"]+k*.12, 700, 720, .1, .05, .05)
tone(C["t_wie"], 523, 523, 1.5, .15, .8); tone(C["t_wie"], 784, 784, 1.5, .1, .8)
out = out/np.max(np.abs(out))*.6
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
