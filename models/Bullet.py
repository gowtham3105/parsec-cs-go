from .Point import Point


class Bullet:
    position: Point
    direction: Point
    # velocity: int
    energy: int

    def __init__(self, position: Point, direction: Point, velocity: int, energy: int):
        self._position = position
        self._direction = direction
        # self._velocity = velocity
        self._energy = energy

    def tick(self) -> None:
        if self.energy > 0:
            self._position.add(self._direction)
        else:
            return
        self._energy -= 1

    def is_alive(self) -> bool:
        return self._energy > 0
