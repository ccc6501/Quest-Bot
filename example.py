#!/usr/bin/env python3
"""
Example demonstration of the Quest-Bot system.
"""

from quest_bot import TheHandler, QuestLogger, PlayerInput


def main():
    """Run example quest demonstration."""
    print("=" * 70)
    print("QUEST-BOT DEMONSTRATION")
    print("=" * 70)
    
    # Initialize the system
    handler = TheHandler()
    logger = QuestLogger()
    
    # Example 1: Urban Evening Quest
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Urban Evening Quest")
    print("=" * 70)
    
    player_input = PlayerInput(
        time="evening",
        location="urban downtown",
        conditions="foggy",
        mood="mysterious"
    )
    
    quest = handler.generate_quest(player_input)
    logger.start_quest(quest)
    
    print(f"\n{quest.transmission}\n")
    
    print("=" * 70)
    print(f"QUEST: {quest.title}")
    print(f"Mission ID: {quest.quest_id}")
    print(f"Difficulty: {quest.difficulty.value.upper()}")
    print("=" * 70)
    
    print("\nOBJECTIVES:")
    for i, obj in enumerate(quest.objectives, 1):
        print(f"  {i}. {obj.description}")
    
    print("\nARTIFACTS TO DISCOVER:")
    for art in quest.artifacts:
        print(f"  • {art.name}: {art.description}")
    
    print("\nSIDE INTELLIGENCE:")
    for intel in quest.side_intelligence:
        print(f"  • {intel}")
    
    # Simulate completing the quest
    print("\n" + "=" * 70)
    print("SIMULATING QUEST COMPLETION...")
    print("=" * 70)
    
    # Complete some objectives
    quest.objectives[0].complete("Found an ancient cornerstone dated 1887")
    print("✓ Objective 1 completed")
    
    quest.objectives[1].complete("Noticed repeating geometric patterns in window designs")
    print("✓ Objective 2 completed")
    
    # Discover an artifact
    quest.artifacts[0].discover("Discovered a faded 'City Hardware' sign painted on brick")
    print("★ Artifact discovered")
    
    # Add memory moments
    logger.add_memory_moment(
        title="The Forgotten Alley",
        description="Found a narrow passage between buildings where ivy has completely taken over one wall",
        location_hint="Between 3rd and 4th Street"
    )
    print("📝 Memory moment recorded")
    
    logger.add_memory_moment(
        title="The Street Performer",
        description="Watched a saxophonist play under a streetlight, fog swirling around the music",
        location_hint="Corner of Main and Broadway"
    )
    print("📝 Memory moment recorded")
    
    # Complete remaining objectives
    for i in range(2, len(quest.objectives)):
        quest.objectives[i].complete()
        print(f"✓ Objective {i+1} completed")
    
    # Show progress
    print("\n" + logger.generate_progress_report())
    
    # Complete the quest
    logger.complete_quest()
    
    print("\n" + "=" * 70)
    print("QUEST COMPLETED!")
    print("=" * 70)
    print(f"\nNarrative summary saved to: quest_logs/{quest.quest_id}_NARRATIVE.txt")
    
    # Example 2: Morning Forest Quest
    print("\n\n" + "=" * 70)
    print("EXAMPLE 2: Morning Forest Quest")
    print("=" * 70)
    
    player_input2 = PlayerInput(
        time="morning",
        location="forest trail",
        conditions="sunny",
        mood="adventurous"
    )
    
    quest2 = handler.generate_quest(player_input2)
    logger.start_quest(quest2)
    
    print(f"\n{quest2.transmission}\n")
    
    print("=" * 70)
    print(f"QUEST: {quest2.title}")
    print(f"Mission ID: {quest2.quest_id}")
    print(f"Difficulty: {quest2.difficulty.value.upper()}")
    print("=" * 70)
    
    print("\nOBJECTIVES:")
    for i, obj in enumerate(quest2.objectives, 1):
        print(f"  {i}. {obj.description}")
    
    print("\nARTIFACTS TO DISCOVER:")
    for art in quest2.artifacts:
        print(f"  • {art.name}: {art.description}")
    
    print("\n" + "=" * 70)
    print("QUEST ACTIVE AND READY FOR EXPLORATION")
    print("=" * 70)
    
    # Show all quests
    print("\n" + "=" * 70)
    print("QUEST ARCHIVES")
    print("=" * 70)
    
    quest_ids = logger.list_quests()
    for quest_id in quest_ids:
        quest_data = logger.load_quest(quest_id)
        if quest_data:
            status = "COMPLETED" if quest_data.get("completed_at") else "IN PROGRESS"
            print(f"\n{quest_id}")
            print(f"  Title: {quest_data.get('title')}")
            print(f"  Status: {status}")
            print(f"  Difficulty: {quest_data.get('difficulty', 'unknown').upper()}")
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\n\"The path reveals itself to those who dare to look.\"")
    print("\n— The Handler\n")


if __name__ == "__main__":
    main()
