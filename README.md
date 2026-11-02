# The System V2

The second version of **The System**, a Solo Leveling-inspired personal progression system.

This repository contains an ongoing rebuild of the original project: [Venexs/The-System](https://github.com/Venexs/The-System).

The goal is to develop a more modular and maintainable version of the system, while expanding its progression mechanics, interface, and supporting features.

**This project is a work in progress and is not currently ready for public playtesting.** Its structure, features, and implementation are still subject to change.

## Why a New Version?

The original version of The System was the foundation for the project, but as more mechanics, interface elements, and supporting features were added, continuing to build on the existing structure became increasingly difficult.

The project needed more than incremental updates. Its underlying organisation needed to be reconsidered so that individual systems could be developed, modified, and expanded without making the entire application harder to maintain.

The purpose of V2 is to address this by:

- **Restructuring the codebase** — separating core mechanics, interface components, and supporting resources.
- **Improving maintainability** — making individual systems easier to modify without unnecessarily affecting others.
- **Supporting expansion** — providing a better foundation for new mechanics, features, and integrations.
- **Reworking existing systems** — allowing older mechanics to be redesigned rather than simply carried over.
- **Improving the interface** — developing a more flexible UI structure for different layouts, animations, and visual themes.

V2 is therefore not intended to be a direct continuation of the original codebase. It is a rebuild of the foundation that will allow The System to grow further.

## Current Direction

The System is designed around turning real-life activities and personal goals into an RPG-style progression experience.

The project includes work on:

- **Player progression** — levels, stats, ranks, titles, and rewards.
- **Quests** — daily quests, random quests, secret quests, and penalties.
- **Dungeons** — ranked dungeon content, encounters, and the Demon Castle.
- **Skills and equipment** — skill progression, inventory, equipment, and item management.
- **Economy** — coins, shops, rewards, and the Night Market.
- **Personal tracking** — activity-related statistics, workout data, and calorie tracking.
- **Interface** — custom Tkinter windows, animated elements, visual effects, and sound effects.
- **Themes and assets** — Anime and Manhwa visual styles, with configurable interface elements.

These are areas of development, not a guarantee that every feature is currently complete or functional.

## Project Structure

| Directory / File | Purpose |
|---|---|
| `thesystem/` | Core progression systems and game logic |
| `anime/` | Interface components and animations |
| `Files/Data/` | Game content, item definitions, quests, and other data |
| `Files/Player Data/` | Player status, settings, inventory, and progression data |
| `Files/Mod/` | Visual themes, images, sounds, and related assets |
| `Files/Workout/` | Workout-related data |
| `anime_temps.py` | Interface setup and shared UI utilities |
| `default.py` | Default interface window |
| `long.py` | Main expanded interface |
| `small.py` | Compact interface |
| `sfx.py` | Sound-effect handling |

## Development Status

The project is undergoing restructuring and refactoring. Existing systems may be incomplete, experimental, or subject to replacement.

There is currently no supported public installation or launch procedure. The repository should be treated as a development snapshot rather than a playable release.

## Relationship to the Original Project

The System V2 is a separate development direction built from the original [The System](https://github.com/Venexs/The-System).

Rather than continuing to expand the original implementation, V2 aims to establish a cleaner foundation for the project's long-term development while retaining its central concept: turning real-life progression into an RPG-style system.
