from flask import Flask, request

from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError

from handlers import receiveMessage_Handler
from handlers import sendMessage_Handler

from utils.env import get_env

LINE_CHANNEL_SECRET = get_env('LINE_CHANNEL_SECRET')

# Webhookの署名を検証するハンドラー
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    if signature is None:
        return "Missing Signature", 403

    body = request.get_data(as_text=True)
    
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
    user_text = event.message.text
    
    replyList = receiveMessage_Handler(user_text)
    result = sendMessage_Handler(replyList, event)

    return result

if __name__ == "__main__":
    app.run(port=5000)
