"""Simulatore esaustivo del semestre dei Malandrini (per i test).

Tutto e' ricavato dai sorgenti, niente tabelle di punti a mano:
- calendario (CAL_GIORNI), registry EVENTI e ATTIVITA (con le scene dei
  minigiochi inserite da pool_aggiungi), catalogo dei doni e mercato sono
  letti dai .rpy (blocchi Python estratti ed eseguiti con stub minimi);
- i punti di ogni evento / scena di territorio / dono vengono da un
  analizzatore di percorsi sui label Ren'Py: segue menu, if/elif/else
  (le condizioni valutabili sullo stato vengono valutate, le altre aprono
  entrambi i rami), call/jump verso altri label, fall-through tra label,
  `$ x += n`, `+= mgl.delta(...)`, `congelate.add(...)`, eco_spendi,
  druso_passo_falso, rivali_sposta;
- soglie e scelta del cuore da routing_logic (rl.cuore_candidati, quindi
  anche rl.CUORE_REQUISITI).

Ricerca: DFS con memoizzazione su tutti i momenti del calendario (fissi,
inviti con le cond vere, luna_min/slot, catene, inviti a scadenza di Ofelia
con gelo, scene di territorio una-tantum, mercato e doni, filtro degli
inviti a route attiva, gelosia di Icaro). Lo spazio delle scelte e' ridotto
ai personaggi bersaglio (piu' "passa": un'attivita' a 0 punti).

Approssimazioni (ottimistiche, documentate): i flag scritti in un evento non
passano agli eventi successivi (le loro condizioni aprono entrambi i rami),
tranne flag_accetta_lavoro/flag_giuramento nelle cond di EVENTI (True);
rea_noti() = True; non modellati il debito con Icaro, i casi casuali in
citta' e gli echi (nessuno sposta affinita' dei bersagli tranne il debito).

Uso: import sim_semestre as ss; ss.run(...). Da riga di comando stampa un
riepilogo: py -3 -I -X utf8 tests/sim_semestre.py
"""
import ast
import functools
import glob
import os
import re
import sys
import textwrap

sys.setrecursionlimit(20000)
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from percorsi import MAL, prepara_import  # noqa: E402
prepara_import()

import calendario_logic as cl  # noqa: E402
import conseguenze_logic as csl  # noqa: E402
import minigiochi_logic as mgl  # noqa: E402
import relazioni_logic as rlz  # noqa: E402
import routing_logic as rl  # noqa: E402

CHARS = list(rl.CUORE_VAR)
VAR = rl.CUORE_VAR
# Variabili numeriche seguite dall'analizzatore (delta per percorso).
TRACK = [VAR[c] for c in CHARS] + ["scudi", "caino_trappole", "aede_sospetto",
                                   "druso_passi_falsi"]
TI = {n: i for i, n in enumerate(TRACK)}
NT = len(TRACK)
ZERO = (0,) * NT
I_SCUDI, I_TRAP, I_SOSP = TI["scudi"], TI["caino_trappole"], TI["aede_sospetto"]
I_PASSI = TI["druso_passi_falsi"]

# Anomalie dell'analisi (il test fallisce se non vuota): costrutti che
# toccano variabili seguite ma non sono stati capiti, label mancanti, ecc.
ANOMALIE = []


def _anomalia(msg):
    if msg not in ANOMALIE:
        ANOMALIE.append(msg)


# Lettura dei sorgenti #######################################################

def _togli_commento(riga):
    q = None
    i = 0
    while i < len(riga):
        ch = riga[i]
        if q:
            if ch == "\\":
                i += 2
                continue
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#":
            return riga[:i]
        i += 1
    return riga


def _profondita(riga):
    q = None
    d = 0
    i = 0
    while i < len(riga):
        ch = riga[i]
        if q:
            if ch == "\\":
                i += 2
                continue
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch in "([{":
            d += 1
        elif ch in ")]}":
            d -= 1
        i += 1
    return d


def _righe_logiche(testo):
    # Docstring a triplo apice: svuotate (gli apostrofi confonderebbero).
    testo = re.sub(r'"""[\s\S]*?"""',
                   lambda m: '""' + "\n" * m.group(0).count("\n"), testo)
    out = []
    righe = testo.split("\n")
    i = 0
    while i < len(righe):
        r = _togli_commento(righe[i]).rstrip()
        i += 1
        if not r.strip():
            continue
        ind = len(r) - len(r.lstrip())
        d = _profondita(r)
        while d > 0 and i < len(righe):
            s = _togli_commento(righe[i]).rstrip()
            i += 1
            r += " " + s.strip()
            d += _profondita(s)
        out.append((ind, r.strip()))
    return out


def _blocco(items, i, ind):
    nodi = []
    while i < len(items) and items[i][0] >= ind:
        if items[i][0] > ind:
            i += 1
            continue
        txt = items[i][1]
        i += 1
        figli = []
        if txt.endswith(":") and i < len(items) and items[i][0] > ind:
            figli, i = _blocco(items, i, items[i][0])
        nodi.append((txt, figli))
    return nodi, i


FILES = sorted(glob.glob(os.path.join(MAL, "**", "*.rpy"), recursive=True))
TESTI = {f: open(f, encoding="utf-8").read() for f in FILES}

# name -> (params [(nome, default_src)], nodi, label seguente nello stesso file)
LABELS = {}
LABEL_TESTO = {}


def _carica_label():
    for f in FILES:
        items = _righe_logiche(TESTI[f])
        tops = [k for k, (ind, _t) in enumerate(items) if ind == 0]
        nomi = []
        for pos, k in enumerate(tops):
            txt = items[k][1]
            m = re.match(r"label\s+(\w+)\s*(\((.*)\))?\s*:$", txt)
            if not m:
                nomi.append(None)
                continue
            fine = tops[pos + 1] if pos + 1 < len(tops) else len(items)
            sub = items[k + 1:fine]
            nodi = _blocco(sub, 0, sub[0][0])[0] if sub else []
            params = []
            if m.group(3):
                for p in m.group(3).split(","):
                    p = p.strip()
                    if p:
                        n, _, dflt = p.partition("=")
                        params.append((n.strip(), dflt.strip() or None))
            if m.group(1) in LABELS:
                _anomalia("label doppio: " + m.group(1))
            LABELS[m.group(1)] = [params, nodi, None]
            LABEL_TESTO[m.group(1)] = "\n".join(t for _i, t in sub)
            nomi.append(m.group(1))
        # fall-through: il label successivo nel file (se il top-level
        # successivo e' un label).
        for a, b in zip(nomi, nomi[1:]):
            if a and b:
                LABELS[a][2] = b
        conta = len(re.findall(r"(?m)^label\s", TESTI[f]))
        trovati = sum(1 for n in nomi if n)
        if conta != trovati:
            _anomalia("%s: %d label nel testo, %d analizzati"
                      % (os.path.basename(f), conta, trovati))


_carica_label()


def _estrai(testo, inizio_re):
    """Sorgenti Python (dedent) delle istruzioni che iniziano con inizio_re:
    righe accumulate finche' il blocco non e' Python valido."""
    out = []
    righe = testo.split("\n")
    for i, r in enumerate(righe):
        if not re.match(r"\s*" + inizio_re, r):
            continue
        ind = len(r) - len(r.lstrip())
        buf = []
        for j in range(i, len(righe)):
            s = righe[j]
            buf.append(s[ind:] if s.startswith(" " * ind) else s.lstrip())
            src = "\n".join(buf)
            try:
                ast.parse(src)
            except SyntaxError:
                continue
            out.append(src)
            break
    return out


def _letterale(nome, file_rel):
    srcs = _estrai(TESTI[os.path.join(MAL, file_rel)], re.escape(nome) + r"\s*=\s*[\[{]")
    if len(srcs) != 1:
        raise RuntimeError("%s: %d definizioni in %s" % (nome, len(srcs), file_rel))
    return ast.literal_eval(srcs[0].split("=", 1)[1].strip())


CAL_GIORNI = _letterale("CAL_GIORNI", "calendario.rpy")
FULLSEQ = cl.genera_sequenza(CAL_GIORNI)
SLOTORD = {s: i for i, s in enumerate(cl.SLOTS)}


def _k(m):
    return (m[0], m[1], SLOTORD[m[2]])


DONI = _letterale("DONI", "economia.rpy")
DONI_GUSTI = _letterale("DONI_GUSTI", "economia.rpy")
MERCATO_LUNE = _letterale("MERCATO_LUNE", "economia.rpy")
PRIMI_ORIGLIATI = _letterale("PRIMI_ORIGLIATI", os.path.join("routes", "origliati.rpy"))
_m = re.search(r"(?m)^\s*ICARO_GELOSIA\s*=\s*(\d+)",
               TESTI[os.path.join(MAL, "routes", "icaro_eventi.rpy")])
ICARO_GELOSIA = int(_m.group(1))

# Registry: EVENTI, ATTIVITA, ATTIVITA_RIPETIBILI, pool_aggiungi.
EVENTI = []
ATTIVITA = {"mattina": [], "pomeriggio": [], "sera": []}
ATTIVITA_RIPETIBILI = {}
REA_NOTI = [True]


def _pool_aggiungi(att_id, label, indice=None):
    for voci in ATTIVITA.values():
        for voce in voci:
            if voce[0] == att_id and label not in voce[3]:
                if indice is None:
                    voce[3].append(label)
                else:
                    voce[3].insert(indice, label)
                return
    raise KeyError(att_id)


_ENV_REG = {"EVENTI": EVENTI, "ATTIVITA": ATTIVITA,
            "ATTIVITA_RIPETIBILI": ATTIVITA_RIPETIBILI,
            "rivali_cuore": rl.rivali_cuore, "rl": rl, "rlz": rlz, "csl": csl,
            "cl": cl, "mgl": mgl, "PRIMI_ORIGLIATI": PRIMI_ORIGLIATI,
            "rea_noti": lambda *a: REA_NOTI[0],
            "pool_aggiungi": _pool_aggiungi}


def _carica_registry():
    pool = []
    for f in FILES:
        t = TESTI[f]
        for pat in (r"EVENTI\.(extend|append)\(", r"ATTIVITA\[",
                    r"ATTIVITA_RIPETIBILI\["):
            for src in _estrai(t, pat):
                exec(src, _ENV_REG)
        pool += _estrai(t, r"pool_aggiungi\(")
    for src in pool:
        exec(src, _ENV_REG)


_carica_registry()
EV = {e["id"]: e for e in EVENTI}
POOL = {}   # att_id -> (char, [label], cond, slot)
for _slot, _voci in ATTIVITA.items():
    for _v in _voci:
        POOL.setdefault(_v[0], (_v[2], _v[3], _v[4] if len(_v) > 4 else None, _slot))
SLOT_ATT = {s: [v[0] for v in voci] for s, voci in ATTIVITA.items()}


# Analizzatore di percorsi ##################################################

class _Ign:
    """Valore sconosciuto: la sua lettura fa fallire la valutazione."""


UNK = _Ign()
_SAFE = {"__builtins__": {}, "rl": rl, "rlz": rlz, "mgl": mgl, "csl": csl,
         "cl": cl, "sorted": sorted, "len": len, "min": min, "max": max,
         "any": any, "all": all, "set": set, "frozenset": frozenset,
         "tuple": tuple, "list": list, "dict": dict, "str": str, "int": int,
         "bool": bool, "abs": abs, "sum": sum, "True": True, "False": False,
         "None": None, "rivali_cuore": rl.rivali_cuore,
         "cuore_classifica": rl.cuore_classifica,
         "cuore_soglie": rl.cuore_soglie, "CUORE_VAR": rl.CUORE_VAR,
         "CAL_AFF_VAR": rl.CUORE_VAR, "DONI": DONI, "DONI_GUSTI": DONI_GUSTI,
         "ICARO_GELOSIA": ICARO_GELOSIA}

BASE_KEYS = set(TRACK) | {"ofelia_mancati", "route_attiva", "route_seconda",
                          "player_gender", "congelate", "eventi_visti",
                          "cal_luna", "dono_tenuto"}


def _cal_vars(env):
    v = {k: env.get(k) for k in BASE_KEYS}
    v.update(visti=env.get("eventi_visti"), luna=env.get("cal_luna"),
             flag_accetta_lavoro=True, flag_giuramento=True)
    return v


FUNCS = {
    "route_viva": (lambda env: lambda: rl.route_viva(env.get("route_attiva"), env.get("congelate")),
                   {"route_attiva", "congelate"}),
    "route_seconda_viva": (lambda env: lambda: rl.route_seconda_viva(
        env.get("route_attiva"), env.get("route_seconda"), env.get("congelate")),
        {"route_attiva", "route_seconda", "congelate"}),
    "cal_vars": (lambda env: lambda: _cal_vars(env), set(BASE_KEYS)),
    "rea_noti": (lambda env: lambda *a: REA_NOTI[0], set()),
}


class Env:
    """Mapping per eval: mods sopra base; UNK -> nome sconosciuto."""
    __slots__ = ("base", "mods")

    def __init__(self, base, mods):
        self.base = base
        self.mods = mods

    def get(self, k, d=None):
        v = self.mods[k] if k in self.mods else self.base.get(k, d)
        return d if v is UNK else v

    def __getitem__(self, k):
        if k in FUNCS:
            return FUNCS[k][0](self)
        v = self.mods[k] if k in self.mods else self.base[k]
        if v is UNK:
            raise KeyError(k)
        return v


@functools.lru_cache(maxsize=None)
def _compila(src):
    return compile(src, "<rpy>", "eval")


def _valuta(src, env):
    """(ok, valore)."""
    try:
        return True, eval(_compila(src.strip()), _SAFE, env)
    except Exception:
        return False, None


def _cond(src, env):
    ok, v = _valuta(src, env)
    if not ok:
        return None
    try:
        return bool(v)
    except Exception:
        return None


# Stato del walker: (delta, cong_aggiunte, mods, finito)
NOMI_RE = re.compile(r"\b[A-Za-z_]\w*\b")
SALTA_CALL = {"dono_check", "dono_reazione", "epilogo_semestre"}
TRACK_RE = re.compile(r"\b(" + "|".join(TRACK) + r")\b\s*(\+=|-=|=(?!=))")


def _applica(st, i, d):
    delta, cong, mods, fin = st
    delta = delta[:i] + (delta[i] + d,) + delta[i + 1:]
    return delta, cong, mods, fin


def _set_mod(st, nome, val):
    delta, cong, mods, fin = st
    m = dict(mods)
    m[nome] = val
    return delta, cong, m, fin


def _env(base, st):
    """Env per eval: i tracciati assoluti = base + delta."""
    delta, cong, mods, _f = st
    m = dict(mods)
    for n, i in TI.items():
        if delta[i]:
            m[n] = base[n] + delta[i]
    if cong:
        m["congelate"] = frozenset(base["congelate"]) | cong
    return Env(base, m)


def _py(s, st, base, ctx):
    """Una istruzione Python (riga di $ o di un blocco python)."""
    s = re.sub(r"\bstore\.", "", s.strip())
    if s in ("pass",) or not s:
        return [st]
    m = re.match(r"(\w+)\s*([+-])=\s*(.+)$", s)
    if m:
        nome, seg, rhs = m.groups()
        if nome in TI:
            ok, v = _valuta(rhs, _env(base, st))
            mg = re.match(r"mgl\.delta\(\s*[\"'](\w+)[\"']\s*,", rhs)
            if not ok and mg:
                # Esito del minigioco sconosciuto: tutti i delta del gioco
                # (piu' 0 = "lasciato").
                vals = {d for (g, _e), d in mgl.DELTA.items() if g == mg.group(1)} | {0}
                return [_applica(st, TI[nome], x if seg == "+" else -x) for x in sorted(vals)]
            if not ok or not isinstance(v, int):
                _anomalia("%s: incremento non valutabile: %s" % (ctx, s))
                return [st]
            return [_applica(st, TI[nome], v if seg == "+" else -v)]
        return [_set_mod(st, nome, UNK)]
    m = re.match(r"([\w\s,]+?)\s*=(?!=)\s*(.+)$", s)
    if m:
        nomi = [n.strip() for n in m.group(1).split(",")]
        for n in nomi:
            if n in TI:
                _anomalia("%s: assegnazione a variabile seguita: %s" % (ctx, s))
        if len(nomi) == 1:
            ok, v = _valuta(m.group(2), _env(base, st))
            return [_set_mod(st, nomi[0], v if ok else UNK)]
        for n in nomi:
            st = _set_mod(st, n, UNK)
        return [st]
    m = re.match(r"congelate\.add\((.+)\)$", s)
    if m:
        ok, v = _valuta(m.group(1), _env(base, st))
        if not ok:
            _anomalia("%s: congelate.add non valutabile: %s" % (ctx, s))
            return [st]
        delta, cong, mods, fin = st
        return [(delta, cong | {v}, mods, fin)]
    m = re.match(r"eco_spendi\((.+)\)$", s)
    if m:
        ok, v = _valuta(m.group(1), _env(base, st))
        if not ok:
            _anomalia("%s: eco_spendi non valutabile: %s" % (ctx, s))
            return [st]
        # eco_spendi non scende sotto zero.
        v = min(v, base["scudi"] + st[0][I_SCUDI])
        return [_applica(st, I_SCUDI, -v)]
    if s == "druso_passo_falso()":
        # druso_core.rpy: -1 sempre; per un uomo conta il passo falso e al
        # secondo Druso congela (rl.druso_passo_falso).
        st = _applica(st, TI[VAR["druso"]], -1)
        p0 = base.get("druso_passi_falsi", 0)
        prima = (0 if p0 is UNK else p0) + st[0][I_PASSI]
        passi, _avvisa, congela = rl.druso_passo_falso(base["player_gender"], prima)
        st = _applica(st, I_PASSI, passi - prima)
        if congela:
            st = (st[0], st[1] | {"druso"}, st[2], st[3])
        return [st]
    m = re.match(r"rivali_sposta\((.+),(.+)\)$", s)
    if m:
        env = _env(base, st)
        ok1, a = _valuta(m.group(1), env)
        ok2, b = _valuta(m.group(2), env)
        if not (ok1 and ok2):
            _anomalia("%s: rivali_sposta non valutabile" % ctx)
            return [st]
        return [_applica(_applica(st, TI[VAR[a]], 1), TI[VAR[b]], -1)]
    m = re.match(r"renpy\.call_in_new_context\(\s*\"(\w+)\"", s)
    if m:
        return _chiama(m.group(1), "", st, base, ctx)
    if TRACK_RE.search(s) or re.search(r"congelate\.\w+\(", s):
        _anomalia("%s: istruzione non capita: %s" % (ctx, s))
    return [st]


def _chiama(nome, args, st, base, ctx):
    if nome in SALTA_CALL:
        return [st]
    if nome not in LABELS:
        _anomalia("%s: call a label inesistente %s" % (ctx, nome))
        return [st]
    params = LABELS[nome][0]
    env = _env(base, st)
    vals = {}
    pos = [a.strip() for a in args.split(",")] if args.strip() else []
    for k, (p, dflt) in enumerate(params):
        src = pos[k] if k < len(pos) else dflt
        if src is None:
            vals[p] = UNK
        else:
            ok, v = _valuta(src, env)
            vals[p] = v if ok else UNK
    out = []
    for d, c, m in esiti_label(nome, env, tuple(sorted(vals.items(), key=lambda t: t[0]))):
        delta = tuple(a + b for a, b in zip(st[0], d))
        mods = dict(st[2])
        mods.update(m)
        out.append((delta, st[1] | c, mods, False))
    return out


def _walk(nodi, stati, base, ctx, py=False):
    vivi = [s for s in stati if not s[3]]
    finiti = [s for s in stati if s[3]]
    i = 0
    while i < len(nodi) and vivi:
        txt, figli = nodi[i]
        i += 1
        if re.match(r"if\b", txt):
            catena = [(txt[2:].rstrip(":").strip(), figli)]
            while i < len(nodi) and re.match(r"(elif\b|else\s*:)", nodi[i][0]):
                t2 = nodi[i][0]
                catena.append((None if t2.startswith("else") else t2[4:].rstrip(":").strip(),
                               nodi[i][1]))
                i += 1
            nuovi = []
            for st in vivi:
                env = _env(base, st)
                resto = True
                for cond, corpo in catena:
                    r = True if cond is None else _cond(cond, env)
                    if r is False:
                        continue
                    nuovi += _walk(corpo, [st], base, ctx, py)
                    if r is True:
                        resto = False
                        break
                if resto:
                    nuovi.append(st)
            vivi = nuovi
        elif not py and re.match(r"menu\b.*:$", txt):
            opz = []
            for t2, f2 in figli:
                if t2.startswith('"') and t2.endswith(":"):
                    mm = re.search(r'"\s*(?:\([^"]*\))?\s*if\s+(.+):$', t2)
                    opz.append((mm.group(1) if mm else None, f2))
            nuovi = []
            for st in vivi:
                env = _env(base, st)
                ok = [(c, f2) for c, f2 in opz if c is None or _cond(c, env) is not False]
                if not ok:
                    nuovi.append(st)
                for _c, f2 in ok:
                    nuovi += _walk(f2, [st], base, ctx, py)
            vivi = nuovi
        elif re.match(r"(while|for)\b", txt):
            vivi = vivi + _walk(figli, vivi, base, ctx, py)
        elif re.match(r"(try|except\b.*|finally|with\b.*)\s*:$", txt) and py:
            vivi = _walk(figli, vivi, base, ctx, py)
        elif re.match(r"python\b.*:$", txt) and not py:
            vivi = _walk(figli, vivi, base, ctx, True)
        elif re.match(r"(def|class)\b", txt):
            pass
        elif txt.startswith("$"):
            nuovi = []
            for st in vivi:
                nuovi += _py(txt[1:], st, base, ctx)
            vivi = nuovi
        elif not py and txt == "return" or py and txt.startswith("return"):
            vivi = [(d, c, m, True) for d, c, m, _f in vivi]
        elif not py and txt.startswith("call "):
            if re.match(r"call\s+(expression|screen)\b", txt):
                continue
            mm = re.match(r"call\s+(\w+)\s*(?:pass\s*)?(?:\((.*?)\))?\s*(?:from\s+\w+)?$", txt)
            if not mm:
                _anomalia("%s: call non capita: %s" % (ctx, txt))
                continue
            nuovi = []
            for st in vivi:
                nuovi += _chiama(mm.group(1), mm.group(2) or "", st, base, ctx)
            vivi = nuovi
        elif not py and txt.startswith("jump "):
            mm = re.match(r"jump\s+(\w+)$", txt)
            nuovi = []
            if mm and mm.group(1) != "expression":
                for st in vivi:
                    nuovi += _chiama(mm.group(1), "", st, base, ctx)
            else:
                nuovi = vivi
            vivi = [(d, c, m, True) for d, c, m, _f in nuovi]
        elif py:
            nuovi = []
            for st in vivi:
                nuovi += _py(txt, st, base, ctx)
            vivi = nuovi
        # altro (dialoghi, show, scene...): nessun effetto.
        if vivi:
            vivi = _dedup(vivi)
        finiti += [s for s in vivi if s[3]]
        vivi = [s for s in vivi if not s[3]]
    return _dedup(finiti + vivi)


def _chiave_mods(m):
    out = []
    for k, v in sorted(m.items(), key=lambda t: t[0]):
        try:
            hash(v)
        except TypeError:
            v = repr(v)
        out.append((k, v))
    return tuple(out)


def _dedup(stati):
    visti = {}
    for s in stati:
        k = (s[0], s[1], _chiave_mods(s[2]), s[3])
        if k not in visti:
            visti[k] = s
    return list(visti.values())


@functools.lru_cache(maxsize=None)
def letture(nome):
    """Nomi dello stato base letti dal label (chiusura su call/jump/
    fall-through)."""
    vis = set()
    out = set()
    pila = [nome]
    while pila:
        n = pila.pop()
        if n in vis or n not in LABELS:
            continue
        vis.add(n)
        testo = LABEL_TESTO[n]
        for tok in set(NOMI_RE.findall(testo)):
            if tok in BASE_KEYS:
                out.add(tok)
            if tok in FUNCS:
                out |= FUNCS[tok][1]
            if tok == "druso_passo_falso":
                out |= {"druso_passi_falsi", "player_gender"}
            if tok == "eco_spendi":
                out.add("scudi")
        pila += re.findall(r"(?:call|jump)\s+(\w+)", testo)
        pila += re.findall(r"call_in_new_context\(\s*\"(\w+)\"", testo)
        if LABELS[n][2]:
            pila.append(LABELS[n][2])
    return frozenset(out)


_CACHE = {}


def esiti_label(nome, env, args=()):
    """Esiti distinti del label: [(delta, cong_aggiunte, mods)]. env: Env o
    dict dello stato di partenza."""
    base = env.base if isinstance(env, Env) else env
    mods0 = env.mods if isinstance(env, Env) else {}
    chiave_stato = []
    for n in sorted(letture(nome)):
        v = env.get(n, UNK) if isinstance(env, Env) else env.get(n, UNK)
        if isinstance(v, (set, frozenset)):
            v = frozenset(v)
        chiave_stato.append(v)
    extra = tuple((k, v) for k, v in sorted(mods0.items()) if k not in BASE_KEYS
                  and re.search(r"\b%s\b" % re.escape(k), LABEL_TESTO.get(nome, "")))
    key = (nome, args, tuple(chiave_stato), _chiave_mods(dict(extra)))
    if key in _CACHE:
        return _CACHE[key]
    _CACHE[key] = [(ZERO, frozenset(), {})]  # guardia contro la ricorsione
    b = {n: (env.get(n, UNK) if isinstance(env, Env) else env.get(n, UNK)) for n in BASE_KEYS}
    m0 = dict(extra)
    m0.update(args)
    stati = [(ZERO, frozenset(), m0, False)]
    n = nome
    visitati = set()
    while True:
        visitati.add(n)
        stati = _walk(LABELS[n][1], stati, b, n)
        prossimo = LABELS[n][2]
        if all(s[3] for s in stati) or not prossimo or prossimo in visitati:
            break
        aperti = [s for s in stati if not s[3]]
        chiusi = [s for s in stati if s[3]]
        stati = chiusi + _walk(LABELS[prossimo][1], aperti, b, prossimo)
        n = prossimo
        if all(s[3] for s in stati):
            break
    res = _dedup([(d, c, m, False) for d, c, m, _f in stati])
    nomi_args = {k for k, _v in args}
    res = [(d, c, {k: v for k, v in m.items() if k not in nomi_args}) for d, c, m, _f in res]
    _CACHE[key] = res
    return res


# Simulatore ################################################################

CUORE = next(m for m in FULLSEQ if (m[0], m[1], m[2]) == (EV["scelta_cuore"]["luna"],
                                                          EV["scelta_cuore"]["giorno"],
                                                          EV["scelta_cuore"]["slot"]))
PRE = [m for m in FULLSEQ if _k(m) <= _k(CUORE)]

# Impegno chiamato dalla scelta del cuore (verificato sul label in
# test_raggiungibilita: ogni label deve comparire in ev_scelta_cuore).
IMPEGNO = {"aede": "impegno_aede", "caino": "impegno_caino",
           "druso": "impegno_druso", "ofelia": "impegno_ofelia",
           ("icaro", "f"): "impegno_icaro", ("icaro", "m"): "impegno_bro",
           "ofelia+aede": "impegno_ofelia_aede",
           "ofelia+caino": "impegno_ofelia_caino"}


def _proj(d, c, targets, mode):
    """Proiezione di un esito sulle dimensioni dei bersagli, orientata in
    modo che "piu' grande = meglio" per la direzione di ricerca."""
    sg = -1 if mode == "min" else 1
    st = sg if mode == "maxtrap" else -sg   # "maxtrap": trappole cercate
    v = tuple(sg * d[TI[VAR[t]]] for t in targets)
    if mode == "somma":   # piu' bersagli: un solo asse, la somma
        v = (sum(v),)
    return v + (d[I_SCUDI], st * d[I_TRAP], -sg * d[I_SOSP], -d[I_PASSI],
                tuple(-(t in c) for t in targets))


def _pota(esiti, targets, mode):
    """max/min: frontiera di Pareto sulle dimensioni dei bersagli (verso
    l'alto o verso il basso); "all": un esito per proiezione distinta."""
    per = {}
    for e in esiti:
        p = _proj(e[0], e[1], targets, mode)
        per.setdefault(p, e)
    if mode == "all" or len(per) == 1:
        return list(per.values())
    ps = list(per)

    def dom(a, b):
        return a != b and all(x >= y for x, y in zip(a[:-1], b[:-1])) and             all(x >= y for x, y in zip(a[-1], b[-1]))
    return [per[p] for p in ps if not any(dom(q, p) for q in ps)]


def run(targets, gender="f", route=None, seconda=None, mode="max", obj=None,
        seq=None, scudi0=None, al_cuore=False, mode_post=None, clamp_cuore=False, inizio=None,
        sempre_passa=False):
    """Esplorazione esaustiva. targets: personaggi su cui scegliere.
    route/seconda: scelta del cuore da tentare (None = nessuna).
    obj(fin) -> tupla da massimizzare; fin = dict finale (aff, visti, cong,
    trap, sosp, passi, route, seconda, mancati, alive). al_cuore: la corsa finisce
    alla scelta del cuore (fin["candidati"] = rl.cuore_candidati).
    mode (prima del cuore) / mode_post (dopo; default = mode): "max" e
    "min" potano gli esiti di ogni scena a Pareto sui bersagli (verso
    l'alto / verso il basso; "maxtrap" come max ma con le trappole di Caino
    cercate invece che evitate; "somma" come max ma sulla somma dei
    bersagli: per le coppie), "all" li tiene tutti. Potare restringe le
    scelte: un punteggio trovato e' sempre raggiungibile nel modello. clamp_cuore: scelto il
    cuore, l'affinita' dei bersagli scende alla soglia del cuore (si parte
    "dalla soglia"). inizio: fin["stato"] di una corsa precedente (es.
    al_cuore) da cui ripartire, con lo stesso seq. Nelle ricerche verso
    l'alto "passa" (attivita' a 0 punti) e' offerto solo se non c'e' altro
    e si da' solo il dono preferito; sempre_passa=True li riapre (per
    cercare partite che rimandano le scene). Ritorna (punteggio, fin).
    """
    mode_pre = mode
    mode_post = mode_post or mode
    targets = tuple(targets)
    seqv = seq or FULLSEQ
    if scudi0 is None:
        scudi0 = int(re.search(r"(?m)^default scudi = (\d+)",
                               TESTI[os.path.join(MAL, "economia.rpy")]).group(1))
    tset = set(targets)

    def fin_di(idx, aff, scudi, trap, sosp, passi, mancati, visti, cong, dono, dati,
               rt, sec, cand=None):
        d = dict(zip(CHARS, aff))
        alive = bool(rt) and rt not in cong and (not sec or sec not in cong)
        return {"aff": d, "visti": visti, "cong": cong, "trap": trap,
                "sosp": sosp, "passi": passi, "route": rt, "seconda": sec, "mancati": mancati,
                "alive": alive, "candidati": cand,
                "stato": (idx, aff, scudi, trap, sosp, passi, mancati, visti, cong,
                          dono, dati, rt, sec)}

    if obj is None:
        def obj(f):
            return (f["alive"],) + tuple(f["aff"][t] for t in targets)

    def base_di(aff, scudi, trap, sosp, passi, mancati, rt, sec, cong, visti, luna, dono):
        b = {VAR[c]: aff[i] for i, c in enumerate(CHARS)}
        b.update(scudi=scudi, caino_trappole=trap, aede_sospetto=sosp, druso_passi_falsi=passi,
                 ofelia_mancati=mancati, route_attiva=rt, route_seconda=sec,
                 player_gender=gender, congelate=cong, eventi_visti=visti,
                 cal_luna=luna, dono_tenuto=dono)
        return b

    def tocca(esiti):
        return any(any(d[TI[VAR[t]]] for t in targets) or (c & tset)
                   for d, c, _m in esiti)

    @functools.lru_cache(maxsize=None)
    def go(idx, aff, scudi, trap, sosp, passi, mancati, visti, cong, dono, dati, rt, sec):
        if idx >= len(seqv):
            f = fin_di(idx, aff, scudi, trap, sosp, passi, mancati, visti, cong, dono, dati, rt, sec)
            return obj(f), f
        mom = seqv[idx]
        luna, _g, slot = mom
        base = base_di(aff, scudi, trap, sosp, passi, mancati, rt, sec, cong, visti, luna, dono)
        vv = _cal_vars(base)
        vv["congelate"] = set(cong)
        vv["visti"] = set(visti)

        mode = mode_post if "scelta_cuore" in visti else mode_pre
        esplora_poco = mode in ("max", "somma", "maxtrap") and not sempre_passa

        def segui(esiti, nv):
            best = None
            for d, c, _m in _pota(esiti, targets, mode):
                na = tuple(aff[i] + d[TI[VAR[ch]]] for i, ch in enumerate(CHARS))
                r = go(idx + 1, na, scudi + d[I_SCUDI], trap + d[I_TRAP],
                       sosp + d[I_SOSP], passi + d[I_PASSI], mancati, nv, cong | c, dono, dati, rt, sec)
                if best is None or r[0] > best[0]:
                    best = r
            return best

        try:
            fx = cl.trova_fisso(mom, EVENTI, vv, visti)
        except Exception as e:  # cond rotta
            _anomalia("cond di fisso in errore a %s: %s" % (mom, e))
            fx = None
        if fx is not None:
            eid = fx["id"]
            nv = visti | {eid}
            if eid == "scelta_cuore":
                cand = rl.cuore_candidati(vv)
                if al_cuore:
                    f = fin_di(idx, aff, scudi, trap, sosp, passi, mancati, visti, cong, dono,
                               dati, rt, sec, cand)
                    return obj(f), f
                if route is None:
                    return go(idx + 1, aff, scudi, trap, sosp, passi, mancati, nv, cong, dono, dati, rt, sec)
                if seconda:
                    ok = route in cand and seconda in cand
                    lab = IMPEGNO[route + "+" + seconda]
                else:
                    ok = route in cand
                    lab = IMPEGNO.get(route) or IMPEGNO[(route, gender)]
                best = None
                if ok:
                    for d, c, m in esiti_label(lab, base):
                        if seconda:
                            if not (m.get("impegno_of") is True and m.get("impegno_altro") is True):
                                continue
                        elif m.get("impegno_esito") is not True:
                            continue
                        na = tuple(aff[i] + d[TI[VAR[ch]]] for i, ch in enumerate(CHARS))
                        if clamp_cuore:
                            sog = rl.cuore_soglie(gender == "f")
                            na = tuple(min(v, sog[ch]) if ch in tset else v
                                       for v, ch in zip(na, CHARS))
                        r = go(idx + 1, na, scudi + d[I_SCUDI], trap + d[I_TRAP], sosp + d[I_SOSP], passi + d[I_PASSI],
                               mancati, nv, cong | c, dono, dati, route, seconda)
                        if best is None or r[0] > best[0]:
                            best = r
                if best is None:
                    best = go(idx + 1, aff, scudi, trap, sosp, passi, mancati, nv, cong, dono, dati, rt, sec)
                return best
            return segui(esiti_label(fx["label"], base), nv)

        # Inviti e attivita' del momento.
        try:
            inv = cl.trova_inviti(mom, EVENTI, vv, visti)
        except Exception as e:
            _anomalia("cond di invito in errore a %s: %s" % (mom, e))
            inv = []
        if rt is not None:
            inv = [e for e in inv if e.get("char") in (None, rt, sec)]
        scade = [e["id"] for e in inv if e.get("scade")]
        att = []
        for a in SLOT_ATT[slot]:
            ch, pool, cond, _s = POOL[a]
            try:
                if cond is not None and not cond(vv):
                    continue
            except Exception as e:
                _anomalia("cond di attivita' %s in errore: %s" % (a, e))
                continue
            att.append(a)
        if not inv and not att:
            return go(idx + 1, aff, scudi, trap, sosp, passi, mancati, visti, cong, dono, dati, rt, sec)

        def dopo_scadenza(scelto, na, ncong, nman):
            """Inviti di Ofelia lasciati cadere (ofelia_scadenza)."""
            ign = cl.inviti_ignorati([{"id": i, "scade": True} for i in scade], scelto)
            extra = ZERO
            for es in rlz.ofelia_esiti_scadenza(ign, nman, "ofelia" in ncong):
                nman += 1
                na = tuple(v - (c == "ofelia") for v, c in zip(na, CHARS))
                if es == "gelo":
                    ncong = ncong | {"ofelia"}
                elif es == "prima":
                    b2 = base_di(na, scudi, trap, sosp, passi, nman, rt, sec, ncong, visti, luna, dono)
                    ee = esiti_label("ofelia_scadenza_prima", b2)
                    if len(ee) != 1 or ee[0][0] != ZERO or ee[0][1]:
                        _anomalia("ofelia_scadenza_prima ha esiti con punti: non modellati")
            return na, ncong, nman, extra

        def dono_dopo(ch, na, ncong, dono_, dati_):
            """dono_check(ch): opzioni (na, dono, dati)."""
            opz = [(na, dono_, dati_)]
            if dono_ is None or not rlz.dono_offribile(dono_, ch, dati_, ncong):
                return opz
            esito, segna = rlz.dono_consegna(DONI_GUSTI, ch, dono_, dati_)
            if esplora_poco:
                # Ricerca verso l'alto: si da' solo il dono preferito.
                if esito != "ama":
                    return opz
                opz = []
            b2 = base_di(na, scudi, trap, sosp, passi, mancati, rt, sec, ncong, visti, luna, dono_)
            for d, _c, _m in esiti_label("dono_" + ch, b2, (("dono_esito", esito),)):
                na2 = tuple(v + d[TI[VAR[c]]] for v, c in zip(na, CHARS))
                opz.append((na2, None, dati_ | ({ch} if segna else frozenset())))
            return opz

        scelte = []
        for e in inv:
            if e.get("char") in tset or tocca(esiti_label(e["label"], base)):
                scelte.append(("inv", e))
        for a in att:
            ch, pool, _c, _s = POOL[a]
            if a in ATTIVITA_RIPETIBILI:
                if ATTIVITA_RIPETIBILI[a] != "eco_mercato":
                    _anomalia("attivita' ripetibile non modellata: " + a)
                    continue
                for k in MERCATO_LUNE.get(luna, MERCATO_LUNE[1]):
                    if DONI[k][1] > scudi:
                        continue
                    utile = any(c2 in tset and c2 not in dati and
                                (DONI_GUSTI[c2][0] == k or (mode in ("min", "all") and DONI_GUSTI[c2][1] == k))
                                for c2 in DONI_GUSTI)
                    if utile:
                        scelte.append(("buy", k))
                continue
            lab = cl.pesca_variante(pool, visti)
            if lab is None:
                if ch in tset and dono is not None:
                    scelte.append(("att", a))
                continue
            if ch in tset or tocca(esiti_label(lab, base)):
                scelte.append(("att", a))
        # "passa" = un'attivita' a 0 punti. Verso l'alto serve solo se non
        # c'e' altro (restringere le scelte resta corretto: ogni punteggio
        # trovato e' giocabile); verso il basso e' sempre possibile.
        if not esplora_poco or not scelte:
            scelte.append(("passa", None))

        best = None
        for kind, x in scelte:
            if kind == "inv":
                nv = visti | {x["id"]}
                ch = x.get("char")
                esiti = [(d, c, m) for d, c, m in esiti_label(x["label"], base)]
                scelto = x["id"]
            elif kind == "att":
                ch, pool, _c, _s = POOL[x]
                lab = cl.pesca_variante(pool, visti)
                nv = visti | ({lab} if lab else set())
                e1 = esiti_label(lab, base) if lab else [(ZERO, frozenset(), {})]
                e2 = esiti_label("eco_dopo_attivita", base, (("att_id", x), ("char", ch)))
                esiti = [(tuple(a + b for a, b in zip(d1, d2)), c1 | c2, {})
                         for d1, c1, _m1 in e1 for d2, c2, _m2 in e2]
                scelto = None
            elif kind == "buy":
                nv, ch, scelto = visti, None, None
                esiti = [(ZERO[:I_SCUDI] + (-DONI[x][1],) + ZERO[I_SCUDI + 1:], frozenset(), {})]
            else:
                nv, ch, scelto, esiti = visti, None, None, [(ZERO, frozenset(), {})]
            for d, c, _m in _pota(esiti, targets, mode):
                na = tuple(aff[i] + d[TI[VAR[cc]]] for i, cc in enumerate(CHARS))
                ncong = cong | c
                ns = scudi + d[I_SCUDI]
                nd = x if kind == "buy" else dono
                # Gelosia di Icaro (cal_post_evento_hooks, solo inviti).
                if (kind == "inv" and ch not in (None, "icaro") and gender == "f"
                        and na[CHARS.index("icaro")] >= ICARO_GELOSIA and rt is None
                        and "icaro" not in ncong):
                    ncong = ncong | {"icaro"}
                na, ncong, nman, _x = dopo_scadenza(scelto, na, ncong, mancati)
                opz = dono_dopo(ch, na, ncong, nd, dati) if ch else [(na, nd, dati)]
                for na2, nd2, ndati in opz:
                    r = go(idx + 1, na2, ns, trap + d[I_TRAP], sosp + d[I_SOSP], passi + d[I_PASSI], nman,
                           nv, ncong, nd2, ndati, rt, sec)
                    if best is None or r[0] > best[0]:
                        best = r
        return best

    if inizio is not None:
        res = go(*inizio)
    else:
        res = go(0, (0,) * len(CHARS), scudi0, 0, 0, 0, 0, frozenset(), frozenset(), None,
                 frozenset(), None, None)
    go.cache_clear()
    return res


if __name__ == "__main__":
    import time
    t0 = time.time()
    for gnd in ("f", "m"):
        for t in CHARS:
            soglia = rl.cuore_soglie(gnd == "f")[t]
            r = run([t], gnd, seq=PRE, al_cuore=True,
                    obj=lambda f, t=t: (t in f["candidati"], f["aff"][t]))
            f = run([t], gnd, route=t)
            print(gnd, t, "max IV/28:", r[0], "soglia", soglia,
                  "| max finale:", f[0], "GOOD", rl.GOOD[t])
    print("anomalie:", ANOMALIE)
    print("%.1f s" % (time.time() - t0))
