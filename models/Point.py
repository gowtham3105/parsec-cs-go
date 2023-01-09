class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

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