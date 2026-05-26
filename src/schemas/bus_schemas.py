from typing import Optional

from pydantic import BaseModel

class BusSchema(BaseModel):
    number: str
    model: str
    brand: str
    year: int
    mileage: int
    status: str
    vin: str
    depot_id: int | None = None
    image_url: str | None = None
