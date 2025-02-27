# handlers/message_receive_handler.py

import re

#from services.features.get_available_time import answer_available_time

def receiveMessage_Handler(message: str):
    """
    受信したメッセージを分析し、リプライメッセージを作成する
    Parameters
    ----------
        message(str) : ユーザーメッセージ
    Returns
    ----------
        dict : リプライメッセージに関する情報
    """
    
    """
    # メッセージに特定のキーワードが含まれている場合に空き時間を検索
    if "いつ" in message or "空いてる" in message:
        return answer_available_time(message)
    """
    
    return [
        {
        "type" : "text",
        "text" : f"あなたのメッセージ：{message}"
        }    
    ]