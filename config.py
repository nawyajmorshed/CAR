"""
Configuration and constants for the 3D Racing Game
"""

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "3D Racing Game - Open World"
FPS = 60
TARGET_DELTA = 1.0 / FPS

# World settings
CHUNK_SIZE = 500.0  # Size of each chunk
RENDER_DISTANCE = 3  # Number of chunks in each direction to render
MAP_SCALE = 1.0

# Physics
GRAVITY = 0.0
DRAG_COEFFICIENT = 0.001  # Very low drag for high speeds
ROAD_FRICTION = 1.0  # No friction on road
DIRT_FRICTION = 0.70
GRASS_FRICTION = 0.50

# Car physics
MAX_SPEED = 500.0  # Increased to allow higher W speeds
ACCELERATION = 2500.0  # Smoother acceleration for gradual speed buildup
BRAKE_DECELERATION = 120.0  # Smooth braking
STEERING_SPEED = 360.0  # Smooth steering response for gradual turns
STEERING_INPUT_SENSITIVITY = 1.1  # Multiplier for steering responsiveness
DRIFT_THRESHOLD = 80.0
DRIFT_MULTIPLIER = 1.2
INPUT_RESPONSE_TIME = 0.02  # Quick input response in seconds

# Nitro system
MAX_NITRO = 100.0
NITRO_CONSUMPTION_RATE = 30.0
NITRO_RECHARGE_RATE = 20.0
NITRO_BOOST_MULTIPLIER = 1.5
NITRO_FOV_BOOST = 15.0

# Camera settings
CAMERA_FOLLOW_HEIGHT = 3.0
CAMERA_FOLLOW_DISTANCE = 12.0
CAMERA_FOLLOW_SPEED = 0.4
CAMERA_MAX_DISTANCE = 30.0
CAMERA_MIN_DISTANCE = 8.0
CAMERA_SHAKE_AMOUNT = 0.01

# Lighting
AMBIENT_LIGHT = 0.4
DIRECTIONAL_LIGHT = [0.8, 0.9, 1.0]
LIGHT_DIRECTION = [-0.2, 0.8, 0.3]
FOG_density = 0.001
SKY_COLOR = [0.53, 0.76, 0.98, 1.0]

# Road generation
ROAD_WIDTH = 24.0
ROAD_HEIGHT_VARIATION = 15.0
NUM_ROAD_SEGMENTS = 50
CURVE_FREQUENCY = 0.1
ELEVATION_FREQUENCY = 0.05

# Environment
NUM_BUILDINGS_PER_CHUNK = 5
NUM_TREES_PER_CHUNK = 10
NUM_STREET_LIGHTS_PER_CHUNK = 3

# Debug
DEBUG_MODE = False
SHOW_WIREFRAME = False
