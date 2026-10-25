---
name: lore-continuity
description: Use when writing or editing scenes that name people, places, history, religion or institutions, when inventing a new proper noun, or when unsure whether a detail contradicts established canon of Date the Dignitas.
---

# Continuità del lore

## Dove vive il canone
- **`docs/lore.md`** — bibbia unica: mondo, Zefiro, Famiglia Dignitas, religione, feste, personaggi. Convenzione: **[canone]** = fissato da spec/manuali del committente; **[scena]** = inventato nelle scene; **INCOERENZA** = conflitto noto, raccolto nella sezione finale.
- Precedenza nei conflitti: committente > spec > manuali ("Il Nord - La Guida", "La Famiglia Dignitas - La Guida").
- Profili personaggio: `docs/profili/{aede,druso,icaro,ofelia}.md`. **`caino.md` non esiste**: il canone di Caino sta in lore.md e nella spec — non inventare un profilo, cerca lì.
- Grafie blindate: lista `SBAGLIATE` in `tests/test_lore.py` (regex delle grafie sbagliate → FAIL).

## Flusso: prima di scrivere la scena
1. Nome proprio nella scena? Cerca la grafia esatta in `docs/lore.md` (es. "la Calà" non "Cala", "Yr-Drazul" non "Drazul", "TESCHIO!" maiuscolo).
2. Fatto storico/relazione (chi è figlio di chi, chi sa cosa)? Verifica in lore.md; in dubbio tra due versioni, vince la precedenza sopra.
3. Chiusura: `py -3 -I -X utf8 tests/test_lore.py`.

## Flusso: nome nuovo inventato
Nello stesso turno in cui il nome entra in un .rpy:
1. Voce in `docs/lore.md` nella sezione giusta, marcata **[scena]**.
2. Regex delle storpiature probabili in `SBAGLIATE` (`tests/test_lore.py`) — accenti, doppie, divisioni in due parole (modello: le voci esistenti).
3. Lancia il test.

## Contraddizione trovata
Non correggerla in silenzio e non ignorarla: marcala **INCOERENZA** in lore.md (sezione finale) e segnalala all'utente — la scelta su quale versione vince è sua, salvo precedenza già chiara.

## Errori comuni
- Nome nuovo nel .rpy senza voce in lore.md: alla scena dopo qualcuno lo storpia e nessun test se ne accorge.
- Aggiornare la grafia in lore.md ma non la regex (o viceversa): il canone e il test devono cambiare insieme.
- Dare per canone un dettaglio [scena]: controlla il marcatore prima di costruirci sopra trama.
