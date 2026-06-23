from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.database.database import Base, engine
from app.models import *
from app.routes.category import router as category_router
from app.routes.product import router as product_router
from app.routes.admin import router as admin_router
from app.routes.cart import router as cart_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgaramMart API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(admin_router)
app.include_router(cart_router)
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