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

    # (sfondo, effetto, quando): quando = None (sempre), "sera" (solo nello
    # slot di sera) o "pioggia" (fuori dalla sera, nei giorni di pioggia).
    # Vale la prima riga che corrisponde.
    EFFETTI_SFONDI = (
        ("bg esterno_neve", "neve", None),
        ("bg cala_notte", "lanterne", None),
        ("bg vicoli_zefiro", "fumo", "sera"),
        ("bg vicoli_zefiro", "pioggia", "pioggia"),
        ("bg sala_svelo", "polvere", None),
        ("bg studio_glauco", "braci", None),
        ("bg corridoio_ceppo", "braci", None),
        ("bg arena_athlion", "nevischio", None),
    )

    def piove_ora():
        if getattr(store, "cal_slot", None) == "sera":
            return False
        return rgl.piove(getattr(store, "cal_luna", 1), getattr(store, "cal_giorno", 1))

    def effetto_corrente():
        if store.main_menu or store._in_replay or mm_movimento_ridotto():
            return None
        for bg, fx, quando in EFFETTI_SFONDI:
            if not renpy.showing(bg):
                continue
            if quando == "sera" and getattr(store, "cal_slot", None) != "sera":
                continue
            if quando == "pioggia" and not piove_ora():
                continue
            return fx
        return None

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

    FX_FABBRICHE = {"neve": _fx_neve, "lanterne": _fx_lanterne,
                    "fumo": _fx_fumo, "polvere": _fx_polvere,
                    "braci": _fx_braci, "nevischio": _fx_nevischio,
                    "pioggia": _fx_pioggia}

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
            renpy.redraw(self, 0)
            return rv

        def visit(self):
            return [self.child]

    class _FxCache(NoRollback):
        def __init__(self):
            self.fx = None
            self.d = None

    _fx_cache = _FxCache()

    def effetto_displayable(fx):
        if fx is None:
            _fx_cache.fx = _fx_cache.d = None
            return Null()
        if fx != _fx_cache.fx or _fx_cache.d is None:
            _fx_cache.fx = fx
            _fx_cache.d = FxOrologio(FX_FABBRICHE[fx]())
        return _fx_cache.d


screen effetti_scena():
    layer "effetti"
    zorder 0

    add effetto_displayable(effetto_corrente())
