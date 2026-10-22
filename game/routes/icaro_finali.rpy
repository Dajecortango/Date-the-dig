# Route Icaro — climax e finali (romance e Bro).

## Climax e finali ###########################################################

label icaro_climax:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "Fine semestre. La saletta è vuota: il tavolo grande, stanotte, è solo nostro. Icaro mescola le carte come altri pregano."
    "Fuori, Zefiro festeggia la chiusura delle Lune. Dentro, solo il fruscio del mazzo e l'odore di resina fredda."
    "Accanto al mazzo, il registro del tavolo piccolo. Chiuso, legato con un nastro."
    if icaro_partita == "smaschera":
        icaro "Teucro ha lasciato Zefiro. Il Ramo di Vittoria l'ha richiamato a casa, «per motivi di salute». La salute di un baro scoperto è fragile."
    elif icaro_partita == "copre":
        icaro "Teucro mi deve ancora una rivincita. E il panno l'ho fatto lavare. Il conto della lavandaia è a tuo nome."
    elif icaro_partita == "silenzio":
        icaro "Milone mi saluta per strada, adesso. Con rispetto. Effetto collaterale del tuo silenzio: non l'avevo messo a bilancio."
    icaro "Ho condonato a Druso i cardini della mensa. Non dirglielo: deve credere che io sia ancora furioso. Lo tiene educato."
    show icaro sereno with qdiss
    "Accende la pipa. Il fumo sale dritto, senza fretta."
    icaro "Ho chiuso i conti del semestre. Tutti. Tranne una voce."
    icaro "Tu. Non so in che colonna metterti. E io so sempre in che colonna mettere tutto."
    "Smette di mescolare. Il mazzo resta fermo tra le sue dita: non gliel'ho mai visto fare."
    show icaro neutro with qdiss
    icaro "Domanda secca. Dimmi una cosa che hai visto di me. Una sola. Che non abbia visto nessun altro."
    menu:
        "Il mazzo è fermo. Aspetta me, per ripartire."
        "«Ti fermi mezzo respiro prima di dire la verità. Mai prima di una bugia.»" (peso=True):
            $ icaro_climax_scelta = "dettaglio"
            $ icaro_affinity += 1
            show icaro sorpreso with qdiss
            icaro "..."
            "Si guarda le mani, come se fossero di un altro."
            icaro "Mezzo respiro. Nessuno ha mai misurato mezzo respiro. Nemmeno io."
            "Ride, piano. È la seconda volta in un semestre. Stavolta non smette subito."
        "Prendergli la pipa, tirare una boccata, rendergliela. Senza una parola" (peso=True):
            $ icaro_climax_scelta = "silenzio"
            "Mi guarda fare. Non protesta, non conta, non si scosta."
            show icaro sereno with qdiss
            icaro "Il silenzio l'ho già comprato, settimane fa. Stanotte volevo il resto."
            icaro "Ma lo prendo lo stesso. Il silenzio non si svaluta."
            "Si riprende la pipa. Il cannello è ancora caldo. Non lo pulisce."
        "«Che bari anche quando giochi da solo.»" (peso=True):
            $ icaro_climax_scelta = "accusa"
            $ icaro_affinity -= 1
            with vpunch
            show icaro irritato with qdiss
            icaro "Io non baro. Io ottimizzo."
            icaro "E per la cronaca: era la risposta che avrebbe dato chiunque. Ti avevo chiesto una cosa che nessuno ha visto."
            "Ricomincia a mescolare. Più veloce di prima."
            icaro "«Ottimizzo.» Lo farò incidere sulla lapide. In piccolo, così nessuno lo contesta."
    "Il mazzo riparte. Icaro fa la sua offerta, come sempre, per ultimo."
    # Routing (rl.finale_icaro): se player_gender == "m" sempre icaro_bro_end;
    # altrimenti icaro_good -> icaro_neutral -> icaro_bad.
    $ cal_finale = rl.finale_icaro(player_gender, icaro_affinity,
                                   flag_icaro_coperto, congelate)
    jump expression cal_finale

label icaro_good:
    show icaro furbo with qdiss
    icaro "Ultima mano del semestre. Posta: tutto il mio inventario contro la tua parola. Carte coperte."
    "Giochiamo. E a fine mano, quando scopro le carte, capisco: ha barato. Al contrario. Per perdere."
    icaro "Hai vinto tutto. Che disastro contabile. Per fortuna il vincitore è... mio. Quindi il patrimonio non si muove."
    pc "Hai perso apposta, Icaro."
    icaro "Dimostralo. Nessuno ha mai dimostrato niente, a questo tavolo."
    pc "Ho visto la carta scivolarti nel polsino. All'incontrario: dentro, non fuori."
    show icaro sorpreso with qdiss
    icaro "...hai visto."
    "Non nega. In un semestre, è la prima volta che Icaro non nega."
    show icaro imbarazzato with dissolve
    "Poi slega il nastro del registro. Lo apre alla pagina della riga coperta. Stavolta la mano resta ferma."
    "Una riga sola, nella sua grafia stretta da notaio. «Voce unica. Non ammortizzabile. Non cedibile.»"
    if icaro_climax_scelta == "dettaglio":
        icaro "Prima di scriverla mi sono fermato mezzo respiro. Ormai sai cosa vuol dire."
    else:
        icaro "L'ho scritta in silenzio. Mi sembrava la lingua giusta, con te."
    pc "E il prezzo?"
    icaro "Fuori listino. Le cose che non si vendono non hanno un prezzo. Hanno un proprietario."
    "Non mi tocca. Sposta il mazzo di un dito verso di me, sul panno. Da Icaro, è una mano tesa."
    scene bg cala_notte with fade
    show icaro sereno with dissolve
    "Il tetto sopra la Consorteria. Due stuoie, una pipa sola, e la regola cambiata: si fuma a turno."
    "Mi passa la pipa. Le nostre dita si toccano, stavolta. Non la ritira."
    icaro "Annotazione d'inventario. Contatto: accettato. Una persona sola. Non allargarti."
    "Non lo dimostrerò mai. Ma la lampada più brutta del magazzino, da quella notte, sta sul mio davanzale. Non è in vendita."
    scene bg nero with fade
    $ sblocca_finale("icaro_good")
    with lampo_oro
    centered "{cps=20}{size=+10}UNTOUCHABLE{/size}\n\nL'eccezione che conferma ogni regola.\nE non è in vendita.{/cps}"
    return

label icaro_neutral:
    show icaro furbo with qdiss
    icaro "Proposta: socio al dieci per cento. Tu guardi le mani, io taglio il mazzo. Niente sentimenti: rendono poco e costano troppo."
    if icaro_climax_scelta == "accusa":
        icaro "E prima che tu lo dica: no, il contratto non è truccato. Leggilo due volte, visto che ti piace accusare."
    elif icaro_climax_scelta == "dettaglio":
        icaro "Hai l'occhio giusto. Mezzo respiro, l'hai detto tu. È per questo che ti pago: per guardare."
    else:
        icaro "Sai tacere. In un socio vale più del capitale."
    icaro "Contratto in triplice copia. Una a te, una a me, una a Caino. Lui le copie non le perde mai."
    "Il registro resta legato. Non lo apre, e non lo sposta dal suo lato del tavolo."
    "Accetto. È il massimo che il suo bilancio concede, e il dieci per cento di Icaro vale più del cento per cento di molti."
    show icaro neutro with qdiss
    "Da allora, ogni fine Luna, una busta sotto la mia porta. Cifra esatta al centesimo, mai un biglietto."
    "Una volta, dentro, c'è una moneta in più. La riporto. La riprende senza commentare."
    "Qualche volta, a fine mano, mi guarda come si guarda una carta scartata troppo presto. Poi rimescola."
    "Al tavolo grande ho un posto. Il tavolo piccolo, quello dove conta, resta suo."
    scene bg nero with fade
    $ sblocca_finale("icaro_neutral")
    centered "{cps=20}{size=+10}IL SOCIO{/size}\n\nDieci per cento.\nPagato puntualmente, ogni Luna.{/cps}"
    return

label icaro_bad:
    show icaro irritato with qdiss
    icaro "Il posto al tavolo era in prova. La prova è scaduta. Niente di personale: è che il personale, con te, non ha mai aperto."
    if icaro_climax_scelta == "accusa":
        icaro "E chi mi dà del baro al mio tavolo non ci si siede due volte. È la regola più vecchia della casa."
    "Spinge il registro dal suo lato. Il nastro resta chiuso: la riga che c'era sopra, se c'era, non la leggerò mai."
    icaro "Domani cambio le serrature della fumeria. Non è contro di te. È contro chiunque."
    "Mi alzo. Non protesto: coi bari inguaribili non si vince, e con Icaro non si pareggia nemmeno."
    show icaro neutro with qdiss
    "Sulla soglia mi volto. Lui sta già mescolando per la prossima mano. Contro nessuno."
    "Un'occhiata rapida al posto vuoto. Poi segna qualcosa a margine del registro. Una voce chiusa, credo. In perdita."
    "In strada mi frugo le tasche, per abitudine. Manca una moneta. Una sola. L'ultimo interesse."
    scene bg nero with fade
    $ sblocca_finale("icaro_bad")
    centered "{cps=20}{size=+10}FUORI LISTINO{/size}\n\nIcaro non perde mai.\nNemmeno quando vinci.{/cps}"
    return

label icaro_bro_end:
    if rl.finale_bro(icaro_affinity, icaro_impegnato) == "icaro_bro_listino":
        icaro "Il semestre chiude in attivo: un fratello acquisito, costo zero, rendita perpetua. Il miglior affare che io non abbia mai pianificato."
        if icaro_climax_scelta == "dettaglio":
            icaro "Mezzo respiro. Nemmeno Caino se n'è accorto, e Caino conta i respiri della gente per mestiere."
        elif icaro_climax_scelta == "silenzio":
            icaro "E la pipa me l'hai resa intera. In questa famiglia nessuno restituisce quello che prende. Nessuno."
        else:
            icaro "Mi hai dato del baro. Lo tollero da un fratello solo, e una volta sola. La tua l'hai spesa."
        show icaro sereno with dissolve
        "Slega il nastro del registro e lo gira verso di me. Una pagina, una riga."
        "«Fratello. Nessuna contropartita.» Sotto, la sua firma. E lo spazio per la mia."
        "Firmo. Lui soffia sull'inchiostro, chiude il registro e torna a mescolare, come se niente fosse."
        icaro "Druso pretenderà di firmare anche lui. Gli dirò che la pagina è finita."
        icaro "Caino lo saprà entro l'alba. Lascialo sapere. Per una volta, è un credito che non può riscuotere."
        icaro "Domani sera, stesso tavolo. Tu guardi le mani degli altri. Le mie no: sono di famiglia."
        "La chiave del magazzino resta nella mia tasca. Il gradino accanto al suo resta mio. Nel Nord, è più di quanto ottenga chiunque."
        scene bg nero with fade
        $ sblocca_finale("icaro_bro_listino")
        centered "{cps=20}{size=+10}LISTINO CHIUSO{/size}\n\n{i}Finale Bro{/i}\n\nNon tutto ciò che è prezioso si tocca.{/cps}"
    else:
        icaro "Buon semestre, [figlio_t] di Briseide. Il tavolo grande apre a chi conta. Torna quando conti."
        if icaro_climax_scelta == "accusa":
            icaro "E la prossima volta che mi dai del baro, porta le prove. Non le troverai, ma almeno sarà sportivo."
        "Il registro resta legato. Se lo infila sotto il braccio e si alza per primo."
        "Spinge la mia sedia sotto il tavolo con la punta dello stivale. Posto libero. Rientra a listino."
        "Alla porta si ferma, la pipa tra i denti. Non si volta."
        icaro "Niente di personale. Il personale è un lusso, e io i lussi li compro solo a prezzo di saldo."
        "Esce. Sul panno ha lasciato il mazzo, tagliato perfetto. Da Icaro, vuol dire che non c'è altro da aggiungere."
        scene bg nero with fade
        $ sblocca_finale("icaro_bro_conti")
        centered "{cps=20}{size=+10}CONTI APERTI{/size}\n\nIl tavolo grande resta dov'era.\nTu no.{/cps}"
    return

## Finale passeggero — In pari ################################################

label icaro_passeggero:
    show icaro neutro with qdiss
    icaro "Ultima mano. Niente posta. Solo per vedere come va a finire."
    "Gioca pulito. Nessuna carta nel polsino, né dentro né fuori. Vince di poco, e lo sa contare."
    "Poi slega il nastro del registro. Lo apre alla pagina della riga coperta e me la gira davanti."
    "C'era scritto qualcosa, nella sua grafia stretta. Una riga tirata sopra, dritta, col righello."
    if "icaro" in congelate:
        icaro "L'avevo scritta prima che accettassi l'invito di qualcun altro. Te l'avevo detto: io non divido. Nemmeno le cose che non ho."
    else:
        icaro "L'avevo scritta la prima sera al tavolo grande. Il mercante gridava al baro, serviva qualcuno che mi coprisse, e tu hai guardato da un'altra parte. Non ti accuso: hai tenuto i conti separati. Ho fatto lo stesso."
    icaro "Voce chiusa. In pari. Né debiti né crediti: un bilancio rarissimo, credimi. Dovresti farlo incorniciare."
    show icaro sereno with qdiss
    "Mi passa la pipa. Una boccata, una sola. Poi se la riprende e pulisce il cannello con cura."
    scene bg vicoli_zefiro with fade
    "Una Luna dopo, la fumeria ha una lampada nuova sul tavolo grande. Brutta, enorme, d'ottone. Icaro la guarda come un figlio."
    show icaro furbo with dissolve
    "Al tavolo piccolo siede un ragazzo che non conosco, coi polsini troppo larghi. Icaro gli insegna a contare le torce."
    "Mi vede sulla soglia. Alza due dita dal mazzo: un saluto da socio di vecchia data, il massimo che concede a chi non gli deve niente."
    show caino sarcastico at left with dissolve
    caino "Tre copie del registro, come sempre. Nella mia c'è la tua riga, tirata via col righello. Mio fratello non cancella mai a mano libera."
    scene bg nero with fade
    $ sblocca_finale("icaro_passeggero")
    centered "{cps=20}{size=+10}IN PARI{/size}\n\nNé debiti né crediti.\nIl bilancio più triste che Icaro abbia mai chiuso.{/cps}"
    return
