from fastapi import APIRouter

from . import timetable

routers = APIRouter()

routers.include_router(timetable.router, prefix="/timetable")
