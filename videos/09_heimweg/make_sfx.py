#!/usr/bin/env python3
"""assets/sfx_bed.wav: Nacht-Drone, Schritte, Bus, Herzschlag, Türglocke, Wähltöne, Hits – an den Cues aus assets/cues.json."""
import json, wave, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "assets/cues.json")))
SR = 44100; T = C["TOTAL"]; n = int(SR * T); t = np.arange(n) / SR
rng = np.random.default_rng(9); out = np.zeros(n)
def add(t0, sig):
    i0 = int(t0 * SR); i1 = min(n, i0 + len(sig))
    if i0 < n: out[i0:i1] += sig[: i1 - i0]
def lp(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
def env(L, a, d): x = np.arange(L) / SR; return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / d)
def tone(t0, f0, f1, dur, g, dec=.4):
    L = int(dur * SR); f = np.linspace(f0, f1, L); add(t0, g * np.sin(2*np.pi*np.cumsum(f)/SR) * env(L, .005, dec))
def step(t0, g=.5):
    L = int(.12 * SR); add(t0, g * env(L, .002, .025) * lp(rng.standard_normal(L), 6)); tone(t0, 90, 60, .1, g*.6, .03)
def steps(t0, t1, period, g=.45, jitter=0.0):
    k = t0
    while k < t1: step(k, g); k += period
def boom(t0, g=1.0):
    L = int(2 * SR); x = np.arange(L)/SR; f = 70*np.exp(-x*1.5)+30
    add(t0, g*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*2.2))
def whoosh(t0, dur, g=.35):
    L = int(dur*SR); x = np.arange(L)/L; add(t0, g*(np.sin(np.pi*x)**2)*lp(rng.standard_normal(L), 14))
def chime(t0):
    for k, f in enumerate((988, 784)): tone(t0 + k*0.35, f, f, 1.2, .25, .5)
def dtmf(t0, d):
    pairs = {"1": (697, 1209), "0": (941, 1336)}
    a, b = pairs[d]; L = int(.16*SR); x = np.arange(L)/SR
    add(t0, .12*(np.sin(2*np.pi*a*x)+np.sin(2*np.pi*b*x))*np.minimum(1, (L-np.arange(L))/400))
# Drone: tiefe Nacht-Fläche, nie Stille
drone = .09*np.sin(2*np.pi*55*t) + .06*np.sin(2*np.pi*73.4*t) + .03*np.sin(2*np.pi*110*t+0.5*np.sin(2*np.pi*.1*t))
drone *= .75 + .25*np.sin(2*np.pi*.15*t); drone += .015*lp(rng.standard_normal(n), 80)
drone *= np.clip((T - t) / 2.0, 0, 1); out += drone
# Bus: Zischen der Tür, Anfahren
whoosh(C["t_steigst"], .7, .35); whoosh(C["t_jemand"] + 1.2, 1.8, .4)
# Schritte (deine + seine, später schneller)
steps(C["t_hoerst"], C["t_bestimmt"], .55, .45); steps(C["t_hoerst"] + .27, C["t_bestimmt"], .55, .3)
steps(C["t_gehst"], C["t_schauf"], .36, .5); steps(C["t_gehst"] + .18, C["t_schauf"], .38, .4)
steps(C["t_vorne"], C["t_rein"], .5, .35)
# Herzschlag im Schaufenster
for k in range(4): tone(C["t_kapuze"] + k*.85, 60, 45, .25, .9, .08); tone(C["t_kapuze"] + .22 + k*.85, 55, 40, .25, .6, .08)
tone(C["t_fehler"], 180, 120, .5, .35, .2)               # Fehler-Ton
boom(C["t_polizei"], .7)                                  # Regel-Teil beginnt
for k in ("t_r1", "t_r2", "t_r3"): whoosh(C[k] - .1, .5, .3); tone(C[k] + .2, 660, 660, .25, .18, .12)
boom(C["t_er2"], .6)                                      # er wechselt auch
chime(C["t_rein"])                                        # Ladentür-Glocke
for k, d in enumerate("110"): dtmf(C["t_waehlst"] + .1 + k*.25, d)
for k in range(3):                                        # Freizeichen
    L = int(1.0*SR); x = np.arange(L)/SR; add(C["t_waehlst"] + 1.2 + k*2.0, .07*np.sin(2*np.pi*425*x)*(x < .9))
tone(C["t_standort"], 1200, 1800, .25, .2, .1)            # Standort gesendet
boom(C["t_weg"], 1.0)                                     # „… geht nicht weg“
boom(C["t_teil2"], .9); whoosh(C["t_teil2"] - .3, 1.2, .35)
out = out / np.max(np.abs(out)) * 0.6
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
