from pydantic import BaseModel
from typing import Optional


class RepairSchema(BaseModel):
    bus_id: int
    description: str
    cost: float = 0
    status: str
