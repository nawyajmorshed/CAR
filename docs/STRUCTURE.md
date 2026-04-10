# Project Structure

This document describes the organization of the CAR racing game project.

## Root Level Files

- **main.py** - Entry point for the game (`python main.py`)
- **config.py** - Global configuration constants
- **debug.py** - Debugging utilities and performance monitoring
- **requirements.txt** - Python package dependencies
- **README.md** - Project overview and quick start
- **.gitignore** - Git ignore rules

## Directory Structure

```
CAR/
├── src/                          # Source code package
│   ├── __init__.py               # Package marker
│   ├── game/                     # Core game logic
│   │   ├── __init__.py
│   │   ├── car.py               # Car physics and AI
│   │   ├── world.py             # World generation
│   │   ├── chunk_manager.py     # Terrain chunk management
│   │   └── physics.py           # Physics calculations
│   └── graphics/                # Graphics and rendering
│       ├── __init__.py
│       ├── simple_renderer.py   # OpenGL renderer
│       ├── camera.py            # Camera system
│       ├── shader.py            # Shader management
│       └── texture_manager.py   # Texture loading
│
├── tests/                        # Testing files
│   ├── test.py                  # Unit tests
│   ├── run_test.py              # Test runner
│   └── diagnose.py              # Diagnostic tools
│
├── docs/                         # Documentation
│   ├── CAMERA_ARCHITECTURE.md
│   ├── CAMERA_QUICK_REFERENCE.md
│   ├── CHECKLIST.md
│   ├── CODE_REVIEW_COMPREHENSIVE.md
│   ├── CONFIGURATION.md
│   ├── INDEX.md
│   ├── MASTER_GUIDE.md
│   ├── PROJECT_OVERVIEW.md
│   ├── QUICK_START.md
│   └── START_HERE.md
│
├── tools/                        # Setup and utility scripts
│   ├── setup.py                 # Setup configuration
│   ├── start.bat                # Windows batch launcher
│   └── start.ps1                # PowerShell launcher
│
├── shaders/                      # GLSL shader files
│   ├── simple.vert
│   ├── simple.frag
│   ├── standard.vert
│   └── standard.frag
│
├── textures/                     # Texture assets
│
├── assets/                       # Other game assets
│
└── .venv/                        # Python virtual environment
```

## Module Organization

### Game Core (`src/game/`)

- **car.py** - `Car` and `AICar` classes for vehicle physics and AI
- **world.py** - `World` class for track generation and environment
- **chunk_manager.py** - `ChunkManager` for terrain optimization
- **physics.py** - `Physics` utility for movement calculations

### Graphics (`src/graphics/`)

- **simple_renderer.py** - `SimpleRenderer` for OpenGL rendering
- **camera.py** - `Camera` for third-person follow camera
- **shader.py** - `ShaderManager` for shader compilation and management
- **texture_manager.py** - `TextureManager` for texture loading

### Configuration & Utilities (Root)

- **config.py** - All game constants and settings
- **debug.py** - Performance monitoring, debug utilities
- **main.py** - Game loop and entry point

## How to Run

```bash
# From root directory
python main.py
```

The game will:
1. Load all modules from `src/` package
2. Initialize game, graphics, and physics
3. Display menu for game mode selection
4. Run 2-player or single-player vs AI race

## Import Examples

From `main.py`:
```python
from graphics import SimpleRenderer, Camera
from game import Car, World
import config
```

From within `src/game/car.py`:
```python
from .physics import Physics
from . import config  # Note: config is still in root
import config  # This also works due to sys.path setup
```

## Adding New Modules

- **Game Logic?** → Add to `src/game/`
- **Graphics/Rendering?** → Add to `src/graphics/`
- **Configuration?** → Update `config.py` in root
- **Tests?** → Add to `tests/`
- **Documentation?** → Add to `docs/`

## Notes

- `src/` is added to `sys.path` in `main.py`, so imports from root context work naturally
- All modules are importable via `from graphics import ...` or `from game import ...`
- The `__init__.py` files in each package export the main classes for clean imports
