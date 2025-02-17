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
    """Randomly determine if the player lands a critical hit
    takes the player stats and monster health and then outputs the new monster health"""
    damage = player_stats['attack']
    monster_health -= damage
    print(f"You strike the monster for {damage} damage!")
    return monster_health

def monster_attack(player_stats):
    """Randomly determine if the monster lands a critical hit
    takes the player stats and then outputs the new player stats"""
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
    takes the player stats, monster health and has treasure
    and then outputs if the player has the treasure"""
    print("A monster appears! Prepare for battle!")

    while player_stats['health'] > 0 and monster_health > 0:
        print(f"Your Health: {player_stats['health']} | Monster's Health: {monster_health}")

        monster_health = player_attack(player_stats, monster_health)
        if monster_health <= 0:
            print("You defeated the monster!")
            return has_treasure

        player_stats = monster_attack(player_stats)
        if player_stats['health'] <= 0:
            print("You have been defeated!")
            return None

def check_for_treasure(has_treasure):
    """Check if the player found the treasure
    takes the has treasure and then outputs if the player has the treasure"""
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

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
    """Discovers an artifact and updates player stats based on its effect."""
    if artifact_name in artifacts: # Use 'in' operator to check if artifact exists in dictionary keys
        artifact = artifacts[artifact_name] # Use dictionary indexing to access artifact details
        print(f"You discovered: {artifact_name} - {artifact['description']}") # Access dictionary values using keys
        effect = artifact['effect']
        power = artifact['power']

        if effect == "increases health":
            player_stats['health'] += power
            print(f"{artifact_name} {effect} by {power}. Your health is now {player_stats['health']}.")
        elif effect == "enhances attack":
            player_stats['attack'] += power
            print(f"{artifact_name} {effect} by {power}. Your attack is now {player_stats['attack']}.")
        elif effect == "solves puzzles":
            print(f"{artifact_name} {effect}. You feel wiser.")

        artifacts.pop(artifact_name) # Use pop() to remove the artifact from the dictionary after discovery
        # pop() is used to remove an item from the dictionary given its key and also returns the removed item.
        return player_stats, artifacts
    else:
        print("You found nothing of interest.")
        return player_stats, artifacts


def find_clue(clues, new_clue):
    """Adds a new clue to the clues set if it's not already present."""
    if new_clue not in clues: # Use 'in' operator to check if clue is already in the set
        clues.add(new_clue) # Use add() to add a new clue to the set
        # add() is used to add a single element to a set.
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """This section goes through the tuple
    of dungeon rooms and then outputs the player stats and inventory"""
    for room_tuple in dungeon_rooms:
        room_description, item, challenge_type, challenge_outcome = room_tuple # Unpack the tuple

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
            choice = input("Do you want to 'disarm' or 'bypass' the trap? ").lower()

            if choice == "disarm":
                success = random.choice([True, False])
                if success:
                    print(challenge_outcome[0])
                else:
                    print(challenge_outcome[1])
                player_stats['health'] += challenge_outcome[2]

        elif challenge_type == "none":
            print("There doesn't seem to be a challenge in this room. You move on.")

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
            selected_clues = random.sample(possible_clues, 2) # Use random.sample to pick 2 unique clues
            for clue in selected_clues:
                clues = find_clue(clues, clue)

            if "staff_of_wisdom" in inventory: # Check if player has staff_of_wisdom in inventory
                print("The Staff of Wisdom hums in your hand, and you feel a surge of understanding. The cryptic texts become clearer, revealing deeper meanings.")
                print("You feel you could now bypass a puzzle if you wished, using this newfound knowledge.") # Staff of Wisdom effect message

        if player_stats['health'] <= 0:
            player_stats['health'] = 0
            print("You are barely alive!")

        display_inventory(inventory)

        # Demonstrate tuple immutability (as requested in Week 4, still relevant to show understanding)
        try:
            room_tuple[1] = "new_item" # Attempt to modify the tuple (will cause error)
        except TypeError as e:
            print(f"\nError: Cannot modify room tuples - they are immutable. {e}")
            print("Tuples are designed to be unchangeable after creation, ensuring data integrity.\n")

    print(f"You exited the dungeon with {player_stats['health']} health.")
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
    ("The Cryptic Library", None, "library", None) # New Cryptic Library room
]
    player_stats = {'health': 100, 'attack': 5} # Player stats as a dictionary, starting attack at 5
    monster_health = 30
    inventory = []
    clues = set() # Initialize empty set for clues
    artifacts = { # Dictionary of artifacts
        "amulet_of_vitality": {
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "A powerful ring that boosts your attack damage.",
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
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            check_for_treasure(treasure_obtained_in_combat)

        if random.random() < 0.3: # 30% chance to find an artifact after combat
            artifact_keys = list(artifacts.keys()) # Get a list of artifact keys
            if artifact_keys: # Check if there are artifacts left to discover
                artifact_name = random.choice(artifact_keys) # Randomly choose an artifact
                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name) # Discover artifact
                display_player_status(player_stats) # Display updated player stats

        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts)
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