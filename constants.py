"""Constants used through the simulation."""
from typing import Dict

BOUNDS_WIDTH: int = 400
MAX_X: float = BOUNDS_WIDTH / 2
MIN_X: float = -MAX_X
VIEW_WIDTH: int = BOUNDS_WIDTH + 20

BOUNDS_HEIGHT: int = 400
MAX_Y: float = BOUNDS_HEIGHT / 2
MIN_Y: float = -MAX_Y
VIEW_HEIGHT: int = BOUNDS_HEIGHT + 20

DISTANCE_THRESHOLD: float = 1

CELL_RADIUS: int = 15

FIRE_COOLDOWN: int = 1

TEAM_COLORS: dict = {
    "red": "#ff0000",
    "blue": "#0000ff"
}

OPPONENT: str = 'opponent'
WALL: str = 'wall'
BULLET: str = 'bullet'
BULLET_HIT: str = 'bullet_hit'

UPDATE_DIRECTION: str = "UPDATE_DIRECTION"
UPDATE_VIEW_DIRECTION: str = "UPDATE_VIEW_DIRECTION"
FIRE: str = "FIRE"

MAX_TIME: int = 5000

TICKS: Dict[str, int] = {  # Ticks per second
    "Bullet": 5,
    "Agent": 1,
}

# multiple all Ticks here always
UNIT_TIME: float = 1 / (TICKS['Bullet'] * TICKS['Agent'])  # Time in which all objects move at least
# once
DAMAGES: Dict[str, int] = {
    BULLET_HIT: 10
}
