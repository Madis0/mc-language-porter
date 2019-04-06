import subprocess
translationLang = "et_EE"
usePackager = False

print("Executing the downloader script...")
subprocess.call(["python", "downloader.py", translationLang])
print("Download script completed.\n\nNow executing the mapper script...")
subprocess.call(["python", "mapper.py"])
print("Mapper script completed.\n\nNow executing the porting script...")
subprocess.call(["python", "porter.py", translationLang])
print("Porting script completed.")

if usePackager:
    print("\nNow packaging files to a mcpack...")
    subprocess.call(["python", "packager.py", translationLang])
