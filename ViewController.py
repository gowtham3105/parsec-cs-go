"""The ViewController drives the visualization of the simulation."""

from turtle import Turtle, Screen, done, register_shape
from models.Environement import Environment
from constants import *
from typing import Any
from time import time_ns
from utils import get_color
from PIL import Image



NS_TO_MS: int = 1000000

AGENT_IMAGE = 'gifs/among_us_cropped.gif'
CUR_AGENT_IMAGE = AGENT_IMAGE.split('.')[0]+"edited.gif"
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

        im = Image.open(AGENT_IMAGE)
        size = (AGENT_RADIUS*2, AGENT_RADIUS*2)
        im.thumbnail(size)
        im.save(CUR_AGENT_IMAGE)
        self.screen.register_shape(CUR_AGENT_IMAGE )
        self.turtle = Turtle(shape=CUR_AGENT_IMAGE)
        self.turtle.hideturtle()

    def start_simulation(self):
        """Call the first tick of the simulation and begin turtle gfx."""
        self.tick()
        done()

    def tick(self) -> dict[str, str or list[int]]:
        """Update the environment state and redraw visualization."""
        start_time = time_ns() // NS_TO_MS
        self.environment.tick()
        self.pen.clear()
        self.turtle.clear()
        print()
        team_side = {"red": MIN_X, "blue": MAX_X- MAX_X/4-4}
        for team in self.environment.agents:
            for agent_id, agent in self.environment.agents[team].items():
                self.pen.penup()
                self.pen.goto(team_side[team], MAX_Y-4-4*int(agent_id))
                self.pen.pendown()
                self.pen.color(get_color(agent.get_team()))
                self.pen.write(f"{agent_id}: {str(agent.get_health())}")
                self.pen.penup()
                self.pen.goto(agent.get_location().x, agent.get_location().y)
                self.pen.pendown()
                self.pen.dot(AGENT_RADIUS * 2) ## comment this line and uncomment the next lines to see
                                                # images instead of lines
                self.turtle.goto(agent.get_location().x, agent.get_location().y)
                self.turtle.stamp()
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
