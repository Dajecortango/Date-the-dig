# Luce dei personaggi: tinta del luogo, chi non parla si scurisce, piccoli
# movimenti quando cambia l'espressione.
#
# Ogni sprite in images/ ("<tag> <espressione>") e' ridefinito qui come
# At(file, luce_personaggio(tag)): l'effetto vive dentro l'immagine, quindi
# le righe "show" restano come sono e la posizione (left/center/right) non
# si perde. Regole pure in regia_logic.py:
#   - tinta: sfondo in scena -> colore tenue (solo sprite, sfondi intatti);
#   - luce: con 2+ sprite in scena, chi ascolta scende al 75% mentre parla
#     un personaggio con sprite; narratore, protagonista e pensieri: tutti
#     a luce piena;
#   - movimento: sobbalzo / arretra / avanza al cambio di espressione
#     (mai alla prima entrata), non piu' di uno ogni 3 interazioni per tag.
# Stato per tag fuori dallo store (NoRollback): niente salvataggi. Si
# azzera dopo un caricamento e al menu principale.
# Con "Animazioni: No" la luce cambia di colpo e niente si muove.

init 1 python:
    import math as _lu_math
    import os as _lu_os
    import time as _lu_time
    import regia_logic as rgl

    LUCE_PASSAGGIO = 0.2     # secondi per scurire/schiarire
    MOVIMENTO_DURATA = 0.35
    DRUSO_RITARDO = 0.3      # il tonfo parte quando finisce la scivolata

    class _LuceStato(NoRollback):
        def __init__(self):
            self.reset()

        def reset(self):
            self.luce = {}     # tag -> (valore attuale, istante)
            self.attr = {}     # tag -> espressione vista per ultima
            self.mov = {}      # tag -> (nome movimento, istante d'inizio)
            self.ultimo = {}   # tag -> interazione dell'ultimo movimento
            self.n = 0         # contatore interazioni
            self.presenti = None   # tag in scena all'interazione prima

    _lu = _LuceStato()

    def _lu_in_scena():
        return [t for t in renpy.get_showing_tags("master") if t != "bg"]

    def _lu_bg():
        attr = renpy.get_attributes("bg", layer="master") or ()
        return attr[0] if attr else None

    def _lu_interazione():
        _lu.n += 1
        if store.main_menu:
            _lu.reset()
            return
        # Chi esce di scena perde l'espressione vista: rientrando non si muove.
        presenti = set(_lu_in_scena())
        for tag in list(_lu.attr):
            if tag not in presenti:
                del _lu.attr[tag]
        # Druso entra col suo tonfo, a fine scivolata (mai dopo un caricamento).
        if (_lu.presenti is not None and "druso" in presenti
                and "druso" not in _lu.presenti
                and not mm_movimento_ridotto() and not renpy.is_skipping()):
            _lu.mov["druso"] = ("tonfo", _lu_time.time() + DRUSO_RITARDO)
            _lu.ultimo["druso"] = _lu.n
        _lu.presenti = presenti

    config.start_interact_callbacks.append(_lu_interazione)
    config.after_load_callbacks.append(_lu.reset)

    def _lu_hex(c):
        c = c.lstrip("#")
        return tuple(int(c[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    def _lu_moltiplicatore(tinta, luce):
        if tinta is None:
            r = g = b = 1.0
        else:
            tr, tg, tb = _lu_hex(tinta)
            f = rgl.TINTA_FORZA
            r, g, b = 1.0 - f + tr * f, 1.0 - f + tg * f, 1.0 - f + tb * f
        return (r * luce, g * luce, b * luce)

    def _lu_curva(nome, k):
        """(xoffset, yoffset, zoom) del movimento a k in [0, 1]."""
        s = _lu_math.sin(_lu_math.pi * k)
        if nome == "sobbalzo":
            return (0, -18 * s, 1.0)
        if nome == "arretra":
            return (0, 6 * s, 1.0 - 0.03 * s)
        if nome == "avanza":
            return (0, 0, 1.0 + 0.03 * s)
        if nome == "tonfo":
            return (0, 10 * s, 1.0 + 0.02 * s)
        if nome == "trema":
            return (4 * _lu_math.sin(k * 40) * (1.0 - k), 0, 1.0)
        return (0, 0, 1.0)

    def _lu_luce(tag, ora, fermo):
        voluta = rgl.LUCE_OSCURATA if rgl.oscurato(
            tag, renpy.get_say_image_tag(), _lu_in_scena()) else 1.0
        valore, prima = _lu.luce.get(tag, (voluta, ora))
        if fermo:
            valore = voluta
        else:
            passo = (ora - prima) / LUCE_PASSAGGIO * (1.0 - rgl.LUCE_OSCURATA)
            if valore < voluta:
                valore = min(voluta, valore + passo)
            else:
                valore = max(voluta, valore - passo)
        _lu.luce[tag] = (valore, ora)
        return valore, valore != voluta

    def _lu_movimento(tag, ora, fermo):
        attr = renpy.get_attributes(tag, layer="master") or ()
        espr = attr[0] if attr else None
        vecchia = _lu.attr.get(tag)
        if espr is not None and espr != vecchia:
            _lu.attr[tag] = espr
            nome = rgl.movimento_per(vecchia, espr)
            if (nome and not fermo and not renpy.is_skipping()
                    and _lu.n - _lu.ultimo.get(tag, -99) >= rgl.MOVIMENTO_PAUSA):
                _lu.mov[tag] = (nome, ora)
                _lu.ultimo[tag] = _lu.n
        if tag not in _lu.mov:
            return (0, 0, 1.0), False
        nome, t0 = _lu.mov[tag]
        if ora < t0:
            return (0, 0, 1.0), True
        k = (ora - t0) / MOVIMENTO_DURATA
        if k >= 1.0 or fermo:
            del _lu.mov[tag]
            return (0, 0, 1.0), False
        return _lu_curva(nome, k), True

    def luce_personaggio(tag):
        def f(trans, st, at):
            ora = _lu_time.time()
            fermo = mm_movimento_ridotto()
            luce, luce_viva = _lu_luce(tag, ora, fermo)
            slot = getattr(store, "cal_slot", None)
            bg = _lu_bg()
            r, g, b = _lu_moltiplicatore(rgl.tinta_per(bg, slot), luce)
            vivo = not fermo and not renpy.is_skipping()
            if vivo and rgl.fuoco_per(bg, slot):
                fl = rgl.fiamma(ora)
                r, g, b = r * fl, g * fl, b * fl
            trans.matrixcolor = TintMatrix(Color(rgb=(min(r, 1.0), min(g, 1.0), min(b, 1.0))))
            (dx, dy, z), mov_vivo = _lu_movimento(tag, ora, fermo)
            trans.xoffset = dx
            trans.yoffset = dy
            trans.zoom = z * (rgl.respiro(ora, rgl.fase_per(tag)) if vivo else 1.0)
            # Animazione in corso: ogni frame. Respiro e fuoco: 30 fps (15
            # su telefono). Da fermi: un controllo leggero, per accorgersi
            # di chi parla e del cambio di sfondo.
            if luce_viva or mov_vivo:
                return 0
            if vivo:
                return SPRITE_PASSO
            return 0.1
        return Transform(function=f)

    SPRITE_PASSO = 1.0 / 15 if renpy.variant("small") else 1.0 / 30

    def muovi(tag, nome):
        """Movimento a mano su uno sprite in scena (sobbalzo, arretra,
        avanza, trema, tonfo): la posizione resta quella dello show."""
        if mm_movimento_ridotto() or renpy.is_skipping():
            return
        if tag not in _lu_in_scena():
            return
        if _lu.n - _lu.ultimo.get(tag, -99) < rgl.MOVIMENTO_PAUSA:
            return
        _lu.mov[tag] = (nome, _lu_time.time())
        _lu.ultimo[tag] = _lu.n

    ## Sfondi: sfocatura della profondita' di campo (regia_intimo, regia.rpy),
    ## blur 0 <-> 6 in 0.4 s, con uno zoom minimo che nasconde i bordi sfumati.
    ## Dopo un caricamento o una "scene" il valore si allinea di colpo.
    FONDO_BLUR = 6.0
    FONDO_PASSAGGIO = 0.4

    class _FondoStato(NoRollback):
        def __init__(self):
            self.k = None    # 0 = nitido, 1 = sfocato; None = da allineare
            self.t = 0.0

    _fo = _FondoStato()

    def _fo_reset():
        _fo.k = None

    config.after_load_callbacks.append(_fo_reset)

    def fondo_fx():
        def f(trans, st, at):
            ora = _lu_time.time()
            voluto = 1.0 if getattr(store, "regia_intimo", False) else 0.0
            if _fo.k is None or mm_movimento_ridotto():
                _fo.k = voluto
            else:
                passo = (ora - _fo.t) / FONDO_PASSAGGIO
                if _fo.k < voluto:
                    _fo.k = min(voluto, _fo.k + passo)
                else:
                    _fo.k = max(voluto, _fo.k - passo)
            _fo.t = ora
            if _fo.k > 0:
                trans.blur = FONDO_BLUR * _fo.k
                trans.zoom = 1.0 + 0.02 * _fo.k
            else:
                trans.blur = None
                trans.zoom = 1.0
            # Velo caldo del fuoco (dietro gli sprite: e' lo sfondo).
            slot = getattr(store, "cal_slot", None)
            fuoco = (not mm_movimento_ridotto() and not renpy.is_skipping()
                     and rgl.fuoco_per(_lu_bg(), slot))
            if fuoco:
                a = rgl.velo_fuoco(ora)
                trans.matrixcolor = TintMatrix(Color(rgb=(1.0, 1.0 - a * 0.31, 1.0 - a * 0.6)))
            else:
                trans.matrixcolor = None
            if _fo.k != voluto:
                return 0
            return SPRITE_PASSO if fuoco else 0.1
        return Transform(function=f)

    OMBRA_SCOSTAMENTO = (14, 8)   # px verso destra e verso il basso

    def _lu_ombra(nome):
        # Immagine pre-sfocata da make_gui.py (ombre_sprite), a meta'
        # risoluzione: "gui/ombre/<tag>_<espressione>.webp".
        f = "gui/ombre/%s.webp" % "_".join(nome.split())
        if not renpy.loadable(f):
            return Null()
        return Transform(f, zoom=2.0, xoffset=OMBRA_SCOSTAMENTO[0],
                         yoffset=OMBRA_SCOSTAMENTO[1])

    def _lu_dimensioni():
        """Dimensioni degli sprite scritte da make_gui.py (ombre_sprite)."""
        import json as _lu_json
        try:
            with renpy.open_file("gui/ombre/dimensioni.json") as f:
                return _lu_json.loads(f.read().decode("utf-8"))
        except Exception:
            return {}

    def _lu_definisci_sprite():
        prefisso = "images/"
        dimensioni = _lu_dimensioni()
        for fn in renpy.list_files():
            if not fn.startswith(prefisso):
                continue
            base, ext = _lu_os.path.splitext(_lu_os.path.basename(fn))
            if ext.lower() not in config.image_extensions:
                continue
            nome = base.lower().partition("@")[0]
            parti = nome.split()
            if len(parti) < 2 or parti[0] == "side":
                continue
            if parti[0] == "bg":
                renpy.image(nome, At(fn, fondo_fx()))
            elif nome not in dimensioni:
                # Senza ombra pre-calcolata: come prima, solo la luce.
                renpy.image(nome, At(fn, luce_personaggio(parti[0])))
            else:
                # Ombra della sagoma dietro lo sprite: gli sprite sono mezzi
                # busti tagliati dal bordo, quindi niente ombra a terra; una
                # sagoma scura e sfocata li stacca dallo sfondo. Respira e si
                # muove con lo sprite (sta dentro la stessa luce).
                renpy.image(nome, At(Fixed(
                    _lu_ombra(nome), fn, xysize=tuple(dimensioni[nome])),
                    luce_personaggio(parti[0])))

    _lu_definisci_sprite()
