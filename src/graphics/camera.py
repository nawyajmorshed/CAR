"""
Third-person camera system with smooth following
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import math
from physics import Physics
import config


class Camera:
    """Third-person follow camera"""
    
    def __init__(self, target_car):
        self.target_car = target_car
        self.position = np.array([0.0, config.CAMERA_FOLLOW_HEIGHT, -config.CAMERA_FOLLOW_DISTANCE], dtype=np.float32)
        self.lookat = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        
        # Camera parameters
        self.fov = 60.0
        self.base_fov = 60.0
        self.near = 0.1
        self.far = 5000.0
        self.distance = 12.0
        self.height = 3.0
        
        # For smooth lag
        self.target_position = self.position.copy()
        self.target_lookat = self.lookat.copy()
    
    def update(self, dt, width, height):
        """Update camera position and view"""
        car_pos = self.target_car.get_position()
        car_velocity = self.target_car.get_velocity()
        
        # Calculate desired camera position relative to car
        car_yaw = self.target_car.rotation[1]
        
        # Dynamic distance based on speed
        speed_factor = min(1.0, car_velocity / config.MAX_SPEED)
        self.distance = Physics.lerp(
            config.CAMERA_FOLLOW_DISTANCE,
            config.CAMERA_MAX_DISTANCE,
            speed_factor
        )
        
        # Camera height
        self.height = config.CAMERA_FOLLOW_HEIGHT
        
        # Calculate camera offset behind and above the car
        offset_distance = self.distance
        offset_x = math.sin(car_yaw) * offset_distance
        offset_z = math.cos(car_yaw) * offset_distance
        
        # Target camera position
        self.target_position = np.array([
            car_pos[0] + offset_x,
            car_pos[1] + self.height,
            car_pos[2] + offset_z
        ], dtype=np.float32)
        
        # Smooth camera follow using LERP (element-wise for numpy arrays)
        lerp_factor = config.CAMERA_FOLLOW_SPEED
        self.position = self.position * (1 - lerp_factor) + self.target_position * lerp_factor
        
        # Add camera shake at high speed
        if speed_factor > 0.7:
            shake_amount = (speed_factor - 0.7) * config.CAMERA_SHAKE_AMOUNT
            self.position[0] += (np.random.random() - 0.5) * shake_amount
            self.position[1] += (np.random.random() - 0.5) * shake_amount
            self.position[2] += (np.random.random() - 0.5) * shake_amount
        
        # Look at point slightly ahead of car
        lookahead = 10.0
        self.target_lookat = np.array([
            car_pos[0] + math.sin(car_yaw) * lookahead,
            car_pos[1] + 1.0,
            car_pos[2] + math.cos(car_yaw) * lookahead
        ], dtype=np.float32)
        
        # Smooth lookat
        lerp_factor = config.CAMERA_FOLLOW_SPEED * 0.5
        self.lookat = self.lookat * (1 - lerp_factor) + self.target_lookat * lerp_factor
        
        # Update FOV with nitro effect
        target_fov = self.base_fov
        if self.target_car.nitro_active:
            target_fov = self.base_fov + config.NITRO_FOV_BOOST
        
        self.fov = Physics.lerp(self.fov, target_fov, 0.1)
    
    def get_view_matrix(self):
        """Get the view matrix"""
        return self.look_at(self.position, self.lookat, self.up)
    
    def get_projection_matrix(self, width, height):
        """Get the projection matrix"""
        return self.perspective(self.fov, width / height, self.near, self.far)
    
    @staticmethod
    def look_at(eye, center, up):
        """Create a look-at matrix"""
        forward = center - eye
        forward = forward / np.linalg.norm(forward)
        
        right = np.cross(forward, up)
        right = right / np.linalg.norm(right)
        
        up_new = np.cross(right, forward)
        up_new = up_new / np.linalg.norm(up_new)
        
        result = np.identity(4, dtype=np.float32)
        result[0, 0:3] = right
        result[1, 0:3] = up_new
        result[2, 0:3] = -forward
        result[0, 3] = -np.dot(right, eye)
        result[1, 3] = -np.dot(up_new, eye)
        result[2, 3] = np.dot(forward, eye)
        
        return result
    
    @staticmethod
    def perspective(fov, aspect, near, far):
        """Create a perspective projection matrix"""
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        result = np.zeros((4, 4), dtype=np.float32)
        
        result[0, 0] = f / aspect
        result[1, 1] = f
        result[2, 2] = (far + near) / (near - far)
        result[2, 3] = -1.0
        result[3, 2] = (2.0 * far * near) / (near - far)
        
        return result
