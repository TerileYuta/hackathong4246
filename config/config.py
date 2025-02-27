import os

class ConfigClass:
    def __init__(self):
        # self.root_path = os.path.dirname(os.getcwd())
        self.root_path = os.path.abspath(os.path.dirname(__file__))

        self.credentials_path = f"{self.root_path}/google_calendar_api/credentials.json"
        self.firebase_json_path = f"{self.root_path}/firebase/firebase-key.json"