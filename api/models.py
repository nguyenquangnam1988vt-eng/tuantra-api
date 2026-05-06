from pydantic import BaseModel

class EncryptedRequest(BaseModel):
    data: str

class AlertModel(BaseModel):
    lat: float
    lng: float
    name: str

class IncidentModel(BaseModel):
    lat: float
    lng: float
    image_url: str

class MarkerModel(BaseModel):
    lat: float
    lng: float

class OfficerUpdateData(BaseModel):
    lat: float
    lng: float
    name: str
    lastUpdate: int

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
