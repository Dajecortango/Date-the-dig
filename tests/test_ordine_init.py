"""Verifica che l'ordine di caricamento dei registry (EVENTI, ATTIVITA,
hook del calendario) non cambi quando i file delle route vengono spostati.

Ren'Py esegue i blocchi init a pari priorita' nell'ordine dei file (percorso
relativo a game/, ordinato) e poi delle righe: lo stesso ordine qui.

Secondo controllo (usi_prematuri): i file sotto game/capitoli/ si ordinano
prima di effetti/feedback/.../screens, quindi il loro codice a init 0 non
deve usare nomi che quei file definiscono a init 0 (serve init 1 o piu').

Uso: py -3 -I tests/test_ordine_init.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.normpath(os.path.join(HERE, "..", "game"))

RE_ID = re.compile(r'"id":\s*"([^"]+)"')
RE_ATT = re.compile(r'ATTIVITA\[[^\]]+\]\.(?:append|extend)\(')
RE_TUPLA = re.compile(r'(?:^|[\[(,]\s*)\(\s*"([^"]+)"')
RE_HOOK = re.compile(r'(\w+_hooks)\.append\((\w+)\)')


def _file_rpy():
    out = []
    for radice, _, nomi in os.walk(GAME):
        for n in nomi:
            if n.endswith(".rpy"):
                p = os.path.join(radice, n)
                out.append(os.path.relpath(p, GAME).replace(os.sep, "/"))
    return sorted(out)


def ordine_init():
    token = []
    for rel in _file_rpy():
        with open(os.path.join(GAME, rel), encoding="utf-8") as f:
            righe = f.read().split("\n")
        in_eventi = False
        in_att = False
        prof_att = 0
        for r in righe:
            s = r.strip()
            if s.startswith("#"):
                continue
            if "EVENTI.extend(" in s or "EVENTI.append(" in s:
                in_eventi = True
            if RE_ATT.search(s):
                in_att = True
            if in_eventi:
                for m in RE_ID.finditer(s):
                    token.append("EV:" + m.group(1))
                if s.startswith("])") or s.endswith("})") or s == ")":
                    in_eventi = False
            if in_att:
                testo = s.split("(", 1)[1] if RE_ATT.search(s) else s
                for m in RE_TUPLA.finditer(testo):
                    token.append("AT:" + m.group(1))
                prof_att += s.count("(") - s.count(")")
                if prof_att <= 0:
                    in_att = False
                    prof_att = 0
            m = RE_HOOK.search(s)
            if m:
                token.append("HK:%s:%s" % (m.group(1), m.group(2)))
    return token


BASELINE = [
    'HK:cal_post_evento_hooks:conseguenze_dopo_evento',
    'AT:mercato',
    'EV:svelo',
    'EV:athlion',
    'EV:aede_cap1',
    'EV:aede_cap3',
    'EV:aede_cap4',
    'EV:interludio2',
    'EV:interludio3',
    'EV:aede_luna6',
    'AT:spada',
    'AT:scudo',
    'AT:studio',
    'AT:spada_p',
    'AT:riti',
    'AT:citta',
    'AT:studio_p',
    'AT:taverna',
    'AT:fumeria',
    'AT:ceppo_sera',
    'EV:adunanza',
    'EV:caino_cap1',
    'EV:caino_cap2',
    'EV:caino_cap3',
    'EV:caino_cap4',
    'EV:caino_cap5',
    'EV:caino_cap6',
    'EV:caino_luna5',
    'EV:caino_luna6',
    'AT:registri',
    'EV:ceppo_vanna',
    'EV:ceppo_corrado',
    'EV:briseide_brodo',
    'EV:ceppo_scelta',
    'EV:druso_ev1',
    'EV:druso_int1',
    'EV:druso_quaderno',
    'EV:druso_ev2',
    'EV:druso_int2',
    'EV:druso_udienza',
    'EV:druso_ev3',
    'EV:druso_int3',
    'EV:druso_ev4',
    'EV:druso_luna5',
    'EV:druso_luna6',
    'EV:icaro_ev1',
    'EV:icaro_int1',
    'EV:icaro_debito_altrui',
    'EV:icaro_ev2',
    'EV:icaro_int2',
    'EV:icaro_febbre',
    'EV:icaro_ev3',
    'EV:icaro_int3',
    'EV:icaro_bro1',
    'EV:icaro_bro2',
    'EV:icaro_luna5',
    'EV:icaro_luna6',
    'HK:cal_post_evento_hooks:icaro_gelosia',
    'EV:trio_lenora',
    'EV:incrocio_palestra',
    'EV:incrocio_carte',
    'EV:incrocio_debiti',
    'EV:incrocio_sorelle',
    'EV:incrocio_serra',
    'EV:udienza_lenora',
    'AT:corte',
    'HK:cal_inviti_ignorati_hooks:ofelia_scadenza',
    'EV:ofelia_ev1',
    'EV:ofelia_ev2',
    'EV:ofelia_ev3',
    'EV:ofelia_ev4',
    'EV:interludio_ofelia_1',
    'EV:interludio_ofelia_2',
    'EV:specchio_ofelia',
    'EV:ballo_pretendenti',
    'EV:interludio_ofelia_luna6',
    'EV:orig_druso_ofelia',
    'EV:rea_caino_conto',
    'EV:rea_lenora_segno',
    'EV:rea_aede_lanternaio',
    'EV:scelta_cuore',
    'EV:fiaccolata',
    'EV:aede_cap6',
    'EV:luna6_climax',
    'EV:rivalita',
]


# File comuni che, a pari priorita', si ordinano dopo game/capitoli/.
COMUNI_DOPO = ("effetti.rpy", "feedback.rpy", "finali_galleria.rpy", "gui.rpy",
               "luce.rpy", "menu_cast.rpy", "regia.rpy", "screens.rpy")
RE_INIT0 = re.compile(r"^init\s+python\s*:")
RE_NOME_DEF = re.compile(r"^    (?:def|class)\s+(\w+)|^    (\w+)\s*=[^=]")
RE_DEFINE = re.compile(r"^(?:define|transform|default)\s+([\w.]+)")
RE_NOME = re.compile(r"\b([A-Za-z_]\w*)\b")


def _nomi_init0(rel):
    """Nomi definiti a priorita' 0 (init python, define, transform) in rel."""
    nomi = set()
    in_init0 = False
    with open(os.path.join(GAME, rel), encoding="utf-8") as f:
        for r in f.read().split("\n"):
            if r and not r[0].isspace():
                in_init0 = bool(RE_INIT0.match(r))
                m = RE_DEFINE.match(r)
                # gui.x, persistent.x: attributi, non nomi dello store.
                if m and "." not in m.group(1):
                    nomi.add(m.group(1))
            elif in_init0:
                m = RE_NOME_DEF.match(r)
                if m:
                    nomi.add(m.group(1) or m.group(2))
    return nomi


def usi_prematuri():
    """(file, riga, nome): codice dei capitoli eseguito a init 0 (righe di
    primo livello di un init python, define, image) che usa un nome definito
    a init 0 in un file comune che si ordina dopo: sarebbe un NameError.
    I corpi di def/class e le screen girano dopo, a runtime."""
    comuni = set()
    for rel in COMUNI_DOPO:
        comuni |= _nomi_init0(rel)
    out = []
    for rel in _file_rpy():
        if not rel.startswith("capitoli/"):
            continue
        in_init0 = False
        with open(os.path.join(GAME, rel), encoding="utf-8") as f:
            righe = f.read().split("\n")
        for n, r in enumerate(righe, 1):
            codice = r.split("#", 1)[0]
            if r and not r[0].isspace():
                in_init0 = bool(RE_INIT0.match(r))
                if not (r.startswith("define ") or r.startswith("image ")):
                    continue
                codice = codice.split("=", 1)[-1]
            elif not (in_init0 and r.startswith("    ") and not r[4:5].isspace()):
                continue
            elif re.match(r"\s*(def|class|@)", codice):
                continue
            codice = re.sub(r'"[^"]*"|\'[^\']*\'', "", codice)
            for m in RE_NOME.finditer(codice):
                if m.group(1) in comuni:
                    out.append((rel, n, m.group(1)))
    return out


def main():
    got = ordine_init()
    if BASELINE is None or "--stampa" in sys.argv:
        print(repr(got))
        if BASELINE is None:
            print("BASELINE mancante")
            return 1
    prematuri = usi_prematuri()
    for rel, n, nome in prematuri:
        print("FAIL %s:%d usa %s a init 0 prima che sia definito" % (rel, n, nome))
    if got == BASELINE:
        print("ordine init ok")
        return 1 if prematuri else 0
    for i, (a, b) in enumerate(zip(got, BASELINE)):
        if a != b:
            print("FAIL indice %d: trovato %s, atteso %s" % (i, a, b))
            break
    else:
        print("FAIL lunghezza: trovati %d, attesi %d" % (len(got), len(BASELINE)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
