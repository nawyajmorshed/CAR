"""
Game core modules - car physics, world generation, chunk management
"""
from .car import Car, AICar, CarType
from .world import World, RoadSegment, EnvironmentObject
from .chunk_manager import ChunkManager

__all__ = ['Car', 'AICar', 'CarType', 'World', 'RoadSegment', 'EnvironmentObject', 'ChunkManager']
