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
def whistle(t0, notes=(784, 659, 698, 587, 659), g=.07, d=.32):   # Spieluhr-artige gepfiffene Melodie
    for k, f in enumerate(notes):
        L = int(d*SR); x = np.arange(L)/SR
        add(t0 + k*d, g*np.sin(2*np.pi*f*x + 3*np.sin(2*np.pi*5.5*x)/5.5)*np.sin(np.pi*x/d)**.6)
def musicbox(t0, notes=(1568, 1319, 1397, 1175, 1319, 1047), g=.05, d=.28):
    for k, f in enumerate(notes): tone(t0 + k*d, f, f, .6, g, .35)
def steps(t0, t1, period=.5, g=.18):
    t = t0
    while t < t1: noise(t, .07, .02, 3, g); t += period
steps(.1, C["t_pfeift"], .5)
whistle(C["t_pfeift"]); musicbox(C["t_melodie"]); musicbox(C["t_melodie"]+1.9, g=.04)
vib(C["t_vibriert"]); tone(C["t_achtung"]-.4, 880, 880, .25, .08, .2); tone(C["t_achtung"]-.15, 660, 660, .3, .08, .2)
steps(C["t_bestimmt"], C["t_doch"], .5)
for k in range(3): creak(C["t_hebt"]+k*.4, .25)
noise(C["t_finger"], 1.6, .8, 2, .12); boom(C["t_spalt"], .5)
vib(C["t_neue"]-.2, .6)
for k in ("t_r1", "t_r2", "t_r3"): boom(C[k], .45); whoosh(C[k]-.2, .5, .22)
whistle(C["t_pfeifen"], g=.05)
steps(C["t_laeufst"], C["t_dann_aus"], .32, .22)
for k in range(3):
    t0 = C["t_dann_aus"] + .5 + k*.7
    for j in range(3): click(t0 + j*.09, .25)
    boom(t0 + .35, .35)
for k in range(2): noise(C["t_hilf"]+k*.6, .4, .2, 8, .1)
vib(C["t_vibr2"])
tone(C["t_wer"], 110, 98, 2.2, .14, 1.6); whoosh(C["t_wer"], 1.5, .25)
for k in range(5): click(C["t_flackert"]+k*.55, .3)
whistle(C["t_nur"], g=.06); boom(C["t_hoert"]+.2, .8)
whoosh(C["t_rennen"]-.6, .5, .3); whoosh(C["t_stehen"]-.6, .5, .3)
step = max(.45, (C["t_folge"] - .3 - C["t_rennen"] - .4)/4)
for k in range(4): click(C["t_rennen"]+.3+k*step+step*.5, .45); tone(C["t_rennen"]+.3+k*step+step*.5, 990, 1320, .12, .08, .06)
for k in range(int((C["t_folge"]-C["t_rennen"])/.5)): tone(C["t_rennen"]+k*.5, 1600, 1600, .03, .04, .01)
tone(C["t_folge"]-.3, 110, 55, 2.0, .2, 1.0); boom(C["t_folge"]-.3, .9); musicbox(C["t_folge"]+.6, g=.035)
out = out/np.max(np.abs(out))*.6
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
