# hackathong4246

## 環境構築方法

``` cmd

git clone https://github.com/TerileYuta/hackathong4246.git -b develop
cd hackathong4246

# 仮想環境の構築
conda create --name myvenv
conda activate myvenv

# pipインストール
pip install --upgrade pip 
pip install -r requirements.txt

```

## フォルダ構成

スケジュール登録機能などはservices/featuresフォルダに作成する

(ex:./hackathong4246/services/features/schedule.py)

``` 
hackathong4246
│   .env                                 # 環境変数
│   app.py                               # メインファイル（Flaskアプリケーション）
│   config.py                            # 設定ファイル（リクエスト上限数、予定取得上限数など）
│   README.md
│   requirements.txt                     # 必要なライブラリのテスト
│   
├───handlers                             # メッセージの送受信関連処理
│   │   message_receive_handler.py       # メッセージの受信関連処理
│   │   message_send_handler.py          # メッセージの送信関連処理
│   │   __init__.py
│   │
│   ├───JSON                             # メッセージ送信時のJSONファイルの雛形
│   │       message.json
│   │
│   ├───langchain                        # AIベースのメッセージの分析
│   │   │   __init__.py
│   │   │
│   │   └───prompts                      # プロンプトエンジニアリング
│   └───rule                             # ルールベースのメッセージ分析
│           __init__.py
│
├───services                             # 機能やAPI関連
│   │   __init__.py
│   │
│   ├───features                         # 機能
│   │       __init__.py
│   │
│   ├───firestore                        # API(DB)
│   │       __init__.py
│   │
│   ├───google_calendar_api              # API(Google Calendar API)
│   │       __init__.py
│   │
│   └───google_map_api                   # API(Google Maps API)
│           __init__.py
│
└───utils                                # ユーティリティ関数
        __init__.py
        
```

## ブランチルール

mainブランチ・developブランチには直接pushしないようによろしくお願いします。

・機能の追加

```cmd
feature-(名前)-(機能名)
```

・issue

```cmd
fix-(名前)-(issue名・番号)
```

## テスト

### cmd上でのテストを行う方法

```cmd
cd test
python test.py

あなた：こんにちは
Bot : type='text' quick_reply=None sender=None text='あなたのメッセージ：こんにちは' emojis=None quote_token=None
あなた：
```

### ngokを用いたテスト方法
PCにngrokをダウンロードする必要があります。

```cmd
python app.py
```

```cmd
ngrok http 5000

ngrok (Ctrl+C to quit)
Sign up to try new private endpoints https://ngrok.com/new-features-update?ref=private

Session Status                online
Account                       
Version                       3.20.0
Region                        United States (us)
Interface                     http://127.0.0.1:4040
Forwarding                    https://5b6b-58-191-117-155.ngrok-free.app -> http://localhost:5000   
```

ForwardingのURL（今回の場合は```https://5b6b-58-191-117-155.ngrok-free.app```）を```https://5b6b-58-191-117-155.ngrok-free.app/callback```という風に編集してlinebotのwebhookに指定する。これによって実際のLINEアプリ上からテストを行うことができます。