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
# dunkle Drone + Höhenwind (Format B Nacht)
pad = sum(g*np.sin(2*np.pi*f*t + .4*np.sin(2*np.pi*.05*t)) for f, g in ((55, .07), (82.4, .05), (110, .03), (116.5, .015)))
pad *= np.clip(t/1.0, 0, 1)*np.clip((T-t)/1.5, 0, 1); out += pad
wind = lp(rng.standard_normal(n), 60)*(.03 + .02*np.sin(2*np.pi*.13*t)**2); out += wind
def creak(t0, g=.25):
    L = int(.7*SR); x = np.arange(L)/SR; f = 180 + 60*np.sin(2*np.pi*3*x)
    add(t0, g*np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*np.exp(-x*3)*.5)
def knock(t0, g=.9): boom(t0, g*.6); noise(t0, .12, .03, 6, g*.5)
def vib(t0, d=1.0):
    L = int(d*SR); x = np.arange(L)/SR; add(t0, .25*np.sin(2*np.pi*170*x)*(np.sin(2*np.pi*9*x) > 0))
tone(C["t_drei0"], 880, 880, .6, .08, .3)
creak(1.2, .15); creak(C["t_bewegt"], .2)
for k in range(6): click(C["t_luftdruck"]+k*.12, .2)
noise(C["t_knackt"], .5, .2, 3, .35); tone(C["t_achtung"]-.3, 660, 660, .25, .12, .2); tone(C["t_achtung"]-.05, 440, 440, .3, .12, .2)
for k in range(4): click(C["t_fenster"]+k*.3, .25)
boom(C["t_kippt"], 1.0); creak(C["t_kippt"]+.1, .35); creak(C["t_kippt"]+1.2, .25)
for k in range(3): tone(C["t_blinkt"]+k*.4, 1200, 1200, .12, .05, .05)
noise(C["t_wieder"], .4, .2, 3, .3)
for k in ("t_r1", "t_r2", "t_r3"): boom(C[k], .5); whoosh(C[k]-.2, .5, .25)
creak(C["t_schritt"]+.2, .3)
boom(C["t_keine"]+.2, .7)
for k in range(3): tone(C["t_waehlst"]+k*.3, 1400, 1400, .12, .12, .05)
knock(C["t_klopft"]); knock(C["t_klopft"]+.45)
creak(C["t_griff"], .3); vib(C["t_vibriert"])
whoosh(C["t_wer"], 1.5, .3); boom(C["t_vor_tuer"], .8)
for k in range(4): noise(C["t_du_musst"]+.4+k*.25, .2, .08, 1, .25)
creak(C["t_dach"]+.3, .4); boom(C["t_dach"]+.5, .6)
tone(C["t_teil2"], 110, 55, 2.0, .2, 1.0); boom(C["t_teil2"], .9)
out = out/np.max(np.abs(out))*.6
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
