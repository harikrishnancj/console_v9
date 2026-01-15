
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import DATABASE_URL
from app.router import signup, tenantpurpose, market, userpurpose
from app.core.database import engine, Base

from .models import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Console API")

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signup.router, prefix="/auth")
app.include_router(tenantpurpose.router)
app.include_router(market.router)
app.include_router(userpurpose.router)