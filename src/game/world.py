"""
World generation and environment system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import math
import config
from .chunk_manager import ChunkManager
from .car import AICar


class RoadSegment:
    """Represents a segment of road"""
    
    def __init__(self, segment_id, start_pos, end_pos, width=config.ROAD_WIDTH, road_type='highway'):
        self.id = segment_id
        self.start_pos = np.array(start_pos, dtype=np.float32)
        self.end_pos = np.array(end_pos, dtype=np.float32)
        self.width = width
        self.road_type = road_type
        
        # Generate mesh
        self.vertices = []
        self.indices = []
        self.normals = []
        self.texcoords = []
        self.vao = None
        self.vertex_count = 0
        
        self.generate_mesh()
    
    def generate_mesh(self):
        """Generate road mesh geometry"""
        # Road direction
        direction = self.end_pos - self.start_pos
        length = np.linalg.norm(direction)
        direction = direction / length
        
        # Perpendicular vector (right side)
        right = np.array([-direction[2], 0, direction[0]], dtype=np.float32)
        
        # Vertices: 4 corners of the road
        half_width = self.width / 2.0
        
        # Front edge
        v0 = self.start_pos - right * half_width
        v1 = self.start_pos + right * half_width
        
        # Back edge
        v2 = self.end_pos - right * half_width
        v3 = self.end_pos + right * half_width
        
        # Bottom vertices (shadow)
        v4 = v0 - np.array([0, 0.1, 0], dtype=np.float32)
        v5 = v1 - np.array([0, 0.1, 0], dtype=np.float32)
        v6 = v2 - np.array([0, 0.1, 0], dtype=np.float32)
        v7 = v3 - np.array([0, 0.1, 0], dtype=np.float32)
        
        self.vertices = [
            v0, v1, v2, v3,  # Top surface
            v4, v5, v6, v7   # Bottom surface
        ]
        
        # Normals
        normal_up = np.array([0, 1, 0], dtype=np.float32)
        normal_down = np.array([0, -1, 0], dtype=np.float32)
        
        self.normals = [
            normal_up, normal_up, normal_up, normal_up,
            normal_down, normal_down, normal_down, normal_down
        ]
        
        # Texture coordinates
        self.texcoords = [
            [0, 0], [1, 0], [1, 1], [0, 1],
            [0, 0], [1, 0], [1, 1], [0, 1]
        ]
        
        # Indices (triangles)
        # Top surface
        self.indices = [
            0, 1, 2,  # First triangle
            1, 3, 2,  # Second triangle
            # Side 1
            0, 2, 4,
            2, 6, 4,
            # Side 2
            1, 5, 3,
            5, 7, 3,
            # Bottom
            4, 6, 5,
            6, 7, 5,
        ]
        
        self.vertex_count = len(self.indices)


class EnvironmentObject:
    """Represents a building, tree, or other environment object"""
    
    types = ['building', 'tree', 'streetlight', 'billboard']
    
    def __init__(self, obj_type, position, rotation=None, scale=None):
        self.type = obj_type
        self.position = np.array(position, dtype=np.float32)
        self.rotation = np.array(rotation if rotation else [0, 0, 0], dtype=np.float32)
        self.scale = np.array(scale if scale else [1, 1, 1], dtype=np.float32)
        self.vertices = []
        self.indices = []
        self.normals = []
        self.texcoords = []
        self.collected = False  # Initialize for all objects (used for pickup items)
        
        self.generate_mesh()
    
    def generate_mesh(self):
        """Generate mesh based on object type"""
        if self.type == 'building':
            self.generate_building()
        elif self.type == 'tree':
            self.generate_tree()
        elif self.type == 'streetlight':
            self.generate_streetlight()
        elif self.type == 'billboard':
            self.generate_billboard()
    
    def generate_building(self):
        """Generate a simple building cube"""
        # Create a rectangular building
        half_w = self.scale[0] / 2.0
        half_d = self.scale[2] / 2.0
        height = self.scale[1]
        
        self.vertices = [
            # Front face
            [-half_w, 0, half_d], [half_w, 0, half_d], [half_w, height, half_d], [-half_w, height, half_d],
            # Back face
            [-half_w, 0, -half_d], [half_w, 0, -half_d], [half_w, height, -half_d], [-half_w, height, -half_d],
            # Top
            [-half_w, height, half_d], [half_w, height, half_d], [half_w, height, -half_d], [-half_w, height, -half_d],
            # Bottom
            [-half_w, 0, half_d], [half_w, 0, half_d], [half_w, 0, -half_d], [-half_w, 0, -half_d],
        ]
        
        self.indices = [
            0, 1, 2, 0, 2, 3,  # Front
            5, 4, 7, 5, 7, 6,  # Back
            8, 9, 10, 8, 10, 11,  # Top
            15, 14, 13, 15, 13, 12,  # Bottom
            4, 5, 1, 4, 1, 0,  # Right
            3, 2, 6, 3, 6, 7,  # Left
        ]
        
        normal_front = [0, 0, 1]
        normal_back = [0, 0, -1]
        normal_top = [0, 1, 0]
        normal_bottom = [0, -1, 0]
        normal_right = [1, 0, 0]
        normal_left = [-1, 0, 0]
        
        vertex_count = len(self.vertices)
        self.normals = [[0, 1, 0]] * vertex_count
        self.texcoords = [[i % 2, (i // 2) % 2] for i in range(vertex_count)]
    
    def generate_tree(self):
        """Generate a simple tree cylinder"""
        radius = self.scale[0]
        height = self.scale[1]
        segments = 8
        
        # Trunk
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            self.vertices.append([x, 0, z])
        
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            self.vertices.append([x, height, z])
        
        # Side faces
        for i in range(segments):
            next_i = (i + 1) % segments
            self.indices.extend([
                i, i + segments, next_i + segments,
                i, next_i + segments, next_i
            ])
        
        self.normals = [[0, 1, 0]] * len(self.vertices)
        self.texcoords = [[i % 2, (i // 2) % 2] for i in range(len(self.vertices))]
    
    def generate_streetlight(self):
        """Generate a streetlight pole"""
        # Simple pole
        self.vertices = [
            [-0.2, 0, -0.2], [0.2, 0, -0.2], [0.2, self.scale[1], -0.2], [-0.2, self.scale[1], -0.2],
            [-0.2, 0, 0.2], [0.2, 0, 0.2], [0.2, self.scale[1], 0.2], [-0.2, self.scale[1], 0.2],
        ]
        self.indices = [0, 1, 2, 0, 2, 3, 5, 4, 7, 5, 7, 6]
        self.normals = [[0, 1, 0]] * len(self.vertices)
        self.texcoords = [[0, 0], [1, 0], [1, 1], [0, 1]] * 2
    
    def generate_billboard(self):
        """Generate a billboard plane"""
        w = self.scale[0]
        h = self.scale[1]
        
        self.vertices = [
            [-w/2, 0, 0], [w/2, 0, 0], [w/2, h, 0], [-w/2, h, 0]
        ]
        self.indices = [0, 1, 2, 0, 2, 3]
        self.normals = [[0, 0, 1]] * 4
        self.texcoords = [[0, 0], [1, 0], [1, 1], [0, 1]]


class World:
    """Manages the game world"""
    
    def __init__(self):
        self.chunk_manager = ChunkManager()
        self.road_segments = []
        self.environment_objects = []
        self.ai_cars = []  # List of AI cars
        self.generate_world()
        self.create_ai_cars()
    
    def create_ai_cars(self):
        """Create 6 AI cars that race on the track, spread across the wider road."""
        # Spread AI cars evenly across the playable width (between barriers)
        # Barriers sit at +/- config.BARRIER_OFFSET; keep a margin of ~6m.
        max_lateral = config.BARRIER_OFFSET - 8.0
        offsets = np.linspace(-max_lateral, max_lateral, 6)
        car_types = ['rally', 'sports', 'truck', 'sports', 'rally', 'truck']
        for i, (offset, ctype) in enumerate(zip(offsets, car_types)):
            self.ai_cars.append(
                AICar(ai_id=i, car_type=ctype, lane_offset=float(offset), start_z=100))
    
    def generate_world(self):
        """Generate initial world"""
        self.generate_roads()
        self.generate_environment()
    
    def generate_ground(self):
        """Generate ground tiles outside the barriers"""
        # Ground only appears outside the barrier area (x < -25 or x > 25)
        # Road with barriers is inside (between x=-20 and x=20)
        ground_tile_size = 100  # Size of each ground tile
        
        # Create ground patches only outside barriers
        for z in range(0, 6000, ground_tile_size):
            # Ground on the left side (outside left barrier)
            for x in range(-200, -25, ground_tile_size):
                ground = EnvironmentObject('ground',
                                          position=[x, -0.5, z],
                                          scale=[ground_tile_size, 1.0, ground_tile_size])
                self.environment_objects.append(ground)
            
            # Ground on the right side (outside right barrier)
            for x in range(25, 200, ground_tile_size):
                ground = EnvironmentObject('ground',
                                          position=[x, -0.5, z],
                                          scale=[ground_tile_size, 1.0, ground_tile_size])
                self.environment_objects.append(ground)
    
    def generate_roads(self):
        """Generate straight highway whose width and length come from config"""
        road_id = 0
        seg_len = config.TRACK_SEGMENT_LENGTH
        num_segments = int(config.TRACK_LENGTH / seg_len)

        # MAIN HIGHWAY - Straight road
        for i in range(num_segments):
            z_start = i * seg_len
            z_end = (i + 1) * seg_len

            for lane_offset in config.LANE_OFFSETS:
                start = [lane_offset, 0, z_start]
                end = [lane_offset, 0, z_end]
                road = RoadSegment(road_id, start, end, config.ROAD_WIDTH, 'highway')
                self.road_segments.append(road)
                road_id += 1
    
    def generate_environment(self):
        """Generate barriers, markers, pickups and roadside scenery."""
        track_len = config.TRACK_LENGTH
        finish_z = track_len - 100.0   # leave 100m runoff before end wall
        start_z = 100.0
        seg_len = config.TRACK_SEGMENT_LENGTH
        barrier_x = config.BARRIER_OFFSET
        pole_x = barrier_x + 3.0
        line_width = (barrier_x * 2) + 10.0  # spans the full road plus margin

        # --- Start line & poles ---
        self.environment_objects.append(
            EnvironmentObject('pole', position=[-pole_x, 2, start_z], scale=[1, 4, 1]))
        self.environment_objects.append(
            EnvironmentObject('pole', position=[pole_x, 2, start_z], scale=[1, 4, 1]))
        self.environment_objects.append(
            EnvironmentObject('start_line', position=[0, 0.0, start_z],
                              scale=[line_width, 0.1, 2]))

        # --- Finish line & poles ---
        self.environment_objects.append(
            EnvironmentObject('pole', position=[-pole_x, 2, finish_z], scale=[1, 4, 1]))
        self.environment_objects.append(
            EnvironmentObject('pole', position=[pole_x, 2, finish_z], scale=[1, 4, 1]))
        self.environment_objects.append(
            EnvironmentObject('finish_line', position=[0, 0.0, finish_z],
                              scale=[line_width, 0.1, 2]))

        # End wall closes off the track
        self.environment_objects.append(
            EnvironmentObject('barrier', position=[0, 2.0, finish_z + 50],
                              scale=[line_width, 4.0, 1]))

        # --- Power-up balls scattered along the track ---
        ball_lanes = config.LANE_OFFSETS  # use the same lanes the road uses
        ball_index = 0
        z = int(start_z)
        while z < finish_z - 50:
            green_x = ball_lanes[ball_index % len(ball_lanes)]
            green_ball = EnvironmentObject('green_ball',
                                           position=[green_x, 1.5, z + 50],
                                           scale=[1.5, 1.5, 1.5])
            green_ball.collected = False
            self.environment_objects.append(green_ball)

            red_x = ball_lanes[(ball_index + 1) % len(ball_lanes)]
            red_ball = EnvironmentObject('red_ball',
                                         position=[red_x, 1.5, z + 200],
                                         scale=[1.5, 1.5, 1.5])
            red_ball.collected = False
            self.environment_objects.append(red_ball)

            ball_index += 1
            z += 300

        # --- Guardrails along the entire length ---
        num_segments = int(track_len / seg_len)
        for i in range(num_segments - 1):
            z_mid = (i + 0.5) * seg_len
            self.environment_objects.append(
                EnvironmentObject('barrier',
                                  position=[-barrier_x, 0.8, z_mid],
                                  scale=[0.5, 1.6, seg_len]))
            self.environment_objects.append(
                EnvironmentObject('barrier',
                                  position=[barrier_x, 0.8, z_mid],
                                  scale=[0.5, 1.6, seg_len]))

        # --- Roadside scenery: trees and buildings outside the barriers ---
        # Deterministic placement so the world is reproducible.
        rng = np.random.default_rng(seed=42)
        scenery_step = 60.0   # one prop band every 60m of track length
        side_min = barrier_x + 8.0
        side_max = barrier_x + 120.0
        num_bands = int(track_len / scenery_step)
        for band in range(num_bands):
            z = band * scenery_step + rng.uniform(-15, 15)
            if z < 50 or z > track_len - 50:
                continue
            for sign in (-1, 1):
                x = sign * rng.uniform(side_min, side_max)
                # ~30% buildings, 70% trees
                if rng.random() < 0.3:
                    h = rng.uniform(10, 35)
                    w = rng.uniform(8, 18)
                    d = rng.uniform(8, 18)
                    self.environment_objects.append(
                        EnvironmentObject('building', position=[x, 0, z],
                                          scale=[w, h, d]))
                else:
                    h = rng.uniform(5, 12)
                    r = rng.uniform(1.0, 2.2)
                    self.environment_objects.append(
                        EnvironmentObject('tree', position=[x, 0, z],
                                          scale=[r, h, r]))
    
    def update(self, car_position):
        """Update world based on car position"""
        self.chunk_manager.update(car_position)
    
    def get_terrain_at_position(self, position):
        """Get terrain type at position"""
        return self.chunk_manager.get_terrain_at_position(position)
