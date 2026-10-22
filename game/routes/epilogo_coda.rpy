# Epilogo: code delle rivalita' (dentro Luna VII) e "un anno dopo" (dopo la
# chiusura del semestre). Chiamate da epilogo_semestre (snodi.rpy).
# Le righe reggono in tutti e tre i modi (epilogo_modo vivo/lontano/morto):
# parlano di chi resta, mai di cosa il protagonista fa adesso.

init python:
    # Rivalita' di IV/18: (coppia ordinata, chi e' stato scelto) -> riga su
    # chi e' rimasto fuori. Il "corridoio" e' la variante generica della
    # rivalita'; le coppie con scena propria citano la loro (serra, Becco
    # Storto, fumeria). Si aggiungono alla riga per-personaggio di
    # epilogo_semestre: qui solo il legame con la rivalita'.
    RIVALI_CODE = {
        ("aede+caino", "aede"):
            "Caino ha chiuso la pratica di quella mattina in corridoio con una riga sola: «ceduto al Ceppo di Glauco». In Consiglio, quando Aede passa, le cede il passo. È l'unica cosa che le cede.",
        ("aede+caino", "caino"):
            "Aede non ha mai chiesto a Caino di quella mattina in corridoio. Ma quando lui attraversa il cortile d'armi, la sua lama va più veloce. Caino finge di non contare i colpi. Li conta.",
        ("aede+druso", "aede"):
            "Druso ha una strofa su quella mattina in corridoio: lui da una parte, la volpe rossa dall'altra. La recita solo quando Aede non c'è. Cioè con molta prudenza.",
        ("aede+druso", "druso"):
            "Aede, in palestra, non ride più alle battute di Druso. Lui se n'è accorto, e ne fa di peggiori apposta, per vedere se cede. Dalla mattina del corridoio, non cede.",
        ("aede+icaro", "aede"):
            "Icaro ha messo a bilancio quella mattina in corridoio: «posizione persa contro una lama». Dice che con le lame non si tratta. Lo dice con rispetto, per una volta.",
        ("aede+icaro", "icaro"):
            "Aede non entra in fumeria nemmeno per servizio. Icaro le ha mandato un biglietto, uno solo: «Nessun debito tra noi». Lei l'ha bruciato senza aprirlo. Lui l'aveva scritto apposta su carta che brucia male.",
        ("aede+ofelia", "aede"):
            "La seconda sedia della serra è sparita il giorno dopo quella mattina in corridoio. A cena da Glauco, Ofelia passa il sale alla sorella senza guardarla. Ascadeo lo quota come armistizio.",
        ("aede+ofelia", "ofelia"):
            "Aede non ha più detto «le mie cose». A cena da Glauco si siede dal lato opposto a Ofelia, da quella mattina in corridoio. Il tavolo è lungo. Lo usano tutto.",
        ("caino+druso", "caino"):
            "Al Becco Storto Druso ha una strofa sul fratello che «deposita i sentimenti sotto il calamaio». La attacca ogni volta che Caino entra. Caino paga il giro. È il loro modo di non parlarne.",
        ("caino+druso", "druso"):
            "Caino non ha più messo piede al Becco Storto. Il conto di quella mattina l'ha saldato lui, però, con una nota a margine. Druso non l'ha mai letta ad alta voce. È l'unica cosa che non legge ad alta voce.",
        ("caino+icaro", "caino"):
            "Al tavolo piccolo della fumeria la sedia costa doppio, per un cliente solo. Caino non ci si è mai seduto. Icaro gliela mette in conto lo stesso, ogni fine Luna, per principio.",
        ("caino+icaro", "icaro"):
            "Caino ha aperto una pratica sulla fumeria dietro la Consorteria. Non la chiude, non la porta in Consiglio. La tiene lì, come una pipa che non si fuma dai sedici anni.",
        ("caino+ofelia", "caino"):
            "A fine semestre Ofelia ha fatto avere a Caino un fiore della serra. Nero, senza biglietto. Caino l'ha pressato in un registro, tra due decime. Sanno tutti e due cosa voleva dire quella mattina in corridoio.",
        ("caino+ofelia", "ofelia"):
            "Quando Ofelia entra in Consiglio, Caino si alza. È l'unico. Lei non lo ringrazia: da quella mattina in corridoio, tra loro due i conti si tengono in silenzio.",
        ("druso+icaro", "druso"):
            "Al Becco Storto il tavolo libero è ancora uno. Icaro ci si siede quando Druso non c'è, e lascia pagato il giro dopo. Druso finge di non sapere chi paga. Lo sa al centesimo.",
        ("druso+icaro", "icaro"):
            "Druso ha una strofa nuova sul fratellino «sobrio in una taverna». La sala ride. Lui, a fine strofa, guarda verso la fumeria. Non ci entra.",
        ("druso+ofelia", "druso"):
            "Ofelia ha congedato Druso dalla fila dei pretendenti con una frase sola, il giorno dopo quella mattina in corridoio. Lui l'ha messa in rima. È la strofa più applaudita del Becco Storto. Ofelia dice di non averla mai sentita.",
        ("druso+ofelia", "ofelia"):
            "Druso non fa più il cascamorto con la figlia di Glauco. Lo fa con tutte le altre, a voce più alta, da quella mattina in corridoio. Ascadeo dice che è il suo modo di stare zitto.",
        ("icaro+ofelia", "icaro"):
            "Per una Luna intera Ofelia ha mandato a Icaro un pretendente al giorno, tutti col vizio delle carte. Icaro li ha spennati uno per uno. Nessuno dei due l'ha mai chiamata vendetta.",
        ("icaro+ofelia", "ofelia"):
            "Nel libretto di Ascadeo c'è una scommessa di Icaro sulla serra: l'unica che abbia mai perso. Non l'ha cancellata. Dice che le perdite insegnano più dei guadagni. Non dice cosa.",
    }

    def epilogo_rivali_riga(coppia, scelti):
        """Riga sulla rivalita' di IV/18 se esattamente uno dei due rivali e'
        stato scelto; None altrimenti (nessuna rivalita', nessuno o entrambi
        scelti, come nel poliamore o nel finale segreto di Caino)."""
        if not coppia or "+" not in coppia:
            return None
        dentro = [c for c in coppia.split("+") if c in scelti]
        if len(dentro) != 1:
            return None
        return RIVALI_CODE.get((coppia, dentro[0]))

    # "Un anno dopo": Vanna e Corrado (ceppo_esito), per modo.
    ANNO_CEPPO = {
        "parte": "Corrado scrive da Hammergrad una volta a Luna, con le date giuste. Vanna legge le lettere ad alta voce in cucina e le corregge lo stesso, a matita, prima di rispondere.",
        "resta": "Corrado insegna gli stemmi alla nuova leva del Ceppo. La lettera degli Arvali è ancora nel libro di araldica, alla pagina del leone. Vanna sa dov'è. Non la tocca.",
        "insieme": "Da Hammergrad arrivano lettere con due calligrafie. Una ha le date giuste. L'altra racconta dei segreti dei morti del Nord, e gli Arvali, dicono, hanno cominciato a parlare.",
        None: "Vanna e Corrado sono ancora nel Ceppo di Briseide. Lei racconta, lui corregge le date. Da Hammergrad, una volta, è arrivata una lettera col sigillo del fiume. È finita nel camino.",
    }
    ANNO_CEPPO_MORTO = {
        "parte": "Nell'ultima lettera da Hammergrad Corrado ha scritto di aver ricopiato un nome nei registri del Margine. Uno che conosceva. Vanna ha letto quella riga una volta sola, e poi più.",
        "resta": "Corrado ha scritto un nome sul margine del libro di araldica, alla pagina del leone. Lo ha scritto lui, perché gli Arvali sono lontani e i nomi, nel Ceppo, non si lasciano ai forestieri.",
        "insieme": "Da Hammergrad Vanna scrive che i registri del Margine hanno un nome nuovo, ricopiato da Corrado con la mano ferma. Lei ha corretto la data. Era giusta. L'ha corretta lo stesso.",
        None: "Vanna e Corrado sono ancora nel Ceppo di Briseide. A cena, da un anno, Vanna sbaglia le date di proposito. Corrado non la corregge più.",
    }

    def anno_dopo_righe():
        """3-5 righe per "un anno dopo", dai fatti e dallo stato. Mai il
        protagonista al presente: reggono i tre modi e ogni finale."""
        modo = store.epilogo_modo
        noti = store.fatti_noti
        righe = []
        esito = store.ceppo_esito
        tabella = ANNO_CEPPO_MORTO if modo == "morto" else ANNO_CEPPO
        righe.append(tabella.get(esito, tabella[None]))
        # Briseide e il nodo di corda.
        if modo == "morto":
            righe.append("Briseide ricorda tutti i suoi Figli: nome, data, motivo. Al mio nome, dicono, si ferma un respiro più a lungo. Poi rimesta il brodo, perché i vivi hanno fame.")
        elif modo == "lontano":
            righe.append("Le lettere di Briseide arrivano una volta a Luna, legate con un pezzo di corda. Dice che il nodo del primo anno non si scioglie per posta: aspetta che io torni.")
        else:
            righe.append("Briseide ha legato il nodo di corda ai polsi di una nuova leva. Il mio l'ha sciolto lei, a fine anno, senza coltello. «Ha tenuto», ha detto. Nient'altro.")
        # Lenora, se alla grata c'e' stato qualcosa da annotare.
        if "lenora_insolenza" in noti:
            righe.append("Nei registri di Pandora l'insolenza della grata c'è ancora. Lenora l'ha riclassificata: non più «insolenza», ma «precedente». Quest'anno, tre Figli hanno risposto a tono.")
        elif "lenora_silenzio" in noti:
            righe.append("Alla grata di Lenora, quest'anno, i Figli di Briseide chinano la testa come feci io. Pandora annota anche quello. Non ha mai sprecato inchiostro.")
        # Zefiro.
        if "druso_lanternaio" in noti:
            righe.append("Nei vicoli bassi di Zefiro, sotto il portico, il lanternaio tiene accesa una lanterna in più. Non la fa pagare a nessuno. Dice che è per il grosso che morde, e per chi gli era venuto dietro.")
        elif "icaro_coperto" in noti:
            righe.append("Il mercante del tavolo grande ha chiuso il banco al mercato coperto. A Zefiro la bugia di quella sera è stata pagata a rate, fino all'ultima.")
        else:
            righe.append("Zefiro accende le lanterne come ogni sera, una per una, dalla Contrada Lumina alla Calà. Rocca Tempesta, sopra, non dorme.")
        return righe


label epilogo_rivali:
    $ ep_rivali_riga = epilogo_rivali_riga(rivali_coppia, epilogo_scelti)
    if ep_rivali_riga:
        $ renpy.say(narrator, ep_rivali_riga)
    return

label epilogo_anno_dopo:
    scene bg nero with fade
    centered "{cps=20}{size=+10}UN ANNO DOPO{/size}{/cps}"
    if epilogo_modo == "lontano":
        scene bg esterno_neve with fade
    elif epilogo_modo == "vivo":
        scene bg corridoio_ceppo with fade
    python:
        for _riga in anno_dopo_righe():
            renpy.say(narrator, _riga)
    scene bg nero with fade
    return
