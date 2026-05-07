from fastapi import Header, HTTPException, Depends
from firebase_admin import auth
from api.firebase import init_firebase


async def verify_token(authorization: str = Header(None)):
    init_firebase()

    if not authorization:
        raise HTTPException(401, "Missing Authorization header")

    try:
        parts = authorization.split(" ")

        if len(parts) != 2:
            raise Exception(f"Invalid auth format: {authorization}")

        scheme, token = parts

        if scheme.lower() != "bearer":
            raise Exception("Authorization must start with Bearer")

        decoded = auth.verify_id_token(token)

        return decoded

    except Exception as e:
        print("❌ VERIFY ERROR:", repr(e))
        raise HTTPException(401, f"Invalid token: {str(e)}")


async def get_user_role(decoded_token=Depends(verify_token)):
    role = decoded_token.get("role")

    if not role:
        raise HTTPException(403, "Role not found")

    return role
