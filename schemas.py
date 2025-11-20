from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


# NOTE: Each Pydantic model below represents a MongoDB collection.
# Collection name = class name lowercased (e.g., ApiListing -> "apilisting").


class User(BaseModel):
    email: str
    password_hash: str
    role: str = Field(default="buyer", description="buyer | seller | admin")
    name: Optional[str] = None
    verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ApiListing(BaseModel):
    owner_id: str
    title: str
    slug: str
    description: str
    category: str
    docs_url: Optional[HttpUrl] = None
    base_url: Optional[HttpUrl] = None
    tags: List[str] = []
    rating: float = 0.0
    rating_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Plan(BaseModel):
    api_id: str
    name: str
    price_cents: int
    billing_cycle: str = Field(description="one_time | monthly | yearly")
    per_minute_limit: int = 60
    monthly_quota: int = 10000
    features: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Subscription(BaseModel):
    user_id: str
    api_id: str
    plan_id: str
    api_key: Optional[str] = None
    active: bool = True
    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Review(BaseModel):
    user_id: str
    api_id: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UsageLog(BaseModel):
    subscription_id: str
    endpoint: str
    method: str
    status_code: int
    latency_ms: int
    created_at: Optional[datetime] = None

