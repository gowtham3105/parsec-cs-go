from .Point import Point
from .Line import Line
from typing import List
from .Line import Line


class Obstacle:
    corners: List[Point]
    n: int  # No of Corners
    STRING: str = "Obstacle with {n} corners at {corners}"

    # Only Polygon Obstacles are allowed
    def __init__(self, corners: List[Point]):
        self.corners = corners
        self.n = len(corners)
    
    def contains_point(self, point: Point) -> bool:
        """
        Returns True if the point is inside the obstacle
        """

        class line:
            def __init__(self, p1, p2):
                self.p1 = p1
                self.p2 = p2

        def onLine(l1, p):
            # Check whether p is on the line or not
            if (
                p.x <= max(l1.p1.x, l1.p2.x)
                and p.x <= min(l1.p1.x, l1.p2.x)
                and (p.y <= max(l1.p1.y, l1.p2.y) and p.y <= min(l1.p1.y, l1.p2.y))
            ):
                return True
            return False

        def direction(a, b, c):
            val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
            if val == 0:
                # Colinear
                return 0
            elif val < 0:
                # Anti-clockwise direction
                return 2
            # Clockwise direction
            return 1

        def isIntersect(l1, l2):
            # Four direction for two lines and points of other line
            dir1 = direction(l1.p1, l1.p2, l2.p1)
            dir2 = direction(l1.p1, l1.p2, l2.p2)
            dir3 = direction(l2.p1, l2.p2, l1.p1)
            dir4 = direction(l2.p1, l2.p2, l1.p2)

            # When intersecting
            if dir1 != dir2 and dir3 != dir4:
                return True

            # When p2 of line2 are on the line1
            if dir1 == 0 and onLine(l1, l2.p1):
                return True

            # When p1 of line2 are on the line1
            if dir2 == 0 and onLine(l1, l2.p2):
                return True

            # When p2 of line1 are on the line2
            if dir3 == 0 and onLine(l2, l1.p1):
                return True

            # When p1 of line1 are on the line2
            if dir4 == 0 and onLine(l2, l1.p2):
                return True

            return False

        # When polygon has less than 3 edge, it is not polygon
        if len(self.corners) < 3:
            return False

        # Create a point at infinity, y is same as point p
        exline = line(point, Point(9999, point.y))
        count = 0
        i = 0
        while True:
            # Forming a line from two consecutive points of poly
            side = line(self.corners[i], self.corners[(i + 1) % n])
            if isIntersect(side, exline):
                # If side is intersects ex
                if (direction(side.p1, point, side.p2) == 0):
                    return onLine(side, point)
                count += 1
            
            i = (i + 1) % len(self.corners)
            if i == 0:
                break

        # When count is odd
        return count & 1

    def __str__(self):
        return self.STRING.format(corners=self.corners)

    def __repr__(self):
        return self.STRING.format(corners=self.corners)
    
    def checkInside(self, p:Point):
            """
            Check whether the point is inside the Polygon.
            """
            # When polygon has less than 3 edge, it is not polygon
            if self.n < 3:
                return False

            # Create a point at infinity, y is same as point p
            exline = Line(p, Point(9999, p.y))
            count = 0
            i = 0
            while True:
                # Forming a line from two consecutive points of poly
                side = Line(self.corners[i], self.corners[(i + 1) % self.n])
                if exline.isIntersect(side, exline):
                    # If side is intersects ex
                    if (Line.direction(side.p1, p, side.p2) == 0):
                        return side.onLine(p)
                    count += 1
                
                i = (i + 1) % self.n
                if i == 0:
                    break

            # When count is odd
            return count & 1

    def get_edges(self) -> List[Line]:
        edges = []
        for i in range(self.n):
            edges.append(Line(self.corners[i], self.corners[(i + 1) % self.n]))
        return edges


