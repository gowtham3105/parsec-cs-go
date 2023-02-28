"""The ViewController drives the visualization of the simulation."""
from math import pi
from turtle import Turtle, Screen, done, register_shape
from models.Environement import Environment
from constants import *
from typing import Any
from time import time_ns
from utils import get_color
from PIL import Image

NS_TO_MS: int = 1000000

AGENT_IMAGE = 'gifs/among_us.gif'
CUR_AGENT_IMAGE = AGENT_IMAGE.split('.')[0] + "edited.gif"


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
        size = (AGENT_RADIUS * 2, AGENT_RADIUS * 2)
        im.thumbnail(size)
        im.save(CUR_AGENT_IMAGE)
        self.screen.register_shape(CUR_AGENT_IMAGE)
        self.turtle = Turtle(shape=CUR_AGENT_IMAGE)
        self.turtle.hideturtle()

    def start_simulation(self):
        """Call the first tick of the simulation and begin turtle gfx."""
        self.tick()
        done()

    def draw_agents(self):
        self.turtle.clear()
        for team in self.environment.agents:
            for agent_id, agent in self.environment.agents[team].items():
                self.pen.color(get_color(agent.get_team()))
                self.pen.penup()
                self.pen.goto(agent.get_location().x, agent.get_location().y)
                self.pen.pendown()
                self.pen.dot(AGENT_RADIUS * 2)  ## comment this line and uncomment the next lines to see
                # images instead of lines
                self.pen.penup()
                self.turtle.goto(agent.get_location().x, agent.get_location().y)
                self.turtle.stamp()

    def draw_bullets(self):
        for bullet in self.environment.bullets:
            if not bullet.is_alive():
                continue
            self.pen.penup()
            self.pen.goto(bullet.get_location().x, bullet.get_location().y)
            self.pen.pendown()
            self.pen.color("white")
            self.pen.dot(BULLET_RADIUS)

    def draw_agent_view_areas(self):
        for team in self.environment.agents:
            for agent_id, agent in self.environment.agents[team].items():
                self.pen.penup()
                self.pen.goto(agent.get_location().x, agent.get_location().y)
                self.pen.pendown()
                self.pen.color(get_color(agent.get_team()))
                self.pen.width(2)
                self.pen.setheading(agent.get_view_direction().get_angle() - (agent.get_view_angle() * 90 / pi))
                self.pen.forward(agent.get_range())
                self.pen.penup()
                self.pen.goto(agent.get_location().x, agent.get_location().y)
                self.pen.setheading(agent.get_view_direction().get_angle() + (agent.get_view_angle() * 90 / pi))
                self.pen.pendown()
                self.pen.forward(agent.get_range())
                self.pen.right(90)
                self.pen.circle(-1 * agent.get_range(), agent.get_view_angle() * 180 / pi, steps=30)

    def draw_information_boards(self):
        # TODO: draw information boards
        # Health, Score Fire COOLDOWN, recent alerts headlines etc.

        pass

    def draw_zones(self):
        # TODO: draw zones
        # square box with a color with the zone coordinates
        pass

    def draw_zone_information_boards(self):
        # TODO: draw zone information boards in the bottom
        # Time left, Time left for next zone shrink etc.
        pass

    def tick(self) -> dict[str, str | list[int]]:
        """Update the environment state and redraw visualization."""
        start_time = time_ns() // NS_TO_MS
        self.environment.tick()
        self.pen.clear()

        self.draw_agent_view_areas()
        self.draw_agents()
        self.draw_bullets()

        self.draw_information_boards()
        self.draw_zones()
        self.draw_zone_information_boards()

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
