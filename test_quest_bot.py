#!/usr/bin/env python3
"""
Test script for Quest-Bot functionality.
"""

from quest_bot import TheHandler, QuestLogger, PlayerInput


def test_quest_generation():
    """Test quest generation."""
    print("=" * 70)
    print("TEST: Quest Generation")
    print("=" * 70)
    
    handler = TheHandler()
    
    # Test with various inputs
    test_inputs = [
        PlayerInput(time="morning", location="forest trail", conditions="sunny", mood="adventurous"),
        PlayerInput(time="evening", location="urban downtown", conditions="foggy", mood="mysterious"),
        PlayerInput(time="night", location="suburban neighborhood", conditions="clear", mood="contemplative"),
    ]
    
    for i, player_input in enumerate(test_inputs, 1):
        print(f"\nTest Case {i}:")
        print(f"  Time: {player_input.time}")
        print(f"  Location: {player_input.location}")
        print(f"  Conditions: {player_input.conditions}")
        print(f"  Mood: {player_input.mood}")
        
        quest = handler.generate_quest(player_input)
        
        print(f"\n  Generated Quest: {quest.title}")
        print(f"  Quest ID: {quest.quest_id}")
        print(f"  Difficulty: {quest.difficulty.value}")
        print(f"  Objectives: {len(quest.objectives)}")
        print(f"  Artifacts: {len(quest.artifacts)}")
        print(f"  Side Intelligence: {len(quest.side_intelligence)}")
        
        assert quest.title, "Quest title should not be empty"
        assert quest.quest_id, "Quest ID should not be empty"
        assert len(quest.objectives) > 0, "Should have at least one objective"
        assert len(quest.artifacts) > 0, "Should have at least one artifact"
        
    print("\n✓ Quest generation test passed!")


def test_quest_logging():
    """Test quest logging."""
    print("\n" + "=" * 70)
    print("TEST: Quest Logging")
    print("=" * 70)
    
    handler = TheHandler()
    logger = QuestLogger(log_directory="/tmp/test_quest_logs")
    
    # Generate a quest
    player_input = PlayerInput(
        time="afternoon",
        location="park",
        conditions="sunny",
        mood="energetic"
    )
    quest = handler.generate_quest(player_input)
    
    print(f"\nStarting quest: {quest.title}")
    logger.start_quest(quest)
    
    # Complete an objective
    print("\nCompleting first objective...")
    quest.objectives[0].complete("Test note for completion")
    logger.update_quest()
    
    # Discover an artifact
    print("Discovering first artifact...")
    quest.artifacts[0].discover("Found it near the old oak tree")
    logger.update_quest()
    
    # Add a memory moment
    print("Adding memory moment...")
    logger.add_memory_moment(
        title="Test Moment",
        description="This is a test memory",
        location_hint="Test location"
    )
    
    # Complete quest
    print("Completing quest...")
    logger.complete_quest()
    
    # Verify logs exist
    quest_ids = logger.list_quests()
    assert quest.quest_id in quest_ids, "Quest should be in logs"
    
    # Load quest back
    loaded_quest_data = logger.load_quest(quest.quest_id)
    assert loaded_quest_data is not None, "Should be able to load quest"
    assert loaded_quest_data['quest_id'] == quest.quest_id, "Quest ID should match"
    
    print("\n✓ Quest logging test passed!")


def test_objective_tracking():
    """Test objective status tracking."""
    print("\n" + "=" * 70)
    print("TEST: Objective Tracking")
    print("=" * 70)
    
    handler = TheHandler()
    player_input = PlayerInput(time="morning", location="urban", conditions="clear", mood="curious")
    quest = handler.generate_quest(player_input)
    
    print(f"\nQuest has {len(quest.objectives)} objectives")
    
    # Initially, quest should not be completed
    assert not quest.is_completed(), "Quest should not be completed initially"
    print("✓ Initial state correct")
    
    # Complete all objectives
    for i, obj in enumerate(quest.objectives, 1):
        obj.complete(f"Completed objective {i}")
        print(f"  Completed objective {i}")
    
    # Now quest should be completable
    assert quest.is_completed(), "Quest should be completed when all objectives are done"
    print("✓ All objectives completed")
    
    # Complete the quest
    quest.complete()
    assert quest.completed_at is not None, "Quest should have completion time"
    print("✓ Quest completion tracked")
    
    print("\n✓ Objective tracking test passed!")


def test_transmission_generation():
    """Test that transmissions are properly formatted."""
    print("\n" + "=" * 70)
    print("TEST: Transmission Generation")
    print("=" * 70)
    
    handler = TheHandler()
    player_input = PlayerInput(
        time="evening",
        location="forest",
        conditions="foggy",
        mood="mysterious"
    )
    quest = handler.generate_quest(player_input)
    
    print("\nGenerated transmission:")
    print("-" * 70)
    print(quest.transmission)
    print("-" * 70)
    
    # Check that transmission has key components
    assert "The Handler" in quest.transmission, "Should be signed by The Handler"
    assert len(quest.transmission) > 100, "Transmission should be substantial"
    
    print("\n✓ Transmission generation test passed!")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("QUEST-BOT TEST SUITE")
    print("=" * 70)
    
    try:
        test_quest_generation()
        test_quest_logging()
        test_objective_tracking()
        test_transmission_generation()
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED! ✓")
        print("=" * 70)
        print("\nThe Handler approves.")
        
    except Exception as e:
        print(f"\n\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
