import re

from services.features.get_available_time import get_available_time
from services.features.travel_time import reply_travel_time
from services.features.get_available_time import reply_available_time
from services.features.travel_time import reply_travel_time
from services.features.schedule_list import reply_events
from services.features.weather import reply_weather

from .langgraph import Model

from .lineProfile import get_user_display_name

from .personalkey import savePersonalKey, getMembersId

# ユーザーの状態を格納する辞書またはデータベースを想定
user_states = {}

def get_user_state(line_id):
    """

    ユーザーの現在の状態と追加のコンテキスト（例: 都市名）を取得する

    Parameters
    ----------
        line_id(str) : ユーザーのID

    Returns
    ----------
        dict : ユーザーの状態とコンテキスト（ない場合はNone）

    """
    return user_states.get(line_id, None)

def update_user_state(line_id, state, context=None):
    """

    ユーザーの状態と追加のコンテキスト（例: 都市名）を更新する

    Parameters
    ----------
        line_id(str) : ユーザーのID
        state(str) : ユーザーの状態
        context(dict) : 状態に関連するコンテキスト（デフォルトはNone）

    """

    if context is None:
        context = {}  # コンテキストが提供されていない場合は空の辞書を設定
    user_states[line_id] = {"state": state, "context": context}

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

    #TODO : DB移行後state関連処理はstateフォルダのstate.pyに移動

    message = event.message.text  # 受信したメッセージのテキストを取得
    line_ids = []

    if hasattr(event.source, "group_id"): # グループ
        group_id = event.source.group_id
        print(group_id)
        line_ids = getMembersId(group_id)

        # groupIDからline IDを取得する処理
    elif hasattr(event.source, "room_id"): # 複数人トークルーム
        room_id = event.source.room_id
        
        # groupIDからline IDを取得する処理
    elif hasattr(event.source, "user_id"): # 個人
        line_ids = [event.source.user_id]
    else:
        sender_type = "不明"
        line_ids = "N/A"

    user_names = [get_user_display_name(line_id) for line_id in line_ids]

    # ユーザーの現在の状態を取得
    """
    state_data = get_user_state(line_ids)
    state = state_data['state'] if state_data else None
    context = state_data['context'] if state_data else None
    """

    #TODO : DB移行後下記ルールベース関連処理はrurleフォルダのrurle.pyに移動

    # ルールベース関連処理
    """
    # メッセージに天気に関するキーワードが含まれている場合
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

    # TODO グループでも送られてしまう問題あり
    if message == "個人識別キー":
        return [
            {
                "type": "text",
                "text": f"{user_names[0]}の個人識別キーは下記になります。下記をそのままコピーしてグループに送信してください。"
            },
            {
                "type": "text",
                "text": f"Personal Identification Key : {line_ids[0]}"
            },
        ]
    
    # 個人識別キーの登録処理
    match = re.search(r"Personal Identification Key\s*:\s*(\S+)", message)

    if match:
        key = match.group(1)
        savePersonalKey(group_id, key)

        return [
            {
                "type": "text",
                "text": "グループに紐づけられました"
            }
        ]

    #LLLM推論部
    model = Model(line_ids, user_names)
    model_output = model.invoke(message)

    return [
        {
            "type" : "text",
            "text" : model_output
        }    
    ]


