import argparse
import os
import time
from collections import defaultdict

from fastapi import HTTPException

from models.Action import Action
from models.State import State


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
    # check if player file exists
    if os.path.exists(f"players/player_{args.player}.py"):
        return True
    else:
        raise Exception(f"Player file players/player_{args.player}.py does not exist")


def convert_to_state(state: dict):
    """Convert the state dictionary to a State object."""
    return State(**state)


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
