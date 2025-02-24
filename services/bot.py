# LINE Botの設定（チャネルアクセストークン & シークレット）
LINE_ACCESS_TOKEN = 'iwaEqLWln0wmgbe2T7sqv2tV9ZVTvnnKmqoztN4yAaAzYxJpB9Qk62JXbwx6uCYY71AQF3HUqw1HoKm0K6ybwm+V9L6YFdqgQa65dKpLTBiSMZndmBejYEj4dniFFLLvAKwtPbCGcdVRvhzC9Gs/QwdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '1efa3dfc6332626bbd4681d509e1755a'

from flask import Flask, request
from linebot.v3.messaging import MessagingApi, ApiClient, Configuration, TextMessage, ReplyMessageRequest
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError

app = Flask(__name__)

# **ApiClient を使用して MessagingApi を設定**
configuration = Configuration(access_token=LINE_ACCESS_TOKEN)
api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)

# Webhookの署名を検証するハンドラー
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
        print(f"エラー発生: {e}")  # エラーメッセージを出力
        return "Internal Server Error", 500

    return "OK", 200

# ユーザーからのメッセージを受け取り、返信する
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_text = event.message.text
    reply_text = f"あなたのメッセージ: {user_text}"

    try:
        request_body = ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=reply_text)]
        )
        messaging_api.reply_message(request_body)
    except Exception as e:
        print(f"メッセージ送信エラー: {e}")  # メッセージ送信時のエラーを出力

if __name__ == "__main__":
    app.run(port=5000)
