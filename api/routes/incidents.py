@router.post("/")
async def create_incident(enc: EncryptedRequest, user=Depends(verify_token)):
    uid = user["uid"]

    data = json.loads(decrypt_message(enc.data))

    db.reference("incidents").push({
        "lat": data["lat"],
        "lng": data["lng"],
        "image_url": data["image_url"],
        "created_by": uid,
        "timestamp": int(time.time() * 1000)
    })

    return {"success": True}
