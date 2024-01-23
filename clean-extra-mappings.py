# Removes lines from extra-mappings.csv that already exist in mappings.csv

# File names
mappings_file = 'mappings.csv'
extra_mappings_file = 'extra-mappings.csv'

def read_mappings(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return set(file.readlines())

def remove_duplicates():
    mappings = read_mappings(mappings_file)
    with open(extra_mappings_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(extra_mappings_file, 'w', encoding='utf-8') as file:
        for line in lines:
            if line not in mappings:
                file.write(line)

# Execute the function to remove duplicates
remove_duplicates()
