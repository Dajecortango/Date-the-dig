# Regia — transizioni condivise dalle route.
#
# Convenzioni:
#   - personaggio della route (Aede, Caino): center / right quando c'è un
#     comprimario in scena; comprimari (Druso, Glauco ospite) a left.
#   - prima entrata in scena: easeinright / easeinleft (scivolata breve);
#   - cambio espressione dello stesso personaggio gia' in scena: "with qdiss"
#     (dissolve rapido: lo stacco emotivo arriva subito);
#   - colpi forti (schiaffo, urlo, shock): "with vpunch" / "with hpunch".

define qdiss = Dissolve(0.15)

# Lampo bianco brevissimo: colpo di lama, rivelazione improvvisa.
define lampo = Fade(0.08, 0.0, 0.25, color="#fff")

# Stacco a tema per i cambi scena: dissolvenza diagonale (alto-sinistra per
# primo), come le righe del pattern Dignitas. Maschera: make_gui.py.
define stacco = ImageDissolve("gui/transizione_diagonale.png", 0.8, ramplen=128)

# Lampo d'oro: momenti solenni e cartelli dei good end.
define lampo_oro = Fade(0.25, 0.15, 0.9, color="#d4af37")

# Transizioni di sistema (qui e non in options.rpy: usano lo stacco).
define config.after_load_transition = stacco
define config.end_game_transition = Fade(0.5, 0.2, 0.6, color="#100c0c")
define config.intra_transition = Dissolve(0.2)

# Micro-movimenti a mano (i cambi di espressione li fanno gia' da soli,
# luce.rpy). Sono relativi: vanno DOPO la posizione, mai da soli, o lo
# sprite perde il posto:  show aede neutra at right, trema
# Con "Animazioni: No" restano fermi.
init python:
    def _mov_manuale(nome):
        def f(trans, st, at):
            if mm_movimento_ridotto() or renpy.is_skipping():
                k = 1.0
            else:
                k = st / MOVIMENTO_DURATA
            if k >= 1.0:
                trans.xoffset, trans.yoffset, trans.zoom = 0, 0, 1.0
                return None
            trans.xoffset, trans.yoffset, trans.zoom = _lu_curva(nome, k)
            return 0
        return f

transform sobbalzo:
    function _mov_manuale("sobbalzo")

transform arretra:
    function _mov_manuale("arretra")

transform avanza:
    function _mov_manuale("avanza")

transform trema:
    function _mov_manuale("trema")

# Indicatore "continua" in coda al testo (ctc nestled): diamantino che pulsa
# (screens.rpy); in auto-avanzamento gira su se stesso; fermo con
# "Animazioni: No". Lo eredita ogni Character (kind=adv di default).
init -1 python:
    adv = Character(None, kind=adv, ctc="ctc_continua", ctc_position="nestled")
    _narrator = Character(None, kind=adv, what_style="say_thought")
    name_only = adv

init python:
    def _ctc_scelta(st, at):
        if mm_movimento_ridotto():
            return "gui/ctc.png", None
        if _preferences.afm_enable:
            return "ctc_auto", None
        return "ctc_diamante", None

transform ctc_gira:
    align (0.5, 0.5)
    rotate 0
    linear 1.6 rotate 360
    repeat

image ctc_auto = Fixed(At("gui/ctc.png", ctc_gira), xysize=(30, 30))
image ctc_continua = DynamicDisplayable(_ctc_scelta)

# Pensieri del protagonista: senza nome, corsivo, colore tenue.
define pensiero = Character(None, what_italic=True, what_color="#c9bfa8")

# Vocabolario delle transizioni (oltre a stacco, lampo, lampo_oro):
#   salto_tempo -> stesso luogo, piu' tardi (nero lungo);
#   shock       -> colpo improvviso senza schiaffo (pixel che si sfaldano);
#   ricordo     -> apertura di un ricordo (bagliore chiaro, lento).
# Con "Animazioni: No" shock e ricordo diventano una dissolvenza breve.
define salto_tempo = Fade(0.5, 0.4, 0.5)
define shock = Pixellate(0.3, 4)
define ricordo = Fade(0.6, 0.0, 0.9, color="#f5e3b8")

# Profondita' di campo: $ intimo() sfoca lo sfondo (mai gli sprite),
# $ fine_intimo() la toglie; ogni "scene" la toglie da sola (luce.rpy,
# fondo_fx). E' nello store: rollback e salvataggi la ritrovano.
default regia_intimo = False

# Camera (layer master): $ camera_dentro(), $ camera_su(x), $ camera_panoramica(),
# $ camera_riposo(). Ogni "scene" e ogni caricamento la rimettono a riposo.
# Con "Animazioni: No" non si muove.
transform cam_dentro:
    subpixel True
    xalign 0.5 yalign 0.5
    ease 1.5 zoom 1.08

transform cam_su(x):
    subpixel True
    yalign 0.4
    ease 1.5 xalign x zoom 1.08

transform cam_panoramica:
    subpixel True
    yalign 0.5 xalign 0.0 zoom 1.1
    ease 6.0 xalign 1.0
    ease 1.0 xalign 0.5 zoom 1.0

transform cam_riposo:
    subpixel True
    ease 0.5 xalign 0.5 yalign 0.5 zoom 1.0

init python:
    def intimo():
        store.regia_intimo = True

    def fine_intimo():
        store.regia_intimo = False

    def _camera(t):
        if not mm_movimento_ridotto():
            renpy.show_layer_at([t], layer="master", camera=True)

    def camera_dentro():
        _camera(cam_dentro)

    def camera_su(x):
        _camera(cam_su(x))

    def camera_panoramica():
        _camera(cam_panoramica)

    def camera_riposo():
        renpy.show_layer_at([cam_riposo], layer="master", camera=True)

    def camera_riposo_subito():
        renpy.show_layer_at([], layer="master", camera=True)

    config.after_load_callbacks.append(camera_riposo_subito)

    # Ogni "scene" sul master: camera a riposo, sfocatura tolta.
    _regia_scene_prec = config.scene

    def _regia_scene(layer="master"):
        if layer == "master":
            store.regia_intimo = False
            camera_riposo_subito()
        _regia_scene_prec(layer)

    config.scene = _regia_scene

    # shock / ricordo con "Animazioni: No": dissolvenza breve. Si concatena
    # con l'effetto audio (audio.rpy).
    _regia_with_prec = config.with_callback

    def _regia_con_transizione(trans, paired):
        if mm_movimento_ridotto() and (trans is store.shock or trans is store.ricordo):
            trans = Dissolve(0.2)
        if _regia_with_prec is not None:
            trans = _regia_with_prec(trans, paired)
        return trans

    config.with_callback = _regia_con_transizione
