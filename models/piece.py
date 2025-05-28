# models/piece.py

from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class Edge(BaseModel):
    edgeId: int
    type: str  # "hembra" o "macho"

class Neighbor(BaseModel):
    edgeId: int
    neighborPiece: Optional[str]  # ObjectId como str o None

class Piece(BaseModel):
    """
    Representa el documento de la colección `pieces`.
    """
    id: str = Field(None, alias="_id")
    puzzleId: str
    code: str
    sector: str
    edges: List[Edge]
    neighbors: List[Neighbor]

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }
