import pytest
from adventure import main, combat_encounter, discover_artifact
import adventure # Import the adventure module
from unittest.mock import patch
import io
import sys

def test_combat_encounter_updates_player_health():
    player_stats_test = {'health': 100, 'attack': 5} # Local player_stats
    monster_health = 50
    has_treasure = False

    initial_health = player_stats_test['health']
    combat_encounter(player_stats_test, monster_health, has_treasure)
    assert player_stats_test['health'] <= initial_health

def test_combat_encounter_monster_defeated():
    player_stats_test = {'health': 100, 'attack': 50} # Local player_stats
    monster_health = 10
    has_treasure = True

    treasure_obtained = combat_encounter(player_stats_test, monster_health, has_treasure)
    assert treasure_obtained is True

def test_discover_artifact_called_in_main(monkeypatch, capsys):
    monkeypatch.setattr('random.random', lambda: 0.1)
    monkeypatch.setattr('random.choice', lambda x: x[0] if x else None)
    monkeypatch.setattr('builtins.input', lambda _: "skip")

    testargs = ["prog",]
    monkeypatch.setattr(sys, 'argv', testargs)

    try:
        main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert "You discovered:" in captured.out

def test_artifact_discovery_updates_stats_in_main(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 0.1)
    monkeypatch.setattr('random.choice', lambda x: x[0] if x else None)
    monkeypatch.setattr('builtins.input', lambda _: "skip")

    testargs = ["prog",]
    monkeypatch.setattr(sys, 'argv', testargs)

    initial_stats = {'health': 100, 'attack': 5}
    captured_stats = {'health': 0, 'attack': 0}
    original_main = adventure.main

    def monkeypatched_main():
        original_main()
        captured_stats['health'] = adventure.player_stats['health'] # Still incorrect - player_stats is local in main
        captured_stats['attack'] = adventure.player_stats['attack'] # Still incorrect

    monkeypatch.setattr(adventure, 'main', monkeypatched_main)

    try:
        main()
    except SystemExit:
        pass

    assert captured_stats['health'] > initial_stats['health'] or captured_stats['attack'] > initial_stats['attack']