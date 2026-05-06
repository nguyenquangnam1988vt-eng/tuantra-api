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

    cred_data = json.loads(cred_json)

    firebase_admin.initialize_app(
        credentials.Certificate(cred_data),
        {"databaseURL": db_url}
    )
