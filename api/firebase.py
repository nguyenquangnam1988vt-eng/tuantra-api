import os
import json
import firebase_admin
from firebase_admin import credentials

def init_firebase():
    if firebase_admin._apps:
        return

    cred_json = os.getenv("FIREBASE_CRED_JSON")
    db_url = os.getenv("FIREBASE_DATABASE_URL")

    if not cred_json:
        raise Exception("FIREBASE_CRED_JSON missing")
    if not db_url:
        raise Exception("FIREBASE_DATABASE_URL missing")

    cred = credentials.Certificate(json.loads(cred_json))

    firebase_admin.initialize_app(cred, {
        "databaseURL": db_url
    })
