import json

# File names
en_us_json_file = 'en_us.json'
extra_mappings_file = 'extra-mappings.csv'

def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)

def read_mappings(file_name):
    existing_mappings = set()
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                existing_mappings.add(parts[1])
    return existing_mappings

def find_new_spawn_eggs(json_data, existing_mappings):
    new_mappings = []
    for key, value in json_data.items():
        if key.startswith("item.minecraft.") and value.endswith(" Spawn Egg"):
            entity_name = key[len("item.minecraft."):-len("_spawn_egg")]
            mapping = f"item.spawn_egg.entity.{entity_name}.name,{key}"
            if key not in existing_mappings:
                new_mappings.append(mapping)
    return new_mappings

def append_new_mappings(new_mappings):
    if new_mappings:  # Check if there are new mappings to add
        with open(extra_mappings_file, 'a', encoding='utf-8') as file:
            file.write('\n')  # Add a newline before appending new mappings
            for mapping in new_mappings:
                file.write(mapping + "\n")

# Main process
json_data = read_json(en_us_json_file)
existing_mappings = read_mappings(extra_mappings_file)
new_mappings = find_new_spawn_eggs(json_data, existing_mappings)
append_new_mappings(new_mappings)

print(f"Appended {len(new_mappings)} new spawn egg mappings to {extra_mappings_file}.")
