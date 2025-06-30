# Board dimensions
DIMENSION = 8  # 8x8 chess board
SQ_SIZE = 64   # Size of each square in pixels
BOARD_WIDTH = BOARD_HEIGHT = DIMENSION * SQ_SIZE
MOVE_LOG_PANEL_WIDTH = 256
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
EVAL_BAR_WIDTH = 32
EVAL_BAR_HEIGHT = BOARD_HEIGHT
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION

# Game settings
MAX_FPS = 15  # For animations
SCROLL_STEP = 4
SCROLL_SPEED = 20

# Resource directories
IMAGES_DIR = "img"
SOUNDS_DIR = "sounds"

# Colors
LIGHT_SQUARE_COLOR = "light gray"
DARK_SQUARE_COLOR = (153, 102, 51)
HIGHLIGHT_COLOR = "blue"
MOVE_HIGHLIGHT_COLOR = "yellow"

# AI constants
CHECKMATE_SCORE = 1000000
DRAW_SCORE = 0
DEFAULT_DEPTH = 3

# Piece values for AI evaluation
PIECE_VALUES = {
    'P': 100,
    'N': 320,
    'B': 330,
    'R': 500,
    'Q': 900,
    'K': 20000
}

# Dictionary to store piece images
IMAGES = {} 