# Route Ofelia — "Tanto bella quanto letale". Difficoltà 4/5.
# Lucchetto dei mancati: Ofelia non aspetta. Ogni suo invito lasciato cadere
# costa un punto; al secondo, per lei sei già un nome tra tanti (congelata).
# Poliamore possibile solo con Aede (che NON sa e NON accetta) e con Caino
# (dichiarato). Mai con Druso o Icaro.

define ofelia = Character("Ofelia", color="#7d3c98", image="ofelia")

default ofelia_affinity = 0
default ofelia_mancati = 0
default route_seconda = None
default aede_sospetto = 0
# Esiti separati degli impegni a coppia (poliamore): Ofelia / l'altro.
default impegno_of = False
default impegno_altro = False
# Prove del poliamore segreto con Aede: cosa puo' rinfacciare nella tempesta.
default ofelia_mano_cala = False
default ofelia_in_pubblico = False
# Deviazioni: "rosso" | "tutti" | "specchio"; "rifiuto" | "biondo" | "me".
default ofelia_specchio_esito = None
default ofelia_ballo_esito = None

init python:
    ATTIVITA["pomeriggio"].append(
        ("corte", "La corte di Ofelia", "ofelia",
         ["att_corte_1", "att_corte_2", "att_corte_3"]))

    # Invito di Ofelia lasciato cadere (scelto altro o un'attivita'): mancato.
    # Conteggio in rlz.ofelia_esiti_scadenza: congela a ofelia_mancati >= 2
    # (rlz.OFELIA_GELO), al primo (ofelia_mancati == 1) la scena di avviso.
    def ofelia_scadenza(ids):
        for esito in rlz.ofelia_esiti_scadenza(
                ids, store.ofelia_mancati, "ofelia" in store.congelate):
            store.ofelia_mancati += 1
            store.ofelia_affinity -= 1
            if esito == "gelo":
                store.congelate.add("ofelia")
                renpy.notify("Per Ofelia sei già un nome tra tanti.")
            elif esito == "prima":
                renpy.call_in_new_context("ofelia_scadenza_prima")
            else:
                renpy.notify("Ofelia non aspetta nessuno.")

    cal_inviti_ignorati_hooks.append(ofelia_scadenza)
