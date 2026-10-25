"""Versioni vere di temi ed effetti con ElevenLabs (al posto dei segnaposto).

Richiede la chiave API: se ELEVENLABS_API_KEY non e' impostata, fare prima
    npx -y @elevenlabs/cli@latest onboard init
dalla cartella del progetto (login guidato, salva la chiave), poi:
    py -3 -m pip install elevenlabs
    py -3 make_musica_elevenlabs.py            # tutto
    py -3 make_musica_elevenlabs.py temi       # solo i 7 temi musicali
    py -3 make_musica_elevenlabs.py effetti    # solo gli effetti

Scrive gli stessi nomi file dei segnaposto (game/audio/...): il gioco non
cambia. Serve ffmpeg nel PATH per la conversione in ogg.
"""

import os
import subprocess
import sys
import tempfile

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game", "audio")
OUT_MAL = os.path.join(OUT, "malandrini")

# Leitmotiv (musica.rpy): prompt per il modello music_v2_5. Strumentazione
# coerente: mondo tardo-medievale/rinascimentale del Nord, niente orchestra
# moderna, niente batteria.
TEMI = {
    "tema_calendario": (
        "Calm renaissance lute and soft low strings, gentle 84 bpm, warm and "
        "patient, winter court daily life, instrumental, loopable background "
        "for a visual novel planner screen, no percussion, no vocals"),
    "tema_aede": (
        "Fiery renaissance theme for a proud red-haired duelist: nervous lute "
        "arpeggios in harmonic minor, urgent bowed strings, 112 bpm, guarded "
        "passion under cold discipline, instrumental, loopable, no drums"),
    "tema_caino": (
        "Low solemn renaissance theme for a shrewd merchant lord: slow dark "
        "viols and sparse plucked bass in minor, 76 bpm, weight of ledgers "
        "and old money, instrumental, loopable, no percussion, no vocals"),
    "tema_druso": (
        "Cheerful tavern theme: bouncy lute and hand drum, major key, 126 "
        "bpm, ale and arm-wrestling, renaissance folk dance, instrumental, "
        "loopable, rustic and warm"),
    "tema_icaro": (
        "Sly smoky theme for a charming gambler: syncopated plucked lute in "
        "minor, lazy pauses, 100 bpm, smoke den and marked cards, "
        "renaissance, instrumental, loopable, no vocals"),
    "tema_ofelia": (
        "Elegant dangerous theme for a beautiful noblewoman: high harp "
        "arpeggios in minor, cold sustained strings underneath, 92 bpm, "
        "greenhouse roses with thorns, instrumental, loopable, no vocals"),
    "tema_finale": (
        "Slow solemn ending theme: distant bells, long low drone, sparse "
        "minor melody on a single string instrument, 60 bpm, snow at dusk, "
        "bittersweet resolution, instrumental, loopable, no percussion"),
    "tema_menu": (
        "Main menu theme for a dark political romance visual novel: patient "
        "solemn renaissance lute over a warm low drone, 72 bpm, northern "
        "winter court, inviting but guarded, instrumental, loopable, no "
        "percussion, no vocals"),
}
TEMI_MS = 90000
# Temi comuni (game/audio/); gli altri in game/audio/malandrini/.
TEMI_COMUNI = {"tema_menu"}

# Effetti (make_audio.py): nome file -> (prompt, durata s, loop).
EFFETTI = {
    "moneta": ("Three silver coins dropped one after another on a wooden "
               "counter, short bright jingle", 1.0, False),
    "lama": ("A sword drawn slowly from a metal scabbard, long cold ring of "
             "steel", 1.5, False),
    "colpo": ("A heavy dull body blow, close and dry, cloth and muscle, "
              "short thud", 0.6, False),
    "carta": ("A parchment scroll unrolled quickly on a table, dry paper "
              "rustle", 0.6, False),
    "sigillo": ("A wax seal stamped firmly onto parchment, soft deep thump",
                0.5, False),
    "scelta": ("Very soft short UI tick, muted wooden click, subtle", 0.5, False),
    "affetto_su": ("Two soft ascending plucked harp notes, warm and "
                   "intimate, short musical sting", 0.8, False),
    "affetto_giu": ("Two soft descending muted lute notes, sad and "
                    "restrained, short musical sting", 0.9, False),
    "campana": ("A single large bronze church bell toll, long natural "
                "decay, distant and cold", 5.0, False),
    "clessidra": ("Fine sand trickling inside an hourglass with a single "
                  "soft wooden tap, short, intimate", 0.9, False),
    "finale_sbloccato": ("Three ascending bright bronze bell notes, solemn "
                         "achievement fanfare, renaissance, short", 3.0, False),
}


def ogg(dati_mp3, destinazione):
    os.makedirs(os.path.dirname(destinazione), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        mp3 = os.path.join(tmp, "in.mp3")
        with open(mp3, "wb") as f:
            f.write(dati_mp3)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3,
                        "-c:a", "libvorbis", "-q:a", "4", destinazione],
                       check=True)
    print(os.path.relpath(destinazione, OUT))


def main():
    if not os.environ.get("ELEVENLABS_API_KEY"):
        sys.exit("ELEVENLABS_API_KEY mancante: npx -y @elevenlabs/cli@latest onboard init")
    from elevenlabs import ElevenLabs
    client = ElevenLabs()
    cosa = sys.argv[1] if len(sys.argv) > 1 else "tutto"

    if cosa in ("tutto", "temi"):
        for nome, prompt in TEMI.items():
            audio = client.music.compose(prompt=prompt,
                                         music_length_ms=TEMI_MS,
                                         model_id="music_v2_5")
            cartella = OUT if nome in TEMI_COMUNI else OUT_MAL
            ogg(b"".join(audio), os.path.join(cartella, nome + ".ogg"))

    if cosa in ("tutto", "effetti"):
        for nome, (prompt, durata, loop) in EFFETTI.items():
            audio = client.text_to_sound_effects.convert(
                text=prompt, duration_seconds=durata,
                prompt_influence=0.6, loop=loop)
            cartella = OUT_MAL if nome == "campana" else OUT
            ogg(b"".join(audio), os.path.join(cartella, nome + ".ogg"))


if __name__ == "__main__":
    main()
