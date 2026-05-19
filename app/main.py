from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

#from app.database import Base, engine
from app.routers import auth_router
from app.routers import users_router
from app.routers import posts_routs

#Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(posts_routs.router)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    print(f"{request.method} {request.url} - {process_time:.4f}s")

    return response

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}