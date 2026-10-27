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

1. [Download Python](https://www.python.org/downloads/)
2. Install the requirements with PIP: `python -m pip install -r requirements.txt`
3. Run `python runall.py`. 
   * Optionally define `true` or `false` as parameters, to control the downloader part. E.g. `python runall.py true` will download latest Mojang files and `python runall.py false` will only use locally existing files
4. Find generated language files in `Output/`.

- `source-en_us.json` adjusts English strings before mapping.
- `extra-*.json` adds or replaces specific strings in a specific language after generic mapping.
- `overrides.json` replaces output values.
- `prefixes.json` adds prefixes to mapped output values. 
Language files are paired automatically when their locale codes match, ignoring case; Bedrock languages without a matching Java language file are skipped.

## Credit

Code and Estonian translations forked from https://github.com/Madis0/mc-language-porter :)