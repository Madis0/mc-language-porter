import json
import sys

# Whether to include strings from main and Realms in mappings (don't disable both, though)
includeJe = True
includeRealms = False
includeExtraMappings = True  # Whether to use user-provided extra mappings
includeExtraTranslations = True  # Whether to use user-provided extra translated phrases

jeLangs = ["et_ee", "vro"]   # Java Edition language codes (lowercase used for json filenames)
beLangs = ["et_EE", "vro_EE"]   # Bedrock Edition language codes (used for .lang filenames)

# File names and -paths
mapPath = "mappings.csv"
extraMapPath = "extra-" + mapPath

# Expect exactly two separate arguments when provided:
# python script.py "et_ee,fr_fr" "et_EE,fr_FR"
if len(sys.argv) > 2:
    jeLangs = [l.strip() for l in sys.argv[1].split(",") if l.strip()]
    beLangs = [l.strip() for l in sys.argv[2].split(",") if l.strip()]

# Arrays to store data in (temporarily)
mapDict = {}

# Parsing functions

def parse_json(path, toDict):
    file = open(path, 'r', encoding='utf-8')
    parsed_json = json.load(file)

    for key, value in parsed_json.items():
        toDict[key] = value

    file.close()

def parse_csv(path, toDict):
    file = open(path, 'r', encoding='utf-8')

    for row in file:
        if row.strip() != "":
            key1, key2 = row.strip().split(",")
            toDict[key1] = key2

    file.close()

def parse_lang(path, toDict):
    file = open(path, 'r', encoding='utf-8')

    for row in file:
        if not row.startswith("##"):
            try:
                # Splitting on the first equals sign only
                parts = row.split("=", 1)
                if len(parts) == 2:
                    key, value = parts
                    toDict[key.strip()] = value.rstrip('\n')  # Preserving trailing spaces, removing only newline
            except:  # Parse the key even when value is None
                pass
    file.close()

# Load mappings once
print("Opening mapped strings...")
parse_csv(mapPath, mapDict)

if includeExtraMappings:
    print("Opening extra mapped strings...")
    parse_csv(extraMapPath, mapDict)

# Require exact pair counts
if len(jeLangs) != len(beLangs):
    print("Error: JE and BE language lists must have the same number of entries. Cancelling.")
    sys.exit(1)

# Process each paired JE/BE language by index
for i in range(len(jeLangs)):
    jeLang = jeLangs[i]
    beLang = beLangs[i]

    jePath = jeLang + ".json"
    realmsPath = "realms-" + jePath

    jeDict = {}
    if includeJe:
        print("Opening Java Edition strings for " + jeLang + "...")
        parse_json(jePath, jeDict)

    if includeRealms:
        print("Opening Realms strings for " + jeLang + "...")
        parse_json(realmsPath, jeDict)

    bePath = beLang + ".lang"
    extraLangPath = "extra-" + bePath
    extraLangDict = {}

    if includeExtraTranslations:
        print("Opening extra translations for " + beLang + "...")
        parse_lang(extraLangPath, extraLangDict)

    print("Writing to " + bePath + "...")
    beFile = open(bePath, 'w', encoding='utf-8')

    for beKey, jeKey in mapDict.items():
        try:
            beFile.write(beKey + "=" + jeDict[jeKey] + "\n")
        except:
            pass

    if includeExtraTranslations:
        for key, value in extraLangDict.items():
            try:
                beFile.write(key + "=" + value + "\n")
            except:
                pass

    beFile.close()
    print("Matching translations have been ported to Bedrock Edition in file " + bePath + ".")
