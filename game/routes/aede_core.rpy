# Route Aede — personaggi, variabili, utilità.

init python:
    def sanitize_name(raw):
        """Nome giocatore: strip, niente tag/interpolazioni, default Elio."""
        if raw is None:
            raw = ""
        for ch in "{}[]":
            raw = raw.replace(ch, "")
        raw = raw.strip()
        if not raw:
            raw = "Elio"
        return raw

## Personaggi #################################################################

define aede = Character("Aede", color="#c0392b")
define glauco = Character("Glauco Severo", color="#6b6b6b")
define briseide = Character("Briseide Ippodamia", color="#b8860b")
define pc = Character("[player_name]", color="#f0e6d2")

# Fratelli di Ceppo del protagonista (Ceppo di Briseide Ippodamia).
define vanna = Character("Vanna", color="#8fbc8f")
define corrado = Character("Corrado", color="#87a7c7")

## Variabili di route #########################################################

default player_name = "Elio"
default aede_affinity = 0
default flag_segreto_svelo = False
default flag_accetta_lavoro = False
default flag_giuramento = False
