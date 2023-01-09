class Action:
    _id: int
    agent_id: int
    type: str  # UPDATE_DIRECTION, UPDATE_VIEW_DIRECTION, FIRE
    # TODO: complete this

    def __init__(self, id, agent_id, action_type):
        self._id = id
        self.agent_id = agent_id
        self.action_type = action_type

    def __str__(self):
        return self._id

    def __repr__(self):
        return self._id
