# models/piece.py
"""
Modelo de datos para una Pieza del rompecabezas.

Incluye validación de campos como código, sector, tipo de bordes y conexiones vecinas.
"""

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
        populate_by_name = True  # replaces allow_population_by_field_name
