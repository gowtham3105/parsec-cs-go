from .Point import Point


class Line:
    def __init__(self, p1: Point, p2: Point):
        self._p1 = p1
        self._p2 = p2

    def passes_through(self, point: Point) -> bool:
        # check if the point is on the line if the point is on the line, then the slope of the line formed by the
        # point and the two points of the line should be equal

        s1 = (self._p2.y - self._p1.y) / (self._p2.x - self._p1.x)
        s2 = (point.y - self._p1.y) / (point.x - self._p1.x)
        return s1 == s2

    def __str__(self):
        return "Line from {p1} to {p2}".format(p1=self._p1, p2=self._p2)

    def __repr__(self):
        return "Line from {p1} to {p2}".format(p1=self._p1, p2=self._p2)