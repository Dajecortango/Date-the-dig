# Nuova partita+ (Blocco D, punto 18).
# (a) Scelte gia' fatte: segno discreto nella screen choice (screens.rpy,
#     i.chosen): una fogliolina d'oro, mai l'esito.
# (b) Prologo gia' visto (persistent.prologo_visto, messo alla fine dello
#     Svelo): capitolo1 offre "Salta il prologo". Genere e nome si scelgono
#     sempre; dello Svelo resta solo la sua unica decisione (cosa dici ad
#     Aede), riassunta in una riga, con gli stessi effetti del prologo. Poi
#     lo stato e' quello dopo lo Svelo: "svelo" in eventi_visti, hook post-
#     evento chiamati, calendario allo slot successivo (Luna I, giorno 6).
# (c) Con almeno un finale sbloccato (ngp_attivo), 1-2 righe di deja-vu nei
#     punti chiave: lo Svelo e la scelta del cuore.

default persistent.prologo_visto = False

init python:

    # Esiti della decisione dello Svelo, identici a quelli di `prologo`
    # (aede_atto1.rpy): (flag_segreto_svelo, delta di aede_affinity).
    SVELO_ESITI = {
        "parola": (True, 2),
        "battuta": (False, 1),
        "minaccia": (False, -2),
    }

    def svelo_esito(chiave):
        segreto, delta = SVELO_ESITI[chiave]
        if segreto:
            store.flag_segreto_svelo = True
        store.aede_affinity += delta

    def ngp_attivo():
        """Almeno un finale sbloccato in una partita precedente."""
        return bool(persistent.finali_visti)

    def salta_prologo_stato():
        """Stato del calendario come dopo lo Svelo (cal_loop + cal_avanza)."""
        store.eventi_visti.add("svelo")
        cal_dopo_evento("svelo")
        store.cal_ultimo_giorno = (1, 1)
        store.cal_idx = CAL_SEQUENZA.index((1, 1, "sera")) + 1


label prologo_o_salto:
    if not persistent.prologo_visto:
        return
    menu:
        "Lo Svelo, la prima notte a Rocca Tempesta. Questa storia l'hai già sentita raccontare."
        "Rivivere lo Svelo":
            return
        "Salta il prologo":
            call salta_prologo
    return

label salta_prologo:
    scene bg nero with fade
    "Lo Svelo passa come un sogno già fatto: le maschere, il corridoio sbagliato, una lama sotto il mento e la volpe dietro la lama."
    menu:
        "Cosa ho detto ad Aede, quella notte?"
        "«Il tuo segreto muore con me. Hai la mia parola.»":
            $ svelo_esito("parola")
        "«Sbagli bersaglio spesso, o sono speciale?»":
            $ svelo_esito("battuta")
        "«Glauco Severo sarà curioso di saperlo.»":
            $ svelo_esito("minaccia")
    $ salta_prologo_stato()
    "Poi è sparita tra le maschere. Il semestre, invece, è appena cominciato."
    return
