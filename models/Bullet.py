from .Point import Point


class Bullet:
    position: Point
    direction: Point
    energy: int
    _id: int
    STRING: str = "Bullet with id {id} at {position} with direction {direction} and energy {energy}"

    def __init__(self, position: Point, direction: Point, energy: int):
        self._position = position
        self._direction = direction
        self._energy = energy
        self._id = id(self)

    def tick(self) -> None:
        if self.energy > 0:
            self._position.add(self._direction)
        else:
            return
        self._energy -= 1

    def is_alive(self) -> bool:
        return self._energy > 0
