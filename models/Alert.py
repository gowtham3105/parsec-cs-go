class Alert:
    _id: int
    alert_type: str  # COLLISION, ZONE, BULLET_HIT, DEAD
    agent_id: int

    def __init__(self, id, alertType, agentId):
        # TODO: implement this
        self._id = id
        self.alert_type = alertType
        self.agent_id = agentId
