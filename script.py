# Creates mappings for easier portability, does not port by itself
import json, difflib

# File names and -paths
jePath = input("File of the English Minecraft Java Edition language file (e.g. en_us.json): ")
bePath = input("File of the English Minecraft Bedrock language file (e.g. en_US.lang): ")
outputPath = "mappings.csv"

# Arrays to store data in (temporarily)
jeDict = {}
beDict = {}
mappings = []

# Open Java Edition strings
print("Opening Java Edition strings...")
jeFile = open(jePath, 'r', encoding='utf-8')
jeJson = json.load(jeFile)

# Send them to array jeList
for key, value in jeJson.items():
    jeDict[key] = value

jeFile.close()

# Open Bedrock Edition strings
print("Opening Bedrock Edition strings...")
beFile = open(bePath, 'r', encoding='utf-8')

# Send them to array beList
for row in beFile:
    if not row.strip().startswith("##"):
        try:
            key, value = row.strip().split("=")
            beDict[key] = value
        except:  # Parse the key even when value is None
            pass

beFile.close()

# Iterate over beList to find matches in jeList
oldPercent = -1
print("Finding equivalent keys...")
for beKey, beValue in enumerate(list(beDict.values())):

    # Show status in percents
    percent = (beKey * 100) // len(beDict)
    if oldPercent != percent:
        print(f"Progress: {percent}%")
        oldPercent = percent

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

    # If there is only one key match, use it
    elif len(valueMatchingKeys) == 1:
        mappings.append((list(beDict.keys())[beKey], valueMatchingKeys[0]))

# Write to file mappings.csv
print("Writing to " + outputPath + "...")
mapFile = open(outputPath, 'w', encoding='utf-8')

for beKey, jeKey in mappings:
    mapFile.write(beKey + "," + jeKey + "\n")

mapFile.close()
print("Identical strings have been written to " + outputPath + ".")
