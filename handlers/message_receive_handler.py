# services/handlers/message_receive_handler.py

import re
from services.features.travel_time import reply_travel_time
from services.features.get_available_time import reply_available_time
from services.features.travel_time import reply_travel_time
from services.features.schedule_list import reply_events
from services.features.weather import reply_weather
from services.features.firestore_logic import get_user_state, update_user_state
from .langgraph import Model

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
    message = event.message.text  # 受信したメッセージのテキストを取得
    line_id = event.source.user_id  # ユーザーIDを取得

    # ユーザーの現在の状態をFirestoreから取得
    state_data = get_user_state(line_id)
    state = state_data['state'] if state_data else None
    context = state_data['context'] if state_data else None

    # ルールベース関連処理
    """
    if "天気" in message:
        # 状態がNoneの場合は、都市名を尋ねて天気の検索を開始
        update_user_state(line_id, "waiting_for_city", None)  # ユーザーの状態を"waiting_for_city"に更新
        return reply_weather(message, line_id, None)  # 初回の状態で天気リプライを呼び出す
    
    elif "いつ" in message or "空いてる" in message:
        return reply_available_time(message, line_id)  # 空き時間を確認するリプライを返す
    
    elif "経路" in message:  # 経路に関するクエリに対応
        return reply_travel_time(message)
    elif "予定" in message:  # 予定に関連するクエリに対応
        return reply_events(event)
    if state == "waiting_for_city":
        return reply_weather(message, line_id, state)  # 都市名の入力を処理
    
    # ユーザーが天気情報を取得している途中で、日付を尋ねる状態
    elif state == "waiting_for_date":
        return reply_weather(message, line_id, state) 

    return [
        {
            "type": "text",
            "text": f"あなたのメッセージ：{message}"  # 認識できないメッセージをそのまま表示
        }
    ]
    """

    #LLLM推論部
    """

    model = Model(line_id)
    model_output = model.invoke(message)

    return [
        {
            "type" : "text",
            "text" : model_output
        }    
    ]
    """