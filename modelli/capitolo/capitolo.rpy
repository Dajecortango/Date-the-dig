# Registrazione del capitolo __NUMERO__, "__TITOLO__". Gli altri campi del
# registro (cast_menu, affinita, regia, ambienti, schede...) restano vuoti
# finche' non servono: vedi LEGGIMI.md.

init 10 python:
    rcap.registra(
        id="__ID__",
        numero=__NUMERO__,
        titolo="__TITOLO__",
        ingresso="__ID___inizio",
        # Galleria dei finali (finali.rpy).
        finali=__ID___FINALI,
        gruppi_finali=["__TITOLO__"],
    )
