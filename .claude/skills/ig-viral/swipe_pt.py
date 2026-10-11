#!/usr/bin/env python3
"""
swipe_pt.py - swipe.py for reels collected in Portuguese. Same ranking (views
over the account's own median), same report, same swipe.md.

What swipe.py gets wrong in Portuguese, and this fixes:
  - formulas: the 26 patterns in hooks.json are English, so a Portuguese hook
    lands in "unclassified" almost every time. Each formula gets a Portuguese
    pattern here, tried after the English one.
  - hook score: uses hookscore_pt.py instead of hookscore.py.
  - numbers: the Brazilian app shows "412 mil", "1,2 mi" and "48,5 mil".
    swipe.py strips everything but digits, so "1,2 mi" becomes 12 views.
  - columns: a header in Portuguese works too (conta, seguidores, mediana,
    views / visualizações, gancho).
  - hook length: accented words count as one word.

Input is the same tab-separated file:

    conta     seguidores   mediana   views     gancho
    @alguem   48 mil       11 mil    412 mil   ninguém te conta que os 30 primeiros flopam

Usage
  python3 swipe_pt.py coleta.tsv
  python3 swipe_pt.py coleta.tsv --out ~/.claude/instagram/swipe.md
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import swipe as s  # noqa: E402

try:
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore_pt import h as _hs_pt  # noqa: E402  (patched hookscore)
    s.score_hook = _hs_pt.run
except Exception:
    pass

s.WORD_RE = re.compile(r"R\$|[A-Za-zÀ-ÖØ-öø-ÿ0-9$%'’-]+")

M = r"(?:R?\$\s?\d|\d[\d.,]*\s?mil\b|\breais\b|\bconto?s?\b)"
PT = {
    1: rf"\bcust(?:ou|a)\s+(?:me|pra mim|caro)\b|\bme custou\b|\bperdi\b[^.!?]{{0,25}}{M}|{M}[^.!?]{{0,20}}\bfoi o que\b",
    2: r"^\s*(?:para|pare|nunca|não|nao|chega de|larga)\b|\b(?:não|nao|nunca) (?:faça|faz|compre|use|comece|poste|mande|cobre)\b",
    3: r"\b(?:ninguém|ninguem)\s+(?:nunca\s+)?(?:te\s+|me\s+)?(?:conta|contou|fala|falou|diz|disse|ensina|ensinou|avisa|avisou)\b",
    4: rf"\bsubstitu(?:i|iu|ir|ímos|imos)\b|\bem vez de (?:pagar|contratar)\b|\bno lugar de (?:pagar|contratar)\b",
    5: r"\b(?:levava|demorava|gastava)\b[^.!?]{0,30}\b(?:horas?|dias?|semanas?)\b|\bagora (?:leva|são|é|demora)\b|\bleva(?:va)?\s+\d+\s*(?:seg|min|h)",
    6: rf"\b(?:fiz|faturei|vendi|postei|testei)\b[^.!?]{{0,30}}\b(?:por|durante|em)\s+\d+\s+(?:dias?|semanas?|meses|anos?)\b|\b(?:aqui estão|olha) os números\b",
    7: r"\b(?:maior|o) erro\b|\berro (?:que|comum)\b|\bvocê (?:tá|está) fazendo\b[^.!?]*\berrado\b|\bfazendo (?:isso )?errado\b",
    8: r"\b(?:trabalhei|passei|fui)\b[^.!?]*\b\d+\s*\+?\s*anos?\b|\bnunca (?:te )?(?:contamos|falamos|mostramos)\b|\bos bastidores\b",
    9: r"^\s*(?:rouba|roube|copia|copie)\b|\b(?:rouba|copia) (?:isso|esse|essa|meu|minha)\b|^\s*(?:aqui está|esse é) (?:o|meu|minha) (?:exato|modelo|roteiro)\b",
    10: r"^\s*se (?:você|voce|vc|eu|a gente|seu|sua|tu)\b",
    11: r"^\s*\d+\s+\w+|\bnúmero \d+\b|\b(?:três|tres|quatro|cinco|sete|dez)\s+\w+\s+(?:que|pra|para)\b",
    12: r"^\s*[\"“'][^\"”']{5,120}[\"”'][,.]?\s*(?:beleza|ok|tá|ta|certo|então)",
    13: r"\b(?:antes|isso era)\b[^.!?]*\b(?:depois|agora é)\b",
    14: r"^\s*(?:todo|toda|todos|todas|qualquer)\s+\w+|^\s*(?:se você é|pra quem|para quem|atenção)\b|^\s*\w+(?:eiros?|eiras?|istas?|ores|oras)\b\s*[,:]",
    15: r"\b(?:meus?|minhas?) primeir[oa]s?\s+\d+\b|\bprimeir[oa]s\s+\d+\s+(?:reels?|vídeos?|videos?|posts?|clientes?|shows?|meses)\b",
    16: r"^\s*[\"“']?(?:como|o que|por que|porque|quando|onde|quem|qual|quanto|quanta|dá pra|vale a pena|você já|vc já|tem como)\b[^?]{3,110}\?",
    17: r"\b(?:vs\.?|versus|ou)\b[^.!?]{0,30}\?|\bdiferença entre\b|\bqual (?:é )?melhor\b",
    18: r"^\s*(?:olha|veja|assiste) (?:isso|o que|só)\b|^\s*(?:deixa eu|vou) te mostrar\b|^\s*repete comigo\b",
    19: r"\bantes (?:que|de)\b[^.!?]*\b(?:mude|acabe|feche|expire|suba|esgote)\b|\baté (?:dia|sexta|domingo|amanhã)\b|\baté 20\d\d\b",
    20: r"\b(?:você|voce|vc) não precisa\b|\bpara de (?:tentar|se preocupar)\b",
    21: r"^\s*(?:\.\.\.|…)|^\s*(?:e (?:foi aí|aí) que|então (?:ele|ela) (?:disse|falou|perguntou))\b|^\s*(?:é|hã|tipo)\b",
    22: r"^\s*[A-Za-zÀ-ÿ][\wÀ-ÿ' ]{2,34}\b(?:é|são|está|tá)\s+(?:morto|morta|errado|errada|superestimad[oa]|subestimad[oa]|melhor|pior)\b",
    23: r"^\s*\d[\d,.]*\s?%|\b\d[\d,.]*\s?%\s+d[oa]s?\b",
    24: r"^\s*(?:então,?\s+)?(?:esse|essa|esses|essas|aqui)\s+(?:é|são)\s+(?:o|a|os|as|meu|minha)?\s*(?:nov[oa]s?)\b|^\s*(?:essa|esse) (?:pequen[oa]|nov[oa])\b",
    25: r"\b(?:tinha|tem) (?:um|uma) (?:cara|menina|cliente|aluno|aluna|amigo|amiga|artista|produtor)\b|\b(?:um|uma) (?:cliente|aluno|aluna|amigo|amiga|artista) (?:meu|minha|que)\b",
    26: r"^\s*(?:o|a)?\s*(?:jeito mais|forma mais|maneira mais)\s+\w+|\b(?:o|a) (?:melhor|pior|maior|único|única) (?:jeito|forma|maneira|erro|segredo)\b|^\s*(?:o|a) (?:mais rápid[oa]|mais fácil|melhor|pior|maior)\b",
}

_load_en = s.load_formulas


def load_formulas(path):
    formulas = _load_en(path)
    if not formulas:
        return formulas
    out = []
    for fid, name, en in formulas:
        if fid in PT:
            pattern = re.compile(f"(?:{en.pattern})|(?:{PT[fid]})", re.IGNORECASE)
        else:
            pattern = en
        out.append((fid, name, pattern))
    return out


s.load_formulas = load_formulas

ALIASES = {
    "conta": "account", "perfil": "account", "seguidores": "followers",
    "mediana": "median", "visualizações": "views", "visualizacoes": "views",
    "views": "views", "plays": "views", "reproduções": "views",
    "gancho": "hook", "hook": "hook",
}


def to_int(cell):
    """'412 mil' -> 412000, '1,2 mi' -> 1200000, '48.500' -> 48500, '12k' -> 12000."""
    t = (cell or "").strip().lower().replace(" ", "")
    if not t:
        return None
    m = re.match(r"^([\d.,]+)(mil|k|mi|mm|m|milhões|milhão|milhoes|milhao|bi)?$", t)
    if not m:
        digits = re.sub(r"[^\d]", "", t)
        return int(digits) if digits else None
    num, unit = m.group(1), m.group(2)
    mult = {"mil": 1e3, "k": 1e3, "mi": 1e6, "mm": 1e6, "m": 1e6, "milhões": 1e6,
            "milhão": 1e6, "milhoes": 1e6, "milhao": 1e6, "bi": 1e9}.get(unit, 1)
    if unit:
        value = float(num.replace(".", "").replace(",", ".")) if "," in num else float(num)
    else:
        value = float(re.sub(r"[.,]", "", num))   # 48.500 / 48,500 -> 48500
    return int(round(value * mult))


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [ALIASES.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [x.strip() for x in cells]))
        r["views"] = to_int(r.get("views")) or 0
        for k in ("followers", "median"):
            r[k] = to_int(r.get(k))
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


s.read_rows = read_rows

if __name__ == "__main__":
    s.main()
