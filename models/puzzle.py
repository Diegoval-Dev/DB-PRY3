# models/puzzle.py

from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime
from bson import ObjectId

class Puzzle(BaseModel):
    id: str = Field(default=None, alias="_id")
    name: str
    totalPieces: int
    sectors: List[str]
    createdAt: datetime

    @field_validator("id", mode="before")
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        allow_population_by_field_name = True
        json_encoders = { ObjectId: lambda oid: str(oid) }
