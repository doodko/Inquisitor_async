from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class SocialContact(BaseModel):
    name: str
    value: HttpUrl


class Establishment(BaseModel):
    id: int
    name: str
    slug: str
    altname: str | None = None
    description: str | None = None
    address: str | None = None
    hint: str | None = None
    tags: List[str]
    category: str
    location: str | None = None
    workhrs: str | None = None
    phone_numbers: List[str]
    social_contact: List[SocialContact]
    logo: Optional[HttpUrl]
    avg_rating: float
    total_votes: int
    created_at: datetime
    updated_at: datetime


class SearchResponse(BaseModel):
    count: int
    pages: int
    result: List[Establishment]
