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
for k in range(6): noise(C["t_kratzt"]+k*.18, .16, .05, 1, .3)     # Kratzen auf Metall
boom(C["t_entsch"]+.1, .5); tone(C["t_luke"], 523, 523, .3, .1, .2)
for k, t0 in enumerate((C["t_dreht"], C["t_zenti"], C["t_zenti"]+.7)): creak(t0, .3)
whoosh(C["t_stange"]-.1, .5, .25); click(C["t_steckst"]+.9, .7); boom(C["t_steckst"]+1.0, .4)
for k in range(2): tone(C["t_halb"]+k*.15, 880+k*220, 880+k*220, .25, .1, .15)
boom(C["t_stoppt"], .8); click(C["t_stoppt"]+.05, .6)
tone(C["t_akku"], 440, 330, .5, .08, .3)
noise(C["t_knackt"], .5, .2, 3, .35); tone(C["t_fahrgast"]-.3, 660, 660, .25, .1, .2)
boom(C["t_regel"], .5); tone(C["t_ruehrst"], 523, 784, .3, .1, .2)
vib(C["t_vibriert"])
whoosh(C["t_wer"], 1.2, .3); boom(C["t_wer"]+.4, .7)
boom(C["t_kippt"], 1.0); creak(C["t_kippt"]+.1, .4); creak(C["t_kippt"]+1.4, .3); boom(C["t_schwer"], .6)
noise(C["t_beschlaegt"], 1.5, .8, 40, .12)
tone(C["t_punkte"], 1800, 1700, 1.2, .04, .8); boom(C["t_punkte"], .6)
for k in range(3): noise(C["t_fluestert"]+k*.4, .3, .15, 8, .1)
whoosh(C["t_lampe"]-.3, .5, .3); whoosh(C["t_dunkel"]-.6, .5, .3)
step = max(.45, (C["t_folge"] - .3 - C["t_lampe"] - .5)/4)
for k in range(4): click(C["t_lampe"]+.4+k*step+step*.5, .45); tone(C["t_lampe"]+.4+k*step+step*.5, 990, 1320, .12, .08, .06)
for k in range(int((C["t_folge"]-C["t_lampe"])/.5)): tone(C["t_lampe"]+.2+k*.5, 1600, 1600, .03, .04, .01)
tone(C["t_folge"]-.3, 110, 55, 2.0, .2, 1.0); boom(C["t_folge"]-.3, .9)
out = out/np.max(np.abs(out))*.6
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
