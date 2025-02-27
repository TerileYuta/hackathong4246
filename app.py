from flask import Flask, jsonify, request

from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError

from handlers import receiveMessage_Handler
from handlers import sendMessage_Handler

""" from services.calendar import get_available_time  
from handlers.message_handler import ask_available_time
from services.firestore_service import add_event, get_all_events   """
from services.features.firestore_logic import add_user_data, get_user_data, update_user_data, delete_user_data
from datetime import datetime

from utils.env import get_env

LINE_CHANNEL_SECRET = get_env('LINE_CHANNEL_SECRET')

# Webhookの署名を検証するハンドラー
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

@app.route('/')
def home():
    return "カレンダーアプリへようこそ！"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    print(f"Received signature: {signature}")
    if signature is None:
        return "Missing Signature", 403
    
    body = request.get_data(as_text=True)
    print(f"Request body: {body}")
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400
    except Exception as e:
        print(f"エラー発生: {e}")  
        return "Internal Server Error", 500

    return "OK", 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # user_text = event.message.text
    
    replyList = receiveMessage_Handler(event)
    result = sendMessage_Handler(replyList, event)

    return result

""" # 空き時間確認のエンドポイント
@app.route('/available-times')
def free_times():
    # この週の空き時間を取得
    free_slots = get_available_time(time_range="this_week") 
    return jsonify(free_slots) """

# ユーザデータを追加するエンドポイント
@app.route('/add-user', methods=['POST'])
def add_user_endpoint():
    try:
        # リクエストのJSONデータを取得
        user_data = request.get_json()

        # 必須フィールドのチェック
        required_fields = ["line_id", "google_email", "access_token", "refresh_token", "token_expiry"]
        if not all(field in user_data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # token_expiry を datetime に変換（文字列なら）
        if isinstance(user_data["token_expiry"], str):
            user_data["token_expiry"] = datetime.strptime(user_data["token_expiry"], "%Y-%m-%d")

        # Firestore にデータを追加
        response = add_user_data(user_data)
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ユーザデータを取得するエンドポイント
@app.route('/get-user/<line_id>', methods=['GET'])
def get_user_endpoint(line_id):
    try:
        # Firestore からユーザデータを取得
        user_data = get_user_data(line_id)
        
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Flask アプリをデバッグモードで実行
    app.run(debug=True)
