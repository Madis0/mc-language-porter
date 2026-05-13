import shutil
import json
import requests
import sys

packFolder = "Eesti keelte pakk/"

langFolder = "texts/"
languages = ["et_EE", "vro_EE"]

manifest = "pack_manifest.json"
packName = "eesti"
packExt = ".mcpack"

# Obtains the latest pre-release version number from resource file (e.g. "v1.26.20.26") and uses first two numbers as a prefix (e.g "26.20.x")
# Also updates the min_engine_version as suggested by MC wiki
useVersionAsPrefix = True
versionUrl = "https://api.github.com/repos/Mojang/bedrock-samples/releases"
versionHeaders = {"Accept": "application/vnd.github+json"}

# Accept an array of languages from command-line arguments
if len(sys.argv) > 1:
    languages = [arg for arg in sys.argv[1:]]

# Generate langFiles and extraFiles from languages
langFiles = [lang + ".lang" for lang in languages]
extraFiles = ["extra-" + lang + ".lang" for lang in languages]

print("Copying language file(s) to pack folder...")
for langFile in langFiles:
    shutil.copyfile(langFile, packFolder + langFolder + langFile)

# Increase version number by one in manifest
def iterate_manifest(manifestFile):
    lines = open(manifestFile, 'r', encoding="utf-8")
    manifestJson = json.load(lines)
    manifestVersion = manifestJson["header"]["version"]
    manifestEngine = manifestJson["header"]["min_engine_version"]

    if useVersionAsPrefix:
        request = requests.get(versionUrl, headers=versionHeaders, timeout=10)
        request.raise_for_status()
        data = request.json()
        tag = next((r.get("tag_name") for r in data if r.get("prerelease") is True), None)
        versionNumber = (tag or "")[3:-8]  # "v1.26.30.28-preview" -> "26.30.28"
        versionPrefix = '.'.join(versionNumber.split('.')[:2]) # "26.30" but also works if more digits e.g. "26.120"

        if versionPrefix == '.'.join(map(str, manifestVersion[:2])):
            manifestVersion[2] += 1 # Append 1 to version's last number
        else:
            manifestVersion[0] = int(versionNumber.split(".")[0])
            manifestVersion[1] = int(versionNumber.split(".")[1])
            manifestVersion[2] = 1  # Create new version number

            manifestEngine[0] = 1   # Hardcoded
            manifestEngine[1] = int(versionNumber.split(".")[0])
            manifestEngine[2] = int(versionNumber.split(".")[1]) - 10 # Allow both latest stable and preview
            print("New minor version " + versionNumber + "!")

    else:
        manifestVersion[2] = manifestVersion[2] + 1  # Append 1 to version's last number

    print("Pack's version is now " + '.'.join(map(str, manifestVersion)) + ".")

    with open(manifestFile, 'w') as outfile:
        json.dump(manifestJson, outfile)


print("Increasing manifest version...")
iterate_manifest(packFolder + manifest)

print("Packaging files to a ZIP...")
shutil.make_archive(packName, 'zip', packFolder)

print("Renaming ZIP to MCPack...")
shutil.move(packName + ".zip", packName + packExt)
print("The pack is ready!")
