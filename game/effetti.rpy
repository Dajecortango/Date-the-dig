# Effetti di scena: particelle leggere scelte in base allo sfondo mostrato.
#   neve           -> bg esterno_neve
#   lanterne       -> bg cala_notte (salgono)
#   fumo leggero   -> bg vicoli_zefiro, solo nello slot di sera
#   polvere dorata -> bg sala_svelo
#   braci          -> bg studio_glauco, bg corridoio_ceppo (salgono)
#   nevischio      -> bg arena_athlion (di traverso, col vento: l'arena e'
#                     innevata)
#   pioggia        -> bg vicoli_zefiro, fuori dalla sera, nei giorni di
#                     pioggia (regia_logic.piove: uguali in ogni partita)
# Overlay (config.overlay_screens) su un layer proprio sopra "master": le
# particelle stanno sopra fondali e sprite ma sotto box, scelte e menu, e
# lo "scene" non le cancella. Costo: un SnowBlossom per effetto (poche
# decine di sprite), la screen si rivaluta solo a ogni interazione.
# Con "Animazioni: No" (mm_movimento_ridotto) niente particelle.
# Le immagini delle particelle vengono da make_gui.py (particelle_effetti).

init python:
    import regia_logic as rgl
    renpy.add_layer("effetti", above="master")
    config.overlay_screens.append("effetti_scena")

    # Regole (sfondo, contesto del calendario, pioggia, tempesta) in
    # regia_logic.effetti_per; le tabelle (EFFETTI_SFONDI, EFFETTI_ASCIUTTO,
    # EFFETTI_CONTESTO) sono del capitolo: capitolo_regia().

    def piove_ora():
        if getattr(store, "cal_slot", None) == "sera":
            return False
        return rgl.piove(getattr(store, "cal_luna", 1), getattr(store, "cal_giorno", 1))

    def effetto_corrente():
        """Tupla degli effetti da mostrare (vuota = niente)."""
        if (store.main_menu or store._in_replay or mm_movimento_ridotto()
                or renpy.is_skipping()):
            return ()
        attr = renpy.get_attributes("bg", layer="master") or ()
        bg = attr[0] if attr else None
        return rgl.effetti_per(bg, getattr(store, "cal_slot", None),
                               getattr(store, "cal_contesto", None), piove_ora(),
                               getattr(store, "regia_tempesta", False),
                               capitolo_regia())

    # Le particelle si costruiscono fresche a ogni cambio d'effetto, avvolte
    # in un orologio proprio (FxOrologio): SnowBlossom sparge le particelle
    # su tutto lo schermo solo al tempo 0, e una screen gia' mostrata non
    # ripartirebbe da 0 (le lanterne arriverebbero col contagocce dal fondo).
    # Tra un'interazione e l'altra l'istanza resta la stessa (_fx_cache,
    # fuori dallo store: niente salvataggi, niente rollback).

    def _fx_neve():
        return Fixed(
            SnowBlossom("gui/fiocco.png", count=30, border=40, xspeed=(15, 50),
                        yspeed=(55, 110), start=10, fast=True),
            SnowBlossom(Transform("gui/fiocco.png", zoom=0.55, alpha=0.7), count=36,
                        border=40, xspeed=(10, 35), yspeed=(30, 60), start=10, fast=True))

    def _fx_lanterne():
        return Fixed(
            SnowBlossom(Transform("gui/fx_lanterna.png", alpha=0.9), count=9, border=70,
                        xspeed=(-12, 14), yspeed=(-48, -30), start=12, fast=True),
            SnowBlossom(Transform("gui/fx_lanterna.png", zoom=0.55, alpha=0.6), count=14,
                        border=50, xspeed=(-8, 10), yspeed=(-30, -18), start=12, fast=True))

    def _fx_fumo():
        return SnowBlossom(Transform("gui/fx_fumo.png", zoom=1.6, alpha=0.32),
                           count=7, border=220, xspeed=(8, 26), yspeed=(-22, -10),
                           start=15, fast=True)

    def _fx_polvere():
        return Fixed(
            SnowBlossom(Transform("gui/fx_polvere.png", alpha=0.75), count=18, border=30,
                        xspeed=(-14, 14), yspeed=(10, 26), start=10, fast=True),
            SnowBlossom(Transform("gui/fx_polvere.png", zoom=0.55, alpha=0.5), count=22,
                        border=30, xspeed=(-10, 10), yspeed=(6, 16), start=10, fast=True))

    def _fx_braci():
        return Fixed(
            SnowBlossom("gui/fx_brace.png", count=8, border=30,
                        xspeed=(-16, 16), yspeed=(-60, -30), start=10, fast=True),
            SnowBlossom(Transform("gui/fx_brace.png", zoom=0.6, alpha=0.7), count=6,
                        border=30, xspeed=(-10, 10), yspeed=(-40, -20), start=10, fast=True))

    def _fx_nevischio():
        # horizontal=True scambia gli assi: yspeed e' la spinta del vento.
        return SnowBlossom(Transform("gui/fiocco.png", zoom=0.6, alpha=0.8), count=30,
                           border=40, xspeed=(10, 40), yspeed=(180, 300),
                           horizontal=True, start=6, fast=True)

    def _fx_pioggia():
        n = 20 if renpy.variant("small") else 40
        return SnowBlossom(Transform("gui/fx_goccia.png", rotate=12, alpha=0.95), count=n,
                           border=60, xspeed=(-140, -110), yspeed=(700, 900),
                           start=2, fast=True)

    def _fx_n(n):
        # Telefono: meta' particelle.
        return max(1, n // 2) if renpy.variant("small") else n

    def _fx_neve_fitta():
        return Fixed(
            SnowBlossom("gui/fiocco.png", count=_fx_n(60), border=40, xspeed=(30, 90),
                        yspeed=(110, 200), start=6, fast=True),
            SnowBlossom(Transform("gui/fiocco.png", zoom=0.55, alpha=0.7), count=_fx_n(70),
                        border=40, xspeed=(20, 70), yspeed=(70, 130), start=6, fast=True),
            Solid("#ffffff0a"))

    def _fx_foglie():
        return Fixed(
            SnowBlossom(Transform("gui/fx_foglia.png", alpha=0.9), count=_fx_n(10), border=40,
                        xspeed=(-20, 30), yspeed=(25, 45), start=10, fast=True),
            SnowBlossom(Transform("gui/fx_foglia.png", zoom=0.6, alpha=0.6,
                                  matrixcolor=TintMatrix("#f2b8c6")),
                        count=_fx_n(10), border=40, xspeed=(-15, 20), yspeed=(15, 30),
                        start=10, fast=True))

    def _fx_fumo_pipa():
        return SnowBlossom(Transform("gui/fx_fumo.png", zoom=1.9, alpha=0.4),
                           count=_fx_n(12), border=240, xspeed=(4, 18), yspeed=(-14, -6),
                           start=15, fast=True)

    def _fx_scintille():
        return SnowBlossom("gui/fx_scintilla.png", count=_fx_n(10), border=20,
                           xspeed=(-40, 40), yspeed=(-180, -90), start=4, fast=True)

    def _fx_luccichii():
        # Riflessi sui canali ghiacciati: punti di luce lenti nel quarto basso.
        return Fixed(
            SnowBlossom(Transform("gui/fx_luccichio.png", alpha=0.7), count=_fx_n(14),
                        border=30, xspeed=(-6, 6), yspeed=(18, 40), horizontal=True,
                        start=4, fast=True),
            ysize=270, yalign=1.0)

    FX_FABBRICHE = {"neve": _fx_neve, "lanterne": _fx_lanterne,
                    "fumo": _fx_fumo, "polvere": _fx_polvere,
                    "braci": _fx_braci, "nevischio": _fx_nevischio,
                    "pioggia": _fx_pioggia, "neve_fitta": _fx_neve_fitta,
                    "foglie": _fx_foglie, "fumo_pipa": _fx_fumo_pipa,
                    "scintille": _fx_scintille, "luccichii": _fx_luccichii}

    FX_PASSO = 1.0 / 30 if renpy.variant("small") else 0

    class FxOrologio(renpy.Displayable):
        """Rende il figlio con un tempo che parte da 0 al primo render."""
        def __init__(self, child, **kwargs):
            super(FxOrologio, self).__init__(**kwargs)
            self.child = child
            self.st0 = None

        def render(self, width, height, st, at):
            if self.st0 is None or st < self.st0:
                self.st0 = st
            t = st - self.st0
            cr = renpy.render(self.child, width, height, t, t)
            rv = renpy.Render(width, height)
            rv.blit(cr, (0, 0))
            # Su telefono le particelle a 30 fps: a fps pieni annullavano il
            # risparmio di SPRITE_PASSO (luce.rpy).
            renpy.redraw(self, FX_PASSO)
            return rv

        def visit(self):
            return [self.child]

    class _FxCache(NoRollback):
        def __init__(self):
            self.fx = None
            self.d = None

    _fx_cache = _FxCache()

    def effetto_displayable(fx):
        """fx: tupla di effetti, disegnati nell'ordine."""
        if not fx:
            _fx_cache.fx = _fx_cache.d = None
            return Null()
        if fx != _fx_cache.fx or _fx_cache.d is None:
            _fx_cache.fx = fx
            _fx_cache.d = FxOrologio(Fixed(*[FX_FABBRICHE[f]() for f in fx]))
        return _fx_cache.d


screen effetti_scena():
    layer "effetti"
    zorder 0

    add effetto_displayable(effetto_corrente())
