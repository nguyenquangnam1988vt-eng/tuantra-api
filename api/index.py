import os
import json
import firebase_admin
from firebase_admin import credentials, db
from fastapi import FastAPI, Depends
from dotenv import load_dotenv

from api.routes import alerts, markers, incidents

load_dotenv()

# --- Init Firebase ---
if not firebase_admin._apps:
    cred_json = os.getenv("FIREBASE_CRED_JSON")

    if not cred_json:
        raise Exception("Missing FIREBASE_CRED_JSON")

    cred = credentials.Certificate(json.loads(cred_json))

    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
    })

app = FastAPI()

app.include_router(alerts.router)
app.include_router(markers.router)
app.include_router(incidents.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}
