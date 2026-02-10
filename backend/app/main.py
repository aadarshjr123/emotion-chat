from fastapi import FastAPI
from app.api import auth_routes, websocket_routes, health, metrics_routes
from app.core.database import Base, engine
from app.api import auth_routes, websocket_routes, user_routes
from fastapi.middleware.cors import CORSMiddleware
from app.api import message_routes
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Emotion Chat Backend")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allowed origins
    allow_credentials=True,  # allow cookies/authorization headers
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # allow all headers
)

app.include_router(auth_routes.router)
app.include_router(health.router)
app.include_router(metrics_routes.router)
app.include_router(websocket_routes.router)
app.include_router(user_routes.router)
app.include_router(message_routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
