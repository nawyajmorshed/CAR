"""
Physics calculations for the car and world
"""
import math
import config


class Physics:
    """Physics engine for car movement"""
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply_acceleration(velocity, acceleration, target_velocity, dt):
        """Apply smooth acceleration with quick response"""
        # Move towards target velocity with exponential easing for smoothness
        diff = target_velocity - velocity
        
        if abs(diff) > 0.1:  # Only apply if difference is significant
            # Exponential approach for smooth acceleration
            if target_velocity > velocity:
                # Accelerate forward - faster response
                velocity += acceleration * dt * (1.0 + abs(diff) / max(1.0, abs(target_velocity)))
                velocity = min(velocity, target_velocity)
            elif target_velocity < velocity:
                # Decelerate/accelerate backward
                velocity -= acceleration * dt * (1.0 + abs(diff) / max(1.0, abs(target_velocity)))
                velocity = max(velocity, target_velocity)
        else:
            # Snap to target if very close
            velocity = target_velocity
        
        return velocity
    
    @staticmethod
    def apply_friction(velocity, friction_coefficient, dt):
        """Apply friction/drag to velocity"""
        friction_force = velocity * config.DRAG_COEFFICIENT
        velocity -= friction_force * dt
        if abs(velocity) < 0.01:
            velocity = 0.0
        return velocity
    
    @staticmethod
    def apply_braking(velocity, deceleration, dt):
        """Apply braking deceleration"""
        if velocity > 0:
            velocity = max(0, velocity - deceleration * dt)
        elif velocity < 0:
            velocity = min(0, velocity + deceleration * dt)
        return velocity
    
    @staticmethod
    def apply_terrain_friction(velocity, terrain_type, dt):
        """Apply different friction based on terrain type"""
        friction_map = {
            'road': config.ROAD_FRICTION,
            'dirt': config.DIRT_FRICTION,
            'grass': config.GRASS_FRICTION,
        }
        
        friction = friction_map.get(terrain_type, config.ROAD_FRICTION)
        velocity *= friction
        return velocity
    
    @staticmethod
    def smooth_steering(current_angle, target_angle, speed, dt):
        """Ultra-responsive steering with speed sensitivity"""
        # Convert STEERING_SPEED from degrees per second to radians per second
        steering_speed_rad_per_sec = math.radians(config.STEERING_SPEED)
        
        # Speed multiplier: faster steering response at higher speeds
        speed_multiplier = 1.0 + (abs(speed) / config.MAX_SPEED) * 0.5  # Up to 1.5x faster
        max_change = steering_speed_rad_per_sec * dt * speed_multiplier * config.STEERING_INPUT_SENSITIVITY
        
        # Calculate angle difference
        diff = target_angle - current_angle
        
        # Wrap angle to [-pi, pi]
        while diff > math.pi:
            diff -= 2 * math.pi
        while diff < -math.pi:
            diff += 2 * math.pi
        
        # Snap to target angle more aggressively for responsive feel
        if abs(diff) > max_change:
            current_angle += math.copysign(max_change, diff)
        else:
            # Immediately snap to target if very close
            if abs(diff) < math.radians(2.0):
                current_angle = target_angle
            else:
                current_angle += diff * 0.95  # Fast lerp for responsiveness
        
        return current_angle
    
    @staticmethod
    def calculate_drift(velocity, steering_angle):
        """Calculate drift effect at high speed"""
        drift_factor = 1.0
        if velocity > config.DRIFT_THRESHOLD:
            excess_speed = velocity - config.DRIFT_THRESHOLD
            drift_factor = 1.0 + (excess_speed / config.MAX_SPEED) * 0.3
        return drift_factor
    
    @staticmethod
    def lerp(a, b, t):
        """Linear interpolation"""
        t = max(0, min(1, t))
        return a + (b - a) * t
