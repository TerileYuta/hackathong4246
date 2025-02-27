import os

class ConfigClass:
    def __init__(self):
        self.root_path = os.path.abspath(os.path.dirname(__file__))
        
        self.credentials_path = f"{self.root_path}/google_calendar_api/credentials.json"
        self.firebase_json_path = f"{self.root_path}/firebase/firebase-key.json"

        self.official_line_id = "@990vsiwc"
        self.google_oauth_callback_url = "oauth/callback"