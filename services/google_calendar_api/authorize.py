# OAuthに使うやつです
from google.oauth2.credentials import Credentials  # 認証情報を管理するクラス
from google_auth_oauthlib.flow import InstalledAppFlow  # OAuth 認証フローを扱うクラス
from google.auth.transport.requests import Request  # 認証トークンを更新するためのクラス
import os  # ファイルやディレクトリの操作用

# Google Calendar API のスコープ（アクセス範囲）
# 'https://www.googleapis.com/auth/calendar' はカレンダーの読み書きを許可するスコープ
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    """
    OAuth 認証を行い、資格情報を取得する関数。
    初回認証時にブラウザで Google アカウントにログインし、認証情報を取得する。
    取得した認証情報は `token.json` に保存し、次回以降は再認証なしで利用可能。
    """
    creds = None

    # `authorize.py` のあるディレクトリのパスを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # `credentials.json` と `token.json` のパスを明示的に指定
    credentials_path = os.path.join(script_dir, 'credentials.json')
    token_path = os.path.join(script_dir, 'token.json')


    # 既存の認証トークンがあるか確認（`token.json` が存在する場合）
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # トークンがない、または無効になっている場合は再認証を行う
    if not creds or not creds.valid:
        # すでにトークンがあるが、期限切れの場合は更新する
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # 認証トークンを自動更新
        else:
            # `credentials.json` を使って新規に OAuth 認証を行う
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)  # ローカルサーバーを起動して認証を実行

        # 取得した認証情報を `token.json` に保存（次回以降の認証を省略するため）
        with open(credentials_path, 'w') as token:
            token.write(creds.to_json())

    return creds  # 認証情報を返す

# スクリプトを直接実行した場合、OAuth 認証を実行する
if __name__ == '__main__':
    get_credentials()  # 認証処理を実行
    print("OAuth 認証が完了しました！")  # 認証成功のメッセージを表示
