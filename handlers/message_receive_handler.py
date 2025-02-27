import re
from services.features.get_available_time import reply_available_time
from services.features.travel_time import reply_travel_time
from services.features.schedule_list import reply_events
from services.features.weather import reply_weather

# ユーザーの状態を格納する辞書またはデータベースを想定
user_states = {}

def get_user_state(user_id):
    """
    ユーザーの現在の状態と追加のコンテキスト（例: 都市名）を取得する
    Parameters
    ----------
        user_id(str) : ユーザーのID
    Returns
    ----------
        dict : ユーザーの状態とコンテキスト（ない場合はNone）
    """
    return user_states.get(user_id, None)

def update_user_state(user_id, state, context=None):
    """
    ユーザーの状態と追加のコンテキスト（例: 都市名）を更新する
    Parameters
    ----------
        user_id(str) : ユーザーのID
        state(str) : ユーザーの状態
        context(dict) : 状態に関連するコンテキスト（デフォルトはNone）
    """
    if context is None:
        context = {}  # コンテキストが提供されていない場合は空の辞書を設定
    user_states[user_id] = {"state": state, "context": context}

def receiveMessage_Handler(event):
    """
    受信したメッセージを分析し、リプライメッセージを作成する
    
    Parameters
    ----------
        event(dict) : イベントオブジェクト（userId と メッセージを含む）
        
    Returns
    ----------
        dict : リプライメッセージに関する情報
    """
    text = event.message.text  # 受信したメッセージのテキストを取得
    user_id = event.source.userId  # ユーザーIDを取得
    
    # ユーザーの現在の状態を取得
    state_data = get_user_state(user_id)
    state = state_data['state'] if state_data else None
    context = state_data['context'] if state_data else None

    # メッセージに天気に関するキーワードが含まれている場合
    if "天気" in text:
        # 状態がNoneの場合は、都市名を尋ねて天気の検索を開始
        update_user_state(user_id, "waiting_for_city", None)  # ユーザーの状態を"waiting_for_city"に更新
        return reply_weather(text, user_id, None)  # 初回の状態で天気リプライを呼び出す
    
    elif "いつ" in text or "空いてる" in text:
        return reply_available_time(event)  # 空き時間を確認するリプライを返す

    elif "経路" in text:  # 経路に関するクエリに対応
        return reply_travel_time(text)

    elif "予定" in text:  # 予定に関連するクエリに対応
        return reply_events(event)
    
    # ユーザーが天気情報を取得している途中で、都市を尋ねる状態
    if state == "waiting_for_city":
        return reply_weather(text, user_id, state)  # 都市名の入力を処理
    
    # ユーザーが天気情報を取得している途中で、日付を尋ねる状態
    elif state == "waiting_for_date":
        return reply_weather(text, user_id, state)  # 日付の入力を処理

    # 認識できないメッセージに対してデフォルトのレスポンス
    return [
        {
            "type": "text",
            "text": f"あなたのメッセージ：{text}"  # 認識できないメッセージをそのまま表示
        }
    ]
