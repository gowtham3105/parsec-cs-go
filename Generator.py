from models.Obstacle import Obstacle
from models.Point import Point
from constants import *
import random
import math



class Generator:
    
    def generate_random_circles(self, N):
        map_area = (MAX_X - MIN_X) * (MAX_Y - MIN_Y)
        circle_area = map_area * OBSTACLE_PERCENTAGE / N
        circles = []
        for i in range(N):
            radius = math.sqrt(circle_area / math.pi)
            x = random.uniform(MIN_X + radius, MAX_X - radius)
            y = random.uniform(MIN_Y + radius, MAX_Y - radius)
            intersects = False
            for circle in circles:
                distance = math.sqrt((x - circle[0]) ** 2 + (y - circle[1]) ** 2)
                if distance < radius + circle[2]:
                    intersects = True
                    break

            if not intersects:
                circles.append((x, y, radius))

        return circles
    
    def get_points_on_circle(self, circle, number_of_points):
        points = []
        radian_hash = {}
        for _ in range(number_of_points):
            theta = random.uniform(0, 2 * math.pi)
            point = Point(circle[0] + circle[2] * math.cos(theta), circle[1] + circle[2] * math.sin(theta))
            radian_hash[str(point)] = theta
            points.append(point)
        points.sort(key=lambda point: radian_hash[str(point)])
        return points

            
    def generate_obstacles(self, number_of_obstacles):
        # TODO: Generate non intersecting polygon obstacles
        obstacles = []
        distinct_circles = self.generate_random_circles(number_of_obstacles)
        for circle in distinct_circles:
            number_of_points = random.randint(3, MAX_OBSTACLE_SIDES)
            obstacle_corners = self.get_points_on_circle(circle, number_of_points)
            obstacle = Obstacle(obstacle_corners)
            obstacles.append(obstacle)
        return obstacles
