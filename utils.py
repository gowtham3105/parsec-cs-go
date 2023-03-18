import os

from shapely import LineString, Polygon
from typing import List
import math
from random import uniform
from constants import *
import re
from models.Point import Point
import numpy as np
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
    vector1 = np.array([polar.x - center.x, polar.y - center.y])
    vector2 = np.array([radial.x - center.x, radial.y - center.y])
    vector_mod = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    if vector_mod == 0:
        return 0

    cos_theta = np.dot(vector1, vector2) / vector_mod
    # Sanity check
    cos_theta = min(1, max(-1, cos_theta))
    return np.arccos(cos_theta)


def get_section_point(point1: Point, point2: Point, m: int, n: int):
    new_x = (m * point2.x + n * point1.x) / (m + n)
    new_y = (m * point2.y + n * point1.y) / (m + n)

    return Point(new_x, new_y)


def get_random_float(num1: float, num2: float) -> float:
    return round(uniform(num1, num2), 2)


def get_zone_color(zone: str) -> str:
    """Return a color based on the zone."""
    return ZONE_COLORS[zone]

def ping_url(url):
    import requests
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False


def validate_player_client_urls(clients: list[dict], health_check_route) -> list[dict]:
    valid_clients = []
    for client in clients:
        if ping_url(client['client_url'] + health_check_route):
            valid_clients.append(client)

    return valid_clients


def get_urls(teams: List[str]) -> list[dict]:
    clients = []
    HEALTH_CHECK_ROUTE = os.getenv("HEALTH_CHECK_ROUTE")
    if not HEALTH_CHECK_ROUTE:
        raise ValueError("HEALTH_CHECK_ROUTE not set")
    for team in teams:
        player_client_host_key = f"PLAYER_{team.upper()}_CLIENT_HOST"
        player_client_port_key = f"PLAYER_{team.upper()}_CLIENT_PORT"
        player_client_token = f"PLAYER_{team.upper()}_TOKEN"

        player_client_host = os.getenv(player_client_host_key)
        player_client_port = os.getenv(player_client_port_key)
        player_client_token = os.getenv(player_client_token)

        url = f"http://{player_client_host}:{player_client_port}"
        data = {
            "token": player_client_token,
            "client_url": url,
            "team": team
        }
        clients.append(data)

    validated_clients = validate_player_client_urls(clients, HEALTH_CHECK_ROUTE)
    return validated_clients
