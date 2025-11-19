from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

# Each Pydantic model corresponds to a Mongo collection with the lowercase class name


class Lead(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, description="E164 or local format")
    business_name: Optional[str] = None
    website: Optional[str] = None
    message: str = Field(..., min_length=3, max_length=2000)
    need_help_with: Optional[Literal["Website", "Reviews", "Automation", "Not sure"]] = None


class LeadIn(Lead):
    pass


class LeadOut(Lead):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
