"""Week 5 Coding Assignment
The Enchanted Artifacts and the Cryptic Library
Made by Andreas Marangos"""

import random

def display_player_status(player_stats):
    """Display the player's current health and attack"""
    print(f"Your current health: {player_stats['health']}")
    print(f"Your current attack: {player_stats['attack']}")

def handle_path_choice(player_stats):
    """Randomly choose a path for the player
    takes the player stats and then outputs the new player stats"""
    path = random.choice(["left", "right"])

    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_stats['health'] = min(player_stats['health'] + 10, 100)
    else:
        print("You fall into a pit and lose 15 health points.")
        player_stats['health'] -= 15
        if player_stats['health'] < 0:
            player_stats['health'] = 0
            print("You are barely alive!")

    return player_stats

def player_attack(player_stats, monster_health):
    """Randomly determine if player critical hits
    takes player stats, monster health, outputs new monster health"""
    damage = player_stats['attack']
    monster_health -= damage
    print(f"You strike the monster for {damage} damage!")
    return monster_health

def monster_attack(player_stats):
    """Randomly determine if monster critical hits
    takes player stats, outputs new player stats"""
    if random.random() < 0.5:
        damage = 20
        print("The monster lands a critical hit for 20 damage!")
    else:
        damage = 10
        print("The monster hits you for 10 damage!")

    player_stats['health'] -= damage
    return player_stats

def combat_encounter(player_stats, monster_health, has_treasure):
    """Combat loop
    takes player stats, monster health, treasure status
    outputs updated treasure status"""
    print("A monster appears! Prepare for battle!")

    while player_stats['health'] > 0 and monster_health > 0:
        print(f"Your Health: {player_stats['health']} | "
              f"Monster's Health: {monster_health}")

        monster_health = player_attack(player_stats, monster_health)
        if monster_health <= 0:
            print("You defeated the monster!")
            return has_treasure

        player_stats = monster_attack(player_stats)
        if player_stats['health'] <= 0:
            print("You have been defeated!")
            return None

def check_for_treasure(has_treasure):
    """Check if player found treasure, outputs result"""
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. "
              "You continue your journey.")

def acquire_item(inventory, item):
    """Add an item to the player's inventory"""
    inventory.append(item) # Use append() to add item to inventory list
    # append() is used to add a single item to the end of the list.
    print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """Display the player's inventory"""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for i, item in enumerate(inventory):
            print(f"{i+1}. {item}")

def discover_artifact(player_stats, artifacts, artifact_name):
    """Discovers artifact, updates player stats based on effect."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You discovered: {artifact_name} - "
              f"{artifact['description']}")
        effect = artifact['effect']
        power = artifact['power']

        if effect == "increases health":
            player_stats['health'] += power
            print(f"{artifact_name} {effect} by {power}. "
                  f"Your health is now {player_stats['health']}.")
        elif effect == "enhances attack":
            player_stats['attack'] += power
            print(f"{artifact_name} {effect} by {power}. "
                  f"Your attack is now {player_stats['attack']}.")
        elif effect == "solves puzzles":
            print(f"{artifact_name} {effect}. You feel wiser.")

        artifacts.pop(artifact_name)
        return player_stats, artifacts
    else:
        print("You found nothing of interest.")
        return player_stats, artifacts


def find_clue(clues, new_clue):
    """Adds new clue to clues set if not already present."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Goes through dungeon rooms, updates player stats, inventory."""
    for room_tuple in dungeon_rooms:
        (room_description, item, challenge_type,
         challenge_outcome) = room_tuple

        print(room_description)

        if item:
            print(f"You found a {item} in the room.!")
            acquire_item(inventory, item)

        if challenge_type == "puzzle":
            print("You encounter a puzzle!")
            choice = input("Do you want to 'solve' or 'skip' the puzzle? ").lower()

            if choice == "solve":
                success = random.choice([True, False])
                if success:
                    print(challenge_outcome[0])
                else:
                    print(challenge_outcome[1])
                player_stats['health'] += challenge_outcome[2]

        elif challenge_type == "trap":
            print("You see a potential trap!")
            choice = input("Do you want to 'disarm' or 'bypass' trap? ").lower()

            if choice == "disarm":
                success = random.choice([True, False])
                if success:
                    print(challenge_outcome[0])
                else:
                    print(challenge_outcome[1])
                player_stats['health'] += challenge_outcome[2]

        elif challenge_type == "none":
            print("No challenge in this room. You move on.")

        elif challenge_type == "library":
            print("You enter the Cryptic Library.")
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows of the ancient ones.",
                "The amulet unlocks the final door.",
                "Seek wisdom in the stars.",
                "The path to power is through knowledge."
            ]
            selected_clues = random.sample(possible_clues, 2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)

            if "staff_of_wisdom" in inventory:
                print("Staff of Wisdom hums, you feel understanding.")
                print("Cryptic texts clearer, revealing deeper meanings.")
                print("You could bypass a puzzle using this knowledge.")

        if player_stats['health'] <= 0:
            player_stats['health'] = 0
            print("You are barely alive!")

        display_inventory(inventory)

        try:
            room_tuple[1] = "new_item"
        except TypeError as e:
            print(f"\nError: Cannot modify room tuples - immutable. {e}")
            print("Tuples are unchangeable after creation, data integrity.\n")

    print(f"You exited dungeon with {player_stats['health']} health.")
    return player_stats, inventory, clues

def main():
    """Main game loop"""
    dungeon_rooms = [
    ("A dusty old library", "key", "puzzle",
     ("You solved the puzzle!", "The puzzle remains unsolved.", -5)),
    ("A narrow passage with a creaky floor", "torch", "trap",
     ("You skillfully avoid the trap!", "You triggered a trap!", -10)),
    ("A grand hall with a shimmering pool", "healing potion", "none", None),
    ("A small room with a locked chest", "treasure", "puzzle",
     ("You cracked the code!", "The chest remains stubbornly locked.", -5)),
    ("The Cryptic Library", None, "library", None)
    ]
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "A powerful ring that boosts attack damage.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "A staff imbued with ancient wisdom.",
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
            print("Clues Discovered:")
            if clues:
                for clue in clues:
                    print(f"- {clue}")
            else:
                print("No clues found.")

if __name__ == "__main__":
    main()