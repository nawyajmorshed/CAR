"""
Comprehensive diagnostic script
"""
import sys
import os

print("="*60)
print("COMPREHENSIVE GAME DIAGNOSTIC")
print("="*60)

# 1. Check environment
print("\n1. PYTHON ENVIRONMENT")
print(f"   Python: {sys.version}")
print(f"   Executable: {sys.executable}")
print(f"   Platform: {sys.platform}")

# 2. Check packages
print("\n2. INSTALLED PACKAGES")
try:
    import pygame
    print(f"   pygame-ce: {pygame.version.ver}")
except ImportError as e:
    print(f"   MISSING: pygame - {e}")

try:
    import OpenGL
    print(f"   OpenGL: {OpenGL.__version__}")
except ImportError as e:
    print(f"   MISSING: OpenGL - {e}")

try:
    import numpy
    print(f"   numpy: {numpy.__version__}")
except ImportError as e:
    print(f"   MISSING: numpy - {e}")

try:
    from PIL import Image
    print(f"   Pillow: {Image.__version__ if hasattr(Image, '__version__') else 'installed'}")
except ImportError as e:
    print(f"   MISSING: Pillow - {e}")

# 3. Check files
print("\n3. GAME FILES")
root_dir = os.path.join(os.path.dirname(__file__), '..')
root_files = ['main.py', 'config.py', 'physics.py', 'debug.py']
game_files = ['src/game/car.py', 'src/game/world.py', 'src/game/chunk_manager.py']
graphics_files = ['src/graphics/simple_renderer.py', 'src/graphics/camera.py', 'src/graphics/shader.py', 'src/graphics/texture_manager.py']

for f in root_files:
    path = os.path.join(root_dir, f)
    status = "OK" if os.path.exists(path) else "MISSING"
    print(f"   {f}: {status}")

for f in game_files:
    path = os.path.join(root_dir, f)
    status = "OK" if os.path.exists(path) else "MISSING"
    print(f"   {f}: {status}")

for f in graphics_files:
    path = os.path.join(root_dir, f)
    status = "OK" if os.path.exists(path) else "MISSING"
    print(f"   {f}: {status}")

# 4. Check shaders
print("\n4. SHADER FILES")
shaders = ['standard.vert', 'standard.frag', 'simple.vert', 'simple.frag']
for s in shaders:
    path = os.path.join(root_dir, 'shaders', s)
    status = "OK" if os.path.exists(path) else "MISSING"
    print(f"   {s}: {status}")

# 5. Import test
print("\n5. MODULE IMPORTS")
root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)  # Add root directory for config, physics, debug
sys.path.insert(0, os.path.join(root_dir, 'src'))  # Add src directory for game, graphics modules
modules_ok = True
try:
    import config
    print("   config: OK")
except Exception as e:
    print(f"   config: ERROR - {e}")
    modules_ok = False

try:
    import physics
    print("   physics: OK")
except Exception as e:
    print(f"   physics: ERROR - {e}")
    modules_ok = False

try:
    from game import Car
    print("   Car: OK")
except Exception as e:
    print(f"   Car: ERROR - {e}")
    modules_ok = False

try:
    from graphics import Camera
    print("   Camera: OK")
except Exception as e:
    print(f"   Camera: ERROR - {e}")
    modules_ok = False

try:
    from game import World
    print("   World: OK")
except Exception as e:
    print(f"   World: ERROR - {e}")
    modules_ok = False

try:
    from game import ChunkManager
    print("   ChunkManager: OK")
except Exception as e:
    print(f"   ChunkManager: ERROR - {e}")
    modules_ok = False

try:
    from graphics import SimpleRenderer
    print("   SimpleRenderer: OK")
except Exception as e:
    print(f"   SimpleRenderer: ERROR - {e}")
    modules_ok = False

# 6. Test object creation
print("\n6. OBJECT CREATION TEST")
try:
    from game import Car
    c = Car('sports')
    print(f"   Car created: OK (position: {c.position})")
except Exception as e:
    print(f"   Car: ERROR - {e}")

try:
    from graphics import Camera
    from game import Car
    car = Car('sports')
    cam = Camera(car)
    print(f"   Camera created: OK (FOV: {cam.fov})")
except Exception as e:
    print(f"   Camera: ERROR - {e}")

try:
    from game import World
    w = World()
    print(f"   World created: OK ({len(w.road_segments)} roads, {len(w.environment_objects)} objects)")
except Exception as e:
    print(f"   World: ERROR - {e}")

# 7. Summary
print("\n" + "="*60)
if modules_ok:
    print("STATUS: READY TO PLAY - All systems OK")
    print("\nRun: python main.py")
else:
    print("STATUS: ERRORS DETECTED - Check above")
print("="*60)
