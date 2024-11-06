from fastapi import FastAPI
from app.routers.route_users import router as users_router

app = FastAPI()

app.include_router(users_router, prefix="/users",tags=["Users Management"])
