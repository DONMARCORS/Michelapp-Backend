import logging
from dotenv import load_dotenv

import time
from pathlib import Path

from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.api.api_v1.api import api_router
from app.core.config import settings

LOG_CONFIG_FILE = "logging.conf"
# setup loggers
logging.config.fileConfig(LOG_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

root_router = APIRouter()
app = FastAPI(title="Michelapp API", openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@root_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    logger.debug("Root GET")
    return {"message": "Welcome to Michelapp API"}

# Example middleware, adds a time header to all responses
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")