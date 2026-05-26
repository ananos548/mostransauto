from pydantic import BaseModel


class DriverSchema(BaseModel):
    full_name: str
    phone: str
    category: str
    experience: int
