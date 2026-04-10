#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from game import World, Car

# Create world and car
w = World()
c = Car('sports')

# Count balls before collection
green_before = sum(1 for o in w.environment_objects if o.type == 'green_ball' and not getattr(o, 'collected', False))
red_before = sum(1 for o in w.environment_objects if o.type == 'red_ball' and not getattr(o, 'collected', False))

print(f"Before collection:")
print(f"  Green balls: {green_before}")
print(f"  Red balls: {red_before}")

# Simulate collecting a green ball and a red ball
green_balls = [o for o in w.environment_objects if o.type == 'green_ball']
red_balls = [o for o in w.environment_objects if o.type == 'red_ball']

if green_balls:
    green_ball = green_balls[0]
    c.position = green_ball.position.copy()
    c.check_booster_collision(w.environment_objects)

if red_balls:
    red_ball = red_balls[0]
    c.position = red_ball.position.copy()
    c.check_booster_collision(w.environment_objects)

# Count balls after collection (excluding collected ones)
green_after = sum(1 for o in w.environment_objects if o.type == 'green_ball' and not getattr(o, 'collected', False))
red_after = sum(1 for o in w.environment_objects if o.type == 'red_ball' and not getattr(o, 'collected', False))

print(f"\nAfter collection:")
print(f"  Green balls: {green_after}")
print(f"  Red balls: {red_after}")

print(f"\nCollected:")
green_collected = sum(1 for o in w.environment_objects if o.type == 'green_ball' and getattr(o, 'collected', False))
red_collected = sum(1 for o in w.environment_objects if o.type == 'red_ball' and getattr(o, 'collected', False))
print(f"  Green balls: {green_collected}")
print(f"  Red balls: {red_collected}")

if green_after == green_before - 1 and red_after == red_before - 1:
    print("\n✅ Balls are being marked as collected correctly!")
    print("✅ When rendered, they will be skipped because collected=True")
else:
    print("\n❌ Issue with ball collection tracking")
