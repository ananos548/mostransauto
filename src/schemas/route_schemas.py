# src/schemas/route_schemas.py

from pydantic import BaseModel


class RouteSchema(BaseModel):
    name: str
    start_point: str
    end_point: str
