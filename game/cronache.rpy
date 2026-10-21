# Cronache: piccola enciclopedia del Nord (personaggi, luoghi, Ceppi e Rami,
# usi e credenze). Una voce si sblocca quando l'evento o il label che la
# rivela e' stato visto: id in eventi_visti (calendario, pool delle
# attivita') oppure renpy.seen_label (persistente: le Cronache ricordano
# anche le partite precedenti). Chiavi vuote = nota fin dall'inizio.
# Testi solo da docs/lore.md (canone e fatti gia' mostrati in scena).
# Si apre dal diario e dal menu di gioco.

init python:

    CRONACHE_CATEGORIE = ["Personaggi", "Luoghi", "Ceppi e Rami", "Usi e credenze"]

    # (id, categoria, titolo, chiavi di sblocco, testo, [(chiavi, aggiunta)])
    CRONACHE = [
        # --- Personaggi ------------------------------------------------------
        ("briseide", "Personaggi", "Briseide Ippodamia", (),
         "Autarca del Ceppo della Columna Lactaria, «la madre degli orfani». "
         "Cinquanta Figli adottati in trent'anni: di ognuno ricorda il nome, la "
         "data e il motivo. Ai Figli del primo anno fa portare al polso un nodo "
         "di corda.",
         [(("att_riti_4",),
           "Nel suo Ceppo i conti si fanno col brodo: «chi parla tagliando non "
           "mente: è impegnato».")]),
        ("vanna_corrado", "Personaggi", "Vanna e Corrado",
         ("athlion", "cap2", "att_studio_1", "att_studio_2", "att_studio_3",
          "att_studio_4"),
         "Fratelli di Ceppo, Figli di Briseide come te. Corrado è l'erudito: "
         "araldica, Virtù, il Margine. Vanna sa chi corre, chi perde e chi "
         "guarda chi, e lo dice ad alta voce.",
         []),
        ("aede", "Personaggi", "Aede", ("svelo", "prologo"),
         "Figlia di Glauco Severo, sorella di Ofelia e di Ascadeo. Capelli rosso "
         "fiamma, occhi grigioverdi. Allo Svelo portava una maschera di volpe e "
         "una lama, e un messaggio da consegnare a qualcun altro.",
         [(("att_riti_2", "interludio2"),
           "Corrado racconta che fu addestrata con lame vere dai sette anni, "
           "«perché le finte insegnano bugie», e che perse la madre a dodici.")]),
        ("glauco", "Personaggi", "Glauco Severo", ("aede_cap1", "cap1"),
         "Autarca, padre adottivo di Aede, Ofelia e Ascadeo. Cortese e glaciale: "
         "non mente mai, non odia mai, non punisce mai per rabbia. Il suo Ceppo, "
         "nel Ramo, fa il lavoro di cui nessuno parla.",
         []),
        ("ofelia", "Personaggi", "Ofelia", ("ofelia_ev1", "att_corte_1"),
         "Figlia di Glauco, sorella di Aede e di Ascadeo. Elegante, riservata, "
         "sarcastica: tiene corte nella serra del padre e congeda i pretendenti "
         "con una frase sola. Il suo colore è il nero; quello di Aede, il rosso.",
         [(("interludio_ofelia_1",),
           "Affila lei le lame del padre da quando aveva nove anni: il fabbro è "
           "morto da sei inverni.")]),
        ("ascadeo", "Personaggi", "Ascadeo", ("interludio_ofelia_2",),
         "Fratello di Aede e Ofelia, sempre ai margini della scena. Da tre anni "
         "tiene un libro di scommesse sui pretendenti di Ofelia.",
         []),
        ("caino", "Personaggi", "Caino", ("adunanza", "ev_adunanza", "caino_prologo"),
         "Primogenito di Lenora, fratello maggiore di Druso e Icaro, Arconte "
         "della Proprietà. Spadaccino, ballerino, calcolatore. Beve idromele di "
         "Rurikstad e detesta il vino di Glostok.",
         [(("caino_cap3",),
           "Al mignolo destro porta un anello col drago di Draken il Mutevole. "
           "Era di suo padre.")]),
        ("druso", "Personaggi", "Druso", ("druso_ev1",),
         "Secondogenito di Lenora, ventisei anni. Poeta di versi osceni e "
         "provocatore di mestiere; codardo, salvo quando non lo è. Al Becco "
         "Storto tiene banco.",
         []),
        ("icaro", "Personaggi", "Icaro", ("icaro_ev1",),
         "Terzogenito di Lenora. Intellettuale, avaro, baro: al tavolo grande "
         "della fumeria vince con la pazienza di un esattore. Fuma dalla pipa e "
         "non sopporta di essere toccato.",
         [(("icaro_int1",),
           "Nel suo registro di cuoio nero c'è una voce per Druso: 42 Scudi, una "
           "spada da parata e una cena.")]),
        ("lenora", "Personaggi", "Lenora", ("udienza_lenora", "att_studio_3"),
         "Lenora Dignitas, Capofamiglia a vita, madre di Caino, Druso e Icaro. "
         "Regna da prima che Caino nascesse. Riceve i Figli dell'anno da dietro "
         "una grata: non li guarda, li ascolta.",
         [(("att_studio_3",),
           "Il Ballo delle Candele Spente fu un'idea sua: spense le candele, e "
           "con le candele una congiura intera.")]),
        ("pandora", "Personaggi", "Pandora", ("udienza_lenora",),
         "Sta accanto alla grata della Capofamiglia con un registro aperto sul "
         "braccio, e chiama i Ceppi uno alla volta. Quando c'è lei, Druso si "
         "raddrizza come un girasole.",
         []),
        ("ottone", "Personaggi", "Ottone", ("att_registri_1", "att_registri_2"),
         "Scrivano anziano della Proprietà. Gira il calamaio ai mancini senza una "
         "parola: lì dentro, dice, le macchie parlano prima di te.",
         []),

        # --- Luoghi ----------------------------------------------------------
        ("zefiro", "Luoghi", "Zefiro", (),
         "Capitale del Nord, la «Città delle Lanterne», divisa in sei Contrade. "
         "Lumina ha lanternai e taverne; la Consorteria cambiavalute e saletta da "
         "gioco; Marcassa magazzini e affari sporchi; da Eburnea parte la Calà.",
         []),
        ("rocca", "Luoghi", "Rocca Tempesta", ("svelo", "prologo"),
         "Il cuore del potere della Famiglia, a Zefiro. Arazzi col leone dorato, "
         "lanterne basse, corridoi laterali in cui è facile sbagliare strada.",
         []),
        ("cala", "Luoghi", "La Calà", ("fiaccolata", "ev_fiaccolata"),
         "Trecento gradini di lanterne, dalla Contrada Eburnea al fiume. Chi li "
         "scende mano nella mano alla Fiaccolata, dice la leggenda, si amerà per "
         "sempre.",
         []),
        ("becco_storto", "Luoghi", "Il Becco Storto", ("druso_ev1", "druso_ev2"),
         "Taverna in fondo a un vicolo: l'unica luce accesa quando Zefiro puzza "
         "di sego, di birra e di neve sporca. Sul retro, botti vuote e un gatto "
         "senza un orecchio.",
         []),
        ("serra", "Luoghi", "La serra di Glauco", ("ofelia_ev1", "att_corte_1"),
         "A Rocca Tempesta, fiori d'inverno e tubi caldi sotto il pavimento. "
         "Ofelia vi tiene corte; i pretendenti fanno la fila.",
         []),
        ("fumeria", "Luoghi", "La fumeria", ("icaro_ev1",),
         "Dietro la Consorteria, senza insegna: una porta bassa, odore dolce di "
         "resina, il fumo a mezz'aria come un secondo soffitto. In fondo, il "
         "tavolo grande.",
         []),
        ("segrete", "Luoghi", "Le Segrete Silenti", ("caino_cap4",),
         "Le prigioni della Famiglia. Chi l'Arconte della Verità trova con i "
         "registri in disordine, ci finisce.",
         []),

        # --- Ceppi e Rami ----------------------------------------------------
        ("famiglia", "Ceppi e Rami", "La Famiglia Dignitas", (),
         "Nel Nord c'è una sola Famiglia, e non è questione di sangue: si entra "
         "per Adozione, con un giuramento che cancella il nome e la vita di "
         "prima. Rivelare il «nome di prima» è il tabù più grande. Lo stemma è il "
         "leone dorato.",
         []),
        ("gerarchia", "Ceppi e Rami", "Ceppi, Rami e Autarchi", ("att_studio_1",),
         "Figlio, Filius, Autarca a capo di un Ceppo, Consiglio degli Autarchi; "
         "in cima, la Capofamiglia. Sessantatré Ceppi in nove Rami, un Primarca "
         "per ogni Ramo.",
         []),
        ("virtu", "Ceppi e Rami", "Le Virtù e gli Arconti", ("att_studio_2",),
         "Operosità, Esclusività, Verità. Ogni Arconte ne custodisce una, ogni "
         "processo ne invoca almeno due. Corrado: «la Virtù che un Dignitas "
         "predica di più è quella che teme di meno».",
         []),
        ("columna", "Ceppi e Rami", "La Columna Lactaria", ("att_riti_1", "interludio1"),
         "Il Ceppo di Briseide: neutrale, benvoluto, «una cucina troppo grande». "
         "Si cresce a brodo, orfani e voci.",
         []),
        ("ramo_lenora", "Ceppi e Rami", "Il Ramo di Lenora", ("druso_int3", "udienza_lenora"),
         "Il Ramo della Capofamiglia. Il suo sigillo è un corvo su un ramo "
         "spoglio, in cera nera. Si riunisce nella sala lunga, tra banchi di "
         "quercia.",
         []),
        ("ramo_vittoria", "Ceppi e Rami", "Il Ramo di Vittoria", ("athlion", "cap2"),
         "All'Athlion, i Figli di Vittoria sono gli avversari da battere.",
         [(("icaro_luna5",),
           "Teucro, Arconte del Ramo, porta un anello a ogni dito; il nipote "
           "Milone ha gli occhi svelti.")]),
        ("malacorte", "Ceppi e Rami", "La Malacorte", ("aede_cap1", "cap1"),
         "Osservatori ed esattori che battono le vie di Zefiro: spiano, "
         "riscuotono, e non sempre con le buone.",
         []),
        ("bocche", "Ceppi e Rami", "Le Bocche Sicofanti", ("aede_cap3", "cap3"),
         "Fessure di pietra sparse per Zefiro, dove chiunque può infilare una "
         "delazione anonima.",
         []),

        # --- Usi e credenze --------------------------------------------------
        ("svelo", "Usi e credenze", "Lo Svelo", ("svelo", "prologo"),
         "Festa in maschera a Rocca Tempesta. Per una notte il ceto non conta: un "
         "Figlio appena adottato può urtare il gomito di un Autarca e riderci "
         "sopra.",
         []),
        ("adunanza", "Usi e credenze", "L'Adunanza e il Dono", ("adunanza", "ev_adunanza"),
         "La riunione annuale della Famiglia. Chi ne ha il diritto può chiedere "
         "il Dono: una richiesta libera alla Capofamiglia.",
         []),
        ("athlion", "Usi e credenze", "L'Athlion", ("athlion", "cap2"),
         "La gara atletica dell'anno tra Ceppi e Rami: corsa, salto, lancio, "
         "lotta.",
         []),
        ("teschio", "Usi e credenze", "Il TESCHIO", ("caino_cap2",),
         "Il colpo basso più famoso della Famiglia, accompagnato dal grido. Il "
         "Codice del Teschio, che Caino dice di aver scritto, ha una regola che "
         "tutti ricordano: si dichiara prima di colpire.",
         []),
        ("draken", "Usi e credenze", "Draken il Mutevole", ("att_studio_1",),
         "Il Nord crede nel Caos. Il suo protettore è Draken il Mutevole, che ha "
         "per simbolo il drago.",
         []),
        ("margine", "Usi e credenze", "Il Margine", ("att_studio_4",),
         "Un fiume lento che, dicono gli Arvali, separa i vivi da Drakengrad, la "
         "sala del Leone dove ogni storia viene raccontata per sempre.",
         []),
    ]

    def cronache_vista(chiavi):
        if not chiavi:
            return True
        visti = getattr(store, "eventi_visti", set())
        return any(k in visti or renpy.seen_label(k) for k in chiavi)

    def cronache_voci(categoria):
        """[(id, titolo, sbloccata)] della categoria, nell'ordine della lista."""
        return [(v[0], v[2], cronache_vista(v[3]))
                for v in CRONACHE if v[1] == categoria]

    def cronache_voce(vid):
        for v in CRONACHE:
            if v[0] == vid:
                return v
        return None

    def cronache_aggiunte(vid):
        v = cronache_voce(vid)
        return [testo for chiavi, testo in v[5] if cronache_vista(chiavi)] if v else []

    def cronache_conto():
        return sum(1 for v in CRONACHE if cronache_vista(v[3])), len(CRONACHE)

    def cronache_prima(categoria):
        for vid, _t, ok in cronache_voci(categoria):
            if ok:
                return vid
        return None


screen cronache():

    tag menu

    default cron_cat = CRONACHE_CATEGORIE[0]
    default cron_sel = cronache_prima(CRONACHE_CATEGORIE[0])

    use game_menu(_("Cronache")):

        vbox:
            spacing 18

            hbox:
                spacing 12
                for cat in CRONACHE_CATEGORIE:
                    textbutton cat:
                        style "cronache_tab"
                        text_style "cronache_tab_text"
                        selected (cat == cron_cat)
                        action [SetScreenVariable("cron_cat", cat),
                                SetScreenVariable("cron_sel", cronache_prima(cat))]
                $ cron_n, cron_tot = cronache_conto()
                text "Voci scoperte: [cron_n] / [cron_tot]" size TESTO_NOTA italic True color "#8f7f5c" yalign 0.5 xoffset 30

            add "gui/divisore.png" xalign 0.0

            hbox:
                spacing 34

                ## Indice della categoria.
                viewport:
                    xsize 400
                    ysize 640
                    scrollbars "vertical"
                    vscrollbar_unscrollable "hide"
                    mousewheel True
                    draggable True
                    vbox:
                        spacing 4
                        xfill True
                        for vid, titolo, ok in cronache_voci(cron_cat):
                            if ok:
                                textbutton titolo:
                                    style "cronache_voce"
                                    text_style "cronache_voce_text"
                                    selected (vid == cron_sel)
                                    action SetScreenVariable("cron_sel", vid)
                            else:
                                textbutton "— ? —":
                                    style "cronache_voce"
                                    text_style "cronache_voce_text"
                                    action None

                ## Pagina della voce.
                frame:
                    style "cronache_pagina"
                    $ cron_v = cronache_voce(cron_sel) if cron_sel else None
                    if cron_v:
                        viewport:
                            scrollbars "vertical"
                            vscrollbar_unscrollable "hide"
                            mousewheel True
                            vbox:
                                spacing 16
                                xfill True
                                text cron_v[2] style "cronache_titolo"
                                text cron_v[1] size TESTO_NOTA italic True color "#8f7f5c"
                                add "gui/divisore.png"
                                text cron_v[4] style "cronache_testo"
                                for agg in cronache_aggiunte(cron_sel):
                                    hbox:
                                        spacing 12
                                        text "◆" size 16 color "#c0392b" yoffset 8
                                        text agg style "cronache_testo"
                    else:
                        text "Pagine ancora bianche. Il semestre le scriverà." style "cronache_testo" align (0.5, 0.5) textalign 0.5


style cronache_tab is button
style cronache_tab:
    background None
    hover_background Frame("gui/button/page_hover_background.png", 10, 10)
    selected_background Frame("gui/button/page_selected_idle_background.png", 10, 10)
    selected_hover_background Frame("gui/button/page_selected_hover_background.png", 10, 10)
    padding (20, 8, 20, 8)

style cronache_tab_text is button_text
style cronache_tab_text:
    size 24
    idle_color "#a89468"
    hover_color "#f0c75e"
    selected_color "#f0c75e"
    outlines [(2, "#140a08", 0, 0)]

style cronache_voce is button
style cronache_voce:
    xfill True
    background None
    hover_background Frame("gui/button/hover_background.png", 12, 12)
    selected_background Frame("gui/button/selected_idle_background.png", 12, 12)
    selected_hover_background Frame("gui/button/selected_hover_background.png", 12, 12)
    padding (22, 8, 22, 8)

style cronache_voce_text is button_text
style cronache_voce_text:
    font gui.text_font
    size 25
    idle_color "#d9c9a8"
    hover_color "#ffffff"
    selected_color "#f0c75e"
    insensitive_color "#6b5f4a"

style cronache_pagina is empty
style cronache_pagina:
    xsize 860
    ysize 640
    background Frame("gui/frame_piccolo.png", 26, 26)
    padding (40, 30, 30, 30)

style cronache_titolo is text
style cronache_titolo:
    font gui.name_text_font
    size 38
    color gui.accent_color
    outlines [(2, "#140a08", 0, 0)]

style cronache_testo is text
style cronache_testo:
    font gui.text_font
    size 26
    color "#e6d9bd"
    line_spacing 4
