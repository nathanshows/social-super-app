#!/usr/bin/env python3
"""
hookscore_pt.py - the same five-check hook ruler as hookscore.py, made to read
Portuguese. The weights, the checks and the 50 cut-off are unchanged; only what
the ruler can see is wider.

Why it exists:  hookscore.py was calibrated on English. Its word pattern is
[A-Za-z], so "Ninguém" counts as two words ("Ningu", "m") and "Você" never
matches the viewer check. Its word lists are English, so "R$", "mil", "nunca",
"prejuízo" or "cachê" count for nothing. A Portuguese hook lost about half its
score for being in Portuguese.

What changed, on top of the English lists (English hooks score the same):
  - words: accented letters count as letters; "R$ 18.000" is one word
  - numbers: R$, mil, horas, min, dias, semanas, meses, anos, numbers in words
  - names: capitalised words with accents ("Simão", "Árvore")
  - stakes, imperatives, weak openers and dealbreakers in Portuguese
  - viewer: você, vocês, seu, sua, te, tu; first person: eu, meu, a gente, nós

Same limits as hookscore.py: it catches empty, slow and generic hooks. It does
not predict views.

Usage
  python3 hookscore_pt.py ganchos.txt          # um gancho por linha, ranqueado
  python3 hookscore_pt.py --hook "Perdi R$ 18 mil num show sem contrato."
  python3 hookscore_pt.py ganchos.txt --json
"""

import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hookscore as h  # noqa: E402


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def with_unaccented(items):
    # People type "voce" and "nao" as often as "você" and "não".
    out = set(items)
    out |= {strip_accents(x) for x in items}
    return out


LETTERS = "A-Za-zÀ-ÖØ-öø-ÿ"
h.WORD_RE = re.compile(rf"R\$|[{LETTERS}0-9$%'’-]+")

h.NUMBER_RE = re.compile(
    r"R?\$\s?\d[\d.,]*"                                   # R$ 18.000 / $4,200
    r"|\b\d[\d.,]*\s?"
    r"(?:%|k\b|x\b|mil\b|hrs?\b|hours?\b|horas?\b|h\b|mins?\b|minutes?\b"
    r"|minutos?\b|days?\b|dias?\b|weeks?\b|semanas?\b|months?\b|m[eê]s\b"
    r"|meses\b|years?\b|anos?\b)?",
    re.IGNORECASE)

h.PROPER_RE = re.compile(r"(?<!^)\b[A-ZÀ-ÖØ-Þ][a-zß-öø-ÿ]{2,}\b")

h.SPOKEN_NUMBERS |= with_unaccented({
    "zero", "dois", "duas", "três", "quatro", "cinco", "seis", "sete", "oito",
    "nove", "dez", "onze", "doze", "quinze", "vinte", "trinta", "quarenta",
    "cinquenta", "sessenta", "setenta", "oitenta", "noventa", "cem", "cento",
    "duzentos", "trezentos", "quinhentos", "mil", "milhão", "milhões",
    "bilhão", "dúzia", "metade", "dobro", "triplo",
})

h.MONEY_WORDS |= with_unaccented({
    "reais", "conto", "contos", "pila", "cachê", "cachês", "faturamento",
    "faturei", "faturou", "lucro", "salário", "aluguel", "bilheteria",
    "ingresso", "ingressos",
})

# "para" is left out on purpose: it is the everyday preposition "for" far more
# often than the imperative "stop". "pare" carries the imperative.
h.STAKES |= with_unaccented({
    "pare", "nunca", "errado", "errada", "erro", "erros", "errei", "perdi",
    "perde", "perder", "perdendo", "perdeu", "prejuízo", "custa", "custou",
    "custo", "caro", "cara", "quebrei", "quebrou", "faliu", "falhou", "falha",
    "ninguém", "não", "nem", "desisti", "demitido", "demiti", "apaguei",
    "cortei", "grátis", "paguei", "pago", "cobrei", "cobrou", "contratei",
    "economizei", "primeiro", "primeira", "proibido", "ilegal", "pior",
    "odeio", "desperdicei", "golpe", "calote", "mentira", "mentiu", "verdade",
    "segredo", "escondido", "roubou", "roubado", "antes", "até", "mas",
    "exceto", "problema", "risco", "perigo", "cuidado", "arrependo",
    "arrependimento", "devia", "deveria", "ainda", "já", "só", "sem", "contra",
    "cancelado", "cancelou", "furou", "atrasou", "multa", "processo", "vazio",
    "lotado", "esgotado", "flopou",
})

h.IMPERATIVES |= with_unaccented({
    "pare", "para", "rouba", "roube", "copia", "copie", "apaga", "apague",
    "tenta", "tente", "assiste", "assista", "lê", "leia", "salva", "salve",
    "usa", "use", "monta", "monte", "faz", "faça", "escreve", "escreva",
    "manda", "mande", "pega", "pegue", "começa", "comece", "nunca", "sempre",
    "não", "cobra", "cobre", "evita", "evite", "guarda", "guarde", "testa",
    "teste", "confere", "confira",
})

h.WEAK_OPENERS += [strip_accents(x) for x in [
    "então", "bom", "oi", "olá", "gente", "galera", "fala", "e aí", "eaí",
    "hoje", "basicamente", "sinceramente", "olha", "vamos", "bora", "nesse",
    "neste", "no vídeo", "você sabia", "sabia que", "já pensou", "tem gente",
    "existe", "isso é", "é que", "como um", "como uma", "quando", "se você",
    "sabe", "tipo", "assim",
]]
# check_frontload compares lowercase words that keep their accents, so keep
# the accented spelling too.
h.WEAK_OPENERS += ["então", "olá", "e aí", "eaí", "no vídeo", "você sabia",
                   "já pensou", "isso é", "é que", "se você"]

h.DEALBREAKERS += [
    (re.compile(r"(?i)^\s*(?:para de rolar|pare de rolar|não rola|nao rola)"),
     "Abre com \"para de rolar\". Pedir atenção prova que você ainda não ganhou."),
    (re.compile(r"(?i)\b(?:n[eo]ss?e v[ií]deo|no v[ií]deo de hoje|vou te mostrar|"
                r"vou mostrar|hoje eu vou)\b"),
     "Preâmbulo de vídeo. Corta e abre direto no que interessa."),
    (re.compile(r"(?i)^\s*(?:oi[ ,]|ol[áa][ ,]|fala (?:galera|gente|pessoal)|"
                r"e a[íi][ ,]|bom dia|boa tarde|boa noite)"),
     "Cumprimento. Ninguém abriu o feed pra ser cumprimentado."),
]

_words_en = h.words


def words(text):
    # "R$ 18.000" and "18.000" are one spoken number, as "$18,000" is.
    text = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", text)
    text = re.sub(r"R\$\s+(?=\d)", "R$", text)
    return _words_en(text)


h.words = words

_VIEWER = r"\b(you|your|you're|youre|yourself|voc[êe]s?|seus?|suas?|te|tu|contigo)\b"
_FIRST = r"\b(i|my|me|we|our|eu|meus?|minhas?|n[óo]s|nossos?|nossas?|a gente|comigo)\b"
_FIRST_VERBS = with_unaccented({
    "perdi", "vendi", "aprendi", "descobri", "percebi", "decidi", "consegui",
    "desisti", "fiz", "tive", "fui", "sou", "estou", "tô", "tava", "tenho",
    "faço", "vendo", "cobro", "pago", "perco", "sei", "vi", "abri", "sofri",
})


def check_address(text):
    """Aimed at one viewer, or floating in the air."""
    low = text.lower()
    w = [x.lower().strip("'’") for x in words(text)]
    if re.search(_VIEWER, low):
        return 100.0, "speaks to the viewer"
    if w and w[0] in h.IMPERATIVES:
        return 90.0, f"imperative opener (\"{w[0]}\")"
    if re.search(_FIRST, low):
        return 70.0, "first person, no viewer named"
    # Portuguese drops the pronoun: "Perdi R$ 18 mil" is first person with no
    # "eu" in it. A past-tense -ei verb or a common irregular gives it away.
    if any(x in _FIRST_VERBS or (len(x) > 4 and x.endswith("ei")) for x in w):
        return 70.0, "first person (verb), no viewer named"
    return 35.0, "third person, nobody in the room"


h.check_address = check_address


def check_stakes(text):
    """Tension, cost, negation. Something the viewer might lose."""
    w = [x.lower().strip("'’") for x in words(text)]
    markers = sorted({x for x in w if x in h.STAKES})
    if re.search(r"R?\$\s?\d", text):
        markers.append("a price")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} tension marker(s)" + (f": {', '.join(markers[:4])}" if markers else
                                         " - nothing is at stake in this line")
    return score, detail


h.check_stakes = check_stakes


if __name__ == "__main__":
    h.main()
