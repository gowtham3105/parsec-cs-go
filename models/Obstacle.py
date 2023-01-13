from .Point import Point
from .Line import Line
from typing import List


class Obstacle:
    corners: List[Point]
    n: int  # No of Corners
    STRING: str = "Obstacle with {n} corners at {corners}"

    # Only Polygon Obstacles are allowed
    def __init__(self, corners: List[Point]):
        self.corners = corners
        self.n = len(corners)

    def get_edges(self) -> List[Line]:
        edges = []
        for i in range(self.n):
            edges.append(Line(self.corners[i], self.corners[(i + 1) % self.n]))
        return edges

    def __str__(self):
        return self.STRING.format(corners=self.corners)

    def __repr__(self):
        return self.STRING.format(corners=self.corners)

