from fastapi import Header, HTTPException
from firebase_admin import auth
from api.firebase import init_firebase

async def verify_token(authorization: str = Header(None)):
    init_firebase()

    print("AUTH HEADER:", authorization)

    if not authorization:
        raise HTTPException(401, "Missing token")

    try:
        parts = authorization.split(" ")

        if len(parts) != 2:
            raise Exception(f"Bad auth format: {authorization}")

        token = parts[1]

        print("TOKEN START:", token[:20])

        decoded = auth.verify_id_token(token)

        print("TOKEN OK:", decoded.get("uid"))

        return decoded

    except Exception as e:
        print("❌ VERIFY ERROR:", str(e))
        raise HTTPException(401, f"Invalid token: {str(e)}")
