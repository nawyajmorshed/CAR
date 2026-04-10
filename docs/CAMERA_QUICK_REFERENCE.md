# Camera System - Quick Reference

## Use This Everywhere

```python
from camera_system import ViewportRenderer

# In your render function:
ViewportRenderer.setup_viewport(x, y, width, height)
ViewportRenderer.setup_projection(width, height)
ViewportRenderer.setup_camera(car.position, car.rotation[1])
```

## Do NOT Do This

❌ **WRONG** - Manual camera setup (causes desync):
```python
gl.glMatrixMode(gl.GL_PROJECTION)
gl.glLoadIdentity()
gluPerspective(60.0, aspect_ratio, 0.1, 5000.0)

gl.glMatrixMode(gl.GL_MODELVIEW)
gl.glLoadIdentity()
gluLookAt(...)
```

✅ **RIGHT** - Use unified system:
```python
ViewportRenderer.setup_projection(width, height)
ViewportRenderer.setup_camera(car.position, car.rotation[1])
```

## Change Camera Defaults

```python
from camera_system import ViewportRenderer, CameraConfig, ProjectionConfig

# Make camera closer/further
ViewportRenderer.DEFAULT_CAMERA_CONFIG = CameraConfig(
    distance_behind=20.0,   # Was 12.0
    height_above=5.0,       # Was 3.5
    lookahead_distance=30.0 # Was 20.0
)

# Change FOV
ViewportRenderer.DEFAULT_PROJECTION_CONFIG = ProjectionConfig(fov=75.0)
```

## Debug Camera State

```python
# Enable debug mode to verify both viewports match
ViewportRenderer.DEBUG_MODE = True

# This will print camera calculations for both render passes
```

## Key Files

- `camera_system.py` - Camera system implementation
- `main.py` - Uses `ViewportRenderer` in `render_split_view()`
- `CAMERA_ARCHITECTURE.md` - Full documentation

## Remember

✅ **All camera logic is in `ViewportRenderer`**
✅ **Both viewports call the same functions**
✅ **Configuration is centralized**
✅ **Changes affect both automatically**

This is defensive against divergence - impossible to accidentally make viewports different.
