"""Week 5 Coding Assignment
The Enchanted Artifacts and the Cryptic Library
Made by Andreas Marangos"""

import random

def display_player_status(player_stats):
    """Display player's health and attack"""
    print(f"Current health: {player_stats['health']}")
    print(f"Current attack: {player_stats['attack']}")

def handle_path_choice(player_stats):
    """Choose path, update player stats."""
    path = random.choice(["left", "right"])
    if path == "left":
        print("Gnome heals you for 10 health.")
        player_stats['health'] = min(player_stats['health'] + 10, 100)
    else:
        print("Fall into pit, lose 15 health.")
        player_stats['health'] -= 15
        if player_stats['health'] < 0:
            player_stats['health'] = 0
            print("Barely alive!")
    return player_stats

def player_attack(player_stats, monster_health):
    """Player attack logic."""
    damage = player_stats['attack']
    monster_health -= damage
    print(f"You strike monster for {damage} damage!")
    return monster_health

def monster_attack(player_stats):
    """Monster attack logic."""
    if random.random() < 0.5:
        damage = 20
        print("Monster critical hit for 20 damage!")
    else:
        damage = 10
        print("Monster hits you for 10 damage!")
    player_stats['health'] -= damage
    return player_stats

def combat_encounter(player_stats, monster_health, has_treasure):
    """Combat loop."""
    print("Monster appears! Battle!")
    while player_stats['health'] > 0 and monster_health > 0:
        print(f"Your Health: {player_stats['health']} | Monster: {monster_health}")
        monster_health = player_attack(player_stats, monster_health)
        if monster_health <= 0:
            print("Monster defeated!")
            return has_treasure
        player_stats = monster_attack(player_stats)
        if player_stats['health'] <= 0:
            print("You defeated!")
            return None
    return None # Consistent return

def check_for_treasure(has_treasure):
    """Check for treasure."""
    if has_treasure:
        print("Treasure found! You win!")
    else:
        print("No treasure. Continue journey.")

def acquire_item(inventory, item):
    """Add item to inventory."""
    inventory.append(item)
    print(f"Acquired {item}!")
    return inventory

def display_inventory(inventory):
    """Display inventory."""
    if not inventory:
        print("Inventory empty.")
    else:
        print("Inventory:")
        for i, item in enumerate(inventory):
            print(f"{i+1}. {item}")

def discover_artifact(player_stats, artifacts, artifact_name):
    """Discover artifact, update stats."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"Discovered: {artifact_name} - {artifact['description']}")
        effect = artifact['effect']
        power = artifact['power']

        if effect == "increases health":
            player_stats['health'] += power
            print(f"{artifact_name} {effect} by {power}. "
                  f"Health now {player_stats['health']}.")
        elif effect == "enhances attack":
            player_stats['attack'] += power
            print(f"{artifact_name} {effect} by {power}. "
                  f"Attack now {player_stats['attack']}.")
        elif effect == "solves puzzles":
            print(f"{artifact_name} {effect}. Wiser.")
        artifacts.pop(artifact_name)
        return player_stats, artifacts
    else:
        print("Nothing of interest.")
        return player_stats, artifacts

def find_clue(clues, new_clue):
    """Add clue if new."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"Discovered new clue: {new_clue}")
    else:
        print("Already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Explore dungeon rooms."""
    for room_tuple in dungeon_rooms:
        (room_description, item, challenge_type,
         challenge_outcome) = room_tuple

        print(room_description)
        if item:
            print(f"Found {item}!")
            acquire_item(inventory, item)

        if challenge_type == "puzzle":
            print("Encounter puzzle!")
            choice = input("Solve/skip puzzle? ").lower()
            if choice == "solve":
                success = random.choice([True, False])
                if success:
                    print(challenge_outcome[0])
                else:
                    print(challenge_outcome[1])
                player_stats['health'] += challenge_outcome[2]

        elif challenge_type == "trap":
            print("See potential trap!")
            choice = input("Disarm/bypass trap? ").lower()
            if choice == "disarm":
                success = random.choice([True, False])
                if success:
                    print(challenge_outcome[0])
                else:
                    print(challenge_outcome[1])
                player_stats['health'] += challenge_outcome[2]

        elif challenge_type == "none":
            print("No challenge. Move on.")

        elif challenge_type == "library":
            print("Enter Cryptic Library.")
            possible_clues = [
                "Treasure where dragon sleeps.",
                "Key with gnome.",
                "Beware ancient shadows.",
                "Amulet unlocks final door.",
                "Seek wisdom in stars.",
                "Path to power via knowledge."
            ]
            selected_clues = random.sample(possible_clues, 2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)

            if "staff_of_wisdom" in inventory:
                print("Staff of Wisdom hums, understanding.")
                print("Texts clearer, deeper meanings.")
                print("Bypass puzzle with knowledge.")

        if player_stats['health'] <= 0:
            player_stats['health'] = 0
            print("Barely alive!")
        display_inventory(inventory)

        try:
            room_tuple[1] = "new_item"
        except TypeError as e:
            print(f"\nError: Cannot modify room tuples - immutable. {e}")
            print("Tuples unchangeable, data integrity.\n")

    print(f"Exited dungeon, health: {player_stats['health']}.")
    return player_stats, inventory, clues

def main():
    """Main game loop."""
    dungeon_rooms = [
    ("Dusty library", "key", "puzzle",
     ("Solved puzzle!", "Puzzle unsolved.", -5)),
    ("Narrow passage, creaky floor", "torch", "trap",
     ("Avoided trap!", "Triggered trap!", -10)),
    ("Grand hall, shimmering pool", "healing potion", "none", None),
    ("Small room, locked chest", "treasure", "puzzle",
     ("Cracked code!", "Chest locked.", -5)),
    ("Cryptic Library", None, "library", None)
    ]
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {
            "description": "Glowing amulet, life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Powerful ring, attack boost.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff of wisdom, ancient.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }
    has_treasure = random.choice([True, False])

    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(
            player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            check_for_treasure(treasure_obtained_in_combat)

        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(
                    player_stats, artifacts, artifact_name)
                display_player_status(player_stats)

        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(
                player_stats, inventory, dungeon_rooms, clues)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:")
            display_inventory(inventory)
            print("Clues:")
            if clues:
                for clue in clues:
                    print(f"- {clue}")
            else:
                print("No clues.")

if __name__ == "__main__":
    main()