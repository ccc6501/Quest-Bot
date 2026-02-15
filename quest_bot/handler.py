"""
The Handler: The mysterious figure that generates and delivers quests.
"""

import random
from datetime import datetime
from .models import (
    Quest, Objective, Artifact, PlayerInput,
    QuestDifficulty, ObjectiveStatus
)


class TheHandler:
    """
    The Handler is a mysterious figure that transforms mundane inputs
    into extraordinary missions. They communicate in cryptic transmissions,
    layering dungeon-crawl style objectives onto everyday experiences.
    """
    
    def __init__(self):
        self.quest_counter = 0
        self.signature_phrases = [
            "The path reveals itself to those who dare to look.",
            "What seems ordinary conceals the extraordinary.",
            "Trust your instincts. Question everything.",
            "The world is more than it appears.",
            "Every shadow holds a secret.",
        ]
    
    def generate_quest(self, player_input: PlayerInput) -> Quest:
        """
        Generate a bespoke quest based on player input.
        
        Args:
            player_input: The player's context (time, location, conditions, mood)
        
        Returns:
            A complete Quest object with cryptic transmission and objectives
        """
        self.quest_counter += 1
        quest_id = f"QUEST-{datetime.now().strftime('%Y%m%d')}-{self.quest_counter:03d}"
        
        # Determine difficulty based on conditions and mood
        difficulty = self._determine_difficulty(player_input)
        
        # Generate quest components
        title = self._generate_title(player_input)
        transmission = self._generate_transmission(player_input, difficulty)
        objectives = self._generate_objectives(player_input, difficulty)
        side_intelligence = self._generate_side_intelligence(player_input)
        artifacts = self._generate_artifacts(player_input)
        
        # Create the quest
        quest = Quest(
            quest_id=quest_id,
            title=title,
            transmission=transmission,
            objectives=objectives,
            side_intelligence=side_intelligence,
            artifacts=artifacts,
            difficulty=difficulty,
            player_input=player_input
        )
        
        return quest
    
    def _determine_difficulty(self, player_input: PlayerInput) -> QuestDifficulty:
        """Determine quest difficulty based on conditions and mood."""
        challenging_conditions = ["foggy", "rainy", "stormy", "snowy"]
        challenging_moods = ["mysterious", "contemplative", "intense"]
        
        challenge_score = 0
        if any(cond in player_input.conditions.lower() for cond in challenging_conditions):
            challenge_score += 1
        if any(mood in player_input.mood.lower() for mood in challenging_moods):
            challenge_score += 1
        
        if challenge_score >= 2:
            return QuestDifficulty.CHALLENGING
        elif challenge_score == 1:
            return QuestDifficulty.STANDARD
        else:
            return QuestDifficulty.RECONNAISSANCE
    
    def _generate_title(self, player_input: PlayerInput) -> str:
        """Generate a cryptic quest title."""
        time_themes = {
            "morning": ["Dawn", "First Light", "Awakening"],
            "afternoon": ["Meridian", "High Sun", "Zenith"],
            "evening": ["Twilight", "Dusk", "Threshold"],
            "night": ["Midnight", "Shadow", "Nocturne"],
        }
        
        location_themes = {
            "urban": ["Streets", "Labyrinth", "Nexus", "Grid"],
            "forest": ["Grove", "Wilds", "Canopy", "Path"],
            "suburban": ["Boundary", "Edge", "Periphery", "Quarter"],
            "park": ["Garden", "Commons", "Green", "Haven"],
            "downtown": ["Core", "Heart", "Center", "Hub"],
        }
        
        # Find matching themes
        time_key = next((k for k in time_themes if k in player_input.time.lower()), "afternoon")
        location_key = next((k for k in location_themes if k in player_input.location.lower()), "urban")
        
        time_word = random.choice(time_themes[time_key])
        location_word = random.choice(location_themes[location_key])
        
        templates = [
            f"The {time_word} {location_word}",
            f"Operation: {location_word} {time_word}",
            f"{time_word} of the {location_word}",
            f"The {location_word} Protocol",
        ]
        
        return random.choice(templates)
    
    def _generate_transmission(self, player_input: PlayerInput, difficulty: QuestDifficulty) -> str:
        """Generate the cryptic transmission message."""
        greeting = random.choice([
            "Agent,",
            "Operative,",
            "Seeker,",
            "Wanderer,",
        ])
        
        context = self._contextualize_input(player_input)
        
        mission_briefing = self._generate_mission_briefing(player_input, difficulty)
        
        signature = random.choice(self.signature_phrases)
        
        transmission = f"""{greeting}

{context}

{mission_briefing}

Your mission parameters are encrypted below. Decode them through direct experience.

{signature}

— The Handler"""
        
        return transmission
    
    def _contextualize_input(self, player_input: PlayerInput) -> str:
        """Create atmospheric context from player input."""
        time_desc = {
            "morning": "as dawn breaks over the horizon",
            "afternoon": "while the sun reaches its apex",
            "evening": "as twilight descends upon us",
            "night": "under the cover of darkness",
        }
        
        conditions_desc = {
            "sunny": "The light reveals all—or does it?",
            "rainy": "The rain washes away the mundane.",
            "foggy": "The fog conceals more than geography.",
            "snowy": "Each snowflake carries a secret.",
            "cloudy": "The clouds mirror the mystery below.",
            "clear": "Clarity of sky, obscurity of purpose.",
        }
        
        time_key = next((k for k in time_desc if k in player_input.time.lower()), "afternoon")
        cond_key = next((k for k in conditions_desc if k in player_input.conditions.lower()), "clear")
        
        context = f"The coordinates indicate {player_input.location}, {time_desc[time_key]}. "
        context += conditions_desc[cond_key]
        
        return context
    
    def _generate_mission_briefing(self, player_input: PlayerInput, difficulty: QuestDifficulty) -> str:
        """Generate the main mission briefing."""
        mood_missions = {
            "adventurous": "Your spirit of adventure will be tested in ways you cannot yet imagine.",
            "contemplative": "This mission requires observation more than action. Watch. Listen. Understand.",
            "energetic": "Channel that energy into purpose. Move with intention.",
            "mysterious": "You seek mystery, and mystery has found you.",
            "curious": "Your curiosity is both your greatest asset and potential liability.",
        }
        
        mood_key = next((k for k in mood_missions if k in player_input.mood.lower()), "adventurous")
        
        difficulty_notes = {
            QuestDifficulty.RECONNAISSANCE: "This is a reconnaissance mission. Gather intelligence. Report findings.",
            QuestDifficulty.STANDARD: "A standard operation, but do not mistake routine for safety.",
            QuestDifficulty.CHALLENGING: "This mission exceeds normal parameters. Proceed with heightened awareness.",
            QuestDifficulty.LEGENDARY: "Only the most dedicated operatives receive such assignments.",
        }
        
        briefing = f"{mood_missions[mood_key]} {difficulty_notes[difficulty]}"
        
        return briefing
    
    def _generate_objectives(self, player_input: PlayerInput, difficulty: QuestDifficulty) -> list:
        """Generate quest objectives."""
        base_objectives = [
            "Identify three points of interest that others overlook",
            "Document the hidden patterns in your surroundings",
            "Make contact with an unexpected element",
            "Discover the story this place wants to tell",
            "Find evidence of change—something that was, is, or will be different",
        ]
        
        location_specific = {
            "urban": [
                "Locate the oldest visible architectural detail",
                "Find three examples of nature reclaiming space",
                "Identify a gathering place for secrets",
            ],
            "forest": [
                "Discover signs of unseen wildlife",
                "Locate a natural landmark that serves as a waypoint",
                "Find evidence of seasonal transformation",
            ],
            "suburban": [
                "Identify the boundary between the ordinary and extraordinary",
                "Locate a space between destinations",
                "Document the personality of the neighborhood",
            ],
            "park": [
                "Find the heart of this green space",
                "Discover where people and nature intersect",
                "Locate the oldest living thing",
            ],
        }
        
        # Select objectives based on difficulty
        num_objectives = {
            QuestDifficulty.RECONNAISSANCE: 3,
            QuestDifficulty.STANDARD: 4,
            QuestDifficulty.CHALLENGING: 5,
            QuestDifficulty.LEGENDARY: 6,
        }[difficulty]
        
        # Mix base and location-specific objectives
        location_key = next((k for k in location_specific if k in player_input.location.lower()), None)
        
        available_objectives = base_objectives.copy()
        if location_key:
            available_objectives.extend(location_specific[location_key])
        
        selected = random.sample(available_objectives, min(num_objectives, len(available_objectives)))
        
        return [Objective(description=obj) for obj in selected]
    
    def _generate_side_intelligence(self, player_input: PlayerInput) -> list:
        """Generate side intelligence and hints."""
        intelligence = [
            "Sometimes the most important discoveries happen between objectives.",
            "Pay attention to transitions—doorways, corners, edges, borders.",
            "What makes a sound? What should make a sound but doesn't?",
            "The Handler is always watching, but never where you expect.",
        ]
        
        condition_intel = {
            "rainy": "Rain reveals textures usually hidden. Notice reflections.",
            "foggy": "In fog, trust your other senses more than sight.",
            "sunny": "Shadows tell their own stories. Follow them.",
            "snowy": "Fresh snow is a canvas. What marks has life left?",
        }
        
        time_intel = {
            "morning": "Morning light is honest. What does it illuminate?",
            "evening": "Twilight is the hour of transformation. Be present for it.",
            "night": "Darkness heightens awareness. What emerges?",
        }
        
        # Add contextual intelligence
        cond_key = next((k for k in condition_intel if k in player_input.conditions.lower()), None)
        if cond_key:
            intelligence.append(condition_intel[cond_key])
        
        time_key = next((k for k in time_intel if k in player_input.time.lower()), None)
        if time_key:
            intelligence.append(time_intel[time_key])
        
        return random.sample(intelligence, min(3, len(intelligence)))
    
    def _generate_artifacts(self, player_input: PlayerInput) -> list:
        """Generate artifacts to discover."""
        artifacts_templates = [
            ("The Overlooked Detail", "Something everyone sees but no one notices"),
            ("Echo of Purpose", "Evidence of this place's original or hidden function"),
            ("Natural Intrusion", "Where the natural world asserts itself"),
            ("Human Trace", "A mark left by someone, intentional or not"),
            ("Temporal Marker", "Something that reveals the passage of time"),
        ]
        
        location_artifacts = {
            "urban": [
                ("Ghost Sign", "Faded advertising or signage from another era"),
                ("Unofficial Path", "A shortcut created by repeated human passage"),
                ("Utility Poetry", "Infrastructure that's accidentally beautiful"),
            ],
            "forest": [
                ("Ancient One", "The oldest tree you can find"),
                ("Wildlife Gallery", "Signs of animal activity"),
                ("Stone Memory", "A rock formation with a story"),
            ],
            "suburban": [
                ("Garden Guardian", "Unexpected greenery in an unlikely place"),
                ("Neighborhood Icon", "A landmark known only to locals"),
                ("Time Capsule", "Something preserved from an earlier decade"),
            ],
        }
        
        # Select artifacts
        available = artifacts_templates.copy()
        location_key = next((k for k in location_artifacts if k in player_input.location.lower()), None)
        if location_key:
            available.extend(location_artifacts[location_key])
        
        selected = random.sample(available, min(3, len(available)))
        
        return [Artifact(name=name, description=desc) for name, desc in selected]
