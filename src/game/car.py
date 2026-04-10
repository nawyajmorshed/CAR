"""
Car system with physics and multiple car types
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import math
import numpy as np
from physics import Physics
import config


class CarType:
    """Defines properties of a specific car type"""
    
    def __init__(self, name, max_speed, acceleration, handling, weight):
        self.name = name
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.handling = handling
        self.weight = weight


# Predefined car types
CAR_TYPES = {
    'sports': CarType('Sports Car', max_speed=100, acceleration=40, handling=0.95, weight=1.0),
    'truck': CarType('Truck', max_speed=60, acceleration=15, handling=0.70, weight=2.0),
    'rally': CarType('Rally Car', max_speed=90, acceleration=37, handling=0.98, weight=0.9),
}


class Car:
    """Represents the player's car"""
    
    def __init__(self, car_type='sports', start_pos=(0, 0, 0)):
        self.car_type = CAR_TYPES.get(car_type, CAR_TYPES['sports'])
        self.position = np.array(start_pos, dtype=np.float32)
        self.rotation = np.array([0, 0, 0], dtype=np.float32)  # pitch, yaw, roll
        
        # Physics properties
        self.velocity = 0.0
        self.target_velocity = 0.0
        self.steering_angle = 0.0
        self.target_steering_angle = 0.0
        self.is_drifting = False
        
        # Nitro system
        self.nitro_amount = config.MAX_NITRO
        self.nitro_active = False
        self.nitro_boost = 1.0
        
        # Boost system (varying speeds based on ball color)
        self.boost_active = False
        self.boost_timer = 0.0
        self.boost_duration = 3.0  # 3 second duration for all boost balls
        self.boost_multiplier = 1.0  # Track current boost multiplier
        
        # Finish line tracking
        self.has_finished = False
        
        # Input state
        self.input_forward = False
        self.input_backward = False
        self.input_left = False
        self.input_right = False
        self.input_nitro = False
        
        # Terrain detection
        self.current_terrain = 'road'
        
        # Model matrix (for rendering)
        self.model_matrix = np.identity(4, dtype=np.float32)
    
    def update(self, dt, terrain_callback=None, world_objects=None, allow_movement=True):
        """Update car physics and state - improved smooth handling"""
        # Get current terrain
        if terrain_callback:
            self.current_terrain = terrain_callback(self.position)
        
        # Only process movement if race has started
        if not allow_movement:
            self.velocity = 0.0
            self.target_velocity = 0.0
            self.update_model_matrix()
            return
        
        # ===== VELOCITY CONTROL =====
        # Handle input to target velocity with smooth transitions
        if self.input_forward:
            # Forward = positive velocity (moving ahead)
            self.target_velocity = self.car_type.max_speed * self.nitro_boost
            # Apply boost multiplier if active
            if self.boost_active:
                self.target_velocity = self.target_velocity * self.boost_multiplier
        elif self.input_backward:
            # Backward = negative velocity (moving back)
            self.target_velocity = -self.car_type.max_speed * self.nitro_boost
        else:
            # No input - smooth deceleration to stop
            self.target_velocity = 0.0
        
        # Apply acceleration or smooth braking
        if abs(self.target_velocity) > abs(self.velocity):
            # Accelerating - use responsive acceleration
            accel = self.car_type.acceleration * 1.2  # Boost responsiveness
            self.velocity = Physics.apply_acceleration(
                self.velocity, accel, self.target_velocity, dt
            )
        else:
            # Decelerating/Braking - smooth deceleration
            brake_decel = config.BRAKE_DECELERATION * 1.1
            self.velocity = Physics.apply_braking(
                self.velocity, brake_decel, dt
            )
        
        # Apply terrain friction
        self.velocity = Physics.apply_terrain_friction(
            self.velocity, self.current_terrain, dt
        )
        
        # ===== STEERING CONTROL =====
        # Better simultaneous key handling
        target_steering = 0.0
        steering_magnitude = 0.0
        
        if self.input_left and self.input_right:
            # Both pressed - stay straight
            target_steering = 0.0
            steering_magnitude = 0.0
        elif self.input_left:
            # Turn left (positive steering angle)
            target_steering = math.radians(50)  # Positive for left
            steering_magnitude = 1.0
        elif self.input_right:
            # Turn right (negative steering angle)
            target_steering = math.radians(-50)  # Negative for right
            steering_magnitude = 1.0
        
        # Apply speed-sensitive steering
        if abs(self.velocity) > 10.0:
            # At speed: tighter steering for better control
            steering_scale = min(1.0, abs(self.velocity) / (config.MAX_SPEED * 0.5))
            target_steering *= steering_scale
        
        # Use improved smooth steering
        self.steering_angle = Physics.smooth_steering(
            self.steering_angle, target_steering, abs(self.velocity), dt
        )
        
        # ===== MOVEMENT CALCULATION =====
        # Check for drift
        self.is_drifting = abs(self.velocity) > config.DRIFT_THRESHOLD
        
        # Update position based on velocity and steering
        if abs(self.velocity) > 0.1:
            # steering_angle is already in radians
            # Calculate rotation/yaw change (responsive steering at any speed)
            speed_factor = min(2.0, abs(self.velocity) / (config.MAX_SPEED * 0.25))
            # Invert steering when moving backward (S key) so reverse steering works correctly
            steering_direction = 1.0 if self.velocity >= 0 else -1.0
            yaw_change = self.steering_angle * steering_direction * speed_factor * dt * 8
            self.rotation[1] += yaw_change  # yaw
            
            # Move forward in the direction we're facing (smooth movement)
            move_x = math.sin(self.rotation[1]) * self.velocity * dt
            move_z = math.cos(self.rotation[1]) * self.velocity * dt
            
            # Calculate new position with smooth interpolation
            new_x = self.position[0] + move_x
            new_z = self.position[2] + move_z
            
            self.position[0] = new_x
            self.position[2] = new_z
        else:
            # Below minimum velocity - instantly snap steering to center when stopped
            if abs(self.velocity) < 0.5 and not (self.input_left or self.input_right):
                self.steering_angle = 0.0
        
        # Check collision with barriers
        if world_objects:
            self.check_barrier_collision(world_objects)
            self.check_booster_collision(world_objects)
        
        # Hard boundary: Stop at end wall (z = 5950) to prevent flying off
        if self.position[2] > 5950:
            self.position[2] = 5950
            self.velocity = 0
        
        # Update boost timer
        if self.boost_active:
            self.boost_timer -= dt
            if self.boost_timer <= 0:
                self.boost_active = False
                self.boost_timer = 0.0
        
        # Update nitro
        self.update_nitro(dt)
        
        # Update model matrix
        self.update_model_matrix()
    
    def check_barrier_collision(self, world_objects):
        """Check collision with barriers and ground - allow car to slide"""
        car_radius = 1.5  # Increased from 0.9 for better detection
        push_distance = 5.0  # How far to push car back from barrier
        
        # Check ground collision first (prevent falling below Y=0)
        if self.position[1] < 1.0:
            self.position[1] = 1.0
        
        # HARD BOUNDARY: Keep car inside road at X = ±20 (where barriers are)
        # This prevents any chance of breakthrough at high speed
        if self.position[0] < -19.5:
            self.position[0] = -19.5
            # Reduce velocity component hitting the barrier (slide effect)
            self.velocity *= 0.5
        elif self.position[0] > 19.5:
            self.position[0] = 19.5
            # Reduce velocity component hitting the barrier (slide effect)
            self.velocity *= 0.5
        
        # Check against barriers and ground
        collision_detected = False
        for obj in world_objects:
            if obj.type in ['barrier', 'ground']:
                # Calculate bounding box
                obj_min_x = obj.position[0] - obj.scale[0] / 2
                obj_max_x = obj.position[0] + obj.scale[0] / 2
                obj_min_z = obj.position[2] - obj.scale[2] / 2
                obj_max_z = obj.position[2] + obj.scale[2] / 2
                obj_min_y = obj.position[1] - obj.scale[1] / 2
                obj_max_y = obj.position[1] + obj.scale[1] / 2
                
                # Check if car is within bounds (with larger collision radius)
                if (self.position[0] + car_radius > obj_min_x and
                    self.position[0] - car_radius < obj_max_x and
                    self.position[2] + car_radius > obj_min_z and
                    self.position[2] - car_radius < obj_max_z and
                    self.position[1] + car_radius > obj_min_y and
                    self.position[1] - car_radius < obj_max_y):
                    
                    collision_detected = True
                    
                    # Collision detected - PUSH CAR BACK OUT
                    # Calculate overlap on each side
                    overlap_left = abs((self.position[0] + car_radius) - obj_min_x)
                    overlap_right = abs(obj_max_x - (self.position[0] - car_radius))
                    overlap_top = abs((self.position[2] + car_radius) - obj_min_z)
                    overlap_bottom = abs(obj_max_z - (self.position[2] - car_radius))
                    overlap_down = abs((self.position[1] + car_radius) - obj_min_y)
                    overlap_up = abs(obj_max_y - (self.position[1] - car_radius))
                    
                    # Find smallest overlap (direction to push out)
                    overlaps = [
                        ('left', overlap_left),
                        ('right', overlap_right),
                        ('top', overlap_top),
                        ('bottom', overlap_bottom),
                        ('down', overlap_down),
                        ('up', overlap_up)
                    ]
                    
                    min_direction, min_overlap = min(overlaps, key=lambda x: x[1])
                    
                    # Push car back in the direction with smallest overlap
                    if min_direction == 'left':
                        self.position[0] = obj_min_x - car_radius - push_distance
                    elif min_direction == 'right':
                        self.position[0] = obj_max_x + car_radius + push_distance
                    elif min_direction == 'top':
                        self.position[2] = obj_min_z - car_radius - push_distance
                    elif min_direction == 'bottom':
                        self.position[2] = obj_max_z + car_radius + push_distance
                    elif min_direction == 'down':
                        self.position[1] = obj_min_y - car_radius - push_distance
                    elif min_direction == 'up':
                        self.position[1] = obj_max_y + car_radius + push_distance
        
        # If collision detected, reduce velocity but allow sliding
        if collision_detected:
            # Car slides and loses some speed but keeps moving forward
            self.velocity *= 0.6  # Keep 60% of velocity for smooth sliding effect
    
    def check_booster_collision(self, world_objects):
        """Check collision with power-up balls and apply boost based on ball color"""
        car_radius = 0.9  # Car half-width
        
        # Boost multipliers for each ball type
        boost_values = {
            'green_ball': 4.0,     # 4x speed for 3 seconds
            'red_ball': 0.25       # 1/4 speed (lose 4x speed) for 3 seconds
        }
        
        boost_durations = {
            'green_ball': 3.0,     # 3 second duration
            'red_ball': 3.0        # 3 second duration
        }
        
        for obj in world_objects:
            if obj.type in boost_values:
                # Skip already collected balls
                if hasattr(obj, 'collected') and obj.collected:
                    continue
                    
                # Calculate ball bounding box (treating balls as spheres with collision radius)
                ball_radius = 2.0  # Increased from 0.75 to 2.0 for easier pickup
                
                # Check distance to ball center
                dist_x = self.position[0] - obj.position[0]
                dist_z = self.position[2] - obj.position[2]
                distance = math.sqrt(dist_x**2 + dist_z**2)
                
                # Check if car collides with ball (with debug output)
                if distance < (car_radius + ball_radius):
                    print(f"✓ BALL COLLECTED: {obj.type} at distance {distance:.2f}")
                    # Ball collected - activate boost based on ball type
                    self.boost_active = True
                    self.boost_timer = boost_durations[obj.type]  # Set duration based on ball type (3 sec)
                    self.boost_multiplier = boost_values[obj.type]  # Set multiplier based on ball type
                    
                    # Remove ball from world IMMEDIATELY (mark as collected)
                    obj.collected = True
                    print(f"  Boost activated: {self.boost_multiplier}x for {self.boost_timer}s")
    
    def update_nitro(self, dt):
        """Update nitro meter and boost"""
        if self.input_nitro and self.nitro_amount > 0:
            self.nitro_active = True
            self.nitro_amount = max(0, self.nitro_amount - config.NITRO_CONSUMPTION_RATE * dt)
            self.nitro_boost = config.NITRO_BOOST_MULTIPLIER
        else:
            self.nitro_active = False
            self.nitro_amount = min(config.MAX_NITRO, self.nitro_amount + config.NITRO_RECHARGE_RATE * dt)
            self.nitro_boost = 1.0
    
    def get_nitro_percentage(self):
        """Return nitro amount as percentage (0-100)"""
        return (self.nitro_amount / config.MAX_NITRO) * 100.0
    
    def get_fov_boost(self):
        """Return FOV adjustment when nitro is active"""
        if self.nitro_active and self.input_nitro:
            return config.NITRO_FOV_BOOST
        return 0.0
    
    def update_model_matrix(self):
        """Update the model matrix for rendering"""
        # Create translation matrix
        T = np.identity(4, dtype=np.float32)
        T[0, 3] = self.position[0]
        T[1, 3] = self.position[1]
        T[2, 3] = self.position[2]
        
        # Create rotation matrices (YXZ order)
        yaw = self.rotation[1]
        pitch = self.rotation[0]
        roll = self.rotation[2]
        
        # Rotation around Y axis (yaw)
        Ry = np.identity(4, dtype=np.float32)
        Ry[0, 0] = math.cos(yaw)
        Ry[0, 2] = math.sin(yaw)
        Ry[2, 0] = -math.sin(yaw)
        Ry[2, 2] = math.cos(yaw)
        
        # Rotation around X axis (pitch)
        Rx = np.identity(4, dtype=np.float32)
        Rx[1, 1] = math.cos(pitch)
        Rx[1, 2] = -math.sin(pitch)
        Rx[2, 1] = math.sin(pitch)
        Rx[2, 2] = math.cos(pitch)
        
        # Rotation around Z axis (roll)
        Rz = np.identity(4, dtype=np.float32)
        Rz[0, 0] = math.cos(roll)
        Rz[0, 1] = -math.sin(roll)
        Rz[1, 0] = math.sin(roll)
        Rz[1, 1] = math.cos(roll)
        
        # Scale matrix for car (cube)
        S = np.identity(4, dtype=np.float32)
        S[0, 0] = 2.0  # width
        S[1, 1] = 1.5  # height
        S[2, 2] = 4.0  # length
        
        # Combine: T * Ry * Rx * Rz * S
        self.model_matrix = T @ Ry @ Rx @ Rz @ S
    
    def set_input(self, key, pressed):
        """Handle input"""
        if key == 'w':
            self.input_forward = pressed  # W = forward
        elif key == 's':
            self.input_backward = pressed  # S = backward  
        elif key == 'a':
            self.input_left = pressed
        elif key == 'd':
            self.input_right = pressed
        elif key == 'shift':
            self.input_nitro = pressed
    
    def get_position(self):
        """Get car position"""
        return self.position
    
    def get_velocity(self):
        """Get current speed"""
        return self.velocity


class AICar:
    """Represents an AI-controlled car that races on the track"""
    
    def __init__(self, ai_id, car_type='sports', lane_offset=0, start_z=0):
        self.ai_id = ai_id  # 0, 1, 2 for the three AI cars
        self.car_type = CAR_TYPES.get(car_type, CAR_TYPES['sports'])
        self.position = np.array([lane_offset, 1.0, start_z], dtype=np.float32)
        self.rotation = np.array([0, 0, 0], dtype=np.float32)  # pitch, yaw, roll
        
        # Physics properties
        self.velocity = 0.0
        self.target_velocity = self.car_type.max_speed * 0.8  # AI drives at 80% max speed
        self.lane_offset = lane_offset  # Target x position (-8, 0, 8)
        
        # Boost system (varying speeds based on ball color)
        self.boost_active = False
        self.boost_timer = 0.0
        self.boost_duration = 3.0  # 3 second duration for all boost balls
        self.boost_multiplier = 1.0  # Track current boost multiplier
        
        # Finish line tracking
        self.has_finished = False
        
        # Nitro system
        self.nitro_boost = 1.0
        
        # Model matrix
        self.model_matrix = np.identity(4, dtype=np.float32)
    
    def update(self, dt, world_objects=None, allow_movement=True):
        """Update AI car physics and movement - smooth and responsive"""
        # Stop if race hasn't started
        if not allow_movement:
            self.velocity = 0.0
            self.update_model_matrix()
            return
        
        # ===== VELOCITY CONTROL =====
        # Calculate target velocity with boost and smooth acceleration
        base_target = self.car_type.max_speed * 0.9  # Slightly increased for better racing
        if self.boost_active:
            self.target_velocity = base_target * self.boost_multiplier  # Use dynamic multiplier
        else:
            self.target_velocity = base_target
        
        # Smooth acceleration towards target velocity (responsive)
        if abs(self.target_velocity) > abs(self.velocity):
            accel = self.car_type.acceleration * 1.1  # Slightly boosted for responsiveness
            self.velocity = Physics.apply_acceleration(
                self.velocity, accel, self.target_velocity, dt
            )
        else:
            # Reduce acceleration if at target
            self.velocity = Physics.apply_acceleration(
                self.velocity, self.car_type.acceleration * 0.9, self.target_velocity, dt
            )
        
        # ===== MOVEMENT =====
        # Move forward (z direction)
        move_z = self.velocity * dt
        self.position[2] += move_z
        
        # Stay in lane with smooth drifting
        lane_diff = self.position[0] - self.lane_offset
        if abs(lane_diff) > 0.15:
            # Smooth lane correction
            drift_speed = 1.5 * (abs(lane_diff) / 2.0)  # Speed depends on distance
            drift_speed = min(drift_speed, 3.0)  # Cap maximum drift correction speed
            if lane_diff > 0:
                self.position[0] -= drift_speed * dt
            else:
                self.position[0] += drift_speed * dt
        
        # ===== COLLISION HANDLING =====
        # Check collision with barriers
        if world_objects:
            car_radius = 1.0  # Consistent with player car
            collision_detected = False
            
            for obj in world_objects:
                if obj.type == 'barrier':
                    barrier_min_x = obj.position[0] - obj.scale[0] / 2
                    barrier_max_x = obj.position[0] + obj.scale[0] / 2
                    barrier_min_z = obj.position[2] - obj.scale[2] / 2
                    barrier_max_z = obj.position[2] + obj.scale[2] / 2
                    
                    if (self.position[0] + car_radius > barrier_min_x and
                        self.position[0] - car_radius < barrier_max_x and
                        self.position[2] + car_radius > barrier_min_z and
                        self.position[2] - car_radius < barrier_max_z):
                        
                        # Collision detected - push back and slide (like player)
                        collision_detected = True
                        
                        # Push back slightly
                        if self.position[0] < barrier_min_x:
                            self.position[0] = barrier_min_x - car_radius - 2.0
                        elif self.position[0] > barrier_max_x:
                            self.position[0] = barrier_max_x + car_radius + 2.0
                        
                        # Reduce speed but allow sliding
                        self.velocity *= 0.65
            
            # Hard boundaries at track edges (like player)
            if self.position[0] < -19.5:
                self.position[0] = -19.5
                self.velocity *= 0.5
            elif self.position[0] > 19.5:
                self.position[0] = 19.5
                self.velocity *= 0.5
            
            # Check for power-up ball collisions
            self.check_booster_collision(world_objects)
        
        # ===== BOOST TIMER =====
        # Update boost timer
        if self.boost_active:
            self.boost_timer -= dt
            if self.boost_timer <= 0:
                self.boost_active = False
                self.boost_timer = 0.0
        
        # Reset to start if went off track (safety)
        if self.position[2] > 6000:
            self.position[2] = 0
        
        # Hard boundary: Stop at end wall (z = 5950) to prevent flying off
        if self.position[2] > 5950:
            self.position[2] = 5950
            self.velocity = 0
        
        self.update_model_matrix()
    
    def check_booster_collision(self, world_objects):
        """Check collision with power-up balls and apply boost based on ball color"""
        if world_objects is None:
            return
        
        car_radius = 0.9  # Car half-width
        
        # Boost multipliers for each ball type
        boost_values = {
            'green_ball': 4.0,     # 4x speed for 3 seconds
            'red_ball': 0.25       # 1/4 speed (lose 4x speed) for 3 seconds
        }
        
        boost_durations = {
            'green_ball': 3.0,     # 3 second duration
            'red_ball': 3.0        # 3 second duration
        }
        
        for obj in world_objects:
            if obj.type in boost_values:
                # Skip already collected balls
                if hasattr(obj, 'collected') and obj.collected:
                    continue
                    
                # Calculate ball bounding box (treating balls as spheres with collision radius)
                ball_radius = 2.0  # Increased from 0.75 to 2.0 for easier pickup
                
                # Check distance to ball center
                dist_x = self.position[0] - obj.position[0]
                dist_z = self.position[2] - obj.position[2]
                distance = math.sqrt(dist_x**2 + dist_z**2)
                
                # Check if car collides with ball
                if distance < (car_radius + ball_radius):
                    print(f"✓ AI BALL COLLECTED: {obj.type} at distance {distance:.2f}")
                    # Ball collected - activate boost based on ball type
                    self.boost_active = True
                    self.boost_timer = boost_durations[obj.type]  # Set duration based on ball type (3 sec)
                    self.boost_multiplier = boost_values[obj.type]  # Set multiplier based on ball type
                    
                    # Remove ball from world IMMEDIATELY (mark as collected)
                    obj.collected = True
    
    def update_model_matrix(self):
        """Update model matrix for rendering"""
        T = np.identity(4, dtype=np.float32)
        T[0, 3] = self.position[0]
        T[1, 3] = self.position[1]
        T[2, 3] = self.position[2]
        
        S = np.identity(4, dtype=np.float32)
        S[0, 0] = 2.0
        S[1, 1] = 1.5
        S[2, 2] = 4.0
        
        self.model_matrix = T @ S
    
    def get_velocity(self):
        """Get current speed"""
        return self.velocity
