class Alert:
    _id: int
    alert_type: str  # COLLISION, ZONE, BULLET_HIT
    agent_id: int
    STRING: str = "Alert with id {id} of type {type} for agent {agent_id}"

    def __init__(self):
        # TODO: implement this
        pass
