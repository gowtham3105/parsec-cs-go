from .Agent import Agent
from typing import Dict, List
from .Alert import Alert
from .Obstacle import Obstacle


class State:
    agents: Dict[str, Agent]  # The player's agents
    object_in_sight: Dict[str, List]  # Agent : [ObjectSighting] ,Bullet: [ObjectSighting]  ,Wall: [ObjectSighting]
    Alerts: List[Alert]  # List of alerts collisions, zone, bullet_hit etc
    team: str
    time: int
    obstacles: List[Obstacle]  # List of obstacles in the environment

    def __init__(self):
        pass
