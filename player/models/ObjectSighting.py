from .Point import Point
from constants import WALL, BULLET, OPPONENT


class ObjectSighting:
    object_type: str  # Opponent's Agent, Bullet
    location: Point
    direction: Point  # For Wall it's Point(0,0)
    _id: int
    STRING: str = "ObjectSighting with id {id} of type {object_type} at {location} with direction {direction}"

    def __init__(self, object_type: str, location: Point, direction: Point):
        self.object_type = object_type
        self.location = location
        if object_type == WALL:
            self.direction = Point(0, 0)
        else:
            self.direction = direction

        self._id = id(self)

    def __str__(self):
        return ObjectSighting.STRING.format(object_type=self.object_type, location=self.location,
                                            direction=self.direction, id=self._id)

    def __repr__(self):
        return ObjectSighting.STRING.format(object_type=self.object_type, location=self.location,
                                            direction=self.direction, id=self._id)

    def set_id(self, id):
        self._id = id

    @staticmethod
    def generate_object(data: dict):
        params = {
            "object_type": data['object_type'],
            "location": Point(data['location']['x'], data['location']['y']),
            "direction": Point(data['direction']['x'], data['direction']['y'])
        }
        object_sighting = ObjectSighting(**params)
        object_sighting.set_id(data['id'])

        return object_sighting
