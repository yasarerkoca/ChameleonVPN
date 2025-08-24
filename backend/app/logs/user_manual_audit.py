import logging

logger = logging.getLogger(__name__)

class UserManualAudit:
    def __init__(self):
        self.events = []

    def log_event(self, user_id: str, action: str, details: str = "") -> None:
        event = {"user_id": user_id, "action": action, "details": details}
        self.events.append(event)
        logger.info("UserManualAudit: %s", event)

    def get_events(self):
        return self.events
