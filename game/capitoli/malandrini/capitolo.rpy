# Registrazione del capitolo I, "Malandrini". Gli altri campi (ritratto...)
# si riempiono man mano. FINALI e GALLERIA_ROUTE: finali.rpy (init 0).

init 10 python:
    from capitoli.malandrini import regia_tabelle
    # La funzione e' definita in conseguenze.rpy (init 999): la si chiama per
    # nome al momento del caricamento, quando esiste di sicuro.
    def _malandrini_migra_salvataggio():
        store._conseguenze_migra_salvataggio()

    # Cast del carosello del menu principale (menu_cast.rpy): (chiave, fase
    # del respiro, profondita' della parallasse in px), nell'ordine del giro.
    # Stesso ordine di make_gui.MM_CAST.
    MM_CAST = [
        ("aede", 0.0, 6),
        ("ofelia", 1.3, 6),
        ("caino", 0.6, 6),
        ("icaro", 2.1, 6),
        ("druso", 1.7, 6),
    ]

    # Colori del diamante nel namebox (screens.rpy, say).
    CHAR_COLORS.update({
        "Aede": "#c0392b", "Caino": "#c87a30", "Druso": "#8a9bb0",
        "Icaro": "#7fa06a", "Glauco Severo": "#6b6b6b",
        "Briseide Ippodamia": "#b8860b", "Vanna": "#8fbc8f",
        "Corrado": "#87a7c7", "Ofelia": "#7d3c98",
        "Lenora": "#a8a8c0", "Pandora": "#c98fa0",
    })

    rcap.registra(
        id="malandrini",
        numero=1,
        titolo="Malandrini",
        sottotitolo="Sei Lune a Rocca Tempesta",
        ingresso="capitolo1",
        copertina=None,
        funzioni={"calendario", "borsa", "diario", "cronache", "trama"},
        # Galleria dei finali (finali.rpy).
        finali=FINALI,
        gruppi_finali=GALLERIA_ROUTE,
        cast_menu=MM_CAST,
        # Schede dei personaggi (schede.rpy).
        schede=SCHEDE_MALANDRINI,
        # Feedback sulle affinita' (feedback.rpy): (variabile di store,
        # ritratto, nome).
        affinita=[
            ("aede_affinity", "aede", "Aede"),
            ("caino_fiducia", "caino", "Caino"),
            ("druso_affinity", "druso", "Druso"),
            ("icaro_affinity", "icaro", "Icaro"),
            ("ofelia_affinity", "ofelia", "Ofelia"),
        ],
        # Tinte, fuoco, effetti di scena e fondi del menu (regia_logic).
        regia=regia_tabelle,
        # Audio (audio.rpy): sfondo -> loop d'ambiente (None = silenzio).
        ambienti={
            "corridoio_ceppo": "audio/malandrini/amb_camino.ogg",
            "studio_glauco": "audio/malandrini/amb_camino.ogg",
            "esterno_neve": "audio/malandrini/amb_vento.ogg",
            "cala_notte": "audio/malandrini/amb_cala.ogg",
            "vicoli_zefiro": "audio/malandrini/amb_strada.ogg",
            "palestra": "audio/malandrini/amb_sala.ogg",
            "consiglio": "audio/malandrini/amb_sala.ogg",
            "sala_svelo": "audio/malandrini/amb_sala.ogg",
            "arena_athlion": "audio/malandrini/amb_folla.ogg",
            "nero": None,
        },
        # Vicoli nei giorni di pioggia: la pioggia copre la strada.
        ambiente_pioggia={"vicoli_zefiro": "audio/malandrini/amb_pioggia.ogg"},
        # La Calà: le campane suonano quando ci si arriva.
        ambiente_arrivo={"audio/malandrini/amb_cala.ogg": "audio/malandrini/campana.ogg"},
        # Druso entra col suo tonfo, a fine scivolata (0.3 s).
        entrate={"druso": ("tonfo", 0.3)},
        dopo_caricamento=[_malandrini_migra_salvataggio],
        # Ritratto di un personaggio (feedback, slot di salvataggio).
        ritratto=cal_portrait,
    )
