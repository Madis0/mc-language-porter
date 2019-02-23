import requests
from io import BytesIO
from zipfile import ZipFile
import urllib.request
import sys

# Choose what files to obtain with the script
getJeOriginal = False
getJeRealms = False
getJeTranslation = True
getJeRealmsTranslation = False
translationLang = "et_ee"  # Used when launched without arguments
getBeOriginal = True

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

# Get latest JE JAR url
if getJeOriginal:
    print("Finding Java Edition JAR URL...")
    jeLatestJarUrl = jeLatestJson['downloads']['client']['url']
    print("Java Edition JAR URL obtained.")

# Get latest JE Realms file URL
if getJeRealms:
    print("Finding Realms JAR URL...")
    jeLatestRealmsUrl = jeLatestJson['libraries'][29]['downloads']['artifact']['url']
    print("Realms JAR URL obtained.")

# Get latest JE assets
if getJeTranslation or getJeRealmsTranslation:
    print("Finding JE assets JSON...")
    jeLatestAssetUrl = jeLatestJson['assetIndex']['url']
    jeLatestAssetJson = requests.get(jeLatestAssetUrl).json()
    print("Assets JSON obtained.")

# Get latest JE translation file URL
if getJeTranslation:
    print("Finding JE translation file URL...")
    jeTranslationHash = jeLatestAssetJson['objects']['minecraft/lang/' + jeTranslationFile]['hash']
    jeTranslationUrl = jeGlobalAssetUrl + jeTranslationHash[0:2] + "/" + jeTranslationHash
    print("Translation file URL obtained.")

# Get latest Realms translation file URL
if getJeRealmsTranslation:
    print("Finding Realms translation file URL...")
    jeRealmsTranslationHash = jeLatestAssetJson['objects']['realms/lang/' + jeTranslationFile]['hash']
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
    print("Downloading and extracting " + jeLangFile + " from Java Edition JAR...")
    unpack_zip(jeLatestJarUrl, jeJarLangPath, jeLangFile)
    print(jeLangFile + " has been saved in the current directory.")

if getJeRealms:
    print("Downloading and extracting " + jeRealmsLangFile + " from Realms JAR...")
    unpack_zip(jeLatestRealmsUrl, jeRealmsLangPath, jeRealmsLangFile)
    print(jeRealmsLangFile + " has been saved in the current directory.")

if getJeTranslation:
    print("Downloading and saving " + jeTranslationFile + " from Java Edition assets...")
    download_text(jeTranslationUrl, jeTranslationFile)
    print(jeTranslationFile + " has been saved in the current directory.")

if getJeRealmsTranslation:
    print("Downloading and saving " + jeRealmsTranslationFile + " from Realms assets...")
    download_text(jeRealmsTranslationUrl, jeRealmsTranslationFile)
    print(jeRealmsTranslationFile + " has been saved in the current directory.")

if getBeOriginal:
    print("Downloading and extracting " + beLangFile + " from Bedrock Edition resources...")
    unpack_zip(beLatestZipUrl, beZipLangPath, beLangFile)
    print(beLangFile + " has been saved in the current directory.")
