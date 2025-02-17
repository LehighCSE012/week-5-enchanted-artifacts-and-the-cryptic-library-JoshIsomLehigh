import pytest
from adventure import enter_dungeon  # Assuming enter_dungeon is in adventure.py
from unittest.mock import patch
import io
import sys

def test_dungeon_rooms_is_list_of_tuples(monkeypatch, capsys): # Added monkeypatch
    monkeypatch.setattr('builtins.input', lambda _: "skip") # Mock input to return "skip"

    dungeon_rooms = [
        ("Room 1", "item1", "none", None),
        ("Room 2", None, "puzzle", ("success", "fail", -5))
    ]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {}
    try:
        enter_dungeon(player_stats, inventory, dungeon_rooms, clues) # Removed artifacts
    except Exception as e:
        pytest.fail(f"enter_dungeon raised an exception with valid dungeon_rooms structure: {e}")

def test_dungeon_room_tuple_structure():
    dungeon_rooms_bad = [
        ("Room 1", "item1", "none"), # Missing challenge_outcome
        ("Room 2", None, "puzzle", "wrong_outcome_type") # outcome not tuple
    ]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {}
    with pytest.raises(ValueError) as excinfo: # Expect ValueError now
        enter_dungeon(player_stats, inventory, dungeon_rooms_bad, clues) # Removed artifacts
    assert "not enough values to unpack" in str(excinfo.value).lower() # More specific assertion

def test_dungeon_rooms_challenge_types(monkeypatch, capsys): # Added monkeypatch
    monkeypatch.setattr('builtins.input', lambda _: "skip") # Mock input to return "skip"

    dungeon_rooms_types = [
        ("Room none", None, "none", None),
        ("Room puzzle", None, "puzzle", ("success", "fail", -5)),
        ("Room trap", None, "trap", ("success", "fail", -5)),
        ("Room library", None, "library", None)
    ]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {}
    try:
        enter_dungeon(player_stats, inventory, dungeon_rooms_types, clues) # Removed artifacts
    except Exception as e:
        pytest.fail(f"enter_dungeon failed to handle all challenge types: {e}")