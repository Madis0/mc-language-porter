# MC language porting tools

An open set of scripts designed to semi-automate the task of porting languages from Minecraft: Java Edition to Minecraft: Bedrock Edition.

[Otsid eesti keele pakki? Vaata siit.](/Juhised.md)

## Scripts

* `runall.py` - Executes the main scripts one-by-one in required order.
* `downloader.py` - Extracts and downloads various language files from official sources, including Java Edition, Java Edition Realms and Bedrock Edition. The script downloads the beta/snapshot versions to get the latest language changes early.
* `mapper.py` - Automatically creates CSV-formatted mappings by comparing Java Edition files with Bedrock Edition ones.
* `porter.py` - Creates a Bedrock Edition-compatible language file using mappings, extra mappings, and/or extra translated phrases.
* `packager.py` - Packages the files to a proper MCPack. Disabled by default in `runall.py` as it uses the Estonian language pack files and format.
* `clean-extra-mappings.py` - Removes mappings from `extra-mappings.csv` that alrady exist in `mappings.csv`
* `spawn-egg-adder.py` - Automatically adds new spawn egg names to `extra-mappings.csv`

## Files

* `(language).json` - A Java Edition language file, not included in this repo. English one downloadable by `downloader.py` or can be obtained from JAR. Translated one also downloaded by the script or can be obtained from `assets`folder.
* `(language).lang` - A Bedrock Edition language file, not included in this repo. English one downloadable by `downloader.py` or can be obtained [from official resources](https://aka.ms/MinecraftBetaResources). Translated one generated by `porter.py`.
* `extra-et_EE.lang` - The extra mappings for Estonian language pack. You can also create one for other languages by using a similar format.
* `mappings.csv` - A CSV-file automatically generated by comparing language files using `mapper.py`, included in the repo for convenience. The `extra-mappings.csv` is human-created for additional mappings.
* `requirements.txt` - Required Python libraries for running all scripts used in the project.
* `Juhised.md` - Download instructions for the Estonian language pack.
* Folder `Test` - A set of tests that can be used with `mapper.py` to verify that it is working correctly.
* Folder `Eesti keele pakk` - Structure of the Estonian language pack, actual language file must be generated with the scripts.

## How to use

1) [Download latest Python](https://www.python.org/downloads/)
2) Download [any relevant requirements](/requirements.txt) [using PIP](https://packaging.python.org/tutorials/installing-packages/#installing-from-pypi)
3) Open `runall.py` and edit the target language/parameters to what you need (at the top of the script)
4) Run `runall.py`
5) Test the output pack in-game
6) Optionally do changes and run the script again, or run other scripts

`downloader.py` and `porter.py` support command line arguments for defining the language, e.g. `py downloader.py ru_ru`. Other settings (e.g which files to download/use) can be set inside the scripts at the start, as booleans `True` or `False`.

Tip: you can also use this tool for backporting new languages or language changes from latest Java Edition version to an older Java Edition version (such as 1.8). For that you just need to get the en_US.lang from the old JAR, map it (`mapper.py`) and port it (`porter.py`). Then you can create a resource pack and use the file there.

## Goals

* Sustainability - the script must do its best to continue working with any new language strings using the same code.
* Flexibility - it must be easy to use the scripts with multiple languages and translation sources. 
* Openness - everyone can use, adapt and improve the tools without relying on one authority.

## Legal

This repository does not and will not host any official assets of the game in either platform, it only provides tools to help you obtain them from official sources and use them to improve your gameplay. No warranties provided for the tools, use them at your own risk. Don't forget to [buy Minecraft](https://minecraft.net)!

---

Not an official Minecraft product. Not accociated with or endorsed by Mojang Studios or Microsoft. "Minecraft" is a trademark of Mojang Studios.
