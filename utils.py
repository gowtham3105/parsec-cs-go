from shapely import LineString, Polygon
from typing import List
import math
from constants import *
import re
from models.Point import Point
from models.Agent import Agent


def get_color(team: str) -> str:
    """Return a color based on the team."""
    return TEAM_COLORS[team]


def unformat(string, pattern):
    regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', pattern)
    values = list(re.search(regex, string).groups())
    keys = re.findall(r'{(.+?)}', pattern)
    _dict = dict(zip(keys, values))
    return _dict


def isBetweenLineOfSight(point1: Point, point2: Point, corners: List[Point]):
    line = LineString([(point1.x, point1.y), (point2.x, point2.y)])
    polygon = Polygon([(i.x, i.y) for i in corners])
    return line.intersection(polygon)


def is_point_in_vision(agent: Agent, polar_point: Point, opponent_agent_radius: int) -> bool:
    center = agent.get_location()

    if center.distance(polar_point) > agent.get_range() + opponent_agent_radius:
        return False

    radial_point = Point(center.x, center.y)
    radial_point.add(agent.get_view_direction())

    if find_angle(center, polar_point, radial_point) <= (agent.get_view_angle() / 2):
        return True

    return False


def find_angle(center: Point, polar: Point, radial: Point) -> float:
    vector1 = Point(polar.x - center.x, polar.y - center.y)
    vector2 = Point(radial.x - center.x, radial.y - center.y)
    dot_product = (vector1.x * vector2.x) + (vector1.y * vector2.y)
    vector_mod = ((vector1.x ** 2 + vector1.y ** 2) ** 0.5) * ((vector2.x ** 2 + vector2.y ** 2) ** 0.5)
    if vector_mod == 0:
        return 0

    angle = dot_product / vector_mod
    return math.acos(angle)
