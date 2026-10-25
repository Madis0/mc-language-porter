# Removes lines from extra-mappings.csv that already exist in mappings.csv

# File names
mappings_file = 'Extra/mappings.csv'
extra_mappings_file = 'Extra/extra-mappings.csv'

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

def main():
    remove_duplicate_generic_mappings()

if __name__ == "__main__":
    main()