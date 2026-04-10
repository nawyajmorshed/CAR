# 🚀 Quick Start Guide

## 1️⃣ Installation

### Option A: Automatic Setup (Recommended)
```bash
python setup.py
```

### Option B: Manual Setup
```bash
pip install -r requirements.txt
python main.py
```

## 2️⃣ System Requirements

- **Python 3.8+**
- **GPU with Modern Driver** (OpenGL 3.3+)
- **RAM**: 2GB minimum, 4GB+ recommended
- **VRAM**: 512MB minimum

### Check GPU Support
Run this to verify OpenGL support:
```python
from OpenGL.GL import glGetString, GL_VERSION
print(glGetString(GL_VERSION))
```

## 3️⃣ Game Controls

| Key | Action |
|-----|--------|
| **W** | Accelerate Forward |
| **S** | Reverse |
| **A** | Steer Left |
| **D** | Steer Right |
| **LShift** | Nitro Boost |
| **ESC** | Exit Game |

## 4️⃣ First Run Tips

### What You'll See
1. **Highway Loop**: Main circular road with elevation changes
2. **City Center**: Dense building area with grid roads
3. **Trees**: Surrounding rural areas
4. **Bridges & Heights**: Various terrain features

### Try This First
1. Drive forward (W) to get a feel for the car
2. Find the highway (main loop)
3. Try nitro boost (Shift) at high speed
4. Notice camera pulls back at speed
5. Drive off-road to see grip changes

### Performance Optimization
If FPS is low, edit `config.py`:
```python
FPS = 30  # Reduce from 60
RENDER_DISTANCE = 2  # Reduce from 3
WINDOW_WIDTH = 800  # Reduce from 1280
WINDOW_HEIGHT = 480  # Reduce from 720
```

## 5️⃣ Project Structure

```
CAR/
├── main.py              # Run this file
├── config.py            # Edit settings here
├── car.py               # Car physics
├── camera.py            # Camera system
├── world.py             # Road generation
├── renderer.py          # OpenGL rendering
├── shader.py            # Shader management
├── physics.py           # Physics calculations
├── chunk_manager.py     # World chunking
├── texture_manager.py   # Texture system
├── debug.py             # Debug tools
├── setup.py             # Setup helper
├── shaders/             # GLSL shader files
├── textures/            # Texture assets
└── README.md            # Full documentation
```

## 6️⃣ Configuration Guide

### Common Tweaks (in `config.py`)

**For Higher FPS:**
```python
FPS = 30  # Lower FPS
RENDER_DISTANCE = 2  # Less chunks
```

**For Better Graphics:**
```python
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 120
```

**For Different Car:**
Change in `main.py`:
```python
self.car = Car('rally', start_pos=(0, 1, 0))  # sports, truck, rally
```

**For Faster Roads:**
```python
MAX_SPEED = 250  # From 150
ACCELERATION = 100  # From 50
```

## 7️⃣ Troubleshooting

### Error: "No module named 'pygame'"
```bash
pip install pygame==2.4.0
```

### Error: "OpenGL not available"
**Windows:**
```bash
pip install PyOpenGL PyOpenGL-accelerate
```

**Linux:**
```bash
sudo apt-get install python3-opengl
pip install PyOpenGL
```

**Mac:**
```bash
brew install python3
pip install PyOpenGL
```

### Slow Performance
1. Lower `WINDOW_WIDTH` and `WINDOW_HEIGHT`
2. Reduce `RENDER_DISTANCE` in config.py
3. Close other applications
4. Update GPU drivers

### Camera Spinning/Weird
Reduce `CAMERA_FOLLOW_SPEED`:
```python
CAMERA_FOLLOW_SPEED = 0.08  # From 0.15
```

### Car Not Moving
Check for console errors and verify:
- OpenGL 3.3+ is available
- Pygame is running
- Input is working (press A/D to see steering)

## 8️⃣ Understanding the Systems

### Chunk System
The world is divided into chunks of `CHUNK_SIZE` (500 units).
- Only nearby chunks render
- `RENDER_DISTANCE` controls how many chunks around you load
- Total area visible = `RENDER_DISTANCE * 2 * CHUNK_SIZE` squared

### Physics
- **Velocity**: Measured in units/second
- **Acceleration**: Units/second²
- **Friction**: Depends on terrain (road > dirt > grass)
- **Steering**: Speed-dependent smoothing with LERP

### Camera
- **Third-person**: Follows car from behind and above
- **Smart Distance**: Pulls back at high speed
- **Smooth Lag**: LERP-based smoothing
- **FOV Change**: Increases with nitro boost

### Nitro System
- **Meter**: 0-100 units
- **When Active**: Consumes 30 units/sec, multiplies speed by 1.5
- **Recharge**: Gains 20 units/sec when inactive
- **Throttle**: Hold Shift to activate

## 9️⃣ World Zones

| Zone | Description | Speed | Grip | Objects |
|------|-------------|-------|------|---------|
| **City** | Dense buildings | Slow | Road | Dense |
| **Highway** | Main loop road | Fast | Road | Sparse |
| **Rural** | Trees & nature | Medium | Grass | Minimal |

## 🔟 Advanced Tips

### Enable Debug Mode
```python
# In config.py
DEBUG_MODE = True
SHOW_WIREFRAME = True
```

### Custom Car Type
```python
# In car.py
CAR_TYPES = {
    'custom': CarType('My Car', max_speed=300, acceleration=100, 
                      handling=0.9, weight=0.8),
}
```

### Extend World
Modify `world.py`:
```python
NUM_ROAD_SEGMENTS = 100  # More road segments
NUM_BUILDINGS_PER_CHUNK = 10  # More buildings
```

### Change Lighting
```python
# In config.py
AMBIENT_LIGHT = 0.6  # Brighter
DIRECTIONAL_LIGHT = [1.0, 1.0, 1.0]  # Whiter
FOG_density = 0.0005  # Less fog
```

## 🎯 Next Steps

1. **Explore the Map**: Drive around, get familiar with terrain
2. **Find Nitro**: Notice speed boost mechanics
3. **Try Different Cars**: Edit main.py to try 'rocket', 'truck', 'rally'
4. **Modify Config**: Tweak settings to your preference
5. **Read Code**: Understand the implementation

## 📞 Support

If you encounter issues:
1. Check the error message carefully
2. Try the troubleshooting section above
3. Verify OpenGL 3.3+ support
4. Check Python version (3.8+)
5. Ensure all dependencies are installed

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] OpenGL 3.3+ available
- [ ] Game window opens
- [ ] Car responds to input (W/A/S/D)
- [ ] Camera follows the car
- [ ] Able to drive long distances
- [ ] FPS display shows in console
- [ ] Nitro system works (Shift key)

Once all boxes are checked, you're ready to explore the world! 🎮

---

**Have fun racing!** 🏎️💨
