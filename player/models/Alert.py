class Alert:
    _id: int
    alert_type: str  # COLLISION, ZONE, BULLET_HIT, DEAD
    agent_id: int
    STRING: str = "Alert with id {id} of type {type} for agent {agent_id}"

    def __init__(self, alertType, agentId):
        self._id = id(self)
        self.alert_type = alertType
        self.agent_id = agentId

    def set_id(self, id):
        self._id = id

    @staticmethod
    def generate_object(data: dict):
        params = {
            "alert_type": data['alert_type'],
            "agent_id": data['agent_id']
        }
        alert = Alert(**params)
        alert.set_id(data['id'])

        return alert
