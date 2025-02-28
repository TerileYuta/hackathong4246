from pathlib import Path
import sys

# 親ディレクトリをパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

from handlers import receiveMessage_Handler
from handlers import sendMessage_Handler

class DummyMessage:
    def __init__(self, text):
        self.text = text

class DummySource:
    def __init__(self, user_id):
        self.user_id = user_id 

class DummyEvent:
    def __init__(self, text, user_id):
        self.message = DummyMessage(text)
        self.source = DummySource(user_id)

debug = True

while(True):
    user_message = input("あなた：")
    user_id = "lineID"
    event = DummyEvent(user_message, user_id)    
    replyList = receiveMessage_Handler(event)
    result = sendMessage_Handler(replyList, None, True)

    for message in result:
        print(f"Bot : {message}")
