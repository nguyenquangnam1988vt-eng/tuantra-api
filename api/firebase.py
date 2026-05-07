import os
import json
import firebase_admin
from firebase_admin import credentials, db

def init_firebase():
    if firebase_admin._apps:
        return

    print("🚀 Init Firebase...")

    cred_json = os.getenv("FIREBASE_CRED_JSON")
    if not cred_json:
        raise Exception("❌ Missing FIREBASE_CRED_JSON")

    try:
        cred_dict = json.loads(cred_json)

        print("📦 Firebase project:", cred_dict.get("project_id"))
        print("PROJECT:", cred_dict.get("project_id"))

        cred = credentials.Certificate(cred_dict)

        firebase_admin.initialize_app(cred, {
            "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
        })

        print("✅ Firebase init SUCCESS")

    except Exception as e:
        print("❌ Firebase init ERROR:", str(e))
        raise
