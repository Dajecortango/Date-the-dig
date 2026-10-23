## Opzioni di configurazione del gioco.

define config.name = _("Date the Dignitas")
define gui.show_name = True
define config.version = "0.1"
define gui.about = _p("""
Visual novel ambientata nel mondo di Yr.
Lore: "Il Nord - La Guida" e "La Famiglia Dignitas - La Guida".
""")

define build.name = "DateTheDig"

## Audio #######################################################################

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

## Transizioni #################################################################

## Menu di gioco (salva, carica, memorie): l'azione più frequente, va
## percepita come immediata.
define config.enter_transition = Dissolve(0.2)
define config.exit_transition = Dissolve(0.15)
## after_load / end_game / intra: in regia.rpy (usano lo stacco a tema).

## Varie #######################################################################

define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

default preferences.text_cps = 40
default preferences.afm_time = 15

## Salvataggi ##################################################################

define config.save_directory = "DateTheDig-1760000000"

## Icona #######################################################################

define config.window_icon = "gui/window_icon.png"

## Lingua predefinita (voci di interfaccia tematiche in game/tl/italian/).
define config.language = "italian"

## Build #######################################################################

init python:
    build.classify('tools/**', None)
    build.classify('docs/**', None)
    build.classify('tests/**', None)
    build.classify('*.ps1', None)
    build.classify('*.py', None)
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
