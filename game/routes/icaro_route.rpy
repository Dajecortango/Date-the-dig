# Route Icaro — "Untouchable" (romance solo per protagonista donna;
# per gli uomini la linea "Bro", stessa trama, finale platonico).
# La più difficile del gioco (5/5). Possessivo: niente poliamore, mai.

default icaro_impegnato = False
default flag_icaro_coperto = False

init python:
    EVENTI.extend([
        {"id": "icaro_ev1", "label": "icaro_ev1", "tipo": "invito",
         "char": "icaro", "titolo": "Un posto al tavolo grande di Icaro",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: v["icaro_affinity"] >= 2},
        {"id": "icaro_ev2", "label": "icaro_ev2", "tipo": "invito",
         "char": "icaro", "titolo": "Icaro vuole mostrarti «una cosa di valore»",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: v["icaro_affinity"] >= 4
         and "icaro_ev1" in v["visti"]},
        {"id": "icaro_ev3", "label": "icaro_ev3", "tipo": "invito",
         "char": "icaro", "titolo": "Una serata placida, pipa e silenzio",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["icaro_affinity"] >= 6
         and "icaro_ev2" in v["visti"]},
    ])

    # Possessività: dopo che il suo interesse e' acceso (>=6), accettare
    # l'invito di un altro personaggio lo chiude per sempre.
    def icaro_gelosia(ev):
        if (ev.get("tipo") == "invito"
                and ev.get("char") not in (None, "icaro")
                and store.icaro_affinity >= 4
                and store.route_attiva is None
                and "icaro" not in store.congelate):
            store.congelate.add("icaro")
            renpy.notify("Icaro non dimentica.")

    cal_post_evento_hooks.append(icaro_gelosia)


## Evento 1 — Il tavolo grande ###############################################

label icaro_ev1:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "Il tavolo grande della saletta: posta alta, un mercante della Consorteria, due Eparchi, e Icaro che vince con la pazienza di un esattore."
    icaro "Siediti qui. Non per giocare: per contare. Voglio vedere se conti come guardi."
    "Tre mani dopo, il mercante — in perdita secca — ringhia che «qualcuno bara»."
    menu:
        "Gli occhi del tavolo cercano un colpevole. Io so chi è."
        "«Ho contato ogni carta. Tutto regolare.» (mentire per lui)":
            $ icaro_affinity += 2
            $ flag_icaro_coperto = True
            icaro "Il [figlio_t] di Briseide conta bene. Pago da bere al tavolo: la sfortuna va consolata."
            "Più tardi, fuori, mi mette in mano tre Scudi senza guardarmi."
            icaro "Non è un regalo. È un dividendo. I soci si pagano."
        "Tacere e guardare altrove":
            $ icaro_affinity += 1
            "Non dico nulla. Il mercante sbollisce da solo. Icaro annota il mio silenzio come annota tutto: alla voce «utile»."
        "Dare ragione al mercante":
            $ congelate.add("icaro")
            icaro "Contate pure. Tutto regolare, come sempre."
            "Regolare, adesso. E il posto al tavolo grande, per me, non esiste più. Da nessuna parte, mai più."
    return


## Evento 2 — Gli averi ######################################################

label icaro_ev2:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "Mi porta in un magazzino dietro la Consorteria. Dentro: casse, stoffe, lampade di Lumina, un servizio da tè di Glostok. Tutto suo. Tutto inventariato."
    icaro "La gente colleziona titoli, favori, sentimenti. Aria. Io colleziono cose. Le cose non mentono, non ti tradiscono e non chiedono nulla: esistono, e sono mie."
    menu:
        "Me lo dice senza vergogna. È la sua visione del mondo, nuda."
        "«E ogni cosa qui dentro ha una storia. Raccontamene una.»":
            $ icaro_affinity += 2
            "Esita. Poi prende la lampada più brutta dello scaffale e racconta: la prima cosa che abbia mai vinto, a nove anni, barando contro un adulto."
            icaro "Valore di mercato: zero. Non è in vendita. Capisci la differenza, o devo rallentare?"
            pc "Capisco. È l'inventario che non mostri."
            icaro "...mh. Conti meglio del previsto."
        "«Le cose non ti terranno compagnia da vecchio.»":
            $ icaro_affinity -= 1
            icaro "La compagnia è una spesa. Le cose sono un attivo. Il tuo bilancio sentimentale non torna, e non è un mio problema."
    return


## Evento 3 — La serata placida ##############################################

label icaro_ev3:
    scene bg cala_notte with fade
    show icaro neutro with dissolve
    "Un tetto sopra la Consorteria, due stuoie, la pipa. Zefiro brilla in basso come il suo magazzino: tutta roba che prima o poi, dice, sarà sua."
    icaro "Regola della serata: niente domande, niente debiti, niente contatto. Si fuma, si guarda, si tace. Chi rompe la regola paga."
    "Fumiamo. Guardiamo. Taccio. Un'ora, forse due. È la cosa più vicina alla pace che il Nord mi abbia concesso."
    if player_gender == "f":
        icaro "...annotazione d'inventario. La tua presenza non è un passivo. Non capita. Non capita mai."
        $ icaro_affinity += 2
        "Da Icaro, è una dichiarazione d'amore in piena regola contabile."
    else:
        icaro "...annotazione d'inventario. Sei l'unico uomo che non mi fa venire voglia di contare l'argenteria. Tienitelo stretto."
        $ icaro_affinity += 2
    return


## Impegno (scelta del cuore) ################################################

label impegno_icaro:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "Mi aspetta al tavolo piccolo, quello dove non gioca: quello dove conta. Davanti a lui, un registro aperto su una pagina bianca."
    icaro "Ho fatto i conti tre volte. Una compagna è un passivo: tempo, attenzioni, rischio. Ogni logica dice di non firmare."
    icaro "Ma ho un buco nel bilancio da tre Lune, e il buco ha la tua faccia. Quindi: o sei l'eccezione che conferma ogni mia regola, o sei l'errore più costoso della mia vita. Scegli tu la voce."
    menu:
        "La pagina bianca aspetta. Icaro non firma mai per primo."
        "«Eccezione. E sono irrevocabile, come le tue regole.»":
            $ impegno_esito = True
            $ icaro_impegnato = True
            icaro "Irrevocabile. Parola da contratto serio. ...venduto."
            "Scrive una riga sola sulla pagina bianca, e la copre con la mano prima che io possa leggerla. Sua. Come tutto ciò che conta."
        "«Non sono una voce del tuo inventario.»":
            $ impegno_esito = False
            $ congelate.add("icaro")
            icaro "Allora il bilancio torna come prima. Perfetto. Era l'ipotesi più probabile, l'avevo già scontata."
            "Lo dice piatto, senza una piega. Solo che per la prima volta da che lo conosco, sbaglia il taglio del mazzo."
    return

label impegno_bro:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "Il tavolo piccolo. Icaro spinge verso di me una chiave di ferro, senza cerimonie."
    icaro "Magazzino. Copia unica. Se muoio, l'inventario va a te: Druso lo venderebbe, Caino lo tasserebbe. Tu lo conteresti. È il massimo che ho da offrire a un uomo, e non si ripete."
    menu:
        "La chiave pesa come un giuramento."
        "Prenderla":
            $ impegno_esito = True
            $ icaro_impegnato = True
            pc "La tengo. E non la conto: la custodisco."
            icaro "...custodire. Verbo accettabile. Fratello."
        "Rifiutarla":
            $ impegno_esito = False
            $ congelate.add("icaro")
            icaro "Come preferisci. L'offerta scade adesso e non rientra a listino."
    return


## Fiaccolata (route attiva) #################################################

label icaro_fiaccolata:
    scene bg cala_notte with fade
    show icaro neutro with dissolve
    "La Calà. Icaro guarda le trecento lanterne con occhio da perito: «olio per quaranta Scudi che cola verso il fiume»."
    if player_gender == "f":
        icaro "La leggenda della mano è un contratto verbale senza testimoni né penali. Ridicolo."
        "Poi mi prende la mano. Lui, che detesta il contatto. La tiene per trecento gradini, rigida e attenta, come si tiene una cosa di valore."
        icaro "Contratto ridicolo. Ma è mio, adesso. E io non mollo ciò che è mio."
    else:
        icaro "Scendiamo dal lato asciutto. Niente mani: la leggenda parla chiaro e io non firmo contratti ambigui. Ma il gradino accanto al mio è tuo. Listino chiuso."
    return


## Climax e finali ###########################################################

label icaro_climax:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "Fine semestre. La saletta è vuota: il tavolo grande, stanotte, è solo nostro. Icaro mescola le carte come altri pregano."
    if player_gender == "m":
        jump icaro_bro_end
    if icaro_affinity >= 10 and flag_icaro_coperto and "icaro" not in congelate:
        jump icaro_good
    elif icaro_affinity >= 6:
        jump icaro_neutral
    else:
        jump icaro_bad

label icaro_good:
    icaro "Ultima mano del semestre. Posta: tutto il mio inventario contro la tua parola. Carte coperte."
    "Giochiamo. E a fine mano, quando scopro le carte, capisco: ha barato. Al contrario. Per perdere."
    icaro "Hai vinto tutto. Che disastro contabile. Per fortuna il vincitore è... mio. Quindi il patrimonio non si muove."
    pc "Hai perso apposta, Icaro."
    icaro "Dimostralo. Nessuno ha mai dimostrato niente, a questo tavolo."
    "Non lo dimostrerò mai. Ma la lampada più brutta del magazzino, da quella notte, sta sul mio davanzale. Non è in vendita."
    scene bg nero with fade
    centered "{cps=20}{size=+10}UNTOUCHABLE{/size}\n\nL'eccezione che conferma ogni regola.\nE non è in vendita.{/cps}"
    return

label icaro_neutral:
    icaro "Proposta: socio al dieci per cento. Tu guardi le mani, io taglio il mazzo. Niente sentimenti: rendono poco e costano troppo."
    "Accetto. È il massimo che il suo bilancio concede, e il dieci per cento di Icaro vale più del cento per cento di molti."
    scene bg nero with fade
    centered "{cps=20}{size=+10}IL SOCIO{/size}\n\nDieci per cento.\nPagato puntualmente, ogni Luna.{/cps}"
    return

label icaro_bad:
    icaro "Il posto al tavolo era in prova. La prova è scaduta. Niente di personale: è che il personale, con te, non ha mai aperto."
    "Mi alzo. Non protesto: coi bari inguaribili non si vince, e con Icaro non si pareggia nemmeno."
    scene bg nero with fade
    centered "{cps=20}{size=+10}FUORI LISTINO{/size}\n\nIcaro non perde mai.\nNemmeno quando vinci.{/cps}"
    return

label icaro_bro_end:
    if icaro_affinity >= 6 and icaro_impegnato:
        icaro "Il semestre chiude in attivo: un fratello acquisito, costo zero, rendita perpetua. Il miglior affare che io non abbia mai pianificato."
        "La chiave del magazzino resta nella mia tasca. Il gradino accanto al suo resta mio. Nel Nord, è più di quanto ottenga chiunque."
        scene bg nero with fade
        centered "{cps=20}{size=+10}LISTINO CHIUSO{/size}\n\n{i}Finale Bro{/i}\n\nNon tutto ciò che è prezioso si tocca.{/cps}"
    else:
        icaro "Buon semestre, [figlio_t] di Briseide. Il tavolo grande apre a chi conta. Torna quando conti."
        scene bg nero with fade
        centered "{cps=20}{size=+10}CONTI APERTI{/size}\n\nIl tavolo grande resta dov'era.\nTu no.{/cps}"
    return
