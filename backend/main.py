from fastapi import FastAPI
from app.routes.address import router as address_router
from app.routes.vendor import router as vendor_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes.order import router as order_router
from app.routes.auth import router as auth_router
from app.database.database import Base, engine
from app.models import *
from app.routes.category import router as category_router
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter
from app.routes.product import router as product_router
from app.routes.admin import router as admin_router
from app.routes.cart import router as cart_router
from app.routes.payment import router as payment_router
from app.routes.upload import router as upload_router
from app.routes.email import router as email_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgaramMart API",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
app.include_router(email_router)
app.include_router(order_router)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(admin_router)
app.include_router(cart_router)
app.include_router(payment_router)
app.include_router(upload_router)
app.include_router(vendor_router)
app.include_router(address_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://192.168.16.1:3000"
    ],
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