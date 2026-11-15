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
# Kühlschrank: Tür + Brummen
for k in ("t_kuehl", "t_naechsten", "t_aufgef"):
    whoosh(C[k], .5, .3); L = int(2.5*SR); x = np.arange(L)/SR; add(C[k]+.2, .05*np.sin(2*np.pi*100*x)*np.minimum(1, x/.3)*np.minimum(1, (2.5-x)/.5))
tone(C["t_joghurt"], 300, 200, .5, .3, .2); tone(C["t_merk"], 880, 880, .4, .2, .2)
def creak(t0, dur=.8, g=.3):
    L = int(dur*SR); x = np.arange(L)/L; f = np.linspace(160, 110, L) + 25*np.sin(2*np.pi*14*x)
    add(t0, g*np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*lp(np.ones(L), 1)*np.sin(np.pi*x)*0.5)
creak(C["t_knarzen"], .9, .35); creak(C["t_knarzen"]+1.1, .7, .25)
boom(C["t_doch"], 1.0)
boom(C["t_japan"]+.22, .5)
click(C["t_ab"]-.2, .6); click(C["t_ab"]+.05, .7); boom(C["t_schl"], .3)
tone(C["t_kamera"], 1500, 1500, .15, .2, .05); tone(C["t_kamera"]+.18, 2000, 2000, .15, .2, .05)
for k in range(5):  # Vibration
    L = int(.12*SR); x = np.arange(L)/SR; add(C["t_vibr"]+k*.15, .25*np.sign(np.sin(2*np.pi*150*x)))
for k in range(4): tone(C["t_fremde"]+k*.75, 60, 45, .25, .9, .08); tone(C["t_fremde"]+.22+k*.75, 55, 40, .25, .6, .08)
boom(C["t_fremde"], .8)
for k in range(2):  # Freizeichen
    L = int(.9*SR); x = np.arange(L)/SR; add(C["t_ruft"]+.3+k*1.4, .07*np.sin(2*np.pi*425*x))
click(C["t_beamten"], .5)
for k in (C["t_tueren"], C["t_tueren"]+.3): tone(k, 400, 300, .15, .3, .05)
tone(C["t_bis"], 110, 110, 2.0, .25, 1.2)
L = int(.8*SR); x = np.arange(L)/L; add(C["t_schiebt"]+.3, .2*lp(rng.standard_normal(L), 30)*np.sin(np.pi*x))  # Schiebetür
boom(C["t_darin"], 1.0)
for k in range(6): click(C["t_sie"]+.2+k*.3, .25)
L = int(1.8*SR); add(C["t_dusch"]-.3, .12*lp(rng.standard_normal(L), 3)*np.minimum(1, np.arange(L)/(.2*SR))*np.minimum(1, (L-np.arange(L))/(.4*SR)))  # Dusche
creak(C["t_und_kn"]+.4, 1.2, .35)
tone(C["t_fehlende"], 220, 220, 1.5, .25, .8); tone(C["t_fehlende"], 330, 330, 1.5, .15, .8)
out = out/np.max(np.abs(out))*.6
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
