"""Registro puro dei capitoli: nessun import di renpy.

Ogni capitolo si registra a init con `registra(...)`. Il registro vive a
livello di modulo e NON va mai salvato: nello store restano solo gli id
(stringhe) dei capitoli.
"""

_CAMPI = (
    "id", "numero", "titolo", "sottotitolo", "ingresso", "copertina",
    "funzioni", "finali", "gruppi_finali", "cast_menu", "affinita", "regia",
    "ambienti", "ambiente_pioggia", "ambiente_arrivo", "entrate", "ritratto",
    "dopo_caricamento", "schede",
)


class Capitolo(object):
    __slots__ = _CAMPI

    def __init__(self, id, numero=0, titolo="", sottotitolo="", ingresso="",
                 copertina=None, funzioni=None, finali=None,
                 gruppi_finali=None, cast_menu=None, affinita=None,
                 regia=None, ambienti=None, ambiente_pioggia=None,
                 ambiente_arrivo=None, entrate=None, ritratto=None,
                 dopo_caricamento=None, schede=None):
        self.id = id
        self.numero = numero
        self.titolo = titolo
        self.sottotitolo = sottotitolo
        self.ingresso = ingresso
        self.copertina = copertina
        self.funzioni = frozenset(funzioni or ())
        self.finali = list(finali or [])
        self.gruppi_finali = list(gruppi_finali or [])
        self.cast_menu = cast_menu
        self.affinita = list(affinita or [])
        self.regia = regia
        self.ambienti = dict(ambienti or {})
        self.ambiente_pioggia = dict(ambiente_pioggia or {})
        self.ambiente_arrivo = dict(ambiente_arrivo or {})
        self.entrate = dict(entrate or {})
        self.ritratto = ritratto
        self.dopo_caricamento = list(dopo_caricamento or [])
        self.schede = dict(schede or {})


_REGISTRO = {}


def registra(**campi):
    cid = campi.get("id")
    if not cid:
        raise ValueError("capitolo senza id")
    if cid in _REGISTRO:
        raise ValueError("capitolo gia' registrato: %r" % (cid,))
    usati = set()
    for c in _REGISTRO.values():
        usati.update(f[0] for f in c.finali)
    for f in campi.get("finali") or []:
        if f[0] in usati:
            raise ValueError("finale gia' usato: %r" % (f[0],))
        usati.add(f[0])
    schede = campi.get("schede") or {}
    for voce in campi.get("cast_menu") or []:
        if voce[0] not in schede:
            raise ValueError("cast_menu: %r senza scheda in schede" % (voce[0],))
    cap = Capitolo(**campi)
    _REGISTRO[cid] = cap
    return cap


def elenco():
    return sorted(_REGISTRO.values(), key=lambda c: c.numero)


def ottieni(cid):
    return _REGISTRO.get(cid)


def ha(cid, funzione):
    c = _REGISTRO.get(cid)
    return c is not None and funzione in c.funzioni


def capitolo_menu(ultimo):
    c = ottieni(ultimo)
    if c is not None:
        return c
    tutti = elenco()
    return tutti[0] if tutti else None


def capitolo_di_finale(fid):
    for c in elenco():
        for f in c.finali:
            if f[0] == fid:
                return c
    return None


def finali_contati(cid, visti):
    c = ottieni(cid)
    if c is None:
        return (0, 0)
    ids = [f[0] for f in c.finali]
    return (sum(1 for i in ids if i in visti), len(ids))


def leggi_variabile(radice, nome):
    """Valore di una variabile di store; il punto entra negli store con nome
    ("zzprova.affinita" = store `zzprova`, variabile `affinita`). None se manca."""
    obj = radice
    for parte in nome.split("."):
        obj = getattr(obj, parte, None)
        if obj is None:
            return None
    return obj


def svuota():
    _REGISTRO.clear()
