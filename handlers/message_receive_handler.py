from handlers.langchain import model_invoke
from langchain_core.messages import HumanMessage

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

    # lang-graphによる処理の場合
    model_output = model_invoke(message)

    return [
        {
            "type" : "text",
            "text" : model_output
        }    
    ]