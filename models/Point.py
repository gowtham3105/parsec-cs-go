from utils import unformat


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float
    STRING: str = "Point({x}, {y})"

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def __init__(self, string: str):
        """Construct a point from a string."""
        string = unformat(string, Point.STRING)
        if "x" in string:
            self.x = string["x"]
        else:
            raise ValueError("Unable to Find x coordinate")
        if "y" in string:
            self.y = string["y"]
        else:
            raise ValueError("Unable to Find y coordinate")

    def add(self, other):
        """Add two Point objects together and return a new Point."""
        self.x += other.x
        self.y += other.y
        return True

    def distance(self, other) -> float:
        """Return the distance between two points."""
        x: float = self.x - other.x
        y: float = self.y - other.y
        return (x ** 2 + y ** 2) ** 0.5

    def make_unit_magnitude(self):
        """Return the unit vector of the point."""
        self.x = self.x / self.distance(Point(0, 0))
        self.y = self.y / self.distance(Point(0, 0))
        
    def __str__(self) -> str:
        """Return a string representation of the point."""
        return Point.STRING.format(self.x, self.y)

    def __repr__(self) -> str:
        """Return a string representation of the point."""
        return Point.STRING.format(self.x, self.y)
