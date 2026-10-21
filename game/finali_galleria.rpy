# Galleria dei finali: registro persistente (sopravvive tra le partite).

default persistent.finali_visti = set()

init python:

    # (id, titolo, route, indizio) -- un indizio orienta, non spiega la soglia.
    FINALI = [
        ("good_end", "TEMPESTA D'AMORE", "Aede",
         "Convinci Aede a disobbedire a Glauco, e che la lama la scelga lei."),
        ("neutral_end", "I DEBITI E L'ASSENZA", "Aede",
         "Resta vicino ad Aede, ma non abbastanza da farle cambiare strada."),
        ("bad_end_aede", "IL NORD NON PERDONA", "Aede",
         "Conosci i suoi segreti, ma lei non ti ha mai davvero lasciato entrare."),
        ("bad_end_glauco", "LA PAROLA DI GLAUCO", "Aede",
         "Muoviti nel buio senza sapere chi ti protegge, e senza averla avvicinata."),
        ("caino_good_end", "LA LEGGE DEL CUORE", "Caino",
         "Sii affidabile nei registri e nei fatti, e non cadere nelle sue trappole."),
        ("caino_secret_end", "TESCHIO", "Caino",
         "Dai tempo a Druso, e lascia che Caino non si fidi fino in fondo."),
        ("caino_bad_end", "LA PEDINA", "Caino",
         "Diventa un nome comodo da sacrificare: troppe cadute o troppa distanza."),
        ("caino_neutral_end", "SOCI", "Caino",
         "Una fiducia onesta ma a metà, senza chiudere né il debito né il patto."),
        ("druso_good", "IL CUORE PROVOCATORE", "Druso",
         "Stagli accanto anche quando lo deridono, mostra coraggio, e davanti al Ramo non parlare al posto suo."),
        ("druso_neutral", "IL POSTO ACCANTO", "Druso",
         "Una bella amicizia, ma senza il gesto che lo convinca a restare."),
        ("druso_bad", "IL CANE CHE ABBAIA", "Druso",
         "Lascialo solo con le sue battute finché nessuno lo prende sul serio."),
        ("icaro_good", "UNTOUCHABLE", "Icaro",
         "Mentigli a favore la prima volta che il tavolo lo accusa, e non sbagliare una mano fino all'ultima."),
        ("icaro_neutral", "IL SOCIO", "Icaro",
         "Fai affari con lui senza mai diventare altro che un buon cliente."),
        ("icaro_bad", "FUORI LISTINO", "Icaro",
         "Passa poco tempo al suo tavolo e lasciagli il conto da pagare."),
        ("icaro_bro_listino", "LISTINO CHIUSO", "Icaro",
         "Come amico, guadagnati la sua fiducia e impegnati per davvero."),
        ("icaro_bro_conti", "CONTI APERTI", "Icaro",
         "Come amico, resta sulla soglia della sua saletta senza mai entrare."),
        ("ofelia_good", "TANTO BELLA QUANTO LETALE", "Ofelia",
         "Non mancare agli inviti, e reggi il colpo davanti a suo padre."),
        ("ofelia_good_caino", "IL CONTRATTO A TRE", "Ofelia",
         "Conquista Ofelia senza mancarle, ma tieni caro anche il Custode dei registri."),
        ("ofelia_good_aede", "LE FIGLIE DI GLAUCO", "Ofelia",
         "Due sorelle, un solo bersaglio: guadagna Aede, senza destare sospetti."),
        ("ofelia_bad_tempesta", "LA TEMPESTA", "Ofelia",
         "Amare due figlie di Glauco di nascosto ha un prezzo, e arriva presto."),
        ("ofelia_neutral", "INTERESSE PASSEGGERO", "Ofelia",
         "Ofelia non aspetta chi manca spesso o non la prende sul serio."),
        ("finale_neutro_semestre", "IL SEMESTRE DEL NOVELLINO", "Semestre",
         "Attraversa il semestre senza legarti a nessuno, guardando e basta."),
    ]

    GALLERIA_ROUTE = ["Aede", "Caino", "Druso", "Icaro", "Ofelia", "Semestre"]

    def sblocca_finale(fid):
        if persistent.finali_visti is None:
            persistent.finali_visti = set()
        persistent.finali_visti.add(fid)
        renpy.save_persistent()

screen galleria_finali():

    tag menu

    use game_menu(_("Finali"), scroll="viewport"):

        vbox:
            spacing 10
            xfill True

            $ visti = persistent.finali_visti or set()
            $ n_visti = len([f for f in FINALI if f[0] in visti])

            text "Finali scoperti: [n_visti] / [len(FINALI)]" size 32 color gui.accent_color

            for gruppo in GALLERIA_ROUTE:

                null height 12
                text gruppo size 28 color "#f5e3b8"

                for fid, titolo, route, indizio in FINALI:
                    if route == gruppo:
                        if fid in visti:
                            text titolo size 24 color "#e0b75a"
                        else:
                            vbox:
                                text "???" size 24 color "#8a8578"
                                text indizio size TESTO_NOTA color "#8a8578" italic True
