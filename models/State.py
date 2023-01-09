from .Agent import Agent
from typing import Dict, List
from .Alert import Alert
from .Obstacle import Obstacle
from .Point import Point


class State:
    agents: Dict[str, Agent]  # The player's agents
    object_in_sight: Dict[str, List]  # Agent : [ObjectSighting] ,Bullet: [ObjectSighting]  ,Wall: [ObjectSighting]
    Alerts: List[Alert]  # List of alerts collisions, zone, bullet_hit etc
    team: str
    time: int
    obstacles: List[Obstacle]  # List of obstacles in the environment
    zone: List[Point]  # List of corners in the zone
    safe_zone: List[Point]  # List of corners in the safe zone
    is_zone_shrinking: bool  # True if zone is shrinking, False if zone is expanding

    def __init__(self, agents: Dict[str, Agent], object_in_sight: Dict[str, List], alerts: List[Alert], team: str, time: int, obstacles: List[Obstacle], zone: List[Point], safe_zone: List[Point], is_zone_shrinking: bool):
        self.agents = agents
        self.object_in_sight = object_in_sight
        self.alerts = alerts
        self.team = team
        self.time = time
        self.obstacles = obstacles
        self.zone = zone
        self.safe_zone = safe_zone
        self.is_zone_shrinking = is_zone_shrinking



