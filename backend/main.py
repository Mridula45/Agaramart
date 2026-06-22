from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.models import *

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgaramMart API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "application": "AgaramMart",
        "version": "1.0.0",
        "status": "Running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }