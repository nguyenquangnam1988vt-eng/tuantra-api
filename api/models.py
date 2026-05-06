from pydantic import BaseModel

class EncryptedRequest(BaseModel):
    data: str

class OfficerUpdateData(BaseModel):
    lat: float
    lng: float
    name: str
    lastUpdate: int
    # có thể thêm các field khác

class UserUpdateData(BaseModel):
    name: str
    role: str
    color: str
    last_seen: int

class TacticalPlanData(BaseModel):
    plan_id: str
    markers: list
    is_active: bool = True

class ArrowLogData(BaseModel):
    from_uid: str
    to_uid: str
    coordinates: list
    timestamp: int

class TrackData(BaseModel):
    uid: str
    lat: float
    lng: float
    timestamp: int
