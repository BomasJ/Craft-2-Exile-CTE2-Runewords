import os
import json

def get_matching_files(base_directory, equipment_type, max_rune_slots):
    directory = os.path.join(base_directory, "data", "mmorpg_runeword")
    matching_files = []

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                slots = data.get('slots', [])
                runes = data.get('runes', [])

                if equipment_type not in slots:
                    continue
                if len(runes) > max_rune_slots:
                    continue

                matching_files.append(filename)

    return matching_files

def format_stats(stats, single_line_format):
    formatted_stats = []

    # Separate stats into percentage and flat, and prioritize negative stats
    negative_stats = [s for s in stats if s['max'] < 0]
    positive_stats = [s for s in stats if s['max'] >= 0]
    percentage_stats = [s for s in positive_stats if s['type'] == 'PERCENT']
    flat_stats = [s for s in positive_stats if s['type'] == 'FLAT']

    # Format negative stats
    for stat in negative_stats:
        stat_str = f"{stat['min']}%" if stat['type'] == 'PERCENT' else f"{stat['min']}"
        formatted_stats.append(f"{stat_str} {stat['stat'].replace('_', ' ').title()}")

    # Format percentage stats
    for stat in percentage_stats:
        if stat['min'] == stat['max']:
            formatted_stats.append(f"+{int(stat['max'])}% {stat['stat'].replace('_', ' ').title()}")
        else:
            formatted_stats.append(f"+{int(stat['min'])}-{int(stat['max'])}% {stat['stat'].replace('_', ' ').title()}")

    # Format flat stats
    for stat in flat_stats:
        if stat['min'] == stat['max']:
            formatted_stats.append(f"+{int(stat['max'])} {stat['stat'].replace('_', ' ').title()}")
        else:
            formatted_stats.append(f"+{int(stat['min'])}-{int(stat['max'])} {stat['stat'].replace('_', ' ').title()}")

    # If single_line_format is True, return stats as a single line
    if single_line_format:
        return ", ".join(formatted_stats)
    else:
        # Otherwise, return each stat on a new line
        return formatted_stats

def display_file_contents(base_directory, filenames, single_line_format):
    slot_order = ['helmet', 'chest', 'boots', 'pants']

    directory = os.path.join(base_directory, "data", "mmorpg_runeword")
    for filename in filenames:
        with open(os.path.join(directory, filename), 'r') as file:
            data = json.load(file)
            runeword_name = data['id'].replace('_', ' ').title()
            runes = ", ".join(rune.upper() for rune in data['runes'])
            slots = sorted(data['slots'], key=lambda s: slot_order.index(s) if s in slot_order else len(slot_order))
            slots = ", ".join(slot.title() for slot in slots)
            stats = format_stats(data['stats'], single_line_format)

            print(f"\n{runeword_name}")
            print(f"Runes: {runes}")
            print(f"Slots: {slots}")
            # Print the stats based on the format toggle
            if isinstance(stats, list):
                for stat in stats:
                    print(stat)
            else:
                print(stats)

def get_equipment_types(base_directory):
    directory = os.path.join(base_directory, "data", "mmorpg_runeword")
    equipment_types = set()

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                slots = data.get('slots', [])
                for slot in slots:
                    equipment_types.add(slot.capitalize())  # Capitalize each type

    return sorted(equipment_types)

def get_max_rune_slots(base_directory):
    directory = os.path.join(base_directory, "data", "mmorpg_runeword")
    max_rune_slots = 0

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                runes = data.get('runes', [])
                max_rune_slots = max(max_rune_slots, len(runes))

    return max_rune_slots

def format_equipment_types(equipment_types):
    categories = {
        "Weapons": ["Sword", "Spear", "Dagger", "Axe", "Hammer", "Staff", "Bow", "Crossbow"],
        "Armor": ["Helmet", "Chest", "Boots", "Pants"],
        "Jewelry": ["Necklace", "Ring"],
        "Miscellaneous": ["Tome", "Totem", "Shield"]
    }

    formatted_output = []
    extra_types = []

    # Group equipment types into categories
    for category, items in categories.items():
        found_items = [item for item in items if item in equipment_types]
        if found_items:
            formatted_output.append(", ".join(found_items))
            for item in found_items:
                equipment_types.remove(item)

    # Add any extra types found (outside of predefined categories)
    if equipment_types:
        extra_types = list(equipment_types)
        formatted_output.append(", ".join(extra_types))
        print(f"Found {len(extra_types)} extra types!")

    return "\n".join(formatted_output)

def main():
    base_directory = os.path.dirname(__file__)  # Get the directory where the script is located

    # Scan for equipment types in the JSON files
    equipment_types = get_equipment_types(base_directory)

    if not equipment_types:
        print("Error: No equipment types found in JSON files.")
        return  # Exit the program if no types are found

    # Format and display the types of equipment
    formatted_types = format_equipment_types(equipment_types)
    print(formatted_types)

    # Display the max number of rune slots (no extra space before this)
    max_rune_slots = get_max_rune_slots(base_directory)
    print(f"Max slots: {max_rune_slots}\n")

    # Proceed with the original prompt
    equipment_type = input("Type of equipment: ").lower()
    max_rune_slots_input = int(input("Number of rune slots: "))

    # Set to True for stats to be displayed in one line, False for separate lines
    single_line_format = True  # You can toggle this between True/False

    matching_files = get_matching_files(base_directory, equipment_type, max_rune_slots_input)

    if not matching_files:
        print("No matching runewords found.")
        return

    runewords = ", ".join(filename.rsplit('.', 1)[0].replace('_', ' ').title() for filename in matching_files)
    print(f"Runewords: {runewords}")

    display_file_contents(base_directory, matching_files, single_line_format)

if __name__ == "__main__":
    main()
