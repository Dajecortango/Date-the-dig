"""Temi musicali di Date the Dignitas, sintetizzati (segnaposto originali).

Leitmotiv per route + tema del calendario e dei finali (musica.rpy, tabella
`musiche` del capitolo). Liuto e bordone additivi; i loop si richiudono senza
giunte perche' le note si avvolgono sul bordo (come make_audio.py).

Uso: py -3 make_musica.py   (richiede numpy e ffmpeg nel PATH)
Scrive game/audio/malandrini/tema_*.ogg. Per sostituirli con musica vera
basta tenere gli stessi nomi (make_musica_elevenlabs.py li genera con
ElevenLabs).
"""

import os
import subprocess
import tempfile
import wave

import numpy as np

from make_audio import SR, secondi, aggiungi, normalizza

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game", "audio")
OUT_MAL = os.path.join(OUT, "malandrini")


def nota_hz(semitoni):
    """Frequenza a `semitoni` da A3 (220 Hz)."""
    return 220.0 * 2 ** (semitoni / 12.0)


def pluck(f, durata, brillanza=1.0):
    """Corda pizzicata: parziali che decadono, le acute prima."""
    t = np.arange(secondi(durata)) / SR
    out = np.zeros_like(t)
    for k, amp in enumerate((1.0, 0.5 * brillanza, 0.28 * brillanza, 0.14 * brillanza)):
        dec = durata * 0.6 / (k + 1)
        out += amp * np.sin(2 * np.pi * f * (k + 1) * t) * np.exp(-t / dec)
    att = max(1, secondi(0.004))
    out[:att] *= np.linspace(0, 1, att)
    return out


def bordone(f, durata):
    """Bordone morbido: due voci leggermente scordate, attacco lento."""
    t = np.arange(secondi(durata)) / SR
    out = (np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 1.003 * t)
           + 0.3 * np.sin(2 * np.pi * f * 2.0 * t))
    inviluppo = np.minimum(1.0, t / 0.8) * np.minimum(1.0, (durata - t) / 1.2)
    return out * inviluppo


# Un tema: scala (semitoni dalla tonica), giro di accordi (gradi della
# scala), motivo (passi di scala sulla melodia, None = pausa), e carattere.
TEMI = {
    # Calendario: dorico sereno, passo tranquillo.
    "calendario": dict(root=5, scala=(0, 2, 3, 5, 7, 9, 10), bpm=84,
                       giro=(0, 5, 3, 4), motivo=(0, 2, 4, 2, 5, 4, 2, None),
                       bri=0.8, basso=0.5, seme=11),
    # Aede: minore armonica, nervosa, note fitte.
    "aede": dict(root=0, scala=(0, 2, 3, 5, 7, 8, 11), bpm=112,
                 giro=(0, 3, 4, 0), motivo=(7, 5, 4, 5, 2, None, 4, 2),
                 bri=1.3, basso=0.6, seme=23),
    # Caino: minore naturale bassa, passo da mercante, solenne.
    "caino": dict(root=-2, scala=(0, 2, 3, 5, 7, 8, 10), bpm=76,
                  giro=(0, 5, 0, 4), motivo=(0, None, 2, 0, 4, None, 2, None),
                  bri=0.7, basso=0.9, seme=37),
    # Druso: maggiore da taverna, saltellante.
    "druso": dict(root=3, scala=(0, 2, 4, 5, 7, 9, 11), bpm=126,
                  giro=(0, 3, 4, 0), motivo=(4, 4, 5, 4, 2, 0, 2, 4),
                  bri=1.1, basso=0.7, seme=41),
    # Icaro: minore sorniona, sincopi e pause.
    "icaro": dict(root=7, scala=(0, 2, 3, 5, 7, 8, 10), bpm=100,
                  giro=(0, 3, 5, 4), motivo=(4, None, 5, 4, None, 2, None, 0),
                  bri=1.0, basso=0.55, seme=53),
    # Ofelia: minore elegante in alto, arpa fitta.
    "ofelia": dict(root=10, scala=(0, 2, 3, 5, 7, 8, 11), bpm=92,
                   giro=(0, 5, 3, 4), motivo=(7, 5, 7, 4, 5, 2, 4, None),
                   bri=0.9, basso=0.4, seme=67),
    # Finali: lento, campane lontane, piu' bordone che melodia.
    "finale": dict(root=0, scala=(0, 2, 3, 5, 7, 8, 10), bpm=60,
                   giro=(0, 3, 5, 0), motivo=(4, None, 2, None, 0, None, None, None),
                   bri=0.6, basso=1.0, seme=79),
    # Menu principale (comune, game/audio/): solenne e paziente, il Nord
    # che aspetta. config.main_menu_music in musica.rpy.
    "menu": dict(root=5, scala=(0, 2, 3, 5, 7, 9, 10), bpm=72,
                 giro=(0, 3, 5, 4), motivo=(4, None, 5, None, 7, None, 4, None),
                 bri=0.7, basso=0.9, seme=97),
}

# Temi comuni a tutto il gioco (gli altri sono di Malandrini).
COMUNI = {"menu"}

BATTUTE = 16          # 4 giri da 4 battute
BEAT_PER_BATTUTA = 4


def grado(spec, g, ottava=0):
    """Frequenza del grado g della scala del tema (g anche oltre 7)."""
    scala = spec["scala"]
    oct_extra, idx = divmod(g, len(scala))
    return nota_hz(spec["root"] + scala[idx] + 12 * (ottava + oct_extra))


def tema(spec):
    rng = np.random.default_rng(spec["seme"])
    spb = 60.0 / spec["bpm"]
    n = secondi(BATTUTE * BEAT_PER_BATTUTA * spb)
    x = np.zeros(n)
    for b in range(BATTUTE):
        acc = spec["giro"][b % len(spec["giro"])]
        t0 = b * BEAT_PER_BATTUTA * spb
        # Bordone/basso sulla fondamentale dell'accordo.
        f_basso = grado(spec, acc, ottava=-1)
        aggiungi(x, spec["basso"] * 0.4 * bordone(f_basso, BEAT_PER_BATTUTA * spb),
                 secondi(t0))
        # Arpeggio dell'accordo (fondamentale, terza, quinta) sui beat.
        for k in range(BEAT_PER_BATTUTA):
            g_arp = acc + (0, 2, 4, 2)[k]
            amp = 0.22 if k else 0.3
            aggiungi(x, amp * pluck(grado(spec, g_arp), spb * 1.8, spec["bri"]),
                     secondi(t0 + k * spb))
        # Melodia: il motivo sugli ottavi, trasposto sull'accordo; nelle
        # battute pari sale di poco (variazione deterministica ma viva).
        for k, passo in enumerate(spec["motivo"]):
            if passo is None:
                continue
            g_mel = acc + passo + (1 if b % 4 == 2 and k < 4 else 0)
            amp = 0.30 + 0.06 * float(rng.uniform(-1, 1))
            aggiungi(x, amp * pluck(grado(spec, g_mel, ottava=1),
                                    spb * 1.2, spec["bri"]),
                     secondi(t0 + k * spb / 2.0))
    return normalizza(x, 0.3)


def salva_tema(nome, x, cartella=None):
    cartella = cartella or OUT_MAL
    os.makedirs(cartella, exist_ok=True)
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, nome + ".wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav,
                        "-c:a", "libvorbis", "-q:a", "4",
                        os.path.join(cartella, nome + ".ogg")], check=True)
    print(os.path.relpath(os.path.join(cartella, nome + ".ogg"), OUT))


def main():
    for nome, spec in TEMI.items():
        salva_tema("tema_" + nome, tema(spec),
                   OUT if nome in COMUNI else OUT_MAL)


if __name__ == "__main__":
    main()
