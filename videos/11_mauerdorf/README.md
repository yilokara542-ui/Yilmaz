# Video 11 – „Die Welt hinter den Mauern“ (eigene Welt, Mitmach-Video)

HyperFrames-Projekt, 1080×1920 (9:16). Skript: `../../11_Skript_Mauerdorf.md`, Sprechertext: `script.txt`.
Alle Figuren, Riesen, Jäger, Wappen und Orte sind eigene Entwürfe.

**Status:** Fertig – Voiceover ElevenLabs „Mark - Natural Conversations“ (73,2 s).

Sobald das echte Voiceover da ist (Datei nach `assets/voiceover.mp3`):
```bash
python3 align.py && python3 build.py && python3 make_sfx.py
npx hyperframes render --fps 60 -o render.mp4
ffmpeg -i render.mp4 -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -movflags +faststart -af loudnorm=I=-12.5:TP=-1.0:LRA=11 -c:a aac -b:a 192k ../11_Mauerdorf_final.mp4
```
