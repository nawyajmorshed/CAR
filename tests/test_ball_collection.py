#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from game import World, Car
import math

# Create world and car
w = World()
c = Car('sports')

# Find a green ball
green_balls = [o for o in w.environment_objects if o.type == 'green_ball']
print(f"Found {len(green_balls)} green balls")

if green_balls:
    ball = green_balls[0]
    print(f"\nBall info:")
    print(f"  Type: {ball.type}")
    print(f"  Position: {ball.position}")
    print(f"  Collected: {getattr(ball, 'collected', 'NOT SET')}")
    
    # Simulate collision by moving car to ball
    print(f"\nMoving car to ball position...")
    c.position = ball.position.copy()
    
    # Call collision check
    print(f"Calling check_booster_collision...")
    c.check_booster_collision(w.environment_objects)
    
    print(f"\nAfter collision check:")
    print(f"  Ball collected: {ball.collected}")
    print(f"  Car boost active: {c.boost_active}")
    print(f"  Car boost multiplier: {c.boost_multiplier}")
    
    if ball.collected:
        print("\n✅ Ball correctly marked as collected!")
    else:
        print("\n❌ Ball NOT marked as collected!")
