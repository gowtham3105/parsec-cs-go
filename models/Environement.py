from __future__ import annotations
from typing import List, Dict
import time
import math
from random import random, randint
from constants import *
from .Agent import Agent
from .Point import Point
from .Bullet import Bullet
from .Action import Action
from .Alert import Alert
from .Obstacle import Obstacle
from .ObjectSighting import ObjectSighting
from math import sin, cos, pi
from .State import State

from player_red import tick as player_red_tick
from player_blue import tick as player_blue_tick

from shapely import LineString, Polygon


class Environment:
    """The state of the environment."""

    agents: Dict[str, Dict[str, Agent]]
    bullets: List[Bullet]
    scores = Dict[str, int]
    obstacles: List[Obstacle]
    time: int = 0
    alerts: Dict[str, List[Alert]]
    _zone: List[Point]
    _safe_zone: List[Point]
    _is_zone_shrinking: bool = False
    _zone_shrink_times: List[int]

    def __init__(self):
        """Initialize the cells with random locations and directions."""
        self.agents = {
            "red": {
                "0": Agent(self.random_location(), self.random_direction(), 10, Point(1, 0), pi, "red", 0),
            }
        }
        self.bullets = []
        self.alerts = {
            "red": [],
            "blue": []
        }
        self._log = open("log.txt", "w")

    def tick(self) -> dict[int | str, int]:
        """Update the state of the simulation by one time step."""

        for team in self.agents:
            for agent in self.agents[team].values():
                agent.tick()
                self.enforce_bounds(agent)
                self.enforce_collisions(agent)
                self.enforce_zone(agent)

        for bullet in self.bullets:
            self.enforce_bullet_collisions(bullet)
            bullet.tick()
            if not bullet.is_alive():
                self.bullets.remove(bullet)

        red_state = self.generate_state('red')
        blue_state = self.generate_state('blue')

        red_actions = player_red_tick(red_state)
        blue_actions = player_blue_tick(blue_state)

        validated_red_actions = self.validate_actions(red_actions, "red")
        validated_blue_actions = self.validate_actions(blue_actions, "blue")

        self.alerts['red'] = self.perform_actions(validated_red_actions, "red")
        self.alerts['blue'] = self.perform_actions(validated_blue_actions, "blue")

        self.write_stats(red_state, blue_state, red_actions, blue_actions, validated_red_actions,
                         validated_blue_actions)

        self.time += 1
        return {}

    def validate_actions(self, actions, team) -> List[Action]:
        """Validate the actions of the agents."""
        #  TODO: implement this
        # - check if the agent is alive/dead
        # - check if the agent is able to fire or not
        # - make the direction's magnitude 1
        # -
        # decrease the score based on that.

        return []

    def perform_actions(self, actions, team) -> List[Alert]:
        """Perform the actions of the agents."""
        # TODO: implement this

        return []

    def write_stats(self, red_state: State, blue_state: State, red_actions: List[Action], blue_actions: List[Action],
                    validated_red_actions: List[Action], validated_blue_actions: List[Action]) -> None:
        """Write the stats of the simulation to a file."""
        self._log.write(f"Game time: {self.time} Real Time: {time.time()}\n")
        self._log.write(f"STARTING GAME LOG FOR TIME {self.time}\n")
        self._log.write(f"Red Agents: {len(self.agents['red'])} Red Score: {self.scores['red']} "
                        f"|| Blue Agents: {len(self.agents['blue'])} Blue Score: {self.scores['blue']}\n")
        # log map elements
        self._log.write("STARTING LOG OF MAP ELEMENTS\n")

        self._log.write("LOGGING AGENTS\n")
        for team in self.agents:
            for agent in self.agents[team].values():
                self._log.write(f"{agent}\n")

        self._log.write("LOGGING BULLETS\n")
        for bullet in self.bullets:
            self._log.write(f"{bullet}\n")

        self._log.write("ENDING LOG OF MAP ELEMENTS\n")

        self._log.write("STARTING LOG OF STATES\n")

        self._log.write("LOGGING RED STATE\n")
        self._log.write(f"{red_state}\n")

        self._log.write("LOGGING BLUE STATE\n")
        self._log.write(f"{blue_state}\n")

        self._log.write("ENDING LOG OF STATES\n")

        self._log.write("STARTING LOG OF ACTIONS\n")

        self._log.write("LOGGING RED ACTIONS\n")
        for action in red_actions:
            self._log.write(f"  {action}\n")

        self._log.write("LOGGING BLUE ACTIONS\n")
        for action in blue_actions:
            self._log.write(f"  {action}\n")

        self._log.write("ENDING LOG OF ACTIONS\n")

        self._log.write("STARTING LOG OF VALIDATED ACTIONS\n")

        self._log.write("LOGGING RED VALIDATED ACTIONS\n")
        for action in validated_red_actions:
            self._log.write(f"  {action}\n")

        self._log.write("LOGGING BLUE VALIDATED ACTIONS\n")
        for action in validated_blue_actions:
            self._log.write(f"  {action}\n")

        self._log.write("ENDING LOG OF VALIDATED ACTIONS\n")

        self._log.write("STARTING LOG OF ALERTS\n")

        self._log.write("LOGGING RED ALERTS\n")
        for alert in self.alerts['red']:
            self._log.write(f"{alert}\n")

        self._log.write("LOGGING BLUE ALERTS\n")
        for alert in self.alerts['blue']:
            self._log.write(f"{alert}\n")

        self._log.write("ENDING LOG OF ALERTS\n")

        self._log.write(f"ENDING GAME LOG FOR TIME {self.time}\n")

    def generate_state(self, team) -> State:
        """Generate the state of the environment."""
        
        _agents = self.agents[team]
        object_in_sight = {}
        
        for agent in _agents:
            object_in_sight[agent] = self.get_object_in_sight(_agents[agent])

        return State(_agents, object_in_sight, self.alerts, team, self.time, self.obstacles, self._zone,self._safe_zone,self._is_zone_shrinking)

    

    def get_object_in_sight(self, agent:Agent) -> List[ObjectSighting]:

        object_in_sight = []
        non_blocked_object_in_sight = []

        #opponent's agents
        for team in self.agents:
            if(team != agent.get_team()):
                for opponent_agent in self.agents[team].values():
                    if(self.is_point_in_vision(agent,opponent_agent.get_location(),opponent_agent.get_radius())):
                        object_in_sight.append(ObjectSighting("Opponent's Agent",opponent_agent.get_location(),opponent_agent.get_direction()))


        #bullets
        for bullet in self.bullets:
            if(self.is_point_in_vision(agent,bullet.position,0)):
                object_in_sight.append(ObjectSighting("bullet",bullet.position,bullet.direction))

        
        # checking if the line of sight passes through a wall
        for object in object_in_sight:
            for obstacle in self.obstacles:
                if(self.isBetweenLineOfSight(agent.get_location(), object.location, obstacle.corners)):
                    break
            non_blocked_object_in_sight.append(object)
        
        return non_blocked_object_in_sight

    def isBetweenLineOfSight(self, point1 : Point, point2 : Point, corners : List[Point]):

        line = LineString([(point1.x, point1.y), (point2.x, point2.y)])
        polygon = Polygon([(i.x, i.y) for i in corners])
        return line.intersection(polygon)

    def is_point_in_vision(self, agent:Agent, polar_point:Point, opponent_agent_radius: int) -> bool:
        center = agent.get_location()

        if(center.distance(polar_point) > agent.get_range() + opponent_agent_radius):
            return False
        
        radial_point = agent.get_location()
        radial_point.add(agent.get_view_direction())

        if(self.angle(center, polar_point, radial_point) <= agent._view_angle()/2):
            return True
        
        return False

    def angle(self, center:Point, polar:Point, radial :Point):
        vector1 = Point(polar.x - center.x, polar.y-center.y)
        vector2 = Point(radial.x-center.x, radial.y - center.y)
        dot_product = (vector1.x*vector2.x) + (vector1.y*vector2.y)
        vector_mod = ((vector1.x**2 + vector1.y**2)**0.5)*((vector2.x**2 + vector2.y**2)**0.5)

        if(vector_mod == 0):
            return 0

        angle = dot_product/vector_mod
        return math.acos(angle)


    def random_location(self) -> Point:
        # TODO: make this more random
        return Point(0, 0)

    def random_direction(self) -> Point:
        """Generate a 'point' used as a directional vector."""
        angle = random() * 2.0 * pi
        x = cos(angle)
        y = sin(angle)
        return Point(x, y)

    def enforce_bounds(self, agent: Agent) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""

        if agent.get_location().x > MAX_X:
            agent.get_location().x = MAX_X
        if agent.get_location().x < MIN_X:
            agent.get_location().x = MIN_X

        if agent.get_location().y > MAX_Y:
            agent.get_location().y = MAX_Y
        if agent.get_location().y < MIN_Y:
            agent.get_location().y = MIN_Y

    def enforce_collisions(self, agent: Agent) -> None:
        """Cause an agent to stop if it collides with another agent."""
        # TODO: implement this
        # - check if the agent is alive/dead
        # - check if it collided with a wall, agent  or bullet
        # - if bullet decrease health
        # - else stop the agent.
        #

        agent.stop()

    def enforce_bullet_collisions(self, bullet: Bullet) -> None:
        """Cause a bullet to stop if it collides with another agent or obstacle."""
        # TODO: implement this
        pass

    def enforce_zone(self, agent):
        # TODO: implement this
        pass

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        # TODO: implement this
        if self.time > MAX_TIME:
            return True
        return False
