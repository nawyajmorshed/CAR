"""
Test runner - starts game and catches errors
"""
import sys
import os

print("Starting game test...")
print("="*60)

try:
    # Add paths for imports
    root_dir = os.path.join(os.path.dirname(__file__), '..')
    sys.path.insert(0, root_dir)  # Add root for config, physics, debug
    sys.path.insert(0, os.path.join(root_dir, 'src'))  # Add src for game, graphics

    # Import all modules first
    print("Loading modules...")
    import config
    from graphics import SimpleRenderer, Camera, ShaderManager, TextureManager
    from game import Car, AICar, World, ChunkManager
    import physics
    import debug
    print("✓ All modules loaded")
    
    # Import Pygame
    print("Initializing Pygame...")
    import pygame
    from pygame.locals import *
    import OpenGL.GL as gl
    from OpenGL.GL import *
    print("✓ Pygame initialized")
    
    # Create window
    print("Creating game window...")
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_COMPATIBILITY)
    
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Racing Game - Test")
    print("✓ Window created")
    
    # Test renderer
    print("Creating renderer...")
    renderer = SimpleRenderer(800, 600)
    print("✓ Renderer created")
    
    # Create game objects
    print("Creating game objects...")
    player_car = Car('sports', start_pos=(0, 1, 0))
    game_camera = Camera(player_car)
    game_world = World()
    print("✓ Game objects created")
    
    # Test rendering
    print("Testing rendering...")
    renderer.clear()
    renderer.setup_matrices_with_camera(game_camera, 800, 600, player_car)
    renderer.render_car(player_car)
    renderer.render_roads(game_world.road_segments[:5])  # Just first 5
    renderer.render_environment(game_world.environment_objects[:10])  # Just first 10
    pygame.display.flip()
    print("✓ Rendering successful")
    
    print("\n" + "="*60)
    print("SUCCESS: Game can be rendered!")
    print("="*60)
    print("\nNow run: python main.py")
    print("\nPress ESC in the game window to exit.")
    
    pygame.quit()
    
except Exception as e:
    print("\n" + "="*60)
    print(f"ERROR: {e}")
    print("="*60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
