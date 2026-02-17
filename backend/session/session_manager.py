import json
import os


SESSION_FILE = ".autonomous_session.json"


class SessionManager:

    def __init__(self):
        self.path = os.path.abspath(SESSION_FILE)

    def exists(self):
        return os.path.exists(self.path)

    def save(self, data: dict):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not self.exists():
            return None
        with open(self.path, "r") as f:
            return json.load(f)

    def clear(self):
        if self.exists():
            os.remove(self.path)
