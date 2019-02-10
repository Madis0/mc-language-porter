# Creates mappings for easier portability, does not port by itself
import json

# File names and -paths
jePath = input("File of the input translated Minecraft Java Edition language (e.g. ru_ru.json): ")
bePath = input("File of the output bedrock Minecraft Bedrock language (e.g. ru_RU.lang): ")
mapPath = "mappings.csv"

# Arrays to store data in (temporarily)
jeDict = {}
mapDict = {}

# Open Java Edition strings
print("Opening Java Edition strings...")
jeFile = open(jePath, 'r', encoding='utf-8')
jeJson = json.load(jeFile)

# Send them to array jeList
for key, value in jeJson.items():
    jeDict[key] = value

jeFile.close()

# Open mapped strings
print("Opening mapped strings...")
mapFile = open(mapPath, 'r', encoding='utf-8')

# Send them to array beList
for row in mapFile:
    beKey, jeKey = row.strip().split(",")
    mapDict[beKey] = jeKey

mapFile.close()

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
