"""
Configuration and constants for the 3D Racing Game
"""

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "3D Racing Game - Open World"
FPS = 60
TARGET_DELTA = 1.0 / FPS

# Graphics quality
MSAA_SAMPLES = 4        # Multi-sample anti-aliasing (0 to disable, 2/4/8 typical)
VSYNC = True            # Vertical sync to eliminate tearing

# World settings
CHUNK_SIZE = 500.0  # Size of each chunk
RENDER_DISTANCE = 3  # Number of chunks in each direction to render
MAP_SCALE = 1.0
TRACK_LENGTH = 12000.0  # Total length of the racing track (m)
TRACK_SEGMENT_LENGTH = 20.0  # Length of one road segment (m)

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
AMBIENT_LIGHT = 0.55
DIRECTIONAL_LIGHT = [1.0, 0.98, 0.92]
LIGHT_DIRECTION = [-0.3, 0.9, 0.4]
FOG_ENABLED = True
FOG_DENSITY = 0.00045        # GL_EXP2 fog density; lower = see further
SKY_COLOR = [0.55, 0.78, 0.98, 1.0]

# Road generation
ROAD_WIDTH = 50.0            # Width of a single lane stripe
LANE_OFFSETS = [-25.0, 0.0, 25.0]  # X positions for the 3 lane stripes
ROAD_HALF_SPAN = 50.0        # Distance from center to outer edge of the road
BARRIER_OFFSET = 52.0        # X position of left/right guardrails
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
