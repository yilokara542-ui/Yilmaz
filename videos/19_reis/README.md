# Video 09 – „HEIMWEG · Teil 1“ (Format B „Regel-Serie“)

HyperFrames-Projekt, 1080×1920 (9:16), 60 fps. Skript: `../../09_Skript_Heimweg-Teil-1.md`.

```bash
python3 build.py      # index.html aus assets/words.json (Wort-Zeitstempel des Voiceovers)
python3 make_sfx.py   # assets/sfx_bed.wav an den Cues
npx hyperframes render --fps 60 -o render.mp4
ffmpeg -i render.mp4 -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -movflags +faststart -af loudnorm=I=-12.5:TP=-1.0:LRA=11 -c:a aac -b:a 192k ../09_Heimweg_Teil1_final.mp4
```
