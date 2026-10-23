# Galleria dei finali: registro persistente (sopravvive tra le partite).

default persistent.finali_visti = set()
# Ultimo finale raggiunto: il menu principale ne prende fondo e personaggio
# (menu_cast.rpy).
default persistent.ultimo_finale = None

init python:

    def sblocca_finale(fid):
        if persistent.finali_visti is None:
            persistent.finali_visti = set()
        persistent.finali_visti.add(fid)
        persistent.ultimo_finale = fid
        renpy.save_persistent()

screen galleria_finali():

    tag menu

    use game_menu(_("Finali"), scroll="viewport"):

        vbox:
            spacing 10
            xfill True

            $ visti = persistent.finali_visti or set()
            $ con_finali = [c for c in rcap.elenco() if c.finali]
            $ n_visti = sum(rcap.finali_contati(c.id, visti)[0] for c in con_finali)
            $ n_tot = sum(rcap.finali_contati(c.id, visti)[1] for c in con_finali)

            text "Finali scoperti: [n_visti] / [n_tot]" size 32 color gui.accent_color

            for c in con_finali:

                $ c_visti, c_tot = rcap.finali_contati(c.id, visti)

                null height 16
                text "[c.titolo]  ([c_visti] / [c_tot])" size 30 color gui.accent_color

                for gruppo in c.gruppi_finali:

                    null height 12
                    text gruppo size 28 color "#f5e3b8"

                    for fid, titolo, route, indizio in c.finali:
                        if route == gruppo:
                            if fid in visti:
                                text titolo size 24 color "#e0b75a"
                            else:
                                vbox:
                                    text "???" size 24 color "#8a8578"
                                    text indizio size TESTO_NOTA color "#8a8578" italic True
