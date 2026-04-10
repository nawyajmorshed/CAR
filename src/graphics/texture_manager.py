"""
Texture generation and management using Pillow
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
from PIL import Image, ImageDraw
import OpenGL.GL as gl


class TextureGenerator:
    """Generate textures procedurally using Pillow"""
    
    @staticmethod
    def create_checkered_texture(size=256, square_size=32):
        """Create a checkered pattern texture"""
        img = Image.new('RGB', (size, size), color=(200, 200, 200))
        pixels = img.load()
        
        for x in range(size):
            for y in range(size):
                if ((x // square_size) + (y // square_size)) % 2 == 0:
                    pixels[x, y] = (100, 100, 100)
        
        return img
    
    @staticmethod
    def create_road_texture(size=512):
        """Create a road texture"""
        img = Image.new('RGB', (size, size), color=(50, 50, 50))
        draw = ImageDraw.Draw(img)
        
        # Add lane markings
        for y in range(0, size, 50):
            draw.line([(0, y), (size, y)], fill=(255, 255, 100), width=2)
        
        return img
    
    @staticmethod
    def create_grass_texture(size=256):
        """Create a grass texture"""
        img = Image.new('RGB', (size, size), color=(34, 139, 34))
        pixels = img.load()
        
        # Add some variation
        np.random.seed(42)
        for x in range(size):
            for y in range(size):
                r = max(0, min(255, 34 + np.random.randint(-10, 10)))
                g = max(0, min(255, 139 + np.random.randint(-10, 10)))
                b = max(0, min(255, 34 + np.random.randint(-10, 10)))
                pixels[x, y] = (r, g, b)
        
        return img
    
    @staticmethod
    def create_building_texture(size=512):
        """Create a building texture (brick pattern)"""
        img = Image.new('RGB', (size, size), color=(180, 80, 40))
        draw = ImageDraw.Draw(img)
        
        # Draw brick grid
        brick_width = 60
        brick_height = 30
        
        for y in range(0, size, brick_height):
            offset = 0 if (y // brick_height) % 2 == 0 else brick_width // 2
            for x in range(-brick_width + offset, size, brick_width):
                draw.rectangle([x, y, x + brick_width, y + brick_height], 
                             outline=(150, 60, 20), width=2)
        
        return img
    
    @staticmethod
    def create_dirt_texture(size=256):
        """Create a dirt/unpaved road texture"""
        img = Image.new('RGB', (size, size), color=(139, 101, 50))
        pixels = img.load()
        
        # Add variation
        np.random.seed(43)
        for x in range(size):
            for y in range(size):
                r = max(0, min(255, 139 + np.random.randint(-20, 20)))
                g = max(0, min(255, 101 + np.random.randint(-20, 20)))
                b = max(0, min(255, 50 + np.random.randint(-20, 20)))
                pixels[x, y] = (r, g, b)
        
        return img


class TextureManager:
    """Manages texture loading and OpenGL binding"""
    
    def __init__(self):
        self.textures = {}
        self.generate_default_textures()
    
    def generate_default_textures(self):
        """Generate and load default textures"""
        textures_to_create = {
            'checkerboard': TextureGenerator.create_checkered_texture(),
            'road': TextureGenerator.create_road_texture(),
            'grass': TextureGenerator.create_grass_texture(),
            'building': TextureGenerator.create_building_texture(),
            'dirt': TextureGenerator.create_dirt_texture(),
        }
        
        for name, img in textures_to_create.items():
            texture_id = self.load_texture_from_pil(img)
            self.textures[name] = texture_id
    
    @staticmethod
    def load_texture_from_pil(img):
        """Load a PIL image as OpenGL texture"""
        # Convert image to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        data = np.array(img)
        
        # Create texture
        texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
        
        # Set texture parameters
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        
        # Upload texture data
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA,
            img.width,
            img.height,
            0,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            data
        )
        
        # Generate mipmaps
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        
        return texture_id
    
    def get_texture(self, name):
        """Get a texture by name"""
        return self.textures.get(name, 0)
    
    def bind_texture(self, name, unit=0):
        """Bind a texture to a texture unit"""
        texture_id = self.get_texture(name)
        if texture_id:
            gl.glActiveTexture(gl.GL_TEXTURE0 + unit)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
    
    def cleanup(self):
        """Delete all textures"""
        for texture_id in self.textures.values():
            gl.glDeleteTextures(1, np.array([texture_id]))
