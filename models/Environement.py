from __future__ import annotations
from typing import List, Dict
from random import random, randint
from constants import *
from .Agent import Agent
from .Point import Point
from math import sin, cos, pi


class Environment:
    """The state of the environment."""

    agents: List[Agent]

    time: int = 0

    def __init__(self):
        """Initialize the cells with random locations and directions."""
        self.agents = []

    def tick(self) -> dict[int | str, int]:
        """Update the state of the simulation by one time step."""
        self.time += 1
        return {}

    def random_location(self) -> Point:
        # TODO: make this more random
        return Point(0, 0)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        angle = random() * 2.0 * pi
        x = speed * cos(angle)
        y = speed * sin(angle)
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

        agent.stop()

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        # TODO: implement this
        return False
