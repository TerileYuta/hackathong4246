# services/handlers/message_receive_handler.py

from .langgraph import Model

from .lineProfile import get_user_display_name
from .personalkey import getMembersId
from .rule import analyze_message

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
    group_id = None
    line_ids = []

    message = event.message.text

    # メッセージ送信元の判別
    if hasattr(event.source, "group_id"): 
        group_id = event.source.group_id

        line_ids = getMembersId(group_id)
    elif hasattr(event.source, "user_id"): 
        line_ids = [event.source.user_id]

    user_names = [get_user_display_name(line_id) for line_id in line_ids]

    # ルールベース処理
    reply = analyze_message(message, group_id, line_ids, user_names)
    if reply:
        return reply

    #LLLM推論部
    model = Model(line_ids, user_names)
    model_output = model.invoke(message)

    return [
        {
            "type" : "text",
            "text" : model_output
        }    
    ]


