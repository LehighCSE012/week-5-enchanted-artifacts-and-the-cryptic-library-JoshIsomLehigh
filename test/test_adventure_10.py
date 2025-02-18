import pytest
from adventure import enter_dungeon
from unittest.mock import patch
import io
import sys

def test_tuple_immutability_error_handling(capsys):
    dungeon_rooms = [("Room 1", "item1", "none", None)]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()

    enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
    captured = capsys.readouterr()
    assert "Error: Cannot modify room tuples - immutable." in captured.out # Correct assertion

def test_enter_dungeon_runs_without_crash(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "skip")

    dungeon_rooms = [
        ("Room 1", "item1", "none", None),
        ("Room 2", None, "puzzle", ("success", "fail", -5))
    ]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    try:
        updated_player_stats, inventory_out, clues_out = enter_dungeon(
            player_stats, inventory, dungeon_rooms, clues)
        assert isinstance(updated_player_stats, dict)
        assert isinstance(inventory_out, list)
        assert isinstance(clues_out, set)
    except Exception as e:
        pytest.fail(f"enter_dungeon raised an exception: {e}")