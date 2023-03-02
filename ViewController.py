"""The ViewController drives the visualization of the simulation."""
from math import pi
from turtle import Turtle, Screen, done, register_shape
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
        self.pen.color("black")

        self.pen.hideturtle()
        self.pen.speed(0)

    def start_simulation(self):
        """Call the first tick of the simulation and begin turtle gfx."""
        
        self.tick()
        done()

    def draw_agents(self):
        for team in self.environment.agents:
            for agent_id, agent in self.environment.agents[team].items():
                self.pen.penup()
                self.pen.goto(agent.get_location().x, agent.get_location().y)
                self.pen.pendown()
                self.pen.color(get_color(agent.get_team()))
                self.pen.dot(AGENT_RADIUS * 2)

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
    
    def draw_obstacles(self):
        # TODO: draw obstacles for each polygon obstacle and fill gray
        for obstacle in self.environment.obstacles:
            points = obstacle.corners
            self.pen.penup()
            self.pen.goto((points[0].x, points[0].y))
            self.pen.pendown()
            self.pen.fillcolor('gray')
            self.pen.begin_fill()

            # Draw lines to connect each point in order
            for point in points[1:]:
                self.pen.goto((point.x, point.y))

            # Return to the starting point to close the polygon
            self.pen.goto((points[0].x, points[0].y))

            # End the fill and hide the turtle
            self.pen.end_fill()
            self.pen.hideturtle()
        
        pass

    def draw_information_boards(self):

        # Score display
        self.pen.penup()
        self.pen.goto(-VIEW_WIDTH / 2, VIEW_HEIGHT / 2)
        self.pen.pendown()
        self.pen.fillcolor("black")
        self.pen.begin_fill()
        self.pen.pencolor('green')
        self.pen.pensize(10)
        self.pen.forward(VIEW_WIDTH - 7)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(10)
        self.pen.forward(VIEW_HEIGHT * 0.23)
        self.pen.right(90)
        self.pen.pencolor('white')
        self.pen.pensize(5)
        self.pen.forward(VIEW_WIDTH - 7)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(10)
        self.pen.forward(VIEW_HEIGHT * 0.23)
        self.pen.right(90)
        self.pen.end_fill()

        # Rectangle for penalty scores
        self.pen.pensize(1)
        self.pen.penup()
        self.pen.goto(-VIEW_WIDTH / 2, VIEW_HEIGHT / 2 - VIEW_HEIGHT * 0.23)
        self.pen.pendown()
        self.pen.fillcolor("black")
        self.pen.begin_fill()
        self.pen.pencolor('white')
        self.pen.pensize(5)
        self.pen.forward(VIEW_WIDTH - 7)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(10)
        self.pen.forward(VIEW_HEIGHT * 0.07)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(4)
        self.pen.forward(VIEW_WIDTH - 7)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(10)
        self.pen.forward(VIEW_HEIGHT * 0.07)
        self.pen.right(90)
        self.pen.end_fill()

        # Dividing score rectangle
        self.pen.penup()
        self.pen.goto(-VIEW_WIDTH / 5, VIEW_HEIGHT / 2 - 5)
        self.pen.pendown()
        self.pen.pencolor("white")
        self.pen.setheading(270)
        self.pen.pensize(1)
        self.pen.forward(VIEW_HEIGHT * 0.23 - 5)
        self.pen.penup()
        self.pen.goto(0, VIEW_HEIGHT / 2 - 5)
        self.pen.pendown()
        self.pen.pensize(4)
        self.pen.forward(VIEW_HEIGHT * 0.23 - 5) 
        self.pen.penup()
        self.pen.goto(VIEW_WIDTH / 5, VIEW_HEIGHT / 2 - 5)
        self.pen.pendown()
        self.pen.pensize(1)
        self.pen.forward(VIEW_HEIGHT * 0.23 - 5)

        # Dividing penalty score rectangle
        self.pen.penup()
        self.pen.goto(-VIEW_WIDTH / 7, VIEW_HEIGHT / 2 - VIEW_HEIGHT * 0.23)
        self.pen.pendown()
        self.pen.pensize(1)
        self.pen.pencolor("white")
        self.pen.setheading(270)
        self.pen.forward(VIEW_HEIGHT * 0.07 - 2.5)
        self.pen.penup()
        self.pen.goto(0, VIEW_HEIGHT / 2 - VIEW_HEIGHT * 0.23)
        self.pen.pendown()
        self.pen.pensize(4)
        self.pen.forward(VIEW_HEIGHT * 0.07 - 4)
        self.pen.penup()
        self.pen.goto(VIEW_WIDTH / 7, VIEW_HEIGHT / 2 - VIEW_HEIGHT * 0.23)
        self.pen.pendown()
        self.pen.pensize(1)
        self.pen.forward(VIEW_HEIGHT * 0.07 - 2.5)

        # Draw score for each team
        for team in self.environment.agents:
            if team == 'red':
                score = 500
                self.pen.penup()
                self.pen.goto(-VIEW_WIDTH / 2 + 10, VIEW_HEIGHT / 2 - 25)
                self.pen.pendown()
                self.pen.pencolor('red')
                i = 1
                for agent_id, agent in self.environment.agents['blue'].items():
                    score -= agent.get_health()

                    # Display agent's health
                    self.pen.write(str(agent_id) + ": " + str(agent.get_health()), font=("Arial", 10, "normal"))   # Write the text "Hello" with the given font and size
                    self.pen.penup()
                    self.pen.goto(-VIEW_WIDTH / 2 + 10, VIEW_HEIGHT / 2 - 25 - 15*i)   # Move the pen to the next line
                    self.pen.pendown()

                # Write score 
                self.pen.penup()
                self.pen.goto(-VIEW_WIDTH / 10, VIEW_HEIGHT / 2 - VIEW_HEIGHT * 0.05 - 35)
                self.pen.pendown()
                self.pen.color(get_color(team))
                self.pen.write(f"{score}", align="center", font=("Arial", 16, "bold"))
                self.pen.penup()
                self.pen.goto(-VIEW_WIDTH / 14, VIEW_HEIGHT / 2 - VIEW_HEIGHT * 0.23 - 25)
                self.pen.pendown()

                # Write penalty Score
                self.pen.write(f"{score}", align="center", font=("Arial", 13, "bold"))

            elif team == 'blue':
                score = 500
                self.pen.penup()
                self.pen.goto(VIEW_WIDTH / 5 + 70, VIEW_HEIGHT / 2 - 25)
                self.pen.pendown()
                self.pen.pencolor('blue')
                i = 1
                for agent_id, agent in self.environment.agents['blue'].items():
                    score -= agent.get_health()

                    # Display agent's health
                    self.pen.write(str(agent_id) + ": " + str(agent.get_health()), font=("Arial", 10, "normal"))   # Write the text "Hello" with the given font and size
                    self.pen.penup()
                    self.pen.goto(VIEW_WIDTH / 5 + 30, VIEW_HEIGHT / 2 - 25 - 15*i)    # Move the pen to the next line
                    self.pen.pendown()

                # Write score
                self.pen.penup()
                self.pen.goto(VIEW_WIDTH / 10, VIEW_HEIGHT / 2 - VIEW_HEIGHT * 0.05 - 35)
                self.pen.pendown()
                self.pen.color(get_color(team))
                self.pen.write(f"{score}", align="center", font=("Arial", 16, "bold"))
                self.pen.penup()
                self.pen.goto(VIEW_WIDTH / 14, VIEW_HEIGHT / 2 - VIEW_HEIGHT * 0.23 - 25)
                self.pen.pendown()

                # Write penalty Score
                self.pen.write(f"{score}", align="center", font=("Arial", 13, "bold"))
    
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

        self.draw_obstacles()
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
