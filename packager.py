import shutil
import json
import requests
import re

packFolder = "Eesti keele pakk/"
extraFile = "extra-et_EE.lang"

langFolder = "texts/"
langFile = "et_EE.lang"

manifest = "pack_manifest.json"
packName = "eesti"
packExt = ".mcpack"

# Obtains the version number from resource file (e.g. 1.13.0.1) and uses first two numbers as a prefix (e.g 1.13.x)
# Also updates the min_engine_version as suggested by MC wiki
useVersionAsPrefix = True
versionUrl = "https://aka.ms/MinecraftBetaResources"
versionRegex = "(\d+\.\d+)\.\d+\.\d+"

print("Copying language file to pack folder...")
shutil.copyfile(langFile, packFolder + langFolder + langFile)


# Increase version number by one in manifest
def iterate_manifest(manifestFile):
    lines = open(manifestFile, 'r', encoding="utf-8")
    manifestJson = json.load(lines)
    manifestVersion = manifestJson["header"]["packs_version"]
    manifestEngine = manifestJson["header"]["min_engine_version"]

    if useVersionAsPrefix:
        request = requests.head(versionUrl, allow_redirects=True)
        versionPrefix = re.findall(versionRegex, request.url)[0]

        if versionPrefix in '.'.join(map(str, manifestVersion)):
            manifestVersion[2] = manifestVersion[2] + 1  # Append 1 to version's last number
        else:
            manifestVersion[0] = int(versionPrefix.split(".")[0])
            manifestVersion[1] = int(versionPrefix.split(".")[1])
            manifestVersion[2] = 1  # Create new version number

            manifestEngine[0] = int(versionPrefix.split(".")[0])
            manifestEngine[1] = int(versionPrefix.split(".")[1])
            print("New major version " + versionPrefix + "!")

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
