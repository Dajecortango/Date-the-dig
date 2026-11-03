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

# Leitmotiv (musica.rpy): piani di composizione per music_v2_5. Musica di corte
# e di strada del Cinquecento italiano: danze vere, modi antichi, strumenti
# d'epoca suonati da piu' voci. Niente fantasy epico, niente celtico.
ESCLUSI = ["synthesizer", "electronic", "drum kit", "modern orchestra",
           "epic trailer", "cinematic hybrid", "celtic", "new age pads",
           "piano", "electric guitar", "lo-fi", "reverb wash"]
EPOCA = ["16th century Italian Renaissance", "historically informed performance",
         "acoustic period instruments", "real ensemble playing together",
         "natural room acoustics", "instrumental"]


def piano(stile, *sezioni):
    """Piano di composizione: stile comune piu' (titolo, secondi, istruzioni)."""
    chunks = []
    for i, (titolo, secondi, nota) in enumerate(sezioni):
        chunks.append({
            "text": "[%s]\n%s" % (titolo, nota),
            "duration_ms": secondi * 1000,
            "positive_styles": (EPOCA + stile) if i == 0 else stile,
            "negative_styles": ESCLUSI,
            "context_adherence": "high",
        })
    return {"chunks": chunks}


TEMI = {
    "tema_menu": piano(
        ["solemn intrada", "cornetts and sackbuts in five parts", "positive organ",
         "stately 4/4", "Dorian mode"],
        ("Intrada", 40, "Slow ceremonial entrance, cornetts answered by sackbuts."),
        ("Second strain", 45, "Imitative counterpoint between the voices, organ underneath."),
        ("Quiet strain", 40, "Only two sackbuts and organ, guarded and wintry."),
        ("Return", 45, "All voices return with the opening strain, no big ending.")),
    "tema_calendario": piano(
        ["passamezzo antico", "Renaissance lute", "alto recorder", "bass viola da gamba",
         "unhurried", "warm and patient", "Dorian mode"],
        ("Passamezzo", 50, "Lute plays the ground with divisions, viol on the bass."),
        ("Variation", 50, "Recorder takes the melody with light ornaments."),
        ("Saltarello strain", 40, "Same harmony in lilting triple time, still quiet."),
        ("Return", 40, "Lute alone, then viol rejoins.")),
    "tema_aede": piano(
        ["galliard in triple time", "viol consort", "tenor viol lead", "light tabor",
         "nervous and proud", "Phrygian mode", "tight counterpoint"],
        ("Strain A", 35, "Quick dotted galliard rhythm, viols chase each other."),
        ("Strain A repeat", 30, "Same strain with ornamented divisions on the tenor viol."),
        ("Strain B", 40, "Tension rises, the tabor drops out, short sharp bowing."),
        ("Strain C", 35, "A brief tender phrase for a single viol, quickly cut off."),
        ("Strain A return", 30, "Full consort, controlled and cold.")),
    "tema_caino": piano(
        ["slow pavane in duple time", "consort of viols", "regal organ",
         "measured and grave", "Aeolian mode", "rich inner voices"],
        ("Pavane strain A", 50, "Long even phrases, bass viol walking under the consort."),
        ("Strain B", 50, "Suspensions pile up slowly, regal doubles the bass."),
        ("Strain C", 40, "Thinner texture, treble viol alone over a held bass."),
        ("Return", 40, "Opening strain, fuller, ends on an open fifth.")),
    "tema_druso": piano(
        ["saltarello", "fast compound time", "shawms", "hurdy-gurdy", "bagpipe drone",
         "tambourine", "rowdy tavern dance", "Mixolydian mode"],
        ("Saltarello", 30, "Shawm over bagpipe drone, tambourine on the off-beats."),
        ("Second strain", 30, "Hurdy-gurdy answers with buzzing rhythm."),
        ("Drunken break", 25, "Everything drops except tambourine and one rude shawm."),
        ("Second dance", 40, "New tune, faster, players stumbling and catching up."),
        ("Return", 35, "All together, loud and rough, a little out of step.")),
    "tema_icaro": piano(
        ["solo Renaissance lute ricercar", "sparse", "long silences between phrases",
         "free rhythm", "sly and unhurried", "Phrygian mode", "occasional bass viol note"],
        ("Ricercar", 55, "Lute alone, a phrase is posed and left hanging."),
        ("Imitation", 50, "The phrase returns in another voice, with a chromatic slip."),
        ("Viol", 35, "A few low viol notes under quiet lute."),
        ("Return", 40, "Lute alone, ending on an unresolved note.")),
    "tema_ofelia": piano(
        ["elegant court basse danse", "Renaissance double harp", "virginal", "treble viol",
         "poised and cold", "Dorian mode", "refined ornaments"],
        ("Basse danse", 45, "Harp alone, slow gliding steps, very clear."),
        ("Second strain", 45, "Virginal joins with fine ornaments."),
        ("Treble viol", 45, "Long cool melody on the treble viol over plucked strings."),
        ("Return", 45, "Harp and virginal together, perfect and without warmth.")),
    "tema_finale": piano(
        ["slow motet", "wordless a cappella choir in four parts", "viols doubling the voices",
         "sacred polyphony", "bittersweet", "Aeolian mode", "very slow"],
        ("Motet", 55, "Voices enter one after another in imitation, no text."),
        ("Second section", 55, "Long suspensions, viols support the lower voices."),
        ("Thin section", 35, "Two voices alone."),
        ("Close", 40, "All voices, settling on an open chord.")),
}
# Temi comuni (game/audio/); gli altri in game/audio/malandrini/.
TEMI_COMUNI = {"tema_menu"}
# Secondi di dissolvenza con cui la coda si richiude sull'inizio del loop.
LOOP_DISSOLVENZA = 5.0
# Originali generati (mp3): rifare il loop non costa una nuova generazione.
GREZZI = os.environ.get("MUSICA_GREZZI") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_grezzo")

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


def durata(percorso):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", percorso], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def ogg_loop(mp3, destinazione):
    """Ogg che si richiude senza giunta: la coda sfuma nell'inizio del brano e
    il file riparte subito dopo quella dissolvenza. Volume uniforme tra i temi."""
    os.makedirs(os.path.dirname(destinazione), exist_ok=True)
    fine = durata(mp3)
    d = LOOP_DISSOLVENZA
    filtro = (
        "[0:a]asplit=3[a][b][c];"
        "[a]atrim=%.3f:%.3f,asetpts=PTS-STARTPTS[corpo];"
        "[b]atrim=%.3f:%.3f,asetpts=PTS-STARTPTS[coda];"
        "[c]atrim=0:%.3f,asetpts=PTS-STARTPTS[testa];"
        "[coda][testa]acrossfade=d=%.3f:c1=tri:c2=tri[giunta];"
        "[corpo][giunta]concat=n=2:v=0:a=1,loudnorm=I=-18:TP=-1.5:LRA=11[out]"
    ) % (d, fine - d, fine - d, fine, d, d)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-filter_complex", filtro,
                    "-map", "[out]", "-ar", "48000", "-c:a", "libvorbis", "-q:a", "5", destinazione],
                   check=True)
    print(os.path.relpath(destinazione, OUT))


def carica_env():
    """Legge ELEVENLABS_API_KEY dal .env del progetto, se non e' gia' impostata."""
    percorso = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.environ.get("ELEVENLABS_API_KEY") or not os.path.exists(percorso):
        return
    with open(percorso, encoding="utf-8") as f:
        for riga in f:
            nome, _, valore = riga.strip().partition("=")
            if nome == "ELEVENLABS_API_KEY":
                os.environ[nome] = valore.strip().strip("\"'")


def main():
    carica_env()
    if not os.environ.get("ELEVENLABS_API_KEY"):
        sys.exit("ELEVENLABS_API_KEY mancante: npx -y @elevenlabs/cli@latest onboard init")
    from elevenlabs import ElevenLabs
    client = ElevenLabs()
    cosa = sys.argv[1] if len(sys.argv) > 1 else "tutto"
    # Un secondo argomento limita i temi: make_musica_elevenlabs.py temi tema_druso
    solo = set(sys.argv[2:])

    if cosa in ("tutto", "temi"):
        os.makedirs(GREZZI, exist_ok=True)
        for nome, plan in TEMI.items():
            if solo and nome not in solo:
                continue
            grezzo = os.path.join(GREZZI, nome + ".mp3")
            if not os.path.exists(grezzo):
                audio = client.music.compose(composition_plan=plan,
                                             model_id="music_v2_5",
                                             output_format="mp3_48000_192")
                with open(grezzo, "wb") as f:
                    f.write(b"".join(audio))
            cartella = OUT if nome in TEMI_COMUNI else OUT_MAL
            ogg_loop(grezzo, os.path.join(cartella, nome + ".ogg"))

    if cosa in ("tutto", "effetti"):
        for nome, (prompt, durata, loop) in EFFETTI.items():
            audio = client.text_to_sound_effects.convert(
                text=prompt, duration_seconds=durata,
                prompt_influence=0.6, loop=loop)
            cartella = OUT_MAL if nome == "campana" else OUT
            ogg(b"".join(audio), os.path.join(cartella, nome + ".ogg"))


if __name__ == "__main__":
    main()
