"""
Database Schemas for COVA Digital

Each Pydantic model represents a MongoDB collection (collection name = class name lowercased).
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class LeadIn(BaseModel):
    name: str = Field(..., description="Full name")
    message: str = Field(..., description="Inquiry message or context")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    business_name: Optional[str] = Field(None, description="Business/Company name")
    website: Optional[str] = Field(None, description="Website URL")
    need_help_with: Optional[str] = Field(None, description="Primary need e.g., Website, Reviews, Automation")

class LeadOut(LeadIn):
    id: str = Field(..., description="Document ID")
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
