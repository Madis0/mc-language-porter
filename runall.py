import subprocess
import sys

# defaults
jeLangs = ["et_ee", "vro"]
beLangs = ["et_EE", "vro_EE"]
useDownloader = True
usePackager = True
extraSteps = True

# Accept two separate arguments: first is comma-separated JE langs, second is comma-separated BE langs
# Example: python run.py "et_ee,fr_fr" "et_EE,fr_FR"
if len(sys.argv) > 2:
    jeLangs = [l.strip() for l in sys.argv[1].split(",") if l.strip()]
    beLangs = [l.strip() for l in sys.argv[2].split(",") if l.strip()]

if useDownloader:
    print("Executing the downloader script for languages: " + ", ".join(jeLangs) + "...")
    subprocess.call(["python", "downloader.py"] + jeLangs)
    print("Download script completed.\n")

print("Now executing the mapper script...")
subprocess.call(["python", "mapper.py"])
print("Mapper script completed.")

if extraSteps:
    print("\nNow executing the spawn egg adding script...")
    subprocess.call(["python", "spawn-egg-adder.py"])
    print("Spawn egg adding script completed.\n\nNow executing the extra mapping cleanup...")
    subprocess.call(["python", "clean-extra-mappings.py"])
    print("\nExtra mapping cleanup completed.")

print("Now executing the porting script for language pairs...")
subprocess.call(["python", "porter.py", ",".join(jeLangs), ",".join(beLangs)])
print("Porting script completed.")

if usePackager:
    print("\nNow packaging files to a mcpack for languages: " + ", ".join(beLangs) + "...")
    subprocess.call(["python", "packager.py"] + beLangs)
