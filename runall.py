import subprocess
translationLang = "et_EE"
useDownloader = True
usePackager = False
extraSteps = True

if useDownloader:
    print("Executing the downloader script...")
    subprocess.call(["python", "downloader.py", translationLang])
    print("Download script completed.\n")

print("Now executing the mapper script...")
subprocess.call(["python", "mapper.py"])
print("Mapper script completed.\n\nNow executing the porting script...")
subprocess.call(["python", "porter.py", translationLang])
print("Porting script completed.")

if usePackager:
    print("\nNow packaging files to a mcpack...")
    subprocess.call(["python", "packager.py", translationLang])
