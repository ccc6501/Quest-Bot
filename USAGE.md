# Quest-Bot Usage Guide

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/ccc6501/Quest-Bot.git
cd Quest-Bot

# Install dependencies
pip install -r requirements.txt
```

## Running Quest-Bot

### Interactive CLI

The easiest way to use Quest-Bot is through the interactive command-line interface:

```bash
python quest_bot_cli.py
```

### Example Session

```
╔══════════════════════════════════════════════════════════════════╗
║                          QUEST-BOT                               ║
║                   Adventure Quest System                         ║
╚══════════════════════════════════════════════════════════════════╝

1. Request New Quest
2. View Past Quests
0. Exit

> 1

MISSION PARAMETERS
Time of day: evening
Location: urban downtown
Current conditions: foggy
Your mood: mysterious

[The Handler generates quest...]

INCOMING TRANSMISSION FROM THE HANDLER
[Cryptic mission briefing...]

QUEST: Twilight of the Grid
Difficulty: CHALLENGING

OBJECTIVES:
  1. Discover the story this place wants to tell
  2. Locate the oldest visible architectural detail
  ...

[Accept and embark on quest]
```

## Using the Python API

### Basic Quest Generation

```python
from quest_bot import TheHandler, QuestLogger, PlayerInput

# Initialize
handler = TheHandler()
logger = QuestLogger()

# Create player input
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
quest.objectives[0].complete("Found cornerstone from 1887")
logger.update_quest()

# Discover an artifact
quest.artifacts[0].discover("Old hardware store sign on brick wall")
logger.update_quest()

# Add a memory moment
logger.add_memory_moment(
    title="The Hidden Garden",
    description="Wildflowers in sidewalk cracks",
    location_hint="Corner of 5th and Main"
)

# View progress
print(logger.generate_progress_report())

# Complete quest
logger.complete_quest()
```

## Quest Input Parameters

### Time
- `morning` - Dawn to mid-morning
- `afternoon` - Midday to early evening
- `evening` - Twilight to dusk
- `night` - After dark

### Location Types
- `urban downtown` - City centers, business districts
- `urban` - General city areas
- `forest` or `forest trail` - Natural wooded areas
- `suburban` or `suburban neighborhood` - Residential areas
- `park` - Parks, green spaces, commons

### Conditions
- `sunny` - Clear, bright weather
- `rainy` - Wet conditions
- `foggy` - Low visibility, atmospheric
- `snowy` - Winter conditions
- `cloudy` - Overcast
- `clear` - Good visibility

### Mood
- `adventurous` - Energy-focused, action-oriented
- `contemplative` - Observation-focused, thoughtful
- `energetic` - Movement-focused, dynamic
- `mysterious` - Discovery-focused, atmospheric
- `curious` - Exploration-focused, investigative

## Quest Difficulty

The Handler automatically determines difficulty based on conditions and mood:

- **Reconnaissance** (3 objectives) - Straightforward exploration
- **Standard** (4 objectives) - Balanced challenge
- **Challenging** (5 objectives) - Requires deeper observation
- **Legendary** (6 objectives) - For dedicated operatives

Challenging conditions (foggy, rainy, stormy) and moods (mysterious, contemplative) increase difficulty.

## Quest Components

### Objectives
Clear goals to accomplish during your quest. Each can be completed with optional notes:

```python
objective.complete("Your notes about completion")
```

### Artifacts
Special items or discoveries to find. Each artifact has a name and description:

```python
artifact.discover("Description of how you found it")
```

### Memory Moments
Significant experiences or discoveries you want to remember:

```python
logger.add_memory_moment(
    title="Moment Title",
    description="What happened",
    location_hint="Where it happened (optional)"
)
```

### Side Intelligence
Hints and contextual information from The Handler to guide your exploration.

## Quest Logs

All quests are saved in the `quest_logs/` directory:

### JSON Logs
Complete quest data in machine-readable format:
```
quest_logs/QUEST-20260215-001.json
```

### Narrative Summaries
Human-readable quest reports:
```
quest_logs/QUEST-20260215-001_NARRATIVE.txt
```

Example narrative summary structure:
```
QUEST LOG: [Title]
Mission ID: [ID]
Difficulty: [Level]

ORIGINAL TRANSMISSION:
[Full transmission text]

OBJECTIVES:
✓ Completed objectives with notes
○ Incomplete objectives

ARTIFACTS:
★ Discovered artifacts with discovery notes
☆ Undiscovered artifacts

MEMORY MOMENTS:
• Title
  Description
  Location
  Timestamp

SIDE INTELLIGENCE:
• Hints provided
```

## Tips for Best Experience

1. **Go Outside**: Quest-Bot is designed for real-world exploration
2. **Take Your Time**: Observe, don't rush
3. **Be Present**: Engage with your surroundings
4. **Record Details**: Add notes to objectives and artifacts
5. **Capture Moments**: Use memory moments for significant discoveries
6. **Review Logs**: Read narrative summaries to relive your adventures

## Advanced Usage

### Custom Quest Logs Directory

```python
logger = QuestLogger(log_directory="/path/to/custom/logs")
```

### Viewing Past Quests

```python
# List all quests
quest_ids = logger.list_quests()

# Load a specific quest
quest_data = logger.load_quest("QUEST-20260215-001")
```

### Generating Progress Reports

```python
# Get current quest progress
report = logger.generate_progress_report()
print(report)
```

## Troubleshooting

### No Dependencies Installed
```bash
pip install -r requirements.txt
```

### Quest Logs Not Saving
Check that the `quest_logs/` directory has write permissions.

### CLI Not Responding
Use Ctrl+C to exit gracefully. The Handler will save your progress.

## Examples

See `example.py` for a complete demonstration:
```bash
python example.py
```

Run tests to verify installation:
```bash
python test_quest_bot.py
```

---

*"The path reveals itself to those who dare to look."*

**— The Handler**
