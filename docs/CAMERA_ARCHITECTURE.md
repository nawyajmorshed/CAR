# Unified Camera System Architecture

## Problem Solved

Previously, split-screen viewports could diverge in their camera setup, leading to:
- Road appearing angled in one viewport but straight in another
- Car not centered consistently
- Different perspective calculations between left/right views

**Solution:** Single source of truth for all camera/projection calculations via `camera_system.py`

---

## Architecture Overview

### Three-Layer System

```
Layer 1: Configuration Classes
├── ProjectionConfig: FOV, near/far planes, aspect ratio
└── CameraConfig: Camera distance, height, lookahead distance

Layer 2: Stateless Functions
└── CameraSetup: Pure functions computing camera matrices
    ├── compute_camera_position()
    ├── compute_lookat_point()
    └── apply_camera_matrix()

Layer 3: Unified Renderer
└── ViewportRenderer: Orchestrates viewport + projection + camera
    ├── setup_viewport()
    ├── setup_projection()
    ├── setup_camera()
    └── teardown_viewport()
```

### Key Design Principles

1. **Immutable Configs**: `ProjectionConfig` and `CameraConfig` are stateless, preventing accidental changes
2. **Stateless Functions**: `CameraSetup` functions have no side effects - same input = same output
3. **Single Orchestrator**: `ViewportRenderer` is the ONLY place that coordinates setup
4. **Consistency Checks**: Debug mode can verify both viewports compute identical values

---

## Configuration Classes

### ProjectionConfig

Controls how the 3D world is projected onto the screen.

```python
ProjectionConfig(fov=60.0, near_plane=0.1, far_plane=5000.0, aspect_ratio=None)
```

**Parameters:**
- `fov`: Field of view in degrees (60° is standard)
- `near_plane`: Close clipping plane (0.1 units)
- `far_plane`: Far clipping plane (5000 units)
- `aspect_ratio`: Width/Height ratio (computed per viewport)

**Default:** `ViewportRenderer.DEFAULT_PROJECTION_CONFIG`

### CameraConfig

Controls camera placement relative to the car.

```python
CameraConfig(distance_behind=12.0, height_above=3.5, lookahead_distance=20.0)
```

**Parameters:**
- `distance_behind`: How many units behind the car (12 units)
- `height_above`: How many units above ground (3.5 units)
- `lookahead_distance`: How far ahead to look (20 units)

**Default:** `ViewportRenderer.DEFAULT_CAMERA_CONFIG`

---

## Stateless Camera Functions

### CameraSetup.compute_camera_position()

Calculates where the camera should be positioned.

```python
camera_pos = CameraSetup.compute_camera_position(
    car_position=np.array([0, 1, 100]),  # [x, y, z]
    car_yaw=0.0,                          # Rotation (radians)
    camera_config=CameraConfig()
)
# Returns: [camera_x, camera_y, camera_z]
```

**Formula:**
```
camera_x = car_x - sin(yaw) * distance_behind
camera_y = car_y + height_above
camera_z = car_z - cos(yaw) * distance_behind
```

### CameraSetup.compute_lookat_point()

Calculates where the camera should look.

```python
lookat_pos = CameraSetup.compute_lookat_point(
    car_position=np.array([0, 1, 100]),
    car_yaw=0.0,
    camera_config=CameraConfig()
)
# Returns: [lookat_x, lookat_y, lookat_z]
```

**Formula:**
```
lookat_x = car_x + sin(yaw) * lookahead_distance
lookat_y = car_y + 0.5
lookat_z = car_z + cos(yaw) * lookahead_distance
```

### CameraSetup.apply_camera_matrix()

Applies the camera transformation to OpenGL.

```python
CameraSetup.apply_camera_matrix(
    car_position=car.position,
    car_yaw=car.rotation[1],
    camera_config=CameraConfig()
)
# Internally calls gluLookAt() with computed values
```

---

## Unified ViewportRenderer

### Complete Rendering Sequence

```python
# 1. Setup viewport bounds and scissor test
ViewportRenderer.setup_viewport(x, y, width, height)

# 2. Setup projection matrix (FOV, near/far planes)
ViewportRenderer.setup_projection(width, height)

# 3. Setup camera matrix (position + look direction)
ViewportRenderer.setup_camera(car.position, car.rotation[1])

# 4. Render scene (calls to render_ground, render_roads, etc.)
renderer.render_ground(...)
renderer.render_roads(...)
renderer.render_car(car)

# 5. Cleanup
ViewportRenderer.teardown_viewport()
```

### Usage in main.py

```python
def render_split_view(self, car, x_offset, y_offset, aspect_ratio, player_name):
    """Unified viewport rendering - both views use identical logic"""
    viewport_width = config.WINDOW_WIDTH
    viewport_height = config.WINDOW_HEIGHT // 2
    
    # This orchestration ensures both viewports stay synchronized
    ViewportRenderer.setup_viewport(x_offset, y_offset, viewport_width, viewport_height)
    ViewportRenderer.setup_projection(viewport_width, viewport_height)
    ViewportRenderer.setup_camera(car.position, car.rotation[1])
    
    # Render
    self.renderer.render_ground(self.world.environment_objects)
    self.renderer.render_roads(self.world.road_segments)
    self.renderer.render_car(car)
    
    ViewportRenderer.teardown_viewport()
```

---

## Customization & Extension

### Changing Camera Parameters

To adjust how the camera follows the car:

```python
# Option 1: Edit defaults once (affects all viewports)
ViewportRenderer.DEFAULT_CAMERA_CONFIG = CameraConfig(
    distance_behind=15.0,   # Move camera further back
    height_above=5.0,       # Raise camera higher
    lookahead_distance=25.0 # Look further ahead
)

# Option 2: Use custom config for specific viewport
custom_config = CameraConfig(distance_behind=20.0)
ViewportRenderer.setup_camera(car.position, car.rotation[1], custom_config)
```

### Changing Projection Parameters

To adjust FOV or clipping planes:

```python
# Option 1: Edit defaults once
ViewportRenderer.DEFAULT_PROJECTION_CONFIG = ProjectionConfig(
    fov=75.0,           # Wider field of view
    near_plane=0.1,
    far_plane=10000.0   # See further away
)

# Option 2: Custom projection for specific viewport
custom_proj = ProjectionConfig(fov=75.0)
ViewportRenderer.setup_projection(width, height, custom_proj)
```

### Debug Mode - Verify Consistency

Enable to verify both viewports compute identical camera positions:

```python
ViewportRenderer.DEBUG_MODE = True

# Output will show:
# [CAMERA DEBUG]
#   Car: [0. 1. 100.] | Yaw: 0.0°
#   Camera Pos: [-12. 3.5 100.]
#   LookAt Pos: [0. 1.5 120.]
#   Config: CameraConfig(behind=12.0, height=3.5, lookahead=20.0)
```

---

## Benefits

### 1. **Guaranteed Synchronization**
Both viewports ALWAYS use identical projection and camera logic. Changes to one automatically apply to the other.

### 2. **Single Point of Modification**
Want to change camera distance? Edit ONE place (`ViewportRenderer.DEFAULT_CAMERA_CONFIG`). Both viewports update instantly.

### 3. **Type Safety**
`ProjectionConfig` and `CameraConfig` are strongly typed - can't accidentally pass wrong values.

### 4. **Stateless & Testable**
`CameraSetup` functions have no side effects - easy to unit test and debug.

### 5. **Clear Architecture**
Anyone reading the code can immediately see:
- What camera parameters are used (CameraConfig)
- How they're computed (CameraSetup functions)
- How they're applied (ViewportRenderer)

### 6. **Extensible**
Easy to add new features:
- Smooth camera transitions: modify `lookahead_distance` over time
- Dynamic FOV: change `fov` based on speed
- Camera shake effects: add random offsets to computed positions

---

## Future Enhancements

### 1. Camera Interpolation
Smooth transitions between camera states:

```python
class CameraInterpolation:
    @staticmethod
    def interpolate_lookat(start_pos, end_pos, t):
        return start_pos + (end_pos - start_pos) * t
```

### 2. Camera Presets
Pre-configured camera modes:

```python
CAMERA_PRESETS = {
    'racing': CameraConfig(distance_behind=12.0, height_above=3.5),
    'cinematic': CameraConfig(distance_behind=20.0, height_above=8.0),
    'cockpit': CameraConfig(distance_behind=0.0, height_above=2.0)
}
```

### 3. Camera Effects
Screen shake, tilt, blur:

```python
def apply_camera_effects(shake_intensity=0.0):
    offset = np.random.randn(3) * shake_intensity
    camera_pos += offset
```

### 4. Multi-Player Spectator Camera
Center camera between both players:

```python
center_pos = (car1.position + car2.position) / 2
ViewportRenderer.setup_camera(center_pos, car1.rotation[1])
```

---

## Troubleshooting

### "Road appears angled in bottom viewport"
Check: Both viewports calling `ViewportRenderer.setup_camera()` with correct parameters

### "Car position differs between viewports"
Check: Both calling `setup_projection()` with same viewport dimensions

### "Camera doesn't rotate with car"
Check: `car.rotation[1]` (yaw) is being updated correctly in Physics/Car systems

### "One viewport has different FOV"
Never modify projection directly - always use `ViewportRenderer.setup_projection()`

---

## Summary

This architecture ensures:
✅ **Both viewports ALWAYS render identically**
✅ **Single source of truth for camera/projection**
✅ **Easy to modify without breaking consistency**
✅ **Extensible for future camera features**
✅ **Testable and maintainable code**

The system is "defensive against divergence" - impossible for the two viewports to accidentally use different camera logic.
