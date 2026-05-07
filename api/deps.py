from fastapi import Header, HTTPException
from firebase_admin import auth
from api.firebase import init_firebase

async def verify_token(authorization: str = Header(None)):
    init_firebase()

    print("📩 RAW AUTH HEADER:", authorization)

    if not authorization:
        raise HTTPException(401, "Missing token")

    try:
        parts = authorization.split(" ")

        # 🔥 thêm check an toàn
        if len(parts) != 2:
            print("❌ AUTH FORMAT WRONG:", parts)
            raise HTTPException(401, "Invalid auth format")

        token = parts[1]

        print("🔑 TOKEN TO VERIFY:", token[:50], "...")

        decoded = auth.verify_id_token(token)

        # 🔥 LOG QUAN TRỌNG NHẤT
        print("👤 UID:", decoded.get("uid"))
        print("🏷️ AUD:", decoded.get("aud"))
        print("🔥 FIREBASE APP:", decoded.get("firebase"))

        return decoded

    except Exception as e:
        print("❌ VERIFY ERROR:", str(e))
        raise HTTPException(401, "Invalid token")


def get_user_role(uid: str):
    from firebase_admin import db
    init_firebase()

    role = db.reference(f"users/{uid}/role").get()
    return role or "officer"
