import requests
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import sys

inputPath = Path("Input")
inputPath.mkdir(exist_ok=True)

# Choose what files to obtain with the script
jeLangs = [
    "bg_bg", "cs_cz", "da_dk", "de_de", "el_gr", "en_gb", "en_au",
    "en_ca", "en_nz", "en_us", "es_es", "es_mx", "et_ee", "fi_fi", 
    "fr_ca", "fr_fr", "hu_hu", "id_id", "it_it", "ja_jp", "ko_kr", 
    "no_no", "nl_nl", "pl_pl", "pt_br", "pt_pt", "ru_ru", "sk_sk", 
    "sv_se", "tr_tr", "uk_ua", "zh_cn", "zh_tw",
]

# Paths and variables -  https://wiki.vg/Game_files
if len(sys.argv) > 1:  # Use the languages provided as arguments if available
    jeLangs = [arg.lower() for arg in sys.argv[1:]]

jeManifestUrl = "https://piston-meta.mojang.com/mc/game/version_manifest.json"
bedrockTextsUrl = "https://api.github.com/repos/Mojang/bedrock-samples/contents/resource_pack/texts?ref=main"
bedrockRawUrl = "https://raw.githubusercontent.com/Mojang/bedrock-samples/main/resource_pack/texts/"
estonianReleaseUrl = "https://api.github.com/repos/Madis0/mc-language-porter/releases/latest"
jeAssetUrl = "https://resources.download.minecraft.net/"

def get_json(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def download(url, path):
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    path.write_bytes(response.content)


print("Finding the latest Java Edition release...")
jeManifest = get_json(jeManifestUrl)
releaseId = jeManifest["latest"]["release"]
release = next(version for version in jeManifest["versions"] if version["id"] == releaseId)
jeVersion = get_json(release["url"])
jeAssets = get_json(jeVersion["assetIndex"]["url"])["objects"]
jeClientUrl = jeVersion["downloads"]["client"]["url"]
print("Latest Java Edition release: " + releaseId)

print("Downloading stable Bedrock Edition language files...")
bedrockEntries = get_json(bedrockTextsUrl)
bedrockFiles = sorted(entry["name"] for entry in bedrockEntries if entry["name"].endswith(".lang"))
for bedrockFile in bedrockFiles:
    download(bedrockRawUrl + bedrockFile, inputPath / bedrockFile)
    print("Downloaded " + bedrockFile)

print("Downloading Estonian from the latest language-pack release...")
estonianRelease = get_json(estonianReleaseUrl)
packAsset = next(
    (asset for asset in estonianRelease["assets"]
     if Path(asset["name"]).suffix.lower() in {".mcpack"}),
    None,
)
if packAsset is None:
    raise RuntimeError("No .mcpack asset found in the latest language-pack release.")
response = requests.get(packAsset["browser_download_url"], timeout=60)
response.raise_for_status()
with ZipFile(BytesIO(response.content)) as archive:
    estonianPath = next(
        name for name in archive.namelist()
        if name.replace("\\", "/").endswith("texts/et_EE.lang")
    )
    (inputPath / "et_EE.lang").write_bytes(archive.read(estonianPath))
print("Downloaded et_EE.lang")

print("Downloading configured Java Edition language files...")
if "en_us" in jeLangs:
    response = requests.get(jeClientUrl, timeout=60)
    response.raise_for_status()
    with ZipFile(BytesIO(response.content)) as archive:
        (inputPath / "en_us.json").write_bytes(archive.read("assets/minecraft/lang/en_us.json"))
    print("Downloaded en_us.json from the Java Edition client JAR")

for jeLang in jeLangs:
    if jeLang == "en_us":
        continue
    jeFile = jeLang + ".json"
    asset = jeAssets.get("minecraft/lang/" + jeFile)
    if asset is None:
        print("No Java Edition language file found: " + jeFile)
        continue
    jeUrl = jeAssetUrl + asset["hash"][:2] + "/" + asset["hash"]
    download(jeUrl, inputPath / jeFile)
    print("Downloaded " + jeFile)
