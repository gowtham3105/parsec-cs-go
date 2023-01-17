"""Constants used through the simulation."""

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

UPDATE_DIRECTION: str = "UPDATE_DIRECTION"
UPDATE_VIEW_DIRECTION: str = "UPDATE_VIEW_DIRECTION"
FIRE: str = "FIRE"

MAX_TIME: int = 5000
INVALID_ACTION: int = 20
INITIAL_BULLET_ENERGY = 50

COLLISION: str = 'collision'
ZONE: str = 'zone'
BULLET_HIT: str = 'bullet_hit'
DEAD: str = 'agent_dead'
FIRE_IMPOSSIBLE: str = 'cannot_fire'
WRONG_AGENT: str = 'opponent_agent'
