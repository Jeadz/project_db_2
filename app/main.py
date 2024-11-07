from fastapi import FastAPI
from app.routers.router_users import router as users_router
from app.routers.router_tables import router as table_router

app = FastAPI()

app.include_router(users_router, prefix="/users",tags=["Users Management"])
app.include_router(table_router, prefix="/tables", tags=["Table Management"])