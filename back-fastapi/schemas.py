from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CountTableBase(BaseModel):
    """Base schema for CountTable"""
    count_number: int
    description: Optional[str] = None


class CountTableCreate(CountTableBase):
    """Schema for creating a new count record"""
    pass


class CountTableUpdate(BaseModel):
    """Schema for updating a count record"""
    count_number: Optional[int] = None
    description: Optional[str] = None


class CountTableResponse(CountTableBase):
    """Schema for count record responses"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
