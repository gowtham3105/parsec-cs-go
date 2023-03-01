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
OUTSIDE_ZONE: str = 'outside_zone'

UPDATE_DIRECTION: str = "UPDATE_DIRECTION"
UPDATE_VIEW_DIRECTION: str = "UPDATE_VIEW_DIRECTION"
FIRE: str = "FIRE"

MAX_TIME: int = 5000
INVALID_ACTION: int = 20
INITIAL_BULLET_ENERGY = 50

COLLISION: str = 'collision'
ZONE: str = 'zone'
SAFE_ZONE: str = 'safe_zone'
DEAD: str = 'agent_dead'
FIRE_IMPOSSIBLE: str = 'cannot_fire'
WRONG_AGENT: str = 'opponent_agent'

AGENT_RADIUS: int = 5

TICKS: Dict[str, int] = {  # Ticks per second
    "Bullet": 5,
    "Agent": 1,
}

# multiple all Ticks here always
UNIT_TIME: int = TICKS['Bullet'] * TICKS['Agent']  # Time in which all objects move at least once
DAMAGES: Dict[str, int] = {
    BULLET_HIT: 10,
    OUTSIDE_ZONE: 1
}

ZONE_COLORS: dict = {
    "zone": "#ffffff",
    "safe_zone": "#ff0000"
}

SHRINK_VALUE: int = 10
