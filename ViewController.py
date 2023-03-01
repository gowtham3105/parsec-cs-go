"""The ViewController drives the visualization of the simulation."""

from turtle import Turtle, Screen, done, register_shape
from models.Environement import Environment
from models.Point import Point
from typing import List
from constants import *
from typing import Any
from time import time_ns
from utils import get_color, get_zone_color

NS_TO_MS: int = 1000000


class ViewController:
    """This class is responsible for controlling the simulation and visualizing it."""
    screen: Any
    pen: Turtle
    environment: Environment

    def __init__(self, environment: Environment):
        """Initialize the VC."""
        self.environment = environment
        self.screen = Screen()
        self.screen.bgcolor("black")
        self.screen.setup(VIEW_WIDTH, VIEW_HEIGHT)
        self.screen.tracer(0, 0)
        self.screen.delay(0)
        self.screen.title("Cluster Funk v2")
        self.pen = Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)

    def start_simulation(self):
        """Call the first tick of the simulation and begin turtle gfx."""
        self.tick()
        done()

    def draw_zone(self, zone: List[Point], zone_color: str):
        zone_length = zone[0].distance(zone[3])
        zone_breadth = zone[0].distance(zone[1])
        self.pen.penup()
        self.pen.goto(zone[3].x, zone[3].y)
        self.pen.pendown()
        self.pen.color(zone_color)

        # Drawing a rectangle for zone
        for _ in range(4):
            self.pen.forward(zone_length if _ % 2 == 0 else zone_breadth)
            self.pen.right(90)

    def tick(self) -> dict[str, str | list[int]]:
        """Update the environment state and redraw visualization."""
        start_time = time_ns() // NS_TO_MS
        self.environment.tick()
        self.pen.clear()

        self.draw_zone(self.environment.get_current_zone(), get_zone_color(ZONE))
        self.draw_zone(self.environment.get_current_safe_zone(), get_zone_color(SAFE_ZONE))

        for team in self.environment.agents:
            for agent_id, agent in self.environment.agents[team].items():
                self.pen.penup()
                self.pen.goto(agent.get_location().x, agent.get_location().y)
                self.pen.pendown()
                self.pen.color(get_color(agent.get_team()))
                self.pen.dot(AGENT_RADIUS * 2)
        self.screen.update()

        if self.environment.is_complete():
            self.screen.bye()
            return
        else:
            end_time = time_ns() // NS_TO_MS
            next_tick = 30 - (end_time - start_time)
            if next_tick < 0:
                next_tick = 0
            self.screen.ontimer(self.tick, next_tick)
