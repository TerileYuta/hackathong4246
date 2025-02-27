import os

class ConfigClass:
    def __init__(self):
        self.root_path = os.getcwd()
        
        self.credentials_path = f"{self.root_path}\\config\\GoogleCalenderAPI\\credentials.json"
        self.firebase_json_path = f"{self.root_path}\\config\\firebase\\firebase-key.json"

        self.official_line_id = "@990vsiwc"
        self.google_oauth_callback_url = "oauth/callback"