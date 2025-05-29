# models/piece.py

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from bson import ObjectId

class Edge(BaseModel):
    edgeId: int
    type: str  # "hembra" o "macho"

class Neighbor(BaseModel):
    edgeId: int
    neighborCode: Optional[str]  # código de la pieza vecina, o None

class Piece(BaseModel):
    id: str = Field(default=None, alias="_id")
    puzzleId: str
    code: str
    sector: str
    edges: List[Edge]
    neighbors: List[Neighbor]

    @field_validator("id", "puzzleId", mode="before")
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        allow_population_by_field_name = True
