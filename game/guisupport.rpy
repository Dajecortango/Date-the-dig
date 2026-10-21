# Supporto GUI. Il template SDK rigenerava qui le immagini di game/gui/ a
# ogni avvio (gui7.generate_gui), sovrascrivendo quelle custom: rimosso.
# Le immagini della GUI sono generate UNA volta da make_gui.py.

init -100 python in gui:

    def scale(n):
        return int(n)
