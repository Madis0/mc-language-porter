# MC language porting tools

An open set of scripts designed to semi-automate the task of porting languages from Minecraft: Bedrock Edition to Minecraft: Java Edition.

[Otsid eesti keelte pakki? Vaata siit.](/Juhised.md)

## Scripts

* `runall.py` - Runs downloading, mapping, and porting in order.
* `downloader.py` - Downloads the latest stable Java Edition language files, all stable Bedrock `.lang` files, and Estonian from the latest language-pack release.
* `mapper.py` - Creates CSV-formatted key mappings by comparing the English Java and Bedrock language files.
* `porter.py` - Uses the mappings and Bedrock translations to create Java Edition `.json` files.

## Files

* `Input/` - Downloaded Java `.json` and Bedrock `.lang` language files, mapping CSVs, and the `extra-en_us.json`, `overrides.json`, and `prefixes.json` configuration files.
* `Input/mappings.csv` - Automatically generated key mappings. `Input/extra-mappings.csv` contains additional human-created mappings.
* `Output/` - Generated Java Edition `.json` language files.
* `requirements.txt` - Required Python libraries for running all scripts used in the project.

## How to use

1) [Download Python](https://www.python.org/downloads/)
2) Install the requirements with PIP.
3) Run `python runall.py`.
4) Find generated language files in `Output/`.

`extra-en_us.json` adjusts English strings before mapping. `overrides.json` replaces output values, and `prefixes.json` adds prefixes to mapped output values. Language files are paired automatically when their locale codes match, ignoring case; Bedrock languages without a matching Java language file are skipped.

## Goals

* Sustainability - the script must do its best to continue working with any new language strings using the same code.
* Flexibility - it must be easy to use the scripts with multiple languages and translation sources. 
* Openness - everyone can use, adapt and improve the tools without relying on one authority.

## Legal

This repository does not and will not host any official assets of the game in either platform, it only provides tools to help you obtain them from official sources and use them to improve your gameplay. No warranties provided for the tools, use them at your own risk. Don't forget to [buy Minecraft](https://minecraft.net)!

---

Not an official Minecraft product. Not accociated with or endorsed by Mojang Studios or Microsoft. "Minecraft" is a trademark of Mojang Studios.
