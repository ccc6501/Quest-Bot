#!/usr/bin/env python3
"""
Quest-Bot CLI: Interactive command-line interface for the adventure quest system.
"""

import sys
from datetime import datetime
from quest_bot import TheHandler, QuestLogger, PlayerInput, ObjectiveStatus


class QuestBotCLI:
    """Command-line interface for Quest-Bot."""
    
    def __init__(self):
        self.handler = TheHandler()
        self.logger = QuestLogger()
        self.running = True
    
    def display_banner(self):
        """Display the Quest-Bot banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════╗
║                          QUEST-BOT                               ║
║                   Adventure Quest System                         ║
║                                                                  ║
║              "What seems ordinary conceals the                   ║
║                     extraordinary."                              ║
║                                                                  ║
║                        — The Handler                             ║
╚══════════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def display_menu(self):
        """Display the main menu."""
        if self.logger.active_quest:
            print("\n" + "=" * 70)
            print("ACTIVE QUEST IN PROGRESS")
            print("=" * 70)
            print("\n1. View Quest Details")
            print("2. Complete Objective")
            print("3. Discover Artifact")
            print("4. Add Memory Moment")
            print("5. View Progress")
            print("6. Complete Quest")
            print("7. Abandon Quest")
        else:
            print("\n" + "=" * 70)
            print("HANDLER OPERATIONS")
            print("=" * 70)
            print("\n1. Request New Quest")
            print("2. View Past Quests")
        
        print("\n0. Exit")
        print("\nEnter choice: ", end="")
    
    def get_player_input(self) -> PlayerInput:
        """Gather player input for quest generation."""
        print("\n" + "=" * 70)
        print("MISSION PARAMETERS")
        print("=" * 70)
        print("\nThe Handler requires the following information...\n")
        
        print("Time of day (e.g., morning, afternoon, evening, night):")
        time = input("> ").strip() or "afternoon"
        
        print("\nLocation (e.g., urban downtown, forest trail, suburban neighborhood, park):")
        location = input("> ").strip() or "urban downtown"
        
        print("\nCurrent conditions (e.g., sunny, rainy, foggy, snowy, cloudy):")
        conditions = input("> ").strip() or "clear"
        
        print("\nYour mood (e.g., adventurous, contemplative, energetic, mysterious, curious):")
        mood = input("> ").strip() or "adventurous"
        
        return PlayerInput(time=time, location=location, conditions=conditions, mood=mood)
    
    def request_new_quest(self):
        """Request and receive a new quest from The Handler."""
        player_input = self.get_player_input()
        
        print("\n" + "=" * 70)
        print("GENERATING TRANSMISSION...")
        print("=" * 70)
        
        quest = self.handler.generate_quest(player_input)
        self.logger.start_quest(quest)
        
        print("\n" + "=" * 70)
        print("INCOMING TRANSMISSION FROM THE HANDLER")
        print("=" * 70)
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
        
        input("\n\nPress Enter to accept the mission...")
    
    def view_quest_details(self):
        """Display current quest details."""
        if not self.logger.active_quest:
            print("\nNo active quest.")
            return
        
        quest = self.logger.active_quest
        
        print("\n" + "=" * 70)
        print(f"QUEST: {quest.title}")
        print(f"Mission ID: {quest.quest_id}")
        print("=" * 70)
        print(f"\n{quest.transmission}\n")
        
        print("=" * 70)
        print("OBJECTIVES:")
        for i, obj in enumerate(quest.objectives, 1):
            status = "✓" if obj.status == ObjectiveStatus.COMPLETED else "○"
            print(f"  {status} {i}. {obj.description}")
            if obj.notes:
                print(f"     Notes: {obj.notes}")
        
        print("\nARTIFACTS:")
        for art in quest.artifacts:
            status = "★" if art.discovered else "☆"
            print(f"  {status} {art.name}: {art.description}")
        
        input("\n\nPress Enter to continue...")
    
    def complete_objective(self):
        """Mark an objective as completed."""
        if not self.logger.active_quest:
            print("\nNo active quest.")
            return
        
        quest = self.logger.active_quest
        pending_objectives = [obj for obj in quest.objectives if obj.status == ObjectiveStatus.PENDING]
        
        if not pending_objectives:
            print("\nAll objectives completed!")
            return
        
        print("\n" + "=" * 70)
        print("COMPLETE OBJECTIVE")
        print("=" * 70)
        
        for i, obj in enumerate(pending_objectives, 1):
            print(f"{i}. {obj.description}")
        
        print("\nSelect objective to complete (or 0 to cancel):")
        try:
            choice = int(input("> ").strip())
            if choice == 0:
                return
            if 1 <= choice <= len(pending_objectives):
                obj = pending_objectives[choice - 1]
                print("\nAdd notes about this objective (optional):")
                notes = input("> ").strip()
                obj.complete(notes)
                self.logger.update_quest()
                print(f"\n✓ Objective completed: {obj.description}")
        except (ValueError, IndexError):
            print("\nInvalid choice.")
        
        input("\nPress Enter to continue...")
    
    def discover_artifact(self):
        """Mark an artifact as discovered."""
        if not self.logger.active_quest:
            print("\nNo active quest.")
            return
        
        quest = self.logger.active_quest
        undiscovered = [art for art in quest.artifacts if not art.discovered]
        
        if not undiscovered:
            print("\nAll artifacts discovered!")
            return
        
        print("\n" + "=" * 70)
        print("DISCOVER ARTIFACT")
        print("=" * 70)
        
        for i, art in enumerate(undiscovered, 1):
            print(f"{i}. {art.name}: {art.description}")
        
        print("\nSelect artifact to discover (or 0 to cancel):")
        try:
            choice = int(input("> ").strip())
            if choice == 0:
                return
            if 1 <= choice <= len(undiscovered):
                art = undiscovered[choice - 1]
                print("\nDescribe your discovery:")
                notes = input("> ").strip()
                art.discover(notes)
                self.logger.update_quest()
                print(f"\n★ Artifact discovered: {art.name}")
        except (ValueError, IndexError):
            print("\nInvalid choice.")
        
        input("\nPress Enter to continue...")
    
    def add_memory_moment(self):
        """Add a memory moment to the quest."""
        if not self.logger.active_quest:
            print("\nNo active quest.")
            return
        
        print("\n" + "=" * 70)
        print("ADD MEMORY MOMENT")
        print("=" * 70)
        
        print("\nTitle for this moment:")
        title = input("> ").strip()
        if not title:
            print("\nCancelled.")
            return
        
        print("\nDescribe this moment:")
        description = input("> ").strip()
        if not description:
            print("\nCancelled.")
            return
        
        print("\nLocation hint (optional):")
        location_hint = input("> ").strip()
        
        self.logger.add_memory_moment(title, description, location_hint)
        print("\n✓ Memory moment recorded.")
        
        input("\nPress Enter to continue...")
    
    def view_progress(self):
        """View quest progress."""
        if not self.logger.active_quest:
            print("\nNo active quest.")
            return
        
        print(self.logger.generate_progress_report())
        input("\nPress Enter to continue...")
    
    def complete_quest(self):
        """Complete the active quest."""
        if not self.logger.active_quest:
            print("\nNo active quest.")
            return
        
        quest = self.logger.active_quest
        
        if not quest.is_completed():
            print("\n" + "=" * 70)
            print("WARNING: Not all objectives are completed.")
            print("=" * 70)
            print("\nAre you sure you want to complete this quest? (yes/no):")
            confirm = input("> ").strip().lower()
            if confirm != "yes":
                print("\nQuest remains active.")
                return
        
        self.logger.complete_quest()
        
        print("\n" + "=" * 70)
        print("QUEST COMPLETED")
        print("=" * 70)
        print(f"\nMission ID: {quest.quest_id}")
        print(f"Title: {quest.title}")
        print("\nA narrative summary has been logged for posterity.")
        print("\nThe Handler acknowledges your effort.")
        print("\n\"The path reveals itself to those who dare to look.\"")
        print("\n— The Handler")
        
        input("\nPress Enter to continue...")
    
    def abandon_quest(self):
        """Abandon the active quest."""
        if not self.logger.active_quest:
            print("\nNo active quest.")
            return
        
        print("\n" + "=" * 70)
        print("ABANDON QUEST")
        print("=" * 70)
        print("\nAre you sure? Progress will be saved but the quest will end. (yes/no):")
        confirm = input("> ").strip().lower()
        
        if confirm == "yes":
            self.logger.update_quest()
            self.logger.active_quest = None
            print("\nQuest abandoned. The Handler understands.")
        else:
            print("\nQuest remains active.")
        
        input("\nPress Enter to continue...")
    
    def view_past_quests(self):
        """View past quest logs."""
        quest_ids = self.logger.list_quests()
        
        if not quest_ids:
            print("\nNo quest logs found.")
            input("\nPress Enter to continue...")
            return
        
        print("\n" + "=" * 70)
        print("QUEST ARCHIVES")
        print("=" * 70)
        
        for quest_id in quest_ids:
            quest_data = self.logger.load_quest(quest_id)
            if quest_data:
                status = "COMPLETED" if quest_data.get("completed_at") else "INCOMPLETE"
                print(f"\n{quest_id} - {quest_data.get('title', 'Unknown')}")
                print(f"  Status: {status}")
                print(f"  Difficulty: {quest_data.get('difficulty', 'Unknown').upper()}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the CLI application."""
        self.display_banner()
        
        while self.running:
            self.display_menu()
            
            try:
                choice = input().strip()
                
                if self.logger.active_quest:
                    if choice == "1":
                        self.view_quest_details()
                    elif choice == "2":
                        self.complete_objective()
                    elif choice == "3":
                        self.discover_artifact()
                    elif choice == "4":
                        self.add_memory_moment()
                    elif choice == "5":
                        self.view_progress()
                    elif choice == "6":
                        self.complete_quest()
                    elif choice == "7":
                        self.abandon_quest()
                    elif choice == "0":
                        print("\nThe Handler awaits your return.")
                        self.running = False
                    else:
                        print("\nInvalid choice.")
                else:
                    if choice == "1":
                        self.request_new_quest()
                    elif choice == "2":
                        self.view_past_quests()
                    elif choice == "0":
                        print("\nThe Handler awaits your return.")
                        self.running = False
                    else:
                        print("\nInvalid choice.")
            
            except KeyboardInterrupt:
                print("\n\nThe Handler awaits your return.")
                self.running = False
            except Exception as e:
                print(f"\nError: {e}")
                input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    cli = QuestBotCLI()
    cli.run()


if __name__ == "__main__":
    main()
