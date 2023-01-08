"""The ViewController drives the visualization of the simulation."""

from turtle import Turtle, Screen, done
from models.Environement import Environment
from constants import *
from typing import Any
from time import time_ns
from utils import get_color

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

    def tick(self) -> dict[str, str | list[int]]:
        """Update the environment state and redraw visualization."""
        start_time = time_ns() // NS_TO_MS
        self.environment.tick()
        self.pen.clear()
        for agent in self.environment.agents:
            self.pen.penup()
            self.pen.goto(agent.get_location().x, agent.get_location().y)
            self.pen.pendown()
            self.pen.color(get_color(agent.get_team()))
            self.pen.dot(CELL_RADIUS)
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
