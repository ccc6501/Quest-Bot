"""
Quest-Bot: An adventure quest system for real-world exploration.

This package provides a story-driven exploration experience guided by The Handler,
a mysterious figure who assigns cryptic missions based on simple player inputs.
"""

__version__ = "1.0.0"
__author__ = "Quest-Bot Team"

from .models import (
    Quest, Objective, Artifact, MemoryMoment, PlayerInput,
    ObjectiveStatus, QuestDifficulty
)
from .handler import TheHandler
from .logger import QuestLogger

__all__ = [
    "Quest",
    "Objective",
    "Artifact",
    "MemoryMoment",
    "PlayerInput",
    "ObjectiveStatus",
    "QuestDifficulty",
    "TheHandler",
    "QuestLogger",
]
