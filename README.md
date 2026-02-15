# Quest-Bot 🗺️

**An adventure quest system for real-world exploration**

Quest-Bot transforms everyday life into a story-driven adventure. Guided by a mysterious figure known as **The Handler**, players receive cryptic missions that layer dungeon-crawl objectives onto their daily experiences. Simple inputs—time, location, conditions, mood—become bespoke quests with objectives, side intelligence, artifacts, and memory moments.

## 🎭 The Experience

Quest-Bot is designed for those who seek the extraordinary in the ordinary. Each quest unfolds like an interactive narrative, encouraging mindful exploration and discovery in familiar places. Progress is logged, creating lasting narrative records of your adventures.

### Key Features

- 🎯 **Cryptic Missions**: The Handler delivers bespoke quests as mysterious transmissions
- 🗺️ **Real-World Integration**: Quests adapt to your time, location, weather, and mood
- 📋 **Dynamic Objectives**: Complete goals that encourage observation and exploration
- ⚡ **Artifacts**: Discover hidden elements in your surroundings
- 📝 **Memory Moments**: Record significant discoveries as lasting narrative records
- 📊 **Progress Tracking**: All quests are logged with detailed narrative summaries
- 🎲 **Variable Difficulty**: From reconnaissance to legendary missions

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ccc6501/Quest-Bot.git
cd Quest-Bot

# Install dependencies
pip install -r requirements.txt
```

### Running Quest-Bot

```bash
python quest_bot_cli.py
```

## 📖 How It Works

### 1. Provide Context
When you request a quest, The Handler asks for simple inputs:
- **Time**: morning, afternoon, evening, night
- **Location**: urban downtown, forest trail, suburban neighborhood, park, etc.
- **Conditions**: sunny, rainy, foggy, snowy, cloudy, clear
- **Mood**: adventurous, contemplative, energetic, mysterious, curious

### 2. Receive Your Mission
The Handler analyzes your inputs and generates:
- A **cryptic transmission** setting the tone
- **Objectives** tailored to your environment
- **Artifacts** to discover
- **Side intelligence** providing hints and context

### 3. Embark on Your Quest
Head out into the real world and:
- Complete objectives through observation and exploration
- Discover artifacts in your surroundings
- Record memory moments of significant discoveries
- Follow side intelligence for deeper insights

### 4. Log Your Progress
Quest-Bot automatically tracks:
- Objective completion with notes
- Artifact discoveries
- Memory moments with timestamps
- Final narrative summaries

## 🎮 Example Quest

```
╔══════════════════════════════════════════════════════════════════╗
║                    INCOMING TRANSMISSION                         ║
╚══════════════════════════════════════════════════════════════════╝

Operative,

The coordinates indicate urban downtown, as twilight descends upon us. 
The fog conceals more than geography.

This mission requires observation more than action. Watch. Listen. 
Understand. A standard operation, but do not mistake routine for safety.

Your mission parameters are encrypted below. Decode them through direct 
experience.

What seems ordinary conceals the extraordinary.

— The Handler

═══════════════════════════════════════════════════════════════════
QUEST: The Twilight Nexus
Mission ID: QUEST-20260215-001
Difficulty: STANDARD
═══════════════════════════════════════════════════════════════════

OBJECTIVES:
  1. Identify three points of interest that others overlook
  2. Document the hidden patterns in your surroundings
  3. Locate the oldest visible architectural detail
  4. Find three examples of nature reclaiming space

ARTIFACTS TO DISCOVER:
  • The Overlooked Detail: Something everyone sees but no one notices
  • Ghost Sign: Faded advertising or signage from another era
  • Natural Intrusion: Where the natural world asserts itself

SIDE INTELLIGENCE:
  • In fog, trust your other senses more than sight.
  • Pay attention to transitions—doorways, corners, edges, borders.
  • Twilight is the hour of transformation. Be present for it.
```

## 🏗️ Architecture

### Core Components

- **`quest_bot/models.py`**: Data models (Quest, Objective, Artifact, MemoryMoment)
- **`quest_bot/handler.py`**: The Handler AI that generates quests
- **`quest_bot/logger.py`**: Quest logging and narrative record system
- **`quest_bot_cli.py`**: Interactive command-line interface

### Data Flow

1. Player provides context (PlayerInput)
2. The Handler generates a quest (Quest object)
3. QuestLogger tracks progress
4. Player completes objectives, discovers artifacts, adds memory moments
5. QuestLogger generates narrative summaries

## 🎯 Quest Structure

### Quest Components

```python
Quest:
  - quest_id: Unique identifier
  - title: Cryptic quest name
  - transmission: The Handler's message
  - objectives: List of goals to complete
  - side_intelligence: Hints and context
  - artifacts: Items to discover
  - memory_moments: Player-recorded discoveries
  - difficulty: reconnaissance, standard, challenging, legendary
```

### Difficulty Levels

- **Reconnaissance**: 3 objectives, exploration-focused
- **Standard**: 4 objectives, balanced challenge
- **Challenging**: 5 objectives, requires deeper observation
- **Legendary**: 6 objectives, for dedicated operatives

## 📚 Usage Examples

### Starting a Quest

```python
from quest_bot import TheHandler, QuestLogger, PlayerInput

# Create instances
handler = TheHandler()
logger = QuestLogger()

# Provide context
player_input = PlayerInput(
    time="evening",
    location="urban downtown",
    conditions="foggy",
    mood="mysterious"
)

# Generate quest
quest = handler.generate_quest(player_input)
logger.start_quest(quest)

# Display transmission
print(quest.transmission)
```

### Tracking Progress

```python
# Complete an objective
quest.objectives[0].complete("Found a century-old cornerstone")
logger.update_quest()

# Discover an artifact
quest.artifacts[0].discover("Spotted faded Coca-Cola ad from the 1950s")
logger.update_quest()

# Add a memory moment
logger.add_memory_moment(
    title="The Hidden Garden",
    description="Found wildflowers growing through sidewalk cracks",
    location_hint="Corner of 5th and Main"
)

# Complete the quest
logger.complete_quest()
```

## 🗂️ Quest Logs

All quests are saved in the `quest_logs/` directory:
- **JSON files**: Complete quest data for loading/analysis
- **Narrative summaries**: Human-readable quest reports

Example narrative summary:
```
======================================================================
QUEST LOG: The Twilight Nexus
Mission ID: QUEST-20260215-001
Difficulty: STANDARD
Completed: 2026-02-15 18:45:32
======================================================================

ORIGINAL TRANSMISSION:
[Full transmission text...]

OBJECTIVES:
✓ 1. Identify three points of interest that others overlook
   Notes: Found a century-old cornerstone
✓ 2. Document the hidden patterns in your surroundings
...

ARTIFACTS:
★ Ghost Sign: Faded advertising or signage from another era
   Discovery: Spotted faded Coca-Cola ad from the 1950s
...

MEMORY MOMENTS:
• The Hidden Garden
  Found wildflowers growing through sidewalk cracks
  Location: Corner of 5th and Main
  Time: 2026-02-15 18:30:15
...
```

## 🎨 Customization

The Handler's personality and quest generation can be customized by modifying:
- Signature phrases in `handler.py`
- Quest templates and themes
- Objective pools
- Artifact types
- Difficulty parameters

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional quest themes and templates
- More location-specific content
- Integration with mapping services
- Photo/media attachment for memory moments
- Multi-player quest sharing

## 📜 License

This project is open source. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

Quest-Bot was created to encourage mindful exploration and discovery in everyday environments. Every quest is an invitation to see the world with fresh eyes.

---

*"The path reveals itself to those who dare to look."*

**— The Handler** 
