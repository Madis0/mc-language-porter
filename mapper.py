import difflib
import json

# Whether to include strings from the main Java Edition language file
includeJe = True
excludeKnownJe = True

# File names and -paths
jePath = "Input/en_us.json"
bePath = "Input/en_US.lang"
extraJePath = "Input/extra-en_us.json"
outputPath = "Input/mappings.csv"
excludeJePath = "exclude.txt"

# Arrays to store data in (temporarily)
jeDict = {}
beDict = {}
excludedKeys = set()
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
        row = row.rstrip('\r\n')
        if row and not row.startswith("##") and "=" in row:
            key, value = row.split("=", 1)
            toDict[key] = value

    file.close()


def parse_exclude(path, toSet):
    file = open(path, 'r', encoding='utf-8')

    for row in file:
        key = row.strip()
        if key:  # Only add non-empty lines
            toSet.add(key)

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

print("Opening extra English strings...")
parse_json(extraJePath, jeDict)

print("Opening Bedrock Edition strings..")
parse_lang(bePath, beDict)

if excludeKnownJe:
    print("Opening excluded keys...")
    parse_exclude(excludeJePath, excludedKeys)

# Iterate over beList to find matches in jeList
print("Finding equivalent keys...")
for beKey, beValue in enumerate(list(beDict.values())):

    count_percent(beKey, len(beDict))

    # Append matches per-string to variable valueMatchingKeys
    valueMatchingKeys = []
    for jeKey, jeValue in enumerate(list(jeDict.values())):
        # Check for identical match (including capitalization)
        if beValue == jeValue:
            valueMatchingKeys.append(list(jeDict.keys())[jeKey])
        # If no identical match found, check for case-insensitive match
        elif not valueMatchingKeys and beValue.lower() == jeValue.lower():
            valueMatchingKeys.append(list(jeDict.keys())[jeKey])

    # If there are multiple key matches, use the best one (minimum 10% similarity)
    if len(valueMatchingKeys) > 1:
        # Filter out excluded keys
        if excludeKnownJe:
            valueMatchingKeys = [key for key in valueMatchingKeys if key not in excludedKeys]
        
        if len(valueMatchingKeys) > 0:
            firstBestMatchingKey = difflib.get_close_matches(list(beDict.keys())[beKey], valueMatchingKeys, 1, 0.1)
            if len(firstBestMatchingKey) > 0:
                mappings.append((list(beDict.keys())[beKey], firstBestMatchingKey[0]))
            # If there are no similar keys, just use the first one (randomly)
            else:
                mappings.append((list(beDict.keys())[beKey], valueMatchingKeys[0]))

    # If there is only one key match, use it (regardless of context)
    elif len(valueMatchingKeys) == 1:
        if not excludeKnownJe or valueMatchingKeys[0] not in excludedKeys:
            mappings.append((list(beDict.keys())[beKey], valueMatchingKeys[0]))

# Write to file mappings.csv
print("Writing to " + outputPath + "...")
mapFile = open(outputPath, 'w', encoding='utf-8')

for beKey, jeKey in mappings:
    mapFile.write(beKey + "," + jeKey + "\n")

mapFile.close()
print("Identical strings have been written to " + outputPath + ".")
