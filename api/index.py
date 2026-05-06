from fastapi import FastAPI

from api.routes.alerts import router as alerts
from api.routes.incidents import router as incidents
from api.routes.markers import router as markers
from api.routes.officers import router as officers
from api.routes.users import router as users
from api.routes.tactical_plans import router as tactical_plans
from api.routes.arrow_logs import router as arrow_logs
from api.routes.tracks import router as tracks
from api.firebase import init_firebase
from api.routes.drawings import router as drawings 
from api.routes.special_points import router as special_points

app = FastAPI()

@app.on_event("startup")
def startup():
    init_firebase()

app.include_router(alerts)
app.include_router(incidents)
app.include_router(markers)
app.include_router(officers)
app.include_router(users)
app.include_router(tactical_plans)
app.include_router(arrow_logs)
app.include_router(drawings) 
app.include_router(special_points)

@app.get("/api/health")
async def health():
    return {"status": "ok"}
