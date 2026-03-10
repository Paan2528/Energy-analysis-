from fastapi import FastAPI
from backend.api.routes import router
from backend.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Solar Energy API", version="5.0")
app.include_router(router)
