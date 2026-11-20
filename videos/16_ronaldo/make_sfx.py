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
pad = sum(g*np.sin(2*np.pi*f*t + .3*np.sin(2*np.pi*.07*t)) for f, g in ((130.8, .04), (164.8, .035), (196.0, .03), (246.9, .015)))
pad *= np.clip(t/1.0, 0, 1)*np.clip((T-t)/1.5, 0, 1); out += pad
wind = lp(rng.standard_normal(n), 60)*(.03 + .02*np.sin(2*np.pi*.13*t)**2); out += wind
def creak(t0, g=.25):
    L = int(.7*SR); x = np.arange(L)/SR; f = 180 + 60*np.sin(2*np.pi*3*x)
    add(t0, g*np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*np.exp(-x*3)*.5)
def knock(t0, g=.9): boom(t0, g*.6); noise(t0, .12, .03, 6, g*.5)
def vib(t0, d=1.0):
    L = int(d*SR); x = np.arange(L)/SR; add(t0, .25*np.sin(2*np.pi*170*x)*(np.sin(2*np.pi*9*x) > 0))
def crowd(t0, dur, g=.05):
    L = int(dur*SR); x = np.arange(L)/SR; add(t0, g*lp(rng.standard_normal(L), 25)*np.sin(np.pi*x/dur)**.5)
def kick(t0, g=.9): boom(t0, g*.5); noise(t0, .05, .02, 2, g*.6)
def steps(t0, t1, period=.4, g=.18):
    t = t0
    while t < t1: noise(t, .06, .02, 3, g); t += period
crowd(0, C["t_doch"], .06); whoosh(C["t_ronaldo1"], .5, .3); tone(C["t_ronaldo1"]+.3, 523, 784, .4, .1, .3)
tone(C["t_d1"], 880, 880, .2, .1, .1); tone(C["t_d1"]+.2, 1175, 1175, .3, .1, .2)
whoosh(C["t_256"], .6, .3); whoosh(C["t_du_spr"], .5, .3); boom(C["t_du_spr"]+.8, .5)
tone(C["t_nicht_mal"]+.15, 392, 330, .5, .1, .3)
tone(C["t_d2"], 880, 880, .2, .1, .1); tone(C["t_d2"]+.2, 1175, 1175, .3, .1, .2); steps(C["t_d2"], C["t_doch"], .36)
for k in range(7): click(C["t_trainierst"]+k*.2, .3)
boom(C["t_doch"], .8); whoosh(C["t_doch"]-.2, .7, .3); tone(C["t_bett"], 523, 523, .5, .08, .4)
for k in range(5): tone(C["t_fuenf"]-.3+k*.18, 660+k*80, 660+k*80, .15, .07, .1)
tone(C["t_fit"], 784, 1047, .3, .08, .2)
for k in range(10): tone(C["t_puls"]+k*.9, 880, 880, .08, .06, .05)
for k in range(4): tone(C["t_wecker"]+.9+k*.25, 1568, 1568, .12, .08, .08)
tone(C["t_woche1"]+.3, 523, 659, .4, .08, .3); tone(C["t_woche4"]+.3, 659, 988, .5, .1, .3); steps(C["t_woche4"], C["t_soweit"], .28, .2)
tone(C["t_d3"], 880, 880, .2, .1, .1); tone(C["t_d3"]+.2, 1175, 1175, .3, .1, .2); crowd(C["t_d3"], C["t_wirst"]-C["t_d3"], .08)
steps(C["t_laeufst"], C["t_laeufst"]+1.0, .3, .25); whoosh(C["t_laeufst"]+.6, .6, .3)
tone(C["t_ehrlich"], 330, 300, .4, .08, .3)
for k in range(3): tone(C["t_schuss"]-1.0+k*.6, 523+k*130, 523+k*130, .3, .08, .2)
out = out/np.max(np.abs(out))*.6
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
