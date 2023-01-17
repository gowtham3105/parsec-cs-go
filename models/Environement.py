from __future__ import annotations
from typing import List, Dict
import time
from random import random, randint
from constants import *
from .Agent import Agent
from .Point import Point
from .Line import Line
from .Bullet import Bullet
from .Action import Action
from .Alert import Alert
from math import sin, cos, pi, sqrt
from .State import State
import math
from .Obstacle import Obstacle

from player_red import tick as player_red_tick
from player_blue import tick as player_blue_tick


class Environment:
    """The state of the environment."""

    agents: Dict[str, Dict[str, Agent]]
    bullets: List[Bullet]
    scores = Dict[str, int]
    time: int = 0
    alerts: Dict[str, List[Alert]]
    obstacles: List[Obstacle]
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
        #  TODO: take a look at this
        if self.time % (UNIT_TIME / TICKS['Bullet']) == 0:
            for bullet in self.bullets:
                self.enforce_bullet_collisions(bullet)
                bullet.tick()
                if not bullet.is_alive():
                    self.bullets.remove(bullet)

        if self.time % (UNIT_TIME / TICKS['Agent']) == 0:
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

            self.write_stats(red_state, blue_state, red_actions, blue_actions, validated_red_actions,
                             validated_blue_actions)

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
        # - check if it collided with a wall, agent
        # - else stop the agent.
        #
        
        # Checking whether the agent is alive or not
        agent_alive = agent.get_health() > 0
        if not agent_alive: 
            agent.stop()
            return
        
        # Checking agent-wall collision
        for obstacle in self.obstacles:
            if obstacle.contains_point(agent.get_location()):
                agent.stop()
                break
        
        # Checking agent-agent collision
        for team in self.agents:
            for other_agent in self.agents[team].values():
                if agent != other_agent:
                    agent_collision = agent.get_location().distance(other_agent.get_location()) <= 2 * AGENT_RADIUS
                    if agent_collision: agent.stop()
                    break
        
        return
        
        agent.stop()

    def is_bullet_colliding(self, bullet: Bullet, obstacle: Obstacle|Agent) -> bool:
        """Given a bullet and obstacle check if they are colliding"""
        if(type(obstacle)== Obstacle):
            # if obstacle is polygon, the ray going in y direction intersects the side only odd times.
            return obstacle.checkInside(bullet._position)
        if(type(obstacle)== Agent):
            # if the obstacle is agent see if they are within some distance of the bullet.
            #  then make the bullet collide with them and make them and bullet die.
            distance = sqrt( (obstacle._location.y- bullet._position.x)**2 + (obstacle._location- bullet._position.y)**2 )
            if(distance<DISTANCE_THRESHOLD):
                return True
            else:
                return False



    def enforce_bullet_collisions(self, bullet: Bullet) -> None:
        """Cause a bullet to stop if it collides with another agent or obstacle."""
        # check collision with walls
        for obstacle in self.obstacles:
            if(self.is_bullet_colliding(bullet, obstacle)):
                bullet.is_alive = False
        
        for team in self.agents:
            for agent in self.agents[team].values():
                if bullet.is_colliding(agent):
                    bullet.is_alive = False
                    agent.decrease_health(BULLET_HIT)
                

    def decrease_agent_health(self, bullet:Bullet, agent):
        """Decrease the heath of agent depending on the energy of bullet"""
        # TODO: find an appropriate formula for health deduction.
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
