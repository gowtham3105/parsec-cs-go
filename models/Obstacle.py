from .Point import Point
from typing import List


class Obstacle:
    corners: List[Point]
    n: int  # No of Corners

    # Only Polygon Obstacles are allowed
    def __init__(self, corners: List[Point]):
        self.corners = corners
        self.n = len(corners)
