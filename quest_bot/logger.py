"""
Quest logging and narrative record system.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from .models import Quest, MemoryMoment


class QuestLogger:
    """
    Manages quest logs and narrative records.
    Transforms shared experiences into lasting records.
    """
    
    def __init__(self, log_directory: str = "quest_logs"):
        """
        Initialize the quest logger.
        
        Args:
            log_directory: Directory to store quest logs
        """
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)
        self.active_quest: Optional[Quest] = None
    
    def start_quest(self, quest: Quest):
        """Begin tracking a quest."""
        self.active_quest = quest
        self._save_quest(quest)
    
    def update_quest(self):
        """Update the current quest log."""
        if self.active_quest:
            self._save_quest(self.active_quest)
    
    def complete_quest(self):
        """Mark the active quest as complete and save."""
        if self.active_quest:
            self.active_quest.complete()
            self._save_quest(self.active_quest)
            
            # Generate narrative summary
            self._generate_narrative_summary(self.active_quest)
            
            self.active_quest = None
    
    def add_memory_moment(self, title: str, description: str, location_hint: str = "") -> Optional[MemoryMoment]:
        """Add a memory moment to the active quest."""
        if self.active_quest:
            moment = self.active_quest.add_memory_moment(title, description, location_hint)
            self._save_quest(self.active_quest)
            return moment
        return None
    
    def _save_quest(self, quest: Quest):
        """Save quest to file."""
        filename = f"{quest.quest_id}.json"
        filepath = self.log_directory / filename
        
        with open(filepath, 'w') as f:
            json.dump(quest.to_dict(), f, indent=2)
    
    def load_quest(self, quest_id: str) -> Optional[dict]:
        """Load a quest from file."""
        filename = f"{quest_id}.json"
        filepath = self.log_directory / filename
        
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    
    def list_quests(self) -> List[str]:
        """List all quest IDs."""
        quest_files = list(self.log_directory.glob("QUEST-*.json"))
        return [f.stem for f in quest_files]
    
    def _generate_narrative_summary(self, quest: Quest):
        """Generate a narrative summary of the quest."""
        summary_filename = f"{quest.quest_id}_NARRATIVE.txt"
        summary_path = self.log_directory / summary_filename
        
        with open(summary_path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write(f"QUEST LOG: {quest.title}\n")
            f.write(f"Mission ID: {quest.quest_id}\n")
            f.write(f"Difficulty: {quest.difficulty.value.upper()}\n")
            f.write(f"Completed: {quest.completed_at.strftime('%Y-%m-%d %H:%M:%S') if quest.completed_at else 'IN PROGRESS'}\n")
            f.write("=" * 70 + "\n\n")
            
            # Original transmission
            f.write("ORIGINAL TRANSMISSION:\n")
            f.write("-" * 70 + "\n")
            f.write(quest.transmission + "\n\n")
            
            # Objectives
            f.write("OBJECTIVES:\n")
            f.write("-" * 70 + "\n")
            for i, obj in enumerate(quest.objectives, 1):
                status_symbol = "✓" if obj.status.value == "completed" else "✗" if obj.status.value == "failed" else "○"
                f.write(f"{status_symbol} {i}. {obj.description}\n")
                if obj.notes:
                    f.write(f"   Notes: {obj.notes}\n")
            f.write("\n")
            
            # Artifacts
            f.write("ARTIFACTS:\n")
            f.write("-" * 70 + "\n")
            for artifact in quest.artifacts:
                discovered_symbol = "★" if artifact.discovered else "☆"
                f.write(f"{discovered_symbol} {artifact.name}: {artifact.description}\n")
                if artifact.discovered and artifact.discovery_notes:
                    f.write(f"   Discovery: {artifact.discovery_notes}\n")
            f.write("\n")
            
            # Memory Moments
            if quest.memory_moments:
                f.write("MEMORY MOMENTS:\n")
                f.write("-" * 70 + "\n")
                for moment in quest.memory_moments:
                    f.write(f"• {moment.title}\n")
                    f.write(f"  {moment.description}\n")
                    if moment.location_hint:
                        f.write(f"  Location: {moment.location_hint}\n")
                    f.write(f"  Time: {moment.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Side Intelligence
            f.write("SIDE INTELLIGENCE:\n")
            f.write("-" * 70 + "\n")
            for intel in quest.side_intelligence:
                f.write(f"• {intel}\n")
            f.write("\n")
            
            # Footer
            f.write("=" * 70 + "\n")
            f.write("The Handler's work is never done. Until next time, Operative.\n")
            f.write("=" * 70 + "\n")
    
    def generate_progress_report(self) -> str:
        """Generate a progress report for the active quest."""
        if not self.active_quest:
            return "No active quest."
        
        quest = self.active_quest
        total_objectives = len(quest.objectives)
        completed_objectives = sum(1 for obj in quest.objectives if obj.status.value == "completed")
        
        discovered_artifacts = sum(1 for art in quest.artifacts if art.discovered)
        total_artifacts = len(quest.artifacts)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║ QUEST PROGRESS: {quest.title:44} ║
╚══════════════════════════════════════════════════════════════════╝

Mission ID: {quest.quest_id}
Difficulty: {quest.difficulty.value.upper()}

OBJECTIVES: {completed_objectives}/{total_objectives} completed
"""
        for i, obj in enumerate(quest.objectives, 1):
            status_symbol = "✓" if obj.status.value == "completed" else "✗" if obj.status.value == "failed" else "○"
            report += f"  {status_symbol} {i}. {obj.description}\n"
        
        report += f"\nARTIFACTS: {discovered_artifacts}/{total_artifacts} discovered\n"
        for art in quest.artifacts:
            symbol = "★" if art.discovered else "☆"
            report += f"  {symbol} {art.name}\n"
        
        report += f"\nMEMORY MOMENTS: {len(quest.memory_moments)} recorded\n"
        
        return report
