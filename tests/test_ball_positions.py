#!/usr/bin/env python3
"""
Test script to check ball and car positions to debug collision issues
"""
import sys
sys.path.insert(0, 'src')

from game import World, Car
import numpy as np

# Create world and car
print("Creating world and car...")
w = World()
c = Car('sports')

# Get all balls
green_balls = [o for o in w.environment_objects if o.type == 'green_ball']
red_balls = [o for o in w.environment_objects if o.type == 'red_ball']

print(f"\nTotal balls: {len(green_balls)} green, {len(red_balls)} red")
print(f"Car position: {c.position}")

# Check first 5 green balls
print("\n=== FIRST 5 GREEN BALLS ===")
for i, ball in enumerate(green_balls[:5]):
    dist_x = c.position[0] - ball.position[0]
    dist_z = c.position[2] - ball.position[2]
    dist = np.sqrt(dist_x**2 + dist_z**2)
    collision_dist = 0.9 + 2.0  # car_radius + ball_radius
    print(f"Ball {i}: pos={ball.position}, dist={dist:.2f}, collision_threshold={collision_dist:.2f}")
    print(f"         In range? {dist < collision_dist}")

# Simulate car movement towards a ball
print("\n=== SIMULATING CAR MOVEMENT ===")
if green_balls:
    target_ball = green_balls[0]
    print(f"Target ball position: {target_ball.position}")
    
    # Move car stepwise towards the ball
    for step in range(10):
        # Linear interpolation towards ball
        progress = (step + 1) / 10
        new_pos = c.position + (target_ball.position - c.position) * progress
        new_pos[1] = 1.0  # Keep Y at ground level
        
        dist_x = new_pos[0] - target_ball.position[0]
        dist_z = new_pos[2] - target_ball.position[2]
        dist = np.sqrt(dist_x**2 + dist_z**2)
        collision_threshold = 0.9 + 2.0
        
        print(f"Step {step+1}: car_pos={new_pos}, dist={dist:.2f}, would_collide={dist < collision_threshold}")
