# 🏎️ 3D Racing Game - Open World Edition

A large-scale, open-world 3D racing game built with Python using PyOpenGL, Pygame, and NumPy. Features Modern OpenGL (Core Profile 3.3+), chunk-based world streaming, advanced car physics, and a dynamic environment.

## 🌍 Features

### World System
- ✅ **Chunk-based World Loading**: Dynamic chunk loading/unloading for infinite-feeling map
- ✅ **Large-Scale Map**: Multiple kilometers of virtual space
- ✅ **Multiple Zones**: City (dense), Highway (fast), Rural (sparse) areas
- ✅ **Procedurally Generated Roads**: Curved roads with elevation changes
- ✅ **Bridges & Structures**: Elevated road segments and infrastructure

### Car Physics
- ✅ **Advanced Physics**: Acceleration, braking, friction, drag
- ✅ **Smooth Steering**: LERP-based steering with speed-dependent sensitivity
- ✅ **Terrain-Based Grip**: Different friction on road/dirt/grass
- ✅ **Drift System**: High-speed drift effects
- ✅ **Multiple Car Types**: Sports, Truck, Rally cars with unique stats

### Visual Features
- ✅ **Modern OpenGL**: Core Profile 3.3+ rendering
- ✅ **Phong Lighting**: Directional sunlight and ambient lighting
- ✅ **Atmospheric Effects**: Fog rendering for distance effect
- ✅ **Environment Objects**: Buildings, trees, street lights, billboards
- ✅ **Dynamic Camera**: Third-person follow camera with smooth lag

### Gameplay
- ✅ **Nitro System**: Speed boost with visual FOV effect
- ✅ **Speed Meter**: Dynamic speed calculations
- ✅ **Off-Road Penalties**: Reduced grip on non-road surfaces
- ✅ **Continuous Play**: Drive long distances without boundaries

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **GPU**: Any modern GPU with OpenGL 3.3+ support
- **Storage**: ~500MB free space

### Required Libraries
All dependencies are listed in `requirements.txt`:
- **pygame-ce** 2.5.7 - Game framework and windowing
- **PyOpenGL** 3.1.10 - OpenGL bindings
- **NumPy** 2.4.4+ - Numerical computations
- **Pillow** 12.2.0+ - Image loading for textures

## 🚀 Installation

### Step 1: Clone or Download Project
```bash
# Using Git
git clone https://github.com/yourusername/CAR.git
cd CAR

# OR download ZIP and extract it
```

### Step 2: Install Python 3.8+

**Windows:**
- Download from https://www.python.org/downloads/
- Run installer, **IMPORTANT: Check "Add Python to PATH"**
- Verify: Open Command Prompt and type `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Verify
python3 --version
```

### Step 3: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### Step 4: Install Dependencies
```bash
# Upgrade pip first (important for Windows!)
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**If you encounter issues:**
```bash
# Try with specific versions
pip install pygame-ce==2.5.7 PyOpenGL==3.1.10 numpy==2.4.4 Pillow==12.2.0
```

### Step 5: Run the Game
```bash
python main.py
```

The game window should open with the main menu. Use arrow keys to select game mode, then press ENTER.

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'pygame'" 
- ✅ Solution: You forgot to activate virtual environment or install requirements
- Run: `pip install pygame-ce`

### "ModuleNotFoundError: No module named 'OpenGL'"
- ✅ Solution: Run `pip install PyOpenGL`

### OpenGL Error / Black Screen
- ✅ Update your GPU drivers to latest version
- Check if your GPU supports OpenGL 3.3+
- Try: `glxinfo | grep -i opengl` on Linux to check version

### "AttributeError: module 'pygame' has no attribute..."
- ✅ Make sure you have pygame-ce (not pygame)
- Run: `pip uninstall pygame` then `pip install pygame-ce==2.5.7`

### Game runs slow / low FPS
- ✅ Lower render distance in config.py: `RENDER_DISTANCE = 2`
- ✅ Reduce window size: `WINDOW_WIDTH = 800`, `WINDOW_HEIGHT = 600`
- ✅ Close other applications

### ImportError in src.game or src.graphics
- ✅ Make sure you're running from project root directory
- ✅ Check that src/ folder contains `__init__.py` files
- ✅ Run: `python main.py` (not from src/ subdirectory)

---

## 🎮 Controls

### Player 1 (Single Player or Multiplayer)
| Key | Action |
|-----|--------|
| **W** | Accelerate forward |
| **S** | Reverse |
| **A** | Steer left |
| **D** | Steer right |
| **Left Shift** | Activate Nitro boost |
| **ESC** | Exit game |

### Player 2 (Multiplayer Only)
| Key | Action |
|-----|--------|
| **↑ Arrow Up** | Accelerate forward |
| **↓ Arrow Down** | Reverse |
| **← Arrow Left** | Steer left |
| **→ Arrow Right** | Steer right |
| **Right Shift** | Activate Nitro boost |

### Menu Navigation
| Key | Action |
|-----|--------|
| **↑ / ↓ Arrow Keys** | Select game mode |
| **ENTER** | Start race |
| **ESC** | Quit |

## 🎯 How to Play

### Game Modes
1. **Single Player vs AI** (Recommended)
   - Race against 6 AI-controlled cars
   - Collect power-up balls to boost speed
   - Cross the finish line before AI cars
   - View live race standings

2. **2-Player Local Multiplayer**
   - Split-screen racing with a friend
   - Top player (red, WASD controls), Bottom player (green, arrows)
   - First player to finish line wins
   - Compete for power-ups

### Power-Ups
- 🟢 **Green Ball**: +4x Speed for 3 seconds (collect to boost)
- 🔴 **Red Ball**: -4x Speed for 3 seconds (slow down - avoid!)
- Balls spawn throughout the track
- Disappear immediately when collected
- Each power-up lasts exactly 3 seconds

### Nitro System
- **Meter**: Located in HUD (accumulates when not in use)
- **Max**: 100 units
- **Usage**: Hold LEFT SHIFT (Player 1) or RIGHT SHIFT (Player 2)
- **Effect**: +50% speed boost + expanded field of view
- **Strategy**: Save for climbs or tight turns

### Race Strategy
1. Collect green balls for speed boosts when behind
2. Avoid red balls or position yourself to use them
3. Use nitro on straightaways for maximum distance gain
4. Stay on the road for better grip
5. Cut corners to shorten the path to finish line

## 📁 Project Structure

```
CAR/
├── main.py                     # Entry point and game loop
├── config.py                   # Configuration constants
├── physics.py                  # Physics calculations
├── debug.py                    # Debug utilities
├── requirements.txt            # Python dependencies
│
├── src/
│   ├── game/                   # Game logic package
│   │   ├── __init__.py
│   │   ├── car.py             # Player and AI car physics
│   │   ├── world.py           # Track generation and AI
│   │   ├── chunk_manager.py   # Chunk-based optimization
│   │
│   └── graphics/              # Rendering package
│       ├── __init__.py
│       ├── simple_renderer.py # OpenGL rendering engine
│       ├── camera.py          # Third-person camera system
│       ├── shader.py          # GLSL shader management
│       └── texture_manager.py # Texture loading
│
├── shaders/                    # GLSL shader files
│   ├── standard.vert
│   ├── standard.frag
│   ├── simple.vert
│   └── simple.frag
│
├── textures/                   # Texture assets
├── tests/                      # Testing utilities
│   ├── diagnose.py            # System diagnostics
│   └── run_test.py            # Rendering tests
│
├── docs/                       # Documentation
└── README.md                   # This file
```

## ⚙️ Configuration

Edit `config.py` to customize game settings:

```python
# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Physics
MAX_SPEED = 500.0
ACCELERATION = 2500.0
BRAKE_DECELERATION = 120.0

# Nitro system
MAX_NITRO = 100.0
NITRO_BOOST_MULTIPLIER = 1.5
NITRO_FOV_BOOST = 15.0

# Camera
CAMERA_FOLLOW_HEIGHT = 3.0
CAMERA_FOLLOW_DISTANCE = 12.0

# World
CHUNK_SIZE = 500.0
RENDER_DISTANCE = 3
```



## 🚗 Car Types

### Sports Car
- Max Speed: 200 units/sec
- Acceleration: 80
- Handling: 0.95 (excellent)
- Weight: 1.0 (standard)

### Truck
- Max Speed: 120 units/sec
- Acceleration: 30
- Handling: 0.70 (sluggish)
- Weight: 2.0 (heavy)

### Rally Car
- Max Speed: 180 units/sec
- Acceleration: 75
- Handling: 0.98 (best)
- Weight: 0.9 (light)

## 🗺️ World Zones

### City Zone (Center)
- Dense buildings and street lights
- Narrow roads with tight turns
- Grid-based street system
- Traffic-like environment

### Highway Zone (Middle Ring)
- Fast, curved roads
- Minimal obstacles
- Open feel
- Elevation changes

### Rural Zone (Outer Ring)
- Trees and sparse environment
- Natural terrain
- Long straight roads
- Off-road areas

## ⚙️ Game Systems

### Chunk Management
- Automatically loads chunks as you drive
- Unloads chunks that are far away
- Seamless world continuation
- Objects cache per chunk

### Physics System
- **Velocity-based movement**: `position += velocity * dt`
- **Acceleration/Braking**: Smooth transitions
- **Steering**: Speed-dependent sensitivity
- **Friction**: Terrain-specific slowing
- **Drift**: High-speed maneuverability

### Camera System
- **Smart Following**: Maintains distance from car
- **Speed-Aware**: Pulls back at high speeds
- **Camera Lag**: LERP smoothing
- **Lookahead**: Camera aims slightly ahead
- **Camera Shake**: Vibration at high speeds

### Nitro System
- **Limited Resource**: 100 unit tank
- **Consumption**: 30 units/second when active
- **Recharge**: 20 units/second when inactive
- **Speed Boost**: 1.5x multiplier
- **Visual Effect**: FOV increases by 15°

## 📊 Performance Tips

1. **Lower Chunk Distance**: Reduce `RENDER_DISTANCE` in config
2. **Smaller Map**: Modify `NUM_ROAD_SEGMENTS`
3. **Fewer Objects**: Reduce `NUM_BUILDINGS_PER_CHUNK`, etc.
4. **Lower Resolution**: Reduce `WINDOW_WIDTH`, `WINDOW_HEIGHT`
5. **Limit FPS**: Reduce `FPS` in config

## 🐛 Troubleshooting

### "ImportError: No module named 'OpenGL'"
```bash
pip install PyOpenGL PyOpenGL-accelerate numpy pygame
```

### "OpenGL version not supported"
- Update GPU drivers
- Ensure OpenGL 3.3+ is available
- Check GPU compatibility

### Low FPS
- Reduce world complexity in config.py
- Lower render distance
- Reduce window resolution
- Check GPU load

### Camera Issues
- Adjust `CAMERA_FOLLOW_SPEED` for smoother/snappier follow
- Change `CAMERA_FOLLOW_HEIGHT` and `CAMERA_FOLLOW_DISTANCE`
- Modify `CAMERA_SHAKE_AMOUNT` for less vibration

## 🎨 Extending the Game

### Add More Road Types
Edit `road.py` and add new road types in `generate_roads()`

### Create Custom Meshes
Extend `EnvironmentObject` class for new object types

### Add Textures
1. Add PNG files to `textures/` folder
2. Load with Pillow in `renderer.py`
3. Apply to meshes

### Implement Sound
1. Use `pygame.mixer` for audio
2. Add SFX to input handling
3. Add music to game loop

### Add NPCs
1. Create `npc.py` module
2. Implement NPC car physics
3. Render in main loop

## 📈 Scalability

The game uses chunk-based rendering for scalability:

- **Chunk Size**: 500 units (configurable)
- **Render Distance**: 3 chunks (configurable)
- **Total Visible**: ~6000x6000 units = 36 km²
- **Seamless**: No boundaries visible to player
- **Infinite Expansion**: Chunks generated on-the-fly

## 🔄 Game Loop Flow

```
1. Handle Input (W,A,S,D, Shift)
2. Update Car (physics, nitro, position)
3. Update World (chunk loading/unloading)
4. Update Camera (smooth following)
5. Clear Screen
6. Render Roads
7. Render Environment
8. Render Car
9. Render HUD (speed, nitro)
10. Swap Buffers
11. Repeat
```

## 📚 OpenGL Details

- **Profile**: Core Profile 3.3+
- **Shaders**: GLSL 330
- **Primitive**: Triangles (GL_TRIANGLES)
- **Depth Test**: Enabled
- **Face Culling**: Enabled (CCW)
- **Blending**: Enabled

## 🎓 Learning Resources

- [PyOpenGL Documentation](https://pyopengl.sourceforge.net/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [OpenGL Tutorials](https://learnopengl.com/)
- [Modern OpenGL](https://learnopengl.com/Getting-started/OpenGL)

## 📝 License

This project is provided as-is for educational and entertainment purposes.

## 🎉 Enjoy!

Drive fast, explore the large world, and have fun!

For issues or improvements, feel free to modify the code to suit your needs.

---

**Game Version**: 1.0  
**Last Updated**: April 8, 2026  
**Engine**: Python + PyOpenGL 3.3+  
