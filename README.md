# Pokemon Dionisien

A Pokemon-inspired 2D RPG game built with Python and Pygame, featuring an explorable world with multiple maps, Pokemon mechanics, and a menu system.

## Features

### Game Mechanics
- **Tile-based Map System**: Multiple interconnected maps (indoor and outdoor) using TMX/Tiled format
- **Player Movement**: WASD/ZQSD controls with smooth 16-pixel grid-based movement and walking animations
- **Collision Detection**: Walls, objects, and map boundaries with pixel-perfect collision system
- **Map Transitions**: Seamless switching between indoor/outdoor maps with spawn point system
- **Pause Menu**: Press SPACE to open/close the menu

### Pokemon System
- **Complete Pokemon Data**: JSON-based pokemon system with stats, types, abilities, and moves
- **Pokemon Stats**: Full stat calculation system (HP, Attack, Defense, Speed, Special Attack, Special Defense)
- **Individual Values (IVs)**: Randomized IVs for each pokemon (1-31)
- **Effort Values (EVs)**: EV system implementation
- **Experience System**: Multiple experience growth curves (Fast, Medium Fast, Medium Slow, Slow, Erratic, Fluctuating)
- **Gender System**: Gender determination based on species female rate
- **Shiny Pokemon**: Rare shiny variants
- **Move System**: Complete move data with power, accuracy, PP, type, and battle effects
- **Moveset Generation**: Pokemon learn moves based on their level and moveset data

### UI System
- **Menu Interface**: Displays player's Pokemon team with stats
- **Interactive Buttons**: Clickable buttons with hover effects
- **Pokemon Boxes**: Detailed pokemon information display showing name, level, type, stats, and moveset

### Technical Features
- **Sprite Animation**: 4-directional character sprites with walking animations
- **Pyscroll Integration**: Smooth camera following and map rendering
- **Delta Time Movement**: Frame-independent movement system
- **Entity System**: Base entity class for all moving objects
- **Key Listener**: Custom keyboard input handling system

## Project Structure

```
pokemon_dionisien/
├── pokemondionisien/
│   ├── code/
│   │   ├── main.py          # Entry point
│   │   ├── game.py          # Main game loop and state management
│   │   ├── player.py        # Player controller with collision and map switching
│   │   ├── entity.py        # Base entity class for sprites
│   │   ├── pokemon.py       # Pokemon class with stats and mechanics
│   │   ├── move.py          # Move class for pokemon abilities
│   │   ├── map.py           # Map loading and switching system
│   │   ├── menu.py          # Pause menu and UI
│   │   ├── ui.py            # UI components (Buttons, PokemonBox)
│   │   ├── screen.py        # Display and framerate management
│   │   ├── keylistener.py   # Keyboard input handler
│   │   ├── switch.py        # Map transition trigger system
│   │   └── tool.py          # Utility functions (sprite splitting)
│   ├── assets/
│   │   ├── json/
│   │   │   ├── pokemon/     # Pokemon data files
│   │   │   ├── moves/       # Move data files
│   │   │   └── abilities/   # Ability data files
│   │   ├── map/             # TMX map files (map_start.tmx, house_0.tmx, etc.)
│   │   └── sprite/          # Character sprites
│   └── requirements.txt     # Python dependencies
└── README.md
```

## Requirements

- Python 3.x
- pygame
- pytmx
- pyscroll

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pokemon_dionisien
```

2. Install dependencies:
```bash
cd pokemondionisien
pip install -r requirements.txt
```

## How to Run

From the `pokemondionisien` directory, run:

```bash
python code/main.py
```

Or from the root directory:

```bash
python pokemondionisien/code/main.py
```

## Controls

- **Z/W**: Move up
- **Q/A**: Move left
- **S**: Move down
- **D**: Move right
- **SPACE**: Open/Close pause menu
- **M**: Print current position (debug)

## Game Architecture

### Game Loop
The main game loop ([game.py:20](pokemondionisien/code/game.py#L20)) handles:
1. Input processing
2. Pause menu state management
3. Map updates and player movement
4. Screen rendering at 144 FPS

### Player Movement System
- Grid-based movement with smooth animation ([entity.py:96](pokemondionisien/code/entity.py#L96))
- Collision checking before movement ([player.py:83](pokemondionisien/code/player.py#L83))
- Map transition detection ([player.py:74](pokemondionisien/code/player.py#L74))

### Map System
- TMX map loading with pytmx ([map.py:23](pokemondionisien/code/map.py#L23))
- Dynamic zoom based on map type (2x for outdoor, 3.75x for indoor)
- Collision objects parsed from map layers
- Switch/portal objects for map transitions
- Spawn point system for player positioning

### Pokemon Mechanics
- Pokemon creation from JSON data ([pokemon.py:147](pokemondionisien/code/pokemon.py#L147))
- Stat calculation using Gen 3+ formula ([pokemon.py:86](pokemondionisien/code/pokemon.py#L86))
- Experience calculation for 6 different growth rates ([pokemon.py:96](pokemondionisien/code/pokemon.py#L96))
- Random moveset generation based on level ([pokemon.py:117](pokemondionisien/code/pokemon.py#L117))

## Current Implementation Status

### ✅ Completed Features
- Player movement and animations
- Multiple map system with transitions
- Collision detection system
- Pokemon data structure and stat calculation
- Move system implementation
- Pause menu with pokemon display
- UI components (buttons, pokemon boxes)
- Experience and level system
- IV/EV system
- Gender and shiny mechanics

### 🚧 Not Yet Implemented
- Wild pokemon encounters
- Battle system
- Pokemon catching mechanism
- Inventory system
- NPC interactions
- Save/Load functionality
- Sound effects and music
- Pokemon evolution system (data structure exists)

## Development Notes

- The game uses a 16x16 pixel grid system for movement and collisions
- All maps must be created in Tiled Map Editor (.tmx format)
- Pokemon and move data follows the Pokemon game structure
- The coordinate system uses spawn points named `"spawn [map_name] [port_number]"` in TMX files

## Recent Updates (from Git History)

- Added collision detection system
- Implemented pause menu
- Fixed map object handling for interiors
- Added map switching functionality
- Integrated player spawn system

## License

[Add your license here]

## Credits

- Game assets and data based on Pokemon franchise
- Built with Pygame, Pytmx, and Pyscroll
