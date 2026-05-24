import logging
from fastapi import FastAPI
from models.base import Base
from models.user import User
from models.todo import Todo
from database import engine
from routes import users_routes
from routes import auth_route
from routes import cloudinary_routes
from routes import todos_routes
from routes import guest_routes
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)

app = FastAPI(
    title = "Todos App",
    version = "0.0.1",
    description = "Todos App"
    )

app.include_router(users_routes.router)
app.include_router(auth_route.router)
app.include_router(todos_routes.router)
app.include_router(guest_routes.router)
app.include_router(cloudinary_routes.router)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"), 
    https_only=False,
)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get('/home')
def home():
    return {
        "status": "success",
        "message": "What's everyone working on today?"
    }