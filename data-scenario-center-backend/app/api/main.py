from fastapi import APIRouter

from app.api.routes import DataScenarioRouter
from app.api.routes import ProjectRouter

api_router = APIRouter()
api_router.include_router(ProjectRouter.router)
