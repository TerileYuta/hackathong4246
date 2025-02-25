# services/firestore/firestore_connection.py

import firebase_admin
from firebase_admin import credentials, firestore

# Firebaseの初期化
cred = credentials.Certificate("firebase-key.json")  # このパスを更新してください
firebase_admin.initialize_app(cred)

# Firestoreインスタンスの取得
db = firestore.client()