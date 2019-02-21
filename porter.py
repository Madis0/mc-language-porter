import json

# File names and -paths
import sys

# Whether to include strings from main and Realms in mappings (don't disable both, though)
includeJe = True
includeRealms = True
includeExtraMap = True  # Whether to use user-provided extra mappings
translationLang = "et_EE"  # Used when launched without arguments

# File names and -paths
jePath = translationLang.lower() + ".json"
realmsPath = "realms-" + jePath
bePath = translationLang + ".lang"
mapPath = "mappings.csv"
extraMapPath = "extra-" + mapPath

if len(sys.argv) > 1:  # Use the language provided as an argument if available
    translationLang = sys.argv[1]

# Arrays to store data in (temporarily)
jeDict = {}
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
        key1, key2 = row.strip().split(",")
        toDict[key1] = key2

    file.close()


# Importing files

if includeJe:
    print("Opening Java Edition strings...")
    parse_json(jePath, jeDict)

if includeRealms:
    print("Opening Realms strings...")
    parse_json(realmsPath, jeDict)

print("Opening mapped strings..")
parse_csv(mapPath, mapDict)

if includeExtraMap:
    print("Opening extra mapped strings..")
    parse_csv(extraMapPath, mapDict)

# Write to translation file
print("Writing to " + bePath + "...")
beFile = open(bePath, 'w', encoding='utf-8')

for beKey, jeKey in mapDict.items():
    try:  # Skip lines that don't have a translation
        beFile.write(beKey + "=" + jeDict[jeKey] + "\n")
    except:
        pass

beFile.close()
print("Matching translations have been ported to Bedrock Edition in file " + bePath + ".")
