# Video 08 – „Was passiert, wenn das Seil deines Aufzugs reißt?“

HyperFrames-Projekt, 1080×1920 (9:16), 60 fps, 80,9 s. Fertiges Video: `../08_Aufzugseil_final.mp4`.

## Neu bauen
```bash
python3 build.py      # index.html aus assets/words.json (wortgenaue Voiceover-Zeitstempel)
python3 make_sfx.py   # assets/sfx_bed.wav (Drone + Soundeffekte an den Cues)
npx hyperframes check
npx hyperframes render --fps 60 -o render.mp4
ffmpeg -i render.mp4 -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -movflags +faststart -af loudnorm=I=-12.5:TP=-1.0:LRA=11 -c:a aac -b:a 192k ../08_Aufzugseil_final.mp4
```

- `assets/voiceover.mp3` – ElevenLabs, Stimme „Mark - Natural Conversations“
- `assets/words.json` – Wort-Zeitstempel (ElevenLabs Scribe)
- `assets/cues.json` – Startzeiten der Schlüsselwörter, an denen Szenen/Effekte hängen
