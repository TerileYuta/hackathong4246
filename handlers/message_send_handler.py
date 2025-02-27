# handlers/message_send_handler.py

from utils.env import get_env

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,

    ReplyMessageRequest,
    PushMessageRequest,

    TextMessage,
)

LINE_ACCESS_TOKEN = get_env('LINE_ACCESS_TOKEN')

configuration = Configuration(access_token=LINE_ACCESS_TOKEN)
api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)

def sendMessage_Handler(sendList: list, event = None, debug: bool = False, line_id:str = None):
    """
    
    メッセージの送信処理

    Parameters
    ----------
        event : 
        replyList(list) : リプライメッセージに関する情報
        degub(bool) : Debugモード

    Returns
    ----------
        dict : リプライメッセージに関する情報

    """

    messages = []

    for sendContent in sendList:
        #TODO : 送るメッセージのタイプ（テキスト、画像など）によって異なる処理を行う必要がある。

        messages.append(TextMessage(text=sendContent["text"]))
    
    if(not debug):
        try:
            if(not line_id):
                request_body = ReplyMessageRequest(
                    reply_token = event.reply_token,
                    messages = messages,
                )
                messaging_api.reply_message(request_body)
            
            else:
                request_body = PushMessageRequest(
                    to = line_id,
                    messages = messages
                )
                messaging_api.push_message(request_body)
        except: 
            print("メッセージ送信エラー")
    else:
        return messages