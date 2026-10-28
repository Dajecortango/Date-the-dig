"""Motore puro delle conseguenze: scelte registrate, fatti, echi, albero.

Nessun import Ren'Py: importabile sia dal gioco (init python) sia dai test.
Un fatto e' un dict con chiavi: id, char, testo, avviso (o None), cond
(callable(vars) -> bool). Un eco e' un dict con chiavi: id, fatto, luoghi
(id di attivita'), label, cond opzionale.
"""

# Slot da lasciar passare prima che un fatto torni come eco: il
# pettegolezzo ha bisogno di tempo per viaggiare.
ECO_RITARDO = 2


def firma_menu(contesto, voci):
    """Identita' stabile di un menu: contesto + didascalia o prima opzione.
    voci = [(testo, selezionabile)]; la didascalia ha selezionabile False."""
    didascalie = [t for t, ok in voci if not ok]
    opzioni = [t for t, ok in voci if ok]
    chiave = didascalie[0] if didascalie else (opzioni[0] if opzioni else "")
    return "%s|%s" % (contesto or "inizio", chiave)


def contesto_di(firma):
    return firma.split("|", 1)[0]


def registra_scelta(scelte, viste, scelte_storiche, firma, opzioni, scelta):
    """Aggiorna scelte (partita), viste (firma -> opzioni in ordine) e
    scelte_storiche (set di (firma, testo)). Idempotente: rigiocare la
    stessa scelta in rollback non cambia niente."""
    elenco = viste.setdefault(firma, [])
    for o in opzioni:
        if o not in elenco:
            elenco.append(o)
    if scelta is not None:
        scelte[firma] = scelta
        scelte_storiche.add((firma, scelta))


def scelto(scelte, contesto, prefisso):
    """True se in questa partita, nel contesto, e' stata scelta un'opzione
    che comincia con prefisso."""
    for firma, testo in scelte.items():
        if contesto_di(firma) == contesto and testo.startswith(prefisso):
            return True
    return False


def nuovi_fatti(fatti, vars, noti):
    """Id dei fatti con cond vera non ancora in noti, nell'ordine del
    registry."""
    return [f["id"] for f in fatti
            if f["id"] not in noti and bool(f["cond"](vars))]


def pesca_eco(echi, luogo, noti, visti, ora, vars, ritardo=ECO_RITARDO):
    """Primo eco del luogo non ancora visto, col fatto noto da almeno
    ritardo slot (noti: id -> (contesto, momento)). None se nessuno."""
    for e in echi:
        if e["id"] in visti or luogo not in e["luoghi"]:
            continue
        nato = noti.get(e["fatto"])
        if nato is None or ora - nato[1] < ritardo:
            continue
        cond = e.get("cond")
        if cond is None or cond(vars):
            return e["id"]
    return None


def stato_nodo(eid, visti_partita, visti_storici):
    if eid in visti_partita:
        return "vissuto"
    if eid in visti_storici:
        return "altrove"
    return "ignoto"


def opzioni_nodo(eid, scelte, viste, scelte_storiche):
    """Menu del nodo: [(didascalia, [(testo, stato)])] con stato in
    'scelta' (questa partita), 'passata' (altre partite), 'mai'."""
    out = []
    for firma, opzioni in viste.items():
        if contesto_di(firma) != eid:
            continue
        righe = []
        for o in opzioni:
            if scelte.get(firma) == o:
                righe.append((o, "scelta"))
            elif (firma, o) in scelte_storiche:
                righe.append((o, "passata"))
            else:
                righe.append((o, "mai"))
        out.append((firma.split("|", 1)[1], righe))
    return out


def albero(nodi, visti_partita, visti_storici, scelte, viste,
           scelte_storiche, noti, fatti):
    """nodi = [(id, titolo, luna)] nell'ordine del racconto. Ritorna
    [(id, titolo, luna, stato, menu, fatti_del_nodo)]; fatti_del_nodo =
    testi dei fatti nati in quel nodo.
    I menu si mostrano solo per i nodi visti almeno una volta."""
    testi = {f["id"]: f["testo"] for f in fatti}
    out = []
    for eid, titolo, luna in nodi:
        stato = stato_nodo(eid, visti_partita, visti_storici)
        menu = ([] if stato == "ignoto"
                else opzioni_nodo(eid, scelte, viste, scelte_storiche))
        nati = [testi[fid] for fid, (ctx, _ora) in noti.items()
                if ctx == eid and fid in testi]
        out.append((eid, titolo, luna, stato, menu, nati))
    return out


def fatti_sciolti(nodi, noti, fatti, char):
    """Fatti del personaggio nati fuori dai nodi (attivita', incroci)."""
    ids_nodi = {n[0] for n in nodi}
    return [f["testo"] for f in fatti
            if f["char"] == char and f["id"] in noti
            and noti[f["id"]][0] not in ids_nodi]


def origliato_id(a, b):
    """Id della scena origliata di una coppia, indipendente dall'ordine."""
    return "orig_" + "_".join(sorted((a, b)))


def origliato_ok(visti, congelate, luna, a, b, primi):
    """Due personaggi parlano di te mentre non ci sei: solo in Lune II-IV,
    se entrambi ti conoscono (primo evento della loro route visto), se
    almeno uno dei due non ti ha chiuso la porta, una volta per partita."""
    return (2 <= luna <= 4
            and primi[a] in visti and primi[b] in visti
            and not (a in congelate and b in congelate)
            and origliato_id(a, b) not in visti)


# Opzioni di menu riscritte (vecchio testo -> nuovo). Lo storico delle
# partite gia' giocate si migra con migra_storico, cosi' l'albero della
# Trama non perde le scelte. Riempita dall'audit delle scelte approvato.
OPZIONI_RINOMINATE = {
    "Restituirlo chiuso": "Restituiscigli il foglio senza leggerlo",
    "Prenderla": "Prendi la chiave del magazzino",
    "Rifiutarla": "Lasciagli la chiave",
    "Aspettare ancora": "Rimandare il saldo dei sei Scudi",
    # Costo uniforme "(N Scudi)" nelle scelte che spendono.
    "Offrire un giro a tutto il tavolo": "Offrire un giro a tutto il tavolo (1 Scudo)",
    "Comprargli una lanterna nuova per il Ceppo": "Comprargli una lanterna nuova per il Ceppo (2 Scudi)",
    # Copione Caino aggiornato: opzioni all'imperativo, Aulo -> Eumene.
    "Restare in silenzio e sorridere": "Resta in silenzio e sorridi",
    "Fermare il servo: «L'Arconte beve idromele di Rurikstad.»": "Ferma il servo: «L'Arconte beve idromele di Rurikstad.»",
    "Prendere la coppa e ringraziare": "Prendi la coppa e ringrazia",
    "Aspettare di vedere se la beve": "Aspetta di vedere se beve",
    "Accettare e lasciarlo condurre": "Accetta e lascialo condurre",
    "Accettare, ma giocare a condurre io": "Accetta, ma punta a condurre tu",
    "Rifiutare con un inchino": "Rifiuta con un inchino",
    "Accettare la gara": "Accetta la gara",
    "Declinare con diplomazia": "Declina con diplomazia",
    "«Trentun anni. Concedigli l'esilio, non le Segrete.»": "«Dieci anni. Concedigli l'esilio, non le Segrete.»",
    "Tacere e lasciare decidere l'Arconte": "Taci e lascia decidere l'Arconte",
    "«Hai fatto bene. Aulo era un peso.»": "«Hai fatto bene. Eumene era un peso.»",
    "Tacere e bere": "Taci e bevi",
    "Bere in silenzio e restare": "Bevi in silenzio e resta con Druso",
    # Copione Aede aggiornato: opzioni all'imperativo e testi rivisti.
    "Tenere il passo in silenzio, senza chiedere nulla": "Tieni il passo in silenzio, senza chiedere nulla",
    "Chiederle cosa c'è dentro la cassetta": "Chiedile cosa c'è dentro la cassetta",
    "Lamentarmi del peso": "Lamentati del peso",
    "Tifare per lei a squarciagola": "Tifa per lei a squarciagola",
    "Aiutarla senza farmi vedere": "Aiutala senza farti vedere",
    "Iscrivermi alla corsa aperta e sfidarla": "Iscriviti alla corsa e sfidala",
    "Ignorare la gara e andarmene presto": "Ignora la gara e vai via presto",
    "«Non ancora. Non così.»": "«Non ancora. Non sono sicur[fin] di essere pront[fin].»",
    "«Il tuo Ceppo salda. Ho capito. Non ho visto niente.»": "«Il tuo Ceppo salda, ho capito. Non ho visto niente.»",
    "«Chi era per te, quest'uomo? Cosa ti costa, questo lavoro?»": "«Chi era per te quest'uomo? Quanto ti costa questo lavoro?»",
    "Prenderle la mano": "Prendile la mano",
    "Camminarle accanto, senza toccarla": "Camminale accanto, senza toccarla",
    "Restare qualche gradino indietro": "Resta qualche gradino indietro",
    "Fermarla. «Il tuo nome di prima è morto. Io voglio quella viva.»": "Fermala. «Il tuo nome di prima è morto. Io voglio quella viva.»",
    "Ascoltarla fino in fondo": "Ascoltala fino in fondo",
    "Fermarla e offrirle il mio, di passato": "Fermala e offrile il tuo passato",
    "Parlarle, un'ultima volta": "Parlale un'ultima volta",
    "Restare in silenzio e guardarla negli occhi": "Resta in silenzio e guardala negli occhi",
    "Tendere la mano, aperta": "Tendi la mano, aperta",
    # Copione parti comuni aggiornato: opzioni all'imperativo e testi rivisti.
    "Tacere, e chinare la testa": "Taci e china la testa",
    "Dare ragione ad Aede, a voce bassa": "Dai ragione ad Aede, a voce bassa",
    "Dare ragione a Ofelia, con un mezzo sorriso": "Dai ragione a Ofelia, con un mezzo sorriso",
    "Restare sedut[fin] accanto a Druso": "Resta sedut[fin] accanto a Druso",
    "Seguire Caino fuori": "Segui Caino fuori",
    "Sedermi al tavolo di Icaro, come se niente fosse": "Mi siedo al tavolo di Icaro, come se niente fosse",
    "Offrire a Caino la pipa di Icaro": "Offri a Caino la pipa di Icaro",
    "Brindare a tutti e due: «Ai figli di Lenora, uno per sera.»": "Brinda a tutti e due: «Ai figli di Lenora, uno per sera.»",
    "Proporre di giocarsela a carte": "Proponi di giocarsela a carte",
    "Andarmene, e lasciarli soli col tavolo": "Vattene e lasciali soli al tavolo",
    "Fermarmi da [rivali_a_nome]": "Fermati da [rivali_a_nome]",
    "Fermarmi da [rivali_b_nome]": "Fermati da [rivali_b_nome]",
    "Passare in mezzo, senza fermarmi": "Passa in mezzo, senza fermarti",
    "Ridere con Druso, forte": "Ridi con Druso, forte",
    "Aiutare Icaro a recuperare le monete, contandole": "Aiuta Icaro a recuperare le monete, contandole",
    "Citare il Codice del Teschio: «si dichiara PRIMA di colpire»": "Cita il Codice del Teschio: «si dichiara PRIMA di colpire»",
    "Applaudire lei: «Pulito. Insegnamelo.»": "Applaudi lei: «Pulito. Insegnamelo.»",
    "Tendere la mano a Druso con un verso: «Cadde il poeta, ma cadde rimando»": "Tendi la mano a Druso con un verso: «Cadde il poeta, ma cadde rimando»",
    "Restare neutrale: qui si rischia la pelle": "Resta neutrale: qui si rischia la pelle",
    "Tacere: al tavolo di Icaro, chi guarda non parla": "Taci: al tavolo di Icaro, chi guarda non parla",
    "Proporre il doppio o niente, mazzo nuovo e mescolo io": "Proponi il doppio o niente, mazzo nuovo e mescoli tu",
    "Leggere ad alta voce la pagina di Druso, cifra per cifra": "Leggi ad alta voce la pagina di Druso, cifra per cifra",
    "Chiudere il registro con una mano: «Non stamattina.»": "Chiudi il registro con una mano: «Non stamattina.»",
    "Chiedere a Ofelia come si legge un filo": "Chiedi a Ofelia come si legge un filo",
    "Dare ragione ad Aede: «Pesa diversa, si vede»": "Dai ragione ad Aede: «Pesa diversa, si vede»",
    "Restare in silenzio e guardare il piede di Aede": "Resta in silenzio e guarda il piede di Aede",
    "Contare a voce alta le bocche di calore, per Caino": "Conta a voce alta le bocche di calore, per Caino",
    "Prendere le parti di Ofelia: «La primavera non si tassa»": "Prendi le parti di Ofelia: «La primavera non si tassa»",
    "Chiedere a Caino quanto vale, a registro, un fiore che non fiorisce": "Chiedi a Caino quanto vale, a registro, un fiore che non fiorisce",
    "Eseguire senza discutere, fino a sbagliare di meno": "Esegui senza discutere, fino a sbagliare di meno",
    "Chiederle di mostrarmi il colpo, lentamente": "Chiedile di mostrarti il colpo, lentamente",
    "Lamentarmi del turno all'alba": "Lamentati del turno all'alba",
    "Colpire la moneta, non il bersaglio": "Colpisci la moneta, non il bersaglio",
    "Colpire il bersaglio, come da consegna": "Colpisci il bersaglio, come da consegna",
    "Ignorarlo e prendere uno scudo in silenzio": "Ignoralo e prendi uno scudo in silenzio",
    "Scusarmi e mettermi in fondo alla fila": "Scusati e mettiti in fondo alla fila",
    "Attaccare per primo, senza aspettare il segnale": "Attacca in anticipo, senza aspettare il segnale",
    "Aspettare il segnale, da regolamento": "Aspetta il segnale, da regolamento",
    "Rifiutare la lotta": "Rifiuta la lotta",
    "«Metrica zoppa. Il contenuto peggio. Bis.»": "«Metrica zoppa. Il contenuto arranca. BIS!»",
    "Applaudire educatamente": "Applaudi educatamente",
    "«Dichiara pure. Ma stanotte dormi con un occhio aperto.»": "«Parla pure. Ma stanotte dormi con un occhio aperto.»",
    "Cambiare discorso": "Cambia discorso",
    "Tacere e perdere l'ottavo Scudo con dignità": "Taci e perdi l'ottavo Scudo con dignità",
    "Sussurrare «bel taglio» a voce bassissima": "Sussurra «bel taglio» a voce bassissima",
    "Gridare al baro": "Grida al baro",
    "Sedermi e stare zitt[fin], godendomi la calma": "Mi siedo e sto zitt[fin], godendomi la calma",
    "Chiedergli quanto ha vinto stasera": "Chiedigli quanto ha vinto stasera",
    "Confessare che non la pulisco da una settimana": "Confessa che non la pulisci da una settimana",
    "«Druso Lenorio, poeta di taverna: rima con 'cena' e con 'vena', ma mai con 'sostanza'.»": "«Druso Lauro, poeta di taverna: rima con 'cena' e con 'vena', ma mai con denaro.»",
    "Rispondere con un verso sconcio, il più sporco che mi viene": "Rispondi con un verso sconcio, il più sporco che ti viene in mente",
    "Guardare e basta, com'è gratis": "Guarda e basta, è gratis",
    "Avvicinarmi, piano": "Mi avvicino, piano",
    "Andarmene. Quello che dicono di me, se lo tengano": "Me ne vado. Quello che dicono di me, se lo tengano",
    # Copioni Druso, Icaro e Ofelia aggiornati: opzioni all'imperativo e testi rivisti.
    "Rovesciargli il boccale addosso": "Rovesciagli il boccale addosso",
    "Prenderla e attaccarlo senza preavviso": "Prendila e attaccalo senza preavviso",
    "Sedermi accanto a lui e guardare gli altri": "Siediti accanto a lui a guardare gli altri",
    "«Vendimi pure. Ma ricorda che poi la leva si gira.»": "«Vendimi pure. Ma ricorda che poi la ruota gira.»",
    "Dirgli il nome: in fondo siamo amici": "Digli il nome: in fondo siamo amici",
    "Minacciarlo: se parla, lo denuncio al Consiglio": "Minaccialo: se parla, lo denunci al Consiglio",
    "Mangiare in silenzio e lasciarli scannare": "Mangia in silenzio e lasciali scannare",
    "Chiuderlo e porgerglielo. Senza una parola": "Chiudilo e porgiglielo. Senza una parola",
    "Rimetterlo sotto la panca prima che si avvicini": "Rimettilo sotto la panca prima che si avvicini",
    "Prendere il foglio senza ridere": "Prendi il foglio senza ridere",
    "Intervenire, adesso": "Intervieni subito",
    "Dargli retta e andarcene": "Dagli retta e andate via",
    "«Icaro, se racconti questa cosa, racconto io della tua pipa.»": "«Icaro, se racconti questa cosa, io racconto della tua pipa.»",
    "Ignorarlo e continuare la lezione": "Ignoralo e continua la lezione",
    "Prenderlo in giro: «Il coraggioso Druso e le sue ombre»": "Prendilo in giro: «Il coraggioso Druso e le sue ombre»",
    "Mettersi in silenzio al suo fianco": "Mettiti in silenzio al suo fianco",
    "Prenderlo per il braccio: «Andiamo. Non ne vale la pena.»": "Prendilo per il braccio: «Andiamo. Non ne vale la pena.»",
    "Restare al tavolo, in silenzio. Tocca a lui.": "Resta al tavolo, in silenzio. Tocca a lui.",
    "«Non portarti una poesia. Portati te stesso.»": "«Non portarti una poesia. Porta te stesso.»",
    "Strappargli la lettera e bruciarla sulla candela": "Strappagli la lettera e bruciala sulla candela",
    "Raccogliere una palla di neve e tirargliela in faccia": "Raccogli una palla di neve e tiragliela in faccia",
    "Sedermi accanto a lui e aspettare": "Siediti accanto a lui e aspetta",
    "Alzarmi e parlare per lui": "Alzati e parla per lui",
    "Restare sedut[fin], e guardarlo. La voce è sua": "Resta sedut[fin], e guardalo. La voce è sua",
    "Smontare la cosa con una battuta": "Smonta la cosa con una battuta",
    "«Ho contato ogni carta. Tutto regolare.» (mentire per lui)": "«Ho contato ogni carta. Tutto regolare.» (menti per lui)",
    "Tacere e guardare altrove": "Taci e guarda altrove",
    "Dare ragione al mercante": "Dai ragione al mercante",
    "Aggiungere una riga alla pagina di Druso": "Aggiungi una riga alla pagina di Druso",
    "Chiudere il registro senza leggere oltre": "Chiudi il registro senza leggere oltre",
    "«E ogni cosa qui dentro ha una storia. Raccontamene una.»": "«Se ogni cosa qui dentro ha una storia, raccontamene una.»",
    "Sollevare una tazza del servizio di Glostok, controluce": "Solleva una tazza del servizio di Glostok, controluce",
    "Indicare una lanterna e prendere la moneta con l'altra mano": "Indica una lanterna e prendi la moneta con l'altra mano",
    "Fargli una domanda vera, e prenderla mentre risponde": "Fagli una domanda vera, e prendi la moneta mentre risponde",
    "Rifiutare: «Non rubo ai soci.»": "Rifiuta: «Non rubo ai soci.»",
    "«Il pettine valeva mezzo Scudo. L'osso era di vacca, non di Glostok.»": "«Il pettine valeva mezzo Scudo, era dozzinale, non di Glostok.»",
    "Restare in silenzio e passargli la lanterna": "Resta in silenzio e passagli la lanterna",
    "Restare zitto, braccia conserte, e guardare l'uscita": "Resta zitto, braccia conserte, e guarda altrove",
    "Inventare un'offerta migliore, a un altro banco": "Inventa un'offerta migliore a un altro banco",
    "Indicare il bollo sotto un piattino: è ridipinto": "Indica lo stemma sotto un piattino: è ridipinto",
    "Fingermi ubriaco e chiedere la strada per il Becco Storto": "Fingiti ubriaco e chiedi la strada per il Becco Storto",
    "Restare fermo nell'ombra, senza respirare": "Resta fermo nell'ombra, senza respirare",
    "Fare un fischio basso, come quello dei lanternai": "Fai un fischio basso, come quello dei lanternai",
    "Rovesciare il bicchiere sul panno: carte fradice, mano nulla": "Rovescia il bicchiere sul panno: carte fradice, mano nulla",
    "«L'anello, Arconte. Il castone. Fa da specchio dall'inizio della sera.»": "«L'anello, Pallante. Il castone. Fa da specchio dall'inizio della sera.»",
    "Restare in silenzio. È la sua partita": "Resta in silenzio. È la sua partita",
    "Chiedergli cosa va scritto lì": "Chiedigli cosa va scritto lì",
    "Leggere il totale del semestre, come se niente fosse": "Leggi il totale del semestre, come se niente fosse",
    "Accendergli la pipa, senza chiedere": "Accendigli la pipa, senza chiedere",
    "Prendere la penna e continuare l'inventario al posto suo": "Prendi la penna e continua l'inventario al posto suo",
    "Andare a chiamare Corrado: lui sa di erbe": "Vai a chiamare Corrado: lui si intende di medicina",
    "Fare come chiede: andarmene e chiudere la porta": "Vai via e chiudi la porta",
    "«Ti fermi mezzo respiro prima di dire la verità. Mai prima di una bugia.»": "«Ti fermi mezzo respiro prima di dire la verità e mai prima di una bugia.»",
    "Prendergli la pipa, tirare una boccata, rendergliela. Senza una parola": "Prendigli la pipa, tira una boccata e rendigliela. Senza una parola",
    "Restare in silenzio, a guardare i fiori": "Resta in silenzio a guardare i fiori",
    "Dargli ragione: «Un orso, certo. Enorme.»": "Dagli ragione: «Un orso, certo. Enorme.»",
    "Svignarmela prima che mi tiri in mezzo": "Svignatela prima che ti tiri in mezzo",
    "Aiutarla a raccogliere gli steli tagliati": "Aiutala a raccogliere gli steli tagliati",
    "Ridere con gli altri: in fondo è teatro": "Ridi con gli altri: in fondo è teatro",
    "Fare un passo avanti: «Basta, Ofelia. Lascialo andare.»": "Fai un passo avanti: «Basta, Ofelia. Lascialo andare.»",
    "Restare immobile, senza ridere e senza intervenire": "Resta immobile, senza ridere e senza intervenire",
    "Stare al gioco, con stile: baciarle la mano come se fosse mia da sempre": "Stai al gioco, con stile: baciale la mano come se fosse tua da sempre",
    "Dirlo in faccia, piano: «Mi stai usando, Ofelia. Lo faccio volentieri, ma voglio che tu lo sappia.»": "Dille in faccia, piano: «Mi stai usando, Ofelia. Lo faccio volentieri, ma voglio che tu lo sappia.»",
    "Fare una scenata: «Io che ci faccio qui? Dimmelo davanti a lui!»": "Fai una scenata: «Io che ci faccio qui? Dimmelo davanti a lui!»",
    "Prendere la cote e affilare la lama in silenzio": "Prendi la cote e affila la lama in silenzio",
    "Leggere tutto, nota compresa": "Leggi tutto, nota compresa",
    "Leggere solo la cifra, e tacere la nota": "Leggi solo la cifra, non la nota",
    "Bruciarla alla torcia senza leggerla": "Bruciala con la torcia senza leggerla",
    "«Nessuno. Il tuo gioco, giocalo da sola.»": "«Nessuno. Gioca da sola.»",
    "Prendere le forbici: «Resto. Anche senza gentilezza.»": "Prendi le forbici: «Resto. Anche senza gentilezza.»",
    "Lasciarle le forbici: «Non ancora, Ofelia.»": "Lasciale le forbici: «Non ancora, Ofelia.»",
    "Reggere il suo sguardo: «Colpisci pure. Non chiederò pietà.»": "Reggi il suo sguardo: «Colpisci pure. Non chiederò pietà.»",
    "Arrendermi con eleganza: «Hai vinto. Ma ti è costato fatica, ammettilo.»": "Arrenditi con eleganza: «Hai vinto. Ma ti è costato fatica, ammettilo.»",
    "Chiedere pietà, ridendo, con le mani in alto": "Chiedi pietà, ridendo, con le mani in alto",
    "Prenderle la mano e scendere senza dire niente": "Prendile la mano e scendi senza dirle niente",
    "Baciarle la mano, come vuole il gesto": "Baciale la mano, come vuole il gesto",
    "Prendere entrambe le mani: «Che guardino.»": "Prendi entrambe le mani: «Che guardino.»",
    "Proporre di scendere a turno, per non dare spettacolo": "Proponi di scendere a turno, per non dare spettacolo",
    "Andare da Aede: stanotte la mano è sua": "Vai da Aede: stanotte la mano è sua",
    "Prendere la mano di Ofelia": "Prendi la mano di Ofelia",
    "Alla luce del sole: toglierle il velo e offrirle il braccio": "Alla luce del sole: toglile il velo e offrile il braccio",
    "Prendere la pergamena e porgerla a Ofelia, dal lato della candela": "Prendi la pergamena e porgila a Ofelia, dal lato della candela",
    "Rispondere a Glauco a testa alta: «Non firmo. Resta lei, e resto io.»": "Rispondi a Glauco a testa alta: «Non firmo. Resta lei, e resto io.»",
    "Prendere le sue difese: «Non decidete voi per lei.»": "Prendi le sue difese: «Non decidete voi per lei.»",
}


def rinomina_firma(firma, mappa):
    """Firma con la chiave (didascalia o prima opzione) rinominata."""
    contesto, _, chiave = firma.partition("|")
    if chiave in mappa:
        return "%s|%s" % (contesto, mappa[chiave])
    return firma


def migra_storico(scelte, viste, scelte_storiche, mappa):
    """In place: firme e testi vecchi -> nuovi in scelte (partita), viste
    (firma -> opzioni in ordine) e scelte_storiche (set di (firma, testo)).
    Le liste di viste si uniscono senza doppioni, nell'ordine di comparsa.
    Idempotente."""
    if not mappa:
        return
    nuove_scelte = {}
    for firma, testo in scelte.items():
        nuove_scelte[rinomina_firma(firma, mappa)] = mappa.get(testo, testo)
    scelte.clear()
    scelte.update(nuove_scelte)
    nuove_viste = {}
    for firma, opzioni in viste.items():
        elenco = nuove_viste.setdefault(rinomina_firma(firma, mappa), [])
        for o in opzioni:
            o = mappa.get(o, o)
            if o not in elenco:
                elenco.append(o)
    viste.clear()
    viste.update(nuove_viste)
    nuove_storiche = {(rinomina_firma(f, mappa), mappa.get(t, t))
                      for f, t in scelte_storiche}
    scelte_storiche.clear()
    scelte_storiche.update(nuove_storiche)
