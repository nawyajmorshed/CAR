"""
Test suite for 3D Racing Game dependencies and systems
"""
import sys
import os


def test_python_version():
    """Test Python version"""
    print("Testing Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Need Python 3.8+, got {version.major}.{version.minor}")
        return False


def test_import(module_name):
    """Test if module can be imported"""
    print(f"Testing {module_name}...", end=" ")
    try:
        __import__(module_name)
        print("✓")
        return True
    except ImportError as e:
        print(f"✗ {e}")
        return False


def test_opengl():
    """Test OpenGL support"""
    print("Testing OpenGL...", end=" ")
    try:
        import pygame
        import OpenGL.GL as gl
        
        pygame.init()
        pygame.display.set_mode((1, 1))
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        
        version_str = gl.glGetString(gl.GL_VERSION).decode()
        version_num = float(version_str.split()[0])
        
        pygame.quit()
        
        if version_num >= 3.3:
            print(f"✓ {version_str}")
            return True
        else:
            print(f"✗ Need OpenGL 3.3+, got {version_num}")
            return False
    except Exception as e:
        print(f"✗ {e}")
        return False


def test_game_modules():
    """Test game module imports"""
    print("\nTesting game modules...")
    
    modules = [
        'config',
        'shader',
        'physics',
        'car',
        'camera',
        'world',
        'chunk_manager',
        'renderer',
        'texture_manager',
        'debug',
    ]
    
    success = True
    for module in modules:
        print(f"  {module}...", end=" ")
        try:
            __import__(module)
            print("✓")
        except Exception as e:
            print(f"✗ {e}")
            success = False
    
    return success


def test_file_structure():
    """Test file structure"""
    print("\nTesting file structure...")
    
    required_files = [
        'config.py',
        'main.py',
        'renderer.py',
        'shader.py',
        'car.py',
        'camera.py',
        'world.py',
        'physics.py',
        'chunk_manager.py',
        'texture_manager.py',
        'debug.py',
        'shaders/standard.vert',
        'shaders/standard.frag',
        'shaders/simple.vert',
        'shaders/simple.frag',
        'requirements.txt',
        'README.md',
    ]
    
    success = True
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ Missing: {file_path}")
            success = False
    
    return success


def test_shader_compilation():
    """Test shader compilation"""
    print("\nTesting shader compilation...")
    
    try:
        from shader import ShaderManager
        manager = ShaderManager()
        shader = manager.get_shader('standard')
        if shader:
            print("  ✓ Shaders compiled successfully")
            manager.cleanup()
            return True
        else:
            print("  ✗ Failed to load shader")
            return False
    except Exception as e:
        print(f"  ✗ {e}")
        return False


def test_game_classes():
    """Test game class instantiation"""
    print("\nTesting game classes...")
    
    try:
        from car import Car
        print("  Car...", end=" ")
        car = Car('sports', start_pos=(0, 0, 0))
        print("✓")
        
        from camera import Camera
        print("  Camera...", end=" ")
        camera = Camera(car)
        print("✓")
        
        from world import World
        print("  World...", end=" ")
        world = World()
        print(f"✓ ({len(world.road_segments)} roads, "
              f"{len(world.environment_objects)} objects)")
        
        return True
    except Exception as e:
        print(f"\n  ✗ {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("3D Racing Game - Dependency Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("pygame", lambda: test_import('pygame')),
        ("PyOpenGL", lambda: test_import('OpenGL')),
        ("numpy", lambda: test_import('numpy')),
        ("Pillow", lambda: test_import('PIL')),
        ("OpenGL Support", test_opengl),
        ("File Structure", test_file_structure),
        ("Game Modules", test_game_modules),
        ("Shader Compilation", test_shader_compilation),
        ("Game Classes", test_game_classes),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n### {test_name} ###")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to play!")
        print("\nRun: python main.py")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        print("Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
