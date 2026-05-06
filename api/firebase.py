import os
import json
import firebase_admin
from firebase_admin import credentials, db

def init_firebase():
    if firebase_admin._apps:
        return

    cred_json = os.getenv("FIREBASE_CRED_JSON")
    if not cred_json:
        raise Exception("Missing FIREBASE_CRED_JSON")

    cred = credentials.Certificate(json.loads(cred_json))

    firebase_admin.initialize_app(cred, {
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
    })
