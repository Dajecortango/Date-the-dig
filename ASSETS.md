# Kit asset — Date the Dig, route di Aede

17 immagini obbligatorie. Sovrascrivi i PNG in `game/images/` con lo STESSO nome file; al riavvio il gioco le usa. Stile consigliato per tutti i prompt: anime/visual novel, illuminazione cinematografica, ambientazione medieval-norrena.

Prompt base stile (da premettere a ogni prompt): 
`anime visual novel style, clean lineart, cinematic lighting, medieval norse fantasy setting`

## Sprite (PNG, sfondo TRASPARENTE, 600×1050 px, figura dalle ginocchia in su, centrata)

Descrizione fissa di Aede da riusare identica in ogni sua espressione:
`young woman, long wavy flame-red hair, grey-green eyes, black dress with red brocade overvest, gold buttons and chains, blue gem necklace`

| File | Espressione nel dettaglio | Prompt (aggiungi dopo la descrizione fissa) |
|---|---|---|
| `aede neutra.webp` | Faccia di guardia, default: viso rilassato ma occhi vigili, sopracciglia dritte, bocca chiusa neutra, mento alto, sguardo che valuta. | `guarded neutral expression, straight brows, closed mouth, chin slightly raised, appraising gaze, arms crossed, knees-up view, transparent background` |
| `aede irritata.webp` | Tsundere: sopracciglia aggrottate, occhi a fessura, broncio marcato, guance gonfie di stizza, testa appena ruotata via. | `annoyed scowl, furrowed brows, narrowed eyes, pronounced tsundere pout, puffed cheeks, head turned slightly away, transparent background` |
| `aede sorpresa.webp` | Occhi spalancati con iridi piccole, sopracciglia alzate, labbra socchiuse, spalle irrigidite di colpo. | `wide eyes with small irises, raised brows, parted lips, stiffened shoulders, caught off guard, transparent background` |
| `aede imbarazzata.webp` | Rossore su guance E orecchie, sguardo deviato in basso a lato, sopracciglia in finta rabbia, mano nei capelli o sulla collana, bocca piccola contratta. | `deep blush on cheeks and ears, looking down and away, flustered angry-but-not-angry brows, hand touching her hair or necklace, small tense mouth, transparent background` |
| `aede sorriso.webp` | Il sorriso raro: morbido, asimmetrico, appena accennato, occhi caldi piegati, niente denti. Deve sembrare rubato. | `rare soft asymmetric smile, barely there, warm crinkled eyes, no teeth, candid stolen expression, transparent background` |
| `aede furia.webp` | Furia fredda: viso di pietra, occhi fissi da predatore, sopracciglia basse, bocca serrata dritta, pugnale sguainato tenuto basso, peso sull'avampiede. | `cold stone-faced fury, unblinking predator stare, low brows, tight straight mouth, drawn dagger held low, forward-leaning stance, transparent background` |
| `glauco neutro.webp` | Cortesia glaciale: postura perfetta, mani dietro la schiena, mezzo sorriso di forma che non arriva agli occhi, sguardo che pesa. | `stern older man, grey hair, immaculate dark noble coat with golden lion brooch, perfect posture, hands behind back, polite half-smile not reaching the cold weighing eyes, transparent background` |
| `glauco minaccioso.webp` | Quasi identico al neutro, ma: testa inclinata avanti di pochi gradi, occhi fissi senza battito, sorriso sparito, ombre più dure. La minaccia è nella differenza minima. | `same stern older man, grey hair, dark noble coat, golden lion brooch, head tilted slightly forward, unblinking icy stare, no smile, harder shadows on face, quiet menace, transparent background` |
| `briseide neutra.webp` | Calore materno + astuzia: sorriso morbido, occhi furbi che sanno già tutto, tazza o mestolo in mano, postura comoda. | `warm matronly woman, 60s, braided grey-auburn hair, gold-trimmed earth-tone robes, soft smile, shrewd knowing eyes, holding a cup, relaxed posture, transparent background` |

Dove compaiono: `neutra` ovunque (default); `irritata` provocazioni/schermaglie; `sorpresa` Svelo, Athlion, ballatoio; `imbarazzata` Calà e ballatoio; `sorriso` fine Athlion, vicolo, good end; `furia` Svelo, magazzino, bad end; `glauco neutro` consegna/cena/good end; `glauco minaccioso` avvertimento, climax, bad end.

Consiglio coerenza: genera prima `aede neutra`, poi usa img2img / reference sulla stessa per le altre 5 espressioni (stessa posa, cambia solo il volto).

## Sfondi (PNG 1920×1080, nessun personaggio)

| File | Prompt |
|---|---|
| `bg sala_svelo.webp` | `grand masquerade hall in a stone fortress at night, hanging lanterns, tapestries with golden lion heraldry, warm candlelight, no people` |
| `bg arena_athlion.webp` | `medieval athletic arena, packed wooden stands, banners of nine clans, trampled snow and sand field, overcast northern sky, no people` |
| `bg vicoli_zefiro.webp` | `narrow medieval alley at dusk, stone houses, hundreds of paper lanterns, "city of lanterns", light snow, no people` |
| `bg cala_notte.webp` | `monumental stone staircase of 300 steps descending to a river at night, a lantern on every step, golden glow, snowy rooftops, no people` |
| `bg studio_glauco.webp` | `austere private study, dark wood, perfectly ordered desk, weapon racks, single candle, cold atmosphere, no people` |
| `bg corridoio_ceppo.webp` | `warm interior of a lived-in medieval manor, wooden beams, hearth light, cloaks on hooks, homely clutter, no people` |
| `bg esterno_neve.webp` | `outside tall city walls at night, heavy falling snow, flat snowfield, distant torchlight on the ramparts, moonlight, no people` |
| `bg nero.webp` | nero pieno — quello attuale va già bene, non serve rigenerarlo |

## Facoltativi (il gioco funziona senza)

- `game/gui/main_menu.png` 1920×1080 — se vuoi un menu illustrato: in `game/gui.rpy` rimetti `define gui.main_menu_background = "gui/main_menu.png"`. Prompt: paesaggio del Nord con leone dorato in cielo.
- Audio in `game/audio/` (ogg/opus): 1 tema menu, 1 tema quotidiano, 1 tema Aede/romantico, 1 tema tensione/Glauco, 1 tema finale. Vanno poi agganciati con `play music` negli script (chiedimelo e lo faccio).

## Checklist dopo la sostituzione

1. Nomi file identici, estensione `.png` (se usi `.jpg` cancella il `.png` omonimo o Ren'Py vede l'immagine doppia).
2. `powershell -File lint.ps1` → nessun problema.
3. Rilancia il gioco.
