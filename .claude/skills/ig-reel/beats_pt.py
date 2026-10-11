#!/usr/bin/env python3
"""
beats_pt.py - beats.py for a Portuguese script. Same timings, same flags,
same thresholds.

What beats.py gets wrong in Portuguese, and this fixes:
  - words: its word pattern is [A-Za-z], so "não" is two words ("n", "o") and
    "começa" is two. Every accented word adds time that is not there, so the
    hook looks longer than it is and the total runs long.
  - concrete: "R$ 18.000", "18 mil" and accented names ("Simão") count.
  - loop: Portuguese stopwords ("de", "que", "você") are not counted as the
    word that ties the last line back to the hook.

Portuguese is usually spoken faster than English. Time yourself reading a
script out loud and pass --wpm (180 is a reasonable start).

Usage
  python3 beats_pt.py roteiro.txt --target 30 --wpm 180
  python3 beats_pt.py roteiro.txt --json
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats as b  # noqa: E402

LETTERS = "A-Za-zÀ-ÖØ-öø-ÿ"
b.WORD_RE = re.compile(rf"R\$|[{LETTERS}0-9$%'’-]+")
b.CONCRETE_RE = re.compile(
    r"R?\$\s?\d|\b\d[\d,.]*\b|(?<!^)\b[A-ZÀ-ÖØ-Þ][a-zß-öø-ÿ]{2,}\b", re.MULTILINE)

b.STOPWORDS |= {
    "o", "a", "os", "as", "um", "uma", "uns", "umas", "e", "ou", "mas", "se",
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "por",
    "pra", "pro", "para", "com", "sem", "que", "isso", "isto", "esse", "essa",
    "este", "esta", "aquele", "aquela", "é", "são", "foi", "era", "ser",
    "estar", "tá", "está", "você", "voce", "vocês", "voces", "seu", "sua",
    "te", "eu", "meu", "minha", "me", "nós", "nos", "a gente", "gente", "ele",
    "ela", "eles", "elas", "lhe", "só", "não", "nao", "já", "ja", "tem",
    "ter", "vai", "vou", "faz", "fazer", "como", "quando", "mais", "muito",
    "também", "tambem", "aqui", "lá", "então", "entao", "ao", "à", "às",
    "r$",
}


def pretty(token):
    """Brazilian thousands separator for display: 18000 -> 18.000."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token)


b.pretty = pretty

_words_en = b.words


def words(text):
    # "R$ 18.000" and "18.000" are one spoken number, as "$18,000" is.
    text = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", text)
    text = re.sub(r"R\$\s+(?=\d)", "R$", text)
    return _words_en(text)


b.words = words

if __name__ == "__main__":
    b.main()
