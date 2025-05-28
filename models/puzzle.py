# models/puzzle.py

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from bson import ObjectId

class Puzzle(BaseModel):
    """
    Representa el documento de la colección `puzzles`.
    """
    id: str = Field(None, alias="_id")
    name: str
    totalPieces: int
    sectors: List[str]
    createdAt: datetime

    class Config:
        # Permite usar el alias "_id" y convertir ObjectId a str automáticamente
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            datetime: lambda dt: dt.isoformat(),
        }
