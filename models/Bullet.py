from .Point import Point
from .Obstacle import Obstacle
from .Agent import Agent
from constants import DISTANCE_THRESHOLD


class Bullet:
    _location: Point
    _direction: Point
    _energy: int
    _id: int
    STRING: str = "Bullet with id {id} at {location} with direction {direction} and energy {energy}"

    def __init__(self, location: Point, direction: Point, energy: int):
        self._location = location
        self._direction = direction
        self._energy = energy
        self._id = id(self)

    def tick(self) -> None:
        if self._energy > 0:
            self._location.add(self._direction)
        else:
            return
        self._energy -= 1

    def is_alive(self) -> bool:
        return self._energy > 0

    def get_direction(self) -> Point:
        return self._direction

    def get_location(self) -> Point:
        return self._location

    def get_energy(self) -> int:
        return self._energy

    def is_colliding_with_agent(self, agent: Agent) -> bool:
        """Given a bullet and agent check if they are colliding"""
        # if the obstacle is agent see if they are within some distance of the bullet.
        #  then make the bullet collide with them and make them and bullet die.
        distance = agent.get_location().distance(self.get_location())
        if distance < DISTANCE_THRESHOLD:
            return True
        else:
            return False

    def is_colliding(self, obj: Obstacle | Agent) -> bool:
        """Given a bullet and obstacle check if they are colliding"""
        if isinstance(obj, Agent):
            return self.is_colliding_with_agent(obj)
        elif isinstance(obj, Obstacle):
            return self.is_colliding_with_obstacle(obj)
