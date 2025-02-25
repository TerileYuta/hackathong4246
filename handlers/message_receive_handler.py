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

    #TODO : メッセージの分析等の処理の追加

    return [
        {
        "type" : "text",
        "text" : f"あなたのメッセージ：{message}"
        }    
    ]