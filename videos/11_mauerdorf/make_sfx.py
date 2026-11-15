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
drone = .09*np.sin(2*np.pi*55*t)+.06*np.sin(2*np.pi*82.4*t)+.03*np.sin(2*np.pi*110*t+.5*np.sin(2*np.pi*.1*t))
drone *= .75+.25*np.sin(2*np.pi*.17*t); drone += .015*lp(rng.standard_normal(n), 80); drone *= np.clip((T-t)/1.5, 0, 1); out += drone
# Morgen-Stimmung: Vögel
for k in range(8): tone(.5+k*.6, 2800+(k%3)*300, 3400, .12, .08, .05)
for k in range(10): tone(C["t_baecker"]+k*.4, 2600+(k%4)*200, 3200, .1, .06, .04)
# Brunnen
L = int((C["t_und1"]-C["t_brunnen"]+.5)*SR); add(C["t_brunnen"], .05*lp(rng.standard_normal(L), 4))
boom(C["t_fuenfzig"], .5)
# Glocke: immer schneller
tt = C["t_glocke"]
for k in range(12):
    d = max(.12, .45-k*.03); tone(tt, 440, 438, 1.6, .22, .9); tone(tt, 880, 878, 1.0, .08, .5); tt += d
# Beben
L = int((C["t_langsam"]-C["t_bebt"]+.6)*SR); x = np.arange(L)/SR
add(C["t_bebt"], .35*lp(rng.standard_normal(L), 300)*np.minimum(1, x/.3)); boom(C["t_bebt"], 1.0)
boom(C["t_ein_r"], 1.2)
for k in range(3): tone(C["t_ein_r"]+.6+k*.7, 70, 50, .5, .5, .3)  # schwere Schritte
tone(C["t_deiner"], 220, 330, .6, .2, .3)
for k in ("t_erst", "t_zweit", "t_dritt"): whoosh(C[k]-.1, .5, .3); tone(C[k]+.3, 660, 990, .25, .15, .1)
for k in range(3): whoosh(C["t_springen"]+k*.12, .5, .35); click(C["t_springen"]+k*.12, .4)
for k in range(3): boom(C["t_verr"]+k*.15, .4)
boom(C["t_hebt"], .9)
tone(C["t_wer"], 330, 330, 1.5, .2, .8); tone(C["t_wer"], 495, 495, 1.5, .12, .8)
out = out/np.max(np.abs(out))*.6
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
