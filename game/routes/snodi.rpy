# Snodi comuni del semestre: scelta del cuore (fine Luna IV), Fiaccolata
# (Luna V), climax di Luna VI, finale neutro.

default semestre_concluso = False
default rivali = None
default rivali_a_nome = ""
default rivali_b_nome = ""
default rivali_coppia = ""
default epilogo_finale = None
default epilogo_scelti = []
default epilogo_modo = "vivo"
# Soglie dell'epilogo (da routing_logic), impostate in epilogo_semestre.
default ep_soglie = {}
default ep_media = {}
# Label del finale scelto dal routing (routing_logic), per jump expression.
default cal_finale = None

init python:
    EVENTI.extend([
        {"id": "scelta_cuore", "label": "ev_scelta_cuore", "tipo": "fisso",
         "char": None, "luna": 4, "giorno": 28, "slot": "sera"},
        {"id": "fiaccolata", "label": "ev_fiaccolata", "tipo": "fisso",
         "char": None, "luna": 5, "giorno": 14, "slot": "sera"},
        # Il giuramento di Aede segue la Fiaccolata, solo a route attiva
        # (o seconda, nel poliamore con Ofelia) e non congelata: il vicolo
        # puo' congelare anche dopo l'impegno.
        {"id": "aede_cap6", "label": "cap6", "tipo": "fisso", "char": "aede",
         "luna": 5, "giorno": 20, "slot": "sera",
         "cond": lambda v: (v["route_attiva"] == "aede"
                            or v["route_seconda"] == "aede")
         and "aede" not in v["congelate"]
         and v["aede_sospetto"] < 2},
        {"id": "luna6_climax", "label": "ev_luna6", "tipo": "fisso",
         "char": None, "luna": 6, "giorno": 21, "slot": "sera"},
        # Dieci giorni prima della scelta: due cuori sopra soglia si
        # accorgono l'uno dell'altro. 0 punti.
        {"id": "rivalita", "label": "ev_rivalita", "tipo": "fisso",
         "char": None, "luna": 4, "giorno": 18, "slot": "mattina",
         "cond": lambda v: rivali_cuore(v) is not None},
    ])

    CUORE_NOMI = {"aede": "Aede", "caino": "Caino",
                  "druso": "Druso", "icaro": "Icaro", "ofelia": "Ofelia"}

    # Soglie e logica della scelta del cuore: UNICA fonte in
    # game/routing_logic.py (rl), usata da scelta, rivalita', udienza di
    # Lenora ed epilogo, e verificata dai test.
    CUORE_VAR = rl.CUORE_VAR
    cuore_soglie = rl.cuore_soglie
    # v = cal_vars(); restituiscono solo stringhe (picklabile).
    cuore_classifica = rl.cuore_classifica
    rivali_cuore = rl.rivali_cuore

    def cuore_candidati():
        """Personaggi sopra soglia e non congelati, per la scelta del cuore."""
        return rl.cuore_candidati(cal_vars())

    def route_viva():
        """Route attiva e non congelata nel frattempo; altrimenti None."""
        return rl.route_viva(store.route_attiva, store.congelate)

    def route_seconda_viva():
        """Seconda route del poliamore (solo con Ofelia viva), se non
        congelata nel frattempo; altrimenti None."""
        return rl.route_seconda_viva(store.route_attiva, store.route_seconda,
                                     store.congelate)

    def cuore_opzioni(cands):
        """Voci del menu del cuore: (testo, chiave), coppie poly comprese."""
        return rl.cuore_opzioni(cands, CUORE_NOMI)

    # Rivalita' (IV/18): sprite neutro per la variante generica.
    RIVALI_ESPR = {"aede": "neutra", "caino": "neutro", "druso": "neutro",
                   "icaro": "neutro", "ofelia": "neutra"}

    # Epilogo: quale finale ha chiuso il climax. Un label callback annota
    # l'ultimo label di finale raggiunto (i finali non si toccano: niente
    # sblocca_finale qui, la galleria resta una voce per label).
    EPILOGO_MORTO = ("bad_end_aede", "bad_end_glauco", "ofelia_bad_tempesta")
    EPILOGO_LONTANO = ("caino_bad_end", "neutral_end", "ofelia_bad")

    def epilogo_traccia_finale(name, abnormal):
        if name == "icaro_bro_end" or any(f[0] == name for f in FINALI):
            store.epilogo_finale = name

    config.label_callbacks.append(epilogo_traccia_finale)


## Scelta del cuore ##########################################################

label ev_scelta_cuore:
    scene bg corridoio_ceppo with fade
    "Fine della quarta Luna. Vanna dice che a Rocca Tempesta i semestri si decidono adesso: «chi non ha scelto entro la Fiaccolata, ha scelto lo stesso»."
    if ngp_attivo():
        vanna "Che faccia, [fratello_t]. Sembri un[fin] che questa sera l'ha già vissuta, e sa già come va a finire."
        "Non lo so. Ma per un attimo ho la sensazione di averla già scelta, questa strada. O un'altra."
    python:
        cuore_lista = cuore_candidati()
    if not cuore_lista:
        "Guardo il semestre alle spalle: facce, allenamenti, serate. Nessun nome pesa più degli altri. Forse è presto. Forse sono io."
        return
    $ cuore_voci = cuore_opzioni(cuore_lista)
    if len(cuore_voci) == 1:
        $ cuore_scelto = cuore_voci[0][1]
    else:
        $ cuore_scelto = renpy.display_menu(
            [("A chi appartiene questo semestre?", None)] + cuore_voci)
    if cuore_scelto in ("ofelia+aede", "ofelia+caino"):
        $ cuore_altro = cuore_scelto.split("+")[1]
        if cuore_altro == "aede":
            call impegno_ofelia_aede
        else:
            call impegno_ofelia_caino
        $ cuore_coppia = rl.risolvi_coppia(impegno_of, impegno_altro, cuore_altro)
        if cuore_coppia:
            $ route_attiva, route_seconda = cuore_coppia
        return
    if cuore_scelto == "aede":
        call impegno_aede
    elif cuore_scelto == "caino":
        call impegno_caino
    elif cuore_scelto == "druso":
        call impegno_druso
    elif cuore_scelto == "ofelia":
        call impegno_ofelia
    elif player_gender == "f":
        call impegno_icaro
    else:
        call impegno_bro
    if impegno_esito:
        $ route_attiva = cuore_scelto
    return


## Fiaccolata della Calà #####################################################

label ev_fiaccolata:
    $ cal_route = route_viva()
    if cal_route == "aede":
        call cap5
    elif cal_route == "caino":
        call fiaccolata_caino
    elif cal_route == "druso":
        call druso_fiaccolata
    elif cal_route == "icaro":
        call icaro_fiaccolata
    elif cal_route == "ofelia" and route_seconda_viva() == "caino":
        call ofelia_fiaccolata_caino
    elif cal_route == "ofelia" and route_seconda_viva() == "aede":
        call ofelia_fiaccolata_aede
    elif cal_route == "ofelia":
        call ofelia_fiaccolata
    else:
        call fiaccolata_neutra
    return

label fiaccolata_caino:
    scene bg cala_notte with fade
    show caino neutro with dissolve
    "La Calà, trecento gradini di lanterne. Caino li scende come scende in Consiglio: contando chi lo guarda."
    caino "Lo sai cosa vale questa leggenda, a registro? Niente. Nessun atto, nessun sigillo, nessun testimone utilizzabile."
    pc "Eppure sei qui."
    show caino tenero with dissolve
    caino "Sono qui perché le cose fuori inventario, ultimamente, rendono meglio di quelle a bilancio. Dammi la mano e non farlo pesare: se mia madre lo viene a sapere, dirò che era un'operazione di mercato."
    "Mano nella mano, dal primo gradino all'ultimo. L'Arconte della Proprietà non lascia la presa nemmeno per salutare due Eparchi. I dettagli possiedono le persone."
    return

label fiaccolata_neutra:
    scene bg cala_notte with fade
    show vanna neutra at left with dissolve
    show corrado neutro at right with dissolve
    "La Fiaccolata. Scendo la Calà con Vanna e Corrado, un gradino di luce alla volta."
    vanna "Guardali, i piccioncini della Rocca. E tu niente, [fratello_t]? Nemmeno una mano da tenere?"
    corrado "Lascialo stare. C'è chi scende la Calà per la leggenda, e chi per contare i gradini. Entrambi arrivano al fiume."
    "Arrivo al fiume. Trecento gradini, nessuna mano. La leggenda, quest'anno, parla d'altro."
    return


## Luna VI — il conto del semestre ###########################################

label ev_luna6:
    $ semestre_concluso = True
    $ cal_route = route_viva()
    # Per l'epilogo: chi era scelto prima del climax, e quale finale chiude.
    $ epilogo_finale = None
    $ epilogo_scelti = [c for c in (cal_route, route_seconda_viva()) if c]
    if cal_route == "aede":
        call climax
    elif cal_route == "caino":
        call caino_climax
    elif cal_route == "druso":
        call druso_climax
    elif cal_route == "icaro":
        call icaro_climax
    elif cal_route == "ofelia":
        if route_seconda_viva() == "aede":
            call climax
        else:
            call ofelia_climax
    else:
        call finale_neutro_semestre
    # Tutti i finali (anche quelli di Aede raggiunti dal poly di Ofelia)
    # tornano qui con return: l'epilogo li chiude tutti.
    call epilogo_semestre
    return

label finale_neutro_semestre:
    scene bg corridoio_ceppo with fade
    show briseide neutra with dissolve
    "Fine della sesta Luna. Briseide mi riceve con due tazze di brodo: il bilancio di fine semestre, nel suo Ceppo, si fa così."
    briseide "Sei mesi. Hai imparato la spada, i registri, le scorciatoie di Zefiro e — mi dicono — anche a reggere un boccale. Non hai perso il nome, non hai perso il sangue. Nel Nord si chiama buon raccolto."
    pc "E il resto, madre?"
    briseide "Il resto ha i suoi tempi. Rocca Tempesta non scappa, e nemmeno i suoi cuori: sono tutti ancora lì, più testardi di prima. Bevi il brodo, [figlio_t] mi[fin]. I semestri finiscono. Le storie no."
    scene bg nero with fade
    $ sblocca_finale("finale_neutro_semestre")
    centered "{cps=20}{size=+10}IL SEMESTRE DEL NOVELLINO{/size}\n\nGuardare, ascoltare, non farsi notare.\nDue su tre, come sempre.{/cps}"
    return


## Luna IV — Rivalità (fisso IV/18 sera) #####################################
# Solo se almeno due candidati sono sopra la soglia del cuore: i due piu'
# alti si accorgono l'uno dell'altro. Varianti per coppia. Prendere una
# parte vale +1 a chi si sceglie e -1 all'altro (puo' far scendere uno dei
# due sotto la soglia del cuore, dieci giorni prima della scelta); le
# uscite neutre valgono 0.

init python:
    def rivali_sposta(scelto, lasciato):
        """Rivalita' generica: +1 a chi si sceglie, -1 all'altro."""
        for char, delta in ((scelto, 1), (lasciato, -1)):
            var = CAL_AFF_VAR[char]
            setattr(store, var, getattr(store, var) + delta)

label ev_rivalita:
    python:
        rivali = rivali_cuore(cal_vars())
        if rivali:
            rivali_a_nome = CUORE_NOMI[rivali[0]]
            rivali_b_nome = CUORE_NOMI[rivali[1]]
            rivali_coppia = "+".join(sorted(rivali))
    if not rivali:
        return
    if rivali_coppia == "aede+ofelia":
        call rivalita_sorelle
    elif rivali_coppia == "caino+druso":
        call rivalita_caino_druso
    elif rivali_coppia == "caino+icaro":
        call rivalita_caino_icaro
    elif rivali_coppia == "druso+icaro":
        call rivalita_druso_icaro
    else:
        call rivalita_generica
    return

label rivalita_sorelle:
    scene bg corridoio_ceppo with fade
    show aede irritata with dissolve
    show ofelia neutra at left with dissolve
    "Dieci giorni alla scelta. Il corridoio è stretto, stamattina. Stretto per tre."
    "Aede da una parte, Ofelia dall'altra. In mezzo io, e un silenzio che si potrebbe affilare."
    ofelia "Sorella. Ti ho vista al cortile, all'alba. Guardavi la porta più dei bersagli."
    aede "E io ho visto la tua serra. Una sedia in più, accanto alla tua. Da quando metti le sedie?"
    show ofelia compiaciuta at left with qdiss
    ofelia "Da quando qualcuno merita di sedersi. Capita di rado. Me l'hai insegnato tu, a non sprecare niente."
    aede "Ti ho insegnato a tenere la guardia. Non a usarla sulle mie cose."
    "«Le mie cose.» Lo dice e se ne pente nello stesso respiro. Troppo tardi: Ofelia l'ha già raccolto, come un guanto."
    menu:
        "Due figlie di Glauco. Nessuna abbassa lo sguardo per prima."
        "«Non sono una cosa. Di nessuna delle due.»":
            show aede imbarazzata with qdiss
            aede "...non intendevo. Lascia stare. Non intendevo niente."
            ofelia "Intendeva tutto. Le capita, quando non pensa. È la sua qualità migliore."
            "Ofelia se ne va per prima. Ha vinto lei. Aede non lo sa ancora."
        "Dare ragione ad Aede, a voce bassa":
            $ aede_affinity += 1
            $ ofelia_affinity -= 1
            show aede neutra with qdiss
            aede "Visto, Ofelia? Almeno qui si sa da che parte stare."
            show ofelia rabbia at left with qdiss
            ofelia "Da che parte stare. Che frase da soldato. Ricordatela, quando ti servirà una serra calda."
        "Dare ragione a Ofelia, con un mezzo sorriso":
            $ ofelia_affinity += 1
            $ aede_affinity -= 1
            ofelia "Visto, sorella? Non tutti scelgono il rosso."
            show aede rabbia with qdiss
            aede "Il rosso non si sceglie. Si porta. Lo vedrai."
            with hpunch
            "Aede mi passa accanto e mi urta con la spalla. Forte. Apposta. Stasera il livido avrà la forma della sua scapola."
    "Vanna, più tardi, mi dice che nel Ceppo di Glauco qualcuno ha cominciato a contare i giorni. Ad alta voce."
    return

label rivalita_caino_druso:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with easeinleft
    "Il Becco Storto, mattina. Druso non è andato a letto: tiene banco con una strofa nuova, davanti a tre avventori e un gatto."
    show caino freddo with dissolve
    "Poi entra Caino, e il banco si svuota da solo."
    caino "Fratello. [Il_t] novellin[fin] mi deve una serata. Siamo d'accordo da settimane."
    druso "D'accordo? Io le sue serate le ho in rima. Batte qualsiasi sigillo."
    caino "Le rime non si depositano."
    druso "Nemmeno i tuoi sentimenti, Arconte. Li hai mai trovati? Hai guardato sotto il calamaio?"
    show caino sarcastico with qdiss
    caino "Sei ubriaco, Druso."
    druso "E tu sei geloso. Stasera uno dei due sarà sobrio."
    with vpunch
    "Caino posa il boccale sul tavolo. Piano. Fa più rumore di un pugno."
    menu:
        "Si voltano tutti e due verso di me. Il Becco Storto trattiene il fiato."
        "«TESCHIO a tutti e due, se non la smettete.»":
            show druso sorpreso at left with qdiss
            druso "...dichiarato PRIMA. Ha dichiarato prima, Caino. Il Codice è dalla sua."
            show caino neutro with qdiss
            caino "Il Codice l'ho scritto io. Per una volta mi pento della clausola."
            "Ridono. Insieme. Per mezzo secondo sono solo due fratelli. Poi se ne accorgono, e smettono."
        "Restare sedut[fin] accanto a Druso":
            $ druso_affinity += 1
            $ caino_fiducia -= 1
            show druso ghigno at left with qdiss
            druso "Visto? Il pubblico ha scelto. Torna ai tuoi registri, fratello."
            show caino freddo with qdiss
            caino "Il pubblico cambia idea, Druso. I registri no."
            "Esce senza pagare. Lo fa apposta: stasera il conto lo troverò a mio nome."
        "Seguire Caino fuori":
            $ caino_fiducia += 1
            $ druso_affinity -= 1
            hide druso with dissolve
            show caino neutro with qdiss
            "Fuori, Caino respira il freddo del mattino come se gli servisse. Non mi guarda."
            caino "Mio fratello ha un talento. Dice ad alta voce le cose vere nel momento sbagliato."
            caino "Non farci l'abitudine. Né a lui, né alle cose vere."
            "Dentro, Druso attacca una strofa sul tradimento. Si sente fino in strada. Ha una rima per ogni mio passo."
    return

label rivalita_caino_icaro:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "La fumeria dietro la Consorteria, di mattina: sedie sui tavoli, il fumo dolce della notte ancora appeso alle travi, Icaro al tavolo piccolo coi conti."
    show caino neutro at left with dissolve
    "Caino non ci entra mai. Stamattina c'è. Si siede senza chiedere, e non gioca."
    caino "Non sono qui per le carte. Sono qui per vedere chi gioca con cosa."
    icaro "Con cosa. Hai detto cosa."
    caino "Ho detto chi. Ascolta meglio, fratello. Di solito sei tu quello che ascolta."
    show icaro irritato with qdiss
    if player_gender == "f":
        icaro "Ciò che siede al mio tavolo è a mio inventario. Non si tassa, non si presta. A te meno che a tutti."
    else:
        icaro "Il mio socio siede dove gli pare. Ma se ti siedi tu, la sedia la conto doppia."
    show caino sarcastico at left with qdiss
    caino "Hai sentito, [player_name]? Mio fratello ti ha già messo a registro. Io, almeno, chiedo il permesso prima."
    icaro "Tu chiedi il permesso come gli esattori chiedono «permesso» sulla porta. Dopo averla aperta."
    menu:
        "Due figli di Lenora, un tavolo solo. E io, a quanto pare, sono la posta."
        "«Non sono a registro di nessuno dei due.»":
            show caino neutro at left with qdiss
            caino "Corretto. Per ora."
            icaro "«Per ora.» Parola sua. Io non tratto i «per ora»: hanno scadenze ambigue."
        "Sedermi al tavolo di Icaro, come se niente fosse":
            $ icaro_affinity += 1
            $ caino_fiducia -= 1
            show icaro furbo with qdiss
            icaro "Visto, fratello? Clientela abituale. Il resto della giornata pagalo tu."
            show caino freddo at left with qdiss
            caino "Lo pago. E me lo segno. Sai cosa succede alle cose che mi segno."
        "Offrire a Caino la pipa di Icaro":
            $ caino_fiducia += 1
            $ icaro_affinity -= 1
            "Prendo la pipa dal tavolo e la porgo a Caino. Icaro mi guarda come se avessi venduto il suo magazzino."
            show caino sorpreso at left with qdiss
            caino "...grazie. Credo. Non fumo da quando avevo sedici anni."
            show icaro sorpreso with qdiss
            icaro "Non hai mai fumato. Ti ho visto provarci e tossire per un'ora."
            "Li vedo d'accordo su una cosa sola: ho appena fatto un errore. Su quale, litigano subito."
    return

label rivalita_druso_icaro:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with easeinleft
    show icaro neutro with dissolve
    "Il Becco Storto. Druso al banco, Icaro all'angolo con un registro. Non si siedono mai allo stesso tavolo. Stamattina è un problema: il tavolo libero è uno."
    druso "Fratellino! Ho saputo che [il_t] novellin[fin] passa le serate da te. Da TE. Fumo e conti. Che tortura [gli_t] infliggi?"
    icaro "La stessa che infliggi tu: la mia compagnia. Solo che la mia è sobria."
    if player_gender == "f":
        show icaro irritato with qdiss
        icaro "E non è una tortura. È una scelta. Conta le sedie, Druso: la tua è vuota, la mia no. Abituati."
    else:
        icaro "Ed è un socio, non un pubblico. Sai cos'è un socio, Druso? Uno a cui non devi soldi."
    show druso irritato at left with qdiss
    druso "Sobria. Hai sentito, linguaccia? Si vanta di essere sobrio. In una taverna. È la cosa più triste che abbia mai sentito."
    menu:
        "Mi guardano entrambi. Il tavolo libero è uno. Io pure."
        "Brindare a tutti e due: «Ai figli di Lenora, uno per sera.»":
            $ druso_affinity += 1
            show druso ghigno at left with qdiss
            druso "Uno per sera! Diplomazia da taverna! Icaro, segnatelo: è più furb[fin] di te."
            icaro "Segnato. Con la data. E l'ora in cui Druso ha ammesso che qualcuno è più furbo di qualcuno."
        "Proporre di giocarsela a carte":
            $ icaro_affinity += 1
            show icaro furbo with qdiss
            icaro "Accetto. Druso, mischia tu."
            druso "Così bari tu e perdo io? Mai. Mischia [lui_t]."
            "Mischio io. Nessuno dei due accetta il mazzo. La partita non comincia. Restano lì, col mazzo in mezzo, fino a mezzogiorno."
        "Andarmene, e lasciarli soli col tavolo":
            hide druso
            hide icaro
            with dissolve
            "Esco. Dietro di me, il Becco Storto resta zitto."
            "Poi due voci, insieme, la stessa domanda: «Dov'è andat[fin]?»"
    return

label rivalita_generica:
    scene bg corridoio_ceppo with fade
    $ renpy.show(rivali[0] + " " + RIVALI_ESPR[rivali[0]], at_list=[left])
    $ renpy.show(rivali[1] + " " + RIVALI_ESPR[rivali[1]], at_list=[right])
    with dissolve
    "Dieci giorni alla scelta del cuore. Il corridoio del Ceppo è lungo, stamattina, e ha due persone in fondo."
    "[rivali_a_nome] da una parte. [rivali_b_nome] dall'altra. Non si parlano. Si misurano."
    "Io sono il metro."
    menu:
        "Tutti e due aspettano di vedere da che parte vado."
        "Fermarmi da [rivali_a_nome]":
            $ rivali_sposta(rivali[0], rivali[1])
            "Mi fermo. [rivali_a_nome] non dice niente: non serve."
            "Alle mie spalle, [rivali_b_nome] se ne va senza fretta. Ha preso nota."
        "Fermarmi da [rivali_b_nome]":
            $ rivali_sposta(rivali[1], rivali[0])
            "Mi fermo. [rivali_b_nome] non dice niente: non serve."
            "Alle mie spalle, [rivali_a_nome] se ne va senza fretta. Ha preso nota."
        "Passare in mezzo, senza fermarmi":
            "Passo in mezzo. Due sguardi mi seguono fino in fondo al corridoio. Non si incrociano mai."
    "Vanna, più tardi, mi dice che a Rocca Tempesta lo sanno già tutti. Io non so nemmeno cosa."
    return


## Epilogo — Luna VII ########################################################
# Dopo il climax (qualunque finale, anche il neutro del semestre). Breve: una
# riga per la route attiva (secondo il finale raggiunto) e una per ogni
# personaggio non scelto (affinita' o congelamento). Nessun finale nuovo.
# Le righe reggono in tutti e tre i modi: vivo a Zefiro, lontano, morto.

label epilogo_semestre:
    python:
        if epilogo_finale in EPILOGO_MORTO:
            epilogo_modo = "morto"
        elif epilogo_finale in EPILOGO_LONTANO:
            epilogo_modo = "lontano"
        else:
            epilogo_modo = "vivo"
        # Nel finale segreto di Caino il semestre e' finito con Druso.
        if epilogo_finale == "caino_secret_end" and "druso" not in epilogo_scelti:
            epilogo_scelti = epilogo_scelti + ["druso"]
        # Soglie dalla fonte unica (routing_logic): "alta" = soglia del
        # cuore, "media" = rl.EPILOGO_MEDIA. Niente numeri qui.
        ep_soglie = rl.cuore_soglie(player_gender == "f")
        ep_media = rl.EPILOGO_MEDIA
    scene bg nero with fade
    centered "{cps=20}{size=+10}LUNA VII{/size}{/cps}"
    if epilogo_modo == "morto":
        "A Drakengrad, dicono gli Arvali, ogni storia viene raccontata per sempre. Anche quelle che continuano senza di me."
    elif epilogo_modo == "lontano":
        scene bg esterno_neve with fade
        "Le notizie di Zefiro arrivano tardi, dove sono adesso. Arrivano lo stesso: Rocca Tempesta non lascia andare niente, nemmeno le voci."
    else:
        scene bg vicoli_zefiro with fade
        "La prima Luna dopo il semestre. Zefiro accende le lanterne come sempre, una per una."
    call epilogo_route

    if "aede" not in epilogo_scelti:
        if "aede" in congelate:
            "Aede ha tolto il saluto a metà semestre. Non l'ha più restituito: con lei, le cose tolte non tornano."
        elif aede_affinity >= ep_soglie["aede"]:
            "Aede si allena all'alba, come sempre. Il posto accanto al suo, nel cortile, resta libero. Se qualcuno lo occupa, lo sposta. Con la lama."
        elif aede_affinity >= ep_media["aede"]:
            "Aede ha un novellino nuovo da squadrare, all'alba. Gli dice le stesse cose che diceva a me. Con meno veleno, giurano."
        else:
            "Aede non ricorda la mia faccia, credo. Ricorda i bersagli, non i passanti."
    if "caino" not in epilogo_scelti:
        if "caino" in congelate:
            "Caino ha chiuso la mia pratica. Alla Proprietà le pratiche chiuse non si riaprono: si archiviano in basso, dove l'umido arriva prima."
        elif caino_fiducia >= ep_soglie["caino"]:
            "Caino, in Consiglio, cita ancora una cosa che ho detto io. Senza nominarmi, ma con le mie parole, nello stesso ordine."
        elif caino_fiducia >= ep_media["caino"]:
            "Caino ricorda il mio nome. Lo usa poco e con cura, come una moneta d'oro in un borsello di rame."
        else:
            "Caino mi ha classificat[fin] a metà semestre. Non ha più riaperto la voce."
    if "druso" not in epilogo_scelti:
        if "druso" in congelate:
            "Druso ha una strofa su di me. Non la recita più. Chi l'ha sentita dice che era la più crudele del repertorio."
        elif druso_affinity >= ep_soglie["druso"]:
            "Druso ha messo un verso col mio nome nel repertorio. Lo recita solo da ubriaco. Cioè quasi sempre."
        elif druso_affinity >= ep_media["druso"]:
            "Druso dedica i versi peggiori ai Figli nuovi. Uno, il peggiore di tutti, lo tiene da parte. Dice che è riservato."
        else:
            "Druso chiede ai novellini se abbaiano o mordono. Di me non ricorda la risposta."
    if "icaro" not in epilogo_scelti:
        if "icaro" in congelate:
            "Icaro ha tirato una riga sul mio nome, a metà semestre. Dritta. Le sue righe non si cancellano: si sommano."
        elif icaro_affinity >= ep_soglie["icaro"] and player_gender == "f":
            "Al tavolo piccolo della fumeria, Icaro tiene una sedia vuota. Non la vende, non la presta. Dice che è a bilancio. Non dice di chi."
        elif icaro_affinity >= ep_soglie["icaro"]:
            "Nel registro di Icaro, alla voce «utili», c'è ancora il mio nome. Non l'ha cancellato. Con gli attivi non lo fa mai."
        elif icaro_affinity >= ep_media["icaro"]:
            "Icaro non mi conta più tra i passivi. Mi ha spostat[fin] in una colonna sua, senza intestazione."
        else:
            "Icaro vince, come il sole sorge. Al suo tavolo piccolo non c'è mai stato posto per me."
    if "ofelia" not in epilogo_scelti:
        if "ofelia" in congelate:
            "Ofelia non pronuncia il mio nome. Per lei è un nome tra tanti, e i nomi tra tanti non si pronunciano."
        elif ofelia_affinity >= ep_soglie["ofelia"]:
            "Ofelia rifiuta ancora ogni ballo. Uno solo l'ha concesso, quest'anno. Non dice a chi, e Ascadeo non riesce a quotarlo."
        elif ofelia_affinity >= ep_media["ofelia"]:
            "Ofelia ha una fila nuova di pretendenti. Li congeda col dorso della mano, come allora. Un po' più in fretta."
        else:
            "Ofelia ha una fila nuova di pretendenti. Nessuno arriva al secondo sguardo. Io, credo, non ci arrivai mai."

    # Code delle rivalita' e "un anno dopo": routes/epilogo_coda.rpy.
    call epilogo_rivali
    scene bg nero with fade
    centered "{cps=20}Il semestre è finito.\nRocca Tempesta, no.{/cps}"
    call epilogo_anno_dopo
    return

label epilogo_route:
    # Una riga sulla route attiva, coerente col finale appena giocato.
    if epilogo_finale == "good_end":
        "Aede si allena ancora all'alba. Quando centra il bersaglio, si volta a controllare che io abbia guardato. Poi nega."
    elif epilogo_finale == "neutral_end":
        "Da Zefiro arrivano voci di una volpe rossa che non sbaglia un lavoro. Uno solo, una volta. Di proposito."
    elif epilogo_finale == "bad_end_aede":
        "Aede si allena da sola, all'alba. Non chiede più a nessuno di guardare. Nessuno si offre."
    elif epilogo_finale == "bad_end_glauco":
        "Nello studio di Glauco la candela è sempre una. Aede non ci entra più. Lui non la chiama."
    elif epilogo_finale == "caino_good_end":
        "Nel registro di Caino c'è una riga scritta con un inchiostro diverso. Non la tassa. Non la archivia. La rilegge."
    elif epilogo_finale == "caino_secret_end":
        "Druso mi insegna il Codice del Teschio, un articolo a sera. Dagli spalti, Caino finge di non contare le volte che ridiamo."
    elif epilogo_finale == "caino_bad_end":
        "A Rurikstad l'idromele è buono, d'inverno. Lo bevo a piccoli sorsi, come mi era stato consigliato. Da chi, non lo dico."
    elif epilogo_finale == "caino_neutral_end":
        "La chiave del cassetto è ancora sul tavolo, tra me e Caino. Nessuno dei due la prende. Nessuno dei due la sposta."
    elif epilogo_finale == "druso_good":
        "Al Becco Storto, a fine serata, Druso recita ancora la sua strofa fuori metrica. La sala, per quella, ha imparato a stare zitta."
    elif epilogo_finale == "druso_neutral":
        "Il posto accanto a Druso, in taverna, è sempre il mio. Il foglio piegato in quattro non l'ho più visto. Non l'ho più chiesto."
    elif epilogo_finale == "druso_bad":
        "Druso fa ridere tutta Zefiro. Quando mi incrocia per strada, la battuta gli muore a metà. La finisce per qualcun altro."
    elif epilogo_finale == "icaro_good":
        "La lampada più brutta del magazzino sta sul mio davanzale. Icaro passa a controllare che ci sia ancora. Dice che è per l'inventario."
    elif epilogo_finale == "icaro_neutral":
        "Fine Luna: una busta sotto la porta, cifra esatta. Il dieci per cento di Icaro non sbaglia mai un centesimo."
    elif epilogo_finale == "icaro_bad":
        "Le serrature della fumeria sono nuove. Icaro le ha cambiate per tutti, dice. Le chiavi le ha contate lui."
    elif epilogo_finale == "icaro_bro_end":
        if rl.finale_bro(icaro_affinity, icaro_impegnato) == "icaro_bro_listino":
            "Stesso tavolo, ogni sera. Icaro guarda le carte, io le mani degli altri. Druso chiede ancora di firmare la pagina. La pagina è ancora finita."
        else:
            "Al tavolo grande della fumeria c'è un posto libero. Icaro non lo riassegna. Lo tiene a listino, a un prezzo che nessuno paga."
    elif epilogo_finale == "ofelia_good":
        "Il guanto di Ofelia è ancora nella mia tasca. A cena da Glauco si siede accanto a me, davanti a tutto il Ceppo, e non lo nomina mai."
    elif epilogo_finale == "ofelia_good_caino":
        "Il contratto a tre ha una quinta clausola, scritta in piccolo da Caino. Ofelia finge di non averla letta. L'ha letta tre volte."
    elif epilogo_finale == "ofelia_good_aede":
        "Aede mi saluta alla luce, Ofelia al buio. Due sorelle, due orari. Nessuna delle due sbaglia mai l'ora."
    elif epilogo_finale == "ofelia_bad_tempesta":
        "A Zefiro le figlie di Glauco non si parlano più. Ascadeo ha chiuso il suo libro di scommesse: dice che non c'è più niente da quotare."
    elif epilogo_finale == "ofelia_passeggero":
        "Il guanto di Ofelia è ancora nella mia tasca. Non l'ho restituito. Lei non l'ha chiesto. Lo teniamo così, senza dircelo."
    elif epilogo_finale == "ofelia_bad":
        "Il drappo col fiocco del Ceppo è in fondo a un baule. Mia madre non l'ha aperto. Dice che certi doni si rispettano chiusi."
    elif epilogo_finale == "ofelia_neutral":
        "Ofelia ha un pretendente nuovo. Ascadeo, nel suo libretto, ha già quotato anche quello. Basso."
    elif epilogo_finale == "finale_neutro_semestre":
        "Briseide mi versa il brodo per prim[fin], adesso. Nel Ceppo dicono che sia un onore. Io dico che è brodo, ed è buono."
    else:
        "Il semestre ha chiuso i suoi conti. Alcuni in attivo."
    # Poly segreto con Aede finito in un finale di Aede: Ofelia era uscita
    # nella neve, e merita la sua riga.
    if "ofelia" in epilogo_scelti and epilogo_finale in ("good_end", "neutral_end", "bad_end_aede", "bad_end_glauco"):
        "Ofelia, a Zefiro, non pronuncia il mio nome. Ascadeo lo tiene in fondo al libretto, senza quota."
    # E il contrario: Ofelia sola nel good, la coda amara. Aede ha visto
    # la neve, e merita la sua riga.
    if "aede" in epilogo_scelti and epilogo_finale == "ofelia_good":
        "Aede si allena all'alba, da sola. Quando passo dal cortile non si volta. Ma il bersaglio, il giorno dopo, è un passo più vicino al cancello."
    return
