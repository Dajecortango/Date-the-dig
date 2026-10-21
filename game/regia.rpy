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
