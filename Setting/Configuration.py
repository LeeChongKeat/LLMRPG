# Game constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60

# OLLAMA configuration - using qwen3:8b model
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3:8b"

# Color definitions 
SKY_BLUE = (135, 206, 235)        # Sky blue background
OCEAN_BLUE = (64, 164, 223)       # Ocean or water elements
SAND_COLOR = (237, 201, 175)      # Sand or light ground
GRASS_GREEN = (34, 139, 34)       # Grass
TREE_GREEN = (0, 100, 0)          # Tree canopies
BROWN = (139, 69, 19)             # Tree trunks, wood
PLAYER_BLUE = (30, 144, 255)      # Player character color
NPC_COLORS = [                     # NPC palette
    (255, 105, 180),  # Hot pink
    (255, 165, 0),    # Orange
    (147, 112, 219)   # Lavender
]
BLACK = (0, 0, 0)                   # Pure black
WHITE = (255, 255, 255)             # Pure white
RED = (255, 0, 0)                   # Bright red
GREEN = (0, 255, 0)                 # Bright green
YELLOW = (255, 255, 0)              # Bright yellow
BLUE = (0, 0, 255)                  # Bright blue
GRAY = (54, 54, 54)                 # Dark gray
DARK_GRAY = (50, 50, 50)            # Slightly darker gray
WALL_COLOR = (150, 100, 50)         # Warm brown walls
FLOOR_COLOR = (200, 180, 150)       # Light beige/tan floor
FURNITURE_COLOR = (100, 70, 30)     # Darker brown for furniture