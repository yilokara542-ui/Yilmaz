# Video 10 – „Könnte jemand jahrelang heimlich in deinem Haus leben?“ (Format A „Erklär-Story“)

HyperFrames-Projekt, 1080×1920 (9:16), 60 fps. Skript: `../../10_Skript_Heimlicher-Mitbewohner.md`.

```bash
python3 align.py      # assets/words.json aus Sprechpausen von assets/voiceover.mp3 + script.txt
python3 build.py      # index.html
python3 make_sfx.py   # assets/sfx_bed.wav
npx hyperframes render --fps 60 -o render.mp4
ffmpeg -i render.mp4 -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -movflags +faststart -af loudnorm=I=-12.5:TP=-1.0:LRA=11 -c:a aac -b:a 192k ../10_Mitbewohner_final.mp4
```
