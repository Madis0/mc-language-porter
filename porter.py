import csv
import json
import re
import sys
from pathlib import Path


inputPath = Path("Input")
outputPath = Path("Output")
outputPath.mkdir(exist_ok=True)

jeLangs = [
    "bg_bg", "cs_cz", "da_dk", "de_de", "el_gr", "en_gb", "en_us",
    "es_es", "es_mx", "et_ee", "fi_fi", "fr_ca", "fr_fr", "hu_hu",
    "id_id", "it_it", "ja_jp", "ko_kr", "no_no", "nl_nl", "pl_pl",
    "pt_br", "pt_pt", "ru_ru", "sk_sk", "sv_se", "tr_tr", "uk_ua",
    "zh_cn", "zh_tw",
]
beLangs = [
    "bg_BG", "cs_CZ", "da_DK", "de_DE", "el_GR", "en_GB", "en_US",
    "es_ES", "es_MX", "et_EE", "fi_FI", "fr_CA", "fr_FR", "hu_HU",
    "id_ID", "it_IT", "ja_JP", "ko_KR", "nb_NO", "nl_NL", "pl_PL",
    "pt_BR", "pt_PT", "ru_RU", "sk_SK", "sv_SE", "tr_TR", "uk_UA",
    "zh_CN", "zh_TW",
]
if len(sys.argv) > 2:
    jeLangs = [lang.strip() for lang in sys.argv[1].split(",") if lang.strip()]
    beLangs = [lang.strip() for lang in sys.argv[2].split(",") if lang.strip()]

if len(jeLangs) != len(beLangs):
    raise SystemExit("Java and Bedrock language lists must have the same number of entries.")

if jeLangs:
    languagePairs = list(zip(jeLangs, beLangs))
    for jeLang, beLang in languagePairs:
        if not (inputPath / (jeLang + ".json")).exists() or not (inputPath / (beLang + ".lang")).exists():
            raise SystemExit("Missing input file for language pair: " + jeLang + ", " + beLang)
else:
    languagePairs = []
    for beFile in sorted(inputPath.glob("*.lang")):
        jeLang = beFile.stem.lower()
        if (inputPath / (jeLang + ".json")).exists():
            languagePairs.append((jeLang, beFile.stem))
        else:
            print("No matching Java Edition language file for " + beFile.name)

mapDict = {}


def parse_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_unicode_escapes(paths):
    escapes = {}
    for path in paths:
        with open(path, "r", encoding="utf-8") as file:
            for code in re.findall(r"\\u([0-9a-fA-F]{4})", file.read()):
                escapes[chr(int(code, 16))] = code
    return escapes


def parse_csv(path, toDict):
    if not path.exists():
        return
    with open(path, "r", encoding="utf-8", newline="") as file:
        for row in csv.reader(file):
            if len(row) >= 2:
                toDict[row[0]] = row[1]


def parse_lang(path):
    parsed = {}
    with open(path, "r", encoding="utf-8") as file:
        for row in file:
            row = row.rstrip("\r\n")
            if row and not row.startswith("##") and "=" in row:
                key, value = row.split("=", 1)
                parsed[key.strip()] = value
    return parsed


print("Opening mapped strings...")
parse_csv(inputPath / "mappings.csv", mapDict)
parse_csv(inputPath / "extra-mappings.csv", mapDict)

extraEnglish = parse_json(inputPath / "extra-en_us.json")
overrides = parse_json(inputPath / "overrides.json")
prefixes = parse_json(inputPath / "prefixes.json")
unicodeEscapes = parse_unicode_escapes([
    inputPath / "extra-en_us.json",
    inputPath / "overrides.json",
    inputPath / "prefixes.json",
])

for jeLang, beLang in languagePairs:
    jeFile = inputPath / (jeLang + ".json")
    beFile = inputPath / (beLang + ".lang")
    jeDict = parse_json(jeFile)
    beDict = parse_lang(beFile)
    outputDict = {}

    for beKey, jeKey in mapDict.items():
        if beKey in beDict and jeKey in jeDict:
            outputDict[jeKey] = beDict[beKey]

    if jeLang == "en_us":
        outputDict.update(extraEnglish)

    for key, value in overrides.items():
        targetKey = key if key in jeDict or key in outputDict else mapDict.get(key, key)
        outputDict[targetKey] = value

    for key, prefix in prefixes.items():
        targetKey = key if key in outputDict else mapDict.get(key, key)
        if targetKey in outputDict:
            outputDict[targetKey] = prefix + outputDict[targetKey]

    outputDict = {
        key: value
        for key, value in outputDict.items()
        if value != jeDict.get(key)
    }

    outputFile = outputPath / (jeLang + ".json")
    with open(outputFile, "w", encoding="utf-8") as file:
        serialized = json.dumps(outputDict, ensure_ascii=False, indent=4)
        for character, code in unicodeEscapes.items():
            serialized = serialized.replace(character, "\\u" + code)
        file.write(serialized + "\n")
    print("Ported " + beLang + ".lang to " + outputFile.as_posix())