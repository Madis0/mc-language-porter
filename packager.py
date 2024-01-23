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
versionUrl = "https://api.github.com/repos/Mojang/bedrock-samples/releases"
version_regex = "v(\d+)\.\d+\.\d+\.\d+"

print("Copying language file to pack folder...")
shutil.copyfile(langFile, packFolder + langFolder + langFile)

def fetch_version(version_url, version_regex):
    try:
        response = requests.get(version_url)
        response.raise_for_status()
        version_match = re.search(version_regex, response.text)
        if version_match:
            return version_match.group(1)
        else:
            print("Version prefix not found in the URL content.")
            return None
    except requests.RequestException as e:
        print(f"Error fetching version: {e}")
        return None

# Increase version number by one in manifest
def iterate_manifest(manifest_file, version_prefix=None):
    with open(manifest_file, 'r', encoding="utf-8") as file:
        manifest_json = json.load(file)

    manifest_version = manifest_json["header"]["version"]
    manifest_engine = manifest_json["header"]["min_engine_version"]
    manifest_vanilla = manifest_json["header"]["vanilla"]

    if version_prefix:
        major_version = int(version_prefix)
        manifest_version[1] = major_version
        manifest_engine[1] = major_version
        manifest_vanilla[1] = major_version
        print(f"Updated to major version: {major_version}")
    else:
        manifest_version[2] += 1

    with open(manifest_file, 'w', encoding="utf-8") as file:
        json.dump(manifest_json, file, indent=4)

    print("Pack's version is now " + '.'.join(map(str, manifest_version)) + ".")


if useVersionAsPrefix:
    version_prefix = fetch_version(versionUrl, version_regex)
    if version_prefix is None:
        print("Falling back to default version increment.")
else:
    version_prefix = None

print("Increasing manifest version...")
iterate_manifest(packFolder + manifest, version_prefix)

print("Packaging files to a ZIP...")
shutil.make_archive(packName, 'zip', packFolder)

print("Renaming ZIP to MCPack...")
shutil.move(packName + ".zip", packName + packExt)
print("The pack is ready!")
