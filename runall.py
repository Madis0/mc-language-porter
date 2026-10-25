import subprocess
import sys

# defaults
jeLangs = [
    "bg_bg", "cs_cz", "da_dk", "de_de", "el_gr", "en_gb", "en_us",
    "es_es", "es_mx", "et_ee", "fi_fi", "fr_ca", "fr_fr", "hu_hu",
    "id_id", "it_it", "ja_jp", "ko_kr", "no_no", "nl_nl", "pl_pl",
    "pt_br", "pt_pt", "ru_ru", "sk_sk", "sv_se", "tr_tr", "uk_ua",
    "zh_cn", "zh_tw",
]
beLangs = [
    "bg_BG", "cs_CZ", "da_DK", "de_DE", "el_GR", "en_GB", "en_US",
    "es_ES", "es_MX", "et_EE", "fi_FI", "fr_CA", "fr_FR", "hu_HU",
    "id_ID", "it_IT", "ja_JP", "ko_KR", "nb_NO", "nl_NL", "pl_PL",
    "pt_BR", "pt_PT", "ru_RU", "sk_SK", "sv_SE", "tr_TR", "uk_UA",
    "zh_CN", "zh_TW",
]
useDownloader = False

# Accept two separate arguments: first is comma-separated JE langs, second is comma-separated BE langs
# Example: python run.py "et_ee,fr_fr" "et_EE,fr_FR"
if len(sys.argv) > 2:
    jeLangs = [l.strip() for l in sys.argv[1].split(",") if l.strip()]
    beLangs = [l.strip() for l in sys.argv[2].split(",") if l.strip()]

if useDownloader:
    print("Executing the downloader script...")
    subprocess.run([sys.executable, "downloader.py"], check=True)
    print("Download script completed.\n")

print("Now executing the mapper script...")
subprocess.run([sys.executable, "mapper.py"], check=True)
print("Mapper script completed.")

print("Now executing the porting script for language pairs...")
porterArgs = [sys.executable, "porter.py"]
if jeLangs or beLangs:
    porterArgs.extend([",".join(jeLangs), ",".join(beLangs)])
subprocess.run(porterArgs, check=True)
print("Porting script completed.")
