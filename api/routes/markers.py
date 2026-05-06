@router.post("/")
async def create_marker(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]

    data = json.loads(decrypt_message(enc.data))

    db.reference(f"markers/{uid}").push({
        "lat": data["lat"],
        "lng": data["lng"],
        "created_by": uid,
        "timestamp": int(time.time() * 1000)
    })

    return {"success": True}
