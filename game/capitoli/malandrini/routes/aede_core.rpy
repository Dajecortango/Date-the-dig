# Route Aede — "Tempesta d'amore". Personaggi, variabili, utilità.
# Aede: figlia di Glauco, sorella di Ofelia e Ascadeo. Difficoltà 3/5.
# Niente poliamore: la scelta del cuore chiude le altre route.

## Personaggi #################################################################

define aede = Character("Aede", color="#c0392b", image="aede")
define glauco = Character("Glauco Severo", color="#6b6b6b", image="glauco")
define briseide = Character("Briseide Ippodamia", color="#b8860b", image="briseide")
define pc = Character("[player_name]", color="#f0e6d2")

# Fratelli di Ceppo del protagonista (Ceppo di Briseide Ippodamia).
define vanna = Character("Vanna", color="#8fbc8f", image="vanna")
define corrado = Character("Corrado", color="#87a7c7", image="corrado")

## Variabili di route #########################################################

default aede_affinity = 0
default flag_segreto_svelo = False
default flag_accetta_lavoro = False
default flag_giuramento = False
default flag_aede_rivelato = False
# La mano sulla Calà (cap5: "presa" | "rifiutata" | "accanto" | "indietro";
# None se cap5 non c'e' stato) e il gesto del climax ("parla" | "silenzio" |
# "mano"): li ricordano climax e finali.
default aede_mano_cala = None
default aede_climax_gesto = None
# La sera in palestra di Luna VI: "resta" | "chiede" | "lascia".
default aede_luna6_esito = None
