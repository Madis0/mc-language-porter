import requests
from io import BytesIO
from zipfile import ZipFile
import urllib.request
import sys

# Choose what files to obtain with the script
# Original files have much larger download sizes as they download the whole archive to extract files from.
getJeOriginal = False            # ~25 MB
getJeRealms = False              # ~25 MB
getJeTranslation = False         # ~0.2 MB
getJeRealmsTranslation = False   # ~0.01 MB
getBeOriginal = True            # ~47 MB
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
    print("Latest snapshot JSON obtained.")

# Get latest JE JAR url (includes Realms)
if getJeOriginal or getJeRealms:
    print("Finding Java Edition JAR URL...")
    jeLatestJarUrl = jeLatestJson['downloads']['client']['url']
    jeLatestJarSize = jeLatestJson['downloads']['client']['size']
    print("Java Edition JAR URL obtained.")

# Get latest JE assets
if getJeTranslation or getJeRealmsTranslation:
    print("Finding JE assets JSON...")
    jeLatestAssetUrl = jeLatestJson['assetIndex']['url']
    jeLatestAssetSize = jeLatestJson['assetIndex']['size']
    jeLatestAssetJson = requests.get(jeLatestAssetUrl).json()
    print("Assets JSON obtained.")

# Get latest JE translation file URL
if getJeTranslation:
    print("Finding JE translation file URL...")
    jeTranslationHash = jeLatestAssetJson['objects']['minecraft/lang/' + jeTranslationFile]['hash']
    jeTranslationSize = jeLatestAssetJson['objects']['minecraft/lang/' + jeTranslationFile]['size']
    jeTranslationUrl = jeGlobalAssetUrl + jeTranslationHash[0:2] + "/" + jeTranslationHash
    print("Translation file URL obtained.")

# Get latest Realms translation file URL
if getJeRealmsTranslation:
    print("Finding Realms translation file URL...")
    jeRealmsTranslationHash = jeLatestAssetJson['objects']['realms/lang/' + jeTranslationFile]['hash']
    jeRealmsTranslationSize = jeLatestAssetJson['objects']['realms/lang/' + jeTranslationFile]['size']
    jeRealmsTranslationUrl = jeGlobalAssetUrl + jeRealmsTranslationHash[0:2] + "/" + jeRealmsTranslationHash
    print("Translation file URL obtained.")


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
    print("Downloading and extracting " + jeLangFile + " (Minecraft) from Java Edition JAR... (" + str(jeLatestJarSize) + " bytes to download)")
    unpack_zip(jeLatestJarUrl, jeJarLangPath, jeLangFile)
    print(jeLangFile + " has been saved in the current directory.")

if getJeRealms:
    print("Downloading and extracting " + jeLangFile + " (Realms) from Java Edition JAR... (" + str(jeLatestJarSize) + " bytes to download)")
    unpack_zip(jeLatestJarUrl, jeRealmsLangPath, jeRealmsLangFile)
    print(jeRealmsLangFile + " has been saved in the current directory.")

if getJeTranslation:
    print("Downloading and saving " + jeTranslationFile + " from Java Edition assets... (" + str(jeTranslationSize) + " bytes to download)")
    download_text(jeTranslationUrl, jeTranslationFile)
    print(jeTranslationFile + " has been saved in the current directory.")

if getJeRealmsTranslation:
    print("Downloading and saving " + jeRealmsTranslationFile + " from Realms assets... (" + str(jeRealmsTranslationSize) + " bytes to download)")
    download_text(jeRealmsTranslationUrl, jeRealmsTranslationFile)
    print(jeRealmsTranslationFile + " has been saved in the current directory.")

if getBeOriginal:
    beLangFileRequest = urllib.request.urlopen(beLatestZipUrl)  # https://stackoverflow.com/a/5935
    print("Downloading and extracting " + beLangFile + " from Bedrock Edition resources... (" + str(beLangFileRequest.info()['Content-Length']) + " bytes to download)")
    unpack_zip(beLatestZipUrl, beZipLangPath, beLangFile)
    print(beLangFile + " has been saved in the current directory.")
