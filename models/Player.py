from typing import List

import requests

from models.Action import Action
from models.State import State
from constants import PLAYER_REQUEST_TIMEOUT


class Player:
    client_url: str
    _id: int
    team: str
    token: str
    sub_path: str = "/tick"

    def __init__(self, team: str, client_url: str, token: str):
        self.client_url = client_url
        self._id = id(self)
        self.token = token
        self.team = team

    def tick(self, state: State) -> List[Action]:
        # make a post request to the client url with the state
        # get the response and convert it to an action
        # return the action

        data = {
            "state": state.__dict__,
            "token": self.token,
        }

        try:
            req = requests.post(
                self.get_full_url(),
                json=data,
                timeout=PLAYER_REQUEST_TIMEOUT,
            )
            if req.status_code == 200:
                return [Action(**action) for action in req.json()["actions"]]
        except requests.exceptions.Timeout:
            print(f"Player {self.team}'s Request timed out")
            return None
        except Exception as e:
            print(e)
            return None

    def __str__(self):
        return f"Player with id {self._id} and token {self.token}"

    def __repr__(self):
        return self.__str__()

    def get_full_url(self):
        return self.client_url + self.sub_path
