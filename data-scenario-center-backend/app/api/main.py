from app.api.routes import DataScenarioRouter
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(DataScenarioRouter.router)
