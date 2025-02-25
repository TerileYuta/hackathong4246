import os
from dotenv import load_dotenv

def get_env(key: str, default=None):
    """
    
    環境変数を取得するヘルパー関数。
    
    Parameters
    ----------
        key(str) : 環境変数のキー名

    Returns
    ----------
        str : 環境変数の値 

    """

    load_dotenv() 
    return os.getenv(key, default)
