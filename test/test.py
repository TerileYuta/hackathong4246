from pathlib import Path
import sys

# 親ディレクトリをパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

from handlers import receiveMessage_Handler
from handlers import sendMessage_Handler

class DummyMessage:
    def __init__(self, text):
        self.text = text

class DummyEvent:
    def __init__(self, text):
        self.message = DummyMessage(text)

debug = True

while(True):
    user_message = input("あなた：")

    replyList = receiveMessage_Handler(user_message)
    result = sendMessage_Handler(replyList, None, True)

    for message in result:
        print(f"Bot : {message}")
