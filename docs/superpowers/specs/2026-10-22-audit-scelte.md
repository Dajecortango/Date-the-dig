# Audit delle scelte (punto 12) — da approvare

Data: 2026-10-22. Criterio (spec `2026-10-22-route-finali-origliati-design.md`
§12): un'opzione si riscrive solo se, letta sullo schermo con la sua
didascalia, non dice cosa stai decidendo. Le battute tra «» non si toccano.

Metodo: estratte tutte le opzioni del gioco (126 menu); 59 sono brevi
(meno di 34 caratteri) e senza «». Quasi tutte sono chiare grazie alla
didascalia che sta sopra (es. "Il ragazzino sta già girando l'angolo." →
"Inseguirlo"). Restano queste.

## Consigliate (scelte che pesano, testo opaco)

| # | File:riga | Ora | Contesto | Proposta |
|---|---|---|---|---|
| 1 | `routes/druso_eventi.rpy:83` | Restituirlo chiuso | Impegno con Druso: ti porge il foglio col poema. È la scelta del cuore: chiude la route. | Restituirgli il foglio senza leggerlo |
| 2 | `routes/icaro_eventi.rpy:129` | Prenderla | Impegno Bro: Icaro ti offre la chiave del magazzino. | Prendere la chiave del magazzino |
| 3 | `routes/icaro_eventi.rpy:136` | Rifiutarla | Come sopra; rifiutare chiude la route. | Lasciargli la chiave |
| 4 | `economia_extra.rpy:390` | Aspettare ancora | Debito con Icaro: saldare ora o rimandare. | Rimandare il saldo dei sei Scudi |

## Facoltative (già chiare con la didascalia, guadagno piccolo)

| # | File:riga | Ora | Contesto | Proposta |
|---|---|---|---|---|
| 5 | `economia.rpy:291` | Tirare dritto | Truffa sulla moneta tosata, al mercato. | Tirare dritto: non sono affari miei |
| 6 | `economia.rpy:304` | Scansarmi | Barile che rotola dai carrettieri. | Scansarmi e lasciarlo rotolare |
| 7 | `economia_extra.rpy:296` | Passare oltre | Cassa degli orfani ai riti. | Passare oltre la cassa |

Non toccate (motivo): "Darglielo" / "Tenerlo per un'altra occasione"
(la didascalia nomina il dono e la persona), "Un uomo" / "Una donna"
(scelta del genere, chiara), le varianti `if` in coppia (es. "Prenderle la
mano"), i menu di climax e finali.

Effetto sullo storico: i testi vecchi passano ai nuovi con
`OPZIONI_RINOMINATE` (conseguenze_logic.py), anche nei salvataggi e nel
persistent, quindi l'albero della Trama non perde le scelte già fatte.
