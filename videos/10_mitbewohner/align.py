#!/usr/bin/env python3
"""Wort-Zeitstempel ohne Transkriptions-Dienst: Sprechpausen messen, Phrasen per DP auf Pausen legen,
Wörter innerhalb einer Phrase nach Silbenlänge verteilen. → assets/words.json"""
import json, re, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
txt = open(os.path.join(HERE, "script.txt"), encoding="utf-8").read()
# Phrasen = an . ? ! : , getrennt
phr = [p.strip() for p in re.findall(r"[^.?!:]+[.?!:]?", txt.replace("\n", " ")) if p.strip() and re.search(r"\w", p)]
o = subprocess.run(["ffmpeg", "-i", os.path.join(HERE, "assets/voiceover.mp3"), "-af", "silencedetect=n=-40dB:d=0.09", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", o)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", o)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(HERE, "assets/voiceover.mp3")], capture_output=True, text=True).stdout)
sil = [(a, b) for a, b in zip(st, en) if a > 0.05]
lead = en[0] if st and st[0] < 0.05 else 0.0
B = [lead] + [b for a, b in sil]; E = [a for a, b in sil] + [dur]
def syl(s): return max(1, len(re.findall(r"[aeiouäöüy]+", s.lower())))
L = [syl(p) for p in phr]; n, m = len(phr), len(B)
best = None
for rate in [x / 1000 for x in range(150, 260, 4)]:
    INF = 1e9; dp = [[INF]*(m+1) for _ in range(n+1)]; bk = [[0]*(m+1) for _ in range(n+1)]; dp[0][0] = 0
    for i in range(n):
        for j in range(m):
            if dp[i][j] >= INF: continue
            for k in range(j+1, min(m, j+6)+1):
                s0 = B[j]; e0 = E[k-1]
                ins = [(a, b) for a, b in sil if s0 < a < e0 - 0.01]
                sp = e0 - s0 - sum(b - a for a, b in ins)
                c = (sp - rate * L[i]) ** 2 + 0.5 * len(ins)
                if dp[i][j] + c < dp[i+1][k]: dp[i+1][k] = dp[i][j] + c; bk[i+1][k] = j
    if best is None or dp[n][m] < best[0]:
        k = m; path = []
        for i in range(n, 0, -1): j = bk[i][k]; path.append((j, k)); k = j
        best = (dp[n][m], rate, path[::-1])
words = []
for (j, k), p in zip(best[2], phr):
    s0, e0 = B[j], E[k-1]; ws_ = p.split(); tot = sum(syl(w) for w in ws_); t = s0
    for w in ws_:
        d = (e0 - s0) * syl(w) / tot; words.append({"t": w, "s": round(t, 3), "e": round(t + d, 3)}); t += d
json.dump(words, open(os.path.join(HERE, "assets/words.json"), "w"), ensure_ascii=False)
print("rate", best[1], "cost", round(best[0], 2), "phrases", n, "pauses", m)
for (j, k), p in zip(best[2], phr): print(f"{B[j]:6.2f}-{E[k-1]:6.2f}  {p}")
