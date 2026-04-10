"""
Chunk-based world management system for large-scale maps
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import math
import config


class Chunk:
    """Represents a chunk of the world"""
    
    def __init__(self, chunk_x, chunk_z):
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        self.world_x = chunk_x * config.CHUNK_SIZE
        self.world_z = chunk_z * config.CHUNK_SIZE
        
        # Chunk data
        self.terrain_type = self.determine_terrain()
        self.objects = []  # Buildings, trees, etc.
        self.road_segments = []  # Road meshes
        self.is_loaded = False
    
    def determine_terrain(self):
        """Determine terrain type based on chunk position"""
        distance_from_center = math.sqrt(self.chunk_x ** 2 + self.chunk_z ** 2)
        
        if distance_from_center < 2:
            return 'city'
        elif distance_from_center < 5:
            return 'highway'
        else:
            return 'rural'
    
    def load(self):
        """Load chunk resources"""
        self.is_loaded = True
    
    def unload(self):
        """Unload chunk resources"""
        self.objects.clear()
        self.road_segments.clear()
        self.is_loaded = False
    
    def get_bounds(self):
        """Get chunk bounding box"""
        return {
            'min_x': self.world_x,
            'max_x': self.world_x + config.CHUNK_SIZE,
            'min_z': self.world_z,
            'max_z': self.world_z + config.CHUNK_SIZE,
        }


class ChunkManager:
    """Manages chunks for infinite-feeling world"""
    
    def __init__(self):
        self.chunks = {}  # Dictionary of loaded chunks
        self.current_chunk = (0, 0)
        self.loaded_chunk_coords = set()
    
    def get_chunk_at_position(self, position):
        """Get chunk coordinates for a world position"""
        chunk_x = int(position[0] / config.CHUNK_SIZE)
        chunk_z = int(position[2] / config.CHUNK_SIZE)
        return (chunk_x, chunk_z)
    
    def update(self, car_position):
        """Update visible chunks based on car position"""
        current_chunk = self.get_chunk_at_position(car_position)
        
        if current_chunk != self.current_chunk:
            self.current_chunk = current_chunk
            self.update_loaded_chunks()
    
    def update_loaded_chunks(self):
        """Load and unload chunks based on render distance"""
        # Chunks to load
        chunks_to_load = set()
        for dx in range(-config.RENDER_DISTANCE, config.RENDER_DISTANCE + 1):
            for dz in range(-config.RENDER_DISTANCE, config.RENDER_DISTANCE + 1):
                chunk_coord = (
                    self.current_chunk[0] + dx,
                    self.current_chunk[1] + dz
                )
                chunks_to_load.add(chunk_coord)
        
        # Unload chunks that are too far
        chunks_to_unload = self.loaded_chunk_coords - chunks_to_load
        for chunk_coord in chunks_to_unload:
            if chunk_coord in self.chunks:
                self.chunks[chunk_coord].unload()
                del self.chunks[chunk_coord]
        
        # Load new chunks
        for chunk_coord in chunks_to_load - self.loaded_chunk_coords:
            chunk = Chunk(chunk_coord[0], chunk_coord[1])
            chunk.load()
            self.chunks[chunk_coord] = chunk
        
        self.loaded_chunk_coords = chunks_to_load
    
    def get_terrain_at_position(self, position):
        """Get terrain type at a position"""
        chunk_coord = self.get_chunk_at_position(position)
        if chunk_coord in self.chunks:
            return self.chunks[chunk_coord].terrain_type
        return 'road'
    
    def get_visual_objects_in_range(self):
        """Get all visual objects to render"""
        objects = []
        for chunk in self.chunks.values():
            if chunk.is_loaded:
                objects.extend(chunk.objects)
                objects.extend(chunk.road_segments)
        return objects
    
    def get_loaded_chunks(self):
        """Get all loaded chunks"""
        return list(self.chunks.values())
