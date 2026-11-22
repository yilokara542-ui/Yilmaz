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
# dunkle Nacht-Drone + leiser Wind
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
def pop_(t0, f=880): tone(t0, f, f*1.5, .12, .08, .06)

def whistle(t0, g=.12, pitch=1.0, echo=False):
    """Kurze 4-Ton-Pfeifmelodie (Sinus + Vibrato + Hauch)."""
    mel = ((1318, .22), (1568, .22), (1175, .22), (1397, .45))
    tt = t0
    for f, d in mel:
        L = int(d*SR); x = np.arange(L)/SR
        fr = f*pitch*(1 + .012*np.sin(2*np.pi*6*x))
        s = np.sin(2*np.pi*np.cumsum(fr)/SR)*np.minimum(1, x/.03)*np.minimum(1, (d-x)/.05)
        s = s*g + .15*g*lp(rng.standard_normal(L), 3)
        if echo:
            s = lp(s, 4)
            for k, a in ((1, .5), (2, .3), (3, .18)):
                add(tt + k*.18, s*a)
        add(tt, s); tt += d + .03
def stamp(t0, g=.9): boom(t0, g*.7); noise(t0, .1, .03, 3, g*.6)
def bell(t0, g=.25):
    for f, a in ((220, 1), (440, .5), (660, .3), (553, .25)):
        tone(t0, f, f, 3.0, g*a, 1.2)
def chirp(t0): tone(t0, 3200, 4200, .08, .05, .04); tone(t0+.1, 3400, 4500, .08, .05, .04)

# Szene A/B: Dämmerung
whoosh(C["t_pf0"]-.1, .4, .25); boom(C["t_pf0"], .35)
whoosh(C["t_schild"]-.3, .4, .2); whoosh(C["t_spiel"]-.25, .4, .2)
for key in ("t_baecker", "t_nachb", "t_buerg"): noise(C[key]+.55, .08, .02, 2, .45); boom(C[key]+.55, .15)
noise(C["t_mund"]+.35, .08, .02, 2, .45); boom(C["t_mund"]+.35, .15)
pop_(C["t_oma"]+.1, 988); noise(C["t_egal"], 1.2, .5, 2, .05)
boom(C["t_pfeif1"], .4)
pop_(C["t_neu"], 1100)
# E: Turmuhr
steps(C["t_also"], C["t_turm"], .32, .15)
bell(C["t_22"], .3); boom(C["t_22"], .6)
# F: du pfeifst – Stille
whistle(C["t_pfeifst"], .13)
for key in ("t_wind", "t_hund", "t_gar"): pop_(C[key], 660)
# G: Antwort aus dem Wald
whistle(C["t_pfeift2"], .09, .97, echo=True); boom(C["t_wald"], .5)
# H: Lichter aus
for k in range(15): click(C["t_ueber"]+.2+k*.07, .18)
tone(C["t_nur"], 330, 330, .8, .06, .5)
# I: rennen, abschließen, Herz, Klopfen
steps(C["t_du_r"], C["t_schliesst"], .16, .22)
click(C["t_ab"], .6); noise(C["t_ab"], .1, .03, 2, .4)
for k in range(10): boom(C["t_herz"]+.2+k*.28, .35)
for k in range(3): knock(C["t_klopft"]+k*.36, 1.0)
# K: Pfeifen vor der Tür
whistle(C["t_pfeift3"], .07, .94, echo=True)
# L: Augen + Grinsen
tone(C["t_gelbe"], 110, 104, 2.5, .12, 1.5); boom(C["t_laecheln"], .5); whoosh(C["t_breit"]-.1, .6, .4); boom(C["t_breit"]+.3, .8)
# M: Morgen – Vögel
for k in range(8): chirp(C["t_am"]+.3+k*.45)
whoosh(C["t_schild2"]-.2, .5, .25)
# N: Stempel
pop_(C["t_name"]-.2, 880); stamp(C["t_gepf"])
# O/P
whistle(C["t_wald2"], .03, .9, echo=True)
whoosh(C["t_denn"]-.2, .5, .3)
def breath(t0, dur=1.6, g=.12):
    L = int(dur*SR); x = np.arange(L)/SR
    add(t0, g*lp(rng.standard_normal(L), 40)*np.sin(np.pi*x/dur)**2*(.6+.4*np.sin(2*np.pi*1.3*x)))
def growl(t0, dur=1.4, g=.18):
    L = int(dur*SR); x = np.arange(L)/SR
    add(t0, g*np.sin(2*np.pi*np.cumsum(55+8*np.sin(2*np.pi*7*x))/SR)*(1+.5*lp(rng.standard_normal(L), 30))*np.sin(np.pi*x/dur))
growl(C["t_wald"], 1.6, .2); breath(C["t_leise"]-.2, 2.0, .1); breath(C["t_gelbe"]-.3, 1.8, .12); growl(C["t_breit"], 1.4, .22)
out = out/np.max(np.abs(out))*.6
with wave.open(os.path.join(HERE, "assets/sfx_bed.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print("ok", T)
