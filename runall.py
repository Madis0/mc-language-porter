import subprocess
import sys

useDownloader = True
extraSteps = True

jeLangs = [
    "bg_bg", "cs_cz", "da_dk", "de_de", "el_gr", "en_gb", "en_au",
    "en_ca", "en_nz", "en_us", "es_es", "es_mx", "et_ee", "fi_fi", 
    "fr_ca", "fr_fr", "hu_hu", "id_id", "it_it", "ja_jp", "ko_kr", 
    "no_no", "nl_nl", "pl_pl", "pt_br", "pt_pt", "ru_ru", "sk_sk", 
    "sv_se", "tr_tr", "uk_ua", "zh_cn", "zh_tw",
]
beLangs = [
    "bg_BG", "cs_CZ", "da_DK", "de_DE", "el_GR", "en_GB", "en_GB",
    "en_GB", "en_GB", "en_US", "es_ES", "es_MX", "et_EE", "fi_FI", 
    "fr_CA", "fr_FR", "hu_HU", "id_ID", "it_IT", "ja_JP", "ko_KR", 
    "nb_NO", "nl_NL", "pl_PL", "pt_BR", "pt_PT", "ru_RU", "sk_SK", 
    "sv_SE", "tr_TR", "uk_UA", "zh_CN", "zh_TW",
]

# "runall.py true" or "runall.py false"; "true" means the downloader will be used, "false" means it will be skipped. 
# If no argument is provided, the downloader will be used by default.
if len(sys.argv) > 1:
    downloaderArg = sys.argv[1].lower()
    if downloaderArg not in {"true", "false"}:
        raise ValueError("The optional argument must be 'true' or 'false'.")
    useDownloader = downloaderArg == "true"

if useDownloader:
    print("Executing the downloader script...")
    subprocess.run([sys.executable, "downloader.py"], check=True)
    print("Download script completed.\n")

print("Now executing the mapper script...")
subprocess.run([sys.executable, "mapper.py"], check=True)
print("Mapper script completed.")

if extraSteps:
    print("\nNow executing the spawn egg adding script...")
    subprocess.call(["python", "spawn-egg-adder.py"])
    print("Spawn egg adding script completed.\n\nNow executing the extra mapping cleanup...")
    subprocess.call(["python", "clean-extra-mappings.py"])
    print("\nExtra mapping cleanup completed.")

print("Now executing the porting script for language pairs...")
porterArgs = [sys.executable, "porter.py"]
if jeLangs or beLangs:
    porterArgs.extend([",".join(jeLangs), ",".join(beLangs)])
subprocess.run(porterArgs, check=True)
print("Porting script completed.")
