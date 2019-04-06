import shutil
import json

packFolder = "Eesti keele pakk/"
extraFile = "extra-et_EE.lang"

langFolder = "texts/"
langFile = "et_EE.lang"

manifest = "pack_manifest.json"
packName = "eesti"
packExt = ".mcpack"

print("Copying language file to pack folder...")
shutil.copyfile(langFile, packFolder + langFolder + langFile)


# Increase version number by one in manifest
def iterate_manifest(manifestFile):
    lines = open(manifestFile, 'r', encoding="utf-8")
    versionJson = json.load(lines)
    versionSegments = versionJson["header"]["packs_version"].split('.')  # Find the version segment, split it up
    versionSegments[2] = str(int(versionSegments[2]) + 1)  # Append 1 to version's last number
    versionJson["header"]["packs_version"] = '.'.join(versionSegments)  # Merge it back
    print("Pack's version is now " + versionJson["header"]["packs_version"] + ".")

    with open(manifestFile, 'w') as outfile:
        json.dump(versionJson, outfile)


print("Increasing manifest version by one...")
iterate_manifest(packFolder + manifest)

print("Packaging files to a ZIP...")
shutil.make_archive(packName, 'zip', packFolder)

print("Renaming ZIP to MCPack...")
shutil.move(packName + ".zip", packName + packExt)
print("The pack is ready!")
