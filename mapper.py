import difflib
import json

# Whether to include strings from main and Realms in mappings (don't disable both, though)
includeJe = True
includeRealms = True

# File names and -paths
jePath = "en_us.json"
bePath = "en_US.lang"
realmsPath = "realms-" + jePath
outputPath = "mappings.csv"

# Arrays to store data in (temporarily)
jeDict = {}
beDict = {}
mappings = []
oldPercent = -1


# Parsing functions

def parse_json(path, toDict):
    file = open(path, 'r', encoding='utf-8')
    parsed_json = json.load(file)

    for key, value in parsed_json.items():
        toDict[key] = value

    file.close()


def parse_lang(path, toDict):
    file = open(path, 'r', encoding='utf-8')

    for row in file:
        if not row.strip().startswith("##"):
            try:
                key, value = row.strip().split("=")
                toDict[key] = value
            except:  # Parse the key even when value is None
                pass

    file.close()


# Show status in percents
def count_percent(index, total):
    global oldPercent
    percent = (index * 100) // total
    if oldPercent != percent:
        print(f"Progress: {percent}%")
        oldPercent = percent


# Importing files

if includeJe:
    print("Opening Java Edition strings...")
    parse_json(jePath, jeDict)

if includeRealms:
    print("Opening Realms strings...")
    parse_json(realmsPath, jeDict)

print("Opening Bedrock Edition strings..")
parse_lang(bePath, beDict)

# Iterate over beList to find matches in jeList
print("Finding equivalent keys...")
for beKey, beValue in enumerate(list(beDict.values())):

    count_percent(beKey, len(beDict))

    # Append matches per-string to variable valueMatchingKeys
    valueMatchingKeys = []
    for jeKey, jeValue in enumerate(list(jeDict.values())):
        if beValue == jeValue:  # Identical match
            valueMatchingKeys.append(list(jeDict.keys())[jeKey])

    # If there are multiple key matches, use the best one (minimum 10% similarity)
    if len(valueMatchingKeys) > 1:
        firstBestMatchingKey = difflib.get_close_matches(list(beDict.keys())[beKey], valueMatchingKeys, 1, 0.1)
        if len(firstBestMatchingKey) > 0:
            mappings.append((list(beDict.keys())[beKey], firstBestMatchingKey[0]))
        # If there are no similar keys, just use the first one (randomly)
        else:
            mappings.append((list(beDict.keys())[beKey], valueMatchingKeys[0]))

    # If there is only one key match, use it (regardless of context)
    elif len(valueMatchingKeys) == 1:
        mappings.append((list(beDict.keys())[beKey], valueMatchingKeys[0]))

# Write to file mappings.csv
print("Writing to " + outputPath + "...")
mapFile = open(outputPath, 'w', encoding='utf-8')

for beKey, jeKey in mappings:
    mapFile.write(beKey + "," + jeKey + "\n")

mapFile.close()
print("Identical strings have been written to " + outputPath + ".")
