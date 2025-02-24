# app.py

from flask import Flask, jsonify
from services.calendar import get_available_time  
from handlers.message_handler import handle_text_message

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Calendar App!"

# 空き時間確認
@app.route('/free-times')
def free_times():
    free_slots = get_available_time(time_range="this week") 
    return jsonify(free_slots)

# 以下：ローカルでのテスト用
class MockEvent:
    def __init__(self, message_text):
        self.message = MockMessage(message_text)
        self.reply_token = "mock_reply_token"

class MockMessage:
    def __init__(self, text):
        self.text = text

class MockLineBotAPI:
    def reply_message(self, reply_token, message):
        print(f"Replying with message: {message.text}")

if __name__ == "__main__":
    mock_event = MockEvent("来月空いてる？")  
    mock_line_bot_api = MockLineBotAPI()
    handle_text_message(mock_event, mock_line_bot_api)

    app.run(debug=True)