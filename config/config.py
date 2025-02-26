import os

class ConfigClass:
    def __init__(self):
        self.root_path = os.path.dirname(os.getcwd())
        
        self.credentials_path = f"{self.root_path}/config/GoogleCalenderAPI/credentials.json"
        self.firebase_json_path = f"{self.root_path}/config/firebase/firebase-key.json"