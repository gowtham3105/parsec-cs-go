from models.State import State
from models.Action import Action
from models.Point import Point
from constants import *
import random
import math
from typing import List

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


def tick(state: State) -> List[Action]:

    actions = []
    for agent_id in state.agents:
        flag = 0
        agent = state.agents[agent_id]
        direction = agent.get_direction()

        if random.random() < 0.2:
            type = UPDATE_VIEW_DIRECTION
            current_direction = agent.get_view_direction()
            x_rad = math.acos(current_direction.x /
                              current_direction.distance(Point(0, 0)))
            y_rad = math.acos(current_direction.y /
                              current_direction.distance(Point(0, 0)))
            x_rad += random.random() * 2 * math.pi
            y_rad += random.random() * 2 * math.pi
            direction = Point(math.cos(x_rad), math.cos(y_rad))
            action = Action(agent_id, type, direction)
            flag = 1

        elif flag == 0:
            opponents = state.object_in_sight[agent_id]["Agents"]
            bullets = state.object_in_sight[agent_id]["Bullets"]

            if len(opponents) != 0:
                type = FIRE
                closest = float("inf")
                for opponent in opponents:
                    dist = opponent.location.distance(agent.get_location())
                    if dist < closest:
                        closest = dist
                        direction = Point(opponent.direction.x - agent.get_direction().x,
                                          opponent.direction.y - agent.get_direction().y)
                action = Action(agent_id, type, direction)
                flag = 1

            elif flag == 0:
                for alert in state.alerts:
                    if alert.alert_type == BULLET:
                        type = UPDATE_DIRECTION
                        direction = Point(agent.get_direction(
                        ).x + 0.69, agent.get_direction().y + 0.7)
                        action = Action(agent_id, type, direction)
                        flag = 1
                        break

                if flag == 0:
                    for alert in state.alerts:
                        if alert.alert_type == COLLISION:
                            type = UPDATE_DIRECTION
                            direction = Point(-agent.get_direction().x, -
                                              agent.get_direction().y)
                            action = Action(agent_id, type, direction)
                            flag = 1
                            break
        if flag == 0:
            type = UPDATE_VIEW_DIRECTION
            action = Action(agent_id, type, direction)
            current_direction = agent.get_view_direction()
            x_rad = math.acos(current_direction.x /
                              current_direction.distance(Point(0, 0)))
            y_rad = math.acos(current_direction.y /
                              current_direction.distance(Point(0, 0)))
            x_rad += random.choice([-1, 1]) * (math.pi/6)
            y_rad += random.choice([-1, 1]) * (math.pi/6)
            direction = Point(math.cos(x_rad), math.cos(y_rad))

        action = Action(agent_id, type, direction)
        actions.append(action)

    return actions
