import requests
from io import BytesIO
from zipfile import ZipFile
from hurry.filesize import size, alternative
import urllib.request
import sys

# Choose what files to obtain with the script
# Original files have much larger download sizes as they download the whole archive to extract files from.
getJeOriginal = True            # ~24 MB
getJeTranslation = True         # ~286 KB
getBeOriginal = True            # ~500 KB
translationLang = "et_ee"       # Used when launched without arguments

# Paths and variables -  https://wiki.vg/Game_files
if len(sys.argv) > 1:  # Use the language provided as an argument if available
    translationLang = sys.argv[1].lower()

jeGlobalJsonUrl = "https://piston-meta.mojang.com/mc/game/version_manifest.json"
jeGlobalJson = None

jeLatestJsonUrl = ""
jeLatestJson = None

jeLatestJarUrl = ""

jeLatestAssetUrl = ""
jeLatestAssetJson = None

jeTranslationHash = None
jeTranslationUrl = None

jeLangFile = "en_us.json"
jeJarLangPath = "assets/minecraft/lang/" + jeLangFile

beLatestLangUrl = "https://raw.githubusercontent.com/Mojang/bedrock-samples/preview/resource_pack/texts/en_US.lang";
beLangFile = "en_US.lang"

jeTranslationFile = translationLang + ".json"
jeGlobalAssetUrl = "https://resources.download.minecraft.net/"

# Get latest JE JSON url - https://stackoverflow.com/a/16130026
if getJeOriginal or getJeTranslation:
    print("Finding the Java Edition latest snapshot JSON...")
    jeGlobalJson = requests.get(jeGlobalJsonUrl).json()
    jeLatestJsonUrl = jeGlobalJson['versions'][0]['url']
    jeLatestJson = requests.get(jeLatestJsonUrl).json()
    print("Latest snapshot JSON obtained: " + jeLatestJsonUrl)

# Get latest JE JAR url (includes Realms)
if getJeOriginal:
    print("Finding Java Edition JAR URL...")
    jeLatestJarUrl = jeLatestJson['downloads']['client']['url']
    jeLatestJarSize = jeLatestJson['downloads']['client']['size']
    print("Java Edition JAR URL obtained: " + jeLatestJarUrl)

# Get latest JE assets
if getJeTranslation:
    print("Finding JE assets JSON...")
    jeLatestAssetUrl = jeLatestJson['assetIndex']['url']
    jeLatestAssetSize = jeLatestJson['assetIndex']['size']
    jeLatestAssetJson = requests.get(jeLatestAssetUrl).json()
    print("Assets JSON obtained: " + jeLatestAssetUrl)

# Get latest JE translation file URL
if getJeTranslation:
    print("Finding JE translation file URL...")
    jeTranslationHash = jeLatestAssetJson['objects']['minecraft/lang/' + jeTranslationFile]['hash']
    jeTranslationSize = jeLatestAssetJson['objects']['minecraft/lang/' + jeTranslationFile]['size']
    jeTranslationUrl = jeGlobalAssetUrl + jeTranslationHash[0:2] + "/" + jeTranslationHash
    print("Translation file URL obtained: " + jeTranslationUrl)

# Obtaining functions
# Unpack zips - https://stackoverflow.com/a/5711095
def unpack_zip(url, filepath, filename):
    openUrl = urllib.request.urlopen(url)
    with ZipFile(BytesIO(openUrl.read())) as zipFile:
        with zipFile.open(filepath) as extractedFile:
            with open(filename, 'w', encoding="utf-8") as savedFile:
                for line in extractedFile:
                    savedFile.write(line.decode('utf-8'))


def download_text(url, filename):
    file = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(file.content)


# File obtaining
if getJeOriginal:
    print("Downloading and extracting " + jeLangFile + " (Minecraft) from Java Edition JAR... (" + size(jeLatestJarSize, system=alternative) + " to download)")
    unpack_zip(jeLatestJarUrl, jeJarLangPath, jeLangFile)
    print(jeLangFile + " has been saved in the current directory.")

if getJeTranslation:
    print("Downloading and saving " + jeTranslationFile + " from Java Edition assets... (" + size(jeTranslationSize, system=alternative) + " to download)")
    download_text(jeTranslationUrl, jeTranslationFile)
    print(jeTranslationFile + " has been saved in the current directory.")

if getBeOriginal:
    print("Downloading and saving " + beLangFile + " from Bedrock Edition resources... (ca 500 KB to download)")
    download_text(beLatestLangUrl, beLangFile)
    print(beLangFile + " has been saved in the current directory.")
