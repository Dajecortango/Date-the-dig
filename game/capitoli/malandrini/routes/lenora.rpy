# L'udienza di Lenora — evento fisso comune (Luna III, giorno 16, sera).
# La Capofamiglia riceve i Figli adottivi dell'anno nella sala lunga del suo
# Ramo, da dietro la grata. Lenora e Pandora: solo voce e narrazione (niente
# sprite). Le battute di Lenora cambiano in base a chi frequenti di piu'
# (cuore_classifica in snodi.rpy). 0 punti: i menu cambiano solo il testo.

define lenora = Character("Lenora", color="#a8a8c0")
define pandora = Character("Pandora", color="#c98fa0")

default lenora_pref = None

init python:
    EVENTI.append(
        {"id": "udienza_lenora", "label": "udienza_lenora", "tipo": "fisso",
         "char": None, "luna": 3, "giorno": 16, "slot": "sera"})

    def lenora_preferito():
        """Il personaggio che frequenti di piu' (margine sulla soglia del
        cuore), se almeno un minimo frequentato; altrimenti None."""
        v = cal_vars()
        classifica = cuore_classifica(v)
        if classifica and v[CUORE_VAR[classifica[0][0]]] >= 3:
            return classifica[0][0]
        return None


label udienza_lenora:
    $ lenora_pref = lenora_preferito()
    scene bg consiglio with fade
    "Rocca Tempesta, la sala lunga del Ramo di Lenora. Banchi di quercia, torce basse, e in fondo una grata di ferro battuto."
    "Una volta l'anno la Capofamiglia riceve i Figli adottati nell'anno. Non li guarda. Li ascolta."
    "Siamo una ventina, in fila per Ceppo. Io in fondo, col nodo di corda al polso."
    show caino neutro at left with dissolve
    show icaro neutro with dissolve
    show druso ghigno at right with dissolve
    "Sul primo banco, i figli di lei. Caino dritto come un atto notarile. Icaro conta qualcosa: le torce, credo. O noi. Druso sbadiglia."
    $ muovi("druso", "sobbalzo")
    "Accanto alla grata, in piedi, una donna con un registro aperto sul braccio. Non la conosco. Druso sì: si raddrizza sul banco come un girasole."
    druso "Pandora. Non guardarla. La guardo io per tutti e due."
    pandora "Ceppo della Columna Lactaria. Avanti."
    pandora "[player_name], [figlio_t] di Briseide Ippodamia. Avanti, ho detto. Qui le cose si scrivono una volta sola."
    "Tre passi. I figli di Lenora alle spalle, la grata davanti. Dietro il ferro, un'ombra seduta. Immobile."
    lenora "Briseide ti ha scelt[fin]. Briseide sceglie bene, di solito. Poi controllo io."
    lenora "Il tuo primo semestre dura sei Lune. Ne sono passate due e mezza. Dimmi come le hai spese."
    "Apro la bocca. La voce dietro la grata arriva prima della mia."
    if lenora_pref == "caino":
        lenora "No. Lo so già. Mio figlio maggiore ti nomina nei suoi rapporti. Caino non nomina mai nessuno due volte."
        show caino freddo at left with qdiss
        caino "Una volta sola, madre. La seconda era una nota a margine."
        lenora "Le note a margine sono le sole che leggo."
    elif lenora_pref == "druso":
        lenora "No. Lo so già. Druso ha una rima nuova, e la rima ha il tuo passo."
        show druso imbarazzato at right with qdiss
        druso "Madre! Era una strofa privata!"
        lenora "In questa famiglia non esiste il privato, Druso. Esiste il non ancora saputo."
    elif lenora_pref == "icaro":
        lenora "No. Lo so già. Icaro ha aperto il suo registro a una voce nuova. Non lo fa per meno di cento Scudi."
        show icaro sorpreso with qdiss
        icaro "Non ho aperto niente."
        lenora "Lo dici in fretta, Icaro. I conti, tu, li fai piano."
    elif lenora_pref == "aede":
        lenora "No. Lo so già. Le tue albe le passi nel cortile d'armi, con la figlia di Glauco. Quella rossa."
        lenora "Le figlie di Glauco non si frequentano. Si sopravvivono. Vedremo."
        "Sul primo banco, Druso si tocca il naso. Come chi ricorda una lama ferma a un dito."
    elif lenora_pref == "ofelia":
        lenora "No. Lo so già. La serra di Glauco, la sera. Una fila di pretendenti, e tu in fila."
        show druso ghigno at right with qdiss
        druso "Anch'io ero in fila, madre."
        lenora "Tu eri in fila per sbaglio, Druso. Come sempre."
    else:
        lenora "Anzi, no. Non rispondere. Non hai frequentato nessuno abbastanza da lasciare un'impronta."
        lenora "Nel primo anno si chiama prudenza. Più tardi diventa un'abitudine. Stai attent[fin] a quale delle due."
    menu:
        "La grata aspetta. Lenora, dicono, non fa mai una domanda due volte."
        "«A guardare, ascoltare e non farmi notare.»":
            lenora "La regola di Briseide. Due su tre. Ti ho notat[fin]."
            lenora "Ma è colpa mia, non tua. Io noto tutto."
        "«Bene. Meglio di quanto Rocca Tempesta si aspettasse.»":
            show druso sorpreso at right with qdiss
            druso "Oh, no."
            lenora "Insolenza. Annotata, non punita. Le insolenze punite non insegnano niente a nessuno."
            lenora "Io non perdono, [figlio_t] di Briseide. Riclassifico. Ricordalo, la prossima volta che apri bocca qui dentro."
        "Tacere, e chinare la testa":
            "Chino la testa. Il silenzio della sala si allunga, una torcia sfrigola. Nessuno respira."
            lenora "Il silenzio. Il più vecchio dei giuramenti."
            lenora "Briseide ti ha insegnato bene. O non ti ha insegnato niente, e sei nat[fin] così. Peggio per chi ti sottovaluta."
    lenora "Vai. La prossima volta che sento il tuo nome, voglio che ci sia una ragione."
    pandora "Il prossimo."
    scene bg corridoio_ceppo with fade
    "Fuori, nel corridoio, l'aria è fredda e normale. I tre figli di Lenora escono per ultimi."
    show druso ghigno at left with dissolve
    druso "Sopravvissut[fin]! Alla prima udienza che ho visto, un novellino ha vomitato su un Arconte."
    show caino sarcastico with dissolve
    caino "Su due."
    show icaro neutro at right with dissolve
    icaro "E tu ridevi, Druso. Madre ti ha chiuso in cantina tre giorni."
    druso "Valeva la pena. Ogni giorno."
    "Ridono. Non insieme: uno dopo l'altro, come tre campane che non si sono messe d'accordo."
    "Dietro di noi la porta della sala lunga si chiude. Dietro la grata, credo, nessuno ride mai."
    return
