from .Point import Point
from constants import UPDATE_DIRECTION, UPDATE_VIEW_DIRECTION, FIRE


class Action:
    _id: int
    agent_id: int
    type: str  # UPDATE_DIRECTION, UPDATE_VIEW_DIRECTION, FIRE
    direction: Point

    # TODO: complete this

    def __init__(self, id, agent_id, action_type):
        # validate the action
        self._id = id
        self.agent_id = agent_id
        if action_type in [UPDATE_DIRECTION, UPDATE_VIEW_DIRECTION, FIRE]:
            self.type = action_type
        else:
            raise ValueError("Invalid action type")

    def __str__(self):
        return self._id

    def __repr__(self):
        return self._id
