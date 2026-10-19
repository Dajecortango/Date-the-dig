# Kit asset — Date the Dig, route di Aede

17 immagini obbligatorie. Sovrascrivi i PNG in `game/images/` con lo STESSO nome file; al riavvio il gioco le usa. Stile consigliato per tutti i prompt: anime/visual novel, illuminazione cinematografica, ambientazione medieval-norrena.

Prompt base stile (da premettere a ogni prompt): 
`anime visual novel style, clean lineart, cinematic lighting, medieval norse fantasy setting`

## Sprite (PNG, sfondo TRASPARENTE, 600×1050 px, figura dalle ginocchia in su, centrata)

Descrizione fissa di Aede da riusare identica in ogni sua espressione:
`young woman, long wavy flame-red hair, grey-green eyes, black dress with red brocade overvest, gold buttons and chains, blue gem necklace`

| File | Prompt (aggiungi dopo la descrizione fissa) |
|---|---|
| `aede neutra.png` | `guarded neutral expression, arms crossed, knees-up view, transparent background` |
| `aede irritata.png` | `annoyed scowl, narrowed eyes, tsundere pout, transparent background` |
| `aede sorpresa.png` | `wide eyes, parted lips, caught off guard, transparent background` |
| `aede imbarazzata.png` | `blushing, looking away, flustered, hand near face, transparent background` |
| `aede sorriso.png` | `rare genuine soft smile, warm eyes, transparent background` |
| `aede furia.png` | `cold fury, drawn dagger in hand, predatory stance, transparent background` |
| `glauco neutro.png` | `stern older man, grey hair, immaculate dark noble coat with golden lion brooch, unreadable polite expression, transparent background` |
| `glauco minaccioso.png` | `same stern older man, grey hair, dark noble coat, golden lion brooch, icy menacing stare, slight forward lean, transparent background` |
| `briseide neutra.png` | `warm matronly woman, 60s, braided grey-auburn hair, gold-trimmed earth-tone robes, kind but shrewd eyes, transparent background` |

Consiglio coerenza: genera prima `aede neutra`, poi usa img2img / reference sulla stessa per le altre 5 espressioni (stessa posa, cambia solo il volto).

## Sfondi (PNG 1920×1080, nessun personaggio)

| File | Prompt |
|---|---|
| `bg sala_svelo.png` | `grand masquerade hall in a stone fortress at night, hanging lanterns, tapestries with golden lion heraldry, warm candlelight, no people` |
| `bg arena_athlion.png` | `medieval athletic arena, packed wooden stands, banners of nine clans, trampled snow and sand field, overcast northern sky, no people` |
| `bg vicoli_zefiro.png` | `narrow medieval alley at dusk, stone houses, hundreds of paper lanterns, "city of lanterns", light snow, no people` |
| `bg cala_notte.png` | `monumental stone staircase of 300 steps descending to a river at night, a lantern on every step, golden glow, snowy rooftops, no people` |
| `bg studio_glauco.png` | `austere private study, dark wood, perfectly ordered desk, weapon racks, single candle, cold atmosphere, no people` |
| `bg corridoio_ceppo.png` | `warm interior of a lived-in medieval manor, wooden beams, hearth light, cloaks on hooks, homely clutter, no people` |
| `bg esterno_neve.png` | `outside tall city walls at night, heavy falling snow, flat snowfield, distant torchlight on the ramparts, moonlight, no people` |
| `bg nero.png` | nero pieno — quello attuale va già bene, non serve rigenerarlo |

## Facoltativi (il gioco funziona senza)

- `game/gui/main_menu.png` 1920×1080 — se vuoi un menu illustrato: in `game/gui.rpy` rimetti `define gui.main_menu_background = "gui/main_menu.png"`. Prompt: paesaggio del Nord con leone dorato in cielo.
- Audio in `game/audio/` (ogg/opus): 1 tema menu, 1 tema quotidiano, 1 tema Aede/romantico, 1 tema tensione/Glauco, 1 tema finale. Vanno poi agganciati con `play music` negli script (chiedimelo e lo faccio).

## Checklist dopo la sostituzione

1. Nomi file identici, estensione `.png` (se usi `.jpg` cancella il `.png` omonimo o Ren'Py vede l'immagine doppia).
2. `powershell -File lint.ps1` → nessun problema.
3. Rilancia il gioco.
