from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
)
from utils.env import get_env

LINE_ACCESS_TOKEN = get_env("LINE_ACCESS_TOKEN")
configuration = Configuration(access_token=LINE_ACCESS_TOKEN)
api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)

def get_user_display_name(user_id:str):
    """
    
    ユーザーIDからLINEの表示名を取得
    
    Parameters
    ----------
        user_id(str) : LINE ID

    Returns
    ----------
        str: ユーザーネーム

    """
    
    try:
        profile = messaging_api.get_profile(user_id)
        return profile.display_name
    
    except Exception as e:
        print(f"ユーザー名の取得に失敗: {e}")

        return None