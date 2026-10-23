# Route Druso — "Il cuore provocatore".
# Lucchetto a rovescio: l'affinità sale solo tenendogli testa. Per un uomo
# la salita è più ripida: due passi falsi e Druso archivia (5/5 contro 4/5).
# Gli interludi (druso_int1-3, druso_luna6) sono a punti zero: solo testo.

default druso_passi_falsi = 0
default flag_druso_coraggio = False
# Scelta davanti al Consiglio (druso_climax): "parla" | "lascia" | "battuta".
default druso_consiglio = None
default druso_sfida = None
# Deviazioni: "detto" | "chiuso" | "nascosto"; "neve" | "chiesto" | "aspettato".
default druso_quaderno_esito = None
default druso_udienza_esito = None

init python:
    def druso_passo_falso():
        # I passi falsi contano solo se player_gender == "m" (rl).
        store.druso_affinity -= 1
        passi, avvisa, congela = rl.druso_passo_falso(
            store.player_gender, store.druso_passi_falsi)
        store.druso_passi_falsi = passi
        if avvisa:
            renpy.notify("Druso se la segna.")
        if congela:
            store.congelate.add("druso")
