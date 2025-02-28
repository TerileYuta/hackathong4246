from .personalkey import addNewGrop

def follow_Handler(line_id : str, root_url):
    """
    
    友達追加時に行う処理

    Parameters
    ----------
        line_id(str) : ユーザーのLINE ID
        root_url(str) : ページのルートURL

    Returns
    ----------
        list : ユーザーへの送信内容

    """

    messages = [{
        "type" : "text",
        "text" : "友だち登録ありがとうございます！"
    }]

    auth_url = f"{root_url}oauth?line_id={line_id}"

    messages.append({
        "type" : "text",
        "text" : "Googleカレンダーにアクセスするための認証を行う必要があります。次のURLにアクセスして認証を完了してください"
    })
    messages.append({
        "type" : "text",
        "text" : auth_url
    })

    return messages

def join_Handler(group_id:str):
    """
    
    アカウントがグループに追加された際の処理

    Paramters
    ---------
        group_id(str) : グループのID

    Returns
    ---------
        list : グループへの送信内容

    """
    
    addNewGrop(group_id)

    return [{
        "type": "text",
        "text": "グループ追加ありがとうございます！\n現在、グループでは個人を識別することができません。そのため個人識別キーの送信をお願いします。\nなお、個人識別キーは公式アカウントのトーク画面で「個人識別キー」とご送信ください。"
    }]
