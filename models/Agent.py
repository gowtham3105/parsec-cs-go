from .Point import Point
from constants import *

class Agent:
    """A model of a cell agent."""
    _location: Point
    _velocity: Point
    _direction: float
    _range: float
    _view_angle: float
    _team: str
    _id: int
    _fire_time: int

    def __init__(self, location: Point, velocity: Point, direction: float, view_range: float, view_angle: float,
                 team: str,
                 id: int):
        """Construct an agent with position, velocity, radius, color, and id."""
        self._location = location
        self._direction = direction
        self._velocity = velocity
        self._range = view_range
        self._view_angle = view_angle
        self._team = team
        self._id = id
        self._fire_time = 0

    def move(self) -> None:
        """Move the agent."""
        self.position = self.position.add(self.velocity)

    def __str__(self) -> str:
        """Return a string representation of the agent."""
        return f"Agent {self.id} at {self.position} with velocity {self.velocity} and direction {self.direction}"

    def __repr__(self) -> str:
        """Return a string representation of the agent."""
        return f"Agent {self.id} at {self.position} with velocity {self.velocity} and direction {self.direction}"

    def get_location(self) -> Point:
        return self._location

    def set_location(self, location: Point) -> None:
        self._location = location

    def get_velocity(self) -> Point:
        return self._velocity

    def set_velocity(self, velocity: Point) -> None:
        self._velocity = velocity

    def get_direction(self) -> float:
        return self._direction

    def set_direction(self, direction: float) -> None:
        self._direction = direction

    def stop(self) -> None:
        """Stop the agent."""
        self._velocity = self.get_location()

    def get_range(self) -> float:
        return self._range

    def set_range(self, range: float) -> None:
        self._range = range

    def get_view_angle(self) -> float:
        return self._view_angle

    def set_view_angle(self, view_angle: float) -> None:
        self._view_angle = view_angle

    def id(self) -> int:
        return self._id

    def get_team(self) -> str:
        return self._team

    def get_fire_time(self) -> int:
        return self._fire_time

    def fire(self) -> None:
        self._fire_time = FIRE_DELAY

