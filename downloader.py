import requests
from io import BytesIO
from zipfile import ZipFile
from hurry.filesize import size, alternative
import urllib.request
import sys

# Choose what files to obtain with the script
# Original files have much larger download sizes as they download the whole archive to extract files from.
getJeOriginal = True            # ~24 MB
getJeRealms = True              # ~24 MB
getJeTranslation = True         # ~286 KB
getJeRealmsTranslation = True   # ~15 KB
getBeOriginal = True            # ~44 MB
translationLang = "et_ee"       # Used when launched without arguments

# Paths and variables -  https://wiki.vg/Game_files
if len(sys.argv) > 1:  # Use the language provided as an argument if available
    translationLang = sys.argv[1].lower()

jeGlobalJsonUrl = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
jeGlobalJson = None

jeLatestJsonUrl = ""
jeLatestJson = None

jeLatestJarUrl = ""
jeLatestRealmsUrl = ""

jeLatestAssetUrl = ""
jeLatestAssetJson = None

jeTranslationHash = None
jeTranslationUrl = None

jeRealmsTranslationHash = ""
jeRealmsTranslationUrl = ""

jeLangFile = "en_us.json"
jeRealmsLangFile = "realms-" + jeLangFile
jeJarLangPath = "assets/minecraft/lang/" + jeLangFile
jeRealmsLangPath = "assets/realms/lang/" + jeLangFile

beLatestZipUrl = "https://aka.ms/MinecraftBetaResources"
beLangFile = "en_US.lang"
beZipLangPath = "texts/" + beLangFile

jeTranslationFile = translationLang + ".json"
jeRealmsTranslationFile = "realms-" + jeTranslationFile
jeGlobalAssetUrl = "https://resources.download.minecraft.net/"

# Get latest JE JSON url - https://stackoverflow.com/a/16130026
if getJeOriginal or getJeRealms or getJeTranslation or getJeRealmsTranslation:
    print("Finding the Java Edition latest snapshot JSON...")
    jeGlobalJson = requests.get(jeGlobalJsonUrl).json()
    jeLatestJsonUrl = jeGlobalJson['versions'][0]['url']
    jeLatestJson = requests.get(jeLatestJsonUrl).json()
    print("Latest snapshot JSON obtained: " + jeLatestJsonUrl)

# Get latest JE JAR url (includes Realms)
if getJeOriginal or getJeRealms:
    print("Finding Java Edition JAR URL...")
    jeLatestJarUrl = jeLatestJson['downloads']['client']['url']
    jeLatestJarSize = jeLatestJson['downloads']['client']['size']
    print("Java Edition JAR URL obtained: " + jeLatestJarUrl)

# Get latest JE assets
if getJeTranslation or getJeRealmsTranslation:
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

# Get latest Realms translation file URL
if getJeRealmsTranslation:
    print("Finding Realms translation file URL...")
    jeRealmsTranslationHash = jeLatestAssetJson['objects']['realms/lang/' + jeTranslationFile]['hash']
    jeRealmsTranslationSize = jeLatestAssetJson['objects']['realms/lang/' + jeTranslationFile]['size']
    jeRealmsTranslationUrl = jeGlobalAssetUrl + jeRealmsTranslationHash[0:2] + "/" + jeRealmsTranslationHash
    print("Translation file URL obtained: " + jeRealmsTranslationUrl)


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

if getJeRealms:
    print("Downloading and extracting " + jeLangFile + " (Realms) from Java Edition JAR... (" + size(jeLatestJarSize, system=alternative) + " to download)")
    unpack_zip(jeLatestJarUrl, jeRealmsLangPath, jeRealmsLangFile)
    print(jeRealmsLangFile + " has been saved in the current directory.")

if getJeTranslation:
    print("Downloading and saving " + jeTranslationFile + " from Java Edition assets... (" + size(jeTranslationSize, system=alternative) + " to download)")
    download_text(jeTranslationUrl, jeTranslationFile)
    print(jeTranslationFile + " has been saved in the current directory.")

if getJeRealmsTranslation:
    print("Downloading and saving " + jeRealmsTranslationFile + " from Realms assets... (" + size(jeRealmsTranslationSize, system=alternative) + " to download)")
    download_text(jeRealmsTranslationUrl, jeRealmsTranslationFile)
    print(jeRealmsTranslationFile + " has been saved in the current directory.")

if getBeOriginal:
    beLangFileRequest = urllib.request.urlopen(beLatestZipUrl)  # https://stackoverflow.com/a/5935
    print("Downloading and extracting " + beLangFile + " from Bedrock Edition resources... (" + size(int(beLangFileRequest.info()['Content-Length']), system=alternative) + " to download)")
    unpack_zip(beLatestZipUrl, beZipLangPath, beLangFile)
    print(beLangFile + " has been saved in the current directory.")
