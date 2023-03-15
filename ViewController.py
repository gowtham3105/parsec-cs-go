"""The ViewController drives the visualization of the simulation."""
from math import pi
from turtle import Turtle, Screen, done, register_shape
from models.Environement import Environment
from models.Point import Point
from typing import List
from constants import *
from typing import Any
from time import time_ns
from utils import get_color, get_zone_color
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
        self.pen.color("black")

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

    def draw_zone(self, zone: List[Point], zone_color: str):
        zone_length = zone[0].distance(zone[3])
        zone_breadth = zone[0].distance(zone[1])
        self.pen.penup()
        self.pen.goto(zone[3].x, zone[3].y)
        self.pen.setheading(0)
        self.pen.pendown()
        self.pen.color(zone_color)

        # Drawing a rectangle for zone
        for _ in range(4):
            self.pen.forward(zone_length if _ % 2 == 0 else zone_breadth)
            self.pen.right(90)

    def draw_agents(self):
        self.turtle.clear()
        for team in self.environment.agents:
            for agent_id, agent in self.environment.agents[team].items():
                if not agent.is_alive():
                    continue
                self.pen.color(get_color(agent.get_team()))
                self.pen.penup()
                self.pen.goto(agent.get_location().x, agent.get_location().y)
                self.pen.pendown()
                self.pen.dot(AGENT_RADIUS * 2)  # comment this line and uncomment the next lines to see
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
                if not agent.is_alive():
                    continue
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
    
    def draw_score_rectangle(self):

        # Draw score rectangle
        self.pen.penup()
        self.pen.goto(-VIEW_WIDTH / 2, VIEW_HEIGHT / 2)
        self.pen.pendown()
        self.pen.fillcolor("black")
        self.pen.begin_fill()
        self.pen.pencolor('green')
        self.pen.pensize(15)
        self.pen.forward(VIEW_WIDTH - 7)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(7)
        self.pen.forward(420 * 0.23)
        self.pen.right(90)
        self.pen.pencolor('white')
        self.pen.pensize(5)
        self.pen.forward(VIEW_WIDTH - 7)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(7)
        self.pen.forward(420 * 0.23)
        self.pen.right(90)
        self.pen.end_fill()

    def draw_penalty_rectangle(self):

        # Draw penalty rectangle
        self.pen.pensize(1)
        self.pen.penup()
        self.pen.goto(-VIEW_WIDTH / 2, VIEW_HEIGHT / 2 - 420 * 0.23)
        self.pen.pendown()
        self.pen.fillcolor("black")
        self.pen.begin_fill()
        self.pen.pencolor('white')
        self.pen.pensize(5)
        self.pen.forward(VIEW_WIDTH - 7)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(7)
        self.pen.forward(420 * 0.07)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(7)
        self.pen.forward(VIEW_WIDTH - 7)
        self.pen.right(90)
        self.pen.pencolor('green')
        self.pen.pensize(7)
        self.pen.forward(420 * 0.07)
        self.pen.right(90)
        self.pen.end_fill()

    def divide_score_rectangle(self):
        self.pen.penup()
        self.pen.goto(-VIEW_WIDTH / 5, VIEW_HEIGHT / 2 - 5)
        self.pen.pendown()
        self.pen.pencolor("white")
        self.pen.setheading(270)
        self.pen.pensize(1)
        self.pen.forward(420 * 0.23 - 5)
        self.pen.penup()
        self.pen.goto(0, VIEW_HEIGHT / 2 - 5)
        self.pen.pendown()
        self.pen.pensize(4)
        self.pen.forward(420 * 0.23 - 5) 
        self.pen.penup()
        self.pen.goto(VIEW_WIDTH / 5, VIEW_HEIGHT / 2 - 5)
        self.pen.pendown()
        self.pen.pensize(1)
        self.pen.forward(420 * 0.23 - 5)

    def divide_penalty_rectangle(self):

        # Divide penalty rectangle
        self.pen.penup()
        self.pen.goto(-VIEW_WIDTH / 7, VIEW_HEIGHT / 2 - 420 * 0.23)
        self.pen.pendown()
        self.pen.pensize(1)
        self.pen.pencolor("white")
        self.pen.setheading(270)
        self.pen.forward(420 * 0.07 - 2.5)
        self.pen.penup()
        self.pen.goto(0, VIEW_HEIGHT / 2 - 420 * 0.23)
        self.pen.pendown()
        self.pen.pensize(4)
        self.pen.forward(420 * 0.07 - 4)
        self.pen.penup()
        self.pen.goto(VIEW_WIDTH / 7, VIEW_HEIGHT / 2 - 420 * 0.23)
        self.pen.pendown()
        self.pen.pensize(1)
        self.pen.forward(420 * 0.07 - 2.5)



    def draw_information_boards(self):

        self.draw_score_rectangle()
        self.draw_penalty_rectangle()
        self.divide_score_rectangle()
        self.divide_penalty_rectangle()

        # Display score for each team
        for team in self.environment.agents:
            if team == 'red':
                score = 500
                self.pen.penup()
                self.pen.goto(-VIEW_WIDTH / 2 + 10, VIEW_HEIGHT / 2 - 27)
                self.pen.pendown()
                self.pen.pencolor('red')
                i = 0
                for agent_id, agent in self.environment.agents['red'].items():
                    # Display agent's health
                    self.pen.write(str(agent_id) + ": " + str(agent.get_health()), font=("Arial", 13, "bold"))
                    self.pen.penup()
                    i += 1
                    self.pen.goto(-VIEW_WIDTH / 2 + 10, VIEW_HEIGHT / 2 - 27 - 17*i)   # Move the pen to the next line
                    self.pen.pendown()

                for agent_id, agent in self.environment.agents['blue'].items():
                    score -= agent.get_health()
                # Write score 
                self.pen.penup()
                self.pen.goto(-VIEW_WIDTH / 10, (VIEW_HEIGHT) / 2 - ((420 * 0.28)/2))
                self.pen.pendown()
                self.pen.color(get_color(team))
                self.pen.write(f"{score}", align="center", font=("Arial", 16, "bold"))
                self.pen.penup()
                self.pen.goto(-VIEW_WIDTH / 14, VIEW_HEIGHT / 2 - 420 * 0.23 - 25)
                self.pen.pendown()

                # Write penalty Score
                self.pen.write(f"{score}", align="center", font=("Arial", 13, "bold"))

            elif team == 'blue':
                score = 500
                self.pen.penup()
                self.pen.goto(VIEW_WIDTH/2 - 75, VIEW_HEIGHT / 2 - 27)
                self.pen.pendown()
                self.pen.pencolor('blue')
                i = 0
                for agent_id, agent in self.environment.agents['blue'].items():
                    # Display agent's health
                    self.pen.write(str(agent_id) + ": " + str(agent.get_health()), font=("Arial", 13, "bold"))
                    self.pen.penup()
                    i+=1
                    self.pen.goto(VIEW_WIDTH/2 - 75, VIEW_HEIGHT / 2 - 27 - 17*i)    # Move the pen to the next line
                    self.pen.pendown()

                for agent_id, agent in self.environment.agents['red'].items():
                    score -= agent.get_health()
                # Write score
                self.pen.penup()
                self.pen.goto(VIEW_WIDTH / 10,  (VIEW_HEIGHT) / 2 - ((420 * 0.28)/2))
                self.pen.pendown()
                self.pen.color(get_color(team))
                self.pen.write(f"{score}", align="center", font=("Arial", 16, "bold"))
                self.pen.penup()
                self.pen.goto(VIEW_WIDTH / 14, VIEW_HEIGHT / 2 - 420 * 0.23 - 25)
                self.pen.pendown()

                # Write penalty Score
                self.pen.write(f"{score}", align="center", font=("Arial", 13, "bold"))
    
        # TODO: draw information boards
        # Health, Score Fire COOLDOWN, recent alerts headlines etc.
        pass
        
    def draw_obstacles(self):
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

    def draw_zone_information_boards(self):
        # TODO: draw zone information boards in the bottom
        # Time left, Time left for next zone shrink etc.
        pass

    def draw_finish_screen(self):
        # TODO: draw finish screen
        # Winner, Score, Time taken etc.
        pass

    def tick(self):
        """Update the environment state and redraw visualization."""
        start_time = time_ns() // NS_TO_MS
        self.environment.tick()
        self.pen.clear()

        self.draw_zone(self.environment.get_current_zone(), get_zone_color(ZONE))
        self.draw_zone(self.environment.get_current_safe_zone(), get_zone_color(SAFE_ZONE))
        self.draw_agent_view_areas()
        self.draw_agents()
        self.draw_bullets()
        self.draw_obstacles()

        self.draw_information_boards()

        self.draw_zone_information_boards()

        self.screen.update()

        if self.environment.is_complete():
            # self.screen.bye()
            self.draw_finish_screen()

            return
        else:
            end_time = time_ns() // NS_TO_MS
            next_tick = 30 - (end_time - start_time)
            if next_tick < 0:
                next_tick = 0
            self.screen.ontimer(self.tick, next_tick)
