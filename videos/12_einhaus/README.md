# Video 12 – „In diesem Haus lebt nur eine einzige Person – ich. Zumindest jetzt noch.“

HyperFrames-Projekt, 1080×1920 (9:16), 60 fps. Skript: `../../12_Skript_Ein-Haus.md`, Sprechertext: `script.txt`.

```bash
python3 align.py && python3 build.py && python3 make_sfx.py
npx hyperframes render --fps 60 -o render.mp4
ffmpeg -i render.mp4 -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -movflags +faststart -af loudnorm=I=-12.5:TP=-1.0:LRA=11 -c:a aac -b:a 192k ../12_EinHaus_final.mp4
```
