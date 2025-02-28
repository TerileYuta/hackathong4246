import os
from pathlib import Path

class ConfigClass:
    def __init__(self):
        self.root_path = os.path.abspath(Path(__file__).resolve().parent.parent)
        
        self.credentials_path = f"{self.root_path}/config/GoogleCalenderAPI/credentials.json"
        self.firebase_json_path = f"{self.root_path}/config/firebase/firebase-key.json"

        self.official_line_id = "@990vsiwc"
        self.google_oauth_callback_url = "oauth/callback"

        self.auth_error_msg = "Authentication error"

        self.llm_model = "gpt-4o"