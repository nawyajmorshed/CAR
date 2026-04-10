"""
World generation and environment system
"""
import numpy as np
import math
import config
from chunk_manager import ChunkManager
from car import AICar


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
        """Create 6 AI cars that race on the track"""
        # AI Car 1 - Blue Rally Car
        ai1 = AICar(ai_id=0, car_type='rally', lane_offset=-15, start_z=100)
        self.ai_cars.append(ai1)
        
        # AI Car 2 - Yellow Sports Car
        ai2 = AICar(ai_id=1, car_type='sports', lane_offset=-10, start_z=100)
        self.ai_cars.append(ai2)
        
        # AI Car 3 - Magenta Truck (Pink) - closer to Yellow
        ai3 = AICar(ai_id=2, car_type='truck', lane_offset=-3, start_z=100)
        self.ai_cars.append(ai3)
        
        # AI Car 4 - Cyan Sports Car
        ai4 = AICar(ai_id=3, car_type='sports', lane_offset=3, start_z=100)
        self.ai_cars.append(ai4)
        
        # AI Car 5 - Orange Rally Car
        ai5 = AICar(ai_id=4, car_type='rally', lane_offset=15, start_z=100)
        self.ai_cars.append(ai5)
        
        # AI Car 6 - Purple Truck
        ai6 = AICar(ai_id=5, car_type='truck', lane_offset=20, start_z=100)
        self.ai_cars.append(ai6)
    
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
        """Generate straight highway with 3 lanes"""
        road_id = 0
        
        # MAIN HIGHWAY - Straight road - 3 lanes
        # Road starts at z=0 (car spawn) and extends forward
        for i in range(300):
            z_start = 0 + i * 20
            z_end = 0 + (i + 1) * 20
            
            # Straight road - no curves
            x_offset = 0
            
            # 3 lanes for full road width coverage
            for lane_offset in [-8, 0, 8]:
                start = [lane_offset + x_offset, 0, z_start]
                end = [lane_offset + x_offset, 0, z_end]
                
                road = RoadSegment(road_id, start, end, config.ROAD_WIDTH, 'highway')
                self.road_segments.append(road)
                road_id += 1
    
    def generate_environment(self):
        """Generate barriers on both sides of road"""
        
        # Start line with poles and checkered pattern
        # Left pole for start
        start_pole_left = EnvironmentObject('pole',
                                           position=[-25, 2, 100],
                                           scale=[1, 4, 1])
        self.environment_objects.append(start_pole_left)
        
        # Right pole for start
        start_pole_right = EnvironmentObject('pole',
                                            position=[25, 2, 100],
                                            scale=[1, 4, 1])
        self.environment_objects.append(start_pole_right)
        
        # Start line (checkered pattern)
        start_line = EnvironmentObject('start_line',
                                      position=[0, 0.0, 100],
                                      scale=[50, 0.1, 2])
        self.environment_objects.append(start_line)
        
        # Finish line with poles and checkered pattern
        # Left pole for finish
        finish_pole_left = EnvironmentObject('pole',
                                            position=[-25, 2, 5900],
                                            scale=[1, 4, 1])
        self.environment_objects.append(finish_pole_left)
        
        # Right pole for finish
        finish_pole_right = EnvironmentObject('pole',
                                             position=[25, 2, 5900],
                                             scale=[1, 4, 1])
        self.environment_objects.append(finish_pole_right)
        
        # Finish line (checkered pattern)
        finish_line = EnvironmentObject('finish_line',
                                       position=[0, 0.0, 5900],
                                       scale=[50, 0.1, 2])
        self.environment_objects.append(finish_line)
        
        # Add end wall where road meets sky (blocks cars from flying off)
        end_wall = EnvironmentObject('barrier',
                                    position=[0, 2.0, 5950],
                                    scale=[50, 4.0, 1])
        self.environment_objects.append(end_wall)
        
        # Add power-up balls scattered along the track
        # green_ball (4x speed, 3 sec), red_ball (-4x speed/slow, 3 sec), yellow_ball (4x speed, 3 sec)
        for z in range(500, 5900, 300):  # Every 300 units for more boost balls
            # Green ball on left lane (4x speed for 3 sec)
            green_ball = EnvironmentObject('green_ball',
                                          position=[-8, 1.5, z],  # Middle of left lane
                                          scale=[1.5, 1.5, 1.5])  # Sphere-like
            green_ball.collected = False
            self.environment_objects.append(green_ball)
            
            # Red ball on right lane (lose speed 4x for 3 sec - slow down effect)
            red_ball = EnvironmentObject('red_ball',
                                        position=[8, 1.5, z + 150],  # Right lane
                                        scale=[1.5, 1.5, 1.5])  # Sphere-like
            red_ball.collected = False
            self.environment_objects.append(red_ball)
            
            # Yellow ball center (4x speed for 3 sec)
            yellow_ball = EnvironmentObject('yellow_ball',
                                           position=[0, 1.5, z + 75],
                                           scale=[1.5, 1.5, 1.5])
            yellow_ball.collected = False
            self.environment_objects.append(yellow_ball)
        
        # Generate barriers with reduced density for better performance
        for i in range(299):
            z_start = 0 + i * 20
            z_end = 0 + (i + 1) * 20
            
            # Straight barriers - no curves, match road
            x_offset = 0
            
            # Left barrier - thin guardrail
            barrier_left = EnvironmentObject('barrier', 
                                            position=[-20 + x_offset, 0.8, (z_start + z_end) / 2],
                                            scale=[0.5, 1.6, 20])  # thin, width, height, depth
            self.environment_objects.append(barrier_left)
            
            # Right barrier - thin guardrail
            barrier_right = EnvironmentObject('barrier',
                                            position=[20 + x_offset, 0.8, (z_start + z_end) / 2],
                                            scale=[0.5, 1.6, 20])  # thin, width, height, depth
            self.environment_objects.append(barrier_right)
    
    def update(self, car_position):
        """Update world based on car position"""
        self.chunk_manager.update(car_position)
    
    def get_terrain_at_position(self, position):
        """Get terrain type at position"""
        return self.chunk_manager.get_terrain_at_position(position)
