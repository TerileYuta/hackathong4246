import re
"""
from services.features.get_available_time import answer_available_time
from services.features.travel_time import search_travel_time
"""

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

    """
    # メッセージに特定のキーワードが含まれている場合に空き時間を検索
    if "いつ" in text or "空いてる" in text:
        return answer_available_time(event)  # イベントオブジェクトを渡して空き時間を回答

    elif "経路" in text:  # ユーザーが経路を尋ねている場合
        return search_travel_time(text)

    

    return [
        {
            "type": "text",
            "text": f"あなたのメッセージ：{text}"  # 他のメッセージがあった場合、そのまま表示
        }
    ]
    """

    model = Model(line_id)
    model_output = model.invoke(message)

    return [
        {
            "type" : "text",
            "text" : model_output
        }    
    ]

