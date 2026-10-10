#!/usr/bin/env python3
"""Generate Estonian itemGroup.name.* plural translations from existing et_ee.json translations.

Requires: pip install estnltk
"""
import json
import re
from pathlib import Path

from estnltk import Text
from estnltk.vabamorf.morf import Vabamorf

VABAMORF = Vabamorf.instance()


# ---- Configuration -------------------------------------------------------
EN_LANG_FILE = "en_US.lang"
ET_JSON_FILE = "et_ee.json"
EXTRA_LANG_FILE = "extra-et_EE.lang"
GROUP_PREFIX = "itemGroup.name."
# Lookup order in the JSON file (item first, block as fallback)
JSON_KEY_PREFIXES = ("item.minecraft", "block.minecraft")
ENCODING = "utf-8"


# ---- File helpers --------------------------------------------------------
def read_lang_keys(path, prefix=""):
    """Return {key: value} for all 'key=value' lines whose key starts with prefix."""
    entries = {}
    file = Path(path)
    if not file.exists():
        return entries
    with file.open(encoding=ENCODING) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("#", "//")) or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if key.startswith(prefix):
                entries[key] = value.strip()
    return entries


def load_json(path):
    with open(path, encoding=ENCODING) as f:
        return json.load(f)  # dict keeps file order


def append_lines(path, lines):
    """Append lines to the file, making sure the existing content ends with a newline."""
    if not lines:
        return
    file = Path(path)
    needs_newline = False
    if file.exists() and file.stat().st_size > 0:
        with file.open("rb") as f:
            f.seek(-1, 2)
            needs_newline = f.read(1) != b"\n"
    with file.open("a", encoding=ENCODING, newline="\n") as f:
        if needs_newline:
            f.write("\n")
        f.write("\n".join(lines) + "\n")


# ---- JSON lookup ---------------------------------------------------------
def find_translation(translations, suffix):
    """Return the first translation whose key matches '<prefix>.(anything)_<suffix>'.

    Tries each prefix in JSON_KEY_PREFIXES in order (item first, then block).
    """
    for prefix in JSON_KEY_PREFIXES:
        # Accepts both "item.minecraft.acacia_boat" and "item.minecraft_acacia_boat"
        pattern = re.compile(rf"^{re.escape(prefix.split('.')[0])}\.minecraft[._].+_{re.escape(suffix)}$")
        for key, value in translations.items():
            if pattern.match(key) and isinstance(value, str) and value.strip():
                return value
    return None


# ---- Morphology (estnltk / vabamorf) -------------------------------------
def last_word(text):
    words = text.split()
    return words[-1] if words else ""


def last_compound(word):
    """Return (last compound part, part of speech) for a word using estnltk."""
    span = Text(word.lower()).tag_layer(["morph_analysis"]).morph_analysis[0]
    tokens = span.root_tokens[0]  # compound parts of the first analysis
    return tokens[-1], span.partofspeech[0]


def to_plural(lemma, pos="S"):
    """Nominative plural ('pl n') of a lemma, or None if synthesis fails."""
    forms = VABAMORF.synthesize(lemma, "pl n", pos)
    return forms[0] if forms else None


def capitalize_first(word):
    return word[:1].upper() + word[1:]


def make_group_translation(translation):
    """'Teemantkirka' -> 'Kirkad'; 'Akaatsiast paat' -> 'Paadid'."""
    word = last_word(translation)
    compound, pos = last_compound(word)
    plural = to_plural(compound, pos)
    return capitalize_first(plural) if plural else None


# ---- Main ----------------------------------------------------------------
def main():
    groups = read_lang_keys(EN_LANG_FILE, GROUP_PREFIX)
    existing = read_lang_keys(EXTRA_LANG_FILE, GROUP_PREFIX)
    translations = load_json(ET_JSON_FILE)

    new_lines, skipped = [], []
    for key in groups:
        if key in existing:
            continue
        suffix = key[len(GROUP_PREFIX):]
        source = find_translation(translations, suffix)
        if source is None:
            skipped.append((key, "no matching key in JSON"))
            continue
        result = make_group_translation(source)
        if result is None:
            skipped.append((key, f"could not pluralise '{source}'"))
            continue
        new_lines.append(f"{key}={result}")
        print(f"{key}={result}   (from '{source}')")

    append_lines(EXTRA_LANG_FILE, new_lines)

    print(f"\nAdded {len(new_lines)} line(s) to {EXTRA_LANG_FILE}.")
    for key, reason in skipped:
        print(f"Skipped {key}: {reason}")


if __name__ == "__main__":
    main()
