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
useVersionAsPrefix = True
versionUrl = "https://aka.ms/MinecraftBetaResources"
versionRegex = "(\d+\.\d+)\.\d+\.\d+"

print("Copying language file to pack folder...")
shutil.copyfile(langFile, packFolder + langFolder + langFile)


# Increase version number by one in manifest
def iterate_manifest(manifestFile):
    lines = open(manifestFile, 'r', encoding="utf-8")
    versionJson = json.load(lines)
    versionSegments = versionJson["header"]["packs_version"].split('.')

    if useVersionAsPrefix:
        request = requests.head(versionUrl, allow_redirects=True)
        versionPrefix = re.findall(versionRegex, request.url)[0]

        if versionPrefix in versionJson["header"]["packs_version"]:
            versionSegments[2] = str(int(versionSegments[2]) + 1)  # Append 1 to version's last number
            versionJson["header"]["packs_version"] = '.'.join(versionSegments)  # Merge it back
        else:
            versionJson["header"]["packs_version"] = versionPrefix + ".1"  # Create new version number
            print("New major version " + versionPrefix + "!")

    else:
        versionSegments[2] = str(int(versionSegments[2]) + 1)  # Append 1 to version's last number
        versionJson["header"]["packs_version"] = '.'.join(versionSegments)  # Merge it back

    print("Pack's version is now " + versionJson["header"]["packs_version"] + ".")

    with open(manifestFile, 'w') as outfile:
        json.dump(versionJson, outfile)


print("Increasing manifest version...")
iterate_manifest(packFolder + manifest)

print("Packaging files to a ZIP...")
shutil.make_archive(packName, 'zip', packFolder)

print("Renaming ZIP to MCPack...")
shutil.move(packName + ".zip", packName + packExt)
print("The pack is ready!")
