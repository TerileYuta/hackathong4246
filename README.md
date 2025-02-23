# hackathong4246

## フォルダ構成（仮）
スケジュール登録機能などはservicesフォルダに作成する
(ex:./line-bot/services/schedule.py)
```
line-bot/
│
├── app.py                # メインのFlaskアプリケーション
├── config.py             # 設定ファイル（アクセストークン、シークレットなど）
├── requirements.txt      # 必要なライブラリのリスト
├── .env                  # 環境変数を管理（アクセストークンなど）
│
├── handlers/             # メッセージ処理のモジュール
│   ├── __init__.py       # このディレクトリをモジュールとして扱うためのファイル
│   ├── message_handler.py # メッセージ受信と応答を処理するロジック
│   └── event_handler.py   # イベント処理（ユーザー追加など）を記述するファイル
│
├── services/             # 外部APIやビジネスロジックを処理
│   ├── __init__.py       # モジュールとして扱うためのファイル
│   └── external_api.py   # 外部APIとの連携ロジック（天気、ニュースなど）
│
├── models/               # データ構造やデータベース関連
│   ├── __init__.py       # モジュールとして扱うためのファイル
│   └── user_model.py     # ユーザー情報を管理するデータモデル
│
└── utils/                # ユーティリティ関数（エラーハンドリング、ログなど）
    ├── __init__.py       # モジュールとして扱うためのファイル
    └── logger.py         # ロギング機能
```
