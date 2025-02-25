# services/features/firestore_logic.py

from services.firestore.firestore_connection import db
import uuid
from datetime import datetime

def generate_uuid():
    """
    新しいUUIDを生成する
    Parameters
    ----------
        なし
    Returns
    ----------
        str : 生成されたUUID
    """

    return str(uuid.uuid4())

def add_user_data(user_data):
    """
    Firestoreの"users"コレクションに新しいユーザーデータを追加する
    Parameters
    ----------
        user_data (dict) : 追加するユーザーの情報（line_id, google_email, access_tokenなど）
    Returns
    ----------
        dict : 新しいユーザーIDを含む結果メッセージ
    """

    # ユーザーのために新しいUUIDを生成
    user_id = generate_uuid()

    # Firestoreの"users"コレクションに新しいユーザーデータを追加
    user_ref = db.collection("users").document(user_id)
    
    # 生成されたUUIDを含めてユーザーデータを追加
    user_ref.set({
        "ID": user_id,
        "line_id": user_data.get("line_id"),
        "google_email": user_data.get("google_email"),
        "access_token": user_data.get("access_token"),
        "refresh_token": user_data.get("refresh_token"),
        "token_expiry": user_data.get("token_expiry"),  # 日付はdatetimeオブジェクトまたはフォーマットされた文字列として渡す
    })
    return {"message": f"ユーザーデータがID {user_id} と共に追加されました"}

def get_user_data(user_id):
    """
    ユーザーIDに基づいてFirestoreからユーザーデータを取得する
    Parameters
    ----------
        user_id (str) : 取得するユーザーのID
    Returns
    ----------
        dict or None : ユーザーデータ（存在しない場合はNone）
    """

    # Firestoreからユーザーデータを取得
    user_ref = db.collection("users").document(user_id)
    user = user_ref.get()
    
    if user.exists:
        return user.to_dict()
    else:
        return None

def update_user_data(user_id, updated_data):
    """
    ユーザーIDに基づいてFirestoreのユーザーデータを更新する
    Parameters
    ----------
        user_id (str) : 更新するユーザーのID
        updated_data (dict) : 更新する新しいデータ
    Returns
    ----------
        dict : 更新操作の結果メッセージ
    """

    # ユーザーのドキュメント参照を取得
    user_ref = db.collection("users").document(user_id)
    
    # ユーザーデータを更新
    user_ref.update(updated_data)
    return {"message": f"ID {user_id} のユーザーデータが正常に更新されました"}

def delete_user_data(user_id):
    """
    ユーザーIDに基づいてFirestoreのユーザーデータを削除する
    Parameters
    ----------
        user_id (str) : 削除するユーザーのID
    Returns
    ----------
        dict : 削除操作の結果メッセージ
    """
    
    # ユーザーのドキュメント参照を取得
    user_ref = db.collection("users").document(user_id)
    
    # ユーザーデータを削除
    user_ref.delete()
    return {"message": f"ID {user_id} のユーザーデータが削除されました"}

