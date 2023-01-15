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
import math

from player_red import tick as player_red_tick
from player_blue import tick as player_blue_tick


class Environment:
    """The state of the environment."""

    agents: Dict[str, Dict[str, Agent]]
    bullets: List[Bullet]
    scores = Dict[str, int]
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

        self.write_stats()

        self.time += 1
        return {}

    def validate_actions(self, actions, team) -> List[Action]:
        """Validate the actions of the agents."""
        #  TODO: implement this
        
        for action in actions:
            agentId = action.agent_id
            actionType = action.type
            actionDirection = action.direction
            agentObject = self.agents[team][str(agentId)]
            allowed = 0

            # check if action is on his agent only
            if agentId in self.agents[team].keys():

                allowed = 1
                # - check if the agent is alive/dead
                if agentObject.get_health() == 0:
                    self.alerts[team].append(Alert(len(self.alerts[team]), DEAD, agentId))
                    allowed = 0
                    # raise Exception("Agent is already dead!")

                # - check if the agent is able to fire or not
                elif actionType == FIRE and not agentObject.can_fire():
                    self.alerts[team].append(Alert(len(self.alerts[team]), FIRE_IMPOSSIBLE, agentId))
                    allowed = 0

                # - make the direction's magnitude 1
                agentObject.set_direction(agentObject.get_direction().make_unit_magnitude())

            else:
                self.alerts[team].append(Alert(len(self.alerts[team]), WRONG_AGENT, agentId))

            # Remove action if invalid and decrease the score based on that.
            if allowed == 0:
                self.scores[team] -= INVALID_ACTION
                actions.remove(action)

        return actions

    def perform_actions(self, actions, team) -> List[Alert]:
        """Perform the actions of the agents."""
        # TODO: implement this

        opponent = "red"
        if team == "red":
            opponent = "blue"
        for action in actions:
            agentId = action.agent_id
            actionType = action.type
            actionDirection = action.direction
            agentObject = self.agents[team][str(agentId)]
            opponentAgents = self.agents[opponent]

            # IF ACTION ---> FIRE
            if actionType == FIRE:
                 if agentObject.fire():
                    actionDirection.make_unit_magnitude()
                    self.bullets.append(Bullet(agentObject.get_location(), actionDirection, INITIAL_BULLET_ENERGY))

            # UPDATE DIRECTION
            if actionType == UPDATE_DIRECTION:
                agentObject.set_direction(actionDirection)

            # UPDATE VIEW DIRECTION
            if actionType == UPDATE_VIEW_DIRECTION:
                agentObject.set_view_direction(actionDirection)
            

        return self.alerts

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

        if agent.get_location().x + AGENT_RADIUS > MAX_X:
            agent.set_location(Point(MAX_X - AGENT_RADIUS, agent.get_location().y))
        if agent.get_location().x - AGENT_RADIUS < MIN_X:
            agent.set_location(Point(MIN_X + AGENT_RADIUS, agent.get_location().y))

        if agent.get_location().y + AGENT_RADIUS > MAX_Y:
            agent.set_location(Point(agent.get_location().x, MAX_Y - AGENT_RADIUS))
        if agent.get_location().y - AGENT_RADIUS < MIN_Y:
            agent.set_location(Point(agent.get_location().x, MIN_Y + AGENT_RADIUS))

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
