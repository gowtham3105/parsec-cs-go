import argparse
import os
import time
from collections import defaultdict
from typing import List, Dict

from fastapi import HTTPException

from models.Agent import Agent
from models.Alert import Alert
from models.ObjectSighting import ObjectSighting
from models.Obstacle import Obstacle
from models.Point import Point
from models.State import State

DEFAULT_PLAYER = 'env'


def get_command_line_args():
    """Get command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--player",
        required=True,
        help="Player name for the server to run",
    )
    return parser.parse_args()


def validate_command_line_args(args: argparse.Namespace):
    if args.player == DEFAULT_PLAYER:
        return True
    # check if player file exists
    if os.path.exists(f"players/player_{args.player}.py"):
        return True
    else:
        raise Exception(f"Player file players/player_{args.player}.py does not exist")


def generate_agents(agents: List) -> List[Agent]:
    """Generate the agents."""
    return [Agent.generate_object(agent) for agent in agents]


def generate_object_sighting(object_in_sight: dict) -> Dict[str, List[ObjectSighting]]:
    """Generate the object sighting."""
    objects = {}
    for object_type in object_in_sight:
        objects[object_type] = [ObjectSighting.generate_object(obj) for obj in object_in_sight[object_type]]

    return objects


def generate_alerts(alerts: List) -> List[Alert]:
    """Generate the alerts."""
    return [Alert.generate_object(alert) for alert in alerts]


def generate_obstacles(obstacles: List) -> List[Obstacle]:
    """Generate the obstacles."""
    return [Obstacle.generate_object(obstacle) for obstacle in obstacles]


def generate_points(points: List) -> List[Point]:
    """Generate the points."""
    return [Point.generate_object(point) for point in points]


def generate_state(state: dict):
    """Convert the state dictionary to a State object."""
    params = {
        "agents": generate_agents(state["agents"]),
        "object_in_sight": generate_object_sighting(state["object_in_sight"]),
        "alerts": generate_alerts(state["alerts"]),
        "team": state["team"],
        "time": state["time"],
        "obstacles": generate_obstacles(state["obstacles"]),
        "zone": generate_points(state["zone"]),
        "safe_zone": generate_points(state["safe_zone"]),
        "is_zone_shrinking": bool(state["is_zone_shrinking"]),
    }

    return State(**params)


def authorized(token: str):
    def wrapper(func):
        def wrapped(body: dict):
            try:
                start_time = time.time()
                # get the token from the body
                if "token" not in body or body["token"] != token:
                    raise Exception("Unauthorized")

                result = func(body)

                print(f"Time taken for response: {time.time() - start_time}")

                return result
            except Exception as e:
                print(e)
                raise HTTPException(status_code=401, detail="Unauthorized")

        return wrapped

    return wrapper


def pre_check():
    def wrapper(func):
        def wrapped(body: dict):
            try:
                # check if state is present
                if "state" not in body or not body.get("state") or not isinstance(body.get("state"), dict):
                    raise Exception("Invalid request body")

                result = func(body)

                return result
            except Exception as e:
                print(e)
                raise HTTPException(status_code=400, detail="Invalid request body")

        return wrapped

    return wrapper


def get_env_vars(team: str) -> dict:
    """Get the dev environment variables."""

    if team == DEFAULT_PLAYER:
        team = os.getenv('PLAYER_TEAM')

    host_key = f"PLAYER_{team.upper()}_CLIENT_HOST"
    port_key = f"PLAYER_{team.upper()}_CLIENT_PORT"
    token_key = f"PLAYER_{team.upper()}_TOKEN"

    return defaultdict(
        lambda: None,
        {
            "host": os.getenv(host_key),
            "port": int(os.getenv(port_key)),
            "token": os.getenv(token_key),
        },
    )
