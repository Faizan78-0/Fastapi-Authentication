from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth_router
from app.routers import users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(users_router.router)
