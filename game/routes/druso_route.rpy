# Route Druso — "Il cuore provocatore".
# Lucchetto a rovescio: l'affinità sale solo tenendogli testa. Per un uomo
# la salita è più ripida: due passi falsi e Druso archivia (5/5 contro 4/5).

default druso_passi_falsi = 0
default flag_druso_coraggio = False

init python:
    def druso_passo_falso():
        store.druso_affinity -= 1
        if store.player_gender == "m":
            store.druso_passi_falsi += 1
            if store.druso_passi_falsi >= 2:
                store.congelate.add("druso")

    EVENTI.extend([
        {"id": "druso_ev1", "label": "druso_ev1", "tipo": "invito",
         "char": "druso", "titolo": "Druso pretende un pubblico: serata di versi",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: v["druso_affinity"] >= 3},
        {"id": "druso_ev2", "label": "druso_ev2", "tipo": "invito",
         "char": "druso", "titolo": "Una scommessa che puzza di trappola",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: v["druso_affinity"] >= 6
         and "druso_ev1" in v["visti"]},
        {"id": "druso_ev3", "label": "druso_ev3", "tipo": "invito",
         "char": "druso", "titolo": "Druso ti vuole con sé. Non spiega perché",
         "luna_min": 4, "slot": "pomeriggio",
         "cond": lambda v: v["druso_affinity"] >= 9
         and "druso_ev2" in v["visti"]},
        {"id": "druso_ev4", "label": "druso_ev4", "tipo": "invito",
         "char": "druso", "titolo": "Notte di guardia sulle mura di Zefiro",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["druso_affinity"] >= 9
         and "druso_ev3" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
    ])


## Evento 1 — Il poeta osceno ################################################

label druso_ev1:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with easeinleft
    "La taverna è sua, stasera: ha pagato un giro per comprarsi il silenzio e lo spreca subito."
    druso "Componimento nuovo! Titolo: «Ode [al_t] novellin[fin] di Briseide». Protagonista: presente in sala. Contenuto: indecente. Obiezioni?"
    menu:
        "Tutti mi guardano. È esattamente ciò che vuole."
        "«Procedi. Ma se la rima è zoppa, il bis lo recito io su di te.»":
            $ druso_affinity += 1
            druso "Minaccia poetica! La più nobile delle minacce!"
            "Recita. È oscena, puntuale, e — maledizione — ben scritta. Rispondo con due versi improvvisati sulla sua barba. La taverna sceglie me."
            show druso ghigno with qdiss
            druso "Hai vinto il pubblico, linguaccia. Il pubblico è MIO. Ora o ti odio o ti tengo. Non ho ancora deciso."
        "Arrossire e pregarlo di smettere":
            $ druso_passo_falso()
            druso "Oh, supplica! Che noia. Le suppliche funzionano solo in chiesa, e il Nord non ne ha."
        "Rovesciargli il boccale addosso":
            $ druso_affinity += 1
            with vpunch
            "Il boccale vola. La taverna tace. Druso si lecca la birra dal baffo, lentamente, come un gatto soddisfatto."
            druso "Reazione violenta e maleducata. Da manuale. CONTINUA COSÌ."
    return


## Evento 2 — La leva ########################################################

label druso_ev2:
    scene bg vicoli_zefiro with fade
    show druso neutro at left with dissolve
    "Druso, stranamente sobrio, mi aspetta nel retro della taverna con una pergamena di scommesse."
    druso "Senti qua. Un Eparca della Consorteria paga bene per sapere chi, nel tuo Ceppo, firma le lettere di Briseide quando lei è fuori città. Io lo so che lo sai. E tu sai che pagherei."
    "Eccolo: il test delle acque. Vuole vedere se sono una leva su cui fare forza."
    menu:
        "Il ghigno è a mezza via tra scherzo e agguato."
        "«Vendimi pure. Ma ricorda che poi la leva si gira.»":
            $ druso_affinity += 2
            show druso ghigno with qdiss
            druso "...risposta da fratello di Ceppo. O da nemico serio. In entrambi i casi: rispetto."
            druso "Era una prova, ovvio. L'Eparca esiste, la paga pure. Il mio rifiuto gliel'ho già venduto a caro prezzo."
        "Dirgli il nome: in fondo siamo amici":
            $ druso_passo_falso()
            $ druso_affinity -= 1
            druso "...l'hai detto davvero. Oh, povero tesoro. No, il nome non lo userò. Ma adesso so che sei un cane che non abbaia neanche."
        "Minacciarlo: se parla, lo denuncio al Consiglio":
            $ druso_passo_falso()
            druso "DENUNCIA! Al CONSIGLIO! Dove siede mia madre! Ti prego, fallo, voglio il posto in prima fila!"
    return


## Evento 3 — Il coraggio che stupisce anche lui #############################

label druso_ev3:
    scene bg vicoli_zefiro with fade
    show druso neutro at left with dissolve
    "Mi trascina «a vedere una cosa» nei vicoli bassi di Zefiro. La cosa è un esattore della Malacorte che spreme un lanternaio — il mio lanternaio, quello che fa credito ai Figli di Briseide."
    druso "Brutto affare. Andiamocene. Non è il nostro Ceppo, non è il nostro problema, e io ci tengo ai miei denti."
    menu:
        "Il lanternaio è a terra. L'esattore conta."
        "Intervenire, adesso":
            $ druso_affinity += 2
            $ flag_druso_coraggio = True
            with vpunch
            "Non aspetto. Due passi, il braccio dell'esattore, la torsione che Aede insegna ai novellini. E poi — dal nulla — un ruggito."
            show druso ghigno with qdiss
            druso "TESCHIO, BRUTTO STRACCIONE!"
            "Druso. Il codardo dichiarato. Addosso all'esattore con tutti i suoi cento chili, la barba e nessun piano."
            "Dopo, mentre il lanternaio ci benedice in tre dialetti, Druso si guarda le mani come se non le riconoscesse."
            show druso imbarazzato with qdiss
            druso "...non dirlo a nessuno. Il coraggio mi rovina la reputazione peggio della gratitudine."
        "Dargli retta e andarcene":
            $ druso_affinity -= 1
            show druso serio with qdiss
            "Ce ne andiamo. Druso non fa battute per tutta la strada. È la cosa più vicina al disprezzo che gli abbia mai visto addosso — e non so se è per me o per sé."
    return


## Evento 4 — La guardia #####################################################

label druso_ev4:
    scene bg vicoli_zefiro with fade
    show druso neutro at left with dissolve
    "Turno di guardia sulle mura di Zefiro, ultimo scalino prima del Nord vero. Druso si è offerto volontario. Il capoguardia ha chiesto se fosse malato."
    druso "Zitto, il vento ascolta. Notte lunga, lanterna corta. Si fa un patto: chi si addormenta paga il giro. O recita."
    "Per due ore il provocatore non provoca. Conta le torce sulla Calà, nomina le stelle sbagliate, e ogni tanto si zittisce a metà frase."
    menu:
        "Un'ombra sul cammino di ronda. Druso afferra la lanterna e non fa battute."
        "«Dimmi cosa c'è. Senza rima.»":
            $ druso_affinity += 1
            show druso serio with qdiss
            druso "...ho paura del buio, ecco. Dei cento chili e della barba, del buio. Dillo e ti butto di sotto."
            "Resto con lui fino all'alba, a un passo, senza dire niente. Il sole sorge sul suo ghigno: per una volta stanco, e vero."
        "Prenderlo in giro: «Il coraggioso Druso e le sue ombre»":
            $ druso_passo_falso()
            show druso irritato with qdiss
            druso "Ah. Bene. Questa me la segno nel registro delle cose che non perdono."
            "Il resto della guardia lo passa a recitare versi osceni al vento, rivolto verso la città. Mai verso di me."
        "Mettersi in silenzio al suo fianco":
            show druso imbarazzato with qdiss
            druso "...grazie. Non lo dirò mai più. Né a te, né alla taverna."
            "Il turno finisce all'alba. Non succede niente, ed è la cosa più importante."
    return


## Impegno (scelta del cuore) ################################################

label impegno_druso:
    scene bg vicoli_zefiro with fade
    show druso imbarazzato at left with dissolve
    "Mi aspetta fuori dalla taverna, per una volta senza pubblico. Ha in mano un foglio piegato in quattro, e l'aria di chi preferirebbe un TESCHIO."
    druso "Ho scritto una cosa. Non oscena. È... il problema è proprio questo, che non è oscena. Prima di dartela devo sapere se ridi."
    "Il foglio trema appena. Il poeta del disagio altrui, in imbarazzo per la prima volta da che lo conosco."
    menu:
        "«Perché il poema più bello non nasce dall'immaginazione.»"
        "Prendere il foglio senza ridere":
            $ impegno_esito = True
            "Lo leggo. Parla di un percorso che si fa assieme, di un'intesa che non ha bisogno di provocazioni. Rima baciata, naturalmente."
            show druso ghigno with qdiss
            druso "Allora? Metrica zoppa? Contenuto peggio? Di' qualcosa o DICHIARO."
            pc "Bis."
            druso "...bis concesso. A vita, se serve."
        "Restituirlo chiuso":
            $ impegno_esito = False
            $ congelate.add("druso")
            druso "Giusto. Che stupidaggine. Era uno scherzo, ovvio! Il finto sentimento: il mio capolavoro!"
            "Ride forte. Troppo forte. E da quella sera le sue poesie tornano oscene, e mai più su di me."
    return


## Fiaccolata (route attiva) #################################################

label druso_fiaccolata:
    scene bg cala_notte with fade
    show druso ghigno at left with dissolve
    "La Calà, trecento gradini di lanterne. Druso li guarda come un palco."
    druso "La leggenda dice mano nella mano. Io dico che la leggenda non ha mai visto le TUE mani: ruvide come la mia poesia."
    "Ma la mano la tende lui. E per trecento gradini il provocatore più insopportabile del Nord non provoca nessuno: cammina, stringe, e ogni venti gradini controlla che io ci sia ancora."
    show druso imbarazzato with dissolve
    druso "Se lo racconti in taverna, nego. Ho una reputazione. ...al gradino duecento puoi raccontare quello che vuoi."
    $ druso_affinity += 1
    return


## Climax e finali ###########################################################

label druso_climax:
    scene bg consiglio with fade
    "Convocazione del Ramo di Lenora. Qualcuno ha riferito alla Capofamiglia che il suo secondogenito «frequenta un[fin] Figli[fin] di Briseide oltre il decoro», e che per giunta ha fatto a botte nei vicoli per un lanternaio."
    show druso serio at left with dissolve
    "Druso, davanti alla madre che non si vede ma si sente, deve scegliere chi essere: il buffone che nega tutto, o l'uomo del gradino duecento."
    if flag_druso_coraggio and druso_affinity >= 13:
        jump druso_good
    elif druso_affinity >= 8:
        jump druso_neutral
    else:
        jump druso_bad

label druso_good:
    show druso ghigno at left with qdiss
    druso "Confermo tutto, madre. Il decoro, la rissa, [il_t] Figli[fin] di Briseide. E aggiungo un componimento in tema, se il Consiglio gradisce. Rima baciata."
    "Lo recita. Davanti a Lenora, agli Arconti, al Nord intero. Il poema non osceno. Il mio."
    "La sala non ride. La sala — che gli Asi la conservino — applaude."
    scene bg cala_notte with fade
    show druso ghigno at left with dissolve
    druso "Hai sentito? Pubblico nuovo. Il migliore. E tutto grazie al mio talento, ovviamente."
    pc "Ovviamente."
    show druso imbarazzato with dissolve
    druso "...e a te. Ma questo è fuori metrica."
    scene bg nero with fade
    centered "{cps=20}{size=+10}IL CUORE PROVOCATORE{/size}\n\nIl poema più bello non nasce dall'immaginazione.\nSi ispira alla realtà.{/cps}"
    return

label druso_neutral:
    show druso ghigno at left with qdiss
    druso "Frequentazione? Madre, io frequento TUTTI. È il mio pubblico. [Il_t] Figli[fin] di Briseide regge bene le mie rime, tutto qui."
    "Ne esce con una battuta, come sempre. E come sempre, la battuta è un muro."
    "Restiamo quello che eravamo: il poeta e la sua spalla. In taverna, ogni sera, il posto accanto al suo è mio. Nessuno dei due chiede di più, ad alta voce."
    scene bg nero with fade
    centered "{cps=20}{size=+10}IL POSTO ACCANTO{/size}\n\nOgni poeta ha una spalla.\nNon ogni poema ha un finale.{/cps}"
    return

label druso_bad:
    show druso serio at left with qdiss
    druso "Chi? Quell[fin]? Madre, ti prego. Un cane che abbaia, al mio seguito. Il pubblico non si sceglie."
    "Lo dice guardandomi. E il ghigno, stavolta, non arriva agli occhi."
    "Da quella sera le sue provocazioni tornano a essere solo crudeli, e io torno a essere solo pubblico. Il gioco crudo e duro ha dato il suo verdetto: non l'ho retto."
    scene bg nero with fade
    centered "{cps=20}{size=+10}IL CANE CHE ABBAIA{/size}\n\nDruso testa le acque di tutti.\nNon tutti galleggiano.{/cps}"
    return
