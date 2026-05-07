from fastapi import Header, HTTPException
from firebase_admin import auth
from api.firebase import init_firebase

async def verify_token(authorization: str = Header(None)):
    init_firebase()
    print("📩 RAW AUTH HEADER:", authorization)  # 👈 THÊM DÒNG NÀY

    if not authorization:
        raise HTTPException(401, "Missing token")

    try:
        token = authorization.split(" ")[1]
        print("🔑 TOKEN TO VERIFY:", token)  # 👈 THÊM DÒNG NÀY
        return auth.verify_id_token(token)
    except:
        raise HTTPException(401, "Invalid token")


def get_user_role(uid: str):
    from firebase_admin import db
    init_firebase()

    role = db.reference(f"users/{uid}/role").get()
    return role or "officer"
