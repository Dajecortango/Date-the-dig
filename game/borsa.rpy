# Borsa: gli Scudi a schermo e l'inventario.
#
# - Overlay "borsa_hud": moneta + Scudi in una pillola leggera in alto a
#   destra. Fissa nel pianificatore; durante le scene compare solo quando
#   Scudi o borsa cambiano (con +N / -N) e sparisce da sola. Toccarla apre
#   l'inventario. Lo snapshot vive fuori dallo store (NoRollback), come il
#   feedback delle affinita' (feedback.rpy).
# - Screen "inventario" (menu di gioco, sigillo Borsa del menu rapido): gli
#   Scudi, il dono in borsa e i ricordi raccolti nelle scene.
# - I ricordi si derivano dallo stato gia' scritto dalle scene (come i FATTI
#   di conseguenze.rpy): nessuna scena cambia per produrli.

init python:
    import time as _bo_time
    import regia_logic as rgl

    # Ricordi: (id, nome, descrizione, cond(vars)). Solo oggetti che le scene
    # mettono davvero in mano al protagonista.
    RICORDI = [
        ("nodo", "Il nodo di corda",
         "Al polso, come tutti i Figli del primo anno di Briseide. Si toglie solo quando il Ceppo lo decide.",
         lambda v: True),
        ("tazza", "Una tazza di Glostok, senza crepe",
         "La tua parte dell'affare di Icaro. «Non è un regalo. È una garanzia.»",
         lambda v: "icaro_bro1" in v["visti"]),
        ("bicchiere", "Un bicchiere di cristallo di Glostok",
         "Trovato sotto la porta, il mattino dopo la partita. Il cartellino del magazzino di Icaro è ancora attaccato.",
         lambda v: v["icaro_partita"] == "copre"),
        ("moneta", "Una moneta del piatto",
         "Icaro te l'ha infilata in tasca, fuori dalla saletta. «Ricordo. Non ricompensa.»",
         lambda v: v["icaro_partita"] == "smaschera"),
        ("rosa", "Una rosa nera",
         "Ofelia te l'ha messa in mano tra due banchi di spezie, senza guardarti. I segreti durano poco, come le rose.",
         lambda v: "ofelia_ev4" in v["visti"] and not v["ofelia_in_pubblico"]),
    ]

    def borsa_vars():
        return {"visti": store.eventi_visti,
                "icaro_partita": store.icaro_partita,
                "ofelia_in_pubblico": store.ofelia_in_pubblico,
                # Ricordi aggiunti da economia_extra.rpy.
                "debito_esito": getattr(store, "debito_esito", None),
                "eco_orfani_dato": getattr(store, "eco_orfani_dato", False)}

    def borsa_ricordi():
        v = borsa_vars()
        return [(nome, desc) for _id, nome, desc, cond in RICORDI if cond(v)]

    def borsa_dono():
        """(nome, costo) del dono in borsa, o None."""
        if store.dono_tenuto is None:
            return None
        nome, costo = DONI[store.dono_tenuto]
        return (nome[0].upper() + nome[1:], costo)

    ## Comparsa a tempo durante le scene ####################################

    BORSA_DURATA = 3.0
    MONETA_VOLO = 0.55       # secondi di volo di una moneta verso la Borsa
    MONETA_PASSO = 0.06      # secondi tra una moneta e la successiva

    class _BorsaStato(NoRollback):
        def __init__(self):
            self.snap = None     # (scudi, dono_tenuto); None = da allineare
            self.delta = 0       # ultima variazione di Scudi da mostrare
            self.fino = 0.0      # time() fino a cui la pillola resta visibile
            self.da = 0          # Scudi di partenza del contatore che scorre
            self.t0 = 0.0        # time() d'inizio del contatore (0 = fermo)
            self.volo = None     # (monete, verso +1/-1, time() d'inizio)

    _bo = _BorsaStato()

    def _bo_reset():
        _bo.snap = None
        _bo.fino = 0.0
        _bo.t0 = 0.0
        _bo.volo = None

    def _bo_controlla():
        """start_interact_callback: Scudi o dono cambiati -> mostra."""
        if store.main_menu or store._in_replay:
            _bo_reset()
            return
        cur = (store.scudi, store.dono_tenuto)
        if (_bo.snap is None or renpy.game.after_rollback
                or renpy.in_rollback()):
            _bo.snap = cur
            _bo.fino = 0.0
            _bo.t0 = 0.0
            _bo.volo = None
            return
        if cur != _bo.snap:
            _bo.delta = cur[0] - _bo.snap[0]
            if _bo.delta:
                _bo.da = _bo.snap[0]
                _bo.t0 = _bo_time.time()
                if not (mm_movimento_ridotto() or renpy.is_skipping()):
                    _bo.volo = (rgl.monete_per(_bo.delta),
                                1 if _bo.delta > 0 else -1, _bo_time.time())
                    # Guadagno: il contatore parte quando arriva la prima moneta.
                    if _bo.delta > 0:
                        _bo.t0 += MONETA_VOLO
            _bo.fino = _bo_time.time() + BORSA_DURATA
            _bo.snap = cur
            if _bo.delta:
                audio_monete()

    ## Contatore che scorre dal vecchio al nuovo valore (~0.6 s), con un
    ## riflesso che passa sullo scudo. Fermo in skip o con "Animazioni: No".

    def _bo_contando():
        if not _bo.t0 or mm_movimento_ridotto() or renpy.is_skipping():
            return False
        return _bo_time.time() - _bo.t0 < 0.6

    def _bo_numero(st, at):
        v = rgl.conteggio(_bo.da, store.scudi, _bo_time.time() - _bo.t0)
        return Text(str(v), style="borsa_pillola_text"), (0.03 if v != store.scudi else None)

    def _bo_scadi():
        if _bo.fino and _bo_time.time() >= _bo.fino:
            _bo.fino = 0.0
            renpy.restart_interaction()

    def borsa_hud_visibile():
        if store.main_menu or not store.quick_menu or _windows_hidden:
            return False
        if renpy.get_screen("cartello_data") or renpy.get_screen("input"):
            return False
        return bool(renpy.get_screen("pianificazione")) or _bo.fino > 0

    config.start_interact_callbacks.append(_bo_controlla)
    config.after_load_callbacks.append(_bo_reset)
    config.overlay_screens.append("borsa_hud")
    config.overlay_screens.append("borsa_monete")

    def _bo_volo_attivo():
        if _bo.volo is None:
            return False
        n, _verso, t = _bo.volo
        if _bo_time.time() > t + MONETA_VOLO + n * MONETA_PASSO + 0.3:
            _bo.volo = None
            return False
        return True

    def _bo_fine_volo():
        if _bo.volo is not None and not _bo_volo_attivo():
            renpy.restart_interaction()


transform borsa_comparsa:
    on show:
        alpha 0.0 yoffset -12
        ease 0.25 alpha 1.0 yoffset 0
    on hide:
        ease 0.4 alpha 0.0

transform borsa_luccica:
    alpha 0.0 xoffset -30
    linear 0.25 alpha 0.8 xoffset 0
    linear 0.25 alpha 0.0 xoffset 30

transform borsa_delta:
    on show:
        alpha 0.0 yoffset 6
        ease 0.3 alpha 1.0 yoffset 0
        pause 1.6
        ease 0.6 alpha 0.0 yoffset -8

screen borsa_hud():
    zorder 55

    if _bo.fino:
        timer 0.25 repeat True action Function(_bo_scadi)

    if borsa_hud_visibile():
        button at borsa_comparsa:
            style "borsa_pillola"
            xalign 1.0 xoffset -28 ypos 24
            action ShowMenu("inventario")
            tooltip _("Borsa e oggetti")
            hbox:
                spacing 8
                if _bo_contando():
                    fixed:
                        fit_first True
                        yalign 0.5
                        add "gui/scudo.png" zoom 0.7
                        add AlphaMask(At("gui/scudo_luccichio.png", borsa_luccica), "gui/scudo.png") zoom 0.7
                    add DynamicDisplayable(_bo_numero) yalign 0.5
                else:
                    add "gui/scudo.png" zoom 0.7 yalign 0.5
                    text "[scudi]" style "borsa_pillola_text"
                if dono_tenuto is not None:
                    text "· 1 dono" style "borsa_pillola_nota"
                if _bo.fino and _bo.delta:
                    text ("%+d" % _bo.delta) at borsa_delta style "borsa_pillola_nota" color ("#9fcf7f" if _bo.delta > 0 else "#e08a74")

style borsa_pillola is button
style borsa_pillola:
    background Frame("gui/borsa_pillola.png", 21, 21)
    hover_background Frame("gui/borsa_pillola.png", 21, 21)
    padding (14, 6, 20, 6)

style borsa_pillola_text is text
style borsa_pillola_text:
    font gui.name_text_font
    size (30 if renpy.variant("small") else 24)
    color "#f0c75e"
    hover_color "#ffffff"
    yalign 0.5
    outlines [(1, "#140a08", 0, 0)]

style borsa_pillola_nota is text
style borsa_pillola_nota:
    font gui.text_font
    size (22 if renpy.variant("small") else 18)
    italic True
    color "#c9b78a"
    yalign 0.5


## Inventario #################################################################

screen inventario():

    tag menu

    use game_menu(_("Borsa"), scroll="viewport"):

        vbox:
            spacing 18
            xfill True

            hbox:
                spacing 16
                add "gui/scudo.png" yalign 0.5
                text "[scudi] Scudi" style "cronache_titolo" yalign 0.5
            text "Paghe dei registri, commissioni del Ceppo, qualche colpo di fortuna. Al mercato coperto diventano doni." size TESTO_NOTA italic True color "#8f7f5c"

            add "gui/divisore.png" xalign 0.0

            text "Il dono in borsa" style "inventario_sezione"
            $ inv_dono = borsa_dono()
            if inv_dono:
                hbox:
                    spacing 14
                    text "◆" size 18 color "#c0392b" yoffset 8
                    vbox:
                        spacing 2
                        text inv_dono[0] style "inventario_nome"
                        text "Pagato [inv_dono[1]] Scudi. Alla fine di un incontro potrai offrirlo. Un dono alla volta: chi lo riceve non lo dimentica." style "inventario_desc"
            else:
                text "Nessuno. Il mercato coperto apre il pomeriggio, se hai almeno due Scudi." style "inventario_desc"

            # Debiti e soffiate: economia_extra.rpy.
            $ inv_debiti = eco_debiti_righe()
            if inv_debiti:
                null height 6
                text "Debiti" style "inventario_sezione"
                for nome, desc in inv_debiti:
                    hbox:
                        spacing 14
                        text "◆" size 18 color "#c0392b" yoffset 8
                        vbox:
                            spacing 2
                            text nome style "inventario_nome"
                            text desc style "inventario_desc"

            $ inv_soffiate = eco_soffiate_righe()
            if inv_soffiate:
                null height 6
                text "Soffiate" style "inventario_sezione"
                for nome, desc in inv_soffiate:
                    hbox:
                        spacing 14
                        text "◆" size 18 color "#8f7f5c" yoffset 8
                        vbox:
                            spacing 2
                            text nome style "inventario_nome"
                            text desc style "inventario_desc"

            null height 6
            text "Ricordi" style "inventario_sezione"
            for nome, desc in borsa_ricordi():
                hbox:
                    spacing 14
                    text "◆" size 18 color "#d4af37" yoffset 8
                    vbox:
                        spacing 2
                        text nome style "inventario_nome"
                        text desc style "inventario_desc"

style inventario_sezione is text
style inventario_sezione:
    font gui.name_text_font
    size 30
    color gui.accent_color
    outlines [(2, "#140a08", 0, 0)]

style inventario_nome is text
style inventario_nome:
    font gui.text_font
    size 26
    color "#f0e6d2"

style inventario_desc is text
style inventario_desc:
    font gui.text_font
    size TESTO_NOTA
    italic True
    color "#c9b78a"


## Monete che volano: dal centro basso alla pillola della Borsa quando gli
## Scudi salgono (arco: x accelera, y frena), o cadono dalla Borsa quando
## scendono. La chiave (istante del volo) fa ripartire le animazioni.

transform moneta_vola(ritardo, chiave):
    xanchor 0.5 yanchor 0.5 xpos 960 ypos 880 zoom 0.8 alpha 0.0
    pause ritardo
    alpha 1.0
    parallel:
        easein 0.55 xpos 1790
    parallel:
        easeout 0.55 ypos 44
    linear 0.1 alpha 0.0

transform moneta_cade(ritardo, chiave):
    xanchor 0.5 yanchor 0.5 xpos 1790 ypos 50 zoom 0.8 alpha 0.0
    pause ritardo
    alpha 1.0
    parallel:
        easein 0.5 ypos 170
    parallel:
        linear 0.5 alpha 0.0

screen borsa_monete():
    zorder 56

    if _bo_volo_attivo():
        timer 0.2 repeat True action Function(_bo_fine_volo)
        $ _bo_n, _bo_verso, _bo_chiave = _bo.volo
        for _bo_i in range(_bo_n):
            if _bo_verso > 0:
                add "gui/scudo.png" at moneta_vola(_bo_i * MONETA_PASSO, _bo_chiave)
            else:
                add "gui/scudo.png" at moneta_cade(_bo_i * 0.08, _bo_chiave)
