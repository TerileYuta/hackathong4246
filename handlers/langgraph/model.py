from utils.text import open_text_file
from .ReAct import model_invoke
from datetime import datetime
from config import Config

class Model:
    def __init__(self, line_id):
        self.system_prompt = open_text_file(f"{Config.root_path}/handlers/langgraph/prompts/tool_selector.txt")
        self.system_prompt += f"\n今は{datetime.now()}です"
        self.line_id = line_id

    def invoke(self, message:str):
        system_message = {"role": "system", "content" : self.system_prompt}
        user_message = {"role": "user", "content": message}

        return model_invoke([system_message, user_message], self.line_id)
