from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from .routers import healthz, today, version

app = FastAPI()


app.include_router(healthz.router)
app.include_router(today.router)
app.include_router(version.router)


@app.get("/")
async def root():
    return {"message": "Hello world from API root!"}


Instrumentator().instrument(app).expose(app)
