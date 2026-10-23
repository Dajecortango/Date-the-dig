"""Effetti e ambienti di Date the Dignitas, sintetizzati (segnaposto originali).

Rumori modellati in frequenza (FFT): il segnale e' circolare, quindi i loop
d'ambiente si richiudono senza giunte. Eventi sparsi (scoppiettii, campane)
si avvolgono sul bordo per la stessa ragione.

Uso: py -3 make_audio.py   (richiede numpy e ffmpeg nel PATH)
Scrive game/audio/*.ogg. Per sostituirli con registrazioni vere basta
tenere gli stessi nomi.
"""

import os
import subprocess
import tempfile
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "game", "audio")
# Ambienti e campana sono di Malandrini: audio/malandrini/. Il resto e' comune.
OUT_MAL = os.path.join(OUT, "malandrini")
SR = 32000
rng = np.random.default_rng(1792)


def secondi(n):
    return int(SR * n)


def rumore_forma(n, forma):
    """Rumore bianco filtrato in frequenza: forma(f) -> guadagno."""
    spettro = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1.0 / SR)
    g = forma(np.maximum(f, 1.0))
    out = np.fft.irfft(spettro * g, n)
    return out / (np.max(np.abs(out)) + 1e-9)


def banda(lo, hi, pendenza=1.0):
    def forma(f):
        g = np.where((f >= lo) & (f <= hi), 1.0, 0.0)
        # bordi morbidi
        g = g + np.exp(-((f - lo) / (lo * 0.35)) ** 2) * (f < lo)
        g = g + np.exp(-((f - hi) / (hi * 0.35)) ** 2) * (f > hi)
        return g / f ** (0.5 * pendenza)
    return forma


def inviluppo_lento(n, hz_max):
    """Inviluppo casuale lento, circolare, in [0, 1]."""
    e = rumore_forma(n, lambda f: np.where(f <= hz_max, 1.0, 0.0))
    e = (e - e.min()) / (e.max() - e.min() + 1e-9)
    return e


def aggiungi(buf, suono, pos):
    """Somma suono a buf da pos, avvolgendo sul bordo (loop)."""
    n = len(buf)
    idx = (np.arange(len(suono)) + pos) % n
    np.add.at(buf, idx, suono)


def parziali(freqs, durata, decadimenti, ampiezze=None):
    t = np.arange(secondi(durata)) / SR
    out = np.zeros_like(t)
    ampiezze = ampiezze or [1.0] * len(freqs)
    for f, d, a in zip(freqs, decadimenti, ampiezze):
        out += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / d)
    return out


def dissolvenza(x, att=0.004, rel=0.02):
    n = len(x)
    a, r = max(1, secondi(att)), max(1, secondi(rel))
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a)
    env[-r:] = np.linspace(1, 0, r)
    return x * env


def normalizza(x, picco):
    return x / (np.max(np.abs(x)) + 1e-9) * picco


def salva(nome, x):
    cartella = OUT_MAL if nome.startswith("amb_") or nome == "campana" else OUT
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
                        "-c:a", "libvorbis", "-q:a", "3",
                        os.path.join(cartella, nome + ".ogg")], check=True)
    print(os.path.relpath(os.path.join(cartella, nome + ".ogg"), OUT))


# --- Effetti ----------------------------------------------------------------

def moneta():
    x = np.zeros(secondi(0.6))
    for k, ritardo in enumerate((0.0, 0.09, 0.16)):
        tintinnio = parziali([2350 + 90 * k, 3120, 4410 - 60 * k, 6230],
                             0.35, [0.18, 0.12, 0.08, 0.05], [1, 0.7, 0.5, 0.3])
        tintinnio = dissolvenza(tintinnio * (0.9 - 0.25 * k), rel=0.05)
        aggiungi(x, tintinnio[:len(x)], secondi(ritardo))
    return normalizza(dissolvenza(x, rel=0.08), 0.6)


def lama():
    n = secondi(1.2)
    t = np.arange(n) / SR
    graffio = rumore_forma(n, banda(2500, 9000)) * np.exp(-t / 0.05)
    canto = parziali([1840, 2710, 3960, 5280], 1.2, [0.6, 0.45, 0.3, 0.2], [1, 0.6, 0.4, 0.25])
    canto *= 1 + 0.15 * np.sin(2 * np.pi * 6 * t)
    return normalizza(dissolvenza(0.8 * graffio + 0.6 * canto, rel=0.2), 0.55)


def colpo():
    n = secondi(0.45)
    t = np.arange(n) / SR
    freq = 95 * np.exp(-t / 0.12) + 45
    tonfo = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-t / 0.11)
    polvere = rumore_forma(n, banda(80, 900)) * np.exp(-t / 0.04)
    return normalizza(dissolvenza(tonfo + 0.5 * polvere, rel=0.08), 0.8)


def campana(durata=4.0, fondamentale=392.0):
    rapporti = [0.5, 1.0, 1.19, 1.5, 2.0, 2.52, 3.0]
    decad = [3.0, 2.2, 1.6, 1.3, 1.0, 0.7, 0.5]
    amp = [0.5, 1.0, 0.6, 0.45, 0.35, 0.25, 0.15]
    x = parziali([fondamentale * r for r in rapporti], durata, decad, amp)
    return dissolvenza(x, att=0.002, rel=0.3)


# --- Ambienti (loop) --------------------------------------------------------

LOOP = 24.0


def amb_camino():
    n = secondi(LOOP)
    rombo = rumore_forma(n, banda(40, 400, 2.0)) * (0.7 + 0.3 * inviluppo_lento(n, 0.4))
    x = 0.5 * rombo
    t = np.arange(secondi(0.03)) / SR
    for _ in range(int(LOOP * 7)):
        click = rumore_forma(len(t), banda(1500, 7000)) * np.exp(-t / 0.006)
        aggiungi(x, click * rng.uniform(0.15, 0.6), rng.integers(0, n))
    return normalizza(x, 0.35)


def vento(n):
    raffiche = 0.35 + 0.65 * inviluppo_lento(n, 0.15)
    sibilo = rumore_forma(n, banda(150, 1400, 1.5))
    return sibilo * raffiche


def amb_vento():
    return normalizza(vento(secondi(LOOP)), 0.35)


def amb_cala():
    n = secondi(LOOP)
    x = 0.8 * normalizza(vento(n), 1.0)
    for pos, f in ((1.5, 392.0), (9.0, 349.2), (16.5, 293.7)):
        aggiungi(x, 0.35 * campana(5.0, f), secondi(pos))
    return normalizza(x, 0.35)


def brusio(n, voci, livello_mod):
    x = np.zeros(n)
    for _ in range(voci):
        centro = rng.uniform(300, 1100)
        voce = rumore_forma(n, banda(centro * 0.7, centro * 1.6))
        sillabe = inviluppo_lento(n, rng.uniform(3, 6)) ** 2
        presenza = inviluppo_lento(n, 0.2)
        x += voce * sillabe * (0.3 + livello_mod * presenza)
    return x


def amb_strada():
    n = secondi(LOOP)
    x = 0.6 * normalizza(brusio(n, 8, 0.7), 1.0) + 0.3 * normalizza(vento(n), 1.0)
    return normalizza(x, 0.3)


def amb_sala():
    n = secondi(LOOP)
    fondo = rumore_forma(n, banda(30, 250, 2.0))
    x = 0.6 * fondo + 0.35 * normalizza(brusio(n, 5, 0.4), 1.0)
    return normalizza(x, 0.25)


def amb_folla():
    n = secondi(LOOP)
    onde = 0.5 + 0.5 * inviluppo_lento(n, 0.25)
    x = normalizza(brusio(n, 18, 1.0), 1.0) * onde
    return normalizza(x, 0.35)


def scelta():
    """Tic morbido dell'hover sulle scelte (~60 ms)."""
    n = secondi(0.08)
    t = np.arange(n) / SR
    tic = parziali([1320, 2210], 0.08, [0.025, 0.018], [1, 0.4])
    tic += 0.3 * rumore_forma(n, banda(2000, 6000)) * np.exp(-t / 0.006)
    return normalizza(dissolvenza(tic, rel=0.02), 0.25)


def carta():
    """Fruscio di pergamena che si srotola (~0.4 s)."""
    n = secondi(0.45)
    t = np.arange(n) / SR
    fruscio = rumore_forma(n, banda(900, 7000)) * inviluppo_lento(n, 30)
    fruscio *= np.minimum(1.0, t / 0.05) * np.exp(-t / 0.25)
    return normalizza(dissolvenza(fruscio, rel=0.08), 0.4)


def sigillo():
    """Tonfo sordo del sigillo di ceralacca (~0.25 s)."""
    n = secondi(0.28)
    t = np.arange(n) / SR
    freq = 160 * np.exp(-t / 0.05) + 70
    tonfo = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-t / 0.06)
    cera = rumore_forma(n, banda(200, 1800)) * np.exp(-t / 0.02)
    return normalizza(dissolvenza(tonfo + 0.35 * cera, rel=0.05), 0.6)


def affetto_su():
    """Due note morbide che salgono (toast ▲, ~0.35 s)."""
    x = np.zeros(secondi(0.4))
    for k, (f, ritardo) in enumerate(((660, 0.0), (880, 0.09))):
        nota = parziali([f, 2 * f], 0.3, [0.12, 0.06], [1, 0.25])
        aggiungi(x, dissolvenza(nota * (0.8 + 0.2 * k), rel=0.05), secondi(ritardo))
    return normalizza(dissolvenza(x, rel=0.08), 0.22)


def affetto_giu():
    """Nota grave smorzata che cala (toast ▼, ~0.4 s)."""
    n = secondi(0.4)
    t = np.arange(n) / SR
    freq = 330 - 60 * np.minimum(1.0, t / 0.3)
    nota = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-t / 0.14)
    return normalizza(dissolvenza(nota, rel=0.08), 0.22)


def amb_pioggia():
    """Pioggia sui vicoli: fruscio largo + gocce sparse, in loop."""
    n = secondi(LOOP)
    x = 0.6 * rumore_forma(n, banda(400, 9000, 0.6)) * (0.8 + 0.2 * inviluppo_lento(n, 0.3))
    for pos in rng.integers(0, n, int(22 * LOOP)):
        m = secondi(0.03)
        goccia = rumore_forma(m, banda(2500, 8000)) * np.exp(-np.arange(m) / SR / 0.006)
        aggiungi(x, 0.5 * goccia, int(pos))
    return normalizza(x, 0.35)


def main():
    salva("scelta", scelta())
    salva("carta", carta())
    salva("sigillo", sigillo())
    salva("amb_pioggia", amb_pioggia())
    salva("moneta", moneta())
    salva("lama", lama())
    salva("colpo", colpo())
    salva("campana", normalizza(campana(), 0.5))
    salva("amb_camino", amb_camino())
    salva("amb_vento", amb_vento())
    salva("amb_cala", amb_cala())
    salva("amb_strada", amb_strada())
    salva("amb_sala", amb_sala())
    salva("amb_folla", amb_folla())


if __name__ == "__main__":
    main()
