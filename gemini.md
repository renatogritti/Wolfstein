# Doom 3D Clone Documentation

## Project Overview
This project is a simplified "Doom clone" implemented in Python using Pygame and a raycasting engine. It features a retro-style 3D view, player movement, and map loading from external text files.

## Directory Structure
- `game.py`: The main entry point for the game.
- `settings.py`: Contains configuration constants (resolution, FPS, colors).
- `map.py`: Handles map loading and processing.
- `player.py`: Implements player movement and camera logic.
- `raycasting.py`: Example of a raycasting engine implementation.
- `renderer.py`: Handles rendering the 3D scene.
- `assets/`: Directory for game assets (e.g., maps).

## How to Run
1. Ensure Python 3.x is installed.
2. Install Pygame: `pip install -r requirements.txt` (or manually via `pip install pygame`).
3. Run the game: `python game.py`.

## Controls
- **W / Up Arrow**: Move forward
- **S / Down Arrow**: Move backward
- **A / Left Arrow**: Rotate left (or strafe left, depending on implementation preference)
- **D / Right Arrow**: Rotate right (or strafe right)
- **Esc**: Exit the game

## Technical Details
The game uses a raycasting algorithm to simulate 3D environments from a 2D grid map. The raycasting engine calculates the distance to walls for each vertical strip of the screen, creating the 3D perspective.

### Map Format
Maps are defined in text files within the `assets/` directory. Each character represents a block in the grid:
- `1`: Wall
- `Wait, `.` or space`: Empty space
- `P`: Player start position (optional, default at fixed location)

Example `map.txt`:
```
1111111111
1........1
1..111...1
1........1
1111111111
```
