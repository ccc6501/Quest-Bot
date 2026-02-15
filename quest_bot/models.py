"""
Core data models for the Quest-Bot system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class QuestDifficulty(Enum):
    """Quest difficulty levels."""
    RECONNAISSANCE = "reconnaissance"
    STANDARD = "standard"
    CHALLENGING = "challenging"
    LEGENDARY = "legendary"


class ObjectiveStatus(Enum):
    """Status of quest objectives."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PlayerInput:
    """Input provided by the player for quest generation."""
    time: str  # e.g., "morning", "afternoon", "evening", "night"
    location: str  # e.g., "urban downtown", "forest trail", "suburban neighborhood"
    conditions: str  # e.g., "rainy", "sunny", "foggy", "snowy"
    mood: str  # e.g., "adventurous", "contemplative", "energetic", "mysterious"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "time": self.time,
            "location": self.location,
            "conditions": self.conditions,
            "mood": self.mood,
        }


@dataclass
class Objective:
    """A quest objective with status tracking."""
    description: str
    status: ObjectiveStatus = ObjectiveStatus.PENDING
    notes: str = ""
    completed_at: Optional[datetime] = None
    
    def complete(self, notes: str = ""):
        """Mark objective as completed."""
        self.status = ObjectiveStatus.COMPLETED
        self.completed_at = datetime.now()
        if notes:
            self.notes = notes
    
    def fail(self, notes: str = ""):
        """Mark objective as failed."""
        self.status = ObjectiveStatus.FAILED
        if notes:
            self.notes = notes
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "description": self.description,
            "status": self.status.value,
            "notes": self.notes,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class Artifact:
    """An artifact or item to discover during the quest."""
    name: str
    description: str
    discovered: bool = False
    discovery_notes: str = ""
    discovered_at: Optional[datetime] = None
    
    def discover(self, notes: str = ""):
        """Mark artifact as discovered."""
        self.discovered = True
        self.discovered_at = datetime.now()
        self.discovery_notes = notes
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "discovered": self.discovered,
            "discovery_notes": self.discovery_notes,
            "discovered_at": self.discovered_at.isoformat() if self.discovered_at else None,
        }


@dataclass
class MemoryMoment:
    """A significant moment or discovery during the quest."""
    title: str
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    location_hint: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "location_hint": self.location_hint,
        }


@dataclass
class Quest:
    """A complete quest with all its components."""
    quest_id: str
    title: str
    transmission: str  # The cryptic message from The Handler
    objectives: List[Objective]
    side_intelligence: List[str]  # Additional clues or hints
    artifacts: List[Artifact]
    memory_moments: List[MemoryMoment] = field(default_factory=list)
    difficulty: QuestDifficulty = QuestDifficulty.STANDARD
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    player_input: Optional[PlayerInput] = None
    
    def add_memory_moment(self, title: str, description: str, location_hint: str = ""):
        """Add a new memory moment to the quest."""
        moment = MemoryMoment(
            title=title,
            description=description,
            location_hint=location_hint
        )
        self.memory_moments.append(moment)
        return moment
    
    def is_completed(self) -> bool:
        """Check if all objectives are completed."""
        return all(obj.status == ObjectiveStatus.COMPLETED for obj in self.objectives)
    
    def complete(self):
        """Mark quest as completed."""
        self.completed_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "quest_id": self.quest_id,
            "title": self.title,
            "transmission": self.transmission,
            "objectives": [obj.to_dict() for obj in self.objectives],
            "side_intelligence": self.side_intelligence,
            "artifacts": [art.to_dict() for art in self.artifacts],
            "memory_moments": [mm.to_dict() for mm in self.memory_moments],
            "difficulty": self.difficulty.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "player_input": self.player_input.to_dict() if self.player_input else None,
        }
