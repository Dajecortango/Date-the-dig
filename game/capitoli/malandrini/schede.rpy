# Schede dei personaggi di Malandrini (screen scheda_personaggio, menu_cast.rpy):
# passate al registro con schede= in capitolo.rpy (init 10).

init python:

    SCHEDE_MALANDRINI = {
        "aede": dict(
            nome="Aede",
            route="Tempesta d'amore",
            difficolta="3/5",
            nota="Nessuna possibilità di poliamore.",
            battuta="«Non siamo niente. Tu non hai visto niente.»",
            profilo=(
                "Una tempesta in una tazzina: la fierezza di una veterana e una "
                "personalità scoppiettante come un fuoco d'artificio. Scontrosa e "
                "pungente con chi non conosce, tiene i sentimenti sepolti sotto "
                "strati di finta sicurezza, e detesta quando qualcuno li intravede."
            ),
            galleria="Aede",
        ),
        "ofelia": dict(
            nome="Ofelia",
            route="Tanto bella quanto letale",
            difficolta="4/5",
            nota="Poliamore possibile, solo con Aede e con Caino.",
            battuta="«Quest'anno cambio. Non montarti la testa: mi annoio in fretta.»",
            profilo=(
                "Letale, elegante, sarcastica quando serve e spietata con i "
                "sentimenti altrui. Corteggiatissima e dagli standard altissimi, "
                "difficilmente prende sul serio un pretendente: dovrai dimostrarle "
                "di essere più di un interesse passeggero."
            ),
            galleria="Ofelia",
        ),
        "caino": dict(
            nome="Caino",
            route="La legge del cuore",
            difficolta="4/5",
            nota="Attento ai dettagli: mette alla prova la tua memoria.",
            battuta="«Era una prova. La sala è piena di gente che mi dà ragione per riflesso. Tu no.»",
            profilo=(
                "Arconte della Proprietà, spadaccino e grande ballerino: farebbe di "
                "tutto per il potere. Calcolatore dal sorriso facile, vince ogni "
                "scontro verbale anche quando ha torto. Conquistata la sua fiducia, "
                "è un amante presente e totale."
            ),
            galleria="Caino",
        ),
        "druso": dict(
            nome="Druso",
            route="Il cuore provocatore",
            difficolta="4/5 (5/5 da uomo)",
            nota="Tienigli testa: le minacce lo esaltano.",
            battuta="«Prendi uno scudo, linguaccia, vediamo se il braccio vale la bocca.»",
            profilo=(
                "Un provocatore nato: sbraita, punzecchia e ti farà pesare ogni "
                "errore. Ma è anche un fine poeta, e nel momento del bisogno trova "
                "un coraggio che stupisce persino lui. Cerca un alleato sincero, "
                "non un cane che abbaia."
            ),
            galleria="Druso",
        ),
        "icaro": dict(
            nome="Icaro",
            route="Untouchable",
            difficolta="5/5",
            nota="Romance solo per protagonista donna; per gli uomini, la linea «Bro».",
            battuta="«Non toccare. Puoi guardare. Guardare è gratis, stasera.»",
            profilo=(
                "Nonchalant, logico, schietto fino alla mancanza di tatto. Ama i "
                "soldi e gli averi più del potere, bara a carte da maestro e guai a "
                "farglielo notare. La route più difficile del gioco: diventa "
                "l'eccezione a ogni sua regola."
            ),
            galleria="Icaro",
        ),
    }
