from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

#from app.database import Base, engine
from app.routers import auth_router
from app.routers import users_router
from app.routers import posts_router
from app.middleware import logging_middleware

#Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(logging_middleware)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(posts_router.router)




@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}