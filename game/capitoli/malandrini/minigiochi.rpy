# Minigiochi di territorio (pacchetto 40 consigli, punti 14-17).
# Quattro scene nuove nei pool delle attivita', ognuna con un minigioco breve:
#   att_spada_duello   (spada, spada_p)  duello con Aede: leggere il segnale
#   att_fumeria_carte  (fumeria)         carte con Icaro: la mano truccata
#   att_registri_conti (registri)        registri di Caino: la riga sbagliata
#   att_taverna_botta  (taverna)         botta e risposta a tempo con Druso
# Sempre saltabili ("Lascia andare": esito neutro, nessun punto).
# Esito = fatto (FATTI) + al massimo +-1 una tantum (la scena sta nel pool).
# Logica pura: minigiochi_logic.py (tests/test_minigiochi.py).
# Spec: docs/superpowers/specs/2026-10-22-pacchetto-40-consigli-design.md

init python:
    from capitoli.malandrini import minigiochi_logic as mgl

    CONSEGUENZE_VARS.extend(["mg_duello", "mg_carte", "mg_registri", "mg_botta"])

    FATTI.extend([
        {"id": "mg_duello_vinto", "char": "aede",
         "testo": "Al cortile d'armi hai letto la guardia di Aede e l'hai battuta.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: v["mg_duello"] == "vinto"},
        {"id": "mg_duello_perso", "char": "aede",
         "testo": "Al cortile d'armi Aede ti ha battut[fin]. Ti sei rialzat[fin] ogni volta.",
         "avviso": None,
         "cond": lambda v: v["mg_duello"] == "perso"},
        {"id": "mg_carte_taciuto", "char": "icaro",
         "testo": "Alla fumeria hai visto la mano truccata di Icaro e non hai detto niente.",
         "avviso": "Icaro se ne ricorderà.",
         "cond": lambda v: v["mg_carte"] == "taciuto"},
        {"id": "mg_carte_detto", "char": "icaro",
         "testo": "Alla fumeria hai detto a Icaro, a quattr'occhi, quale mano era truccata.",
         "avviso": "Icaro se ne ricorderà.",
         "cond": lambda v: v["mg_carte"] == "detto"},
        {"id": "mg_carte_sviato", "char": "icaro",
         "testo": "Alla fumeria hai cercato il trucco di Icaro nella mano sbagliata.",
         "avviso": None,
         "cond": lambda v: v["mg_carte"] == "sviato"},
        {"id": "mg_registri_trovato", "char": "caino",
         "testo": "Ai registri hai trovato la somma che mentiva, davanti a Caino.",
         "avviso": "Caino se ne ricorderà.",
         "cond": lambda v: v["mg_registri"] == "trovato"},
        {"id": "mg_registri_sbagliato", "char": "caino",
         "testo": "Ai registri hai corretto una somma giusta. Sotto gli occhi di Caino.",
         "avviso": "Caino se ne ricorderà.",
         "cond": lambda v: v["mg_registri"] == "sbagliato"},
        {"id": "mg_botta_vinta", "char": "druso",
         "testo": "Alla taverna hai tenuto testa a Druso, battuta su battuta.",
         "avviso": "Druso se ne ricorderà.",
         "cond": lambda v: v["mg_botta"] == "vinta"},
        {"id": "mg_botta_persa", "char": "druso",
         "testo": "Alla taverna Druso ti ha messo a tacere davanti a tutti.",
         "avviso": "Druso se ne ricorderà.",
         "cond": lambda v: v["mg_botta"] == "persa"},
    ])

# Seconda visita del territorio (indice 1). spada e spada_p condividono gia'
# le stesse scene: eventi_visti e' unico, quindi il duello si gioca una volta
# sola, la prima volta che capita in uno dei due slot.
init 5 python:
    pool_aggiungi("spada", "att_spada_duello", 1)
    pool_aggiungi("spada_p", "att_spada_duello", 1)
    pool_aggiungi("fumeria", "att_fumeria_carte", 1)
    pool_aggiungi("registri", "att_registri_conti", 1)
    pool_aggiungi("taverna", "att_taverna_botta", 1)

# Esiti: None = mai giocato; "lasciato" = Lascia andare.
default mg_duello = None
# Costumanze > "Scelte a tempo": No toglie la clessidra alla sfida di Druso
# (accessibilita': chi legge lento o gioca su telefono).
default persistent.scelte_a_tempo = True
default mg_carte = None
default mg_registri = None
default mg_botta = None


## Schermata comune ##########################################################
# opzioni: [(etichetta, valore)]. Ritorna il valore, "lascia" o, col tempo,
# "silenzio" allo scadere.

define MG_TESTO = (38 if renpy.variant("small") else 29)
define MG_BOTTONE = (36 if renpy.variant("small") else 27)

transform mg_lato:
    xalign 0.1 yalign 1.0

screen mg_prova(titolo, testo, opzioni, tempo=None):
    modal True
    zorder 110
    style_prefix "mg"

    frame:
        vbox:
            spacing 18
            text titolo style "mg_titolo"
            text testo style "mg_testo"
            if tempo:
                bar value AnimatedValue(0.0, tempo, tempo, tempo) style "mg_barra"
                timer tempo action Return("silenzio")
            null height 4
            for etichetta, valore in opzioni:
                textbutton etichetta action Return(valore) style "mg_bottone" text_style "mg_bottone_text"
            textbutton _("Lascia andare") action Return("lascia") style "mg_lascia" text_style "mg_lascia_text"

style mg_frame is frame:
    background Frame("gui/frame_piccolo.png", 26, 26)
    xalign 0.94
    yalign 0.42
    xsize 1120
    padding (52, 40, 52, 34)

style mg_frame:
    variant "small"
    xalign 0.5
    xsize 1500
    yalign 0.5

style mg_titolo is text:
    font gui.name_text_font
    size 26
    color "#f0c75e"
    outlines [(2, "#140a08", 0, 0)]

style mg_titolo:
    variant "small"
    size 34

style mg_testo is text:
    font gui.text_font
    size MG_TESTO
    color "#f0e6d2"
    outlines [(1, "#140a08", 0, 0)]

style mg_barra is bar:
    ysize 16
    left_bar Solid("#f0c75e")
    right_bar Solid("#2a1a12")
    thumb None

style mg_barra:
    variant "small"
    ysize 24

style mg_bottone is button:
    background Frame("gui/button/choice_idle_background.png", 100, 16)
    hover_background Frame("gui/button/choice_hover_background.png", 100, 16)
    xfill True
    yminimum 84
    padding (70, 16, 70, 16)

style mg_bottone:
    variant "small"
    yminimum 116

style mg_bottone_text is text:
    font gui.text_font
    size MG_BOTTONE
    idle_color "#d9c9a8"
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5
    textalign 0.5

style mg_lascia is button:
    background None
    hover_background Frame("gui/button/page_hover_background.png", 10, 10)
    xalign 0.5
    yminimum 64
    padding (36, 12, 36, 12)

style mg_lascia:
    variant "small"
    yminimum 96

style mg_lascia_text is text:
    font gui.interface_text_font
    size 22
    idle_color "#a89468"
    hover_color "#f0c75e"
    yalign 0.5
    outlines [(2, "#140a08", 0, 0)]

style mg_lascia_text:
    variant "small"
    size 32


## 1. Duello con Aede — spada ################################################

define MG_DUELLO_MOSSE = [("Fendente", "fendente"), ("Parata", "parata"), ("Finta", "finta")]
define MG_DUELLO_COLPO = {
    "parata": "La sua lama scende dove sapevo. La fermo a un dito dal collo, legno contro legno.",
    "finta": "Accenno a destra. La sua guardia si apre a sinistra, e io ci sono già dentro.",
    "fendente": "Colpisco nel varco. Il legno le batte sul fianco, secco.",
}

label att_spada_duello:
    scene bg palestra with fade
    show aede neutra with dissolve
    "Aede mi lancia una spada da esercizio. La prendo al volo. Quasi."
    aede "Basta paglia. Oggi la paglia sono io. Tre riprese."
    aede "Non guardare la lama: guarda me. Il corpo dice sempre cosa farà la mano, un battito prima."
    show aede neutra at mg_lato with move
    $ mg_segnali = mgl.pesca_segnali(renpy.random)
    $ mg_punti = 0
    $ mg_i = 0
    $ mg_lascia = False
    while mg_i < 3:
        $ mg_segnale, mg_giusta = mg_segnali[mg_i]
        $ mg_titolo = "Ripresa %d di 3" % (mg_i + 1)
        call screen mg_prova(mg_titolo, mg_segnale, MG_DUELLO_MOSSE)
        if _return == "lascia":
            $ mg_lascia = True
            $ mg_i = 3
        elif _return == mg_giusta:
            $ mg_punti += 1
            $ mg_i += 1
            $ mg_riga = MG_DUELLO_COLPO[mg_giusta]
            show aede sorpresa with qdiss
            "[mg_riga]"
        else:
            $ mg_i += 1
            show aede irritata with qdiss
            with hpunch
            "Aede mi passa sotto la guardia. Il legno mi bacia le costole."
    show aede neutra at center with move
    if mg_lascia:
        $ mg_duello = "lasciato"
        show aede irritata with qdiss
        aede "Abbassi la spada a metà ripresa? Va bene. Domani si ricomincia da dove sei scappat[fin]."
        "Lo dice senza cattiveria. Peggio: lo dice come un'annotazione."
    elif mgl.esito_duello(mg_punti) == "vinto":
        $ mg_duello = "vinto"
        $ aede_affinity += mgl.delta("duello", "vinto")
        show aede sorriso with dissolve
        aede "...chi ti ha insegnato a leggere una guardia così?"
        pc "Tu. Stamattina. «Guarda me, non la lama.»"
        show aede imbarazzata with qdiss
        aede "Non ripetere le mie frasi. Suonano meglio quando le dico io."
        "Raccoglie la spada da terra, di spalle. Credo che sorrida ancora."
    else:
        $ mg_duello = "perso"
        show aede neutra with qdiss
        aede "Persa. Ma ti sei rialzat[fin] ogni volta, senza guardare la porta."
        aede "Il Nord ne ha visti tanti cadere. Pochi che si rialzano per il gusto di farlo."
    return


## 2. Carte con Icaro — fumeria ##############################################

define MG_ORDINALI = ["Prima", "Seconda", "Terza"]

label att_fumeria_carte:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "La fumeria, tardi. Icaro gioca contro un mercante di lana che crede di essere fortunato."
    "Tre mani di fila. Il mercante perde la prima, la seconda e la terza. Una sola, ne sono sicur[fin], non era fortuna."
    show icaro neutro at mg_lato with move
    python:
        mg_mani, mg_truccata = mgl.pesca_mani(renpy.random)
        mg_opz = [("%s mano: %s" % (MG_ORDINALI[i], m), i) for i, m in enumerate(mg_mani)]
    call screen mg_prova("Quale mano era truccata?", "Ripenso alle sue dita, una mano alla volta.", mg_opz)
    $ mg_scelta = _return
    show icaro neutro at center with move
    if mg_scelta == "lascia":
        $ mg_carte = "lasciato"
        "Smetto di guardare le mani. Il fumo è dolce, la sera è lunga, e gli Scudi del mercante non sono miei."
        icaro "Mh. Ti sei distratt[fin]. Fai bene: guardare costa."
        return
    if mg_scelta != mg_truccata:
        $ mg_carte = "sviato"
        $ mg_giusta_txt = MG_ORDINALI[mg_truccata].lower()
        show icaro furbo with qdiss
        "Il mercante se ne va. Icaro raccoglie le carte e mi guarda come si guarda un conto sbagliato."
        icaro "Fissavi la mano sbagliata. Peccato: era la sola onesta della serata."
        "La [mg_giusta_txt] mano, allora. Ripenso alle sue dita, e adesso lo vedo. Troppo tardi."
        return
    $ mg_giusta_txt = MG_ORDINALI[mg_truccata].lower()
    "La [mg_giusta_txt] mano. Rivedo il gesto come se fosse ancora sul panno."
    "Il mercante se ne va contando le monete che gli restano. Icaro accende la pipa."
    menu:
        "Ho visto. Lui non sa ancora che ho visto."
        "Aspettarlo fuori e dirglielo a quattr'occhi":
            $ mg_carte = "detto"
            scene bg vicoli_zefiro with fade
            show icaro irritato with dissolve
            pc "La [mg_giusta_txt] mano. Le tue dita, sul mazzo."
            icaro "Era irreprensibile."
            "Un silenzio lungo. Il fumo della pipa gli sale storto."
            show icaro imbarazzato with qdiss
            icaro "...la sistemo. Non perché l'hai vista tu. Perché qualcun altro, prima o poi, ha i tuoi occhi."
        "Tacere e godersi il fumo":
            $ mg_carte = "taciuto"
            $ icaro_affinity += mgl.delta("carte", "taciuto")
            "Non dico niente. Guardo il fumo salire, e le sue mani che mescolano di nuovo."
            show icaro sereno with dissolve
            icaro "Hai guardato la mano giusta. E hai tenuto la bocca chiusa."
            icaro "Due qualità nella stessa sera. Le tengo a mente."
    return


## 3. Registri di Caino — registri ###########################################

label att_registri_conti:
    scene bg studio_glauco with fade
    "Ottone mi posa davanti un foglio di decime ricopiato in fretta. Cinque righe. Ogni riga, la sua somma."
    show caino neutro with dissolve
    caino "Una di quelle somme mente. Trovala prima che la trovi io."
    caino "Hai il tempo che ti serve. Io ne ho meno."
    show caino neutro at mg_lato with move
    python:
        mg_righe, mg_errata = mgl.genera_registro(renpy.random)
        mg_opz = [(mgl.riga_testo(r), i) for i, r in enumerate(mg_righe)]
        mg_cardia_errata = mg_righe[mg_errata]["nome"] == mgl.CARDIA
    call screen mg_prova("Decime della Proprietà", "Tocca la riga con la somma sbagliata.", mg_opz)
    $ mg_scelta = _return
    show caino neutro at center with move
    if mg_scelta == "lascia":
        $ mg_registri = "lasciato"
        "Rendo il foglio a Ottone senza segni. Lui lo prende, lo piega in quattro e se lo mette nella manica."
        caino "Chi non firma non sbaglia. Né conta."
        return
    if mg_scelta == mg_errata:
        $ mg_registri = "trovato"
        $ caino_fiducia += mgl.delta("registri", "trovato")
        $ mg_riga = mg_righe[mg_errata]["nome"]
        "«[mg_riga]». Rifaccio la somma due volte, poi la cerchio a margine."
        show caino sarcastico with qdiss
        caino "Esatto. Lo scrivano che l'ha copiata dormirà peggio, stanotte. Io meglio."
        if mg_cardia_errata and "att_registri_1" in eventi_visti:
            pc "Il Ceppo di Cardia. Quelli che pagano sempre il giorno prima."
            show caino sorpreso with qdiss
            caino "...te lo ricordi."
            "Non aggiunge altro. Ma prende il foglio e lo mette sotto il suo, non sotto quello di Ottone."
    else:
        $ mg_registri = "sbagliato"
        $ caino_fiducia += mgl.delta("registri", "sbagliato")
        show caino freddo with qdiss
        caino "Hai corretto una somma giusta. Adesso nel registro ci sono due errori: quello che c'era, e il tuo."
        "Ottone mi toglie il foglio dalle mani. Raschia la mia correzione con l'unghia, senza una parola."
    return


## 4. Botta e risposta con Druso — taverna ###################################

define MG_BOTTA_REAZIONE = {
    "buona": "Ah! Sangue! La taverna fischia, e Druso batte il boccale sul tavolo come un giudice.",
    "debole": "Druso sbadiglia, platealmente. Qualcuno, in fondo, ride di me e non di lui.",
    "cattiva": "Druso si porta una mano al cuore. «Supplica! Signori, abbiamo una supplica!»",
    "silenzio": "Apro la bocca. Non ne esce niente. La taverna ride al posto mio.",
}

label att_taverna_botta:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with easeinleft
    "Druso è in piedi su una panca, il boccale alzato come uno scettro."
    druso "Gara di lingue! Tre colpi. Chi tace, paga. Novellin[fin], tocca a te: la carne fresca va in prima fila."
    $ mg_battute = mgl.pesca_battute(renpy.random)
    $ mg_punti = 0
    $ mg_i = 0
    $ mg_lascia = False
    while mg_i < 3:
        $ mg_b = mg_battute[mg_i]
        $ mg_titolo = "Colpo %d di 3" % (mg_i + 1)
        $ mg_opz = [(t, k) for t, k in mg_b["risposte"]]
        call screen mg_prova(mg_titolo, "Druso: " + mg_b["battuta"], mg_opz,
                             tempo=(mgl.DRUSO_TEMPO if persistent.scelte_a_tempo else None))
        if _return == "lascia":
            $ mg_lascia = True
            $ mg_i = 3
        else:
            $ mg_punti += mgl.VALORE_RISPOSTA[_return]
            $ mg_i += 1
            $ mg_riga = MG_BOTTA_REAZIONE[_return]
            if _return == "buona":
                show druso sorpreso at left with qdiss
            elif _return == "cattiva":
                show druso ghigno at left with qdiss
            else:
                show druso neutro at left with qdiss
            "[mg_riga]"
    if mg_lascia:
        $ mg_botta = "lasciato"
        show druso ghigno at left with qdiss
        druso "Se ne va! Signori, la ritirata più elegante della stagione. Applaudite, che non torna."
        "Esco con le orecchie calde. Ma senza aver chiesto niente a nessuno."
        return
    $ mg_botta = mgl.esito_botta(mg_punti)
    $ druso_affinity += mgl.delta("botta", mg_botta)
    if mg_botta == "vinta":
        show druso imbarazzato at left with qdiss
        druso "...va bene. Va bene! Stasera pago io. Non abituarti."
        "Scende dalla panca e mi spinge un boccale davanti. È la cosa più vicina a un inchino che gli abbia mai visto fare."
    elif mg_botta == "persa":
        show druso ghigno at left with qdiss
        druso "Tre colpi, zero ferite. Su di me, almeno. Paga l'oste, novellin[fin], e impara a mordere."
    else:
        show druso neutro at left with qdiss
        druso "Pari. Che noia. Il pareggio è la morte del teatro."
        "Però mi lascia il posto sulla panca. Per Druso, un pareggio è già un contratto."
    return
