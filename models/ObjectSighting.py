from .Point import Point
from constants import WALL, BULLET, OPPONENT


class ObjectSighting:
    object_type: str  # Opponent's Agent, Bullet, Wall
    location: Point
    direction: Point  # For Wall it's Point(0,0)

    def __init__(self, object_type: str, location: Point, direction: Point):
        self.object_type = object_type
        self.location = location
        if object_type == WALL:
            self.direction = Point(0, 0)
        else:
            self.direction = direction
