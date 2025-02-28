# hackathong4246

## 技術スタック

- フレームワーク：Flask
- データベース: Firestore
- API: Google Calendar API, Google Maps API, OpenWeatherMap
- AI: LangGraph(gpt-4o)


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

```

hackathong4246
│   .env
│   .gitignore
│   app.py
│   README.md
│   requirements.txt
│
├───config
│   │   config.py
│   │   __init__.py
│   │
│   ├───firebase
│   │       firebase-key.json
│   │
│   └───GoogleCalenderAPI
│           credentials.json
│
├───handlers
│   │   event_hadler.py
│   │   lineProfile.py
│   │   message_receive_handler.py
│   │   message_send_handler.py
│   │   personalkey.py
│   │   __init__.py
│   │
│   ├───langgraph
│   │   │   model.py
│   │   │   openai_api.py
│   │   │   ReAct.py
│   │   │   tools.py
│   │   │   __init__.py
│   │   │
│   │   └───prompts
│   │           tool_selector.txt
│   │
│   └───rule
│           rule.py
│           __init__.py
│
├───services
│   ├───features
│   │       get_available_time.py
│   │       schedule.py
│   │       travel_time.py
│   │       weather.py
│   │
│   ├───firestore
│   │       firestore_connection.py
│   │       __init__.py
│   │
│   └───google_calendar_api
│           calendar_api_connection.py
│           __init__.py
│
├───test
│       test.py
│
└───utils
        env.py
        text.py

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