from .Point import Point
from constants import *


class Agent:
    """A model of a cell agent."""
    _location: Point  # current location of the agent
    _direction: Point  # angle in which the agent is going

    _range: float  # range of the agent's view
    _view_angle: float

    _view_direction: Point  # angle in which the agent is facing
    _fire_time: int  # time until the agent can fire again

    _health: int = 100  # health of the agent

    _team: str
    _id: int

    def __init__(self, location: Point, direction: Point, view_range: float, view_direction: Point, view_angle: float,
                 team: str, id: int):
        """Construct an agent with position, velocity, radius, color, and id."""
        self._location = location
        self._direction = direction  # only 8 directions possible
        self._range = view_range
        self._view_angle = view_angle
        self._view_direction = view_direction
        self._health = 100
        self._team = team
        self._id = id
        self._fire_time = 0

    def __str__(self) -> str:
        """Return a string representation of the agent."""
        return f"Agent {self.id} at {self._location}  and direction {self._direction}"

    def __repr__(self) -> str:
        """Return a string representation of the agent."""
        return f"Agent {self.id} at {self._location} and direction {self._direction}"

    def get_location(self) -> Point:
        return self._location

    def get_direction(self) -> Point:
        return self._direction

    def set_direction(self, direction: Point) -> None:
        # TODO: round off to closest 8 directions
        self._direction = direction

    def stop(self) -> None:
        """Stop the agent."""
        self._direction = Point(0, 0)

    def get_range(self) -> float:
        return self._range

    def set_range(self, range: float) -> None:
        self._range = range

    def set_range(self, range: float) -> None:
        self._range = range

    def get_view_angle(self) -> float:
        return self._view_angle

    def get_view_direction(self) -> Point:
        return self._view_direction

    def set_view_direction(self, view_direction: Point) -> None:
        self._view_direction = view_direction

    def id(self) -> int:
        return self._id

    def get_team(self) -> str:
        return self._team

    def get_fire_time(self) -> int:
        return self._fire_time

    def get_health(self) -> int:
        return self._health

    def fire(self) -> bool:
        if self._fire_time == 0:
            self._fire_time = FIRE_COOLDOWN
            return True
        return False

    def tick(self) -> None:
        """Update the state of the agent by one time step."""
        self._location.add(self._direction)

        if self._fire_time > 0:
            self._fire_time -= 1
