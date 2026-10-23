# Date the Dignitas — entry point.
# Con un solo capitolo registrato si entra subito; con piu' capitoli si
# sceglie (screen scegli_capitolo in capitoli.rpy). Dal menu principale la
# scelta parte con Start(ingresso) e non passa di qui.
# I capitoli vivono in game/capitoli/<id>/ (Malandrini: routes/ e calendario.rpy).

label start:

    if len(rcap.elenco()) == 1:
        jump expression rcap.elenco()[0].ingresso

    call screen scegli_capitolo
    # "Indietro" senza scelta: di nuovo la scelta.
    if not _return:
        jump start
    jump expression _return
