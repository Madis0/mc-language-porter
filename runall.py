import subprocess
translationLang = "et_EE"

print("Executing the downloader script...")
subprocess.call(["python", "downloader.py", translationLang])
print("Download script completed.\n\nNow executing the mapper script...")
subprocess.call(["python", "mapper.py"])
print("Mapper script completed.\n\nNow executing the porting script...")
subprocess.call(["python", "porter.py", translationLang])
print("Porter script completed.\n\nYour language file is now ready to ZIP into a mcpack format.")

