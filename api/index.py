from fastapi import FastAPI

from api.routes.alerts import router as alerts
from api.routes.incidents import router as incidents
from api.routes.markers import router as markers

app = FastAPI()

app.include_router(alerts)
app.include_router(incidents)
app.include_router(markers)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
