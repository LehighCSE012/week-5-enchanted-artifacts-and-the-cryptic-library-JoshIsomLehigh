import pytest
from adventure import main, combat_encounter, discover_artifact, player_stats  # Import player_stats
import adventure # Import the adventure module
from unittest.mock import patch
import io
import sys

def test_combat_encounter_updates_player_health():
    player_stats_test = {'health': 100, 'attack': 5} # Use local player_stats for test
    monster_health = 50
    has_treasure = False

    initial_health = player_stats_test['health']
    combat_encounter(player_stats_test, monster_health, has_treasure)
    assert player_stats_test['health'] <= initial_health # Health should decrease or stay 0 if lost

def test_combat_encounter_monster_defeated():
    player_stats_test = {'health': 100, 'attack': 50} # High attack for win
    monster_health = 10
    has_treasure = True

    treasure_obtained = combat_encounter(player_stats_test, monster_health, has_treasure)
    assert treasure_obtained is True # Should return treasure status

def test_discover_artifact_called_in_main(monkeypatch, capsys):
    monkeypatch.setattr('random.random', lambda: 0.1)  # Always find artifact
    monkeypatch.setattr('random.choice', lambda x: x[0] if x else None) # Pick first artifact
    monkeypatch.setattr('builtins.input', lambda _: "skip") # Mock input for main

    testargs = ["prog",]
    monkeypatch.setattr(sys, 'argv', testargs)

    try:
        main() # Run main game
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert "You discovered:" in captured.out # Check if artifact discovery message is printed

def test_artifact_discovery_updates_stats_in_main(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 0.1)  # Always find artifact
    monkeypatch.setattr('random.choice', lambda x: x[0] if x else None) # Pick first artifact
    monkeypatch.setattr('builtins.input', lambda _: "skip") # Mock input for main

    testargs = ["prog",]
    monkeypatch.setattr(sys, 'argv', testargs)

    initial_stats = {'health': 100, 'attack': 5}
    # Monkeypatch main to capture player_stats *after* main function runs
    captured_stats = {'health': 0, 'attack': 0} # Placeholder
    original_main = adventure.main # Now adventure is imported

    def monkeypatched_main():
        original_main()
        captured_stats['health'] = adventure.player_stats['health'] # Capture stats after main
        captured_stats['attack'] = adventure.player_stats['attack']

    monkeypatch.setattr(adventure, 'main', monkeypatched_main) # Replace main with monkeypatched version

    try:
        main()
    except SystemExit:
        pass

    assert captured_stats['health'] > initial_stats['health'] or captured_stats['attack'] > initial_stats['attack'] # Stats should be updated