from fastapi import FastAPI

from api.routes.alerts import router as alerts
from api.routes.incidents import router as incidents
from api.routes.markers import router as markers
from api.firebase import init_firebase
from api.routes import officers, users, tactical_plans, arrow_logs, tracks

app = FastAPI()

init_firebase()

app.include_router(alerts)
app.include_router(incidents)
app.include_router(markers)
app.include_router(officers.router)
app.include_router(users.router)
app.include_router(tactical_plans.router)
app.include_router(arrow_logs.router)
app.include_router(tracks.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
