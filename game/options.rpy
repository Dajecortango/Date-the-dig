## Opzioni di configurazione del gioco.

define config.name = _("Date the Dig")
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

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

## Varie #######################################################################

define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

default preferences.text_cps = 40
default preferences.afm_time = 15

## Salvataggi ##################################################################

define config.save_directory = "DateTheDig-1760000000"

## Icona #######################################################################

# define config.window_icon = "gui/window_icon.png"

## Build #######################################################################

init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
