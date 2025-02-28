from services.firestore import db
from google.cloud import firestore

def savePersonalKey(group_id, key):
    """
    
    groupIDに紐づかせてlineIDを保存する

    Parameters
    ----------
        group_id(str) : グループID
        key(str) : パーソナルキー

    Returns
    ----------
        bool : 

    """
    
    doc_ref = db.collection("groups").document(group_id)
    doc_ref.update({
        "users": firestore.ArrayUnion([key])
    })

def getMembersId(group_id):
    """
    
    グループIDからメンバーのLINE IDを取得

    Parameters
    ----------
        group_id(str) : group ID

    
    Returns
    ----------
        list : メンバーのユーザーIDのリスト

    
    """

    doc_ref = db.collection("groups").document(group_id)
    doc = doc_ref.get()

    line_ids = []

    if doc.exists:
        data = doc.to_dict()

        line_ids = data.get("users")

    return line_ids

def addNewGrop(group_id):
    """
    
    グループIDのドキュメントを作る

    """

    doc_ref = db.collection("groups").document(group_id)
    doc_ref.set({
        'users': []  # 空の配列
    }, merge=True) 