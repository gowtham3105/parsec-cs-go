from __future__ import annotations
from typing import List, Dict
from random import random, randint
from constants import *
from .Agent import Agent
from .Point import Point
from .Bullet import Bullet
from .Action import Action
from .Alert import Alert
from math import sin, cos, pi
from .State import State

from player_red import tick as player_red_tick
from player_blue import tick as player_blue_tick


class Environment:
    """The state of the environment."""

    agents: Dict[str, Dict[str, Agent]]
    bullets: List[Bullet]
    scores = Dict[str, int]
    time: int = 0
    alerts: Dict[str, List[Alert]]

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

    def tick(self) -> dict[int | str, int]:
        """Update the state of the simulation by one time step."""

        for team in self.agents:
            for agent in self.agents[team].values():
                agent.tick()
                self.enforce_bounds(agent)
                self.enforce_collisions(agent)
                self.enforce_zone(agent)

        red_state = self.generate_state('red')
        blue_state = self.generate_state('blue')

        red_actions = player_red_tick(red_state)
        blue_actions = player_blue_tick(blue_state)

        validated_red_actions = self.validate_actions(red_actions, "red")
        validated_blue_actions = self.validate_actions(blue_actions, "blue")

        self.alerts['red'] = self.perform_actions(validated_red_actions, "red")
        self.alerts['blue'] = self.perform_actions(validated_blue_actions, "blue")

        self.write_stats()

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

    def write_stats(self) -> None:
        pass

    def generate_state(self, team) -> State:
        """Generate the state of the environment."""
        # TODO: implement this

        return State()

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

        agent.stop()

    def enforce_zone(self, agent):

        pass

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        # TODO: implement this
        return False
