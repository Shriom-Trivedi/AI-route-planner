from fastapi import FastAPI
from app.routes import calculate_route

app = FastAPI()

app.include_router(calculate_route.router)