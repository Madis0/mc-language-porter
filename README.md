# MC language porting tools

An open set of scripts designed to semi-automate the task of porting languages from Minecraft: Java Edition to Minecraft: Bedrock Edition.

## The scripts

* `runall.py` - Executes all other scripts one-by-one.
* `downloader.py` - Extracts and downloads various language files from official sources, including Java Edition, Java Edition Realms and Bedrock Edition. The script downloads the beta/snapshot versions to get the latest language changes early.
* `mapper.py` - Automatically creates CSV-formatted mappings by comparing Java Edition files with Bedrock Edition ones.
* `porter.py` - Creates a Bedrock Edition-compatible language file using mappings, extra mappings, and/or extra translated phrases.

## The files

* `(language).json` - A Java Edition language file, not included in this repo. English one downloadable by `downloader.py` or can be obtained from JAR. Translated one also downloaded by the script or can be obtained from `assets`folder.
* `(language).lang` - A Bedrock Edition language file, not included in this repo. English one downloadable by `downloader.py` or can be obtained [from official resources](https://aka.ms/MinecraftBetaResources). Translated one generated by `porter.py`.
* `mappings.csv` - A CSV-file automatically generated by comparing language files using `mapper.py`. The `extra-mappings.csv` is human-created for additional mappings.
* Folder `Test` - A set of tests that can be used with `mapper.py` to verify that it is working correctly.
* Folder `Eesti keele pakk` - Base resources for the Estonian language pack.

## How to use

1) Download latest Python
2) Download any relevant requirements using PIP
3) Run scripts according to your needs or all at once using `runall.py`.

`downloader.py` and `porter.py` support command line arguments for defining the language, e.g. `py downloader.py ru_ru`. Other settings (e.g which files to download/use) can be set inside the scripts at the start, as booleans `True` or `False`.

## FAQ

### What are the goals of the project?

* Sustainability - the script must do it's best to continue working with any new language strings using the same code.
* Fleksibility - it must be easy to use the scripts with multiple languages and translation sources. 
* Openness - everyone can use, adapt and improve the tools without relying on one authority.

### Is this project related to a similar one, "Translations for Minecraft"?

Not directly. The project in question has gained lots of popularity, I have also endorsed and contributed to it as I think it has great potential. 
However it seems to have gotten abandoned and as it is closed source, it cannot be forked either, which led me to create these Python tools. 
Either way, my tools are still meant to *complete* it, not *compete* with it.

### Legal aspects?

This repository does not and will not host any official assets of the game in either platform, it only provides tools to help you obtain them from official sources and use them to improve your gameplay. No warranties provided for the tools, use them at your own risk. Don't forget to [buy Minecraft](https://minecraft.net)!

---

Not an official Minecraft product. Not accociated with or endorsed by Mojang AB or Microsoft. "Minecraft" is a trademark of Mojang Synergies AB.