from models.State import State
from models.Action import Action
from models.Point import Point
from models.Obstacle import Obstacle
from constants import *
import random
import math
from typing import List
import socket
import pickle
import sys


#     agents: Dict[str, Agent]  # The player's agents
#     object_in_sight: Dict[str, List[ObjectSighting]]  # Agent : [ObjectSighting] ,Bullet: [ObjectSighting]  ,Wall: [
#     # ObjectSighting]
#     Alerts: List[Alert]  # List of alerts collisions, zone, bullet_hit etc
#     team: str
#     time: int
#     obstacles: List[Obstacle]  # List of obstacles in the environment
#     zone: List[Point]  # List of corners in the zone
#     safe_zone: List[Point]  # List of corners in the safe zone
#     is_zone_shrinking: bool  # True if zone is shrinking, False if zone is expanding
#     STRING = "Agents: {agents} \n Object in sight: {object_in_sight} \n Alerts: {alerts} \n Team: {team} \n Time: {" \
#              "time} \n Obstacles: {obstacles} \n Zone: {zone} \n Safe Zone: {safe_zone} \n Is Zone Shrinking: {" \
#              "is_zone_shrinking} "

def is_safe_zone(agent, safe_zone):
    pseudo_obstacle = Obstacle(safe_zone)
    return pseudo_obstacle.checkInside(agent.get_location())


def tick(state: State) -> List[Action]:

    actions = []
    for agent_id in state.agents:
        flag = 0
        agent = state.agents[agent_id]
        direction = agent.get_direction()

        if not is_safe_zone(agent, state.safe_zone):
            p1, p2, p3, p4 = state.safe_zone
            center_x, center_y = (p1.x + p3.x)/2, (p1.y + p3.y)/2
            type = UPDATE_DIRECTION
            direction = Point(center_x - agent.get_location().x,
                              center_y - agent.get_location().y)
            flag = 1

        if flag == 0:
            opponents = state.object_in_sight[agent_id]["Agents"]
            bullets = state.object_in_sight[agent_id]["Bullets"]

            if len(opponents) != 0:
                type = FIRE
                closest = float("inf")
                len(opponents)
                for opponent in opponents:
                    dist = opponent.get_location().distance(agent.get_location())
                    if dist < closest:
                        closest = dist
                        direction = Point(opponent.get_location().x - agent.get_location().x,
                                          opponent.get_location().y - agent.get_location().y)
                action = Action(agent_id, type, direction)
                flag = 1

            if flag == 0:
                for alert in state.alerts:
                    if alert.alert_type == COLLISION:
                        # print("Alert Collision BLUE")
                        type = UPDATE_DIRECTION
                        direction = Point(agent.get_direction().x,
                                          agent.get_direction().y) + Point(random.uniform(-3, 3), random.uniform(-3, 3))
                        action = Action(agent_id, type, direction)
                        flag = 1
                        break
        if flag == 0:
            if random.uniform(0, 1) < 1:
                type = UPDATE_VIEW_DIRECTION
                action = Action(agent_id, type, direction)
                current_direction = agent.get_view_direction()
                direction = current_direction + \
                    Point(random.uniform(-1, 1), random.uniform(-1, 1))
            else:
                type = UPDATE_DIRECTION
                action = Action(agent_id, type, direction)
                current_direction = agent.get_direction()
                direction = current_direction + \
                    Point(random.uniform(-1, 1), random.uniform(-1, 1))

        action = Action(agent_id, type, direction)
        # print("Blue:", action)
        actions.append(action)

    return actions


if __name__ == '__main__':
    server_port = ENV_PORT
    server_host = 'localhost'

    blue_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    blue_socket.settimeout(2)

    blue_host = 'localhost'
    blue_port = BLUE_PORT
    blue_socket.bind((blue_host, blue_port))
    print("Blue player is ready to receive messages...")
    while True:
        try:
            environment_message, addr = blue_socket.recvfrom(65527)
        except:
            print("Environment Not Responding...Blue Closed")
            blue_socket.close()
            sys.exit(1)
        state = pickle.loads(environment_message)
        actions = tick(state)
        new_message = pickle.dumps(actions)
        blue_socket.sendto(new_message, (server_host, server_port))
