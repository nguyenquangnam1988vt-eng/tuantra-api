from pydantic import BaseModel

class AlertModel(BaseModel):
    lat: float
    lng: float
    name: str

class MarkerModel(BaseModel):
    lat: float
    lng: float

class IncidentModel(BaseModel):
    lat: float
    lng: float
    image_url: str
