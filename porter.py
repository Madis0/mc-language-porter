import json
import sys

# Whether to include strings from main and Realms in mappings (don't disable both, though)
includeJe = True
includeRealms = True
includeExtraMappings = True  # Whether to use user-provided extra mappings
includeExtraTranslations = False  # Whether to use user-provided extra translated phrases
translationLang = "et_EE"  # Used when launched without arguments

# File names and -paths
jePath = translationLang.lower() + ".json"
realmsPath = "realms-" + jePath
bePath = translationLang + ".lang"
mapPath = "mappings.csv"
extraMapPath = "extra-" + mapPath
extraLangPath = "extra-" + bePath

if len(sys.argv) > 1:  # Use the language provided as an argument if available
    translationLang = sys.argv[1]

# Arrays to store data in (temporarily)
jeDict = {}
mapDict = {}
extraLangDict = {}

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


# Importing files
if includeJe:
    print("Opening Java Edition strings...")
    parse_json(jePath, jeDict)

if includeRealms:
    print("Opening Realms strings...")
    parse_json(realmsPath, jeDict)

print("Opening mapped strings...")
parse_csv(mapPath, mapDict)

if includeExtraMappings:
    print("Opening extra mapped strings...")
    parse_csv(extraMapPath, mapDict)

if includeExtraTranslations:
    print("Opening extra translations...")
    parse_lang(extraLangPath, extraLangDict)

# Write to translation file
print("Writing to " + bePath + "...")
beFile = open(bePath, 'w', encoding='utf-8')

for beKey, jeKey in mapDict.items():
    try:  # Skip lines that don't have a translation
        beFile.write(beKey + "=" + jeDict[jeKey] + "\n")
    except:
        pass

if includeExtraTranslations:
    for key, value in extraLangDict.items():
        try:  # Skip lines that don't have a translation
            beFile.write(key + "=" + value + "\n")
        except:
            pass

beFile.close()
print("Matching translations have been ported to Bedrock Edition in file " + bePath + ".")
