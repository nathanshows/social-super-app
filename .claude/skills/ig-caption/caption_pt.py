#!/usr/bin/env python3
"""
caption_pt.py - caption.py for a Portuguese caption. Same eight checks, same
125-character window, same five-hashtag cap.

What caption.py gets wrong in Portuguese, and this fixes:
  - hashtags: its pattern is [A-Za-z0-9_], so "#clínicadeestética" is read as
    "#cl". Counting, placement and generic-tag checks all ran on the stub.
  - the one ask: "comenta PELE", "me chama no direct", "salva esse post",
    "link na bio", "me segue", "me conta" count as calls to action.
  - concrete: "R$ 150", "18 mil" and accented names count.
  - search terms: matched without accents and case, so "clinica de estetica"
    finds "Clínica de Estética" and the other way round.
  - links: ".com.br" counts as a dead link in the body.

Usage
  python3 caption_pt.py legenda.txt --keywords "clínica de estética,limpeza de pele"
  python3 caption_pt.py legenda.txt --json
"""

import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import caption as c  # noqa: E402


def fold(s):
    return "".join(ch for ch in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(ch) != "Mn")


c.HASHTAG_RE = re.compile(r"(?:^|\s)(#[\wÀ-ÖØ-öø-ÿ]+)")
c.CONCRETE_RE = re.compile(
    r"R?\$\s?\d|\b\d[\d,.]*\b|(?<!^)\b[A-ZÀ-ÖØ-Þ][a-zß-öø-ÿ]{2,}\b", re.MULTILINE)
c.LINK_RE = re.compile(
    r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app)(?:\.br)?(?:/\S*|\b)"
    r"|\b[a-z0-9-]+\.br\b", re.IGNORECASE)

c.ASKS = c.ASKS + [
    (re.compile(r"(?i)\bcoment[ae] (?:a palavra |\")?[A-ZÀ-Ý0-9]{2,}\b"), "comment a keyword"),
    (re.compile(r"(?i)\b(?:me chama|chama no|manda (?:um )?(?:direct|dm|mensagem)|"
                r"me manda (?:um )?(?:direct|dm|mensagem))\b"), "DM me"),
    (re.compile(r"(?i)\bsalv[ae] (?:esse|este|isso|o post|pra depois)\b"), "save this"),
    (re.compile(r"(?i)\b(?:compartilh[ae]|manda (?:pra|para) (?:alguém|quem|aquel))"), "share this"),
    (re.compile(r"(?i)\b(?:me segue|siga|segue (?:o perfil|a gente|@))"), "follow"),
    (re.compile(r"(?i)\blink (?:na|da) bio\b"), "link in bio"),
    (re.compile(r"(?i)\b(?:arrasta|deslize|arraste) (?:pro lado|para o lado|pra)?"), "swipe or tap"),
    (re.compile(r"(?i)\bme conta\b|\bme diz\b|\bqual (?:você|voce|vc)\b|\bcomenta aqui\b"),
     "answer a question"),
]

c.FILLER_TAGS |= {"#viralizar", "#explorar", "#reelsbrasil", "#instabrasil",
                  "#brasil", "#sigam", "#segue", "#curtir", "#tbt", "#fy"}

_analyse_en = c.analyse


def analyse(text, cut=c.TRUNCATE, keywords=None):
    a = _analyse_en(text, cut=cut, keywords=keywords)
    keywords = [k.strip() for k in (keywords or []) if k.strip()]
    if keywords:
        body, window = fold(text.strip()), fold(a["visible"])
        found = [k for k in keywords if fold(k) in body]
        missing = [k for k in keywords if fold(k) not in body]
        in_window = [k for k in found if fold(k) in window]
        status = "PASS" if not missing else ("WARN" if found else "FAIL")
        detail = (f"{len(found)}/{len(keywords)} present"
                  + (f", {len(in_window)} in the visible window" if found else "")
                  + (f". Missing: {', '.join(missing)}" if missing else ""))
        for chk in a["checks"]:
            if chk["check"] == "SEARCH TERMS":
                chk["status"], chk["detail"] = status, detail
    fails = sum(1 for x in a["checks"] if x["status"] == "FAIL")
    warns = sum(1 for x in a["checks"] if x["status"] == "WARN")
    a["verdict"] = "FIX" if fails else ("REVIEW" if warns else "READY")
    return a


c.analyse = analyse

if __name__ == "__main__":
    c.main()
