# Advanced Configuration Guide

This guide explains every configurable setting in the 3D Racing Game.

## Window Settings

```python
WINDOW_WIDTH = 1280          # Screen width in pixels
WINDOW_HEIGHT = 720          # Screen height in pixels
WINDOW_TITLE = "3D Racing Game - Open World"  # Window title
FPS = 60                     # Target frames per second
TARGET_DELTA = 1.0 / FPS     # Time between frames
```

**Tips:**
- Higher resolution = better visuals but lower FPS
- 1280x720 is a good balance
- Try 1920x1080 on powerful GPU
- Reduce to 800x600 on weak systems

---

## World Settings

```python
CHUNK_SIZE = 500.0           # Size of each world chunk (units)
RENDER_DISTANCE = 3          # Chunks loaded in each direction
MAP_SCALE = 1.0              # Overall world scale multiplier
```

**Tips:**
- `CHUNK_SIZE` = 500 means each chunk is 500x500 units
- `RENDER_DISTANCE` = 3 loads 7x7 chunks = 3500x3500 units visible
- Higher render distance = more visible world but lower FPS
- Increase MAP_SCALE to make distances feel larger

**Performance Impact:**
- RENDER_DISTANCE: HIGH impact (biggest effect on FPS)
- CHUNK_SIZE: MEDIUM impact (affects memory usage)

---

## Physics Settings

```python
GRAVITY = 0.0                # Gravity acceleration (not used yet)
DRAG_COEFFICIENT = 0.1       # Air resistance
ROAD_FRICTION = 0.85         # Fast surface (asphalt)
DIRT_FRICTION = 0.70         # Medium surface (unpaved)
GRASS_FRICTION = 0.50        # Slow surface (grass/trees)
```

**Friction Values:**
- 1.0 = no slowdown
- 0.5 = lose half speed per frame
- 0.0 = stop immediately

**Tips:**
- Lower friction = slide more (drifting easier)
- Higher friction = grip more (turning tighter)
- Dirt should be between road and grass

---

## Car Physics

```python
MAX_SPEED = 150.0            # Maximum car speed (units/sec)
ACCELERATION = 50.0          # How fast car speeds up
BRAKE_DECELERATION = 100.0   # How fast car slows
STEERING_SPEED = 3.0         # How fast steering responds (degrees/sec)
DRIFT_THRESHOLD = 80.0       # Speed above which drifting starts
DRIFT_MULTIPLIER = 1.2       # How much drifting affects movement
```

**Speed Reference:**
- 100 units/sec = moderate highway speed
- 150 units/sec = fast
- 200 units/sec = very fast

**Tuning Examples:**

*Arcade Style (Fast, Loose):*
```python
MAX_SPEED = 200
ACCELERATION = 100
STEERING_SPEED = 5.0
ROAD_FRICTION = 0.90
```

*Realistic Style (Slower, Grounded):*
```python
MAX_SPEED = 100
ACCELERATION = 30
STEERING_SPEED = 2.0
ROAD_FRICTION = 0.95
```

*Drift Style (Drifty, Slidey):*
```python
MAX_SPEED = 180
DRIFT_THRESHOLD = 60.0
DRIFT_MULTIPLIER = 1.5
ROAD_FRICTION = 0.80
```

---

## Nitro System

```python
MAX_NITRO = 100.0            # Maximum nitro meter
NITRO_CONSUMPTION_RATE = 30.0    # Units/sec consumed when active
NITRO_RECHARGE_RATE = 20.0   # Units/sec gained when inactive
NITRO_BOOST_MULTIPLIER = 1.5 # Speed multiplier (1.5 = 50% faster)
NITRO_FOV_BOOST = 15.0       # FOV increase degrees
```

**Examples:**

*Extreme Nitro:*
```python
NITRO_CONSUMPTION_RATE = 15.0
NITRO_RECHARGE_RATE = 30.0
NITRO_BOOST_MULTIPLIER = 2.0
NITRO_FOV_BOOST = 25.0
```

*Subtle Nitro:*
```python
NITRO_CONSUMPTION_RATE = 50.0
NITRO_RECHARGE_RATE = 10.0
NITRO_BOOST_MULTIPLIER = 1.2
NITRO_FOV_BOOST = 5.0
```

---

## Camera Settings

```python
CAMERA_FOLLOW_HEIGHT = 8.0   # Height above car (units)
CAMERA_FOLLOW_DISTANCE = 15.0    # Distance behind car (units)
CAMERA_FOLLOW_SPEED = 0.15   # How smooth camera follows (0-1)
CAMERA_MAX_DISTANCE = 30.0   # Max distance at high speed
CAMERA_MIN_DISTANCE = 8.0    # Min distance at low speed
CAMERA_SHAKE_AMOUNT = 0.05   # Vibration intensity
```

**Tips:**
- Smaller `CAMERA_FOLLOW_SPEED` = more lag, smoother
- Larger `CAMERA_FOLLOW_SPEED` = less lag, snappier
- 0.15 is default smooth
- 0.05 = very smooth, dreamy
- 0.30 = snappy, responsive
- Higher `CAMERA_SHAKE_AMOUNT` = more vibration at speed

---

## Lighting Settings

```python
AMBIENT_LIGHT = 0.4          # Overall brightness (0-1)
DIRECTIONAL_LIGHT = [0.8, 0.9, 1.0]  # Light color (RGB)
LIGHT_DIRECTION = [-0.2, 0.8, 0.3]   # Light source direction
FOG_density = 0.001          # Fog thickness
SKY_COLOR = [0.53, 0.76, 0.98, 1.0]  # Sky color (RGBA)
```

**Lighting Styles:**

*Bright Day:*
```python
AMBIENT_LIGHT = 0.6
DIRECTIONAL_LIGHT = [1.0, 1.0, 0.9]
FOG_density = 0.0005
SKY_COLOR = [0.8, 0.9, 1.0, 1.0]
```

*Dark Evening:*
```python
AMBIENT_LIGHT = 0.2
DIRECTIONAL_LIGHT = [1.0, 0.7, 0.5]
FOG_density = 0.002
SKY_COLOR = [0.3, 0.3, 0.4, 1.0]
```

*Foggy:*
```python
FOG_density = 0.005
AMBIENT_LIGHT = 0.5
DIRECTIONAL_LIGHT = [0.8, 0.8, 0.9]
```

---

## Road Generation

```python
ROAD_WIDTH = 10.0            # Width of roads (units)
ROAD_HEIGHT_VARIATION = 15.0 # Max elevation change
NUM_ROAD_SEGMENTS = 50       # Number of road pieces
CURVE_FREQUENCY = 0.1        # How curvy roads are
ELEVATION_FREQUENCY = 0.05   # How hilly roads are
```

**Tips:**
- Increase `ROAD_WIDTH` for easier driving
- Increase `NUM_ROAD_SEGMENTS` for more complex roads
- Increase `CURVE_FREQUENCY` for windier roads (0.0-0.5)
- Increase `ELEVATION_FREQUENCY` for hillier terrain

---

## Environment Settings

```python
NUM_BUILDINGS_PER_CHUNK = 5  # Buildings in city areas
NUM_TREES_PER_CHUNK = 10     # Trees in rural areas
NUM_STREET_LIGHTS_PER_CHUNK = 3  # Street lights per chunk
```

**Performance Impact:**
- More buildings/trees = lower FPS
- Recommended: Keep total objects < 1000 per chunk

---

## Debug Settings

```python
DEBUG_MODE = False           # Enable debug output
SHOW_WIREFRAME = False       # Show wireframe rendering
```

**To Enable Debug:**
```python
DEBUG_MODE = True
# Console will print:
# - Car position every frame
# - Camera info
# - World state
# - Performance metrics
```

---

## Performance Tuning Guide

### For Low-End GPU (Intel HD, Mobile)

```python
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30
RENDER_DISTANCE = 2
NUM_BUILDINGS_PER_CHUNK = 2
NUM_TREES_PER_CHUNK = 3
NUM_STREET_LIGHTS_PER_CHUNK = 1
FOG_density = 0.005  # Reduces draw distance
```

### For Mid-Range GPU (GTS 1050, RX 560)

```python
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
RENDER_DISTANCE = 3
NUM_BUILDINGS_PER_CHUNK = 5
NUM_TREES_PER_CHUNK = 8
```

### For High-End GPU (RTX 3070, 4090)

```python
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 120
RENDER_DISTANCE = 4
NUM_BUILDINGS_PER_CHUNK = 10
NUM_TREES_PER_CHUNK = 15
```

---

## Gameplay Customization

### Slow Realistic Driving

```python
MAX_SPEED = 80
ACCELERATION = 20
STEERING_SPEED = 1.5
DRIFT_THRESHOLD = 150  # Hard to drift
NITRO_BOOST_MULTIPLIER = 1.2
```

### Fast Arcade Racing

```python
MAX_SPEED = 300
ACCELERATION = 200
STEERING_SPEED = 10
DRIFT_THRESHOLD = 50  # Easy to drift
NITRO_BOOST_MULTIPLIER = 2.0
```

### Exploration Mode (Large World)

```python
MAX_SPEED = 120
RENDER_DISTANCE = 4
CHUNK_SIZE = 1000  # Larger chunks
MAP_SCALE = 2.0    # Feels larger
FOG_density = 0.0008  # See further
```

---

## Custom Car Types

In `car.py`, add new car types:

```python
CAR_TYPES = {
    'sports': CarType('Sports Car', max_speed=200, acceleration=80, 
                      handling=0.95, weight=1.0),
    'truck': CarType('Truck', max_speed=120, acceleration=30, 
                     handling=0.70, weight=2.0),
    'rally': CarType('Rally Car', max_speed=180, acceleration=75, 
                     handling=0.98, weight=0.9),
    
    # Add your custom car
    'supercar': CarType('Super Car', max_speed=280, acceleration=150, 
                        handling=0.92, weight=0.8),
    'bus': CarType('Bus', max_speed=90, acceleration=15, 
                   handling=0.60, weight=3.0),
}
```

Then in `main.py`:
```python
self.car = Car('supercar', start_pos=(0, 1, 0))
```

---

## Performance Checklist

✓ Target FPS = 60? (Adjust if getting lower)
✓ RENDER_DISTANCE appropriate for GPU?
✓ WINDOW_WIDTH/HEIGHT reasonable?
✓ FOG_density set to reduce far-plane rendering?
✓ NUM_OBJECTS tuned for expected object count?

---

## Common Tweaks

**"Game is too slow"**
→ Reduce RENDER_DISTANCE, WINDOW_WIDTH, FPS

**"Car feels unresponsive"**
→ Increase MAX_SPEED, ACCELERATION, STEERING_SPEED

**"Car slides too much"**
→ Increase ROAD_FRICTION

**"Roads are boring"**
→ Increase CURVE_FREQUENCY, ELEVATION_FREQUENCY

**"Camera is jerky"**
→ Decrease CAMERA_FOLLOW_SPEED (0.08 for smooth)

**"Can't see far enough"**
→ Decrease FOG_density

---

## Notes

- All numeric values are in arbitrary game units
- Changes take effect immediately on next game start
- Some settings require code changes (noted in comments)
- For best results, tweak one setting at a time and test

Good luck tuning! 🎮
