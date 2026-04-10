"""
Setup and launcher script for the 3D Racing Game
"""
import sys
import subprocess
import platform


def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    requirements = [
        'pygame==2.4.0',
        'PyOpenGL==3.1.6',
        'numpy==1.24.3',
        'Pillow==10.0.0',
    ]
    
    # Try to install OpenGL accelerate (optional for Windows)
    if platform.system() == 'Windows':
        requirements.insert(3, 'PyOpenGL-accelerate==3.1.6')
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            return False
    
    return True


def check_opengl():
    """Check OpenGL support"""
    print("\nChecking OpenGL support...")
    
    try:
        import pygame
        import OpenGL.GL as gl
        from OpenGL.GL import glGetString, GL_VERSION, GL_SHADING_LANGUAGE_VERSION
        
        pygame.init()
        pygame.display.set_mode((1, 1))
        
        version = glGetString(GL_VERSION).decode()
        glsl_version = glGetString(GL_SHADING_LANGUAGE_VERSION).decode()
        
        print(f"✓ OpenGL Version: {version}")
        print(f"✓ GLSL Version: {glsl_version}")
        
        # Check minimum version
        version_num = float(version.split()[0])
        if version_num >= 3.3:
            print("✓ OpenGL 3.3+ support confirmed")
            return True
        else:
            print("✗ OpenGL 3.3+ required")
            return False
    
    except Exception as e:
        print(f"✗ OpenGL check failed: {e}")
        return False


def main():
    """Main launcher"""
    print("=" * 50)
    print("3D Racing Game - Setup & Launcher")
    print("=" * 50)
    
    # Check Python version
    print(f"\nPython Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("Python 3.8+ required")
        return 1
    
    # Try to import dependencies
    try:
        import pygame
        import OpenGL.GL
        import numpy
        from PIL import Image
        print("\n✓ All dependencies already installed")
    except ImportError:
        print("\n✗ Missing dependencies, installing...")
        if not install_dependencies():
            print("Failed to install dependencies")
            return 1
    
    # Check OpenGL
    if not check_opengl():
        print("\n⚠ Warning: OpenGL 3.3+ may not be available")
    
    # Run the game
    print("\n" + "=" * 50)
    print("Starting 3D Racing Game...")
    print("=" * 50)
    print("\nControls:")
    print("  W    - Forward")
    print("  S    - Reverse")
    print("  A    - Turn Left")
    print("  D    - Turn Right")
    print("  Shift - Nitro Boost")
    print("  ESC  - Exit")
    print("\n")
    
    try:
        from main import Game
        game = Game()
        game.run()
    except Exception as e:
        print(f"\nGame Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
