# services/firestore/firestore_connection.py

from config import Config

import firebase_admin
from firebase_admin import credentials, firestore

# Firebaseの初期化
cred = credentials.Certificate(Config.firebase_json_path)
firebase_admin.initialize_app(cred)

# Firestoreインスタンスの取得
db = firestore.client()