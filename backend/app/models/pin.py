from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class PinBase(BaseModel):
    """Base Pin model with common fields."""

    title: str
    description: str
    lat: float
    lng: float


class PinCreate(PinBase):
    """Pin model for creating a new pin."""

    pass


class PinInDB(PinBase):
    """Pin model as stored in the database."""

    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

    @classmethod
    def from_mongo(cls, data):
        """Convert MongoDB document to PinInDB model."""
        if data:
            data["id"] = str(data.pop("_id"))
            return cls(**data)
        return None


class Pin(PinInDB):
    """Pin model for API responses."""

    pass
