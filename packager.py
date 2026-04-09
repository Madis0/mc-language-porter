import shutil
import json
import requests

packFolder = "Eesti keele pakk/"
extraFile = "extra-et_EE.lang"

langFolder = "texts/"
langFile = "et_EE.lang"

manifest = "pack_manifest.json"
packName = "eesti"
packExt = ".mcpack"

# Obtains the version number from resource file (e.g. "v1.26.20.26") and uses first two numbers as a prefix (e.g "26.20.x")
# Also updates the min_engine_version as suggested by MC wiki
useVersionAsPrefix = True
versionUrl = "https://api.github.com/repos/Mojang/bedrock-samples/releases/latest"
versionHeaders = {"Accept": "application/vnd.github+json"}

print("Copying language file to pack folder...")
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
        versionPrefix = request.json().get("tag_name", "")[3:] # "v1.26.20.26" -> "26.20.26"

        if versionPrefix in '.'.join(map(str, manifestVersion)):
            manifestVersion[2] = manifestVersion[2] + 1  # Append 1 to version's last number
        else:
            manifestVersion[0] = int(versionPrefix.split(".")[0])
            manifestVersion[1] = int(versionPrefix.split(".")[1])
            manifestVersion[2] = 1  # Create new version number

            manifestEngine[0] = 1   # Hardcoded
            manifestEngine[1] = int(versionPrefix.split(".")[0])
            manifestEngine[2] = int(versionPrefix.split(".")[1])
            print("New minor version " + versionPrefix + "!")

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
