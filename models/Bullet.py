from Point import Point


class Bullet:
    position: Point
    direction: Point
    velocity: int
    energy: int

    def __init__(self, position: Point, direction: Point, velocity: int, energy: int):
        self._position = position
        self._direction = direction
        self._velocity = velocity
        self._energy = energy
