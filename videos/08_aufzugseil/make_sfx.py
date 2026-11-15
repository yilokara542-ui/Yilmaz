#!/usr/bin/env python3
"""Erzeugt assets/sfx_bed.wav: Spannungs-Drone + Soundeffekte an den Cue-Zeiten (deterministisch)."""
import json, wave, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "assets/cues.json")))
SR, T = 44100, 80.8
n = int(SR * T); t = np.arange(n) / SR
rng = np.random.default_rng(7)
out = np.zeros(n)

def env(t0, a, d, length):
    i0 = int(t0 * SR); L = int(length * SR); x = np.arange(L) / SR
    e = np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / d)
    return i0, e

def add(t0, sig):
    i0 = int(t0 * SR); i1 = min(n, i0 + len(sig)); out[i0:i1] += sig[: i1 - i0]

def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")

def noise_hit(t0, dur, dec, k, g):
    _, e = env(t0, .003, dec, dur); add(t0, g * e * lowpass(rng.standard_normal(len(e)), k))

def boom(t0, g=1.0):
    L = int(2.0 * SR); x = np.arange(L) / SR
    f = 70 * np.exp(-x * 1.5) + 30
    add(t0, g * np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-x * 2.2))
    noise_hit(t0, 1.5, .35, 40, .6 * g)

def whoosh(t0, dur, g=.35, rising=True):
    L = int(dur * SR); x = np.arange(L) / L
    e = (x if rising else 1 - x) ** 2 * np.sin(np.pi * x)
    add(t0, g * e * lowpass(rng.standard_normal(L), 12))

def tone(t0, f0, f1, dur, g, dec=.4):
    L = int(dur * SR); x = np.arange(L) / SR
    f = np.linspace(f0, f1, L)
    add(t0, g * np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-x / dec))

# Drone (durchgehend, keine Stille)
drone = .10*np.sin(2*np.pi*55*t) + .07*np.sin(2*np.pi*82.4*t) + .04*np.sin(2*np.pi*110.2*t)
drone *= 0.75 + 0.25*np.sin(2*np.pi*0.18*t)
drone += .02 * lowpass(rng.standard_normal(n), 60)
# Flashback leiser, Ende ausblenden
drone *= np.where((t > C["t_doch"]) & (t < C["t_doch"] + 0.6), 0.2, 1)
drone *= np.clip((T - t) / 1.5, 0, 1)
out += drone

noise_hit(C["t_reisst"], .6, .12, 3, .9)                  # Seil reißt (Snap)
noise_hit(C["t_knall"], 1.2, .25, 10, 1.2); boom(C["t_knall"], .6)  # Knall
L = int(1.0*SR); x = np.arange(L)/SR                       # Licht-Brummen
add(C["t_licht"], .08*np.sign(np.sin(2*np.pi*100*x)) * (np.sin(2*np.pi*9*x) > 0))
whoosh(C["t_hoch"], .5, .4)                                # Sprung
tone(C["t_bringt"], 180, 120, .5, .35, .2)                 # „Fehler“
boom(C["t_doch"], 1.0)                                     # Bass-Hit Wendung
boom(C["t_1945"] + 0.22, .5)                               # Stempel
whoosh(C["t_bomber"] - 0.2, C["t_building"] - C["t_bomber"] + 0.3, .45)  # Flugzeug
boom(C["t_building"] + 0.05, 1.3)                          # Einschlag
noise_hit(C["t_seile1"], .6, .12, 3, .9)                   # Seile durchtrennt
whoosh(C["t_75"] - 0.5, 2.6, .5)                           # Sturz-Wind
for k in range(2):                                         # Herzschlag
    tone(C["t_ueberlebt"] + .1 + k*.8, 60, 45, .25, .9, .08); tone(C["t_ueberlebt"] + .32 + k*.8, 55, 40, .25, .6, .08)
noise_hit(C["t_reissen"], .6, .12, 3, 1.0)                 # alle Seile reißen
whoosh(C["t_kab_f"], 4.0, .55)                             # Fall-Wind
tone(C["t_blockiert"], 900, 600, .2, .5, .05); noise_hit(C["t_blockiert"], .2, .04, 2, .6)  # Klack
L = int(1.2*SR); x = np.arange(L)/SR                        # Kreischen der Keile
add(C["t_keile"], .18*np.sin(2*np.pi*(2400+300*np.sin(2*np.pi*13*x))*x) * np.exp(-x/0.8) * np.minimum(1, x/0.05))
noise_hit(C["t_schienen"], .9, .3, 2, .35)
boom(C["t_fest"], .8)                                      # Stopp
tone(C["t_feder"], 200, 520, .6, .35, .3)                  # Feder-Boing

out = out / np.max(np.abs(out)) * 0.6
pcm = (out * 32767).astype(np.int16)
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok")
