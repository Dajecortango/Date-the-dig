# Route Caino — climax e finali.

################################################################################
## CLIMAX — Il Consiglio
################################################################################

label caino_climax:

    scene bg consiglio with fade

    "La Sala del Consiglio di Rocca Tempesta. Non dovrei essere qui: i Figli nuovi non entrano. Ma il mio nome è sulla convocazione, scritto da mano ignota."

    "Al centro, Caino. Davanti a lui, il semicerchio degli Arconti. E sul seggio più alto, una donna che non ha bisogno di presentazioni: fredda, dorata, immobile. Lenora."

    show caino neutro with dissolve

    "L'accusa è semplice: l'Arconte della Proprietà ha trattenuto le prove contro Aulo per sei mesi, usandole quando conveniva a lui. Abuso della Virtù dell'Operosità. Qualcuno deve pagare."

    "E io so — perché i registri li tengo io — che esiste una via d'uscita perfetta: le date di consultazione sono annotate con la MIA mano. Basta una parola di Caino, e il ritardo diventa colpa mia. Lo scrivano nuovo, inesperto, del Ceppo di Briseide. Il capro perfetto."

    "Il Primo Arconte legge l'accusa con voce piatta, da notaio. Ogni data cade nella sala come una moneta sul tavolo."

    "Lenora non guarda né l'accusatore né l'accusato. Si osserva le mani. Le dita intrecciate, immobili, come chi ha già fatto il conto e aspetta solo il totale."

    "Al terzo banco a sinistra, Druso. Ha le braccia incrociate e la mascella serrata. Per una volta, niente TESCHIO."

    "Caino lo sa. Mi guarda. La sala intera segue il suo sguardo fino a me."

    # Routing (rl.finale_caino) — ordine vincolante: caino_good_end ->
    # caino_passeggero -> caino_secret_end -> caino_bad_end ->
    # caino_neutral_end.
    $ cal_finale = rl.finale_caino(caino_fiducia, caino_trappole,
                                   caino_memoria, caino_druso)
    jump expression cal_finale

################################################################################
## GOOD END — La legge del cuore
################################################################################

label caino_good_end:

    show caino neutro with dissolve

    caino "Arconti. La tempistica dei registri di Aulo ha un solo responsabile."

    "Il silenzio della sala è un animale affamato. Caino mi guarda un'ultima volta. E sorride — non il sorriso facile. L'altro. Quello che siamo in tre a conoscere."

    caino "Io. Li ho trovati, li ho tenuti, li ho usati. Per ambizione. Come ogni cosa che ho fatto in questa Rocca, tranne una."

    "La sala esplode. Lenora alza una mano e il rumore muore."

    "La Capofamiglia guarda suo figlio per un tempo lunghissimo. Poi:"

    "«La Proprietà passa ad altra mano per un anno. L'onestà, per quanto tardiva, resta una Virtù. Seduta tolta.»"

    scene bg esterno_neve with fade

    show caino neutro with dissolve

    "Sugli spalti, dopo. Caino guarda Zefiro con l'aria di chi ha perso una carica e non riesce a smettere di sorridere."

    caino "Vent'anni di scalata. Bruciati in una frase. Dovrei odiarti."

    pc "E invece?"

    caino "Invece ho fatto i conti. Io i conti li faccio sempre, lo sai. Carica: persa. Seggio: rimandato. Madre: furiosa, il che è quasi un guadagno."

    show caino tenero with dissolve

    caino "Tu: qui. Il registro chiude in attivo, [player_name]. Per la prima volta in vita mia, il registro chiude in attivo senza che io abbia fregato nessuno."

    pc "Tua madre ti perdonerà?"

    caino "Mia madre non perdona. Riclassifica. Fra un anno sarò una voce in attivo anche per lei, vedrai. Le piacciono i figli che sanno perdere al momento giusto."

    "Mi prende il viso tra le mani — le mani callose dello spadaccino, attente come su un filo di lama."

    caino "La pergamena di destra. Quella senza niente scritto. La firmo io, se tu la firmi con me. E ti avverto: quello che c'è sotto l'Arconte farebbe di tutto per te. Di tutto. È l'unico contratto che non so limitare."

    pc "Allora firmiamo senza limiti."

    caino "TESCHIO."

    with vpunch

    pc "Cosa—"

    "Il pugno si ferma a un dito dal mio inguine. Caino ride come suo fratello, finalmente."

    caino "Benvenut[fin] nella famiglia. Quella piccola. La regola è una sola: si dichiara prima di colpire."

    scene bg nero with fade

    $ sblocca_finale("caino_good_end")
    with lampo_oro
    centered "{cps=20}{size=+10}LA LEGGE DEL CUORE{/size}\n\nIl registro chiude in attivo.\nPer sempre.{/cps}"

    return

################################################################################
## SECRET END — Teschio
################################################################################

label caino_secret_end:

    show caino neutro with dissolve

    caino "Arconti. La tempistica è colpa mia. Del mio metodo. Ne risponderò alla Capofamiglia in forma privata."

    "Lenora inclina la testa di un grado: concesso. La sala si svuota con un brusio deluso: niente teste, oggi."

    "Caino mi passa accanto senza fermarsi."

    caino "Grazie per il silenzio, Figlio di Briseide. Il tuo conto è pari."

    "Pari. Un registro chiuso. Tutto qui."

    "Nessuno sguardo, nessun drago al mignolo. Le mani nude, come la sera del ballo."

    scene bg palestra with fade

    show druso neutro with dissolve

    "È Druso che mi trova, la sera, nel cortile d'armi. Due corni di idromele, uno me lo pianta in mano senza chiedere."

    druso "Mio fratello è un idiota."

    pc "Tuo fratello è l'uomo più intelligente di Rocca Tempesta."

    druso "Le due cose convivono benissimo, fidati, li conosco da quando è nato. Ha davanti una cosa vera — la prima della sua vita — e la archivia come un conto pari, perché i conti pari non fanno paura."

    "Druso beve metà corno in un sorso, poi mi guarda. Senza sorriso, per la terza volta da che lo conosco."

    druso "Io invece le cose vere le riconosco. E non le archivio."

    pc "Druso—"

    druso "Non dire niente. Di' solo se la regola la conosci."

    "La regola. La regola di questa famiglia piccola e assurda, l'unica legge che Caino ha scritto per amore e non per potere."

    menu:
        "Il corno di idromele è caldo tra le mani."

        "«TESCHIO.»":
            pc "TESCHIO."

            show druso ghigno with qdiss

            "Druso para ridendo, e l'idromele vola, e da qualche parte sugli spalti giuro che qualcuno — qualcuno con un anello col drago — ci guarda e scuote la testa, sorridendo suo malgrado."

            druso "Dichiarazione accettata. Da domani, novellin[fin], ti insegno il Codice intero. Articolo primo: il cuore si difende come i genitali. Sempre in guardia, e mai da solo."

        "Bere in silenzio e restare":
            "Non dico niente. Resto. E il restare, con un uomo come Druso, è già una dichiarazione."

            show druso ghigno with qdiss

            druso "Lo prendo come un TESCHIO sussurrato. Vale, per stavolta."

    scene bg nero with fade

    $ sblocca_finale("caino_secret_end")
    centered "{cps=20}{size=+10}TESCHIO{/size}\n\n{i}Finale segreto{/i}\n\nIl fratello sbagliato. O forse quello giusto.{/cps}"

    return

################################################################################
## BAD END — La pedina
################################################################################

label caino_bad_end:

    show caino freddo with dissolve

    caino "Arconti. Le date di consultazione dei registri parlano chiaro. La mano è quella dello scrivano: [player_name], del Ceppo di Briseide. Nuov[fin], inespert[fin]. Il ritardo nasce lì."

    "Lo dice senza guardarmi. Liscio, misurato, perfetto. La voce del Ballo delle Candele Spente."

    "Provo a parlare: il Primo Arconte mi toglie la parola. I Figli nuovi non parlano in Consiglio. Il mio nome entra nei verbali; la Virtù della Verità richiede un'ammenda; Briseide ottiene — a fatica — che sia l'esilio dalla capitale e non le Segrete Silenti."

    "Caino vota con la maggioranza. Ovviamente. Vince gli scontri, Caino. Tutti. Soprattutto quando è dalla parte del torto."

    "Dal terzo banco, Druso si alza e se ne va prima del voto. È l'unico rumore della seduta."

    "Lenora firma l'atto senza leggerlo. Le basta il nome in fondo: il mio."

    scene bg vicoli_zefiro with fade

    "Al cancello di Zefiro, la mattina dopo, c'è una figura che non mi aspettavo."

    show caino sarcastico with dissolve

    caino "Niente rancore, Figlio di Briseide. Eri il pezzo giusto nel turno sbagliato. Capita ai migliori. Soprattutto ai migliori: i pezzi scarsi non li gioca nessuno."

    pc "Mi hai usato dal primo giorno."

    caino "Ti ho ASSUNTO dal primo giorno. L'uso era nel contratto; dovevi leggere le clausole. I dettagli, ricordi? I dettagli possiedono le persone."

    "Si volta. Poi, un passo dopo, si ferma — un mezzo istante, le spalle rigide — come se il registro, da qualche parte, non chiudesse."

    caino "...Rurikstad è decente, d'inverno. Evita il vino di Glostok."

    "È l'unica crepa che gli vedrò mai. La porto in esilio con me: non vale niente, e non smette di pesare."

    scene bg nero with fade

    $ sblocca_finale("caino_bad_end")
    centered "{cps=20}{size=+10}LA PEDINA{/size}\n\nNel registro di Caino\nla tua riga è già archiviata.{/cps}"

    return

################################################################################
## NEUTRAL END — Soci
################################################################################

label caino_neutral_end:

    show caino neutro with dissolve

    caino "Arconti. I registri hanno due mani: la mia e quella del mio scrivano. La tempistica è mia. Gli errori di forma, suoi. Propongo ammenda doppia e chiudiamo: il Consiglio ha guerre più vere di questa."

    "Mezza colpa a testa. Il compromesso perfetto: nessuno cade, nessuno vince. Lenora approva con un cenno annoiato."

    scene bg studio_glauco with fade

    show caino neutro with dissolve

    "Nello studio, quella sera, le due pergamene sono ancora sul tavolo. Caino spinge verso di me quella di sinistra: la nomina."

    caino "Primo Scrivano della Proprietà. Te la sei guadagnata: metà colpa, metà merito. È così che si costruiscono le carriere vere."

    pc "E la pergamena di destra?"

    "Caino la prende, la guarda un lungo istante. Poi la tiene — non la straccia. La ripone nel cassetto, sotto chiave."

    "La chiave non la mette al collo, come le altre. La lascia sul tavolo, tra noi due, dove chiunque potrebbe prenderla."

    caino "Archiviata. Non cancellata. C'è differenza, nei registri: le cose archiviate, un giorno, si possono riaprire."

    pc "E chi decide quando?"

    show caino sarcastico with qdiss

    caino "Il tempo. O un idromele abbastanza buono. Al lavoro, Primo Scrivano. La Proprietà non si amministra da sola."

    scene bg nero with fade

    $ sblocca_finale("caino_neutral_end")
    centered "{cps=20}{size=+10}SOCI{/size}\n\nLa pergamena di destra resta nel cassetto.\nArchiviata. Non cancellata.{/cps}"

    return

################################################################################
## FINALE PASSEGGERO — Un'altra mano
################################################################################

label caino_passeggero:

    show caino neutro with dissolve

    caino "Arconti. La tempistica dei registri è mia. Solo mia. Lo scrivano ha copiato quello che gli ho dettato."

    "Si prende tutto. Non mi guarda mentre lo fa. È questo, capisco dopo, il punto."

    "Lenora toglie la seduta con un gesto. La Proprietà passa ad altra mano per un anno."

    scene bg esterno_neve with fade

    show caino freddo with dissolve

    pc "Potevi dividere la colpa. Ti avrei coperto."

    if caino_trappole > rl.CAINO_TRAPPOLE_GOOD:
        caino "Nelle trappole ci sei cadut[fin] più di una volta. Ogni volta mi hai chiesto scusa un passo dopo. Le scuse tardive, nei registri, si chiamano rettifiche."
    else:
        caino "Lo so. Ma a coprire serve ricordare. E tu le cose che ti ho detto le hai lasciate cadere, una a una. Come fogli in un archivio senza indice."

    show caino neutro with qdiss

    caino "Non è un rimprovero. È un saldo. Sei stat[fin] lo scrivano migliore che ho avuto. Non ti chiedo di essere altro."

    "Mi tende la mano. Una stretta da notaio: ferma, breve, registrata."

    scene bg consiglio with fade

    "Una Luna dopo lo vedo alla Rocca, già in piedi, a un banco più in fondo. Caino non resta a terra a lungo."

    show caino sarcastico with dissolve

    "Accanto a lui c'è uno scrivano nuovo. Giovane, attento, prende appunti su tutto. Anche sulle battute."

    "Caino gli dice qualcosa e lo scrivano ride. Io quella battuta la conoscevo. Me l'aveva detta per primo."

    "Al terzo banco Druso mi fa un cenno, la mascella storta. Ha l'aria di chi ha visto chiudersi una porta e non ha avuto il coraggio di dire niente."

    scene bg nero with fade

    $ sblocca_finale("caino_passeggero")
    centered "{cps=20}{size=+10}UN'ALTRA MANO{/size}\n\nCaino ha pagato da solo.\nIl conto, con te, era già chiuso.{/cps}"

    return
