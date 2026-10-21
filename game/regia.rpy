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
