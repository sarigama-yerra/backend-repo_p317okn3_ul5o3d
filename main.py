from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import os

# Database helpers (MongoDB pre-configured)
from database import db, create_document, get_documents

app = FastAPI(title="API Marketplace Platform", version="0.1.0")

# CORS for local dev and preview environment
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "API Marketplace backend is running"}


@app.get("/test")
async def test_db():
    # Try simple no-op query to show connection info
    info = {
        "backend": "FastAPI",
        "database": "MongoDB",
        "database_url": os.getenv("DATABASE_URL", "(env not exposed)"),
        "database_name": os.getenv("DATABASE_NAME", "marketplace_db"),
        "connection_status": "connected",
        "collections": list(db.list_collection_names()) if db else [],
    }
    return info


class CreateApiListing(BaseModel):
    owner_id: str
    title: str
    slug: str
    description: str
    category: str
    tags: Optional[List[str]] = None


@app.post("/api/listings")
async def create_listing(payload: CreateApiListing):
    data = payload.dict()
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    # default fields
    data.update({
        "docs_url": None,
        "base_url": None,
        "rating": 0.0,
        "rating_count": 0,
    })
    inserted = await create_document("apilisting", data)
    return {"id": str(inserted.inserted_id), **data}


@app.get("/api/listings")
async def list_listings(q: Optional[str] = None, category: Optional[str] = None, limit: int = 20):
    filters = {}
    if q:
        # crude filter example - real impl would use text index
        filters["title"] = {"$regex": q, "$options": "i"}
    if category:
        filters["category"] = category
    docs = await get_documents("apilisting", filters, limit)
    # Convert ObjectId to string in a safe way
    results = []
    for d in docs:
        d["id"] = str(d.pop("_id", ""))
        results.append(d)
    return {"items": results}
