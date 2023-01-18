from .Point import Point


class Bullet:

    _position: Point
    _direction: Point  # Only 8 directions possible and 0,0 is allowed for stop
    _energy: int
    _id: int
    STRING: str = "Bullet with id {id} at {position} with direction {direction} and energy {energy}"

    def __init__(self, position: Point, direction: Point, energy: int):
        self._position = position
        self._direction = direction
        self._energy = energy
        self._id = id(self)

    def get_postion(self) -> Point:
        return self._position

    def get_direction(self) -> Point:
        return self._direction
    
    def get_energy(self) -> int:
        return self._energy

    def tick(self) -> None:
        if self._energy > 0:
            self._position.add(self._direction)
        else:
            return
        self._energy -= 1

    def is_alive(self) -> bool:
        return self._energy > 0
