import secrets

from flask import Flask, request, redirect, session
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent, JoinEvent
from linebot.v3.exceptions import InvalidSignatureError

from google_auth_oauthlib.flow import Flow

from handlers import receiveMessage_Handler
from handlers import sendMessage_Handler
from handlers import follow_Handler, join_Handler

from config import Config
from services.google_calendar_api import GoogleCalendarAPI
from utils.env import get_env


LINE_CHANNEL_SECRET = get_env('LINE_CHANNEL_SECRET')

# Webhookの署名を検証するハンドラー
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32) 
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # https接続

# Oauth認証用ページ
@app.route('/oauth')
def google_login():
    """
    
    Google認証用URLを作成する

    Parameters
    ----------
        None

    Returns
    ----------
        リダイレクトURL

    """

    line_id = request.args.get('line_id')

    if not line_id:
       return redirect(f"https://line.me/R/ti/p/{Config.official_line_id}")
    
    session["line_id"] = line_id

    google_calendar_api = GoogleCalendarAPI(line_id, request.root_url)
    auth_url = google_calendar_api.authenticate()

    if auth_url:
        return redirect(auth_url)
    else:
        sendMessage_Handler(
            [{
                "type": "text",
                "text": "Google Calendarの認証が完了しました"
            }],
            line_id = line_id
        )

        return redirect(f"https://line.me/R/ti/p/{Config.official_line_id}")
    
# Oauth認証のcallbackページ
@app.route("/oauth/callback")
def google_callback():
    """

    Google認証後、アクセストークンを取得しFirestoreに保存

    Parameters
    ----------
        None

    Returns
    ----------
        リダイレクトURL
    
    """

    line_id = session.get("line_id")
    if not line_id:
        return redirect(f"https://line.me/R/ti/p/{Config.official_line_id}")

    flow = Flow.from_client_secrets_file(
        Config.credentials_path,
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri=f"{request.root_url}{Config.google_oauth_callback_url}"
    )

    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials

    google_api = GoogleCalendarAPI(line_id, "")
    google_api.updateToken({
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes
    })

    sendMessage_Handler(
        [{
            "type": "text",
            "text": "Google Calendarの認証が完了しました"
        }],
        line_id = line_id
    )

    return redirect(f"https://line.me/R/ti/p/{Config.official_line_id}")

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
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

# Message受信イベント
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):    
    replyList = receiveMessage_Handler(event)
    sendMessage_Handler(replyList, event)

# 友達追加イベント
@handler.add(FollowEvent)
def handle_follow(event):
    line_id = event.source.user_id
    replyList = follow_Handler(line_id, request.url_root)

    sendMessage_Handler(replyList, event)

# グループ追加イベント
@handler.add(JoinEvent)
def handle_join(event):
    group_id = event.source.group_id

    replyList = join_Handler(group_id)

    sendMessage_Handler(replyList, event)

if __name__ == "__main__":
    app.run(port=5000)