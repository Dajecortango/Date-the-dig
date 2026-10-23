# Il Ceppo di Briseide: l'arco di Vanna e Corrado (Lune II, III, V) e il
# brodo di meta' semestre con Briseide (III/25 sera).
# Spec: docs/superpowers/specs/2026-10-22-pacchetto-40-consigli-design.md
# (Narrativa, punti 10 e 13). Ordine imposto dalle cond: ceppo_vanna ->
# ceppo_corrado -> ceppo_scelta. Nessun punto di affinita'.

default ceppo_vanna = None      # scena 1: "chiedi" / "spia" / "lascia"
default ceppo_segreto = False   # scena 2: promesso a Corrado di tacere con Vanna
default ceppo_esito = None      # scena 3: "parte" / "resta" / "insieme"

init python:
    EVENTI.extend([
        # Luna II: Vanna trova un sigillo degli Arvali nel camino.
        {"id": "ceppo_vanna", "label": "ceppo_vanna", "tipo": "invito",
         "char": None, "ritratto": "vanna",
         "titolo": "Vanna ha trovato qualcosa nel camino",
         "luna_min": 2, "slot": "pomeriggio",
         "cond": lambda v: "svelo" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Luna III: Corrado confessa l'offerta degli Arvali.
        {"id": "ceppo_corrado", "label": "ceppo_corrado", "tipo": "invito",
         "char": None, "ritratto": "corrado",
         "titolo": "Corrado ti aspetta in archivio, a porta chiusa",
         "luna_min": 3, "slot": "pomeriggio",
         "cond": lambda v: "ceppo_vanna" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Meta' semestre: il brodo con Briseide.
        {"id": "briseide_brodo", "label": "ceppo_briseide", "tipo": "fisso",
         "char": None, "luna": 3, "giorno": 25, "slot": "sera",
         "cond": lambda v: "svelo" in v["visti"]},
        # Luna V: il corriere degli Arvali parte a mezzogiorno.
        {"id": "ceppo_scelta", "label": "ceppo_scelta", "tipo": "fisso",
         "char": None, "luna": 5, "giorno": 20, "slot": "mattina",
         "cond": lambda v: "ceppo_corrado" in v["visti"]},
    ])

    TRAMA_TITOLI.update({
        "briseide_brodo": "Il brodo di metà semestre",
        "ceppo_scelta": "Il corriere degli Arvali",
    })

    CONSEGUENZE_VARS.extend(["ceppo_vanna", "ceppo_segreto", "ceppo_esito"])

    FATTI.extend([
        {"id": "cep_segreto", "char": None,
         "testo": "Hai promesso a Corrado di non dire niente a Vanna delle lettere degli Arvali.",
         "avviso": "Vanna se ne ricorderà.",
         "cond": lambda v: v["ceppo_segreto"]},
        {"id": "cep_parte", "char": None,
         "testo": "Hai detto a Corrado di partire per Hammergrad. Vanna è rimasta al Ceppo.",
         "avviso": "Il Ceppo se ne ricorderà.",
         "cond": lambda v: v["ceppo_esito"] == "parte"},
        {"id": "cep_resta", "char": None,
         "testo": "Hai chiesto a Corrado di restare. La lettera degli Arvali è finita in un cassetto.",
         "avviso": "Corrado se ne ricorderà.",
         "cond": lambda v: v["ceppo_esito"] == "resta"},
        {"id": "cep_insieme", "char": None,
         "testo": "Hai convinto Vanna a partire con Corrado. Il Ceppo ha due sedie vuote.",
         "avviso": "Il Ceppo se ne ricorderà.",
         "cond": lambda v: v["ceppo_esito"] == "insieme"},
    ])

    # Briseide a meta' semestre: i fatti di Lune I-III che una madre di
    # cinquanta Figli puo' sapere (Consiglio, Pandora, mercanti, Vanna).
    # Ordine = priorita'; al massimo due battute.
    # eco_orfani / eco_debito_insoluto vengono da economia_extra.rpy: se il
    # fatto non esiste (o non e' nato) la voce e' semplicemente ignorata.
    BRISEIDE_FATTI = [
        ("eco_orfani",
         "Nella cassa degli orfani ho trovato due Scudi che nessuno aveva chiesto. Conosco le monete del mio Ceppo, [player_name]. Quelle erano tue."),
        ("lenora_insolenza",
         "Alla grata di Lenora hai risposto a tono. Me l'ha detto Pandora, con la faccia di chi ha già trovato la pagina giusta."),
        ("lenora_silenzio",
         "Alla grata hai chinato la testa. Bene. Davanti a Lenora non è vergogna, è aritmetica. La vergogna è chinarla davanti a chi non conta."),
        ("caino_massacro",
         "All'Adunanza hai chiamato il Ballo delle Candele Spente col suo nome. Io in trent'anni di Consiglio non l'ho mai fatto. Coraggio o fretta: nel Nord, spesso, è la stessa cosa."),
        ("caino_trappola",
         "All'Adunanza hai lodato il Ballo delle Candele Spente. Caino recita la parte di chi lo ricorda come una festa. Tu gli hai creduto, e lui ti ha archiviat[fin] per questo."),
        ("icaro_coperto",
         "Un mercante della Consorteria mi ha chiesto se nel mio Ceppo si insegna a contare o a mentire. Gli ho detto: tutte e due, in quest'ordine. Ricordatelo, l'ordine."),
        ("ofelia_gelo",
         "Vanna dice che la figlia di Glauco ha cancellato un nome con l'inchiostro rosso. Non chiedo quale. Chiedo se l'hai lasciato cadere o se ti è caduto."),
        ("ofelia_attesa",
         "Ho saputo che Ofelia ti ha aspettat[fin], una sera. Una figlia di Glauco che aspetta. Nel Nord non si vede spesso. E non si vede due volte."),
        ("eco_debito_insoluto",
         "Un esattore di Icaro è passato dalla porta del Ceppo, a chiedere di te. Ha avuto quello che cercava, mi dicono. Da me ha avuto solo il brodo: i debiti dei miei Figli li pagano i miei Figli."),
        ("caino_teschio",
         "Druso va dicendo per le taverne che sei il suo testimone del Codice del Teschio. Non voglio sapere cosa sia. Voglio sapere se ti ha mai fatto testimoniare qualcosa di vero."),
    ]

    def briseide_battute(noti, massimo=2):
        """Fino a `massimo` battute di Briseide sui fatti gia' noti, in
        ordine di priorita'. Ofelia: il gelo assorbe l'attesa."""
        out = []
        for fid, riga in BRISEIDE_FATTI:
            if fid not in noti:
                continue
            if fid == "ofelia_attesa" and "ofelia_gelo" in noti:
                continue
            out.append(riga)
            if len(out) >= massimo:
                break
        return out


## Luna II — il sigillo nel camino (invito, Vanna) ###########################

label ceppo_vanna:
    scene bg corridoio_ceppo with fade
    show vanna neutra with dissolve
    "Vanna mi trascina in cucina per la manica. Ha le dita nere di cenere e l'aria di chi ha appena vinto una scommessa con se stessa."
    vanna "Guarda. Era nel camino, sotto la brace. Qualcuno l'ha bruciato male."
    "Un pezzo di ceralacca grigia. Dentro, inciso, un fiume che scorre in tondo."
    vanna "Il sigillo degli Arvali, [fratello_t]. Quelli del Margine, dei morti, dei registri dei morti. Corrado ne ha ricevute tre, in una Luna."
    vanna "Corrado non riceve lettere. Corrado riceve libri, e li tratta meglio delle persone."
    menu:
        "Vanna rigira la ceralacca tra le dita, come una moneta falsa."
        "«Gliel'hai chiesto?»":
            $ ceppo_vanna = "chiedi"
            vanna "Chiedere? A Corrado? Ti risponde con una data e una nota a piè di pagina."
            vanna "E poi chiedere è da gente che non ha fonti. Io ho le fonti. Ho il camino."
        "«Lo scopro io.»":
            $ ceppo_vanna = "spia"
            vanna "Ecco. Lo sapevo che eri [il_t] mi[fin] preferit[fin]. Non dirlo agli altri."
            vanna "Tu hai la faccia da novellin[fin]. Di te non sospetta nessuno. È il tuo unico talento, usalo."
        "«Sono lettere sue, Vanna.»":
            $ ceppo_vanna = "lascia"
            vanna "Lo so che sono sue. È per questo che le ha bruciate."
            "Abbassa la ceralacca. Per un attimo smette di essere la pettegola del Ceppo."
    vanna "Se se ne va, chi mi corregge le date? Io le sbaglio apposta, sai. Per sentirlo sbuffare."
    "Si mette la ceralacca in tasca. Al brodo, stasera, siede accanto a Corrado e non gli chiede niente. Lo guarda mangiare."
    return


## Luna III — l'archivio a porta chiusa (invito, Corrado) ####################

label ceppo_corrado:
    scene bg studio_glauco with fade
    show corrado neutro with dissolve
    if ceppo_vanna == "spia":
        "Lo seguo fino all'archivio, tre passi indietro, come mi ha insegnato Vanna. Corrado apre la porta prima che io bussi."
        corrado "Vanna ti ha mandat[fin] a spiarmi. Lo so perché ieri sera me l'ha detto lei. Per sbaglio, credo."
    else:
        "L'archivio del Ceppo, di pomeriggio. Corrado chiude la porta alle mie spalle. Non l'ha mai chiusa, nemmeno d'inverno."
    corrado "Siediti, [fratello_t]. Oggi niente stemmi."
    "Tira fuori una lettera da un libro di araldica. Il sigillo, stavolta, è intero: il fiume che gira in tondo."
    corrado "Gli Arvali di Hammergrad cercano un copista per i registri del Margine. Tre anni a ricopiare i nomi dei morti. Poi, forse, un posto tra i custodi."
    corrado "Hanno letto le mie note sul Ballo delle Candele Spente. Dicono che scrivo come uno che ha paura di dimenticare. È un complimento, lassù."
    pc "E Briseide?"
    corrado "Briseide dirà sì. Briseide dice sempre sì, a chi parte. Poi conta i giorni."
    corrado "Devo rispondere entro la fine della quinta Luna. Se lo dico a Vanna, non parto più. Se non glielo dico, parto male."
    menu:
        "Corrado tiene la lettera per un angolo, come se scottasse ancora."
        "«Non dirò niente a Vanna. Decidi tu.»":
            $ ceppo_segreto = True
            corrado "Grazie. Prima decido io, poi lo sa lei. L'ordine giusto."
            "Lo dice col tono degli stemmi. Poi si pulisce gli occhiali, che erano già puliti."
        "«Diglielo. Oggi.»":
            corrado "Oggi."
            "Ripiega la lettera in quattro. Poi in otto."
            corrado "Domani, forse. Oggi lei ha il turno delle cipolle, e piange già per conto suo."
        "«Cosa vuoi tu, Corrado?»":
            "Ci pensa. Corrado pensa sempre prima di rispondere. Stavolta ci mette tanto che sento la candela consumarsi."
            corrado "Voglio un posto dove le date non le sbaglia nessuno apposta."
            corrado "E voglio che qualcuno, qui, le sbagli ancora. Non si possono volere tutte e due, [fratello_t]. Le Virtù non lo permettono."
    "Rimette la lettera nel libro di araldica, alla pagina del leone. Chiude il libro. Riapre la porta."
    return


## Luna III — il brodo di meta' semestre (fisso III/25 sera, Briseide) ######

label ceppo_briseide:
    scene bg corridoio_ceppo with fade
    show briseide neutra with dissolve
    "Metà semestre. Briseide mi chiama in cucina dopo cena: due tazze di brodo, la porta chiusa, il pentolone che borbotta da solo."
    briseide "Tre Lune, [player_name]. A metà strada si assaggia, come col brodo. Poi si aggiusta il sale."
    $ briseide_righe = briseide_battute(fatti_noti)
    if briseide_righe:
        "Sa già tutto. Briseide sa sempre già tutto: cinquanta Figli sono cinquanta orecchie."
        python:
            for _riga in briseide_righe:
                renpy.say(briseide, _riga)
        briseide "Non ti sgrido. Ti conto. Una madre conta tutto: le notti, le fosse, le cose dette ad alta voce."
    else:
        briseide "Nessuno mi ha raccontato niente di te. Né Pandora, né i mercanti, né Vanna. Vanna, [player_name]. Lo sai quanto è difficile?"
        briseide "Un Figlio di cui nessuno parla, a metà semestre, sta imparando. O si sta nascondendo. Spero la prima."
    "Mi prende il polso. Gira il nodo di corda con il pollice, una volta, due, cercando il punto lento."
    briseide "Il nodo tiene?"
    menu:
        "Le sue dita sono calde di brodo. Il nodo, sotto, è ruvido come il primo giorno."
        "«Tiene. Prude, ma tiene.»":
            briseide "Prude perché è nuovo. Anche il Ceppo prude, il primo anno. Poi ci si fa il callo, e si smette di sentirlo."
            briseide "È lì che bisogna stare attenti."
        "«Quando si toglie?»":
            briseide "Quando lo decido io. E lo decido quando smetti di chiederlo."
            "Sorride. Ha detto la stessa frase a tutti i Figli prima di me. Si sente: le viene bene."
        "Stringerlo da sol[fin], davanti a lei":
            "Tiro il capo della corda finché non morde. Briseide scuote la testa."
            briseide "Troppo stretto. Lo fate tutti, a metà anno: credete che tenga di più. Tiene di meno, e fa male."
            "Lo allenta di un dito. Senza coltello, solo con le unghie."
    briseide "Bevi, prima che si freddi. Il resto del semestre non aspetta, e nemmeno il brodo."
    return


## Luna V — il corriere degli Arvali (fisso V/20 mattina) ####################

label ceppo_scelta:
    scene bg corridoio_ceppo with fade
    show vanna neutra at left with dissolve
    show corrado neutro at right with dissolve
    "La quinta Luna, di mattina. Nel corridoio del Ceppo Vanna e Corrado non si parlano. Si stanno parlando da un'ora."
    "Tra loro, sul davanzale, la lettera degli Arvali. Aperta."
    vanna "Il corriere parte a mezzogiorno. Lo sapevi? Lui lo sapeva da una Luna e mezza."
    if ceppo_segreto:
        vanna "E lo sapevi anche tu, [fratello_t]. Si vede. Hai la faccia di quando nascondi il pane sotto il tavolo."
        pc "Gliel'avevo promesso."
        vanna "Lo so. Fa più male così: non ti posso nemmeno dare torto."
    elif ceppo_vanna == "spia":
        vanna "Ti avevo mandat[fin] a scoprirlo. L'ho scoperto da sola, dal camino. Come sempre. Le fonti, [fratello_t]."
    corrado "Hammergrad. Tre anni. Non è la fine del mondo, Vanna."
    vanna "È la fine del Nord. Dicono che lassù la neve non se ne va mai. E non c'è nessuno che sbagli le date."
    corrado "Appunto."
    "Si voltano insieme verso di me. Fratelli di Ceppo: anche quando litigano, si girano dalla stessa parte."
    corrado "Decidi tu, [fratello_t]. Noi due litighiamo fino a mezzogiorno, e il corriere parte lo stesso."
    menu:
        "La lettera, sul davanzale, aspetta una firma o il fuoco."
        "«Parti, Corrado.»":
            $ ceppo_esito = "parte"
            corrado "...grazie. Credo. Ci voleva qualcuno che lo dicesse ad alta voce. Io lo dico solo per iscritto."
            vanna "Traditore. Tutti e due."
            "Ma è lei a dargli la penna. E a tenergli ferma la lettera mentre firma, perché le mani a Corrado tremano."
            vanna "Scrivimi. Con le date giuste. Così le correggo io."
        "«Resta. Il Ceppo ha bisogno di qualcuno che corregga le date.»":
            $ ceppo_esito = "resta"
            "Corrado guarda la lettera a lungo. Poi la piega in quattro, in otto, e la mette in tasca. Non nel camino."
            corrado "In tasca. Non si sa mai. Gli Arvali hanno pazienza: lavorano coi morti."
            vanna "Resta. Hai sentito, archivista? Resta."
            "Lo abbraccia così forte che a Corrado cadono gli occhiali. Non si china a raccoglierli finché lei non lo lascia."
        "«Vanna, va' con lui.»":
            $ ceppo_esito = "insieme"
            vanna "Io? A Hammergrad? Con la neve che non se ne va e i morti in fila nei registri?"
            "Si ferma. La vedo fare il conto, come lo farebbe Briseide: le cucine, i fratelli del Ceppo, i pettegolezzi di Zefiro."
            vanna "Dicono che gli Arvali sappiano i segreti di tutti i morti del Nord. Trecento anni di pettegolezzi, [fratello_t]. Mai raccontati a nessuno."
            corrado "Gli Arvali non raccontano."
            vanna "Gli Arvali non mi conoscono ancora."
            "Corrado ride. Non l'ho mai sentito ridere così, a bocca aperta, senza una nota a piè di pagina."
    "A mezzogiorno il corriere parte. Dalla finestra del corridoio lo guardiamo in tre, finché la strada non lo inghiotte."
    return
