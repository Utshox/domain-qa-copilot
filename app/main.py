from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import endpoints as auth_endpoints
from app.api.ingestion import endpoints as ingestion_endpoints
from app.api.query import endpoints as query_endpoints
from app.api.feedback import endpoints as feedback_endpoints
from app.core.config import settings
from app.db.session import engine, Base

# Create tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create tables. Database might be unavailable: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_endpoints.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(ingestion_endpoints.router, prefix=f"{settings.API_V1_STR}/ingest", tags=["ingestion"])
app.include_router(query_endpoints.router, prefix=f"{settings.API_V1_STR}/query", tags=["query"])
app.include_router(feedback_endpoints.router, prefix=f"{settings.API_V1_STR}/feedback", tags=["feedback"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Domain Q&A Copilot API"}
