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
