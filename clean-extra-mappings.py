# Removes lines from extra-mappings.csv that already exist in mappings.csv

# File names
mappings_file = 'mappings.csv'
extra_mappings_file = 'extra-mappings.csv'
extra_specific_mappings = ['extra-et_EE.lang', 'extra-vro_EE.lang']

def read_mappings(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return set(file.readlines())

def remove_duplicate_generic_mappings():
    mappings = read_mappings(mappings_file)
    with open(extra_mappings_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(extra_mappings_file, 'w', encoding='utf-8') as file:
        for line in lines:
            if line not in mappings:
                file.write(line)

def read_left_keys(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        lefts = set()
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split(',', 1)  # mappings_file uses comma
            left = parts[0].strip()
            if left:
                lefts.add(left)
    return lefts

def remove_duplicate_specific_mappings():
    mapping_lefts = read_left_keys(mappings_file)

    for fname in extra_specific_mappings:
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File not found: {fname}")
            continue

        keep_lines = []
        for line in lines:
            stripped = line.rstrip('\n')
            if not stripped:
                keep_lines.append(line)
                continue
            parts = stripped.split('=', 1)  # extra_specific_mappings use "="
            left = parts[0].strip() if parts else ''
            if left and left in mapping_lefts:
                continue
            keep_lines.append(line)

        with open(fname, 'w', encoding='utf-8') as f:
            f.writelines(keep_lines)

def main():
    remove_duplicate_generic_mappings()
    #remove_duplicate_specific_mappings()

if __name__ == "__main__":
    main()