import re
from ..personalkey import savePersonalKey
def analyze_message(message, group_id, line_ids, user_names):
    """

    ユーザーからのメッセージをルールーベースで分析する

    Parameters
    ----------
        message(str) : ユーザーメッセージ

    Returns
    ----------
        list : レスポンスメッセージ

    """

    # 識別キーの発行
    if message == "個人識別キー" and group_id is None:
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
        
    # 識別キーの登録処理
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
    
    return False
