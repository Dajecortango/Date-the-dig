# Ricordi che contano (pacchetto 40 consigli, punto 21): un ricordo della
# Borsa (borsa.rpy, RICORDI) torna in un'attivita' pertinente. Mostrarlo o
# tenerlo in tasca cambia una battuta e lascia un fatto. Una volta sola
# (ECHI: echi_visti). Il nodo di corda e' di Briseide, altrove.
#
# Tempi: la tazza nasce in Luna III-IV (icaro_bro1) -> citta'.
# Bicchiere e moneta nascono a V/26 sera (icaro_luna5): l'eco (ritardo 2
# slot) cade a VI/5 sera, in fumeria o in taverna (VI/12 sera e' di
# icaro_luna6). La rosa nasce a V/26 pomeriggio (ofelia_ev4): corte e citta'
# non tornano piu' di pomeriggio (VI/5 e' dell'interludio di Ofelia), quindi
# taverna, VI/5 o VI/12 sera.

# Ricordo -> "mostrato" | "tenuto".
default ricordi_usati = {}

init 1 python:
    CONSEGUENZE_VARS.extend(["ricordi_usati"])

    FATTI.extend([
        # Inneschi: il ricordo e' in tasca (nessun avviso, la Borsa lo mostra).
        {"id": "eco_tazza_garanzia", "char": "icaro",
         "testo": "Icaro ti ha messo in mano una tazza di Glostok, quella senza crepe: la tua parte dell'affare.",
         "avviso": None,
         "cond": lambda v: "icaro_bro1" in v["visti"]},
        {"id": "eco_rosa_segreta", "char": "ofelia",
         "testo": "Tra due banchi di spezie Ofelia ti ha dato una rosa nera, senza guardarti.",
         "avviso": None,
         "cond": lambda v: "ofelia_ev4" in v["visti"] and not v["ofelia_in_pubblico"]},
        # Esiti.
        {"id": "eco_tazza_mostrata", "char": "icaro",
         "testo": "Hai mostrato la tazza di Icaro al mercante di Glostok. Ha capito di chi eri socio, e ha abbassato gli occhi.",
         "avviso": "Il mercato se ne ricorderà.",
         "cond": lambda v: v["ricordi_usati"].get("tazza") == "mostrato"},
        {"id": "eco_tazza_tenuta", "char": "icaro",
         "testo": "Davanti al mercante di Glostok la tazza di Icaro è rimasta in tasca. Il servizio resta completo a metà.",
         "avviso": None,
         "cond": lambda v: v["ricordi_usati"].get("tazza") == "tenuto"},
        {"id": "eco_bicchiere_mostrato", "char": "icaro",
         "testo": "Hai bevuto con Icaro nel suo bicchiere di Glostok, cartellino compreso. Il conto, per una sera, era pari.",
         "avviso": "Icaro se ne ricorderà.",
         "cond": lambda v: v["ricordi_usati"].get("bicchiere") == "mostrato"},
        {"id": "eco_bicchiere_tenuto", "char": "icaro",
         "testo": "Il bicchiere di Icaro è rimasto avvolto nel panno. Certi debiti pari non si mostrano.",
         "avviso": None,
         "cond": lambda v: v["ricordi_usati"].get("bicchiere") == "tenuto"},
        {"id": "eco_moneta_mostrata", "char": "icaro",
         "testo": "Hai messo sul panno la moneta di Icaro. Lui l'ha ripresa prima che toccasse il tavolo.",
         "avviso": "Icaro se ne ricorderà.",
         "cond": lambda v: v["ricordi_usati"].get("moneta") == "mostrato"},
        {"id": "eco_moneta_tenuta", "char": "icaro",
         "testo": "Con la posta scoperta e la borsa vuota, la moneta di Icaro è rimasta in tasca.",
         "avviso": None,
         "cond": lambda v: v["ricordi_usati"].get("moneta") == "tenuto"},
        {"id": "eco_rosa_mostrata", "char": "ofelia",
         "testo": "Hai mostrato a Druso la rosa nera di Ofelia. In taverna, adesso, la serra ha un verso osceno in più.",
         "avviso": "Ofelia se ne ricorderà.",
         "cond": lambda v: v["ricordi_usati"].get("rosa") == "mostrato"},
        {"id": "eco_rosa_tenuta", "char": "ofelia",
         "testo": "La rosa nera è rimasta nel mantello, anche sotto gli occhi di Druso. Il segreto di Ofelia è ancora vostro.",
         "avviso": None,
         "cond": lambda v: v["ricordi_usati"].get("rosa") == "tenuto"},
    ])

    ECHI.extend([
        {"id": "echi_ricordo_tazza", "fatto": "eco_tazza_garanzia",
         "luoghi": ("citta",), "label": "echi_ricordo_tazza"},
        {"id": "echi_ricordo_bicchiere", "fatto": "icaro_copre",
         "luoghi": ("fumeria", "taverna"), "label": "echi_ricordo_bicchiere"},
        {"id": "echi_ricordo_moneta", "fatto": "icaro_smaschera",
         "luoghi": ("fumeria", "taverna"), "label": "echi_ricordo_moneta"},
        {"id": "echi_ricordo_rosa", "fatto": "eco_rosa_segreta",
         "luoghi": ("taverna",), "label": "echi_ricordo_rosa"},
    ])


# Tazza (Bro di Icaro): il mercante di Glostok del servizio (città).
label echi_ricordo_tazza:
    scene bg vicoli_zefiro with dissolve
    "Al mercato coperto rivedo il mercante di Glostok. Quello del servizio da tè: trentadue pezzi, comprati da Icaro a un terzo del prezzo."
    "Ha un banco nuovo, più piccolo. Su un panno, sei tazze scompagnate. Gli manca un servizio intero, e lo sa."
    menu:
        "In tasca, la tazza senza crepe pesa poco. Lui no: lui mi riconosce."
        "Posare la tazza sul suo banco, accanto alle altre":
            $ ricordi_usati["tazza"] = "mostrato"
            "La poso tra le sue, scheggiate sul bordo. Lui la gira con due dita e cerca il marchio sotto il piede."
            "«Il socio del magro con la pipa», dice piano. «Ditegli che non vendo più niente a Zefiro. Ditegli che ho capito.»"
            "Riprendo la tazza. Non ho detto una parola."
        "Tenerla in tasca e passare oltre":
            $ ricordi_usati["tazza"] = "tenuto"
            "Tiro dritto. Lui si lamenta con la vicina del «magro con la pipa», e di [un_t] ragazz[fin] con la faccia seria che non diceva niente."
            "Non mi volto. Il servizio è completo a metà, e la metà mia resta dove deve stare: lontano dai banchi."
    $ conseguenze_aggiorna()
    return

# Bicchiere (Icaro, la partita: «copre»): sera, sotto il portico.
label echi_ricordo_bicchiere:
    scene bg vicoli_zefiro with dissolve
    show icaro neutro with dissolve
    "Sotto il portico della Consorteria, Icaro fuma da solo. Ha una bottiglia aperta e nessun bicchiere: li conta, i bicchieri, e stasera non ne vuole sporcare."
    menu:
        "Nel panno, in borsa, c'è il suo cristallo di Glostok. Cartellino ancora attaccato."
        "Tirarlo fuori e porgerglielo":
            $ ricordi_usati["bicchiere"] = "mostrato"
            show icaro sorpreso with qdiss
            icaro "Il cartellino. Non l'hai tolto."
            pc "Era tuo. Non mi sembrava mio da togliere."
            show icaro sereno with qdiss
            "Versa. Beve un sorso, poi me lo rende pieno a metà. Per una sera, il conto è pari davvero."
        "Lasciarlo nel panno":
            $ ricordi_usati["bicchiere"] = "tenuto"
            icaro "Il vino di stasera si beve a canna. Come i debiti pari: senza testimoni."
            "Beve dalla bottiglia. Il bicchiere resta nel panno. Lui guarda il panno una volta, poi la strada."
    $ conseguenze_aggiorna()
    return

# Moneta (Icaro, la partita: «smaschera»): sera, una posta scoperta.
label echi_ricordo_moneta:
    scene bg vicoli_zefiro with dissolve
    show icaro neutro at left with dissolve
    "Sotto il portico della Consorteria si gioca a dadi su un barile. Un carrettiere di Marcassa tiene il banco. Mi manca uno Scudo per coprire la posta, e la posta è già sul legno."
    menu:
        "In tasca c'è la moneta del piatto. Icaro, dall'altra parte del portico, mi guarda le mani."
        "Mettere la moneta sul barile":
            $ ricordi_usati["moneta"] = "mostrato"
            "La moneta non tocca il legno. Due dita la prendono a mezz'aria. Non l'ho visto arrivare."
            show icaro irritato with qdiss
            icaro "Questa no. È fuori corso. Ricordo, non ricompensa: e nemmeno posta."
            "Me la rimette in tasca, nella stessa tasca, e copre la posta con uno Scudo suo. «Interesse a parte», dice."
        "Tenerla in tasca e lasciare la posta scoperta":
            $ ricordi_usati["moneta"] = "tenuto"
            "Ritiro la mano. Il carrettiere si prende la posta con un ghigno, e io perdo il giro."
            show icaro furbo with qdiss
            icaro "Potevi giocarla. Nessuno l'avrebbe distinta dalle altre."
            icaro "Io sì. Annotato."
    $ conseguenze_aggiorna()
    return

# Rosa (Ofelia, ev4 in segreto): Druso la fiuta in taverna.
label echi_ricordo_rosa:
    scene bg vicoli_zefiro with dissolve
    show druso ghigno at left with easeinleft
    druso "Novellin[fin]! Che cos'hai lì, nel mantello? Odore di serra. Di serra di Glauco, per la precisione."
    "Il naso di un poeta: fiuta i segreti come i porci i tartufi. La rosa nera è nella fodera, e lui lo sa già a metà."
    menu:
        "La taverna si sporge. Per sentire, non per aiutare."
        "Tirarla fuori: che si sappia":
            $ ricordi_usati["rosa"] = "mostrato"
            show druso sorpreso with qdiss
            druso "Una rosa nera. Ce n'è una sola, a Rocca Tempesta, che le coltiva fino all'osso."
            show druso ghigno with qdiss
            druso "Componimento immediato: «Spina nel pugno, serra nel letto...» Il resto domani, quando il verso si sarà sporcato abbastanza."
            "La taverna ride. Domani lo sentirà anche la serra. Ofelia non ama le cose che si sanno. Nemmeno quelle belle."
        "«È mia. E resta nel mantello.»":
            $ ricordi_usati["rosa"] = "tenuto"
            show druso irritato with qdiss
            druso "Avaro di segreti! Il peggiore degli avari! Mio fratello Icaro almeno i soldi li fa vedere."
            show druso neutro with qdiss
            druso "...va bene. Tienila. Ma se è di chi penso, guardati le spalle. Le spine, laggiù, crescono anche sui coltelli."
            "La rosa resta nella fodera. Il segreto, per stasera, è ancora nostro."
    $ conseguenze_aggiorna()
    return
