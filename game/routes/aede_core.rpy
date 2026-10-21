# Route Aede — "Tempesta d'amore". Personaggi, variabili, utilità.
# Aede: figlia di Glauco, sorella di Ofelia e Ascadeo. Difficoltà 3/5.
# Niente poliamore: la scelta del cuore chiude le altre route.

init python:
    def set_gender(g):
        """Imposta genere del protagonista e tutte le varianti di testo."""
        store.player_gender = g
        if g == "f":
            store.fin = "a"; store.figlio_t = "Figlia"
            store.fratello_t = "sorellina"; store.il_fratello_t = "la sorellina"
            store.uomo_t = "donna"; store.un_t = "una"; store.Un_t = "Una"
            store.il_t = "la"; store.Il_t = "La"; store.al_t = "alla"
            store.gli_t = "le"; store.lui_t = "lei"
        else:
            store.fin = "o"; store.figlio_t = "Figlio"
            store.fratello_t = "fratellino"; store.il_fratello_t = "il fratellino"
            store.uomo_t = "uomo"; store.un_t = "un"; store.Un_t = "Un"
            store.il_t = "il"; store.Il_t = "Il"; store.al_t = "al"
            store.gli_t = "gli"; store.lui_t = "lui"

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

define aede = Character("Aede", color="#c0392b", image="aede")
define glauco = Character("Glauco Severo", color="#6b6b6b")
define briseide = Character("Briseide Ippodamia", color="#b8860b")
define pc = Character("[player_name]", color="#f0e6d2")

# Fratelli di Ceppo del protagonista (Ceppo di Briseide Ippodamia).
define vanna = Character("Vanna", color="#8fbc8f")
define corrado = Character("Corrado", color="#87a7c7")

## Variabili di route #########################################################

default player_name = "Elio"
default player_gender = "m"
default fin = "o"
default figlio_t = "Figlio"
default fratello_t = "fratellino"
default il_fratello_t = "il fratellino"
default uomo_t = "uomo"
default un_t = "un"
default Un_t = "Un"
default il_t = "il"
default Il_t = "Il"
default al_t = "al"
default gli_t = "gli"
default lui_t = "lui"
default aede_affinity = 0
default flag_segreto_svelo = False
default flag_accetta_lavoro = False
default flag_giuramento = False
default flag_aede_rivelato = False
